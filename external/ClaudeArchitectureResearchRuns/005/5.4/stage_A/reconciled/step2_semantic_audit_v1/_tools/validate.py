"""Deterministic gates for the Step 2 semantic audit.

  python -B _tools/validate.py          runs every gate and writes VALIDATION_RESULT.json (exit 1 on any FAIL)
  python -B _tools/validate.py --no-write   same, without writing

Gates read files; none is passed by hand. A failed gate gives BLOCKED. A pass means the checks hold, not that readings are right.
"""
import json
import os
import re
import sys
import time
from collections import Counter

from acommon import CANDIDATES, DEC, EXPECTED_RECORDS, OUT, ROOT, S2, TOOLS, baseline, canon, coverage, norm_ws, out_path, policies, read_jsonl, rec_hash, sha256_file, source_range, utf8_stdout, write_json
from dsl import load_blind, load_decisions, verify_quote
from overlay import coverage_of, replay
from preflight import verify as verify_upstream
from targets import SPECIAL_CELLS, compute, override_rows

STRIP = ('audit_overlay', 'audit_subclauses')


class Gates:
    def __init__(self):
        self.items = []

    def add(self, gate, errors, detail=None):
        self.items.append({'gate': gate, 'status': 'PASS' if not errors else 'FAIL', 'n_errors': len(errors), 'errors': errors[:40], 'detail': detail})


def load(name):
    return read_jsonl(out_path(name))


def upstream(g):
    r = verify_upstream(quiet=True)
    errs = ['changed ' + x for x in r['changed']] + ['missing ' + x for x in r['missing']] + ['added ' + x for x in r['added']]
    g.add('ALL_UPSTREAM_INPUTS_UNCHANGED', errs, {'n_checked': r['n_checked'], 'scope': 'inputs/, step1_union, step1_union_augmented_pass1, step2_classification'})


def accounted(g):
    ledger = {r['case_id']: r for r in load('AUDIT_LEDGER.jsonl')}
    errs = []
    n = [x for x in read_jsonl(os.path.join(S2, '_decisions', 'A13_AUDIT_FINDINGS.jsonl')) if x['category'] == 'N']
    om = read_jsonl(os.path.join(S2, 'POTENTIAL_OVERMERGES.jsonl'))
    unc = read_jsonl(os.path.join(S2, 'UNCERTAIN_CLASSIFICATIONS.jsonl'))
    orp = read_jsonl(os.path.join(S2, 'ORPHAN_REVIEW_QUEUE.jsonl'))
    fhd = read_jsonl(os.path.join(S2, 'FUTURE_HUMAN_DECISIONS.jsonl'))
    ov = override_rows()
    expect = {'PI012_N': (len(n), 79), 'OVERMERGE': (len(om), 33), 'UNCERTAIN_LIST': (len(unc), 91), 'ORPHAN': (len(orp), 21), 'FHD': (len(fhd), 24), 'COVERAGE_OVERRIDE': (len(ov), 38), 'STRENGTH_SPECIAL_5': (len(SPECIAL_CELLS), 5),
              'UNCERTAIN_RECORD': (sum('UNCERTAIN_RECORD' in x['reasons'] for x in unc), 19), 'UNCERTAIN_SUBCLAUSE': (sum('UNCERTAIN_SUBCLAUSE' in x['reasons'] for x in unc), 4),
              'LOW_CONFIDENCE': (sum('LOW_CONFIDENCE' in x['reasons'] for x in unc), 33), 'REVIEW_NEEDED': (sum('REVIEW_NEEDED' in x['reasons'] for x in unc), 90)}
    for k, (got, want) in expect.items():
        if got != want:
            errs.append('%s count %d expected %d' % (k, got, want))
    keys = [('REC:' + x['key']) for x in n] + [('REC:' + x['source_key']) for x in om + unc + fhd] + [('ORP:' + x['item_id']) for x in orp] + [('COV:%s:%s' % cell) for cell in ov + SPECIAL_CELLS]
    for k in keys:
        if k not in ledger:
            errs.append('no ledger row: ' + k)
        elif ledger[k].get('decision') not in ('UPHOLD', 'CORRECT', 'UNRESOLVED', 'NOT_A_SEPARATE_CLAUSE', 'OVERMERGE_FACET', 'EVIDENCE_CONFLICT'):
            errs.append('no decision: ' + k)
    pi = load('PI012_NEGATIVE_MODALITY_REVIEW.jsonl')
    if len(pi) != 79 or {r['key'] for r in pi} != {x['key'] for x in n}:
        errs.append('PI012 review does not match the 79')
    if len(load('OVERMERGE_REVIEW.jsonl')) != 33:
        errs.append('overmerge review not 33')
    if len(load('ORPHAN_REVIEW.jsonl')) != 21:
        errs.append('orphan review not 21')
    if len(load('COVERAGE_OVERRIDE_REVIEW.jsonl')) != 43:
        errs.append('coverage review not 43')
    if len(load('FHD_REVIEW.jsonl')) != 24:
        errs.append('FHD review not 24')
    missing = [r['case_id'] for r in ledger.values() if r.get('audit_status') == 'MISSING_DECISION']
    errs += ['missing decision: ' + m for m in missing]
    g.add('AUDIT_TARGETS_EXHAUSTIVELY_ACCOUNTED', errs, {k: v[0] for k, v in expect.items()} | {'ledger_rows': len(ledger)})


def sample(g):
    errs = []
    plan_frozen = json.load(open(out_path('SAMPLING_PLAN.json'), encoding='utf-8'))
    plan_now, _ = compute()
    for k in ('samples', 'm_calibration', 'queue_sample', 'drift_sample'):
        if canon(plan_frozen[k]) != canon(plan_now[k]):
            errs.append('selection not reproducible: ' + k)
    dec, blind = load_decisions(), load_blind()
    log = read_jsonl(out_path('CHECKPOINTS', 'BLIND_LOG.jsonl'))
    hashes = {}
    for row in log:
        hashes.setdefault(row['batch'], set()).add(row['blind_sha256'])
    for c, xs in plan_frozen['samples'].items():
        if len(xs) < 24:
            errs.append('%s sample below 24' % c)
    for c, xs in list(plan_frozen['samples'].items()) + [('M', plan_frozen['m_calibration'])]:
        for s in xs:
            k = s['source_key']
            if k not in blind:
                errs.append('no blind reading: ' + k)
            if k not in dec:
                errs.append('no decision: ' + k)
    if len(plan_frozen['m_calibration']) < 8 or not {'FG-M-22cae42396', 'FG-M-1c4fc44b5e', 'FG-M-d0b6a09cce'} <= {x['source_key'] for x in plan_frozen['m_calibration']}:
        errs.append('M calibration incomplete')
    if len(plan_frozen['queue_sample']) < 48 or any(v < 8 for v in Counter(x['candidate'] for x in plan_frozen['queue_sample']).values()):
        errs.append('queue sample below 48 or 8 per candidate')
    for x in plan_frozen['queue_sample']:
        if 'QUE:' + x['queue_id'] not in dec:
            errs.append('no queue decision ' + x['queue_id'])
    batches = {b['batch'] for b in blind.values()}
    for b in batches:
        if sha256_file(os.path.join(DEC, b + '.blind')) not in hashes.get(b, set()):
            errs.append('blind file changed after reveal or never logged: ' + b)
    if not all(hashes.get(b) for b in batches):
        errs.append('batch without a reveal log')
    if plan_frozen['shortfalls'] or plan_frozen['queue_shortfalls']:
        errs.append('shortfalls exist without note')
    g.add('INDEPENDENT_SAMPLE_FROZEN_AND_READ', errs, {'samples': {c: len(v) for c, v in plan_frozen['samples'].items()}, 'm_calibration': len(plan_frozen['m_calibration']), 'queue': len(plan_frozen['queue_sample']), 'blind_batches': len(batches)})


def quotes(g):
    errs, n = [], 0
    cors = load('CORRECTION_PROPOSALS.jsonl')
    ncp = load('NEW_CLAUSE_PROPOSALS.jsonl')
    for row in cors + ncp:
        qs = row.get('quotes') or row.get('evidence')
        if not qs:
            errs.append('no quote: %s' % (row.get('correction_id') or row.get('proposal_id')))
        for q in qs or []:
            n += 1
            if norm_ws(q['quote']) not in norm_ws(source_range(q['path'], q['start_line'], q['end_line'])):
                errs.append('quote not in source: %s %s:%s' % (row.get('correction_id') or row.get('proposal_id'), q['path'], q['start_line']))
    for row in load('AUDIT_LEDGER.jsonl'):
        for q in row.get('source') or []:
            if q.get('verified') is False:
                errs.append('unverified quote in ledger ' + row['case_id'])
    g.add('ALL_QUOTES_SOURCE_VERIFIED', errs, {'quotes_checked': n, 'corrections': len(cors), 'new_clause_proposals': len(ncp)})


def effective(g):
    eff_rows = load('EFFECTIVE_CLASSIFICATIONS.jsonl')
    cov_rows = load('EFFECTIVE_POLICY_COVERAGE.jsonl')
    cors = load('CORRECTION_PROPOSALS.jsonl')
    errs_silent, errs_ident, errs_replay, errs_unc = [], [], [], []
    # identities
    keys = [r['source_key'] for r in eff_rows]
    if len(keys) != 6402 or len(set(keys)) != 6402:
        errs_ident.append('records %d unique %d' % (len(keys), len(set(keys))))
    for c in CANDIDATES:
        ks = {r['source_key'] for r in eff_rows if r['candidate'] == c}
        if ks != set(baseline(c)) or len(ks) != EXPECTED_RECORDS[c]:
            errs_ident.append('candidate identity set differs: ' + c)
    cells = [(r['candidate'], r['policy_id']) for r in cov_rows]
    if len(cells) != 1176 or len(set(cells)) != 1176:
        errs_ident.append('coverage rows %d unique %d' % (len(cells), len(set(cells))))
    # no silent reclassification: differing rows are exactly the corrected rows
    corrected = {c['source_key'] for c in cors}
    by_key = {r['source_key']: r for r in eff_rows}
    for c in CANDIDATES:
        for k, b in baseline(c).items():
            r = dict(by_key[k])
            ov = r.pop('audit_overlay', None)
            r.pop('audit_subclauses', None)
            same = canon(r) == canon(b)
            has_extra = 'audit_subclauses' in by_key[k]
            if k in corrected and same and not has_extra:
                errs_silent.append('correction with no effect: ' + k)
            if k not in corrected and (not same or has_extra):
                errs_silent.append('changed with no correction: ' + k)
            if ov is None or ov['baseline_record_sha256'] != rec_hash(b):
                errs_silent.append('baseline hash mismatch: ' + k)
    for row in cors:
        if 'PROPOSED' not in row['ratification'] or 'RATIFIED' in row['ratification']:
            errs_silent.append('ratification word: ' + row['correction_id'])
        if row['depends_on'] == 'PI012' and row['ratification'] != 'PROPOSED_PENDING_METHODOLOGY_PI012':
            errs_silent.append('methodology dependence not marked: ' + row['correction_id'])
        if not row['changed_fields'] and 'subclauses_add' not in row['set']:
            errs_silent.append('empty before/after: ' + row['correction_id'])
    # replay
    eff = replay(cors, CANDIDATES)
    for c in CANDIDATES:
        for k, r in eff[c].items():
            e = dict(by_key[k])
            e.pop('audit_overlay', None)
            if canon(e) != canon(r):
                errs_replay.append('replay differs: ' + k)
    man = json.load(open(out_path('EFFECTIVE_VIEW_MANIFEST.json'), encoding='utf-8'))
    for f, h in man['view_sha256'].items():
        if sha256_file(out_path(f)) != h:
            errs_replay.append('manifest hash differs: ' + f)
    for c in CANDIDATES:
        for f, h in man['baseline_sha256'][c].items():
            if sha256_file(os.path.join(S2, 'per_candidate', c, f)) != h:
                errs_replay.append('baseline hash differs: %s %s' % (c, f))
    # coverage recompute
    errs_cov = []
    for c in CANDIDATES:
        base_cov = coverage_of(list(baseline(c).values()))
        for p, row in coverage(c).items():
            for f in ('computed_status', 'strength_status', 'direct_source_keys', 'strength_equivalent_source_keys', 'weaker_source_keys', 'stronger_source_keys', 'partial_source_keys'):
                if canon(base_cov[p][f]) != canon(row[f]):
                    errs_cov.append('engine does not reproduce baseline %s %s %s' % (c, p, f))
        ev = coverage_of(list(eff[c].values()))
        for row in (r for r in cov_rows if r['candidate'] == c):
            p = row['policy_id']
            if row['strength_status'] != ev[p]['strength_status'] or row['computed_status'] != ev[p]['computed_status']:
                errs_cov.append('effective coverage differs %s %s' % (c, p))
            if row['audit_overlay']['baseline_row_sha256'] != rec_hash(coverage(c)[p]):
                errs_cov.append('coverage baseline hash %s %s' % (c, p))
            if coverage(c)[p].get('reviewer_override_note') and row.get('reviewer_override_note') != coverage(c)[p].get('reviewer_override_note'):
                errs_cov.append('override note lost %s %s' % (c, p))
            if coverage(c)[p].get('reviewer_override_note') and not row['audit_overlay']['flags']:
                errs_cov.append('override row without review flag %s %s' % (c, p))
    # uncertain not forced
    dec = load_decisions()
    for k, x in dec.items():
        if x['decision'] == 'UNRESOLVED':
            base = k.split('/')[0]
            if k.startswith(('ORP:', 'QUE:')):
                continue
            if base in corrected and x['set']:
                errs_unc.append('UNRESOLVED carries a correction: ' + k)
            if by_key[base]['classification'] != baseline(by_key[base]['candidate'])[base]['classification']:
                errs_unc.append('UNRESOLVED changed label: ' + k)
            if not x['alt']:
                errs_unc.append('UNRESOLVED has no alternatives: ' + k)
    baseline_un = {k for c in CANDIDATES for k, r in baseline(c).items() if r['classification'] == 'UNCERTAIN'}
    for k in baseline_un:
        r = by_key[k]
        if r['classification'] != 'UNCERTAIN':
            cs = [c for c in cors if c['source_key'] == k]
            if not cs or not all(c['alternatives'] or c['confidence'] == 'HIGH' for c in cs):
                errs_unc.append('UNCERTAIN resolved without a recorded alternative or HIGH basis: ' + k)
    g.add('NO_SILENT_RECLASSIFICATION', errs_silent, {'corrected_records': len(corrected), 'corrections': len(cors)})
    g.add('BASELINE_6402_1176_IDENTITIES_PRESERVED', errs_ident, {'records': len(keys), 'coverage_rows': len(cells)})
    g.add('OVERLAY_REPLAYABLE', errs_replay, {'method': 'baseline plus CORRECTION_PROPOSALS rows gives EFFECTIVE_CLASSIFICATIONS exactly, ignoring audit_overlay'})
    g.add('COVERAGE_ENGINE_AND_OVERRIDE_LINEAGE', errs_cov, {'method': 'overlay.coverage_of on baseline reproduces every stored row; effective rows equal the recompute; override notes kept and reviewed'})
    g.add('UNCERTAIN_NOT_FORCED', errs_unc, {'effective_uncertain': sum(1 for r in eff_rows if r['classification'] == 'UNCERTAIN'), 'baseline_uncertain': len(baseline_un)})


def references(g):
    errs = []
    pol = set(policies())
    all_keys = {k for c in CANDIDATES for k in baseline(c)}
    for row in load('CORRECTION_PROPOSALS.jsonl'):
        if row['source_key'] not in all_keys:
            errs.append('unknown key ' + row['source_key'])
        for f in ('canonical_coverage',):
            for x in row['set'].get(f) or []:
                if x['policy_id'] not in pol:
                    errs.append('unknown policy ' + x['policy_id'])
        for s in (row['set'].get('subclauses') or []) + (row['set'].get('subclauses_add') or []):
            for x in s.get('canonical_coverage') or []:
                if x['policy_id'] not in pol:
                    errs.append('unknown policy ' + x['policy_id'])
        for p in row['set'].get('related_policy_ids') or []:
            if p not in pol:
                errs.append('unknown policy ' + p)
    for r in load('EFFECTIVE_CLASSIFICATIONS.jsonl'):
        for e in r['evidence_refs']:
            if source_range(e['path'], e['start_line'], e['end_line']) is None:
                errs.append('bad range ' + r['source_key'])
        cov = r.get('canonical_coverage') or []
        if r['classification'] == 'CANONICAL_ONLY':
            if not cov:
                errs.append('CO with no link ' + r['source_key'])
            if r['normative_strength_equivalence'] == 'STRONGER_THAN_CANONICAL':
                errs.append('CO stronger ' + r['source_key'])
        if r['classification'] == 'CANONICAL_PLUS_DELTA' and not r.get('extra_fragment'):
            errs.append('CD with no remainder ' + r['source_key'])
        if r['classification'] in ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW') and not r.get('distinguishing_scenario'):
            errs.append('EXTRA with no scenario ' + r['source_key'])
        if r['normative_strength_equivalence'] == 'WEAKER_THAN_CANONICAL' and r['classification'] == 'CANONICAL_ONLY' and (r.get('strength_resolution') or {}).get('code') not in ('AM', 'GR', 'CN', 'PM'):
            errs.append('weaker with no weaker code ' + r['source_key'])
    g.add('REFERENCES_RANGES_AND_RECORD_RULES', errs, None)


def scope(g):
    errs_pass2, errs_writes, errs_step3, errs_lim = [], [], [], []
    needle = 'codex_iterative' + '_search'
    for f in os.listdir(TOOLS):
        if f.endswith('.py') and needle in open(os.path.join(TOOLS, f), encoding='utf-8').read():
            errs_pass2.append('tool names the Pass 2 path: ' + f)
    for f in os.listdir(OUT):
        p = os.path.join(OUT, f)
        if os.path.isfile(p) and f.endswith(('.jsonl', '.md')) and os.path.getsize(p) < 40_000_000:
            with open(p, encoding='utf-8') as fh:
                t = fh.read()
            if 'pass_0002' in t:
                errs_pass2.append('Pass 2 reference in ' + f)
    try:
        out_path('..', 'step2_classification', 'x')
        errs_writes.append('write fence did not refuse an upstream path')
    except SystemExit:
        pass
    r = verify_upstream(quiet=True)
    if r['changed'] or r['missing'] or r['added']:
        errs_writes.append('upstream differs from manifest')
    names = ' '.join(os.listdir(OUT)).lower()
    if 'step3' in names or 'unified' in names or 'unification' in names:
        errs_step3.append('an output name suggests Step 3 or unification')
    rep = out_path('SEMANTIC_AUDIT_REPORT.md')
    if os.path.exists(rep):
        t = open(rep, encoding='utf-8').read()
        for needed in ('## Limitations', 'CONDITIONAL_GO', 'not an unbiased', 'Stop'):
            if needed not in t:
                errs_lim.append('report lacks: ' + needed)
    else:
        errs_lim.append('report missing')
    for f in ('METHODOLOGY_NOTE.md', 'DRIFT_DIAGNOSTIC.md', 'SWAGGER_UI_REVIEW.md', 'STATUS.json', 'SAMPLING_PLAN.json', 'AUDIT_TARGETS.jsonl', 'AUDIT_LEDGER.jsonl', 'CORRECTION_PROPOSALS.jsonl', 'NEW_CLAUSE_PROPOSALS.jsonl', 'UNRESOLVED_QUEUE.jsonl', 'HUMAN_DECISION_QUEUE.jsonl', 'PI012_NEGATIVE_MODALITY_REVIEW.jsonl', 'COVERAGE_OVERRIDE_REVIEW.jsonl', 'OVERMERGE_REVIEW.jsonl', 'ORPHAN_REVIEW.jsonl', 'QUEUE_SAMPLE_REVIEW.jsonl', 'EFFECTIVE_CLASSIFICATIONS.jsonl', 'EFFECTIVE_POLICY_COVERAGE.jsonl', 'EFFECTIVE_VIEW_MANIFEST.json'):
        if not os.path.exists(out_path(f)):
            errs_lim.append('missing deliverable: ' + f)
    g.add('NO_PASS2_IMPORTED', errs_pass2, None)
    g.add('NO_SOURCE_TEMPLATE_OR_ORIGINAL_STEP2_WRITES', errs_writes, None)
    g.add('NO_STEP3_OR_UNIFICATION', errs_step3, None)
    g.add('LIMITATIONS_REPORTED', errs_lim, None)


def main():
    utf8_stdout()
    g = Gates()
    upstream(g)
    accounted(g)
    sample(g)
    quotes(g)
    effective(g)
    references(g)
    scope(g)
    failed = [x['gate'] for x in g.items if x['status'] != 'PASS']
    n_open = len(load('UNRESOLVED_QUEUE.jsonl')) if os.path.exists(out_path('UNRESOLVED_QUEUE.jsonl')) else 0
    n_hq = len(load('HUMAN_DECISION_QUEUE.jsonl')) if os.path.exists(out_path('HUMAN_DECISION_QUEUE.jsonl')) else 0
    outcome = 'BLOCKED' if failed else ('PASS_WITH_OPEN_ISSUES' if n_open or n_hq else 'PASS')
    res = {'validator': '_tools/validate.py', 'status': 'PASS' if not failed else 'BLOCKED', 'audit_outcome': outcome, 'open_records': n_open, 'human_questions': n_hq, 'failed_gates': failed, 'at': time.strftime('%Y-%m-%dT%H:%M:%S'),
           'meaning': 'Mechanical gates pass or fail on files. A PASS does not prove any reading is right, and open questions stay open: see SEMANTIC_AUDIT_REPORT.md.', 'gates': g.items}
    if '--no-write' not in sys.argv:
        write_json('VALIDATION_RESULT.json', res)
    for x in g.items:
        print(x['status'], x['gate'], x['n_errors'], (x['errors'][:4] if x['errors'] else ''))
    print('OVERALL', res['status'], res['audit_outcome'], 'open', n_open, 'questions', n_hq)
    raise SystemExit(0 if not failed else 1)


if __name__ == '__main__':
    main()
