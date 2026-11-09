"""Read-only structural validator. This does NOT prove semantic completeness."""
import hashlib,json,sys
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parent.parent
C={'M','M1','L0','L1','K0','K1'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def main():
 errors=[]; checks={}; state=read(O/'STATE.json'); manifest=read(O/'BASELINE_MANIFEST.json')
 for x in manifest['files']:
  p=R/x['path']
  if not p.is_file() or sha(p)!=x['sha256']: errors.append('Input missing/changed: '+x['path'])
 actual=set()
 for prefix in ['inputs','stage_A/primary','stage_A/replica','stage_A/independent']:
  actual.update(p.relative_to(R).as_posix() for p in (R/prefix).rglob('*') if p.is_file())
 if actual!={x['path'] for x in manifest['files']}: errors.append('Frozen input file set changed')
 fp=hashlib.sha256(''.join(f"{x['path']}\0{x['sha256']}\n" for x in sorted(manifest['files'],key=lambda x:x['path'])).encode()).hexdigest()
 if fp!=state['baseline_fingerprint'] or fp!=manifest['baseline_fingerprint']: errors.append('Fingerprint mismatch')
 baseline=jl(O/'BASELINE_RECORD_INDEX.jsonl'); keys={r['index_key'] for r in baseline}
 if len(keys)!=len(baseline): errors.append('Duplicate baseline index keys')
 checks['baseline_ambiguities']=sum(bool(r['ambiguities']) for r in baseline)
 sources=jl(O/'SOURCE_FILE_INDEX.jsonl'); sourcekeys={(r['candidate'],r['path']) for r in sources}
 for unit in state['completed_units']:
  for name,digest in unit.get('outputs',{}).items():
   if not (O/name).is_file() or sha(O/name)!=digest: errors.append('Checkpoint output missing/changed: '+name)
 findings=jl(O/'NOVEL_FINDINGS.jsonl')+jl(O/'UNRESOLVED_FINDINGS.jsonl')+jl(O/'ALREADY_COVERED_SAMPLES.jsonl'); ids={x['id'] for x in findings}
 if len(ids)!=len(findings): errors.append('Duplicate finding IDs')
 for f in findings:
  for k in ['id','candidate','path','start_line','end_line','quote','claim','trigger','modality','domain','baseline_comparisons','comparison_status','evidence_verification_status']:
   if k not in f: errors.append(f"Finding {f.get('id')} missing {k}")
  if (f.get('candidate'),f.get('path')) not in sourcekeys: errors.append('Unknown finding source '+f.get('id','?')); continue
  p=R/'inputs'/f['candidate']/f['path']; lines=p.read_text(encoding='utf-8-sig').splitlines()
  quote='\n'.join(lines[f['start_line']-1:f['end_line']])
  if quote!=f['quote']: errors.append('Quote mismatch '+f['id'])
  for comp in f.get('baseline_comparisons',[]):
   for k in comp.get('baseline_keys',[]):
    if k not in keys: errors.append('Broken baseline ref '+k)
 if len({u['unit'] for u in state['completed_units']})!=len(state['completed_units']): errors.append('Duplicate committed units')
 byid={f['id']:f for f in findings}
 for fid,meta in state.get('finding_revisions',{}).items():
  rev=read(O/meta['revision'])
  if fid not in byid or rev['finding_id']!=fid or rev['effective_status']!=meta['effective_status']: errors.append('Invalid revision '+fid)
  if any(k not in keys for k in rev.get('baseline_keys',[])): errors.append('Broken revision reference '+fid)
  if rev['previous_status']!=byid[fid]['comparison_status']: errors.append('Revision predecessor mismatch '+fid)
 completed=[]
 for d in sorted((O/'PASSES').glob('pass_*')) if (O/'PASSES').exists() else []:
  coverage=jl(d/'FILE_COVERAGE.jsonl'); claims=jl(d/'CANDIDATE_CLAIMS.jsonl'); comparisons=jl(d/'NOVELTY_COMPARISONS.jsonl')
  covkeys=[(x['candidate'],x['path']) for x in coverage]
  if len(covkeys)!=len(set(covkeys)) or not set(covkeys)<=sourcekeys: errors.append('Invalid active coverage '+d.name)
  sourcebykey={(x['candidate'],x['path']):x for x in sources}
  for row in coverage:
   src=sourcebykey.get((row['candidate'],row['path']))
   if src and (src['sha256']!=row['sha256'] or src['line_count']!=row['line_count']): errors.append('Coverage source mismatch '+row['path'])
   for a,b in row.get('inspected_ranges',[]):
    if a<1 or b<a or b>row['line_count']: errors.append('Invalid inspected range '+row['path'])
  claimids=[x['id'] for x in claims]
  if len(claimids)!=len(set(claimids)): errors.append('Duplicate active claim IDs '+d.name)
  if set(claimids)!={x['claim_id'] for x in comparisons} or len(comparisons)!=len(claims): errors.append('Comparison accounting mismatch '+d.name)
  for claim in claims:
   if claim['comparison_status']!='DUPLICATE_IN_THIS_SEARCH' and byid.get(claim['id'])!=claim: errors.append('Global/pass claim mismatch '+claim['id'])
  receipt_cov=[]; receipt_ids=[]
  for unit in state['completed_units']:
   for name in unit.get('outputs',{}):
    if name.startswith(d.relative_to(O).as_posix()+'/') and name.endswith('.receipt.json'):
     receipt=read(O/name); receipt_cov.extend(receipt['coverage']); receipt_ids.extend(receipt['claim_ids'])
     batch=read(O/'BATCHES'/(receipt['unit']+'.json'))
     if sha(O/'BATCHES'/(receipt['unit']+'.json'))!=receipt['batch_input_sha256']: errors.append('Receipt batch mismatch '+receipt['unit'])
     for original in batch.get('claims',[]):
      committed=next((x for x in claims if x['id']==original['id']),{})
      if any(committed.get(k)!=value for k,value in original.items()): errors.append('Committed claim changed '+original['id'])
  if receipt_cov!=coverage or receipt_ids!=claimids: errors.append('Append-only receipt accounting mismatch '+d.name)
  policy_file=d/'POLICY_BOUNDARY_REVIEW.jsonl'
  if policy_file.exists():
   reviews=jl(policy_file); reviewkeys=[(r['candidate'],r['policy_id']) for r in reviews]
   if len(reviewkeys)!=len(set(reviewkeys)): errors.append('Duplicate canonical reviews '+d.name)
   receipt_reviews=[]
   for unit in state['completed_units']:
    for name in unit.get('outputs',{}):
     if name.startswith(d.relative_to(O).as_posix()+'/') and name.endswith('.policy_receipt.json'):
      receipt=read(O/name); batchpath=O/'BATCHES'/(receipt['unit']+'.json')
      if sha(batchpath)!=receipt['batch_input_sha256']: errors.append('Policy batch mismatch '+receipt['unit'])
      batch=read(batchpath)
      if len(batch['reviews'])!=len(receipt['reviews']): errors.append('Policy review count mismatch '+receipt['unit'])
      for original,committed in zip(batch['reviews'],receipt['reviews']):
       if any(committed.get(k)!=value for k,value in original.items()): errors.append('Policy judgment mutated '+receipt['unit'])
      receipt_reviews.extend(receipt['reviews'])
   if reviews!=receipt_reviews: errors.append('Policy append-only accounting mismatch '+d.name)
   for review in reviews:
    c=review['candidate']; inventory=read(R/'inputs'/c/'source/inventory.json')
    canon={p['id']:p for g in inventory['policygroups'] for p in g['policies']}
    canon.update({p['id']:p for p in read(R/'inputs'/c/'source/shared-research-invariants.json')['invariants']})
    if review['canonical_policy']!=canon.get(review['policy_id']): errors.append('Canonical wording mismatch '+review['policy_id'])
    if any(k not in keys for k in review['baseline_keys']): errors.append('Broken policy comparison reference '+review['policy_id'])
    if any(fid not in byid for fid in review.get('new_finding_ids',[])): errors.append('Broken policy finding reference '+review['policy_id'])
    for context in review['retrieved_source_contexts']:
     p=R/'inputs'/c/context['path']; lines=p.read_text(encoding='utf-8-sig').splitlines()
     if sha(p)!=context['sha256'] or context['context_quotes']!=['\n'.join(lines[a-1:b]) for a,b in context['inspected_ranges']]: errors.append('Policy source context mismatch '+context['path'])
   checks[d.name+'_canonical_reviews']=len(reviews)
  v=d/'PASS_VALIDATION.json'
  if not v.exists() or read(v).get('status')!='COMPLETE': continue
  completed.append(read(v)); coverage=jl(d/'FILE_COVERAGE.jsonl')
  if {(x['candidate'],x['path']) for x in coverage}!=sourcekeys or len(coverage)!=len(sourcekeys): errors.append('Incomplete/duplicate coverage '+d.name)
  if {x['candidate'] for x in coverage}!=C: errors.append('Missing candidate '+d.name)
  for name in ['PASS_PLAN.md','CANDIDATE_CLAIMS.jsonl','NOVELTY_COMPARISONS.jsonl','PASS_REPORT.md','CHECKPOINT_HASHES.json']:
   if not (d/name).is_file(): errors.append('Missing '+d.name+'/'+name)
  if (d/'CHECKPOINT_HASHES.json').exists():
   for name,digest in read(d/'CHECKPOINT_HASHES.json').items():
    if not (d/name).is_file() or sha(d/name)!=digest: errors.append('Closed pass mutation '+d.name+'/'+name)
  for name in ['CANDIDATE_CLAIMS.jsonl','NOVELTY_COMPARISONS.jsonl']:
   if (d/name).exists():
    rr=jl(d/name); ii=[x['id'] for x in rr]
    if len(ii)!=len(set(ii)): errors.append('Duplicate record IDs '+d.name+'/'+name)
 if [x['pass_id'] for x in completed]!=list(range(1,len(completed)+1)): errors.append('Nonmonotonic completed passes')
 if state['final_status'] in ['CONVERGED','SEARCH_SATURATED_WITH_OPEN_ISSUES']:
  if len({x['strategy_family'] for x in completed})<6: errors.append('Mandatory strategy families incomplete')
  if not (O/'UNATTRIBUTED_CLAUSE_REVIEW.jsonl').exists(): errors.append('Final clause review missing')
 if state['final_status']=='CONVERGED':
  if len(completed)<2 or any(x['new_distinct_claims'] or x['new_plausible_unresolved'] for x in completed[-2:]): errors.append('Two zero-discovery passes absent')
  elif completed[-1]['strategy_family']==completed[-2]['strategy_family']: errors.append('Zero passes use same method')
  if any(f.get('status','OPEN')=='OPEN' for f in jl(O/'UNRESOLVED_FINDINGS.jsonl')): errors.append('Open issues prevent strong closure')
 checks.update(input_files=len(actual),baseline_records=len(baseline),source_files=len(sources),findings=len(findings),completed_passes=len(completed))
 print(json.dumps({'status':'FAIL' if errors else 'PASS_STRUCTURAL_ONLY','checks':checks,'errors':errors,'semantic_completeness_proven':False},indent=2))
 return bool(errors)
if __name__=='__main__': sys.exit(main())
