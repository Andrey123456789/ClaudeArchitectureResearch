"""Save a candidate-level checkpoint after reviewed file batches; no semantic inference."""
import json,hashlib,sys
from pathlib import Path
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');t.replace(p)
s=read(O/'STATE.json');c=sys.argv[1];d=O/'PASSES'/f"pass_{s['current_pass_id']:04d}";unit=f"P{s['current_pass_id']:04d}-{c}-COMPLETE"
assert not any(u['unit']==unit for u in s['completed_units'])
coverage=[r for r in jl(d/'FILE_COVERAGE.jsonl') if r['candidate']==c]
sources=[r for r in jl(O/'SOURCE_FILE_INDEX.jsonl') if r['candidate']==c]
assert len(coverage)==len(sources) and {r['path'] for r in coverage}=={r['path'] for r in sources}
policy_reviews=[]
if s['current_pass_id']==2:
 root=O.parent.parent
 inventory=read(root/'inputs'/c/'source/inventory.json')
 expected={p['id'] for g in inventory['policygroups'] for p in g['policies']}
 expected.update(p['id'] for p in read(root/'inputs'/c/'source/shared-research-invariants.json')['invariants'])
 policy_reviews=[r for r in jl(d/'POLICY_BOUNDARY_REVIEW.jsonl') if r['candidate']==c]
 assert len(expected)==196 and len(policy_reviews)==196 and {r['policy_id'] for r in policy_reviews}==expected
claims=[r for r in jl(d/'CANDIDATE_CLAIMS.jsonl') if r['candidate']==c]
counts={k:sum(r['comparison_status']==k for r in claims) for k in ['NOVEL_CLAUSE','RECLASSIFICATION_CANDIDATE','UNCERTAIN_NOVELTY','ALREADY_COVERED','DUPLICATE_IN_THIS_SEARCH']}
original_counts=counts.copy()
revisions={r['id']:s.get('finding_revisions',{}).get(r['id'],{}) for r in claims}
counts={k:sum(revisions[r['id']].get('effective_status',r['comparison_status'])==k for r in claims) for k in counts}
record={'unit':unit,'pass_id':s['current_pass_id'],'strategy':s['current_strategy'],'candidate':c,'source_files':len(sources),'source_lines':sum(r['line_count'] for r in sources),'claim_counts':counts,'claim_ids':[r['id'] for r in claims],'coverage':coverage,'full_pass_complete':False,'semantic_completeness_proven':False,'cautions':['Novel relative to extraction is not proven EXTRA.','Deferred hotspots and unresolved cases require other strategies.']}
record['original_claim_counts']=original_counts
if policy_reviews:
 record['canonical_policies_reviewed']=len(policy_reviews)
 record['policy_review_units']=sorted({r['unit'] for r in policy_reviews})
record['applied_revisions']={k:v for k,v in revisions.items() if v}
p=d/(c+'_CANDIDATE_CHECKPOINT.json');save(p,record)
s['completed_units'].append({'unit':unit,'outputs':{p.relative_to(O).as_posix():sha(p)}})
save(O/'STATE.json',s);print(json.dumps({k:record[k] for k in ['unit','source_files','source_lines','claim_counts','full_pass_complete']}))
