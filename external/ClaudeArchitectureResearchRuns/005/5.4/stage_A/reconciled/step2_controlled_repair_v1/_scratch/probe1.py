import json,re
from collections import Counter
from rcommon import CANDIDATES, baseline, coverage, out_path, read_jsonl, utf8_stdout, norm_ws, policies
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
R={r['source_key']:r for r in rows}
F={k:r for c in CANDIDATES for k,r in baseline(c).items()}
def flagged(r):
    out=[]
    for o in [r]+list(r.get('subclauses') or [])+list(r.get('audit_subclauses') or []):
        if o.get('classification') in('CANONICAL_ONLY','CANONICAL_PLUS_DELTA') and o.get('strength_vs_canonical')=='SAME' and o.get('strength_mechanical_mismatch') and not o.get('strength_resolution'):
            for l in o.get('strength_links') or []:
                if l['mechanical_relation'] in('RECORD_WEAKER','RECORD_STRONGER'):
                    out.append((l['policy_id'],l['policy_strength'],l['record_modality'],l['mechanical_relation'],l['coverage']))
    return out
b=Counter(); a=Counter()
newly=[]
for k,r in F.items():
    fb=flagged(r); fa=flagged(R[k]) if R[k]['repair']['active'] else []
    b['flag']+=bool(fb); a['flag']+=bool(fa)
    if fa and not fb: newly.append((k,fa))
print('SAME with mechanical mismatch and no resolution code: baseline',b['flag'],'repaired',a['flag'],'newly',len(newly))
for k,f in newly[:40]:
    print(k,f[:2],'|',R[k]['repair']['rules'],'|',norm_ws(R[k]['claim_text'])[:100])
ch=[k for k in F if R[k]['modality']!=F[k].get('modality')]
print('modality changed',len(ch),Counter((F[k].get('modality'),R[k]['modality']) for k in ch).most_common(12))
# strength witness stability
moved=[]
for c in CANDIDATES:
    cov=[x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl')) if x['candidate']==c]
    for x in cov:
        bb=coverage(c)[x['policy_id']]
        if set(bb.get('direct_source_keys') or [])!=set(x['direct_source_keys']) :
            moved.append((c,x['policy_id'],len(bb.get('direct_source_keys') or []),len(x['direct_source_keys'])))
print('cells whose direct witness set changed',len(moved),moved[:30])
gone=[m for m in moved if m[3]==0 and m[2]>0]
print('cells that lost all direct witnesses',gone)
print('empty direct in baseline',sum(1 for c in CANDIDATES for p,v in coverage(c).items() if not v.get('direct_source_keys')))
