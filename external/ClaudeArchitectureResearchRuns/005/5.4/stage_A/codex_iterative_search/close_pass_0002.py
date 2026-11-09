"""Close the reviewed second pass, retaining all earlier immutable records."""
import json,hashlib,subprocess,sys
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
jl=lambda p:[json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');t.replace(p)
s=read(O/'STATE.json');d=O/'PASSES/pass_0002'
assert s['current_pass_id']==2 and not (d/'PASS_VALIDATION.json').exists()
v=subprocess.run([sys.executable,str(O/'VALIDATE_ITERATIVE_SEARCH.py')],capture_output=True,text=True)
assert v.returncode==0,v.stdout+v.stderr
validation=json.loads(v.stdout);cov=jl(d/'FILE_COVERAGE.jsonl');src=jl(O/'SOURCE_FILE_INDEX.jsonl');reviews=jl(d/'POLICY_BOUNDARY_REVIEW.jsonl');claims=jl(d/'CANDIDATE_CLAIMS.jsonl')
assert len(cov)==len(src)==448 and {(r['candidate'],r['path']) for r in cov}=={(r['candidate'],r['path']) for r in src}
counts={}
for c in ['M','M1','L0','L1','K0','K1']:
 assert any(u['unit']==f'P0002-{c}-COMPLETE' for u in s['completed_units'])
 assert len([r for r in reviews if r['candidate']==c])==196
 counts[c]=dict(Counter(s.get('finding_revisions',{}).get(r['id'],{}).get('effective_status',r['comparison_status']) for r in claims if r['candidate']==c))
new=sum(x.get('NOVEL_CLAUSE',0)+x.get('RECLASSIFICATION_CANDIDATE',0) for x in counts.values());unc=sum(x.get('UNCERTAIN_NOVELTY',0) for x in counts.values())
record=dict(status='COMPLETE',pass_id=2,strategy_family=2,strategy=s['current_strategy'],baseline_fingerprint=s['baseline_fingerprint'],source_files=448,canonical_policy_reviews=1176,new_distinct_claims=new,new_plausible_unresolved=unc,effective_counts_by_candidate=counts,structural_validation_before_close=validation,semantic_completeness_proven=False)
report='# Pass 0002 — Canonical-policy boundary sweep\n\nAll six candidates and 448 active source files accounted for. Reviewed 196 canonical boundaries per candidate (1176 total), including policy wording, candidate implementation context and semantic baseline actions from all three runs. Source ranges outside those contexts were separately inspected; completed receipts preserve the judgments. Frozen input hashes validated at closure.\n\n| Candidate | Files | Verified novel/reclassification | New unresolved |\n|---|---:|---:|---:|\n'
for c,x in counts.items():report+=f"| {c} | {sum(r['candidate']==c for r in cov)} | {x.get('NOVEL_CLAUSE',0)+x.get('RECLASSIFICATION_CANDIDATE',0)} | {x.get('UNCERTAIN_NOVELTY',0)} |\n"
report+=f'\nNew verified distinct clauses: {new}; new plausible unresolved hypotheses: {unc}. This is a nonzero pass for convergence purposes. No findings are proven EXTRA or proven cross-candidate differences.\n\nResidual questions concern conditional technique/API preferences, omitted subordinate review atoms, numeric hook budgets and stronger or narrower interpretations than canonical rules. Existing source-verified hypotheses are preserved; policy linkage and previous implementation labels do not decide normativity. Hard negative comparisons include bodyless304, optional AAA comments, local-account review items in M, migration script preferences, header concurrency, scope-appropriate verification and feed trust.\n\nNext: family3 orphan/non-normative challenge, candidate order L0, M, K1, M1, L1, K0. Challenge rejected source contexts independently, including previous ORACLE_LINKED passages for omitted atoms, and revisit unresolved hypotheses with parent/load evidence. All six strategy families and final unattributed review remain mandatory. Structural validation does not prove semantic completeness.\n'
(d/'PASS_REPORT.md').write_text(report,encoding='utf-8');save(d/'PASS_VALIDATION.json',record)
save(d/'CHECKPOINT_HASHES.json',{p.name:sha(p) for p in sorted(d.iterdir()) if p.is_file() and p.name!='CHECKPOINT_HASHES.json'})
s['completed_units'].append(dict(unit='P0002-COMPLETE',outputs={'PASSES/pass_0002/CHECKPOINT_HASHES.json':sha(d/'CHECKPOINT_HASHES.json')}))
s['convergence_history'].append({k:record[k] for k in ['pass_id','strategy_family','new_distinct_claims','new_plausible_unresolved','baseline_fingerprint']});s['last_completed_pass']=2;s['current_pass_id']=3;s['current_strategy']='ORPHAN_NON_NORMATIVE_CHALLENGE';s['candidate']='L0';s['next_file_batch']='Build L0 orphan/coverage challenge inventory and inspect root/rules contexts; preserve completed passes.';s['current_candidate_findings']=[]
p3=O/'PASSES/pass_0003';p3.mkdir(exist_ok=False)
(p3/'PASS_PLAN.md').write_text('# Pass 0003 — Orphan / non-normative challenge\n\nFamily3. Order L0, M, K1, M1, L1, K0. Use all previous orphan resolutions and coverage classifications as challenge targets, not truth labels. Inspect rejected and ORACLE_LINKED source contexts for independent procedural duties, technical prerequisites, defaults and exceptions. Reuse verified source index and prior reads for full-file accounting; inspect relevant contexts anew, with explicit line ranges and reasons for portions not reread. Compare each plausible action to the complete semantic union and prior iterative findings. Preserve unresolved cases; do not inflate discoveries by reciting them. Every file/batch receives durable accounting.\n',encoding='utf-8')
for name in ['FILE_COVERAGE.jsonl','CANDIDATE_CLAIMS.jsonl','NOVELTY_COMPARISONS.jsonl']:(p3/name).write_text('',encoding='utf-8')
save(O/'STATE.json',s)
p=O/'RESUME.md';p.write_text('\n'.join('State truth: STATE.json. Current pointer: pass 3, candidate L0; passes1 and2 frozen.' if l.startswith('State truth:') else 'Next ONE action: '+s['next_file_batch'] if l.startswith('Next ONE action:') else l for l in p.read_text(encoding='utf-8-sig').splitlines())+'\n',encoding='utf-8')
print(json.dumps(dict(closed_pass=2,new_distinct=new,new_unresolved=unc,next_pass=3)))
