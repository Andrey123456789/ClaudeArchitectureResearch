"""Writes POLICY_DEPENDENCY_GRAPH.json from the final view and the change log. Each edge cites a record and a current line, or a rule and a touched file."""
import importlib.util
import os
from collections import defaultdict
from itertools import combinations

from order import ALL
from rcommon import CANDIDATES, all_change_rows, now, out_path, policies, read_jsonl, utf8_stdout, write_json


def pointer(r):
    refs = [x for x in r.get('current_evidence_refs') or [] if x.get('start_line')]
    if not refs:
        return {'key': r['source_key'], 'path': None, 'line': None}
    return {'key': r['source_key'], 'path': refs[0]['path'].split('/template/')[1], 'line': refs[0]['start_line']}


def module_of(rule, name):
    p = out_path('_rules', rule, name)
    if not os.path.exists(p):
        return None
    spec = importlib.util.spec_from_file_location('m' + rule.replace('-', '_') + name.replace('.', '_'), p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rule_policies():
    out = {}
    for rule in ALL:
        s = set()
        m = module_of(rule, 'patches.py')
        if m is not None:
            s.update(getattr(m, 'POLICIES', []) or [])
        m = module_of(rule, 'review.py')
        if m is not None:
            s.update(r['policy'] for r in m.REVIEW)
        out[rule] = sorted(p for p in s if p in policies())
    return out


def rule_files():
    out = defaultdict(set)
    for r in all_change_rows():
        if r.get('kind') == 'TEMPLATE':
            out[r['rule']].add('%s:%s' % (r['candidate'], r['file']))
    return out


def build():
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    by = {r['source_key']: r for r in rows}
    cons = defaultdict(list)
    for r in rows:
        if r['repair']['active']:
            for pid in r.get('related_policy_ids') or []:
                cons[(r['candidate'], pid)].append(pointer(r))
    per = {c: {} for c in CANDIDATES}
    for cell in cov:
        c, pid = cell['candidate'], cell['policy_id']
        owners = [pointer(by[k]) for k in cell['direct_source_keys']]
        partial = [pointer(by[k]) for k in cell['partial_source_keys']]
        enforce = [p for p in owners + partial if p['path'] and ('/hooks/' in p['path'] or '/scripts/' in p['path'] or p['path'].endswith('settings.json'))]
        per[c][pid] = {'owners': owners, 'partial_witnesses': partial, 'consumers': cons.get((c, pid), []), 'enforcement': enforce}
    rp, rf = rule_policies(), rule_files()
    edges = []
    for a, b in combinations(ALL, 2):
        sf, sp = sorted(rf.get(a, set()) & rf.get(b, set())), sorted(set(rp[a]) & set(rp[b]))
        if sf or sp:
            edges.append({'a': a, 'b': b, 'shared_files': sf, 'shared_policies': sp})
    return {'version': 'step2-controlled-repair-v2', 'semantics': 'Owners: records with a FULL canonical link not coded by-reference or corollary. Consumers: records naming the policy as related. Enforcement: witnesses in hooks, scripts or settings. An edge is traceability, not a parity claim.', 'rule_policies': rp, 'rule_files': {k: sorted(v) for k, v in rf.items()}, 'rule_edges': edges, 'per_candidate': per}


def main():
    utf8_stdout()
    g = build()
    write_json('POLICY_DEPENDENCY_GRAPH.json', dict(g, at=now()))
    print('edges', len(g['rule_edges']), 'owners per cell min', min(len(v['owners']) for c in g['per_candidate'].values() for v in c.values()))


if __name__ == '__main__':
    main()
