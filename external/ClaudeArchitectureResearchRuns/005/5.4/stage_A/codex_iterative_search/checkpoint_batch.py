"""Commit manually reviewed batches. Does not generate semantic judgments."""
import json,hashlib,sys
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');t.replace(p)
def append(p,rows):
 old=p.read_text(encoding='utf-8') if p.exists() else ''
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(old+''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8');t.replace(p)
b=read(Path(sys.argv[1])); s=read(O/'STATE.json');d=O/'PASSES'/f"pass_{s['current_pass_id']:04d}"
if any(x['unit']==b['unit'] for x in s['completed_units']): raise RuntimeError('Batch already committed')
coverage=[];claims=[];comparisons=[];novel=[];unresolved=[];covered=[]
for f in b['files']:
 source=R/'inputs'/b['candidate']/f['path']; lines=source.read_text(encoding='utf-8-sig').splitlines()
 coverage.append({'candidate':b['candidate'],'path':f['path'],'sha256':sha(source),'line_count':len(lines),'read_index_status':f['read_index_status'],'inspected_ranges':f['inspected_ranges'],'hotspots':f['hotspots'],'deferred_deeper_reread':f['deferred_deeper_reread'],'review_notes':f['review_notes'],'batch':b['unit']})
for f in b.get('claims',[]):
 f={'candidate':b['candidate'],'discovery_pass':s['current_pass_id'],'discovery_strategy':s['current_strategy'],**f}
 lines=(R/'inputs'/f['candidate']/f['path']).read_text(encoding='utf-8-sig').splitlines();f['quote']='\n'.join(lines[f['start_line']-1:f['end_line']]);f['evidence_verification_status']='EXACT_SOURCE_VERIFIED_NEWLINES_NORMALIZED'
 claims.append(f);comparisons.append({'id':f['id']+'-CMP','claim_id':f['id'],'comparison_status':f['comparison_status'],'baseline_comparisons':f['baseline_comparisons'],'reason':f['comparison_reason']})
 if f['comparison_status'] in ['NOVEL_CLAUSE','RECLASSIFICATION_CANDIDATE']:novel.append(f)
 elif f['comparison_status']=='UNCERTAIN_NOVELTY':unresolved.append(f)
 elif f['comparison_status']=='ALREADY_COVERED':covered.append(f)
for name,rr in [('FILE_COVERAGE.jsonl',coverage),('CANDIDATE_CLAIMS.jsonl',claims),('NOVELTY_COMPARISONS.jsonl',comparisons)]:append(d/name,rr)
for name,rr in [('NOVEL_FINDINGS.jsonl',novel),('UNRESOLVED_FINDINGS.jsonl',unresolved),('ALREADY_COVERED_SAMPLES.jsonl',covered)]:append(O/name,rr)
receipt=d/(b['unit']+'.receipt.json');save(receipt,{'unit':b['unit'],'batch_input_sha256':sha(Path(sys.argv[1])),'coverage':coverage,'claim_ids':[x['id'] for x in claims]})
s['completed_units'].append({'unit':b['unit'],'outputs':{receipt.relative_to(O).as_posix():sha(receipt),Path(sys.argv[1]).resolve().relative_to(O).as_posix():sha(Path(sys.argv[1]))}})
s['candidate']=b.get('next_candidate',b['candidate']);s['next_file_batch']=b['next_action'];s['current_candidate_findings']=[x['id'] for x in novel+unresolved]
s['counts']['novel_findings']=len((O/'NOVEL_FINDINGS.jsonl').read_text(encoding='utf-8').splitlines());s['counts']['unresolved_findings']=len((O/'UNRESOLVED_FINDINGS.jsonl').read_text(encoding='utf-8').splitlines());save(O/'STATE.json',s)
p=O/'RESUME.md';text=p.read_text(encoding='utf-8-sig');text='\n'.join(('Next ONE action: '+b['next_action'] if line.startswith('Next ONE action:') else 'State truth: STATE.json. Current pointer: pass '+str(s['current_pass_id'])+', candidate '+s['candidate']+', after '+b['unit']+'.' if line.startswith('State truth:') else line) for line in text.splitlines())+'\n';p.write_text(text,encoding='utf-8')
print(json.dumps({'committed':b['unit'],'files':len(coverage),'claims':len(claims),'novel':len(novel),'unresolved':len(unresolved),'next':b['next_action']}))
