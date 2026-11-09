"""Preflight: verify upstream hashes, create byte-identical working copies and write the two manifests.

Idempotent. If working copies already exist they are verified against WORKING_COPY_MANIFEST.json, never replaced.
"""
import csv
import os
import shutil
import sys

from rcommon import (AUD, CANDIDATES, INPUTS, OUT, ROOT, S2, VERSION, input_template_root, now, read_json, sha256_file, template_root,
                     utf8_stdout, walk_files, write_json)


def verify_upstream():
    man = read_json(os.path.join(AUD, 'UPSTREAM_MANIFEST.json'))
    n, bad, missing = 0, [], []
    for tree, entries in man['trees'].items():
        for rel, want in entries.items():
            n += 1
            p = os.path.join(ROOT, rel.replace('/', os.sep))
            if not os.path.exists(p):
                missing.append(rel)
                continue
            want_sha = want if isinstance(want, str) else want.get('sha256')
            if sha256_file(p) != want_sha:
                bad.append(rel)
    return {'n_checked': n, 'n_files_by_tree': man['n_files'], 'mismatch': bad, 'missing': missing}


def verify_input_csv():
    p = os.path.join(INPUTS, 'INPUT_MANIFEST_SHA256.csv')
    n, bad = 0, []
    with open(p, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            n += 1
            fp = os.path.join(INPUTS, row['relative_path'].replace('/', os.sep))
            if not os.path.exists(fp) or sha256_file(fp) != row['sha256']:
                bad.append(row['relative_path'])
    return {'n_checked': n, 'mismatch': bad}


def main():
    utf8_stdout()
    up = verify_upstream()
    csvr = verify_input_csv()
    print('upstream', up['n_checked'], up['n_files_by_tree'], 'bad', len(up['mismatch']), 'missing', len(up['missing']))
    print('input csv', csvr['n_checked'], 'bad', len(csvr['mismatch']))
    if up['mismatch'] or up['missing'] or csvr['mismatch']:
        print('STOP: upstream hash mismatch', up['mismatch'][:10], up['missing'][:10], csvr['mismatch'][:10])
        return 2
    base = {'version': VERSION, 'created_at': now(), 'upstream_verification': up, 'input_csv_verification': csvr,
            'frozen_classification_sha256': {}, 'candidates': {}}
    for c in CANDIDATES:
        root = input_template_root(c)
        files = {rel: sha256_file(os.path.join(root, rel.replace('/', os.sep))) for rel in walk_files(root)}
        base['candidates'][c] = {'template_root': 'inputs/%s/output/template' % c, 'n_files': len(files), 'files': files,
                                 'candidate_md_sha256': sha256_file(os.path.join(INPUTS, c, 'CANDIDATE.md')),
                                 'inventory_sha256': sha256_file(os.path.join(INPUTS, c, 'source', 'inventory.json')),
                                 'shared_invariants_sha256': sha256_file(os.path.join(INPUTS, c, 'source', 'shared-research-invariants.json'))}
        pc = os.path.join(S2, 'per_candidate', c)
        base['frozen_classification_sha256'][c] = {n: sha256_file(os.path.join(pc, n)) for n in ('CLASSIFICATIONS.jsonl', 'POLICY_COVERAGE.jsonl')}
    if len({base['candidates'][c]['inventory_sha256'] for c in CANDIDATES}) != 1:
        print('STOP: inventories differ')
        return 2
    bp = os.path.join(OUT, 'BASELINE_MANIFEST.json')
    if os.path.exists(bp):
        old = read_json(bp)
        for c in CANDIDATES:
            if old['candidates'][c]['files'] != base['candidates'][c]['files']:
                print('STOP: BASELINE_MANIFEST differs from inputs for', c)
                return 2
        print('baseline manifest verified, unchanged')
    else:
        write_json('BASELINE_MANIFEST.json', base)
    wp = os.path.join(OUT, 'WORKING_COPY_MANIFEST.json')
    if os.path.exists(wp):
        print('working copy manifest exists; not replacing')
        return 0
    wc = {'version': VERSION, 'created_at': now(), 'origin': 'byte-for-byte copy of inputs/<C>/output/template before first patch', 'candidates': {}}
    for c in CANDIDATES:
        src, dst = input_template_root(c), template_root(c)
        if os.path.exists(dst) and os.listdir(dst):
            print('STOP: unknown existing working copy for', c)
            return 2
        rows = {}
        for rel in walk_files(src):
            s = os.path.join(src, rel.replace('/', os.sep))
            d = os.path.join(dst, rel.replace('/', os.sep))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)
            a, b = sha256_file(s), sha256_file(d)
            if a != b:
                print('STOP: copy mismatch', c, rel)
                return 2
            rows[rel] = {'original_sha256': a, 'copy_at_creation_sha256': b, 'origin': 'inputs/%s/output/template/%s' % (c, rel)}
        wc['candidates'][c] = {'working_root': 'stage_A/reconciled/step2_controlled_repair_v1/candidates/%s/template' % c, 'n_files': len(rows), 'files': rows}
        print(c, 'copied', len(rows))
    write_json('WORKING_COPY_MANIFEST.json', wc)
    return 0


if __name__ == '__main__':
    sys.exit(main())
