"""Operational validation only; no cross-candidate semantic comparison.

Reads only finalized independent artifacts and each candidate's permitted immutable
template/canonical evidence. Writes only new completion evidence beside this script.
Never executes candidate code or changes finalized findings/reports/markers.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
CANDIDATES = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

def main():
    destinations = [OUT / 'SWEEP_COMPLETE.json', OUT / 'SWEEP_VALIDATION_SUMMARY.md']
    assert not any(p.exists() for p in destinations), 'Preserve previous completion evidence; version any later run.'
    manifest_hash = sha(ROOT / 'inputs/INPUT_MANIFEST_SHA256.csv')
    results = []
    protected = {}
    for candidate in CANDIDATES:
        folder = ROOT / 'stage_A/independent' / candidate / 'blind'
        base = ROOT / 'inputs' / candidate
        marker_path = folder / 'BLIND_COMPLETE.json'
        meta = read_json(marker_path)
        assert meta['status'] == 'FINALIZED' and meta['candidate'] == candidate
        assert meta['input_manifest_sha256'] == manifest_hash
        for name, expected in meta['artifacts_sha256'].items():
            path = folder / name
            assert sha(path) == expected, (candidate, name)
            protected[str(path.relative_to(ROOT))] = expected
        protected[str(marker_path.relative_to(ROOT))] = sha(marker_path)
        inv = read_json(base / 'source/inventory.json')
        policies = {p['id']: p['normalized_policy'] for group in inv['policygroups'] for p in group['policies']}
        policies.update({p['id']: p['normalized_policy'] for p in read_json(base / 'source/shared-research-invariants.json')['invariants']})
        assert len(policies) == 196
        findings = read_jsonl(folder / 'BLIND_FINDINGS.jsonl')
        ledger = read_jsonl(folder / 'FILE_REVIEW_LEDGER.jsonl')
        verified = read_json(folder / 'SOURCE_VERIFICATION.json')
        active = {p.relative_to(base).as_posix(): p for p in (base / 'output/template').rglob('*') if p.is_file()}
        assert set(meta['source_files_scanned']) == set(active)
        assert len(meta['source_files_scanned']) == len(active) == meta['source_file_count']
        assert {r['path'] for r in ledger} == set(active) and len(ledger) == len(active)
        expected_evidence = set(active) | {'source/inventory.json', 'source/shared-research-invariants.json'}
        assert {r['path'] for r in verified['files']} == expected_evidence
        assert len(verified['files']) == len(expected_evidence)
        for row in verified['files']:
            path = base / row['path']
            assert row['manifest_match'] and row['sha256'] == sha(path) and row['size_bytes'] == path.stat().st_size
        linked = {path: [] for path in active}
        for ordinal, finding in enumerate(findings, 1):
            assert finding['id'] == f'BF-{candidate}-{ordinal:04d}'
            assert finding['candidate'] == candidate and finding['path'] in active
            assert type(finding['start_line']) is int and type(finding['end_line']) is int
            assert isinstance(finding['closest_policy_ids'], list)
            assert len(set(finding['closest_policy_ids'])) == len(finding['closest_policy_ids'])
            assert set(finding['closest_policy_ids']) <= set(policies)
            assert finding['closest_policy_text'] == {key: policies[key] for key in finding['closest_policy_ids']}
            uncertain = finding['confidence'] != 'HIGH' or finding['classification'] == 'AMBIGUOUS'
            assert finding['assessment_status'] == ('UNCERTAIN' if uncertain else 'SUSPECTED')
            assert finding['explanation'].startswith('UNCERTAIN: ') == uncertain
            linked[finding['path']].append(finding['id'])
        for row in ledger:
            assert row['finding_ids'] == linked[row['path']]
            assert row['lines'] == len(active[row['path']].read_text(encoding='utf-8-sig').splitlines())
            assert row['review'] == 'SOURCE_READ_AND_REVERSE_QUESTION' and row['unreadable'] is False
        uncertain_count = sum(f['assessment_status'] == 'UNCERTAIN' for f in findings)
        assert uncertain_count == meta['uncertain_items']
        assert len(findings) == meta['number_of_issues']
        assert dict(Counter(f['classification'] for f in findings)) == meta['classification_counts']
        assert not meta['unreadable_files'] and not meta['unexamined_active_files']
        for field in ['primary_outputs_read', 'replica_outputs_read', 'reconciled_outputs_read', 'previous_audit_findings_read', 'semantic_exhaustiveness_claimed']:
            assert meta[field] is False
        validations = [read_json(p) for p in folder.glob('*VALIDATION*.json')]
        assert validations and all(v['status'] == 'PASS' for v in validations)
        latest = max(validations, key=lambda x: x['validated_at_utc'])
        assert latest['issues'] == len(findings) and latest['source_file_count'] == len(active)
        results.append({'candidate': candidate, 'status': 'FINALIZED', 'validation': 'PASS', 'source_files': len(active), 'allowed_evidence_files': len(expected_evidence), 'potential_findings': len(findings), 'uncertain_items': uncertain_count, 'classification_counts': meta['classification_counts'], 'finalized_at_utc': meta['finalized_at_utc'], 'latest_validation_at_utc': latest['validated_at_utc']})
    for relative, expected in protected.items():
        assert sha(ROOT / relative) == expected, ('changed during validation', relative)
    result = {
        'status': 'ALL_SIX_INDEPENDENT_BLIND_PASSES_FINALIZED',
        'validated_at_utc': datetime.now(timezone.utc).isoformat(),
        'manifest_sha256': manifest_hash,
        'candidates': results,
        'totals': {key: sum(r[key] for r in results) for key in ['source_files', 'allowed_evidence_files', 'potential_findings', 'uncertain_items']},
        'checks': ['Per-candidate saved validator: schema, exact source quotes/ranges, canonical IDs, manifest hashes/sizes, artifact hashes and active coverage PASS', 'Supplemental: sequential finding IDs, exact stored canonical text, uncertainty counts/labels, exact per-file finding links, line counts and source-verification coverage PASS', 'All finalized artifact digests match stored finalization hashes; markers and artifacts unchanged during final validation'],
        'preserved_artifacts_sha256': protected,
        'unresolved': 'All findings are independent hypotheses, not adjudicated violations; uncertain items remain explicitly labeled. No reconciliation performed.',
        'limitations': ['Static source analysis only; candidate scripts/hooks were not executed.', 'No runtime host, generated application, external registry/deprecation or tool-version validation.', 'Coverage proves every active file was represented in the source/reverse-review ledger, not semantic exhaustiveness.', 'Integrity scope is the active template trees and two canonical source files per candidate; descriptive reports and other forbidden/out-of-scope inputs were not opened or hashed.', 'Counts are extraction records, not unique canonical-policy counts or comparative architecture scores.'],
        'blind_independence': 'No primary, replica, reconciled, prior Phase 5.3 or other non-blind audit findings read. No Stage B comparison.',
    }
    destinations[0].write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    lines = ['# Stage A independent blind sweep — completion validation', '',
        'All six independent blind passes are FINALIZED and validation is PASS. This is an operational completion record, not a comparison of candidate architectures or reconciliation of findings.', '',
        '| Candidate | Active files | Potential findings | Uncertain subset | Validation |',
        '|---|---:|---:|---:|---|']
    lines += [f"| {r['candidate']} | {r['source_files']} | {r['potential_findings']} | {r['uncertain_items']} | PASS |" for r in results]
    totals = result['totals']
    lines += [f"| Total | {totals['source_files']} | {totals['potential_findings']} | {totals['uncertain_items']} | PASS |", '',
        f"Verified {totals['allowed_evidence_files']} allowed evidence files (active templates plus 12 canonical source files) against the immutable manifest. Manifest SHA-256: `{manifest_hash}`.", '',
        '## Validation and preservation', '']
    lines += ['- ' + item for item in result['checks']]
    lines += ['', 'M, M1, L0 and L1 were recovered from valid final artifacts and were not reanalyzed or regenerated. K0 and K1 were completed in sequence. Existing findings, notes, references and support scripts were retained. Final validation adds new validation records; it does not replace final findings, reports or completion markers.', '',
        '## Unresolved findings', '', result['unresolved'], '',
        f"There are {totals['uncertain_items']} explicitly uncertain records among {totals['potential_findings']} potential findings. Exact IDs, source quotations, behavioral scenarios, nearest canonical policies and explanations remain in each candidate's BLIND_FINDINGS.jsonl and BLIND_REPORT.md. No findings were artificially resolved to reach completion.", '',
        '## Methodological limits', '']
    lines += ['- ' + item for item in result['limitations']]
    lines += ['', result['blind_independence'], '', 'All generated research and validation artifacts are under stage_A/independent/. No immutable input, canonical policy, candidate template or Claude result was modified.', '',
        f"Validation completed: {result['validated_at_utc']}", '']
    destinations[1].write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'totals': totals, 'validation': 'PASS', 'output': [str(p) for p in destinations]}))

if __name__ == '__main__':
    main()
