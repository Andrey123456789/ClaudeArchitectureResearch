"""Phase 0: verify the audit universe and freeze upstream fingerprints.

  python -B _tools/preflight.py manifest   hash every upstream file into UPSTREAM_MANIFEST.json (refuses to overwrite)
  python -B _tools/preflight.py counts     recompute counts from files, compare with the expected reference counts
  python -B _tools/preflight.py replay     run Step 2's own validator on an isolated copy inside this folder
  python -B _tools/preflight.py verify     re-hash upstream against the manifest (read-only; used by the gates)

Step 2's `finalize.py validate` writes VALIDATION_RESULT.json into its own folder, so it is never run in place. The replay
copies the needed trees to _isolated_validator/, runs there, keeps the result under PREFLIGHT/, and removes the copy.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter

from acommon import (CANDIDATES, EXPECTED_RECORDS, INPUTS, OUT, P1, REC, ROOT, S1, S2, out_path, read_jsonl, sha256_file, utf8_stdout,
                     write_json)

TREES = {'inputs': INPUTS, 'step1_union': S1, 'step1_union_augmented_pass1': P1, 'step2_classification': S2}


def hash_tree(base):
    d = {}
    for dp, dn, fn in os.walk(base):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            d[os.path.relpath(p, ROOT).replace(os.sep, '/')] = sha256_file(p)
    return d


def manifest():
    p = out_path('UPSTREAM_MANIFEST.json')
    if os.path.exists(p):
        raise SystemExit('UPSTREAM_MANIFEST.json exists; it is frozen. Use verify.')
    trees = {k: hash_tree(v) for k, v in TREES.items()}
    write_json('UPSTREAM_MANIFEST.json', {'frozen_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'trees': trees,
                                          'n_files': {k: len(v) for k, v in trees.items()},
                                          'excluded': 'The Codex Pass 2 search folder is neither read nor hashed'})
    print({k: len(v) for k, v in trees.items()})


def verify(quiet=False):
    m = json.load(open(out_path('UPSTREAM_MANIFEST.json'), encoding='utf-8'))
    bad, missing, added = [], [], []
    for name, base in TREES.items():
        cur = hash_tree(base)
        old = m['trees'][name]
        bad += [k for k in old if k in cur and cur[k] != old[k]]
        missing += [k for k in old if k not in cur]
        added += [k for k in cur if k not in old]
    res = {'changed': bad, 'missing': missing, 'added': added, 'n_checked': sum(len(v) for v in m['trees'].values())}
    if not quiet:
        print(res)
    return res


def counts():
    rep = {'records': {}, 'coverage': {}}
    keys = set()
    for c in CANDIDATES:
        rows = read_jsonl(os.path.join(S2, 'per_candidate', c, 'CLASSIFICATIONS.jsonl'))
        ks = [r['source_key'] for r in rows]
        keys |= set(ks)
        cov = read_jsonl(os.path.join(S2, 'per_candidate', c, 'POLICY_COVERAGE.jsonl'))
        rep['records'][c] = {'n': len(rows), 'unique': len(set(ks)), 'expected': EXPECTED_RECORDS[c],
                             'classes': dict(Counter(r['classification'] for r in rows)),
                             'types': dict(Counter(r['view_record_type'] for r in rows))}
        rep['coverage'][c] = {'n': len(cov), 'unique': len({r['policy_id'] for r in cov}),
                              'status': dict(Counter(r['status'] for r in cov)),
                              'strength_status': dict(Counter(r['strength_status'] for r in cov)),
                              'overrides': sum(1 for r in cov if r.get('reviewer_override_note'))}
    rep['total_records'] = sum(v['n'] for v in rep['records'].values())
    rep['unique_keys'] = len(keys)
    rep['total_coverage'] = sum(v['n'] for v in rep['coverage'].values())
    rep['candidates'] = len(CANDIDATES)
    rep['ok'] = (rep['total_records'] == 6402 and rep['unique_keys'] == 6402 and rep['total_coverage'] == 1176
                 and all(v['n'] == v['expected'] == v['unique'] for v in rep['records'].values())
                 and all(v['n'] == 196 == v['unique'] for v in rep['coverage'].values()))
    hashes = json.load(open(os.path.join(S2, 'INPUT_HASHES.json'), encoding='utf-8'))
    table = hashes.get('files', hashes)
    bad = [p for p, h in table.items() if isinstance(h, str) and (not os.path.exists(os.path.join(ROOT, p)) or sha256_file(os.path.join(ROOT, p)) != h)]
    rep['step2_INPUT_HASHES'] = {'n': len(table), 'mismatches': bad}
    write_json('PREFLIGHT/COUNTS.json', rep)
    print(json.dumps({k: rep[k] for k in ('total_records', 'unique_keys', 'total_coverage', 'ok')}), 'INPUT_HASHES mismatches', len(bad))
    return rep


def replay():
    iso = out_path('_isolated_validator')
    if os.path.exists(iso):
        shutil.rmtree(iso)
    before = sha256_file(os.path.join(S2, 'VALIDATION_RESULT.json'))
    rec_iso = os.path.join(iso, 'stage_A', 'reconciled')
    os.makedirs(rec_iso)
    shutil.copytree(INPUTS, os.path.join(iso, 'inputs'))
    for name, src in (('step1_union', S1), ('step1_union_augmented_pass1', P1), ('step2_classification', S2)):
        shutil.copytree(src, os.path.join(rec_iso, name))
    tools = os.path.join(rec_iso, 'step2_classification', '_tools')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    t0 = time.time()
    r = subprocess.run([sys.executable, '-B', os.path.join(tools, 'finalize.py'), 'validate'], cwd=os.path.join(rec_iso, 'step2_classification'),
                       env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    res_path = os.path.join(rec_iso, 'step2_classification', 'VALIDATION_RESULT.json')
    res = json.load(open(res_path, encoding='utf-8'))
    after = sha256_file(os.path.join(S2, 'VALIDATION_RESULT.json'))
    write_json('PREFLIGHT/VALIDATOR_REPLAY.json', {
        'isolation': 'Copied inputs/, step1_union, step1_union_augmented_pass1 and step2_classification to _isolated_validator/ '
                     '(same relative layout, so common.py resolves ROOT to the copy). finalize.py validate ran from the copy with -B. '
                     'The copy was then deleted; only this result is kept.',
        'returncode': r.returncode, 'stdout_tail': r.stdout[-800:], 'stderr_tail': r.stderr[-800:], 'seconds': round(time.time() - t0, 1),
        'upstream_VALIDATION_RESULT_sha256_before': before, 'upstream_VALIDATION_RESULT_sha256_after': after,
        'upstream_unchanged': before == after, 'status': res['status'], 'failed_gates': res['failed_gates'],
        'gates': [{'gate': g['gate'], 'status': g['status'], 'n_errors': g['n_errors']} for g in res['gates']],
        'meaning': 'A replay of the structural validator. It says nothing about whether any reading is right.'})
    shutil.rmtree(iso)
    print('replay', res['status'], res['failed_gates'], 'gates', len(res['gates']), 'upstream unchanged', before == after, 'rc', r.returncode)


def main():
    utf8_stdout()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'manifest':
        manifest()
    elif cmd == 'counts':
        counts()
    elif cmd == 'replay':
        replay()
    elif cmd == 'verify':
        r = verify()
        raise SystemExit(1 if (r['changed'] or r['missing'] or r['added']) else 0)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
