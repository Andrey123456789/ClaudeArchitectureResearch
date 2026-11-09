#!/usr/bin/env python3
"""Run-2 replica builder: compiles compact per-batch annotation files (.ann) into the
Stage A ledgers under stage_A/replica/<candidate>/.

Reads ONLY: inputs/<candidate>/** (immutable snapshot), stage_A/_control/<candidate>_WORK_QUEUE.json
(read-only) and stage_A/replica/<candidate>/_annotations/*. Writes ONLY stage_A/replica/<candidate>/.

Annotation DSL (one directive per line, '#' starts a comment line):
  FILE <template-relative path> [| scan note]
  <a>[-<b>] <DISP> [cid,cid,...] | [quote-spec] [⟫ reason]
      DISP: NN=NON_NORMATIVE IM=IMPLEMENTATION DU=DUPLICATE OL=ORACLE_LINKED EX=EXTRA
            LU=LINK_UNCERTAIN MX=MIXED.  For NN/IM the text after '|' is the reason.
      quote-spec: empty -> whole trimmed range text; 'A…B' -> exact source substring from A to B;
                  otherwise a literal substring of the range (verified).
  C <cid> <OL|EX|LU> <policy,policy|-> | modality | action | trigger scope | exceptions [| why | behavior]
  O <path> <a>[-<b>] <ER|PL|LU|NN|DU> <cids|-> <closest policies|-> | quote-spec | reason | behavior
  P <policy-id> <M|PA|NE|UN> | search notes          (POLICIES.ann only)
  DONE                                               (batch annotation finished)
Short constraint ids: R12 -> RULE-<cand>-0012, X3 -> EXTRA-<cand>-0003, U1 -> UNCERTAIN-<cand>-0001.
EXTRA / LINK_UNCERTAIN constraints automatically receive an orphan-ledger row built from their first
EXTRA/LINK_UNCERTAIN/MIXED evidence segment.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DISP = {'NN': 'NON_NORMATIVE', 'IM': 'IMPLEMENTATION', 'DU': 'DUPLICATE', 'OL': 'ORACLE_LINKED',
        'EX': 'EXTRA', 'LU': 'LINK_UNCERTAIN', 'MX': 'MIXED'}
ORIG = {'OL': 'ORACLE_LINKED', 'EX': 'EXTRA', 'LU': 'LINK_UNCERTAIN'}
RES = {'ER': 'EXTRA_REGISTERED', 'PL': 'POLICY_LINKED', 'LU': 'LINK_UNCERTAIN', 'NN': 'NON_NORMATIVE',
       'DU': 'DUPLICATE'}
RES_ORIGIN = {'EXTRA_REGISTERED': 'EXTRA', 'POLICY_LINKED': 'ORACLE_LINKED', 'LINK_UNCERTAIN': 'LINK_UNCERTAIN'}
STAT = {'M': 'MATCHED', 'PA': 'PARTIAL', 'NE': 'NOT_EVIDENCED', 'UN': 'UNCERTAIN'}
SEG_RE = re.compile(r'^(\d+)(?:-(\d+))?\s+(NN|IM|DU|OL|EX|LU|MX)(?:\s+([^\s|]+))?\s*(?:\|(.*))?$')
TP = 'output/template/'


class BuildError(Exception):
    pass


def expand(tok, cand):
    tok = tok.strip()
    m = re.fullmatch(r'([RXU])(\d+)', tok)
    if m:
        pre = {'R': 'RULE', 'X': 'EXTRA', 'U': 'UNCERTAIN'}[m.group(1)]
        return f'{pre}-{cand}-{int(m.group(2)):04d}'
    return tok


def expand_text(text, cand):
    """Expand short constraint ids (R12, X3, U1) appearing in free text to full ids."""
    return re.sub(r'(?<![\w-])([RXU])(\d+)(?![\w-])', lambda m: expand(m.group(0), cand), text or '')


def id_list(s, cand):
    s = (s or '').strip()
    if not s or s == '-':
        return []
    return [expand(t, cand) for t in s.split(',') if t.strip()]


def resolve_quote(spec, text, where, errors):
    spec = (spec or '').strip()
    if not spec:
        q = text.strip()
        if not q:
            errors.append(f'{where}: empty range text for auto quote')
        return q
    if '…' in spec and spec not in text:
        a, b = spec.split('…', 1)
        a, b = a.strip(), b.strip()
        i = text.find(a)
        if i < 0:
            errors.append(f'{where}: quote prefix not found: {a!r}')
            return spec
        j = text.find(b, i + len(a))
        if j < 0:
            errors.append(f'{where}: quote suffix not found after prefix: {b!r}')
            return spec
        return text[i:j + len(b)]
    if spec not in text:
        errors.append(f'{where}: literal quote not in range: {spec[:90]!r}')
    return spec


def load_lines(root, cand, rel):
    data = (root / 'inputs' / cand / rel).read_bytes()
    if b'\0' in data:
        return None
    try:
        return data.decode('utf-8-sig').splitlines()
    except UnicodeDecodeError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--candidate', required=True)
    ap.add_argument('--final', action='store_true', help='require POLICIES.ann and emit reports')
    args = ap.parse_args()
    root = args.root.resolve()
    cand = args.candidate
    out = root / 'stage_A' / 'replica' / cand
    ann_dir = out / '_annotations'
    queue = json.loads((root / 'stage_A' / '_control' / f'{cand}_WORK_QUEUE.json').read_text(encoding='utf-8'))
    qfiles = {f['path']: f for f in queue['files']}
    errors, warnings = [], []

    constraints = {}          # cid -> dict
    corder = []
    file_sections = {}        # rel path -> {'note':..., 'segs':[...], 'batch':...}
    orphans_explicit = []     # (batch, row)
    batch_done = {}
    batch_cdefs = defaultdict(list)

    def parse_file(path, batch):
        cur = None
        for n, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.rstrip()
            where = f'{path.name}:{n}'
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if line.startswith('FILE '):
                body = line[5:]
                rel, _, note = body.partition(' | ')
                rel = rel.strip()
                rel = rel if rel.startswith('output/') else TP + rel
                if rel not in qfiles:
                    errors.append(f'{where}: FILE not in queue: {rel}')
                if rel in file_sections:
                    errors.append(f'{where}: duplicate FILE section {rel}')
                cur = {'note': note.strip(), 'segs': [], 'batch': batch, 'rel': rel}
                file_sections[rel] = cur
            elif line.strip() == 'DONE':
                batch_done[batch] = True
            elif line.startswith('C '):
                parts = line[2:].split(' | ')
                head = parts[0].split()
                if len(head) != 3 or head[1] not in ORIG:
                    errors.append(f'{where}: bad constraint head {parts[0]!r}')
                    continue
                cid = expand(head[0], cand)
                if cid in constraints:
                    errors.append(f'{where}: duplicate constraint {cid}')
                    continue
                f = [expand_text(p.strip(), cand) for p in parts[1:]] + [''] * 7
                row = {'id': cid, 'origin': ORIG[head[1]], 'policy_ids': id_list(head[2], cand),
                       'normative_action': f[1], 'modality': f[0], 'trigger_scope': f[2],
                       'exceptions': f[3] or 'none stated', 'evidence_segment_ids': [],
                       'why_extra_or_uncertain': f[4], '_behavior': f[5], '_batch': batch, '_where': where}
                pre = {'ORACLE_LINKED': 'RULE', 'EXTRA': 'EXTRA', 'LINK_UNCERTAIN': 'UNCERTAIN'}[row['origin']]
                if not cid.startswith(f'{pre}-{cand}-'):
                    errors.append(f'{where}: id prefix does not match origin: {cid}')
                if not row['normative_action'] or not row['modality']:
                    errors.append(f'{where}: constraint missing modality/action {cid}')
                if row['origin'] != 'ORACLE_LINKED' and (not row['why_extra_or_uncertain'] or not row['_behavior']):
                    errors.append(f'{where}: EXTRA/LU constraint needs why + behavior {cid}')
                if row['origin'] == 'ORACLE_LINKED' and not row['policy_ids']:
                    errors.append(f'{where}: ORACLE_LINKED without policy {cid}')
                constraints[cid] = row
                corder.append(cid)
                batch_cdefs[batch].append(cid)
            elif line.startswith('O '):
                parts = line[2:].split(' | ')
                head = parts[0].split()
                if len(head) != 5 or head[2] not in RES:
                    errors.append(f'{where}: bad orphan head {parts[0]!r}')
                    continue
                rel = head[0] if head[0].startswith('output/') else TP + head[0]
                a, _, b = head[1].partition('-')
                f = [p.strip() for p in parts[1:]] + [''] * 4
                f = [f[0]] + [expand_text(x, cand) for x in f[1:]]
                orphans_explicit.append((batch, {'rel': rel, 'a': int(a), 'b': int(b or a), 'res': RES[head[2]],
                                                 'cids': id_list(head[3], cand), 'closest': id_list(head[4], cand),
                                                 'qspec': f[0], 'reason': f[1], 'behavior': f[2], 'where': where}))
            else:
                m = SEG_RE.match(line)
                if not m or cur is None:
                    errors.append(f'{where}: unparseable line {line[:80]!r}')
                    continue
                a = int(m.group(1))
                b = int(m.group(2) or a)
                disp = DISP[m.group(3)]
                cids = id_list(m.group(4), cand)
                rest = m.group(5) or ''
                if disp in ('NON_NORMATIVE', 'IMPLEMENTATION'):
                    qspec, reason = '', rest.strip()
                    if cids:
                        errors.append(f'{where}: {disp} must not link constraints')
                elif disp == 'DUPLICATE' and '⟫' not in rest:
                    qspec, reason = '', rest.strip()
                else:
                    qspec, _, reason = rest.partition('⟫')
                cur['segs'].append({'a': a, 'b': b, 'disp': disp, 'cids': cids, 'qspec': qspec,
                                    'reason': expand_text(reason.strip(), cand), 'where': where})

    ann_files = sorted(ann_dir.glob('B*.ann'))
    batch_ids = [b['id'] for b in queue['batches']]
    for p in ann_files:
        if p.stem not in batch_ids:
            errors.append(f'annotation for unknown batch {p.name}')
            continue
        parse_file(p, p.stem)
    sweep = ann_dir / 'SWEEP.ann'
    if sweep.is_file():
        parse_file(sweep, 'SWEEP')

    # ---- segments
    segments = []
    seg_by_id = {}
    file_rows = []
    batch_ok = {}
    seq = 0
    for b in queue['batches']:
        bid = b['id']
        ok = (ann_dir / f'{bid}.ann').is_file()
        if not ok:
            batch_ok[bid] = False
            continue
        nerr0 = len(errors)
        for rel in b['files']:
            meta = qfiles[rel]
            sec = file_sections.get(rel)
            if sec is None:
                errors.append(f'{bid}: missing FILE section for {rel}')
                continue
            if sec['batch'] != bid:
                errors.append(f'{rel}: annotated in {sec["batch"]} but queued in {bid}')
            current = (root / 'inputs' / cand / rel).read_bytes()
            if hashlib.sha256(current).hexdigest() != meta['sha256']:
                errors.append(f'SNAPSHOT CHANGED {rel}')
            lines = load_lines(root, cand, rel)
            ftype = 'text' if lines is not None else 'binary'
            if ftype != meta['type']:
                errors.append(f'type mismatch {rel}')
            cnt = Counter()
            if lines is None:
                if sec['segs']:
                    errors.append(f'{rel}: binary file cannot have segments')
            else:
                covered = [0] * (len(lines) + 1)
                for s in sorted(sec['segs'], key=lambda x: x['a']):
                    a, bb = s['a'], s['b']
                    if not (1 <= a <= bb <= len(lines)):
                        errors.append(f'{s["where"]}: range {a}-{bb} out of bounds ({len(lines)})')
                        continue
                    for i in range(a, bb + 1):
                        if covered[i]:
                            errors.append(f'{s["where"]}: overlap at {rel}:{i}')
                        covered[i] = 1
                    text = '\n'.join(lines[a - 1:bb])
                    if not text.strip():
                        errors.append(f'{s["where"]}: segment covers only blank lines')
                    seq += 1
                    sid = f'{cand}-S{seq:06d}'
                    row = {'segment_id': sid, 'path': rel, 'start_line': a, 'end_line': bb,
                           'disposition': s['disp'], 'constraint_ids': s['cids']}
                    if s['disp'] in ('ORACLE_LINKED', 'EXTRA', 'LINK_UNCERTAIN', 'MIXED'):
                        if not s['cids']:
                            errors.append(f'{s["where"]}: normative segment without constraints')
                        row['quote'] = resolve_quote(s['qspec'], text, s['where'], errors)
                        reason = s['reason']
                        if s['disp'] in ('LINK_UNCERTAIN', 'MIXED') and not reason:
                            errors.append(f'{s["where"]}: {s["disp"]} requires reason')
                        if not reason:
                            pol = sorted({p for c in s['cids'] if c in constraints for p in constraints[c]['policy_ids']})
                            reason = f'{s["disp"]} clause; constraints {", ".join(s["cids"])}' + (f'; policies {", ".join(pol)}' if pol else '')
                        row['reason'] = reason
                        origins = set()
                        for c in s['cids']:
                            if c not in constraints:
                                errors.append(f'{s["where"]}: unknown constraint {c}')
                                continue
                            origins.add(constraints[c]['origin'])
                            if s['disp'] != 'MIXED' and constraints[c]['origin'] != s['disp']:
                                errors.append(f'{s["where"]}: origin mismatch {c} ({constraints[c]["origin"]}) in {s["disp"]}')
                        if s['disp'] == 'MIXED' and len(origins) < 2:
                            warnings.append(f'{s["where"]}: MIXED segment links a single origin {origins}')
                    else:
                        if not s['reason']:
                            errors.append(f'{s["where"]}: {s["disp"]} requires reason')
                        row['reason'] = s['reason']
                        if s['disp'] == 'DUPLICATE':
                            row['quote'] = resolve_quote(s['qspec'], text, s['where'], errors) if s['qspec'].strip() else text.strip()[:400]
                            for c in s['cids']:
                                if c not in constraints:
                                    errors.append(f'{s["where"]}: unknown constraint {c}')
                    cnt[s['disp']] += 1
                    segments.append(row)
                    seg_by_id[sid] = row
                    for c in s['cids']:
                        if c in constraints:
                            constraints[c]['evidence_segment_ids'].append(sid)
                unc = [i for i in range(1, len(lines) + 1) if lines[i - 1].strip() and not covered[i]]
                if unc:
                    errors.append(f'{rel}: uncovered nonblank lines {unc[:15]}{" ..." if len(unc) > 15 else ""}')
            nb = meta['nonblank_lines']
            note = f'Read in full ({meta["total_lines"]} lines, {nb} nonblank, {meta["bytes"]} bytes, sha256 {meta["sha256"][:12]}). '
            if lines is None:
                note += 'Binary/non-UTF-8: not decoded; no line coverage possible.'
            elif not lines:
                note += 'Empty file: no lines, no normative content.'
            else:
                note += 'Segments: ' + ', '.join(f'{k}={v}' for k, v in sorted(cnt.items())) + '.'
            if sec['note']:
                note += ' ' + sec['note']
            file_rows.append({'path': rel, 'type': ftype, 'encoding': 'utf-8' if ftype == 'text' else None,
                              'scan_notes': note})
        if not batch_done.get(bid):
            errors.append(f'{bid}: annotation not marked DONE') if False else warnings.append(f'{bid}: not marked DONE')
        batch_ok[bid] = batch_done.get(bid, False) and len(errors) == nerr0
    # sweep-only segments are not allowed (sweep file holds constraints/orphans only)

    for cid in corder:
        if not constraints[cid]['evidence_segment_ids']:
            errors.append(f'constraint without evidence segment: {cid} ({constraints[cid]["_where"]})')
        for pid in constraints[cid]['policy_ids']:
            if not re.fullmatch(r'[A-Z]+-\d{3}', pid):
                errors.append(f'bad policy id {pid} in {cid}')

    # ---- orphans
    orphan_rows = []
    oseq = 0

    def add_orphan(rel, a, b, res, cids, closest, qspec, reason, behavior, where):
        nonlocal oseq
        lines = load_lines(root, cand, rel)
        if lines is None or not (1 <= a <= b <= len(lines)):
            errors.append(f'{where}: orphan range invalid {rel}:{a}-{b}')
            return
        text = '\n'.join(lines[a - 1:b])
        q = resolve_quote(qspec, text, where, errors)
        for c in cids:
            if c not in constraints:
                errors.append(f'{where}: orphan links unknown constraint {c}')
            elif res in RES_ORIGIN and constraints[c]['origin'] != RES_ORIGIN[res]:
                errors.append(f'{where}: orphan {res} links {c} with origin {constraints[c]["origin"]}')
        if res in ('EXTRA_REGISTERED', 'POLICY_LINKED', 'LINK_UNCERTAIN') and not cids:
            errors.append(f'{where}: operative orphan without constraints')
        if res == 'NON_NORMATIVE' and cids:
            errors.append(f'{where}: NON_NORMATIVE orphan must not link constraints')
        if not reason:
            errors.append(f'{where}: orphan without reason')
        if res in ('EXTRA_REGISTERED', 'LINK_UNCERTAIN') and not behavior:
            errors.append(f'{where}: orphan without specific behavior')
        oseq += 1
        orphan_rows.append({'id': f'ORPHAN-{cand}-{oseq:04d}', 'candidate': cand, 'path': rel, 'start_line': a,
                            'end_line': b, 'quote': q, 'resolution': res, 'constraint_ids': cids,
                            'closest_policy_ids': closest, 'reason': reason, 'specific_behavior': behavior or ''})

    explicit_cids = {c for _, o in orphans_explicit for c in o['cids'] if o['res'] in ('EXTRA_REGISTERED', 'LINK_UNCERTAIN')}
    for batch in batch_ids + ['SWEEP']:
        if batch != 'SWEEP' and not (ann_dir / f'{batch}.ann').is_file():
            continue
        for bt, o in orphans_explicit:
            if bt == batch:
                add_orphan(o['rel'], o['a'], o['b'], o['res'], o['cids'], o['closest'], o['qspec'], o['reason'],
                           o['behavior'], o['where'])
        for cid in batch_cdefs.get(batch, []):
            c = constraints[cid]
            if c['origin'] == 'ORACLE_LINKED' or cid in explicit_cids:
                continue
            seg = next((seg_by_id[s] for s in c['evidence_segment_ids']
                        if seg_by_id[s]['disposition'] in ('EXTRA', 'LINK_UNCERTAIN', 'MIXED')), None)
            if seg is None:
                seg = next((seg_by_id[s] for s in c['evidence_segment_ids']), None)
            if seg is None:
                continue
            res = 'EXTRA_REGISTERED' if c['origin'] == 'EXTRA' else 'LINK_UNCERTAIN'
            add_orphan(seg['path'], seg['start_line'], seg['end_line'], res, [cid], c['policy_ids'],
                       seg.get('quote', ''), c['why_extra_or_uncertain'], c['_behavior'], c['_where'])

    # ---- policies
    oracle = []
    inv = json.loads((root / 'inputs' / cand / 'source' / 'inventory.json').read_text(encoding='utf-8-sig'))
    shared = json.loads((root / 'inputs' / cand / 'source' / 'shared-research-invariants.json').read_text(encoding='utf-8-sig'))
    oracle = [p['id'] for g in inv['policygroups'] for p in g['policies']] + [i['id'] for i in shared['invariants']]
    oracle_set = set(oracle)
    for cid in corder:
        for pid in constraints[cid]['policy_ids']:
            if pid not in oracle_set:
                errors.append(f'{cid}: unknown oracle policy {pid}')
    policy_rows = []
    pol_file = ann_dir / 'POLICIES.ann'
    if pol_file.is_file():
        seen = {}
        for n, raw in enumerate(pol_file.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^P\s+([A-Z]+-\d{3})\s+(M|PA|NE|UN)\s*\|\s*(.+)$', line)
            if not m:
                errors.append(f'POLICIES.ann:{n}: unparseable')
                continue
            pid, st, notes = m.group(1), STAT[m.group(2)], expand_text(m.group(3).strip(), cand)
            if pid in seen:
                errors.append(f'POLICIES.ann:{n}: duplicate {pid}')
            seen[pid] = (st, notes)
        for pid in oracle:
            if pid not in seen:
                if args.final:
                    errors.append(f'policy row missing: {pid}')
                continue
            st, notes = seen[pid]
            linked = [c for c in corder if pid in constraints[c]['policy_ids'] and constraints[c]['origin'] != 'EXTRA']
            extras = [c for c in corder if pid in constraints[c]['policy_ids'] and constraints[c]['origin'] == 'EXTRA']
            ev = []
            for c in linked:
                for s in constraints[c]['evidence_segment_ids']:
                    if s not in ev:
                        ev.append(s)
            if st == 'MATCHED' and not any(constraints[c]['origin'] == 'ORACLE_LINKED' for c in linked):
                errors.append(f'{pid}: MATCHED without ORACLE_LINKED constraint')
            if st == 'NOT_EVIDENCED' and any(constraints[c]['origin'] == 'ORACLE_LINKED' for c in linked):
                errors.append(f'{pid}: NOT_EVIDENCED but has ORACLE_LINKED constraints {linked}')
            if st in ('PARTIAL',) and not linked:
                errors.append(f'{pid}: PARTIAL without any linked constraint')
            refs = []
            for s in ev:
                seg = seg_by_id[s]
                ref = f'{seg["path"].replace(TP, "")}:{seg["start_line"]}' + (f'-{seg["end_line"]}' if seg["end_line"] != seg["start_line"] else '')
                if ref not in refs:
                    refs.append(ref)
            auto = (f'Search: all {cand} template files read in full plus reverse sweep. '
                    f'Linked constraints: {len(linked)}; evidence ({len(refs)} segment locations): '
                    + '; '.join(refs[:8]) + (' ...' if len(refs) > 8 else '') + '. ') if linked else \
                   f'Search: all {cand} template files read in full plus reverse sweep; no linked constraint. '
            notes = auto + 'Assessment: ' + notes
            if extras:
                notes += f' Related EXTRA constraints (closest-policy link only, not counted as evidence): {", ".join(extras)}.'
            policy_rows.append({'rule_id': pid, 'status': st, 'atomic_constraint_ids': linked,
                                'evidence_segment_ids': ev, 'search_notes': notes})
        for pid in seen:
            if pid not in oracle_set:
                errors.append(f'POLICIES.ann: unknown policy {pid}')
    elif args.final:
        errors.append('POLICIES.ann missing for --final')

    # ---- write
    out.mkdir(parents=True, exist_ok=True)

    def wj(name, rows):
        with (out / name).open('w', encoding='utf-8', newline='\n') as fp:
            for r in rows:
                fp.write(json.dumps(r, ensure_ascii=False) + '\n')

    crow = []
    for cid in corder:
        c = constraints[cid]
        crow.append({k: c[k] for k in ('id', 'origin', 'policy_ids', 'normative_action', 'modality', 'trigger_scope',
                                       'exceptions', 'evidence_segment_ids', 'why_extra_or_uncertain')})
    wj('files.jsonl', file_rows)
    wj('coverage_ranges.jsonl', segments)
    wj('constraints.jsonl', crow)
    wj('ORPHAN_CANDIDATES.jsonl', orphan_rows)
    if policy_rows and (args.final or len(policy_rows) == len(oracle)):
        wj('policies.jsonl', policy_rows)
    completed = [b for b in batch_ids if batch_ok.get(b)] if not errors else \
        [b for b in batch_ids if batch_ok.get(b)]
    prog_path = out / 'PROGRESS.json'
    prev = json.loads(prog_path.read_text(encoding='utf-8')) if prog_path.is_file() else {}
    state = {'candidate': cand, 'completed_batch_ids': completed,
             'notes': f'Run 2 replica (blind). Built from _annotations/*.ann by _tools/build.py. '
                      f'{len(completed)}/{len(batch_ids)} batches complete; {len(segments)} segments; '
                      f'{len(crow)} constraints; {len(orphan_rows)} orphan rows; policies.jsonl '
                      f'{"written" if (out / "policies.jsonl").is_file() else "pending"}. '
                      + (prev.get('extra_notes', '') if isinstance(prev, dict) else '')}
    if isinstance(prev, dict) and prev.get('extra_notes'):
        state['extra_notes'] = prev['extra_notes']
    prog_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # constraint index for the annotator
    idx = []
    for cid in corder:
        c = constraints[cid]
        idx.append(f'{cid} {c["origin"][:2]} {",".join(c["policy_ids"]) or "-"} [{c["modality"]}] {c["normative_action"][:150]}')
    (ann_dir / '_INDEX.txt').write_text('\n'.join(idx) + '\n', encoding='utf-8')

    oc = Counter(c['origin'] for c in crow)
    print(f'{cand}: batches complete {len(completed)}/{len(batch_ids)} {completed}')
    print(f'segments={len(segments)} constraints={len(crow)} {dict(oc)} orphans={len(orphan_rows)} '
          f'orphan_res={dict(Counter(o["resolution"] for o in orphan_rows))} policies={len(policy_rows)}')
    for w in warnings[:40]:
        print('WARN:', w)
    if errors:
        for e in errors[:120]:
            print('ERROR:', e)
        print(f'BUILD FAIL ({len(errors)} errors)')
        sys.exit(1)
    print('BUILD OK')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
