import json
from rcommon import out_path, read_jsonl, utf8_stdout, v1_path
utf8_stdout()
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
for k,r in v1.items():
    if k in v2 and r.get('strength_resolution')!=v2[k].get('strength_resolution'):
        print(k,'rules',[x.split(':')[0] for x in v2[k]['repair']['rules']][-3:])
        print('  v1',json.dumps(r.get('strength_resolution'))[:200],'code',r.get('strength_resolution_code'),'mech',r.get('strength_mechanical_mismatch'),'str',r.get('strength_vs_canonical'),'mod',r.get('modality'))
        print('  v2',json.dumps(v2[k].get('strength_resolution'))[:200],'code',v2[k].get('strength_resolution_code'),'mech',v2[k].get('strength_mechanical_mismatch'),'str',v2[k].get('strength_vs_canonical'),'mod',v2[k].get('modality'))
print('---review_reason')
for k,r in v1.items():
    if k in v2 and r.get('review_reason') and not v2[k].get('review_reason'):
        print(k,[x.split(':')[0] for x in v2[k]['repair']['rules']][-3:],'|',r['review_reason'][:200])
# How many v2-updated records would the wipe reach, and what do they hold?
upd=[r for r in v2.values() if any(x.split(':')[0][:2] in ('C0',) for x in r['repair']['rules'])]
print('records touched by a v2 change',len(upd),'with a code field set',sum(1 for r in upd if r.get('strength_resolution_code')),'with resolution',sum(1 for r in upd if r.get('strength_resolution')))
