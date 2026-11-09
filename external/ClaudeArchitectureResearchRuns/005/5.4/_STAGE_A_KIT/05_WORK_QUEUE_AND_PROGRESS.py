#!/usr/bin/env python3
"""Stage A work queue and read-only checkpoint verification.

init: create stable batches from immutable snapshot (no candidate edits).
check: validate claimed completed batches against the partial extraction ledgers.
A checkpoint PASS proves accounted-for lines, NOT semantic correctness.
"""
import argparse
import hashlib
import json
from pathlib import Path

CANDIDATES = ('M','M1','L0','L1','K0','K1')
NORMATIVE = {'ORACLE_LINKED','EXTRA','LINK_UNCERTAIN','MIXED'}
ALL_DISPOSITIONS = NORMATIVE | {'NON_NORMATIVE','IMPLEMENTATION','DUPLICATE'}

def read_jsonl(path):
    if not path.exists():
        return []
    result=[]
    for n, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if line.strip():
            try:
                row=json.loads(line)
            except Exception as e:
                raise ValueError(f'{path}:{n}: {e}')
            if not isinstance(row,dict):
                raise ValueError(f'{path}:{n}: expected JSON object')
            result.append(row)
    return result

def generate(root, candidate, max_nonblank):
    tmpl=root/'inputs'/candidate/'output'/'template'
    if not tmpl.exists():
        raise ValueError(f'Missing snapshot {tmpl}')
    files=[]
    for p in sorted(tmpl.rglob('*')):
        if not p.is_file():
            continue
        data=p.read_bytes()
        rel=p.relative_to(root/'inputs'/candidate).as_posix()
        try:
            if b'\0' in data: raise UnicodeError('NUL')
            lines=data.decode('utf-8-sig').splitlines()
            ftype='text'
            nonblank=sum(bool(x.strip()) for x in lines)
            line_count=len(lines)
        except (UnicodeError,UnicodeDecodeError):
            ftype='binary'
            nonblank=0
            line_count=0
        files.append({'path':rel,'type':ftype,'sha256':hashlib.sha256(data).hexdigest(),
                      'total_lines':line_count,'nonblank_lines':nonblank,'bytes':len(data)})
    batches=[]
    group=[]
    load=0
    for row in files:
        weight=max(row['nonblank_lines'],1)
        if group and load+weight>max_nonblank:
            batches.append({'id':f'B{len(batches)+1:03}', 'files':group, 'nonblank_lines':load})
            group=[]
            load=0
        group.append(row['path'])
        load+=weight
    if group:
        batches.append({'id':f'B{len(batches)+1:03}', 'files':group, 'nonblank_lines':load})
    return {'schema_version':1,'candidate':candidate,'snapshot_root':f'inputs/{candidate}',
            'max_batch_nonblank_lines':max_nonblank,'files':files,'batches':batches}

def check(root, candidate, plan):
    out=root/'stage_A'/'primary'/candidate
    progress_path=out/'PROGRESS.json'
    if not progress_path.is_file():
        raise ValueError(f'Missing progress file: {progress_path}')
    state=json.loads(progress_path.read_text(encoding='utf-8-sig'))
    if state.get('candidate')!=candidate:
        raise ValueError('PROGRESS candidate mismatch')
    completed=state.get('completed_batch_ids',[])
    if not isinstance(completed,list) or len(completed)!=len(set(completed)):
        raise ValueError('Invalid completed_batch_ids')
    by_batch={b['id']:b for b in plan['batches']}
    for bid in completed:
        if bid not in by_batch:
            raise ValueError(f'Unknown batch {bid}')
    file_rows=read_jsonl(out/'files.jsonl')
    spans=read_jsonl(out/'coverage_ranges.jsonl')
    constraints=read_jsonl(out/'constraints.jsonl')
    rows_by_path={}
    errors=[]
    for row in file_rows:
        p=row.get('path')
        if p in rows_by_path:
            errors.append(f'Duplicate files.jsonl entry {p}')
        rows_by_path[p]=row
    spans_by_path={}
    ids=set()
    for s in spans:
        sid=s.get('segment_id')
        if sid in ids: errors.append(f'Duplicate segment ID: {sid}')
        ids.add(sid)
        spans_by_path.setdefault(s.get('path'),[]).append(s)
    cids={c.get('id') for c in constraints}
    file_index={f['path']:f for f in plan['files']}
    for bid in completed:
        for path in by_batch[bid]['files']:
            meta=file_index[path]
            current=(root/'inputs'/candidate/path).read_bytes()
            if hashlib.sha256(current).hexdigest()!=meta['sha256']:
                errors.append(f'Snapshot changed: {path}')
            if path not in rows_by_path:
                errors.append(f'Completed batch {bid} has uninventoried file {path}')
                continue
            if rows_by_path[path].get('type')!=meta['type']:
                errors.append(f'Wrong type for {path}')
            if meta['type']=='binary':
                continue
            lines=current.decode('utf-8-sig').splitlines()
            seen=set()
            for s in spans_by_path.get(path,[]):
                try:
                    a,b=int(s['start_line']),int(s['end_line'])
                    assert 1<=a<=b<=len(lines)
                except Exception:
                    errors.append(f'Invalid range in {path}: {s}')
                    continue
                if s.get('disposition') not in ALL_DISPOSITIONS:
                    errors.append(f'Invalid disposition in {path}:{a}-{b}')
                for i in range(a,b+1):
                    if i in seen: errors.append(f'Overlap {path}:{i}')
                    seen.add(i)
                if s.get('disposition') in NORMATIVE:
                    for cid in s.get('constraint_ids') or []:
                        if cid not in cids: errors.append(f'Unknown constraint {cid} in {path}:{a}')
                    if not s.get('constraint_ids'):
                        errors.append(f'Unlinked normative segment {path}:{a}')
                    quote=s.get('quote','')
                    if not quote or quote not in '\n'.join(lines[a-1:b]):
                        errors.append(f'Missing/inexact quote {path}:{a}')
                elif not str(s.get('reason','')).strip():
                    errors.append(f'Missing disposition reason {path}:{a}')
            uncovered=[i for i,line in enumerate(lines,1) if line.strip() and i not in seen]
            if uncovered:
                errors.append(f'Unclassified nonblank lines in {path}: {uncovered[:12]} (+{max(0,len(uncovered)-12)})')
    print(f'{candidate}: {len(completed)}/{len(by_batch)} claimed complete batches; {len(file_rows)} file rows, {len(spans)} coverage spans, {len(constraints)} constraints')
    if errors:
        for e in errors[:100]: print('ERROR:',e)
        if len(errors)>100: print(f'... {len(errors)-100} more')
        raise ValueError(f'CHECKPOINT FAIL ({len(errors)} problems)')
    print('PASS: claimed completed batches have structural coverage (not semantic proof).')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('operation', choices=('init','check'))
    ap.add_argument('--root',type=Path,default=Path('.'))
    ap.add_argument('--candidate',required=True,choices=CANDIDATES)
    ap.add_argument('--max-nonblank',type=int,default=500)
    a=ap.parse_args()
    root=a.root.resolve()
    location=root/'stage_A'/'_control'/f'{a.candidate}_WORK_QUEUE.json'
    if a.operation=='init':
        if location.exists():
            old=json.loads(location.read_text(encoding='utf-8'))
            new=generate(root,a.candidate,old['max_batch_nonblank_lines'])
            if old!=new:
                raise ValueError('Existing work queue does not match snapshot; no overwrite')
            print('PASS: existing queue identical:',location)
        else:
            plan=generate(root,a.candidate,a.max_nonblank)
            location.parent.mkdir(parents=True,exist_ok=True)
            location.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print('Created:',location, 'batches:',len(plan['batches']),'files:',len(plan['files']))
    else:
        if not location.is_file(): raise ValueError(f'Queue missing: {location}')
        plan=json.loads(location.read_text(encoding='utf-8'))
        current=generate(root,a.candidate,plan['max_batch_nonblank_lines'])
        if plan!=current: raise ValueError('Work queue changed or snapshot modified')
        check(root,a.candidate,plan)

if __name__=='__main__':
    main()
