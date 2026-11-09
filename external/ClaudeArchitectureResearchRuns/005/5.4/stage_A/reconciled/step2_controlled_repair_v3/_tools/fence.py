"""Immutable-input fence for v3. Ported from v2.

The snapshot is PREFLIGHT_PROTECTED_MANIFEST.json, taken by preflight_v3.py before any v3 work. verify() re-hashes the same trees and files.
Fenced: inputs, primary, replica, independent, _control, the kit, Step 1, the Pass 1 augmented union, Step 2, the semantic audit, v1, v2,
their archives, the root decision files and the Codex area (read-only for v3; PASSES/pass_0004 and later are pruned before entry).
A kit file the user adds later is tolerated; a changed or removed known kit file is an error. Any other changed, missing or new file is an error.
A file absent at preflight (the v1 archive, PRE-W01) must stay absent.
A protected file removed later outside this run (EXTERNAL_EVENTS.json, ENV-01: the v2 archive) may stay absent only while the tree it
archives has no fence error; it is reported as a warning. If it reappears it must have its preflight bytes.
"""
import os
import sys

import external_events
from preflight_v3 import PROTECTED_FILES, PROTECTED_TREES, CODEX as CODEX_ROOT, codex_prune, hash_tree
from rcommon import AUD, OUT, ROOT, read_json, sha256_file, utf8_stdout

SNAPSHOT = 'PREFLIGHT_PROTECTED_MANIFEST.json'


def verify():
    errors = []
    snap = read_json(os.path.join(OUT, SNAPSHOT))
    counts = {}
    trees = dict(PROTECTED_TREES, codex_iterative_search=CODEX_ROOT)
    for name, root in trees.items():
        cur = hash_tree(root, codex_prune if name == 'codex_iterative_search' else None)
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
    # A protected file removed outside this run (EXTERNAL_EVENTS.json) may stay absent only while the tree it archives is clean.
    events = external_events.load()
    warnings = []
    for name, p in PROTECTED_FILES.items():
        now_h = sha256_file(p) if os.path.exists(p) else None
        rec = [e for e in events['removed'] if e['name'] == name]
        tree_errors = [e for e in errors if rec and (' %s/' % rec[0]['archived_tree']) in e]
        err = external_events.protected_file_error(name, now_h, snap['files'][name], tree_errors, events)
        if err:
            errors.append(err)
        elif now_h != snap['files'][name]:
            warnings.append('%s %s absent (recorded external removal; %s verified unchanged)' % (rec[0]['id'], name, rec[0]['archived_tree']))
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
    return {'n_upstream_checked': n, 'n_by_tree': counts, 'errors': errors[:50], 'n_errors': len(errors), 'warnings': warnings}


if __name__ == '__main__':
    utf8_stdout()
    print(verify())
