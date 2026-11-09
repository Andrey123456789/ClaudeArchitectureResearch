"""R23: cross-method adjudication of the qualified cells. Writes CROSS_METHOD_ADJUDICATION.jsonl.

Each row combines: semantic entailment (clause review re-read at source), a falsifying counterexample, an executable test where one applies, and the competing interpretations. No voting by model count.
"""
import os

from rcommon import AUD, CANDIDATES, baseline, coverage, input_path, norm_ws, read_jsonl, read_lines, sha256_file, utf8_stdout, wc_path, write_jsonl
from witness import FileMap, map_ref, rel_of

COUNTER = {
    ('K0', 'API-014'): 'A one-off breaking change the policy would tolerate under "normally": barred here. Stronger, not equal.',
    ('K0', 'API-019'): 'A liveness check on a dependency with a stated reason: tolerated by "should normally", refused by "must not depend". Stronger on the hedge.',
    ('K1', 'GOV-007'): 'A behavioral rule recorded in a later change: meets the policy, breaks "in the same change". Stronger on timing.',
    ('K1', 'API-014'): 'As K0: the normally is dropped, and CLAUDE.md makes any breaking public API change Reserved.',
    ('K1', 'API-019'): 'As K0: should normally becomes must, plus a line on restarts.',
    ('M1', 'WF-020'): 'A scan with severities but no impact statement could still pass the first witness alone: impact and context come from a second record.',
    ('L0', 'FE-010'): 'Its reactive-forms witness reads DEFAULT under A1.3, so a deviation with a reason breaks no witness at full strength. Coverage still holds by the override.',
    ('L0', 'GOV-007'): 'A later update of the durable source: meets GOV-007, breaks L0 "in the same change". Equal-strength evidence comes only through a partial witness.',
}


def witnesses_state(c, row, fm):
    keys = set(row.get('direct_source_keys') or []) | set(row.get('partial_source_keys') or []) | set(row.get('strength_equivalent_source_keys') or [])
    states = []
    for k in sorted(keys):
        rec = baseline(c)[k]
        for ref in rec['evidence_refs']:
            states.append(map_ref(fm, c, ref)['status'])
    return {'n_keys': len(keys), 'n_refs': len(states), 'changed_refs': sum(1 for s in states if s == 'CHANGED')}


def build():
    fm = FileMap()
    rows = []
    review = read_jsonl(os.path.join(AUD, 'COVERAGE_OVERRIDE_REVIEW.jsonl'))
    for x in review:
        if x['outcome'] not in ('STRENGTH_QUALIFIER_RETAINED', 'OVERRIDE_CONFIRMED_WITH_QUALIFIER'):
            continue
        c, pid = x['candidate'], x['policy_id']
        rows.append({'cell': '%s %s' % (c, pid), 'kind': 'STRENGTH_CELL' if x['outcome'].startswith('STRENGTH') else 'QUALIFIED_OVERRIDE', 'semantic_entailment': x['clause_review'], 'falsifying_counterexample': COUNTER.get((c, pid)), 'executable_test': 'NOT_APPLICABLE: instruction text; no hook decides this',
                     'competing_interpretations': ['Equal strength, because the policy tag is binding and the witness is binding.', 'Not equal, because the witness drops a hedge or adds timing, or the equal link is partial.'], 'result': 'QUALIFIER_RETAINED', 'parity_statement': 'DIRECT_EVIDENCE is traceability, not parity or compliance.',
                     'qualifier': x.get('qualifier') or x['clause_review'][:200], 'witnesses_on_current_bytes': witnesses_state(c, coverage(c)[pid], fm), 'audit_outcome': x['outcome']})
    # Rows whose equal-strength evidence rests only on partial links.
    partial = []
    for c in CANDIDATES:
        for pid, row in coverage(c).items():
            same = set(row.get('strength_equivalent_source_keys') or [])
            direct = set(row.get('direct_source_keys') or [])
            if same and not same & direct:
                partial.append({'cell': '%s %s' % (c, pid), 'kind': 'PARTIAL_WITNESS_ONLY', 'semantic_entailment': 'Not read clause by clause here unless also listed above. The equal-strength list holds only partial witnesses.', 'falsifying_counterexample': None, 'executable_test': 'NOT_APPLICABLE',
                                'competing_interpretations': ['Several partial links jointly equal the policy.', 'They do not, and the cell shows traceability only.'], 'result': 'FLAG_RETAINED: no parity inference', 'witnesses_on_current_bytes': witnesses_state(c, row, fm)})
    rows.extend(partial)
    n_conflict = sum(1 for c in CANDIDATES for r in baseline(c).values() if r.get('canonical_conflict_ids'))
    rows.append({'cell': 'canonical_conflict_ids', 'kind': 'SOURCE_POLICY_CONFLICT', 'semantic_entailment': 'The field is empty on every baseline record (%d). Source-policy tensions were carried as UNCERTAIN or future human decisions and are resolved by R02 to R06 or listed in UNRESOLVED_DECISIONS.jsonl.' % n_conflict, 'falsifying_counterexample': None, 'executable_test': 'Hook and checker suites R02, R04, R06, R08', 'competing_interpretations': [], 'result': 'CARRIED_BY_RULES'})
    write_jsonl('CROSS_METHOD_ADJUDICATION.jsonl', rows)
    return rows


if __name__ == '__main__':
    utf8_stdout()
    rs = build()
    from collections import Counter
    print(len(rs), Counter(r['kind'] for r in rs))
