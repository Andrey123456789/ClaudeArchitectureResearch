import sys
from rcommon import out_path, read_jsonl, utf8_stdout, norm_ws
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
ctx=[r for r in rows if r['repair']['status']=='REWORDED_CONTEXT']
a,b=int(sys.argv[1]),int(sys.argv[2])
print(len(ctx))
for r in ctx[a:b]:
    q=[x for x in r['current_evidence_refs'] if x['status'] not in('SAME','MOVED')]
    print(r['source_key'][3:],r['classification'][:9],r['modality'],'|',norm_ws(r['claim_text'])[:150],'||',' / '.join(norm_ws(x.get('new_quote') or x['status'])[:120] for x in q[:2]))
