"""Tests for the audit tools, including that the checks catch tampering.

  python -B _tools/test_tools.py

Uses in-memory data only. It writes nothing except PREFLIGHT/TOOL_TESTS.json.
"""
import copy
import json
import sys

from acommon import CANDIDATES, baseline, canon, coverage, norm_ws, out_path, rec_hash, source_range, utf8_stdout, write_json
from dsl import parse_blind_line, parse_pol, parse_value, verify_quote
from overlay import apply_set, coverage_of, recompute_strength, replay

RESULTS = []


def check(name, cond):
    RESULTS.append({'test': name, 'pass': bool(cond)})
    print('PASS' if cond else 'FAIL', name)


def main():
    utf8_stdout()
    # write fence
    try:
        out_path('..', 'step2_classification', 'CLASSIFICATION_PROTOCOL.md')
        check('write fence refuses an upstream path', False)
    except SystemExit:
        check('write fence refuses an upstream path', True)
    # parser
    check('parse_pol reads partial marks', parse_pol('WF-005~,API-016') == [{'policy_id': 'WF-005', 'coverage': 'PARTIAL'}, {'policy_id': 'API-016', 'coverage': 'FULL'}])
    check('parse_pol treats empty forms as none', parse_pol('-') == [] and parse_pol('[]') == [] and parse_value('canonical_coverage', '[]') == [])
    b = parse_blind_line('KEY || cls=CD mod=DEFAULT dom=WF rel=PE pol=WF-006~ conf=M || actor=a; act=b; trig=c; scope=d; exc=e; time=f; enf=g || test=h', 't')
    check('blind line parses', b['classification'] == 'CANONICAL_PLUS_DELTA' and b['facts']['trigger'] == 'c' and b['entailment_test'] == 'h')
    try:
        parse_blind_line('KEY || cls=CD conf=M || actor=a || test=h', 't')
        check('blind line missing fields is refused', False)
    except SystemExit:
        check('blind line missing fields is refused', True)
    # quote verification
    good = {'path': '.claude/skills/swagger/SKILL.md', 'start_line': 70, 'end_line': 70, 'quote': 'open the Development Swagger UI and confirm it loads'}
    bad = dict(good, quote='open the Production Swagger UI')
    check('real quote verifies', verify_quote('K1', good)[1])
    check('false quote fails', not verify_quote('K1', bad)[1])
    # overlay
    k = 'FG-K1-2b15ea3da2'
    base = baseline('K1')[k]
    keep = rec_hash(base)
    after = apply_set(base, {'classification': 'CANONICAL_PLUS_DELTA', 'oracle_relation': 'PARTIALLY_ENTAILED', 'strength_vs_canonical': 'SAME'})
    check('overlay leaves the baseline object unchanged', rec_hash(baseline('K1')[k]) == keep)
    check('CD at SAME becomes portion-equivalent', after['normative_strength_equivalence'] == 'PORTION_EQUIVALENT_WITH_REMAINDER')
    n = apply_set(base, {'modality': 'NONE', 'canonical_coverage': [], 'strength_vs_canonical': 'N/A', 'strength_resolution_code': None})
    check('removing links clears coverage and links', n['strength_links'] == [] and n['canonical_semantic_coverage'] == 'NONE' and n['canonical_policy_ids'] == [])
    try:
        apply_set(base, {'source_key': 'X'})
        check('illegal overlay field is refused', False)
    except ValueError:
        check('illegal overlay field is refused', True)
    # engine reproduces baseline coverage
    ok = True
    for c in CANDIDATES:
        cov = coverage_of(list(baseline(c).values()))
        for p, row in coverage(c).items():
            if cov[p]['strength_status'] != row['strength_status'] or cov[p]['computed_status'] != row['computed_status']:
                ok = False
    check('coverage engine reproduces all 1,176 stored rows', ok)
    # replay detects a tampered proposal
    cors = [json.loads(l) for l in open(out_path('CORRECTION_PROPOSALS.jsonl'), encoding='utf-8')]
    eff = replay(cors, ['K1'])
    t = copy.deepcopy(cors)
    for row in t:
        if row['case_key'] == k:
            row['set']['classification'] = 'EXTRA_WORKFLOW'
    eff2 = replay(t, ['K1'])
    check('replay shows a tampered correction', canon(eff['K1'][k]) != canon(eff2['K1'][k]))
    check('replay is deterministic', canon(replay(cors, ['K1'])['K1'][k]) == canon(eff['K1'][k]))
    # the key finding is in the replay
    check('K1 Swagger record is CD after replay', eff['K1'][k]['classification'] == 'CANONICAL_PLUS_DELTA' and eff['K1'][k]['modality'] == 'DEFAULT')
    check('K1 Swagger baseline stays CO', baseline('K1')[k]['classification'] == 'CANONICAL_ONLY')
    write_json('PREFLIGHT/TOOL_TESTS.json', {'results': RESULTS, 'all_pass': all(r['pass'] for r in RESULTS)})
    raise SystemExit(0 if all(r['pass'] for r in RESULTS) else 1)


if __name__ == '__main__':
    main()
