"""Read-only check that this folder is still what the final audit saw. Takes about a minute and writes nothing.

  PYTHONPATH=_tools python -B _tools/verify_final.py

It checks the fence, every candidate file against V2_FINAL_MANIFEST.json, and that a replay from the frozen baseline gives the stored view. To repeat the whole audit, run _tools/final_audit_v2.py: it takes about 20 minutes, regenerates its result files, and leaves candidates untouched.
"""
import sys

import dataset
from fence import verify as fence_verify
from rcommon import CANDIDATES, out_path, read_json, read_jsonl, rec_hash, sha256_file, template_root, utf8_stdout, walk_files, wc_path


def main():
    utf8_stdout()
    errors = []
    f = fence_verify()
    errors += f['errors'][:10]
    man = read_json(out_path('V2_FINAL_MANIFEST.json'))['candidates']
    n = 0
    for c in CANDIDATES:
        files = man[c]['files']
        now = set(walk_files(template_root(c)))
        if now != set(files):
            errors.append('%s: file set differs: %s' % (c, sorted(now ^ set(files))[:5]))
        for rel in now & set(files):
            n += 1
            if sha256_file(wc_path(c, rel)) != files[rel]['sha256']:
                errors.append('%s: %s differs from the manifest' % (c, rel))
    rows, cross = dataset.build()
    if rec_hash([r for c in CANDIDATES for r in rows[c]]) != rec_hash(read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))):
        errors.append('the replay differs from REPAIRED_CLASSIFICATIONS.jsonl')
    if rec_hash(cross) != rec_hash(read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))):
        errors.append('the replay differs from ORIGINAL_TO_REPAIRED_CLAIMS.jsonl')
    print({'fenced_files_checked': sum(f['n_by_tree'].values()), 'candidate_files_checked': n, 'errors': len(errors)})
    for e in errors:
        print('ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
