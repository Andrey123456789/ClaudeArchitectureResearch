"""Candidate-level steps after all batches of a candidate are checkpointed.

  python -B candidate.py <C> assemble                  verify batch checkpoints, apply CORRECTED_RECORDS overlay and A1 enrichment,
                                                       write per_candidate/<C>/CLASSIFICATIONS.jsonl
  python -B candidate.py <C> strength                  list records whose strength still needs a resolution (st=/sr=/STRENGTH.dec)
  python -B candidate.py <C> coverage [--view]         POLICY_COVERAGE.jsonl (196 rows) and STRENGTH_DIVERGENCES.jsonl
  python -B candidate.py <C> orphans --view|--build    Step-1 pending orphans, Pass-1 unresolved items, Step-1 conflict/unresolved queue items
  python -B candidate.py <C> challenge --view [N] [--round R]    frozen deterministic semantic-challenge sample (N per family, default 3)
  python -B candidate.py <C> challenge --build         compile _decisions/<C>/CHALLENGES[_R<n>].dec -> per_candidate/<C>/SEMANTIC_CHALLENGES.jsonl
  python -B candidate.py <C> finish                    assemble, coverage, orphans --build, challenge --build, assemble, coverage, report
  python -B candidate.py <C> report                    validate candidate outputs, write CANDIDATE_REPORT.md and the candidate checkpoint

COVERAGE.dec lines:  <POLICY-ID> <DIRECT_EVIDENCE|PARTIAL_EVIDENCE|NOT_EVIDENCED|UNCERTAIN> | note
ORPHANS.dec lines:   <n> <ATTACH key[,key]|NON_NORMATIVE|QUEUE|RESOLVED key[,key]> | note
CHALLENGES.dec:      <n> <UPHELD|REVISED_NEEDED|UNCERTAIN> | challenge note (counterexample tried, outcome)
STRENGTH.dec lines:  <source_key[/S#]> <SL|PC|CK|CR|PM|AM|GR|CN> | note

Guard (Addendum A1): a REVISED_NEEDED challenge without a linked correction, or an UNCERTAIN challenge on a record without
review_needed, is an error, so a failed challenge can never coexist with a passing candidate report.
"""
import hashlib
import json
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict

from common import (OUT, ROOT, S1, P1, PROTOCOL_VERSION, CANDIDATES, policies, read_jsonl, write_jsonl_atomic,
                    write_json_atomic, sha256_file, sha256_text, union_view, source_key, occurrences,
                    NOT_OWNER_CODES)
from enrich import enrich, load_strength_dec, rows_needing_strength_review

STATUSES = ('DIRECT_EVIDENCE', 'PARTIAL_EVIDENCE', 'NOT_EVIDENCED', 'UNCERTAIN')


def pc(c, *p):
    return os.path.join(OUT, 'per_candidate', c, *p)


def load_cls(c):
    return read_jsonl(pc(c, 'CLASSIFICATIONS.jsonl'))


def assemble(c):
    plan = json.load(open(os.path.join(OUT, '_batches', c + '.json'), encoding='utf-8'))
    rows, problems = [], []
    for b in plan['batches']:
        ck = os.path.join(OUT, 'CHECKPOINTS', c, b['batch_id'] + '.checkpoint.json')
        f = pc(c, 'batches', b['batch_id'] + '.jsonl')
        if not os.path.exists(ck):
            problems.append('missing checkpoint ' + b['batch_id']); continue
        ckj = json.load(open(ck, encoding='utf-8'))
        if ckj.get('status') != 'COMPLETE' or sha256_file(f) != ckj['batch_file_sha256']:
            problems.append('checkpoint/hash mismatch ' + b['batch_id']); continue
        part = read_jsonl(f)
        if [r['source_key'] for r in part] != [x['source_key'] for x in b['records']]:
            problems.append('key order mismatch ' + b['batch_id'])
        rows.extend(part)
    if problems:
        print('ERRORS', problems); sys.exit(1)
    expected = [source_key(r) for r in union_view() if r['candidate'] == c]
    if sorted(r['source_key'] for r in rows) != sorted(expected) or len(rows) != len(set(r['source_key'] for r in rows)):
        print('ERROR: assembled keys differ from union view'); sys.exit(1)
    overlay = {}
    if os.path.exists(pc(c, 'CORRECTED_RECORDS.jsonl')):
        ck = json.load(open(os.path.join(OUT, 'CHECKPOINTS', c, 'CORRECTIONS.checkpoint.json'), encoding='utf-8'))
        if sha256_file(pc(c, 'CORRECTED_RECORDS.jsonl')) != ck['corrected_records_sha256']:
            print('ERROR: CORRECTED_RECORDS hash differs from its checkpoint'); sys.exit(1)
        overlay = {r['source_key']: r for r in read_jsonl(pc(c, 'CORRECTED_RECORDS.jsonl'))}
    table = load_strength_dec(c)
    challenge_by_key = {}
    if os.path.exists(pc(c, 'SEMANTIC_CHALLENGES.jsonl')):
        for x in read_jsonl(pc(c, 'SEMANTIC_CHALLENGES.jsonl')):
            challenge_by_key.setdefault(x['source_key'], []).append(
                {k: x.get(k) for k in ('round', 'outcome', 'resolution', 'resolved_by_corrections')})
    out = []
    for r in rows:
        rec = overlay.get(r['source_key'], r)
        rec = enrich(dict(rec), table)
        rec['correction_history'] = rec.get('correction_history') or []
        rec['semantic_challenge'] = challenge_by_key.get(r['source_key']) or []
        out.append(rec)
    write_jsonl_atomic(pc(c, 'CLASSIFICATIONS.jsonl'), out)
    print('assembled', len(out), dict(Counter(r['classification'] for r in out)), 'corrected', len(overlay))


def strength(c):
    sys.stdout.reconfigure(encoding='utf-8')
    rows = load_cls(c)
    pending = rows_needing_strength_review(rows)
    by = {r['source_key']: r for r in rows}
    for key, why in pending:
        r = by[key.split('/')[0]]
        print('%s %s %s %s | %s | %s' % (key, r['classification'][:12], r['modality'], r['canonical_policy_ids'], why, r['claim_text'][:110]))
    print('pending', len(pending))


def policy_links(rows):
    links = defaultdict(list)
    for r in rows:
        for rec, sub in [(r, None)] + [(r, s) for s in r.get('subclauses') or []]:
            obj = sub or rec
            cls = obj['classification']
            res = obj.get('strength_resolution') or {}
            for l in obj.get('strength_links') or []:
                kind = 'UNCERTAIN_LINK' if cls == 'UNCERTAIN' else l['coverage']
                if kind == 'FULL' and res.get('code') in NOT_OWNER_CODES:
                    kind = 'PARTIAL'
                links[l['policy_id']].append({
                    'source_key': rec['source_key'], 'subclause_id': sub['subclause_id'] if sub else None,
                    'classification': cls, 'link': kind, 'confidence': rec['confidence'],
                    'equivalence': obj.get('normative_strength_equivalence'), 'resolution': res.get('code'),
                    'modality': obj.get('modality'), 'claim_text': (sub['text'] if sub else rec['claim_text'])[:300]})
    return links


def coverage(c, view=False):
    rows = load_cls(c)
    links = policy_links(rows)
    overrides = {}
    ov = os.path.join(OUT, '_decisions', c, 'COVERAGE.dec')
    if os.path.exists(ov):
        for ln, raw in enumerate(open(ov, encoding='utf-8'), 1):
            raw = raw.strip()
            if not raw or raw.startswith('#'):
                continue
            m = re.match(r'^(\S+)\s+(\S+)\s*\|\s*(.+)$', raw)
            if not m or m.group(1) not in policies() or m.group(2) not in STATUSES:
                print('bad COVERAGE.dec line', ln, raw); sys.exit(1)
            overrides[m.group(1)] = (m.group(2), m.group(3))
    out = []
    for pid, p in policies().items():
        ls = links.get(pid, [])
        canon = [l for l in ls if l['classification'] in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA')]
        full = [l for l in canon if l['link'] == 'FULL' and l['confidence'] in ('HIGH', 'MEDIUM')]
        part = [l for l in ls if l['link'] in ('PARTIAL', 'FULL') and l not in full and l['classification'] != 'UNCERTAIN']
        unc = [l for l in ls if l['link'] == 'UNCERTAIN_LINK']
        status = 'DIRECT_EVIDENCE' if full else ('PARTIAL_EVIDENCE' if part else ('UNCERTAIN' if unc else 'NOT_EVIDENCED'))
        computed = status
        note = None
        if pid in overrides:
            status, note = overrides[pid]
        same = sorted({l['source_key'] for l in canon if l['equivalence'] in ('EQUIVALENT', 'PORTION_EQUIVALENT_WITH_REMAINDER') and l['resolution'] not in NOT_OWNER_CODES})
        weaker = sorted({l['source_key'] for l in canon if l['equivalence'] == 'WEAKER_THAN_CANONICAL'})
        stronger = sorted({l['source_key'] for l in canon if l['equivalence'] == 'STRONGER_THAN_CANONICAL'})
        strength_status = ('EQUIVALENT_EVIDENCE_PRESENT' if same else
                           'STRONGER_AND_WEAKER_EVIDENCE' if weaker and stronger else
                           'ONLY_WEAKER_EVIDENCE' if weaker else
                           'ONLY_STRONGER_EVIDENCE' if stronger else
                           'NO_STRENGTH_EVIDENCE')
        out.append({
            'protocol_version': PROTOCOL_VERSION, 'protocol_addendum': 'A1', 'candidate': c, 'policy_id': pid, 'policy_name': p['name'],
            'policy_origin_file': p['origin_file'], 'normative_strength': p['normative_strength'],
            'status': status, 'computed_status': computed, 'reviewer_override_note': note,
            'direct_source_keys': sorted({l['source_key'] for l in full}),
            'partial_source_keys': sorted({l['source_key'] for l in part}),
            'uncertain_source_keys': sorted({l['source_key'] for l in unc}),
            'strength_status': strength_status,
            'strength_equivalent_source_keys': same, 'weaker_source_keys': weaker, 'stronger_source_keys': stronger,
            'n_links': len(ls),
            'semantics': 'traceability only: NOT_EVIDENCED means no adequate evidence in this classified dataset, not a violation; status is semantic coverage, strength_status is strength equivalence'})
    if len(out) != 196:
        print('ERROR coverage rows', len(out)); sys.exit(1)
    write_jsonl_atomic(pc(c, 'POLICY_COVERAGE.jsonl'), out)
    owners = {o['policy_id']: o['strength_equivalent_source_keys'] for o in out}
    div = []
    for r in rows:
        for key, obj in [(r['source_key'], r)] + [('%s/%s' % (r['source_key'], s['subclause_id']), s) for s in r.get('subclauses') or []]:
            if obj.get('classification') not in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA'):
                continue
            eq = obj.get('normative_strength_equivalence')
            if eq in ('WEAKER_THAN_CANONICAL', 'STRONGER_THAN_CANONICAL', 'INCOMPARABLE') or obj.get('strength_mechanical_mismatch'):
                res = obj.get('strength_resolution') or {}
                div.append({'protocol_version': PROTOCOL_VERSION, 'protocol_addendum': 'A1', 'candidate': c, 'source_key': key,
                            'classification': obj['classification'], 'record_modality': obj.get('modality'),
                            'canonical_semantic_coverage': obj.get('canonical_semantic_coverage'),
                            'normative_strength_equivalence': eq, 'links': obj.get('strength_links'),
                            'resolution_code': res.get('code'), 'resolution_label': res.get('label'), 'resolution_note': res.get('note'),
                            'equal_strength_owner_keys': {l['policy_id']: [k for k in owners.get(l['policy_id'], []) if k != r['source_key']][:6] for l in obj.get('strength_links') or []},
                            'claim_text': (obj.get('text') or obj.get('claim_text') or '')[:300],
                            'primary_anchor': r.get('primary_anchor')})
    write_jsonl_atomic(pc(c, 'STRENGTH_DIVERGENCES.jsonl'), div)
    print('coverage', dict(Counter(o['status'] for o in out)), 'strength', dict(Counter(o['strength_status'] for o in out)),
          'overrides', len(overrides), 'strength divergences', len(div))
    if view:
        sys.stdout.reconfigure(encoding='utf-8')
        for o in out:
            if o['computed_status'] != 'DIRECT_EVIDENCE' or o['strength_status'] != 'EQUIVALENT_EVIDENCE_PRESENT':
                p = policies()[o['policy_id']]
                print('\n## %s [%s] %s -> computed %s, strength %s%s' % (o['policy_id'], p['normative_strength'], p['normalized_policy'],
                                                                       o['computed_status'], o['strength_status'],
                                                                       (' / override ' + o['status']) if o['policy_id'] in overrides else ''))
                for l in links.get(o['policy_id'], [])[:8]:
                    print('   - %s %s %s %s/%s %s %s: %s' % (l['source_key'], l['subclause_id'] or '', l['classification'][:9], l['link'],
                                                            l['confidence'][0], l['equivalence'], l['resolution'] or '', l['claim_text'][:170]))


def orphan_items(c):
    items = []
    acc = read_jsonl(os.path.join(S1, 'RECORD_ACCOUNTING.jsonl'))
    sri = {r['record_key']: r for r in read_jsonl(os.path.join(S1, 'SOURCE_RECORD_INDEX.jsonl')) if r['candidate'] == c}
    for a in acc:
        if a['candidate'] == c and a['disposition'] == 'ORPHAN_PENDING_REVIEW':
            raw = sri[a['record_key']]['raw_record']
            items.append({'item_type': 'STEP1_ORPHAN_PENDING_REVIEW', 'item_id': a['record_key'],
                          'path': raw.get('path'), 'start_line': raw.get('start_line'), 'end_line': raw.get('end_line'),
                          'text': raw.get('quote') or raw.get('specific_behavior') or '',
                          'prior': '%s: %s' % (raw.get('resolution'), raw.get('reason') or ''),
                          'co_located_group_ids': a.get('co_located_group_ids') or []})
    for q in read_jsonl(os.path.join(P1, 'UNRESOLVED_REVIEW_QUEUE.jsonl')):
        if q['candidate'] == c:
            e = q.get('evidence') or {}
            items.append({'item_type': 'PASS1_UNRESOLVED', 'item_id': q['queue_id'], 'path': e.get('path'),
                          'start_line': e.get('start_line'), 'end_line': e.get('end_line'),
                          'text': e.get('quote') or '', 'prior': '%s / %s: %s' % (q.get('issue_type'), q.get('effective_status'), q.get('question')),
                          'co_located_group_ids': q.get('compared_group_ids') or []})
    for q in read_jsonl(os.path.join(S1, 'MERGE_REVIEW_QUEUE.jsonl')):
        if q['candidate'] == c and q['item_type'] in ('APPARENT_CONFLICT', 'UNRESOLVED'):
            items.append({'item_type': 'STEP1_QUEUE_' + q['item_type'], 'item_id': q['queue_id'], 'path': None,
                          'start_line': None, 'end_line': None, 'text': q.get('open_question') or '',
                          'prior': q['item_type'],
                          'co_located_group_ids': (q.get('group_ids_a') or []) + (q.get('group_ids_b') or [])})
    return items


def orphans(c, mode):
    items = orphan_items(c)
    cls = {r['source_key']: r for r in load_cls(c)}
    if mode == '--view':
        sys.stdout.reconfigure(encoding='utf-8')
        for i, it in enumerate(items, 1):
            print('[%d] %s %s %s' % (i, it['item_type'], it['item_id'],
                                      ('%s:%s-%s' % (str(it['path']).replace('output/template/', ''), it['start_line'], it['end_line'])) if it['path'] else ''))
            print('   text: ' + ' '.join(str(it['text']).split())[:260])
            print('   prior: ' + ' '.join(str(it['prior']).split())[:230])
            for g in it['co_located_group_ids'][:4]:
                r = cls.get(g)
                if r:
                    print('   ~ %s %s: %s' % (g, r['classification'], r['claim_text'][:120]))
        print('n items', len(items))
        return
    dec = os.path.join(OUT, '_decisions', c, 'ORPHANS.dec')
    decs = {}
    for ln, raw in enumerate(open(dec, encoding='utf-8'), 1):
        raw = raw.rstrip('\n')
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        m = re.match(r'^(\d+)\s+(ATTACH|NON_NORMATIVE|QUEUE|RESOLVED)\s*([^|]*)\|\s*(.+)$', raw)
        if not m:
            print('bad ORPHANS.dec line', ln, raw); sys.exit(1)
        keys = [k.strip() for k in m.group(3).split(',') if k.strip()]
        for k in keys:
            if k not in cls:
                print('unknown key in ORPHANS.dec line', ln, k); sys.exit(1)
        if m.group(2) in ('ATTACH', 'RESOLVED') and not keys:
            print('ATTACH/RESOLVED needs keys, line', ln); sys.exit(1)
        decs[int(m.group(1))] = (m.group(2), keys, m.group(4).strip())
    if set(decs) != set(range(1, len(items) + 1)):
        print('ORPHANS.dec coverage mismatch', sorted(set(range(1, len(items) + 1)) - set(decs))[:20], sorted(set(decs) - set(range(1, len(items) + 1)))[:20]); sys.exit(1)
    rows = []
    for i, it in enumerate(items, 1):
        d, keys, note = decs[i]
        rows.append(dict(it, protocol_version=PROTOCOL_VERSION, candidate=c, disposition=d, attached_source_keys=keys,
                         attached_classifications=[cls[k]['classification'] for k in keys], note=note,
                         evidence_ref=({'path': 'inputs/%s/%s' % (c, it['path']), 'start_line': it['start_line'],
                                        'end_line': it['end_line']} if it['path'] else None)))
    write_jsonl_atomic(pc(c, 'ORPHAN_DISPOSITIONS.jsonl'), rows)
    print('orphan dispositions', len(rows), dict(Counter(r['disposition'] for r in rows)))


def families(rows):
    def fam(name):
        if name == 'CO_EQUIVALENT':
            return [r for r in rows if r['classification'] == 'CANONICAL_ONLY' and r['normative_strength_equivalence'] == 'EQUIVALENT' and r['confidence'] == 'HIGH']
        if name == 'CO_WEAKER':
            return [r for r in rows if r['classification'] == 'CANONICAL_ONLY' and r['normative_strength_equivalence'] == 'WEAKER_THAN_CANONICAL']
        if name == 'NN':
            pool = [r for r in rows if r['classification'] == 'NON_NORMATIVE']
            return [r for r in pool if r['confidence'] == 'HIGH'] or pool
        if name == 'IA':
            return [r for r in rows if r['classification'] == 'INTERNAL_ARCHITECTURE' and r['confidence'] == 'HIGH']
        if name == 'EXTRA':
            return [r for r in rows if r['classification'] in ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW')]
        if name == 'CD':
            return [r for r in rows if r['classification'] == 'CANONICAL_PLUS_DELTA']
        return [r for r in rows if r['classification'] == 'MIXED']
    return [(n, fam(n)) for n in ('CO_EQUIVALENT', 'CO_WEAKER', 'NN', 'IA', 'EXTRA', 'CD', 'MX')]


def sample_path(c):
    return os.path.join(OUT, '_decisions', c, 'CHALLENGE_SAMPLE.json')


def frozen_sample(c, rnd, n, rows, only=None):
    """Freeze the sample on first use, so later corrections cannot shift the challenged set."""
    p = sample_path(c)
    data = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'candidate': c, 'rounds': {}}
    if str(rnd) not in data['rounds']:
        taken = {k for v in data['rounds'].values() for k in v}
        rng = random.Random(int(hashlib.sha256(('step2-v1-challenge-%s-r%d' % (c, rnd)).encode()).hexdigest()[:8], 16))
        keys = []
        for name, pool in families(rows):
            if only and name != only:
                continue
            pool = sorted([r['source_key'] for r in pool if r['source_key'] not in taken])
            keys.extend(rng.sample(pool, min(n, len(pool))))
        data['rounds'][str(rnd)] = keys
        write_json_atomic(p, data)
    return data['rounds'][str(rnd)]


def challenge(c, mode, n=3, rnd=1, only=None):
    rows = load_cls(c)
    by = {r['source_key']: r for r in rows}
    if mode == '--view':
        sys.stdout.reconfigure(encoding='utf-8')
        for i, key in enumerate(frozen_sample(c, rnd, n, rows, only), 1):
            r = by[key]
            print('[%d] %s %s %s pol=%s m=%s c=%s eq=%s t=%s' % (i, r['source_key'], r['classification'], r['domain'], ','.join(r['canonical_policy_ids']),
                                                                 r['modality'], r['confidence'], r['normative_strength_equivalence'], str(r['trigger'])[:80]))
            print('   C: ' + r['claim_text'][:300])
            print('   why: ' + (r['rationale'] or '')[:300])
            if r.get('extra_fragment'):
                print('   x: ' + r['extra_fragment'][:200])
            print('   src %s:%s-%s: %s' % (r['primary_anchor']['path'].split('template/')[-1], r['primary_anchor']['start_line'], r['primary_anchor']['end_line'],
                                           ' '.join(r['primary_quote'].split())[:520]))
        return
    samples = json.load(open(sample_path(c), encoding='utf-8'))['rounds']
    corr = defaultdict(list)
    if os.path.exists(pc(c, 'CORRECTIONS.jsonl')):
        for l in read_jsonl(pc(c, 'CORRECTIONS.jsonl')):
            corr[l['source_key']].append(l['correction_id'])
    out = []
    for rnd_s, keys in sorted(samples.items(), key=lambda kv: int(kv[0])):
        name = 'CHALLENGES.dec' if rnd_s == '1' else 'CHALLENGES_R%s.dec' % rnd_s
        dec = os.path.join(OUT, '_decisions', c, name)
        decs = {}
        for ln, raw in enumerate(open(dec, encoding='utf-8'), 1):
            raw = raw.strip()
            if not raw or raw.startswith('#'):
                continue
            m = re.match(r'^(\d+)\s+(UPHELD|REVISED_NEEDED|UNCERTAIN)\s*\|\s*(.+)$', raw)
            if not m:
                print('bad', name, 'line', ln); sys.exit(1)
            decs[int(m.group(1))] = (m.group(2), m.group(3))
        if set(decs) != set(range(1, len(keys) + 1)):
            print(name, 'coverage mismatch', len(decs), len(keys)); sys.exit(1)
        for i, key in enumerate(keys, 1):
            outcome, note = decs[i]
            ids = corr.get(key, [])
            r = by[key]
            if outcome == 'REVISED_NEEDED':
                resolution = 'RESOLVED_BY_CORRECTION' if ids else 'OPEN_UNRESOLVED'
            elif outcome == 'UNCERTAIN':
                resolution = 'OPEN_REVIEW_FLAGGED' if r['review_needed'] else 'OPEN_UNRESOLVED'
            else:
                resolution = 'UPHELD_WITH_FIELD_CORRECTION' if ids else 'NOT_NEEDED'
            out.append({'protocol_version': PROTOCOL_VERSION, 'protocol_addendum': 'A1', 'candidate': c, 'round': int(rnd_s), 'source_key': key,
                        'classification_at_report': r['classification'], 'confidence_at_report': r['confidence'],
                        'classification_challenged': (r['correction_history'][0]['classification_before'] if r['correction_history'] else r['classification']),
                        'outcome': outcome, 'challenge_note': note, 'resolution': resolution, 'resolved_by_corrections': ids})
    write_jsonl_atomic(pc(c, 'SEMANTIC_CHALLENGES.jsonl'), out)
    print('challenges', len(out), dict(Counter(r['outcome'] for r in out)), dict(Counter(r['resolution'] for r in out)))


def validate(c):
    errs, warns = [], []
    rows = load_cls(c)
    view = {source_key(r): r for r in union_view() if r['candidate'] == c}
    keys = [r['source_key'] for r in rows]
    if len(keys) != len(set(keys)):
        errs.append('duplicate source keys')
    if set(keys) != set(view):
        errs.append('key set differs from union view (%d vs %d)' % (len(set(keys)), len(view)))
    for r in rows:
        v = view.get(r['source_key'])
        if v and v['view_record_type'] != r['view_record_type']:
            errs.append('type mismatch ' + r['source_key'])
        for p in r['canonical_policy_ids'] + r['related_policy_ids'] + r['canonical_conflict_ids']:
            if p not in policies():
                errs.append('undefined policy %s in %s' % (p, r['source_key']))
        for s in r.get('subclauses') or []:
            for p in s['canonical_policy_ids']:
                if p not in policies():
                    errs.append('undefined policy %s in %s/%s' % (p, r['source_key'], s['subclause_id']))
        if not r['evidence_refs']:
            errs.append('no evidence ' + r['source_key'])
        cl = r['classification']
        if cl == 'CANONICAL_ONLY' and not (r['canonical_policy_ids'] and r['canonical_entailment_rationale']):
            errs.append('CO without policies/rationale ' + r['source_key'])
        if cl in ('CANONICAL_PLUS_DELTA', 'EXTRA_PRODUCT', 'EXTRA_WORKFLOW') and not (r['extra_fragment'] and r['distinguishing_scenario']):
            errs.append('extra without fragment/scenario ' + r['source_key'])
        if cl == 'MIXED' and len(r['subclauses']) < 2:
            errs.append('MIXED without subclauses ' + r['source_key'])
        if (cl == 'UNCERTAIN' or r['review_needed']) and not r['review_reason']:
            errs.append('review without reason ' + r['source_key'])
        if r['view_record_type'] == 'PROVISIONAL_FACET_OVERLAY' and not r.get('facet_assessment'):
            errs.append('facet without assessment ' + r['source_key'])
        q = r.get('source_quote_verification') or {}
        if q.get('status') not in ('VERIFIED', 'VERIFIED_WITH_RANGE_ONLY_REFS'):
            errs.append('source quote not verified %s: %s' % (r['source_key'], q.get('failures')))
        if r['confidence'] == 'HIGH' and q.get('primary_anchor_status') == 'RANGE_CHECKED_NO_QUOTE':
            warns.append('HIGH confidence with range-only primary anchor ' + r['source_key'])
        if r['trigger_status'] == 'MISSING':
            errs.append('normative record without trigger ' + r['source_key'])
        if r['exceptions_status'] == 'MISSING':
            errs.append('normative record without exceptions statement ' + r['source_key'])
    for key, why in rows_needing_strength_review(rows):
        errs.append('strength unresolved %s: %s' % (key, why))
    cov = read_jsonl(pc(c, 'POLICY_COVERAGE.jsonl')) if os.path.exists(pc(c, 'POLICY_COVERAGE.jsonl')) else []
    if sorted(x['policy_id'] for x in cov) != sorted(policies()):
        errs.append('policy coverage rows != 196 canonical ids')
    od = pc(c, 'ORPHAN_DISPOSITIONS.jsonl')
    if not os.path.exists(od):
        errs.append('ORPHAN_DISPOSITIONS missing')
    elif len(read_jsonl(od)) != len(orphan_items(c)):
        errs.append('orphan dispositions incomplete')
    ch = read_jsonl(pc(c, 'SEMANTIC_CHALLENGES.jsonl')) if os.path.exists(pc(c, 'SEMANTIC_CHALLENGES.jsonl')) else []
    if not ch:
        errs.append('SEMANTIC_CHALLENGES missing')
    for x in ch:
        if x['resolution'] == 'OPEN_UNRESOLVED':
            errs.append('failed semantic challenge left unresolved: %s (%s)' % (x['source_key'], x['outcome']))
    by = {r['source_key']: r for r in rows}
    if os.path.exists(pc(c, 'CORRECTIONS.jsonl')):
        for l in read_jsonl(pc(c, 'CORRECTIONS.jsonl')):
            hist = by.get(l['source_key'], {}).get('correction_history') or []
            if l['correction_id'] not in [h['correction_id'] for h in hist]:
                errs.append('correction %s missing from record history' % l['correction_id'])
    return errs, warns, rows, cov


def counts(items):
    return ', '.join('%s %d' % kv for kv in sorted(Counter(items).items()))


def report(c):
    errs, warns, rows, cov = validate(c)
    status = 'PASS' if not errs else 'FAIL'
    od = read_jsonl(pc(c, 'ORPHAN_DISPOSITIONS.jsonl')) if os.path.exists(pc(c, 'ORPHAN_DISPOSITIONS.jsonl')) else []
    ch = read_jsonl(pc(c, 'SEMANTIC_CHALLENGES.jsonl')) if os.path.exists(pc(c, 'SEMANTIC_CHALLENGES.jsonl')) else []
    corr = read_jsonl(pc(c, 'CORRECTIONS.jsonl')) if os.path.exists(pc(c, 'CORRECTIONS.jsonl')) else []
    div = read_jsonl(pc(c, 'STRENGTH_DIVERGENCES.jsonl')) if os.path.exists(pc(c, 'STRENGTH_DIVERGENCES.jsonl')) else []
    unc = [r for r in rows if r['classification'] == 'UNCERTAIN']
    rev = [r for r in rows if r['review_needed']]
    fhd = [r for r in rows if r.get('future_human_decision')]
    om = [r for r in rows if r.get('potential_overmerge')]
    co = [r for r in rows if r['classification'] == 'CANONICAL_ONLY']
    failed = [x for x in ch if x['outcome'] != 'UPHELD']
    lines = ['# Candidate %s — Step 2 classification report' % c, '',
             'Protocol `%s` with Addendum A1. Mechanical validation: **%s**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).' % (PROTOCOL_VERSION, status), '',
             '## Counts', '',
             '- Records classified: %d (union view: %d).' % (len(rows), len([1 for r in union_view() if r['candidate'] == c])),
             '- By classification: ' + counts(r['classification'] for r in rows),
             '- CANONICAL_ONLY by strength: ' + counts(r['normative_strength_equivalence'] for r in co) + ' (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).',
             '- CANONICAL_ONLY by semantic coverage: ' + counts(r['canonical_semantic_coverage'] for r in co),
             '- By domain: ' + counts(r['domain'] for r in rows),
             '- By oracle relation: ' + counts(r['oracle_relation'] for r in rows),
             '- By confidence: ' + counts(r['confidence'] for r in rows),
             '- Provisional records: ' + counts('%s/%s' % (r['view_record_type'], r['classification']) for r in rows if r['view_record_type'] != 'ORIGINAL_GROUP'),
             '- Source-quote verification: ' + counts(r['source_quote_verification']['status'] for r in rows) + '; primary anchors: ' + counts(r['source_quote_verification']['primary_anchor_status'] for r in rows),
             '', '## Policy coverage (traceability, not compliance)', '',
             '- Semantic coverage: ' + counts(x['status'] for x in cov),
             '- Strength: ' + counts(x['strength_status'] for x in cov),
             '- Non-DIRECT policies: ' + (', '.join('%s (%s)' % (x['policy_id'], x['status']) for x in cov if x['status'] != 'DIRECT_EVIDENCE') or 'none'),
             '- Policies without equal-strength evidence: ' + (', '.join('%s (%s)' % (x['policy_id'], x['strength_status']) for x in cov if x['strength_status'] != 'EQUIVALENT_EVIDENCE_PRESENT') or 'none'),
             '- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: %d (%s).' % (len(div), counts(d['normative_strength_equivalence'] for d in div)),
             '', '## Corrections', '',
             '- Corrections applied: %d on %d records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: %d.' % (
                 len(corr), len({l['source_key'] for l in corr}), len([l for l in corr if l['classification_before'] != l['classification_after']])),
             '- By finding: ' + (counts(l['finding_ref'] for l in corr) or 'none')]
    for l in corr:
        if l['classification_before'] != l['classification_after']:
            lines.append('  - `%s` %s: %s -> %s. %s' % (l['source_key'], l['correction_id'], l['classification_before'], l['classification_after'], l['reason'][:170]))
    lines += ['', '## Open and uncertain items', '',
              '- UNCERTAIN classifications: %d; records with review_needed: %d; future human decisions: %d; potential Step-1 overmerges flagged: %d.' % (len(unc), len(rev), len(fhd), len(om))]
    for r in unc:
        lines.append('  - `%s`: %s' % (r['source_key'], (r['review_reason'] or '')[:220]))
    lines += ['', '## Orphan and queue closure', '',
              '- Items reviewed: %d — ' % len(od) + counts(x['disposition'] for x in od)]
    for x in od:
        if x['disposition'] == 'QUEUE':
            lines.append('  - QUEUE `%s`: %s' % (x['item_id'], x['note'][:200]))
    lines += ['', '## Semantic challenge sample', '',
              '- %d challenged: ' % len(ch) + counts(x['outcome'] for x in ch) + '. Resolution: ' + counts(x['resolution'] for x in ch) + '.',
              '- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.']
    for x in failed:
        lines.append('  - %s `%s` (round %d, challenged as %s, now %s): %s [%s %s]' % (
            x['outcome'], x['source_key'], x['round'], x['classification_challenged'], x['classification_at_report'], x['challenge_note'][:170], x['resolution'], ','.join(x['resolved_by_corrections'])))
    lines += ['', '## Validation', '']
    lines += ['- ERROR: ' + e for e in errs] or ['- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.']
    lines += ['- WARNING: ' + w for w in warns[:20]]
    lines.append('')
    with open(pc(c, 'CANDIDATE_REPORT.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    files = ['CLASSIFICATIONS.jsonl', 'POLICY_COVERAGE.jsonl', 'ORPHAN_DISPOSITIONS.jsonl', 'SEMANTIC_CHALLENGES.jsonl', 'STRENGTH_DIVERGENCES.jsonl', 'CORRECTIONS.jsonl', 'CORRECTED_RECORDS.jsonl', 'CANDIDATE_REPORT.md']
    write_json_atomic(os.path.join(OUT, 'CHECKPOINTS', c, 'CANDIDATE.checkpoint.json'), {
        'protocol_version': PROTOCOL_VERSION, 'protocol_addendum': 'A1', 'candidate': c,
        'status': 'COMPLETE' if status == 'PASS' else 'FAILED_VALIDATION',
        'validator': status, 'errors': errs, 'warnings': warns[:50], 'n_records': len(rows),
        'open_failed_challenges': [x['source_key'] for x in ch if x['resolution'] == 'OPEN_UNRESOLVED'],
        'files': {f: sha256_file(pc(c, f)) for f in files if os.path.exists(pc(c, f))},
        'at': time.strftime('%Y-%m-%dT%H:%M:%S')})
    print(status, len(errs), 'errors', len(warns), 'warnings')
    for e in errs[:40]:
        print(' ', e)


def finish(c):
    assemble(c)
    coverage(c)
    orphans(c, '--build')
    challenge(c, '--build')
    assemble(c)
    coverage(c)
    report(c)


def main():
    c, cmd = sys.argv[1], sys.argv[2]
    if cmd == 'assemble':
        assemble(c)
    elif cmd == 'strength':
        strength(c)
    elif cmd == 'coverage':
        coverage(c, '--view' in sys.argv)
    elif cmd == 'orphans':
        orphans(c, sys.argv[3])
    elif cmd == 'challenge':
        args = sys.argv[3:]
        rnd = int(args[args.index('--round') + 1]) if '--round' in args else 1
        nums = [a for i, a in enumerate(args) if a.isdigit() and (i == 0 or args[i - 1] != '--round')]
        only = args[args.index('--only') + 1] if '--only' in args else None
        challenge(c, args[0], int(nums[0]) if nums else 3, rnd, only)
    elif cmd == 'finish':
        finish(c)
    elif cmd == 'report':
        report(c)


if __name__ == '__main__':
    main()
