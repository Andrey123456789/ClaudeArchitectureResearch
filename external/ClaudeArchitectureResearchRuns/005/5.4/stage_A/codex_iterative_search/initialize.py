"""Read-only input inventory; writes exclusively beside this helper."""
import csv, hashlib, json
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
CANDIDATES = ['M','M1','L0','L1','K0','K1']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(name, obj):
    p=OUT/name; t=p.with_suffix(p.suffix+'.tmp')
    t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); t.replace(p)
def jsonl(name, rows):
    p=OUT/name; t=p.with_suffix(p.suffix+'.tmp')
    t.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8'); t.replace(p)
def rows(p):
    return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]

def main():
    state=json.loads((OUT/'STATE.json').read_text(encoding='utf-8-sig'))
    if state.get('baseline_fingerprint'): raise RuntimeError('Already frozen; use validator, do not reinitialize')
    errors=[]; counts={}; files=[]; sources=[]; index=[]; canonical=[]; completion={}
    for prefix in ['inputs','stage_A/primary','stage_A/replica','stage_A/independent']:
        for p in sorted((ROOT/prefix).rglob('*')):
            if not p.is_file(): continue
            files.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'size_bytes':p.stat().st_size})
            if p.suffix=='.jsonl':
                try: counts[p.relative_to(ROOT).as_posix()]=len(rows(p))
                except Exception as e: errors.append(f'Unreadable JSONL {p.relative_to(ROOT)}: {e}')
    for row in csv.DictReader((ROOT/'inputs/INPUT_MANIFEST_SHA256.csv').read_text(encoding='utf-8-sig').splitlines()):
        p=ROOT/'inputs'/row['relative_path']
        if not p.is_file(): errors.append('Missing manifest input: '+row['relative_path'])
        elif sha(p).lower()!=row['sha256'].lower(): errors.append('Manifest SHA mismatch: '+row['relative_path'])
        elif p.stat().st_size!=int(row['size_bytes']): errors.append('Manifest size mismatch: '+row['relative_path'])
    for c in CANDIDATES:
        base=ROOT/'inputs'/c
        for p in sorted((base/'output/template').rglob('*')):
            if not p.is_file(): continue
            data=p.read_bytes()
            try:
                content=data.decode('utf-8-sig'); binary='\x00' in content
            except UnicodeDecodeError: content=''; binary=True
            sources.append({'candidate':c,'path':p.relative_to(base).as_posix(),'sha256':sha(p),'size_bytes':len(data),'line_count':len(content.splitlines()) if not binary else None,'encoding':'binary' if binary else 'utf-8','status':'INDEXED_NOT_SEMANTICALLY_REVIEWED'})
        for name,field in [('inventory.json','policygroups'),('shared-research-invariants.json','invariants')]:
            p=base/'source'/name
            if not p.is_file(): errors.append(f'Missing canonical file {c}/{name}'); continue
            obj=json.loads(p.read_text(encoding='utf-8-sig'))
            policies=[v for g in obj[field] for v in g['policies']] if field=='policygroups' else obj[field]
            if len(policies)!=(194 if field=='policygroups' else 2): errors.append(f'Unexpected canonical count {c}/{name}: {len(policies)}')
            canonical.extend({'candidate':c,'source_path':'source/'+name,**r} for r in policies)
        for run in ['primary','replica','independent']:
            d=ROOT/'stage_A'/run/c
            if run=='independent': d=d/'blind'
            required=['BLIND_FINDINGS.jsonl','FILE_REVIEW_LEDGER.jsonl','BLIND_COMPLETE.json'] if run=='independent' else ['constraints.jsonl','coverage_ranges.jsonl','policies.jsonl','ORPHAN_CANDIDATES.jsonl','PROGRESS.json','EXTRACTION_REPORT.md']
            for name in required:
                if not (d/name).is_file(): errors.append(f'Missing required baseline {run}/{c}/{name}')
            if any(not (d/name).is_file() for name in required): continue
            complete_name='BLIND_COMPLETE.json' if run=='independent' else 'PROGRESS.json'
            completion[f'{run}/{c}']=json.loads((d/complete_name).read_text(encoding='utf-8-sig'))
            segs={r['segment_id']:r for r in rows(d/'coverage_ranges.jsonl')} if run!='independent' else {}
            kinds=['BLIND_FINDINGS.jsonl','FILE_REVIEW_LEDGER.jsonl'] if run=='independent' else ['constraints.jsonl','coverage_ranges.jsonl','policies.jsonl','ORPHAN_CANDIDATES.jsonl']
            for kind in kinds:
                for n,r in enumerate(rows(d/kind),1):
                    key=r.get('id',r.get('segment_id',r.get('rule_id',r.get('path',str(n)))))
                    evidence=[]; ambiguities=[]
                    for sid in r.get('evidence_segment_ids',[]):
                        if sid in segs: evidence.append({'run':run,**segs[sid]})
                        else: ambiguities.append('Unresolved same-run segment '+sid)
                    if r.get('path'): evidence.append({k:r[k] for k in ['path','start_line','end_line','quote'] if k in r})
                    claim=r.get('normative_action') or r.get('specific_behavior') or r.get('explanation') or r.get('reason') or r.get('search_notes') or r.get('reverse_question','')
                    index.append({'index_key':f'{run}/{c}/{kind}/{key}','run':run,'candidate':c,'record_kind':kind,'original_key':key,'record_number':n,'claimed_normative_action':claim,'labels':{k:r[k] for k in ['origin','classification','disposition','resolution','status','assessment_status'] if k in r},'evidence':evidence,'scope':r.get('trigger_scope'),'modality':r.get('modality'),'exceptions':r.get('exceptions'),'policy_references':r.get('policy_ids',r.get('closest_policy_ids',[r['rule_id']] if 'rule_id' in r else [])),'semantic_lookup':{'actor':None,'action_object':claim,'trigger_scope':r.get('trigger_scope'),'modality':r.get('modality'),'exceptions':r.get('exceptions'),'lifecycle':None,'note':'Missing dimensions require source-context interpretation; no equivalence inferred.'},'ambiguities':ambiguities,'raw_record':r})
    fingerprint=hashlib.sha256(''.join(f"{r['path']}\0{r['sha256']}\n" for r in sorted(files,key=lambda x:x['path'])).encode()).hexdigest()
    manifest={'status':'BLOCKED' if errors else 'FROZEN','baseline_fingerprint':fingerprint,'files':files,'jsonl_counts':counts,'errors':errors,'quote_normalization':'UTF-8; CRLF/CR normalized to LF only. No whitespace or punctuation normalization.'}
    atomic('BASELINE_MANIFEST.json',manifest)
    jsonl('SOURCE_FILE_INDEX.jsonl',sources); jsonl('BASELINE_RECORD_INDEX.jsonl',index); jsonl('CANONICAL_POLICY_INDEX.jsonl',canonical)
    atomic('BASELINE_COMPLETION_EVIDENCE.json',completion)
    loc=[]
    for rec in index:
        for ev in rec['evidence']:
            if 'path' in ev: loc.append({'candidate':rec['candidate'],'path':ev['path'].replace('\\','/'),'start_line':ev.get('start_line'),'end_line':ev.get('end_line'),'baseline_key':rec['index_key']})
    jsonl('BASELINE_LOCATION_MAP.jsonl',loc)
    for name in ['NOVEL_FINDINGS.jsonl','UNRESOLVED_FINDINGS.jsonl','ALREADY_COVERED_SAMPLES.jsonl']:
        if not (OUT/name).exists(): (OUT/name).write_text('',encoding='utf-8')
    state.update(baseline_fingerprint=fingerprint,final_status='BLOCKED' if errors else 'IN_PROGRESS',next_file_batch='Resolve frozen-input validation errors' if errors else 'Inspect baseline completion evidence then start Pass 0001',counts={'source_files':dict(Counter(r['candidate'] for r in sources)),'baseline_records':dict(Counter(r['run']+'/'+r['record_kind'] for r in index))},completed_units=[{'unit':'BASELINE_INDEX','outputs':{n:sha(OUT/n) for n in ['BASELINE_MANIFEST.json','SOURCE_FILE_INDEX.jsonl','BASELINE_RECORD_INDEX.jsonl','CANONICAL_POLICY_INDEX.jsonl','BASELINE_LOCATION_MAP.jsonl','BASELINE_COMPLETION_EVIDENCE.json']}}])
    atomic('STATE.json',state)
    print(json.dumps({'fingerprint':fingerprint,'errors':errors,'counts':state['counts'],'total_input_files':len(files)},indent=2))
if __name__=='__main__': main()
