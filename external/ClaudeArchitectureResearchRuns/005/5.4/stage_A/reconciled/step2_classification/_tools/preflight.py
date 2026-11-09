"""Hash every immutable input consumed by Step 2 and verify the inputs manifest.

  python -B preflight.py           -> writes ../INPUT_HASHES.json (refuses to overwrite unless --force)
  python -B preflight.py --verify  -> recomputes and compares; exit 1 on any difference
"""
import csv
import json
import os
import sys

from common import (ROOT, OUT, S1, P1, INPUTS, CANDIDATES, sha256_file, write_json_atomic)

S1_FILES = ['MERGED_FINDINGS.jsonl', 'SOURCE_OCCURRENCES.jsonl', 'SOURCE_CLAUSES.jsonl',
            'SOURCE_RECORD_INDEX.jsonl', 'RECORD_ACCOUNTING.jsonl', 'MERGE_REVIEW_QUEUE.jsonl',
            'MERGE_DECISIONS.jsonl', 'CO_LOCATION_INDEX.jsonl', 'SOURCE_VERIFICATION_ISSUES.jsonl',
            'STEP1_UNION_REPORT.md', 'MERGE_PROTOCOL.md']
P1_FILES = ['AUGMENTED_UNION_VIEW.jsonl', 'NEW_CLAUSE_PROPOSALS.jsonl', 'EXISTING_GROUP_FACETS.jsonl',
            'PASS1_REVIEW_LEDGER.jsonl', 'UNRESOLVED_REVIEW_QUEUE.jsonl', 'REVIEW_REPORT.md',
            'INPUT_HASHES.json', 'VALIDATION_RESULT.json', 'UNION_AUGMENTATION_MANIFEST.json']


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


def collect():
    files = {}
    for f in S1_FILES:
        files[rel(os.path.join(S1, f))] = None
    for f in P1_FILES:
        files[rel(os.path.join(P1, f))] = None
    files[rel(os.path.join(INPUTS, 'INPUT_MANIFEST_SHA256.csv'))] = None
    for c in CANDIDATES:
        base = os.path.join(INPUTS, c)
        for dp, dn, fn in os.walk(base):
            for f in fn:
                files[rel(os.path.join(dp, f))] = None
    for k in files:
        files[k] = sha256_file(os.path.join(ROOT, k))
    return dict(sorted(files.items()))


def check_manifest():
    """Verify inputs/** against the supplied INPUT_MANIFEST_SHA256.csv."""
    bad = []
    with open(os.path.join(INPUTS, 'INPUT_MANIFEST_SHA256.csv'), encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        p = os.path.join(INPUTS, r['relative_path'].replace('/', os.sep))
        if not os.path.exists(p):
            bad.append(('MISSING', r['relative_path']))
        elif sha256_file(p) != r['sha256']:
            bad.append(('HASH_MISMATCH', r['relative_path']))
    return len(rows), bad


def main():
    target = os.path.join(OUT, 'INPUT_HASHES.json')
    n, bad = check_manifest()
    cur = collect()
    if '--verify' in sys.argv:
        old = json.load(open(target, encoding='utf-8'))['files']
        diff = [k for k in set(old) | set(cur) if old.get(k) != cur.get(k)]
        print('manifest rows %d, manifest mismatches %d, hashed files %d, changed %d'
              % (n, len(bad), len(cur), len(diff)))
        for d in sorted(diff)[:50]:
            print('  CHANGED', d)
        for b in bad[:50]:
            print('  ', *b)
        sys.exit(1 if (diff or bad) else 0)
    if os.path.exists(target) and '--force' not in sys.argv:
        print('INPUT_HASHES.json exists; use --verify'); sys.exit(2)
    if bad:
        print('input manifest mismatches:', bad[:20]); sys.exit(1)
    write_json_atomic(target, {'protocol_version': 'step2-v1', 'manifest_rows_verified': n,
                               'n_files': len(cur), 'files': cur})
    print('wrote', target, len(cur), 'files; manifest rows verified', n)


if __name__ == '__main__':
    main()
