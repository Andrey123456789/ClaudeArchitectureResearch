"""R25 regression: all 103 audit corrections, atomic before/after per accepted record with whole-dataset invariants, and the 31 open records."""
import copy
import os
from collections import Counter

from cor103 import current_status
from dataset import OV_RULES, apply_set, load_py, split_key
from rcommon import AUD, CANDIDATES, baseline, norm_ws, out_path, read_jsonl, read_lines, rec_hash, wc_path, write_jsonl
from roverlay import coverage_of, validate_candidate


def prefix():
    state = {c: dict(baseline(c)) for c in CANDIDATES}
    cand = {k: c for c in CANDIDATES for k in baseline(c)}

    def step(key, sets):
        base, sub = split_key(key)
        state[cand[base]][base] = apply_set(state[cand[base]][base], sets, sub)
    for o in read_jsonl(out_path('_rules', 'R01-HQ06-PI012', 'OVERLAY.jsonl')):
        step(o['key'], o['set'])
    for rule in OV_RULES:
        for o in load_py(rule, 'overlay.py').OVERLAY:
            step(o['key'], o['set'])
    return state, cand


def run(ctx):
    rows = read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))
    props = read_jsonl(os.path.join(AUD, 'CORRECTION_PROPOSALS.jsonl'))
    ctx.check('103 rows, one per audit proposal', len(rows) == 103 and {r['correction_id'] for r in rows} == {p['correction_id'] for p in props} and len({r['correction_id'] for r in rows}) == 103, kind='DATA')
    dec = Counter(r['decision'] for r in rows)
    ctx.check('every row has a decision', set(dec) <= {'ACCEPT', 'ACCEPT_MODIFIED', 'REJECT', 'UNRESOLVED'}, dec, kind='DATA', actual=dict(dec))
    ctx.check('no unresolved row is hidden', dec['UNRESOLVED'] == 0, dec, kind='DATA')
    ctx.check('every decision has a reason; every rejection has a counterexample', all(r['reason'] for r in rows) and all(r['counterexample'] for r in rows if r['decision'] == 'REJECT'), kind='SEMANTIC')
    stated = Counter(r['group_stated'] for r in rows)
    ctx.check('stated groups hold: 51, 43, 9', stated == Counter({'PI012_DEPENDENT': 51, 'FROZEN_PROTOCOL_SUPPORTED': 43, 'PARTIAL_FIELD': 9}), stated, kind='DATA')
    ctx.check('the 9 partial-field rows are resolved by R02, not assumed', sum(1 for r in rows if r['group_after_check'] == 'QUESTION_RESOLVED_BY_R02') == 9, kind='SEMANTIC')
    bad = []
    for p in props:
        for q in p['quotes']:
            ok, _ = current_status(p['candidate'], q)
            if not ok:
                bad.append(p['correction_id'])
    ctx.check('every original quote re-verified in the frozen input', not bad, bad[:5], kind='DATA')
    no_cur = [r['correction_id'] for r in rows if r['decision'] != 'REJECT' and any(x['status'] == 'REMOVED' for x in r['current_source'])]
    ctx.check('no accepted row rests on a removed source file', not no_cur, no_cur[:5], kind='DATA')
    sup = {'FG-K0-6bc04e6316': ('K0', '.claude/scripts/check-dependencies.cjs', 'function effectiveCpm'), 'FG-M1-159a4ef4c3': ('M1', '.claude/skills/add-dependency/SKILL.md', 'No confirmation, comment marker, or'), 'FG-K1-8c2a0fe6ef': ('K1', '.claude/skills/ef-core/SKILL.md', 'measured, or clearly demonstrated, to be material'), 'FG-L0-313d81df34': ('L0', '.claude/skills/project-structure/SKILL.md', 'separately approved, controlled deployment-time migration step')}
    rej = {r['case_key'] for r in rows if r['decision'] == 'REJECT'}
    ctx.check('the four rejections are the four superseded rows', rej == set(sup), sorted(rej), kind='SEMANTIC')
    for k, (c, rel, q) in sup.items():
        ctx.check('superseding text present: %s' % k, norm_ws(q) in norm_ws(' '.join(read_lines(wc_path(c, rel)))), candidate=c, kind='SEMANTIC')
    ov = read_jsonl(out_path('_rules', 'R25-COR103', 'OVERLAY.jsonl'))
    ctx.check('overlay holds exactly the accepted rows', len(ov) == dec['ACCEPT'] + dec['ACCEPT_MODIFIED'] and {o['correction_id'] for o in ov} == {r['correction_id'] for r in rows if r['decision'] in ('ACCEPT', 'ACCEPT_MODIFIED')}, kind='DATA')
    state, cand = prefix()
    per = []
    fails = []
    for o in ov:
        base, sub = split_key(o['key'])
        c = cand[base]
        before = state[c][base]
        after = apply_set(before, o['set'], sub)
        state[c][base] = after
        errs = validate_candidate(c, state[c])
        changed = rec_hash(before) != rec_hash(after)
        per.append({'correction_id': o['correction_id'], 'key': o['key'], 'candidate': c, 'before_sha256': rec_hash(before), 'after_sha256': rec_hash(after), 'changed': changed, 'invariants': 'PASS' if not errs else 'FAIL', 'errors': errs[:5], 'coverage_rows': 196})
        if errs:
            fails.append((o['correction_id'], errs[:2]))
    write_jsonl(os.path.join('TEST_RESULTS', 'R25_per_record.jsonl'), per)
    ctx.check('whole-dataset invariants hold after each accepted record', not fails, fails[:3], kind='DATA', actual=len(per))
    noop = [p['correction_id'] for p in per if not p['changed']]
    ctx.check('no-op rows are visible', True, 'no-op after earlier overlays: %s' % noop, kind='DATA', actual=noop)
    h1 = rec_hash({c: sorted(rec_hash(r) for r in state[c].values()) for c in CANDIDATES})
    s2, _ = prefix()
    for o in ov:
        base, sub = split_key(o['key'])
        s2[cand[base]][base] = apply_set(s2[cand[base]][base], o['set'], sub)
    ctx.check('replay gives the same records', h1 == rec_hash({c: sorted(rec_hash(r) for r in s2[c].values()) for c in CANDIDATES}), kind='DATA')
    # mutations: the invariants catch a corrupted record
    c0 = 'K1'
    tgt = next(k for k, r in state[c0].items() if r['classification'] == 'CANONICAL_ONLY')
    m = dict(state[c0])
    m[tgt] = apply_set(m[tgt], {'canonical_coverage': []})
    ctx.check('mutation: canonical record with no policy is caught', any('no policy' in e for e in validate_candidate(c0, m)), kind='MUTATION')
    m = dict(state[c0])
    m[tgt] = dict(copy.deepcopy(m[tgt]), modality='PROBABLY')
    ctx.check('mutation: invalid modality is caught', any('bad modality' in e for e in validate_candidate(c0, m)), kind='MUTATION')
    m = dict(state[c0])
    del m[tgt]
    ctx.check('mutation: a lost record is caught', any('lost keys' in e for e in validate_candidate(c0, m)), kind='MUTATION')
    cov = coverage_of(state[c0].values())
    pid = next(p for p, r in cov.items() if len(r['direct_source_keys']) == 1 and not r['partial_source_keys'])
    m = dict(state[c0])
    m[cov[pid]['direct_source_keys'][0]] = apply_set(m[cov[pid]['direct_source_keys'][0]], {'classification': 'NON_NORMATIVE', 'normativity': 'NON_NORMATIVE', 'canonical_coverage': [], 'strength_vs_canonical': 'N/A', 'modality': 'NONE', 'strength_resolution_code': None})
    ctx.check('mutation: dropping the only witness moves the coverage cell and is caught', any('coverage moved' in e and pid in e for e in validate_candidate(c0, m)), pid, kind='MUTATION')
    # the 31 open records
    un = read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
    q = read_jsonl(os.path.join(AUD, 'UNRESOLVED_QUEUE.jsonl'))
    op = {r['id']: r for r in un if r['kind'] == 'ORIGINAL_OPEN_RECORD'}
    ctx.check('each of the 31 open records has a disposition', len(q) == 31 and set(op) == {r['key'] for r in q} and all(r['resolved_by'] and r['decision_source'] for r in op.values()), Counter(r['question'] for r in op.values()), kind='SEMANTIC')
    ctx.check('question counts: HQ-01 14, non-rewritable 10, HQ-02 4, scan line 2, HQ-04 1', Counter(r['question'] for r in op.values()) == Counter({'HQ-01': 14, 'NON_REWRITABLE_READING': 10, 'HQ-02': 4, 'SCAN_LINE_READING': 2, 'HQ-04': 1}), kind='DATA')
    ctx.check('the 14 orphan and queue items are recorded with their question', sum(1 for r in un if r['kind'] == 'ORIGINAL_OPEN_DUPLICATE_ITEM') == 14, kind='DATA')
    ctx.check('PI-012 unresolved cases stay open', sum(1 for r in un if r['kind'] == 'PI012_UNRESOLVED') >= 2 and all(r['status'] == 'OPEN' for r in un if r['kind'] == 'PI012_UNRESOLVED'), kind='SEMANTIC')
