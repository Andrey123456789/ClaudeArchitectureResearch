"""Read-only source/baseline display helper. Retrieval never determines equivalence."""
import argparse,json,re
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parent.parent
p=argparse.ArgumentParser(); p.add_argument('mode',choices=['source','baseline','list']); p.add_argument('candidate'); p.add_argument('pattern',nargs='?',default=''); p.add_argument('--start',type=int,default=1); p.add_argument('--end',type=int,default=100000); p.add_argument('--all-kinds',action='store_true'); a=p.parse_args()
if a.mode in ['source','list']:
 for line in (O/'SOURCE_FILE_INDEX.jsonl').read_text(encoding='utf-8').splitlines():
  s=json.loads(line)
  if s['candidate']!=a.candidate or not re.search(a.pattern,s['path'],re.I): continue
  print(s['path'],s['line_count'])
  if a.mode=='source':
   for n,line in enumerate((R/'inputs'/a.candidate/s['path']).read_text(encoding='utf-8-sig').splitlines(),1):
    if a.start<=n<=a.end: print(f'{n}: {line}')
else:
 for line in (O/'BASELINE_RECORD_INDEX.jsonl').read_text(encoding='utf-8').splitlines():
  s=json.loads(line)
  if s['candidate']!=a.candidate: continue
  if not a.all_kinds and s['record_kind'] not in ['constraints.jsonl','BLIND_FINDINGS.jsonl','ORPHAN_CANDIDATES.jsonl']: continue
  if not re.search(a.pattern,json.dumps(s,ensure_ascii=False),re.I): continue
  print(json.dumps({k:s[k] for k in ['index_key','claimed_normative_action','labels','scope','modality','exceptions','policy_references']},ensure_ascii=False))
