import json
from collections import Counter
from rcommon import CANDIDATES, baseline, out_path, read_json, read_jsonl, utf8_stdout, v1_path
from order import V2_ORDER
utf8_stdout()
rows=read_jsonl(out_path('FINAL_AUDIT_RESULTS.jsonl'))
print('audit',Counter(r['status'] for r in rows))
print('by section',{s:dict(Counter(r['status'] for r in rows if r['section']==s)) for s in 'ABCDEFGHI'})
print('NOT_RUN rows:')
seen=[]
for r in rows:
    if r['status']=='NOT_RUN':
        print('  ',r['section'],r['test'][:120],'|',r['detail'][:120])
print('FINDING rows:')
for r in rows:
    if r['status']=='FINDING': print('  ',r['section'],r['test'][:170])
t=read_json(out_path('FINAL_SUITE_TALLY.json')); print('tally',t['tally'])
print('v1 suites',sum(1 for k in t['by_suite'] if k.startswith('R')),'v2 suites',sum(1 for k in t['by_suite'] if not k.startswith('R')))
print({k:v for k,v in t['by_suite'].items() if k[0] in 'CV'})
man=read_json(out_path('V2_FINAL_MANIFEST.json'))
tot=dict(v1=0,fr=0,files=0)
for c in CANDIDATES:
    m=man['candidates'][c]; print(c,'files',m['n_files'],'vs v1',m['n_changed_vs_v1'],'vs frozen',m['n_changed_vs_frozen'])
    tot['v1']+=m['n_changed_vs_v1'];tot['fr']+=m['n_changed_vs_frozen'];tot['files']+=m['n_files']
print('tot',tot)
per=Counter()
for c in CANDIDATES:
    for rel,f in man['candidates'][c]['files'].items():
        for r in f['rules']:
            if r[:2]=='C0': per[(r,c)]+=1
for r in V2_ORDER:
    print(r,{c:per[(r,c)] for c in CANDIDATES if per[(r,c)]})
cw=read_jsonl(out_path('V1_TO_V2_CROSSWALK.jsonl')); print('v1_to_v2',Counter(x['status'] for x in cw))
ds=read_json(out_path('DATASET_MANIFEST.json')); c=ds['counts']; print({k:c[k] for k in ('baseline_records','repaired_rows','active_rows','inactive_removed_rows','added_claims','proposed_clauses','by_crosswalk_status','by_candidate','coverage_or_strength_moved')}); print('applic',c['applicability_status'])
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
frozen={k:r for cc in CANDIDATES for k,r in baseline(cc).items()}
F=('claim_text','classification','modality')
for n,base in (('v1',v1),('frozen',frozen)):
    ch=[k for k,b in base.items() if k in v2 and any(v2[k].get(f)!=b.get(f) for f in F)]
    print('vs',n,'records with claim, classification or modality changed',len(ch),'added',sum(1 for k in v2 if k not in base),'inactive',sum(1 for k in base if k in v2 and not v2[k]['repair']['active']))
    print('   each',{f:sum(1 for k,b in base.items() if k in v2 and v2[k].get(f)!=b.get(f)) for f in F})
touched=[k for k,r in v2.items() if any(x[:2]=='C0' for x in r['repair']['rules'])]
print('records touched by a v2 rule',len(touched),{r:sum(1 for k in touched if r in [x.split(':')[0] for x in v2[k]['repair']['rules']]) for r in V2_ORDER})
print('hints',sum(1 for r in v2.values() if r.get('applicability_scope_hint')))
print('review flags',Counter(bool(r.get('review_needed')) for r in v2.values() if r['repair']['active']))
cov=read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
print('cells',len(cov),Counter(x['status'] for x in cov),Counter(x['strength_status'] for x in cov),'status changed',sum(1 for x in cov if x['status_changed']),'strength changed',sum(1 for x in cov if x['strength_status_changed']))
print('no direct',sum(1 for x in cov if not x['direct_source_keys']))
pm=read_jsonl(out_path('POLICY_PARITY_MATRIX.jsonl')); print('matrix',Counter(x['check_level'] for x in pm))
g=read_jsonl(out_path('GATE_LOG.jsonl'))
for x in g: print(x['rule'],x['gate'],x['seconds'],{k:v for k,v in (x.get('tally') or {}).items()})
print('claim gate',Counter((r['change'],r.get('attempt',1),r['status']) for r in read_jsonl(out_path('CLAIM_GATE_LOG.jsonl'))))
print('change log',Counter((r['rule'],r.get('kind')) for r in read_jsonl(out_path('CHANGE_LOG.jsonl'))))
print('C03 supersede',[r for r in V2_ORDER])
