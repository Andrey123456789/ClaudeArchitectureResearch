#!/usr/bin/env python3
"""Stage A primary-extraction builder (Claude primary extractor tooling).

Converts hand-written per-batch annotation files (a compact line DSL) under
stage_A/primary/<cand>/_work/annot/*.txt into the mandated Stage A ledgers:
files.jsonl, coverage_ranges.jsonl, constraints.jsonl, policies.jsonl,
ORPHAN_CANDIDATES.jsonl, EXTRA_CONSTRAINTS.md, PROGRESS.json (+ stats JSON).

It never writes outside stage_A/primary/<cand>/. It reads inputs read-only.
All semantic judgements live in the annotation files; this tool only does
deterministic bookkeeping: ID assignment (stable registry), quote extraction and
verification, backlinks, coverage checks and counting.

DSL (one directive per line, '#' comment lines ignored):
  @@ <path under inputs/<cand>/> [;; scan note]
  @scope <default trigger scope for following C lines in this file>
  <a>[-<b>] <OL|EX|LU|MX|NN|IM|DU> [refs] ;; <reason> [;; <quote substring>]
  C <label> <OL|EX|LU> <PID,PID|-> <modality> ;; <action> ;; <scope|=> ;; <exceptions> ;; <why>
  O <a>[-<b>] <EX|PL|LU|NN|DU> [refs] ;; <reason> ;; <specific behavior> [;; <quote>]
refs are written as [label1,label2]. Omitted quote => full verbatim range text.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

DISP = {'OL': 'ORACLE_LINKED', 'EX': 'EXTRA', 'LU': 'LINK_UNCERTAIN', 'MX': 'MIXED',
        'NN': 'NON_NORMATIVE', 'IM': 'IMPLEMENTATION', 'DU': 'DUPLICATE'}
ORIG = {'OL': 'ORACLE_LINKED', 'EX': 'EXTRA', 'LU': 'LINK_UNCERTAIN'}
ORES = {'EX': 'EXTRA_REGISTERED', 'PL': 'POLICY_LINKED', 'LU': 'LINK_UNCERTAIN',
        'NN': 'NON_NORMATIVE', 'DU': 'DUPLICATE'}
STATUS = {'MATCHED', 'PARTIAL', 'NOT_EVIDENCED', 'UNCERTAIN'}
RANGE_RE = re.compile(r'^(\d+)(?:-(\d+))?\s+([A-Z]{2})\s*(\[[^\]]*\])?\s*$')


class Fail(Exception):
    pass


def src_lines(path):
    data = path.read_bytes()
    if b'\x00' in data:
        return None
    try:
        return data.decode('utf-8-sig').splitlines()
    except UnicodeDecodeError:
        return None


def oracle(root, cand):
    c = root / 'inputs' / cand / 'source'
    inv = json.loads((c / 'inventory.json').read_text(encoding='utf-8-sig'))
    sh = json.loads((c / 'shared-research-invariants.json').read_text(encoding='utf-8-sig'))
    ids = [p['id'] for g in inv['policygroups'] for p in g['policies']]
    ids += [i['id'] for i in sh['invariants']]
    return ids


def parse_refs(tok):
    if not tok:
        return []
    inner = tok.strip()[1:-1]
    return [x.strip() for x in inner.split(',') if x.strip()]


def parse(root, cand, errors):
    work = root / 'stage_A' / 'primary' / cand / '_work'
    annot_dir = work / 'annot'
    files = OrderedDict()   # path -> dict(note, segs, orphans)
    cons = OrderedDict()    # label -> dict
    if not annot_dir.is_dir():
        return files, cons
    for af in sorted(annot_dir.glob('*.txt')):
        cur = None
        scope = ''
        for n, raw in enumerate(af.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.rstrip()
            loc = f'{af.name}:{n}'
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            try:
                if line.startswith('@@+'):
                    # re-open an already declared file section (reverse-sweep additions)
                    p = line[3:].split(';;', 1)[0].strip()
                    if p not in files:
                        raise Fail(f'@@+ re-opens undeclared file section: {p}')
                    cur = p
                    scope = ''
                elif line.startswith('@@'):
                    body = line[2:].strip()
                    parts = body.split(';;', 1)
                    p = parts[0].strip()
                    note = parts[1].strip() if len(parts) > 1 else ''
                    if p in files:
                        raise Fail(f'file section repeated: {p}')
                    files[p] = {'note': note, 'segs': [], 'orphans': [], 'src': loc}
                    cur = p
                    scope = ''
                elif line.startswith('@scope'):
                    scope = line[len('@scope'):].strip()
                elif line.startswith('C '):
                    head, *rest = line[2:].split(';;')
                    hp = head.split()
                    if len(hp) < 4:
                        raise Fail('C needs: label origin pids modality')
                    label, og, pids, modality = hp[0], hp[1], hp[2], ' '.join(hp[3:])
                    if og not in ORIG:
                        raise Fail(f'bad origin {og}')
                    if label in cons:
                        raise Fail(f'constraint label redefined: {label}')
                    rest = [r.strip() for r in rest] + [''] * 5
                    action, tscope, exc, why = rest[0], rest[1], rest[2], rest[3]
                    if tscope in ('', '='):
                        tscope = scope
                    cons[label] = {'label': label, 'origin': ORIG[og],
                                   'pids': [] if pids == '-' else [x for x in pids.split(',') if x],
                                   'modality': modality, 'action': action, 'scope': tscope,
                                   'exceptions': exc or 'none stated', 'why': why, 'loc': loc,
                                   'file': cur}
                elif line.startswith('O '):
                    if cur is None:
                        raise Fail('O outside file section')
                    head, *rest = line[2:].split(';;', 3)
                    m = RANGE_RE.match(head.strip())
                    if not m:
                        raise Fail(f'bad O head: {head}')
                    a = int(m.group(1)); b = int(m.group(2) or m.group(1))
                    res = m.group(3)
                    if res not in ORES:
                        raise Fail(f'bad orphan resolution {res}')
                    rest = [r.strip() for r in rest] + ['', '', '']
                    files[cur]['orphans'].append({'a': a, 'b': b, 'res': res, 'refs': parse_refs(m.group(4)),
                                                  'reason': rest[0], 'behavior': rest[1],
                                                  'quote': rest[2] if len(rest) > 2 else '', 'loc': loc})
                else:
                    if cur is None:
                        raise Fail('segment outside file section')
                    head, *rest = line.split(';;', 2)
                    m = RANGE_RE.match(head.strip())
                    if not m:
                        raise Fail(f'bad segment head: {head!r}')
                    a = int(m.group(1)); b = int(m.group(2) or m.group(1))
                    d = m.group(3)
                    if d not in DISP:
                        raise Fail(f'bad disposition {d}')
                    reason = rest[0].strip() if rest else ''
                    quote = rest[1].strip() if len(rest) > 1 else ''
                    files[cur]['segs'].append({'a': a, 'b': b, 'd': d, 'refs': parse_refs(m.group(4)),
                                               'reason': reason, 'quote': quote, 'loc': loc})
            except Fail as e:
                errors.append(f'{loc}: {e}')
    return files, cons


def load_registry(work):
    p = work / 'ids.json'
    if p.is_file():
        return json.loads(p.read_text(encoding='utf-8'))
    return {'constraints': {}, 'segments': {}, 'orphans': {}, 'counters': {}}


def next_id(reg, kind, prefix, width):
    c = reg['counters'].get(prefix, 0) + 1
    reg['counters'][prefix] = c
    return f'{prefix}{c:0{width}d}'


def build(root, cand, complete=None, write=True, quiet=False):
    errors, warnings = [], []
    out = root / 'stage_A' / 'primary' / cand
    work = out / '_work'
    snap = root / 'inputs' / cand
    queue = json.loads((root / 'stage_A' / '_control' / f'{cand}_WORK_QUEUE.json').read_text(encoding='utf-8'))
    qfiles = {f['path']: f for f in queue['files']}
    order = {f['path']: i for i, f in enumerate(queue['files'])}
    ids = oracle(root, cand)
    idset = set(ids)
    files, cons = parse(root, cand, errors)
    reg = load_registry(work)

    # --- sources
    texts = {}
    for p in files:
        if p not in qfiles:
            errors.append(f'annotated file not in queue: {p}')
            continue
        lines = src_lines(snap / p)
        if lines is None:
            errors.append(f'annotated file is not UTF-8 text: {p}')
            continue
        texts[p] = lines

    # --- constraints referenced
    used = defaultdict(list)  # label -> [(path, segidx)]
    seg_rows = []
    for p in sorted(texts, key=lambda x: order[x]):
        lines = texts[p]
        segs = sorted(files[p]['segs'], key=lambda s: (s['a'], s['b']))
        covered = {}
        for s in segs:
            a, b = s['a'], s['b']
            if a < 1 or b < a or b > len(lines):
                errors.append(f'{s["loc"]}: range {a}-{b} out of bounds for {p} ({len(lines)} lines)')
                continue
            for i in range(a, b + 1):
                if i in covered:
                    errors.append(f'{s["loc"]}: overlap at {p}:{i} with {covered[i]}')
                covered[i] = s['loc']
            text = '\n'.join(lines[a - 1:b])
            if not text.strip():
                errors.append(f'{s["loc"]}: range {a}-{b} is entirely blank')
            d = s['d']
            norm = d in ('OL', 'EX', 'LU', 'MX')
            q = s['quote']
            if norm:
                if not q:
                    q = text.strip()
                elif q not in text:
                    errors.append(f'{s["loc"]}: quote not found in {p}:{a}-{b}: {q[:80]!r}')
                if not s['refs']:
                    errors.append(f'{s["loc"]}: normative segment without refs')
            else:
                if q and q not in text:
                    errors.append(f'{s["loc"]}: quote not found in {p}:{a}-{b}: {q[:80]!r}')
            if d in ('NN', 'IM', 'DU', 'LU', 'MX') and not s['reason']:
                errors.append(f'{s["loc"]}: disposition {d} requires reason')
            origins = set()
            for r in s['refs']:
                if r not in cons:
                    errors.append(f'{s["loc"]}: unknown constraint label {r}')
                    continue
                origins.add(cons[r]['origin'])
                if d in ('OL', 'EX', 'LU') and cons[r]['origin'] != DISP[d]:
                    errors.append(f'{s["loc"]}: {d} segment refs {r} with origin {cons[r]["origin"]}')
            if d == 'MX' and len(origins) < 2:
                errors.append(f'{s["loc"]}: MIXED segment must link >=2 constraint origins (has {origins})')
            if d in ('NN', 'IM') and s['refs']:
                errors.append(f'{s["loc"]}: {d} segment must not link constraints')
            key = f'{p}|{a}|{b}'
            sid = reg['segments'].get(key)
            if sid is None:
                sid = next_id(reg, 'seg', f'{cand}-S', 6)
                reg['segments'][key] = sid
            row = OrderedDict([('segment_id', sid), ('path', p), ('start_line', a), ('end_line', b),
                               ('disposition', DISP[d]),
                               ('constraint_ids', s['refs'][:]),
                               ('quote', q if (norm or q) else ''),
                               ('reason', s['reason'])])
            seg_rows.append(row)
            for r in s['refs']:
                used[r].append(sid)
        for i, line in enumerate(lines, 1):
            if line.strip() and i not in covered:
                errors.append(f'UNCOVERED {p}:{i}: {line.strip()[:70]}')

    # --- constraint ids
    lab2id = {}
    for lab, c in cons.items():
        cid = reg['constraints'].get(lab)
        if cid is None:
            prefix = {'ORACLE_LINKED': f'RULE-{cand}-', 'EXTRA': f'EXTRA-{cand}-',
                      'LINK_UNCERTAIN': f'UNCERTAIN-{cand}-'}[c['origin']]
            cid = next_id(reg, 'con', prefix, 4)
            reg['constraints'][lab] = cid
        expected_prefix = {'ORACLE_LINKED': 'RULE-', 'EXTRA': 'EXTRA-', 'LINK_UNCERTAIN': 'UNCERTAIN-'}[c['origin']]
        if not cid.startswith(expected_prefix):
            errors.append(f'{c["loc"]}: label {lab} registered as {cid} but origin is now {c["origin"]}; rename label')
        lab2id[lab] = cid
        for pid in c['pids']:
            if pid not in idset:
                errors.append(f'{c["loc"]}: unknown policy id {pid}')
        if c['origin'] == 'ORACLE_LINKED' and not c['pids']:
            errors.append(f'{c["loc"]}: ORACLE_LINKED constraint {lab} without policy ids')
        if c['origin'] in ('EXTRA', 'LINK_UNCERTAIN') and not c['why']:
            errors.append(f'{c["loc"]}: {c["origin"]} constraint {lab} missing why/question')
        if not c['action']:
            errors.append(f'{c["loc"]}: constraint {lab} missing action')
        if lab not in used:
            errors.append(f'{c["loc"]}: constraint {lab} has no evidence segment')

    for row in seg_rows:
        row['constraint_ids'] = [lab2id.get(r, r) for r in row['constraint_ids']]
    sid_by_key = {f"{r['path']}|{r['start_line']}|{r['end_line']}": r for r in seg_rows}

    con_rows = []
    for lab, c in cons.items():
        con_rows.append(OrderedDict([
            ('id', lab2id[lab]), ('origin', c['origin']), ('policy_ids', c['pids']),
            ('normative_action', c['action']), ('modality', c['modality']),
            ('trigger_scope', c['scope']), ('exceptions', c['exceptions']),
            ('evidence_segment_ids', sorted(set(used.get(lab, [])))),
            ('why_extra_or_uncertain', c['why'] if c['origin'] != 'ORACLE_LINKED' else (c['why'] or ''))]))
    con_by_id = {r['id']: r for r in con_rows}

    # --- orphans
    orphan_rows = []
    explicit_refs = set()
    for p in sorted(texts, key=lambda x: order[x]):
        lines = texts[p]
        for o in files[p]['orphans']:
            a, b = o['a'], o['b']
            if a < 1 or b < a or b > len(lines):
                errors.append(f'{o["loc"]}: orphan range out of bounds')
                continue
            text = '\n'.join(lines[a - 1:b])
            q = o['quote'] or text.strip()
            if q not in text:
                errors.append(f'{o["loc"]}: orphan quote not found: {q[:80]!r}')
            for r in o['refs']:
                if r not in cons:
                    errors.append(f'{o["loc"]}: orphan unknown ref {r}')
            res = ORES[o['res']]
            want = {'EXTRA_REGISTERED': 'EXTRA', 'POLICY_LINKED': 'ORACLE_LINKED', 'LINK_UNCERTAIN': 'LINK_UNCERTAIN'}.get(res)
            for r in o['refs']:
                if r in cons and want and cons[r]['origin'] != want:
                    errors.append(f'{o["loc"]}: orphan {res} ref {r} has origin {cons[r]["origin"]}')
            if res in ('EXTRA_REGISTERED', 'POLICY_LINKED', 'LINK_UNCERTAIN') and not o['refs']:
                errors.append(f'{o["loc"]}: operative orphan without refs')
            if res == 'NON_NORMATIVE' and o['refs']:
                errors.append(f'{o["loc"]}: NON_NORMATIVE orphan must not link constraints')
            if not o['reason']:
                errors.append(f'{o["loc"]}: orphan missing reason')
            if res in ('EXTRA_REGISTERED', 'LINK_UNCERTAIN') and not o['behavior']:
                errors.append(f'{o["loc"]}: orphan missing specific behavior')
            if res != 'DUPLICATE':
                explicit_refs.update(o['refs'])
            key = f'x|{p}|{a}|{b}|{o["res"]}|{",".join(o["refs"])}'
            oid = reg['orphans'].get(key)
            if oid is None:
                oid = next_id(reg, 'orph', f'ORPHAN-{cand}-', 4)
                reg['orphans'][key] = oid
            closest = sorted({pid for r in o['refs'] if r in cons for pid in cons[r]['pids']})
            orphan_rows.append(OrderedDict([
                ('id', oid), ('candidate', cand), ('path', p), ('start_line', a), ('end_line', b),
                ('quote', q), ('resolution', res), ('constraint_ids', [lab2id.get(r, r) for r in o['refs']]),
                ('closest_policy_ids', closest), ('reason', o['reason']),
                ('specific_behavior', o['behavior'] or '')]))
    for lab, c in cons.items():
        if c['origin'] not in ('EXTRA', 'LINK_UNCERTAIN') or lab in explicit_refs:
            continue
        sids = sorted(set(used.get(lab, [])))
        if not sids:
            continue
        # first evidence segment in source order
        segs = [r for r in seg_rows if r['segment_id'] in sids]
        segs.sort(key=lambda r: (order.get(r['path'], 1e9), r['start_line']))
        s = segs[0]
        key = f'auto|{lab}'
        oid = reg['orphans'].get(key)
        if oid is None:
            oid = next_id(reg, 'orph', f'ORPHAN-{cand}-', 4)
            reg['orphans'][key] = oid
        res = 'EXTRA_REGISTERED' if c['origin'] == 'EXTRA' else 'LINK_UNCERTAIN'
        also = ''
        if len(segs) > 1:
            also = ' Also evidenced at: ' + '; '.join(f"{r['path']}:{r['start_line']}-{r['end_line']}" for r in segs[1:])
        orphan_rows.append(OrderedDict([
            ('id', oid), ('candidate', cand), ('path', s['path']), ('start_line', s['start_line']),
            ('end_line', s['end_line']), ('quote', s['quote']), ('resolution', res),
            ('constraint_ids', [lab2id[lab]]), ('closest_policy_ids', c['pids']),
            ('reason', c['why'] + also), ('specific_behavior', c['action'])]))
    orphan_rows.sort(key=lambda r: r['id'])

    # --- policies
    pol_rows = []
    pfile = work / 'policies.txt'
    pol_decl = OrderedDict()
    if pfile.is_file():
        for n, raw in enumerate(pfile.read_text(encoding='utf-8').splitlines(), 1):
            if not raw.strip() or raw.lstrip().startswith('#'):
                continue
            head, *rest = raw.split(';;', 1)
            hp = head.split()
            if len(hp) < 2 or hp[1] not in STATUS:
                errors.append(f'policies.txt:{n}: bad line')
                continue
            pid = hp[0]
            extra_labels = parse_refs(hp[2]) if len(hp) > 2 else []
            if pid in pol_decl:
                errors.append(f'policies.txt:{n}: duplicate {pid}')
            if pid not in idset:
                errors.append(f'policies.txt:{n}: unknown policy {pid}')
            pol_decl[pid] = (hp[1], rest[0].strip() if rest else '', extra_labels)
    for pid in ids:
        ol = [lab for lab, c in cons.items() if pid in c['pids'] and c['origin'] == 'ORACLE_LINKED']
        ex = [lab for lab, c in cons.items() if pid in c['pids'] and c['origin'] != 'ORACLE_LINKED']
        if pid not in pol_decl:
            continue
        status, notes, extra_labels = pol_decl[pid]
        atomic = ol + [l for l in extra_labels if l not in ol]
        for l in extra_labels:
            if l not in cons or pid not in cons[l]['pids']:
                errors.append(f'policies.txt {pid}: extra label {l} unknown or not linked to policy')
        evid = sorted({sid for l in atomic if l in cons for sid in used.get(l, [])})
        if status == 'MATCHED' and not ol:
            errors.append(f'policies.txt {pid}: MATCHED without ORACLE_LINKED constraint')
        if status == 'NOT_EVIDENCED' and ol:
            errors.append(f'policies.txt {pid}: NOT_EVIDENCED but has ORACLE_LINKED constraints {ol}')
        if not notes:
            errors.append(f'policies.txt {pid}: missing search notes')
        rel = [lab2id[l] for l in ex if l not in extra_labels]
        if rel:
            notes = notes + f' Related non-oracle constraints referencing this policy as closest: {", ".join(rel)}.'
        pol_rows.append(OrderedDict([('rule_id', pid), ('status', status),
                                     ('atomic_constraint_ids', [lab2id[l] for l in atomic if l in lab2id]),
                                     ('evidence_segment_ids', evid), ('search_notes', notes)]))
    missing_pol = [pid for pid in ids if pid not in pol_decl]

    # --- files.jsonl
    file_rows = []
    for f in queue['files']:
        p = f['path']
        if p not in files and f['type'] == 'text':
            continue
        lines = texts.get(p)
        note = files.get(p, {}).get('note', '')
        if f['type'] == 'binary':
            file_rows.append(OrderedDict([('path', p), ('type', 'binary'), ('encoding', None),
                                          ('scan_notes', note or 'binary/non-UTF-8; not decoded')]))
            continue
        nb = sum(1 for x in lines if x.strip()) if lines else 0
        segs = [r for r in seg_rows if r['path'] == p]
        dc = Counter(r['disposition'] for r in segs)
        auto = (f'{len(lines)} lines ({nb} nonblank) partitioned into {len(segs)} ranges: '
                + ', '.join(f'{k}={v}' for k, v in sorted(dc.items())) + '.')
        file_rows.append(OrderedDict([('path', p), ('type', 'text'), ('encoding', 'utf-8'),
                                      ('scan_notes', (note + ' ' if note else '') + auto)]))

    # --- progress / batch completeness
    annotated_complete = set()
    unc_by_file = Counter()
    for e in errors:
        if e.startswith('UNCOVERED '):
            unc_by_file[e.split(' ', 1)[1].rsplit(':', 2)[0]] += 1
    for p in texts:
        if unc_by_file.get(p, 0) == 0:
            annotated_complete.add(p)
    batch_ok = []
    hard_errors = [e for e in errors if not e.startswith('UNCOVERED ')]
    for bt in ([] if hard_errors else queue['batches']):
        if all((p in annotated_complete) or (qfiles[p]['type'] == 'binary') for p in bt['files']):
            batch_ok.append(bt['id'])

    stats = OrderedDict([
        ('candidate', cand), ('annotated_files', len(texts)), ('queue_files', len(queue['files'])),
        ('segments', len(seg_rows)), ('segment_dispositions', dict(Counter(r['disposition'] for r in seg_rows))),
        ('constraints', len(con_rows)), ('constraint_origins', dict(Counter(r['origin'] for r in con_rows))),
        ('orphans', len(orphan_rows)), ('orphan_resolutions', dict(Counter(r['resolution'] for r in orphan_rows))),
        ('policies_declared', len(pol_decl)), ('policy_status', dict(Counter(v[0] for v in pol_decl.values()))),
        ('batches_fully_annotated', batch_ok), ('errors', len(errors))])

    if write:
        out.mkdir(parents=True, exist_ok=True)
        work.mkdir(parents=True, exist_ok=True)
        (work / 'ids.json').write_text(json.dumps(reg, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        lab_map = {lab: lab2id[lab] for lab in cons}
        (work / 'label_map.json').write_text(json.dumps(lab_map, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')

        def wj(name, rows):
            (out / name).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
        wj('files.jsonl', file_rows)
        wj('coverage_ranges.jsonl', seg_rows)
        wj('constraints.jsonl', con_rows)
        wj('ORPHAN_CANDIDATES.jsonl', orphan_rows)
        if pol_rows:
            wj('policies.jsonl', pol_rows)
        write_extra_md(out, cand, con_rows, seg_rows)
        prog_p = out / 'PROGRESS.json'
        prog = json.loads(prog_p.read_text(encoding='utf-8')) if prog_p.is_file() else {
            'candidate': cand, 'completed_batch_ids': [], 'notes': ''}
        if complete:
            for bid in complete:
                if bid not in batch_ok:
                    errors.append(f'cannot mark {bid} complete: not fully annotated / has errors')
                elif bid not in prog['completed_batch_ids']:
                    prog['completed_batch_ids'].append(bid)
            prog['completed_batch_ids'].sort()
        prog['notes'] = (f'Batches checked: {len(prog["completed_batch_ids"])}/{len(queue["batches"])}. '
                         f'Annotation sources: _work/annot/*.txt; policy decisions: _work/policies.txt; '
                         f'stable IDs: _work/ids.json. Last build errors: {len(errors)}.')
        prog_p.write_text(json.dumps(prog, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        (work / 'build_stats.json').write_text(json.dumps(stats, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    stats['errors'] = len(errors)
    stats['missing_policy_decls'] = len(missing_pol)
    return stats, errors, warnings


def write_extra_md(out, cand, con_rows, seg_rows):
    seg = {r['segment_id']: r for r in seg_rows}
    lines = [f'# EXTRA and LINK_UNCERTAIN constraints — candidate {cand}', '',
             'Generated deterministically from the annotation ledger. Each entry cites the exact',
             'source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry',
             'name the closest oracle policy only; origin stays EXTRA.', '']
    for origin, title in (('EXTRA', 'EXTRA constraints'), ('LINK_UNCERTAIN', 'LINK_UNCERTAIN constraints')):
        rows = [r for r in con_rows if r['origin'] == origin]
        lines += [f'## {title} ({len(rows)})', '']
        for r in rows:
            lines.append(f'### {r["id"]}')
            lines.append(f'- Closest oracle policies: {", ".join(r["policy_ids"]) or "none"}')
            lines.append(f'- Modality: {r["modality"]}')
            lines.append(f'- Normative action: {r["normative_action"]}')
            lines.append(f'- Trigger/scope: {r["trigger_scope"]}')
            lines.append(f'- Exceptions: {r["exceptions"]}')
            lines.append(f'- {"Why EXTRA" if origin == "EXTRA" else "Open question"}: {r["why_extra_or_uncertain"]}')
            for sid in r['evidence_segment_ids']:
                s = seg[sid]
                q = s['quote'].replace('\n', ' ⏎ ')
                if len(q) > 400:
                    q = q[:400] + ' …'
                lines.append(f'- Evidence {sid}: `{s["path"]}:{s["start_line"]}-{s["end_line"]}` — "{q}"')
            lines.append('')
    (out / 'EXTRA_CONSTRAINTS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


NORM_RE = re.compile(r"\b(must|never|always|only|should|shall|do not|don't|avoid|prefer|require[sd]?|default|unless|except|forbid|block|deny|reject|exit\s*\(|process\.exit|throw|error|warn|fail|stop|approval|approve|mandatory|allowed?|disallow|prohibit|instead)\b", re.I)


def sweep(root, cand):
    out = root / 'stage_A' / 'primary' / cand
    segs = [json.loads(l) for l in (out / 'coverage_ranges.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    snap = root / 'inputs' / cand
    cache = {}
    hits = 0
    for s in segs:
        if s['disposition'] not in ('NON_NORMATIVE', 'IMPLEMENTATION', 'DUPLICATE'):
            continue
        p = s['path']
        if p not in cache:
            cache[p] = src_lines(snap / p)
        for i in range(s['start_line'], s['end_line'] + 1):
            t = cache[p][i - 1]
            if NORM_RE.search(t):
                hits += 1
                print(f'{s["segment_id"]} {s["disposition"][:3]} {p}:{i}: {t.strip()[:150]}')
    print(f'# keyword hits in non-normative/implementation/duplicate spans: {hits}', file=sys.stderr)


def show(root, cand, path, a=None, b=None):
    lines = src_lines(root / 'inputs' / cand / path)
    a = a or 1
    b = b or len(lines)
    for i in range(a, b + 1):
        print(f'{i:5d}  {lines[i-1]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('op', choices=('build', 'sweep', 'show', 'uncovered'))
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--candidate', required=True)
    ap.add_argument('--complete', default='')
    ap.add_argument('--path')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--maxerr', type=int, default=60)
    a = ap.parse_args()
    root = a.root.resolve()
    if a.op == 'build':
        comp = [x for x in a.complete.split(',') if x]
        stats, errors, warns = build(root, a.candidate, complete=comp, write=not a.dry)
        print(json.dumps(stats, ensure_ascii=False))
        unc = [e for e in errors if e.startswith('UNCOVERED')]
        other = [e for e in errors if not e.startswith('UNCOVERED')]
        for e in other[:a.maxerr]:
            print('ERROR:', e)
        if unc:
            byf = Counter(e.split(' ', 1)[1].rsplit(':', 2)[0] for e in unc)
            for f, n in byf.items():
                print(f'UNCOVERED-SUMMARY {f}: {n} lines')
            for e in unc[:a.maxerr]:
                print(e)
        sys.exit(1 if other else 0)
    elif a.op == 'sweep':
        sweep(root, a.candidate)
    elif a.op == 'show':
        show(root, a.candidate, a.path)


if __name__ == '__main__':
    main()
