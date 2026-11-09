"""Immutable-input fence: hash everything the contract freezes and compare later.

snapshot: writes FENCE_SNAPSHOT.json (audit tree and kit; inputs and Step 2 come from UPSTREAM_MANIFEST.json).
verify(): returns a dict; any mismatch, missing or new file in a fenced tree is an error.
stage_A/codex_iterative_search is neither read nor hashed, as in the audit.
"""
import os
import sys

from rcommon import AUD, OUT, REC, ROOT, S2, INPUTS, now, read_json, sha256_file, utf8_stdout, walk_files, write_json

KIT = os.path.join(ROOT, '_STAGE_A_KIT')
TREES = {'semantic_audit': AUD, 'kit': KIT}
UPSTREAM_DIRS = {'inputs': INPUTS, 'step1_union': os.path.join(REC, 'step1_union'), 'step1_union_augmented_pass1': os.path.join(REC, 'step1_union_augmented_pass1'), 'step2_classification': S2}


def hash_tree(root):
    return {rel: sha256_file(os.path.join(root, rel.replace('/', os.sep))) for rel in walk_files(root)}


def snapshot():
    write_json('FENCE_SNAPSHOT.json', {'at': now(), 'trees': {k: hash_tree(v) for k, v in TREES.items()}})


def verify():
    errors = []
    snap = read_json(os.path.join(OUT, 'FENCE_SNAPSHOT.json'))
    for name, root in TREES.items():
        cur = hash_tree(root)
        want = snap['trees'][name]
        for rel in set(cur) | set(want):
            if rel not in cur:
                errors.append('missing %s/%s' % (name, rel))
            elif rel not in want:
                # the kit may gain README files from the user; only changed bytes on known files are an error for it
                if name != 'kit':
                    errors.append('new file %s/%s' % (name, rel))
            elif cur[rel] != want[rel]:
                errors.append('changed %s/%s' % (name, rel))
    man = read_json(os.path.join(AUD, 'UPSTREAM_MANIFEST.json'))
    n = 0
    for tree, entries in man['trees'].items():
        have = set()
        for rel, want in entries.items():
            n += 1
            have.add(rel)
            p = os.path.join(ROOT, rel.replace('/', os.sep))
            if not os.path.exists(p):
                errors.append('missing ' + rel)
            elif sha256_file(p) != want:
                errors.append('changed ' + rel)
        root = UPSTREAM_DIRS[tree]
        prefix = os.path.relpath(root, ROOT).replace(os.sep, '/')
        for rel in walk_files(root):
            full = prefix + '/' + rel
            if full not in have:
                errors.append('new file ' + full)
    return {'n_upstream_checked': n, 'n_audit_checked': len(snap['trees']['semantic_audit']), 'n_kit_checked': len(snap['trees']['kit']), 'errors': errors[:50], 'n_errors': len(errors)}


if __name__ == '__main__':
    utf8_stdout()
    if sys.argv[1] == 'snapshot':
        snapshot()
    print(verify())
