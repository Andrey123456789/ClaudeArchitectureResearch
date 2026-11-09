import json
from collections import Counter
from rcommon import out_path, read_jsonl, read_json, utf8_stdout
utf8_stdout()
log=read_jsonl(out_path('CHANGE_LOG.jsonl'))
print(len(log), Counter(r.get('kind') for r in log), sorted(log[0].keys()))
print(json.dumps(log[0],ensure_ascii=False)[:400])
print(Counter(r.get('rule') for r in log))
g=read_json(out_path('POLICY_DEPENDENCY_GRAPH.json'))
print({k:len(v) for k,v in g['rule_policies'].items()})
print({k:len(v) for k,v in g['rule_files'].items()})
print([(e['a'][:3],e['b'][:3],len(e['shared_files']),len(e['shared_policies'])) for e in g['rule_edges']])
zero=[(c,p) for c,d in g['per_candidate'].items() for p,v in d.items() if not v['owners']]
print('cells with no FULL owner',len(zero),zero[:12])
