"""Commit manually reviewed canonical boundary units and their retrieved evidence."""
import json,hashlib,sys
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');t.replace(p)
b=read(Path(sys.argv[1]));s=read(O/'STATE.json');d=O/'PASSES'/f"pass_{s['current_pass_id']:04d}"
assert s['current_pass_id']==2
assert not any(u['unit']==b['unit'] for u in s['completed_units'])
c=b['candidate'];inv=read(R/'inputs'/c/'source/inventory.json')
pp={p['id']:p for g in inv['policygroups'] for p in g['policies']}
pp.update({p['id']:p for p in read(R/'inputs'/c/'source/shared-research-invariants.json')['invariants']})
rr=jl(O/'BASELINE_RECORD_INDEX.jsonl'); keys={r['index_key'] for r in rr}
old=jl(d/'POLICY_BOUNDARY_REVIEW.jsonl')
assert not {(r['candidate'],r['policy_id']) for r in old}&{(c,r['policy_id']) for r in b['reviews']}
rows=[]
for r in b['reviews']:
 assert all(k in keys for k in r['baseline_keys'])
 pid=r['policy_id'];ranges={}
 for rec in rr:
  if rec['candidate']!=c or pid not in rec['policy_references'] or rec['record_kind'] not in ['constraints.jsonl','BLIND_FINDINGS.jsonl','policies.jsonl']:continue
  for e in rec['evidence']:
   if not e.get('path') or not e.get('start_line'):continue
   path=R/'inputs'/c/e['path']
   if not path.is_file():continue
   n=len(path.read_text(encoding='utf-8-sig').splitlines())
   ranges.setdefault(e['path'],set()).update(range(max(1,e['start_line']-1),min(n,e['end_line']+1)+1))
 evidence=[]
 for path,ns in sorted(ranges.items()):
  src=R/'inputs'/c/path;ls=src.read_text(encoding='utf-8-sig').splitlines();merged=[]
  for n in sorted(ns):
   if merged and n==merged[-1][1]+1:merged[-1][1]=n
   else:merged.append([n,n])
  evidence.append({'path':path,'sha256':sha(src),'inspected_ranges':merged,'context_quotes':['\n'.join(ls[a-1:z]) for a,z in merged]})
 rows.append({'candidate':c,'pass_id':2,'unit':b['unit'],'canonical_policy':pp[pid],**r,'retrieved_source_contexts':evidence})
receipt=d/(b['unit']+'.policy_receipt.json')
save(receipt,{'unit':b['unit'],'batch_input_sha256':sha(Path(sys.argv[1])),'reviews':rows})
p=d/'POLICY_BOUNDARY_REVIEW.jsonl';t=p.with_suffix('.jsonl.tmp');t.write_text(p.read_text(encoding='utf-8')+''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8');t.replace(p)
s['completed_units'].append({'unit':b['unit'],'outputs':{receipt.relative_to(O).as_posix():sha(receipt),Path(sys.argv[1]).resolve().relative_to(O).as_posix():sha(Path(sys.argv[1]))}})
s['candidate']=c;s['next_file_batch']=b['next_action'];save(O/'STATE.json',s)
p=O/'RESUME.md';t=p.read_text(encoding='utf-8-sig');t='\n'.join('State truth: STATE.json. Current pointer: pass 2, candidate '+c+', after '+b['unit']+'.' if l.startswith('State truth:') else 'Next ONE action: '+b['next_action'] if l.startswith('Next ONE action:') else l for l in t.splitlines())+'\n';p.write_text(t,encoding='utf-8')
print(json.dumps({'committed':b['unit'],'policy_reviews':len(rows),'total_policy_reviews':len(old)+len(rows),'next':b['next_action']}))

