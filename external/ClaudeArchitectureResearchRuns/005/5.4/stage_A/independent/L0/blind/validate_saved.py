import csv, hashlib, json, sys
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[4]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(c):
    out=ROOT/'stage_A/independent'/c/'blind'; base=ROOT/'inputs'/c
    meta=json.loads((out/'BLIND_COMPLETE.json').read_text(encoding='utf-8'))
    assert meta['candidate']==c and meta['status']=='FINALIZED'
    manifest=ROOT/'inputs/INPUT_MANIFEST_SHA256.csv'
    assert meta['input_manifest_sha256']==sha(manifest)
    for name,digest in meta['artifacts_sha256'].items(): assert sha(out/name)==digest,(c,name)
    files=sorted(p for p in (base/'output/template').rglob('*') if p.is_file())
    paths={p.relative_to(base).as_posix() for p in files}
    assert paths==set(meta['source_files_scanned']) and len(files)==meta['source_file_count']
    rows={r['relative_path']:r for r in csv.DictReader(manifest.open(encoding='utf-8-sig')) if r['candidate']==c}
    assert {c+'/'+p for p in paths}=={k for k in rows if k.startswith(c+'/output/template/')}
    for p in files+[base/'source/inventory.json',base/'source/shared-research-invariants.json']:
        r=rows[p.relative_to(ROOT/'inputs').as_posix()]
        assert sha(p)==r['sha256'] and p.stat().st_size==int(r['size_bytes'])
    inv=json.loads((base/'source/inventory.json').read_text(encoding='utf-8-sig'))
    ids={p['id'] for g in inv['policygroups'] for p in g['policies']}
    ids.update(p['id'] for p in json.loads((base/'source/shared-research-invariants.json').read_text(encoding='utf-8-sig'))['invariants'])
    findings=[json.loads(s) for s in (out/'BLIND_FINDINGS.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    seen=set()
    for f in findings:
        assert f['candidate']==c and f['id'] not in seen; seen.add(f['id'])
        assert f['path'] in paths and set(f['closest_policy_ids'])<=ids
        assert f['classification'] in {'POTENTIAL_EXTRA','POTENTIAL_DIFFERENT_STRENGTH','MISSING_POLICY_LINK','AMBIGUOUS','OTHER'}
        assert f['confidence'] in {'HIGH','MEDIUM','LOW'}
        assert all(f.get(k) for k in ['quote','behavioral_scenario','explanation'])
        lines=(base/f['path']).read_text(encoding='utf-8-sig').splitlines()
        a,b=f['start_line'],f['end_line']; assert 1<=a<=b<=len(lines)
        assert '\n'.join(lines[a-1:b])==f['quote']
    assert len(findings)==meta['number_of_issues']
    assert dict(Counter(f['classification'] for f in findings))==meta['classification_counts']
    ledger=[json.loads(s) for s in (out/'FILE_REVIEW_LEDGER.jsonl').read_text().splitlines()]
    assert {r['path'] for r in ledger}==paths and len(ledger)==len(paths)
    for r in ledger: assert r['sha256']==sha(base/r['path']) and set(r['finding_ids'])<=seen
    assert 'Primary outputs were not read.' in (out/'BLIND_REPORT.md').read_text(encoding='utf-8')
    result={'candidate':c,'validated_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','source_file_count':len(files),'issues':len(findings),'uncertain_items':meta['uncertain_items'],'checks':['artifact hashes','manifest hashes and sizes','active-file completeness','schema and canonical IDs','verbatim quotation ranges','ledger coverage','finalization counts'],'original_artifacts_modified':False}
    dest=out/'RESUME_VALIDATION.json'
    if dest.exists(): dest=out/('FINAL_VALIDATION_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.json')
    dest.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
for c in sys.argv[1:]: validate(c)
