"""Atomic change patches on the v3 working copies. Ported from v2.

A change's patches live in _rules/<CHANGE>/patches.py as PATCHES = [(candidate, rel_path, old, new), ...].
apply: refuses unless every earlier v3 change has a PASS checkpoint; validates every `old` matches exactly once before writing
anything; snapshots each touched file to _rules/<CHANGE>/before/; writes atomically; appends one CHANGE_LOG row per file.
rollback: restores the snapshot and logs it.
Line endings are detected per file: patch text uses LF and is converted to the file's convention.
"""
import importlib.util
import os
import shutil
import sys

from order import V3_ORDER
from rcommon import CANDIDATES, OUT, append_jsonl, now, out_path, read_json, sha256_file, utf8_stdout, wc_path, write_json


def load_patches(rule):
    p = out_path('_rules', rule, 'patches.py')
    spec = importlib.util.spec_from_file_location('patches_' + rule.replace('-', '_'), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def prev_rule_ok(rule):
    i = V3_ORDER.index(rule)
    for r in V3_ORDER[:i]:
        cp = out_path('CHECKPOINTS', r + '.checkpoint.json')
        if not os.path.exists(cp) or read_json(cp).get('gate') not in ('PASS', 'PASS_WITH_DOCUMENTED_NOT_RUN'):
            return r
    return None


def eol_of(data):
    return '\r\n' if '\r\n' in data else '\n'


def apply(rule, dry=False):
    blocker = prev_rule_ok(rule)
    if blocker:
        raise SystemExit('refused: %s has no PASS checkpoint, so %s may not start' % (blocker, rule))
    mod = load_patches(rule)
    files = {}
    for c, rel, old, new in mod.PATCHES:
        assert c in CANDIDATES, c
        k = (c, rel)
        if k not in files:
            with open(wc_path(c, rel), encoding='utf-8', newline='') as f:
                files[k] = f.read()
        data = files[k]
        eol = eol_of(data)
        o, n = old.replace('\n', eol), new.replace('\n', eol)
        count = data.count(o)
        if count != 1:
            raise SystemExit('patch does not match exactly once (%d): %s %s\n--- %s' % (count, c, rel, old[:300]))
        files[k] = data.replace(o, n)
    if dry:
        print('dry run ok: %d patches on %d files' % (len(mod.PATCHES), len(files)))
        return
    before = {}
    for (c, rel) in files:
        src = wc_path(c, rel)
        before[(c, rel)] = sha256_file(src)
        snap = out_path('_rules', rule, 'before', c, *rel.split('/'))
        os.makedirs(os.path.dirname(snap), exist_ok=True)
        if not os.path.exists(snap):
            shutil.copyfile(src, snap)
    for (c, rel), data in files.items():
        dst = wc_path(c, rel)
        tmp = dst + '.tmp-patch'
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            f.write(data)
        os.replace(tmp, dst)
    for (c, rel) in files:
        append_jsonl('CHANGE_LOG.jsonl', {'at': now(), 'rule': rule, 'candidate': c, 'file': rel, 'action': 'PATCH', 'before_sha256': before[(c, rel)], 'after_sha256': sha256_file(wc_path(c, rel)),
                                          'affected_policies': getattr(mod, 'POLICIES', []), 'reason': getattr(mod, 'REASON', ''), 'source_evidence': getattr(mod, 'EVIDENCE', None), 'kind': 'TEMPLATE'})
    print('applied %d patches on %d files' % (len(mod.PATCHES), len(files)))


def rollback(rule, why):
    root = out_path('_rules', rule, 'before')
    n = 0
    for d, _, fs in os.walk(root):
        for name in fs:
            snap = os.path.join(d, name)
            parts = os.path.relpath(snap, root).split(os.sep)
            c, rel = parts[0], '/'.join(parts[1:])
            dst = wc_path(c, rel)
            b = sha256_file(dst)
            shutil.copyfile(snap, dst)
            append_jsonl('CHANGE_LOG.jsonl', {'at': now(), 'rule': rule, 'candidate': c, 'file': rel, 'action': 'ROLLBACK', 'before_sha256': b, 'after_sha256': sha256_file(dst), 'reason': why, 'kind': 'TEMPLATE'})
            n += 1
    shutil.rmtree(root)
    print('rolled back %d files' % n)


if __name__ == '__main__':
    utf8_stdout()
    cmd, rule = sys.argv[1], sys.argv[2]
    if cmd == 'apply':
        apply(rule)
    elif cmd == 'dry':
        apply(rule, dry=True)
    elif cmd == 'rollback':
        rollback(rule, ' '.join(sys.argv[3:]) or 'rollback')
