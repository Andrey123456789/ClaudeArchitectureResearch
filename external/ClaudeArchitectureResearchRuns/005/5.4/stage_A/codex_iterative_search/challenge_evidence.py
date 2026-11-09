"""Read-only family3 source packets; no automatic semantic classification."""
import json,sys,re
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent.parent
jl=lambda p:[json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
c,pattern,mode=sys.argv[1:4];rows=[r for r in jl(O/'BASELINE_RECORD_INDEX.jsonl') if r['candidate']==c]
findings=[r for n in ['NOVEL_FINDINGS.jsonl','UNRESOLVED_FINDINGS.jsonl'] for r in jl(O/n) if r['candidate']==c]
for f in jl(O/'SOURCE_FILE_INDEX.jsonl'):
 if f['candidate']!=c or not re.search(pattern,f['path']):continue
 path=f['path']; rr=[r for r in rows if any(e.get('path')==path for e in r['evidence'])];lines=(R/'inputs'/c/path).read_text(encoding='utf-8-sig').splitlines()
 targets=[r for r in rr if (r['record_kind']=='coverage_ranges.jsonl' and r['labels'].get('disposition') in ['NON_NORMATIVE','IMPLEMENTATION','MIXED']) or (r['record_kind']=='ORPHAN_CANDIDATES.jsonl' and r['labels'].get('resolution')!='EXTRA_REGISTERED')]
 selected=set()
 for r in targets:
  for e in r['evidence']:
   if e.get('path')==path and e.get('start_line') and e.get('end_line'): selected.update(range(max(1,e['start_line']-2),min(len(lines),e['end_line']+2)+1))
 # Also inspect any lines with no coverage evidence in either prior Claude run.
 annotated=set()
 for r in rr:
  if r['record_kind']=='coverage_ranges.jsonl':
   for e in r['evidence']:
    if e.get('path')==path and e.get('start_line') and e.get('end_line'):annotated.update(range(e['start_line'],e['end_line']+1))
 missing=set(range(1,len(lines)+1))-annotated;selected.update(missing)
 if mode=='inventory':print(path,len(lines),'challenge_lines',len(selected),'unannotated',len(missing),'targets',len(targets));continue
 print('\nFILE',path,'LINES',len(lines),'CHALLENGE',len(selected),'UNANNOTATED',len(missing))
 for x in findings:
  if x['path']==path:print('OWN',x['id'],x['claim'])
 if mode=='baseline':
  for r in rr:
   if r['record_kind'] in ['constraints.jsonl','BLIND_FINDINGS.jsonl','ORPHAN_CANDIDATES.jsonl']:print(r['index_key'],r['labels'],r['claimed_normative_action'])
  continue
 for r in targets:
  if r['record_kind']=='ORPHAN_CANDIDATES.jsonl':print('CHALLENGE',r['index_key'],r['labels'],r['claimed_normative_action'])
 if mode=='all':selected=set(range(1,len(lines)+1))
 last=0
 for n in sorted(selected):
  if n>last+1:print('...')
  print(f'{n}: {lines[n-1]}');last=n
