import json
from collections import Counter
from rcommon import out_path, read_jsonl, utf8_stdout, v1_path
utf8_stdout()
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
print('v1 with resolution',sum(1 for r in v1.values() if r.get('strength_resolution')),'v2 with',sum(1 for r in v2.values() if r.get('strength_resolution')))
lost=[k for k,r in v1.items() if r.get('strength_resolution') and k in v2 and not v2[k].get('strength_resolution')]
print('lost',len(lost))
for k in lost:
    r=v2[k]; print(k,r['classification'],r.get('modality'),r.get('strength_vs_canonical'),'mech',r.get('strength_mechanical_mismatch'),'v1code',v1[k]['strength_resolution'].get('code'),'rules',[x.split(':')[0] for x in r['repair']['rules']],'status',r['repair']['status'])
chg=[k for k,r in v1.items() if k in v2 and r.get('strength_resolution')!=v2[k].get('strength_resolution')]
print('changed',len(chg))
# every other field dropped between v1 and v2 by a v2 rule
drop=Counter()
for k,r in v1.items():
    if k not in v2: continue
    for f,val in r.items():
        if val not in (None,[],{},'') and v2[k].get(f) in (None,[],{},''):
            drop[f]+=1
print('non-empty in v1, empty in v2, by field:',dict(drop))
