"""Read-only canonical/source retrieval. No semantic equivalence is inferred."""
import json,sys
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
c=sys.argv[1];wanted=sys.argv[2].split(',');mode=sys.argv[3] if len(sys.argv)>3 else 'source'
inventory=read(R/'inputs'/c/'source/inventory.json')
policies=[p for g in inventory['policygroups'] for p in g['policies']]+read(R/'inputs'/c/'source/shared-research-invariants.json')['invariants']
selected=[p for p in policies if p['id'] in wanted or any(p['id'].startswith(w+'-') for w in wanted)]
records=[r for r in jl(O/'BASELINE_RECORD_INDEX.jsonl') if r['candidate']==c and set(r['policy_references'])&{p['id'] for p in selected} and r['record_kind'] in ['constraints.jsonl','BLIND_FINDINGS.jsonl','policies.jsonl']]
if mode in ['source','source-new','canonical']:
 for p in selected:print(p['id']+' ['+p['normative_strength']+'; '+p['trigger_class']+'; '+p['scope']+'] '+p['normalized_policy'])
if mode in ['source','source-new']:
 reused={}
 if mode=='source-new':
  s=read(O/'STATE.json'); ledger=O/'PASSES'/f"pass_{s['current_pass_id']:04d}"/'POLICY_BOUNDARY_REVIEW.jsonl'
  if ledger.exists():
   for r in jl(ledger):
    if r['candidate']!=c:continue
    for ctx in r['retrieved_source_contexts']:
     for a,b in ctx['inspected_ranges']:reused.setdefault(ctx['path'],set()).update(range(a,b+1))
 ranges={}
 for r in records:
  for e in r['evidence']:
   if not e.get('path') or not e.get('start_line'):continue
   p=R/'inputs'/c/e['path']
   if not p.is_file():continue
   ls=p.read_text(encoding='utf-8-sig').splitlines()
   a=max(1,e['start_line']-1);b=min(len(ls),e['end_line']+1)
   ranges.setdefault(e['path'],set()).update(range(a,b+1))
 for path,nn in sorted(ranges.items()):
  ls=(R/'inputs'/c/path).read_text(encoding='utf-8-sig').splitlines()
  print('\nSOURCE '+path)
  if mode=='source-new':
   old=nn & reused.get(path,set())
   if old:print('REUSED '+str(len(old))+' already-inspected lines from current-pass policy receipts; no second review credit.')
   nn=nn-old
  prev=0
  for n in sorted(nn):
   if n>prev+1:print('...')
   print(str(n)+': '+ls[n-1]);prev=n
if mode=='baseline':
 for r in records:
  if r['record_kind']=='policies.jsonl':continue
  print(r['index_key']+' | '+','.join(r['policy_references'])+' | '+str(r['claimed_normative_action'])+' | exceptions: '+str(r['exceptions']))

