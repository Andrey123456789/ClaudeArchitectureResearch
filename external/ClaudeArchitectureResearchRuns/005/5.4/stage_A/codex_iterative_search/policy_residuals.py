"""Display source contexts outside committed policy retrieval; no review inference."""
import json,sys,re
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parent.parent
def jl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
s=json.loads((O/'STATE.json').read_text(encoding='utf-8-sig')); c=sys.argv[1]; pattern=sys.argv[2]
seen={}
for r in jl(O/'PASSES'/f"pass_{s['current_pass_id']:04d}"/'POLICY_BOUNDARY_REVIEW.jsonl'):
 if r['candidate']!=c:continue
 for e in r['retrieved_source_contexts']:
  for a,b in e['inspected_ranges']:seen.setdefault(e['path'],set()).update(range(a,b+1))
prior={r['path']:r for r in jl(O/'PASSES/pass_0001/FILE_COVERAGE.jsonl') if r['candidate']==c}
for r in jl(O/'SOURCE_FILE_INDEX.jsonl'):
 if r['candidate']!=c or not re.search(pattern,r['path']):continue
 print('\nSOURCE',r['path'])
 print('PRIOR_REVIEW',prior[r['path']]['review_notes'])
 last=0
 for n,l in enumerate((R/'inputs'/c/r['path']).read_text(encoding='utf-8-sig').splitlines(),1):
  if n in seen.get(r['path'],set()):continue
  if n!=last+1:print('...')
  print(f'{n}: {l}');last=n
