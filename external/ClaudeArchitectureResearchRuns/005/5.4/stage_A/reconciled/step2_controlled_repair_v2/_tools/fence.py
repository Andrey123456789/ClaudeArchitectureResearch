"""Immutable-input fence for v2: hash everything the contract freezes and compare later.

snapshot: writes FENCE_SNAPSHOT.json. verify(): returns a dict; any changed, missing or new file in a fenced tree is an error.
Fenced: inputs, step1_union, step1_union_augmented_pass1, step2_classification, step2_semantic_audit_v1, step2_controlled_repair_v1 (with its archive) and the kit files.
A kit file the user adds later is tolerated; a changed or removed known kit file is an error.
stage_A/codex_iterative_search* is never read, listed, hashed or stat'ed by this run, as the contract requires.
"""
import os
import sys

from rcommon import AUD, INPUTS, OUT, REC, ROOT, S2, V1, now, read_json, sha256_file, utf8_stdout, walk_files, write_json

KIT = os.path.join(ROOT, '_STAGE_A_KIT')
TREES = {'inputs': INPUTS, 'step1_union': os.path.join(REC, 'step1_union'), 'step1_union_augmented_pass1': os.path.join(REC, 'step1_union_augmented_pass1'), 'step2_classification': S2, 'semantic_audit': AUD, 'v1': V1, 'kit': KIT}
FILES = {'v1_archive': os.path.join(REC, 'step2_controlled_repair_v1.zip')}


def hash_tree(root):
    return {rel: sha256_file(os.path.join(root, rel.replace('/', os.sep))) for rel in walk_files(root)}


def snapshot():
    write_json('FENCE_SNAPSHOT.json', {'at': now(), 'trees': {k: hash_tree(v) for k, v in TREES.items()}, 'files': {k: sha256_file(v) for k, v in FILES.items()}, 'not_covered': 'stage_A/codex_iterative_search* is not read by this run.'})


def verify():
    errors = []
    snap = read_json(os.path.join(OUT, 'FENCE_SNAPSHOT.json'))
    counts = {}
    for name, root in TREES.items():
        cur = hash_tree(root)
        want = snap['trees'][name]
        counts[name] = len(want)
        for rel in set(cur) | set(want):
            if rel not in cur:
                errors.append('missing %s/%s' % (name, rel))
            elif rel not in want:
                if name != 'kit':
                    errors.append('new file %s/%s' % (name, rel))
            elif cur[rel] != want[rel]:
                errors.append('changed %s/%s' % (name, rel))
    for name, p in FILES.items():
        if not os.path.exists(p) or sha256_file(p) != snap['files'][name]:
            errors.append('changed or missing %s' % name)
    man = read_json(os.path.join(AUD, 'UPSTREAM_MANIFEST.json'))
    n = 0
    for tree, entries in man['trees'].items():
        for rel, want in entries.items():
            n += 1
            p = os.path.join(ROOT, rel.replace('/', os.sep))
            if not os.path.exists(p):
                errors.append('missing ' + rel)
            elif sha256_file(p) != want:
                errors.append('changed ' + rel)
    return {'n_upstream_checked': n, 'n_by_tree': counts, 'errors': errors[:50], 'n_errors': len(errors)}


if __name__ == '__main__':
    utf8_stdout()
    if sys.argv[1] == 'snapshot':
        snapshot()
    print(verify())
