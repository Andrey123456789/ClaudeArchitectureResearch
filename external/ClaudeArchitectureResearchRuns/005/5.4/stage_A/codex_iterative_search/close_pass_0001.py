"""Freeze a reviewed full pass after actual structural validation; never infer semantics."""
import json,hashlib,subprocess,sys
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');t.replace(p)
s=read(O/'STATE.json'); n=s['current_pass_id']; d=O/'PASSES'/f'pass_{n:04d}'
assert n==1, 'This closure script is specific to reviewed Pass 0001.'
assert not (d/'PASS_VALIDATION.json').exists()
v=subprocess.run([sys.executable,str(O/'VALIDATE_ITERATIVE_SEARCH.py')],capture_output=True,text=True)
assert v.returncode==0,v.stdout+v.stderr
validation=json.loads(v.stdout)
cov=jl(d/'FILE_COVERAGE.jsonl'); src=jl(O/'SOURCE_FILE_INDEX.jsonl')
assert len(cov)==len(src)==448
assert {(r['candidate'],r['path']) for r in cov}=={(r['candidate'],r['path']) for r in src}
claims=jl(d/'CANDIDATE_CLAIMS.jsonl'); revisions=s.get('finding_revisions',{})
counts={}; raw={}
for c in ['M','M1','L0','L1','K0','K1']:
 assert any(u['unit']==f'P0001-{c}-COMPLETE' for u in s['completed_units'])
 rr=[r for r in claims if r['candidate']==c]
 counts[c]=dict(Counter(revisions.get(r['id'],{}).get('effective_status',r['comparison_status']) for r in rr))
 raw[c]=dict(Counter(r['comparison_status'] for r in rr))
new=sum(x.get('NOVEL_CLAUSE',0)+x.get('RECLASSIFICATION_CANDIDATE',0) for x in counts.values())
unc=sum(x.get('UNCERTAIN_NOVELTY',0) for x in counts.values())
record={'status':'COMPLETE','pass_id':1,'strategy_family':1,'strategy':s['current_strategy'],'baseline_fingerprint':s['baseline_fingerprint'],'source_files':448,'new_distinct_claims':new,'new_plausible_unresolved':unc,'effective_counts_by_candidate':counts,'original_counts_by_candidate':raw,'applied_revisions':revisions,'structural_validation_before_close':validation,'semantic_completeness_proven':False}
report='# Pass 0001 — Reverse normative-clause sweep\n\nCompleted all 448 active files across M, M1, L0, L1, K0 and K1. Inspected source ranges, conditional loading and independently violable subclauses before semantic comparison to all three frozen baselines. Source and baseline fingerprint validated at closure.\n\n'
report+='| Candidate | Source files | Effective novel/reclassification | Unresolved | Covered samples |\n|---|---:|---:|---:|---:|\n'
for c,x in counts.items():
 report+=f"| {c} | {sum(r['candidate']==c for r in cov)} | {x.get('NOVEL_CLAUSE',0)+x.get('RECLASSIFICATION_CANDIDATE',0)} | {x.get('UNCERTAIN_NOVELTY',0)} | {x.get('ALREADY_COVERED',0)} |\n"
report+=f'\nEffective discoveries: {new}; new plausible unresolved: {unc}. Original novel queue contains 60 records: CIS-M1-0004 was withdrawn by auditable revision after replica EXTRA-M1-0012 established equivalence. Three L1 options hypotheses have corrected RUN-022 links. Raw records and all completed batches remain unchanged.\n\n'
report+='Recurring residual areas: executable parse/read/root boundaries, subordinate procedural review duties, technical prerequisites, optional response fields, and conditional API recommendations. Unresolved questions concern normativity, equivalence, scope/loading or actual trigger interpretation; they remain open for another strategy. File ledgers identify deferred contexts. Exact source verification does not adjudicate normative significance.\n\n'
report+='Selected hard negative matches include K1 feed-trust review, bodyless 304 responses, measurement before hedging, selective reference loading and direct HttpClient construction in tests: these are already represented in the baseline union. No finding is a proven EXTRA or a proven cross-candidate difference.\n\n'
report+='Result: stopping criteria not met. Only strategy family 1 is complete and this pass is nonzero. Next: family 2 canonical-policy boundaries, with changed candidate order K1, L1, M1, K0, L0, M. Structural validation is PASS_STRUCTURAL_ONLY and cannot prove semantic completeness.\n'
(d/'PASS_REPORT.md').write_text(report,encoding='utf-8');save(d/'PASS_VALIDATION.json',record)
hashes={p.name:sha(p) for p in sorted(d.iterdir()) if p.is_file() and p.name!='CHECKPOINT_HASHES.json'}
save(d/'CHECKPOINT_HASHES.json',hashes)
s['completed_units'].append({'unit':'P0001-COMPLETE','outputs':{(d/'CHECKPOINT_HASHES.json').relative_to(O).as_posix():sha(d/'CHECKPOINT_HASHES.json')}})
s['convergence_history'].append({k:record[k] for k in ['pass_id','strategy_family','new_distinct_claims','new_plausible_unresolved','baseline_fingerprint']})
s['last_completed_pass']=1
s['current_pass_id']=2;s['current_strategy']='CANONICAL_POLICY_BOUNDARY_SWEEP';s['candidate']='K1'
s['next_file_batch']='Build canonical-policy evidence packets from frozen inventory and source index; inspect K1 governance boundaries first.'
s['current_candidate_findings']=[]
p2=O/'PASSES/pass_0002';p2.mkdir(exist_ok=False)
(p2/'PASS_PLAN.md').write_text('# Pass 0002 — Canonical-policy boundary sweep\n\nStrategy family 2. Candidate order K1, L1, M1, K0, L0, M. Inspect all 196 canonical policies for each candidate against actual implementation wording, including source context, exceptions, modality, technology choices and approval gates. Canonical links are retrieval hints, not equivalence verdicts. Challenge both prior classifications and broad registered claims. Reuse the verified source index and first-pass read ledger; every active file receives accounting for this pass, with relevant ranges inspected and explicit rationale for index-only portions. No coverage credit is granted merely for a keyword hit. Persist policy-level reviews as well as file coverage; revisit relevant unresolved hypotheses with canonical entailment evidence.\n',encoding='utf-8')
for name in ['FILE_COVERAGE.jsonl','CANDIDATE_CLAIMS.jsonl','NOVELTY_COMPARISONS.jsonl','POLICY_BOUNDARY_REVIEW.jsonl']:(p2/name).write_text('',encoding='utf-8')
save(O/'STATE.json',s)
p=O/'RESUME.md';t=p.read_text(encoding='utf-8-sig')
t='\n'.join('State truth: STATE.json. Current pointer: pass 2, candidate K1; Pass 0001 is frozen and complete.' if l.startswith('State truth:') else 'Next ONE action: '+s['next_file_batch'] if l.startswith('Next ONE action:') else l for l in t.splitlines())+'\n';p.write_text(t,encoding='utf-8')
print(json.dumps({'closed_pass':1,'effective_new':new,'unresolved':unc,'next_pass':2}))

