"""Writes POLICY_IMPACT_GRAPH.json and REGRESSION_MATRIX.md from the change log, source reviews and gate log. Reporting only; it changes nothing that a gate reads."""
import importlib.util
import os
from collections import Counter, defaultdict

from order import ORDER, V2_ORDER
from rcommon import CANDIDATES, now, out_path, policies, read_jsonl, utf8_stdout, write_json, write_text

# Adjacent policies each change was checked against: what could conflict, beside what it edits. From the declarations.
ADJACENT = {
    'C01-CPM-EFFECTIVE': ['DEP-003', 'DEP-004', 'DEP-025', 'DEP-007', 'GOV-017'],
    'C02-RUN008-EVIDENCE': ['RUN-007', 'SEC-004', 'ARC-019', 'GOV-013'],
    'C03-WF019-EXCEPTION': ['PST-004', 'PST-005', 'PST-006', 'PST-009', 'PST-010', 'SEC-001', 'GOV-017', 'WF-018'],
    'C04-GIT-CONDITIONAL': ['DEP-001', 'DEP-003', 'DEP-004', 'DEP-025', 'GOV-017', 'GOV-019', 'GOV-020', 'PST-010'],
    'C05-PI012-RESIDUAL': ['SEC-003', 'SEC-016', 'SEC-017', 'DEP-001', 'API-016', 'ARC-025', 'WF-012'],
    'C06-REVIEW-SETS': ['GOV-015', 'GOV-017', 'DEP-003', 'DEP-006', 'DEP-025', 'WF-006', 'TST-004'],
    'C06B-R22-APPLICABILITY': [],
    'C07-PARITY-CLOSE': ['TST-006', 'WF-018', 'SEC-003'],
}


def review_policies(rule):
    p = out_path('_rules', rule, 'review.py')
    if not os.path.exists(p):
        return []
    spec = importlib.util.spec_from_file_location('im_' + rule.replace('-', '_'), p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return sorted({r['policy'] for r in m.REVIEW})


def main():
    utf8_stdout()
    log = read_jsonl(out_path('CHANGE_LOG.jsonl'))
    gates = read_jsonl(out_path('GATE_LOG.jsonl'))
    changes = {}
    for rule in V2_ORDER:
        rows = [r for r in log if r.get('rule') == rule]
        files = sorted({'%s:%s' % (r['candidate'], r['file']) for r in rows if r.get('kind') == 'TEMPLATE'})
        data = sorted({r['key'] for r in rows if r.get('kind') == 'DATA'})
        pol = sorted({p for r in rows if r.get('kind') == 'TEMPLATE' for p in r.get('affected_policies') or []} | set(review_policies(rule)))
        changes[rule] = {'edited_policies': pol, 'adjacent_policies': [p for p in ADJACENT.get(rule, []) if p in policies()], 'files': files, 'n_files': len(files), 'candidates': sorted({f.split(':')[0] for f in files}), 'data_records': data, 'n_data_records': len(data), 'last_gate': next((g['gate'] for g in reversed(gates) if g['rule'] == rule), None), 'attempts': sum(1 for g in gates if g['rule'] == rule)}
    edges = []
    names = list(changes)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared_files = sorted(set(changes[a]['files']) & set(changes[b]['files']))
            shared_pol = sorted((set(changes[a]['edited_policies']) | set(changes[a]['adjacent_policies'])) & (set(changes[b]['edited_policies']) | set(changes[b]['adjacent_policies'])))
            if shared_files or shared_pol:
                edges.append({'a': a, 'b': b, 'shared_files': shared_files, 'shared_policies': shared_pol})
    write_json('POLICY_IMPACT_GRAPH.json', {'version': 'step2-controlled-repair-v2', 'at': now(), 'semantics': 'What each v2 change edited and what it was checked against. An edge means the later gate re-ran the earlier suite on the shared surface; it is not a parity claim.', 'changes': changes, 'edges': edges, 'v1_rules_replayed': ORDER})
    suites = ORDER + V2_ORDER
    passed = [g for g in gates if g['gate'] != 'FAIL']
    latest = {}
    for g in passed:
        latest[g['rule']] = g
    t = ['# Regression matrix', '', 'Each row is a gate that passed, on the bytes of that gate. Each column is a suite: pass, then not run in brackets. A dash means the suite did not exist yet. Counts come from `GATE_LOG.jsonl`. Failed attempts are listed under the table; they are not silent.', '', '| Suite | ' + ' | '.join(r.split('-')[0] if r.startswith('C') or r.startswith('V') else r for r in V2_ORDER) + ' |', '|---|' + '---:|' * len(V2_ORDER)]
    for s in suites:
        cells = []
        for r in V2_ORDER:
            g = latest.get(r)
            v = (g['steps']['CUMULATIVE']['by_suite'].get(s) if g else None)
            cells.append('%d (%d)' % (v.get('PASS', 0), v.get('NOT_RUN', 0)) if v else '-')
        t.append('| %s | %s |' % (s, ' | '.join(cells)))
    t.extend(['', '## Gate attempts', '', '| Change | Attempts | Failed | Result | Seconds of last |', '|---|---:|---:|---|---:|'])
    for r in V2_ORDER:
        gs = [g for g in gates if g['rule'] == r]
        if gs:
            t.append('| %s | %d | %d | %s | %d |' % (r, len(gs), sum(1 for g in gs if g['gate'] == 'FAIL'), gs[-1]['gate'], gs[-1]['seconds']))
    fails = [g for g in gates if g['gate'] == 'FAIL']
    if fails:
        t.extend(['', '## Failed attempts, and why', ''])
        for g in fails:
            bad = [k for k, v in g['steps'].items() if v['status'] != 'PASS']
            first = (g['steps'].get('CUMULATIVE') or {}).get('failures') or []
            t.append('- `%s`, %s: failed step %s. %s %s' % (g['rule'], g['at'], ', '.join(bad), g.get('note') or '', ('First failure: %s.' % first[0]['test'][:110]) if first else ''))
    write_text('REGRESSION_MATRIX.md', '\n'.join(t) + '\n')
    print('impact', len(changes), 'edges', len(edges))


if __name__ == '__main__':
    main()
