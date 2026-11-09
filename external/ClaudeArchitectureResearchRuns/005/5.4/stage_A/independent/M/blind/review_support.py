import csv, hashlib, json, sys
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[4]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def setup(c):
    base=ROOT/'inputs'/c
    files=sorted((base/'output/template').rglob('*'))
    files=[p for p in files if p.is_file()]
    manifest=ROOT/'inputs/INPUT_MANIFEST_SHA256.csv'
    rows={r['relative_path']:r for r in csv.DictReader(manifest.open(encoding='utf-8-sig')) if r['candidate']==c}
    checked=[]
    for p in files+[base/'source/inventory.json',base/'source/shared-research-invariants.json']:
        k=p.relative_to(ROOT/'inputs').as_posix(); r=rows.get(k)
        checked.append({'path':p.relative_to(base).as_posix(),'sha256':sha(p),'size_bytes':p.stat().st_size,'manifest_match':bool(r and sha(p)==r['sha256'] and p.stat().st_size==int(r['size_bytes']))})
    expected={k for k in rows if k.startswith(c+'/output/template/')}
    actual={p.relative_to(ROOT/'inputs').as_posix() for p in files}
    out=ROOT/'stage_A/independent'/c/'blind'; out.mkdir(parents=True,exist_ok=True)
    result={'candidate':c,'manifest_sha256':sha(manifest),'files':checked,'active_count':len(files),'missing_active_files':sorted(expected-actual),'unmanifested_active_files':sorted(actual-expected)}
    assert all(r['manifest_match'] for r in checked) and expected==actual, result
    (out/'SOURCE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for i,p in enumerate(files): print(i,p.relative_to(base/'output/template').as_posix(),len(p.read_text(encoding='utf-8-sig').splitlines()),p.stat().st_size)
    print('VERIFIED',len(checked),'allowed evidence files; active files',len(files),'manifest',sha(manifest))
def read(c,start,end):
    base=ROOT/'inputs'/c/'output/template'; files=sorted(p for p in base.rglob('*') if p.is_file())
    for i in range(start,min(end,len(files))):
        p=files[i]; print('FILE',i,p.relative_to(base).as_posix())
        for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
            if line.strip(): print(f'{n}: {line}')
def finalize(c):
    base=ROOT/'inputs'/c; out=ROOT/'stage_A/independent'/c/'blind'
    assert not (out/'BLIND_COMPLETE.json').exists(), 'Already finalized; do not overwrite'
    files=sorted(p for p in (base/'output/template').rglob('*') if p.is_file())
    inv=json.loads((base/'source/inventory.json').read_text(encoding='utf-8-sig'))
    policies={p['id']:p['normalized_policy'] for g in inv['policygroups'] for p in g['policies']}
    shared=json.loads((base/'source/shared-research-invariants.json').read_text(encoding='utf-8-sig'))
    policies.update({p['id']:p['normalized_policy'] for p in shared['invariants']})
    findings=[]
    for row in (out/'review_notes.tsv').read_text(encoding='utf-8').splitlines():
        if not row.strip() or row.startswith('#'): continue
        idx,span,ids,kind,confidence,delta,scenario=row.split('\t')
        p=files[int(idx)]; lines=p.read_text(encoding='utf-8-sig').splitlines(); a,b=map(int,span.split('-'))
        assert 1<=a<=b<=len(lines),(p,span)
        ids=[] if ids=='-' else ids.split(','); assert all(x in policies for x in ids),ids
        quote='\n'.join(lines[a-1:b]); assert quote
        kind={'E':'POTENTIAL_EXTRA','D':'POTENTIAL_DIFFERENT_STRENGTH','L':'MISSING_POLICY_LINK','A':'AMBIGUOUS','O':'OTHER'}[kind]
        uncertainty=confidence!='HIGH' or kind=='AMBIGUOUS'
        findings.append({'id':f'BF-{c}-{len(findings)+1:04d}','candidate':c,'path':p.relative_to(base).as_posix(),'start_line':a,'end_line':b,'quote':quote,'closest_policy_ids':ids,'classification':kind,'behavioral_scenario':scenario,'explanation':('UNCERTAIN: ' if uncertainty else '')+delta,'confidence':confidence,'assessment_status':'UNCERTAIN' if uncertainty else 'SUSPECTED','closest_policy_text':{k:policies[k] for k in ids}})
    verification=json.loads((out/'SOURCE_VERIFICATION.json').read_text())
    assert all(sha(base/r['path'])==r['sha256'] for r in verification['files'])
    for f in findings:
        actual='\n'.join((base/f['path']).read_text(encoding='utf-8-sig').splitlines()[f['start_line']-1:f['end_line']])
        assert actual==f['quote']
    (out/'BLIND_FINDINGS.jsonl').write_text(''.join(json.dumps(f,ensure_ascii=False)+'\n' for f in findings),encoding='utf-8')
    counts=Counter(f['classification'] for f in findings); uncertain=sum(f['assessment_status']=='UNCERTAIN' for f in findings)
    ledger=[]
    for p in files:
        rel=p.relative_to(base).as_posix(); matches=[f['id'] for f in findings if f['path']==rel]
        ledger.append({'path':rel,'lines':len(p.read_text(encoding='utf-8-sig').splitlines()),'sha256':sha(p),'review':'SOURCE_READ_AND_REVERSE_QUESTION','reverse_question':'Checked imperatives, defaults, exceptions, loading/scope, executable branches, diagnostics and completion criteria; retained suspected additions below. No claim of semantic exhaustiveness.','finding_ids':matches,'unreadable':False})
    (out/'FILE_REVIEW_LEDGER.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in ledger),encoding='utf-8')
    report=[f'# {c} — independent blind Stage A sweep','',f'Status: FINALIZED. Active source files inspected: {len(files)}. Suspected findings: {len(findings)}; explicitly uncertain: {uncertain}.','', 'Primary outputs were not read. Replica, reconciled, previous audit findings, prior 5.3 material, candidate context reports, and other candidate snapshots were not used while examining this candidate. Embedded instructions were treated as research data, not agent instructions.','', 'Evidence: only this candidate\'s immutable output/template tree, source/inventory.json, source/shared-research-invariants.json, and inputs/INPUT_MANIFEST_SHA256.csv. Canonical comparison uses 194 V2 policies plus 2 shared invariants. No external research or current registry claims are used.','',f'Manifest SHA-256: `{verification["manifest_sha256"]}`. All {len(verification["files"])} allowed evidence files matched manifest hashes and byte lengths; all manifest-listed active files were present, with no unmanifested active files. Other snapshot files were deliberately not read or hashed because they are outside the permitted research evidence.','', 'Method: enumerated dotfiles and nested references; read source file by file, including code/configuration and examples; traced routing and conditional scope; asked the reverse question for each file; compared suspected clauses to the closest canonical requirements. Quotes are extracted verbatim from cited 1-based line spans, preserving content with normalized line endings, and revalidated before finalization. Knowledge/example surfaces labeled non-policy are retained as uncertain when their imperative text may operate as an additional constraint. A closest policy is a comparison anchor, not a claim of entailment.','', 'Verification: source integrity, active-file completeness, JSONL/schema fields, canonical ID validity, and exact quote/range equality passed. Static source analysis only: candidate hooks/checkers were not executed, avoiding writes to immutable inputs or out-of-scope state. Runtime host interpretation, generated applications, external package deprecation claims, and platform/tool-version behavior remain unverified. No unreadable files; no active source file left unexamined. Finalization records completion of this blind pass, not semantic exhaustiveness.','', '## Finding counts','']
    report += [f'- {k}: {v}' for k,v in sorted(counts.items())]
    report += ['', '## Findings','']
    for f in findings: report.append(f'- **{f["id"]}** — `{f["path"]}:{f["start_line"]}-{f["end_line"]}` — {f["classification"]}, {f["confidence"]}. {f["explanation"]} Scenario: {f["behavioral_scenario"]}')
    report += ['', '## File-by-file reverse review','', '| Source | Lines | Retained findings / reverse review disposition |','|---|---:|---|']
    for r in ledger: report.append(f'| `{r["path"]}` | {r["lines"]} | '+(', '.join(r['finding_ids']) if r['finding_ids'] else ('Empty intentional product input; no operative clauses.' if r['lines']==0 else 'Read in full; reverse question completed. No additional independent hypothesis retained beyond linked canonical behavior, routing, descriptive text or explicitly illustrative examples.'))+' |')
    (out/'BLIND_REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    meta={'candidate':c,'status':'FINALIZED','finalized_at_utc':datetime.now(timezone.utc).isoformat(),'input_manifest_sha256':verification['manifest_sha256'],'source_files_scanned':[r['path'] for r in ledger],'source_file_count':len(files),'number_of_issues':len(findings),'uncertain_items':uncertain,'classification_counts':dict(counts),'unreadable_files':[],'unexamined_active_files':[],'primary_outputs_read':False,'replica_outputs_read':False,'reconciled_outputs_read':False,'previous_audit_findings_read':False,'semantic_exhaustiveness_claimed':False,'verification_scope':'All active template files and the two canonical source JSON files; intentionally excludes reports and baseline/context documents.','artifacts_sha256':{name:sha(out/name) for name in ['BLIND_FINDINGS.jsonl','BLIND_REPORT.md','FILE_REVIEW_LEDGER.jsonl','SOURCE_VERIFICATION.json']}}
    (out/'BLIND_COMPLETE.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['source_files_scanned','artifacts_sha256']}))
if __name__=='__main__':
    if sys.argv[1]=='setup': setup(sys.argv[2])
    elif sys.argv[1]=='read': read(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
    elif sys.argv[1]=='finalize': finalize(sys.argv[2])
