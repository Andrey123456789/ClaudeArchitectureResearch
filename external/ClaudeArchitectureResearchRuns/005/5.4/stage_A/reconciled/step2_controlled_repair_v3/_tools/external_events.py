"""External events: changes outside this run's root that no v3 tool made, recorded so the fence and the R27 newer-file walk stay strict.

Detected at the V3-D02-MODALITY86 gate, attempt 1 (2026-11-06): after the v3 run started, outside this session,
  ENV-01  stage_A/reconciled/step2_controlled_repair_v2.zip (a protected convenience archive, hashed at preflight) is gone;
  ENV-02  stage_A/reconciled/step2_controlled_repair_v3.zip appeared (the user's archive of this run folder, made for an interim review);
  ENV-03  Stage_A_Step2_V3_Independent_Interim_Review_EN.md appeared at the repository root (the user's independent interim review).
No v3 tool writes an archive (R27 checks that) or writes outside the run root.

What is tolerated, and nothing more:
  - a protected file recorded as REMOVED may stay absent only if its preflight hash is the recorded one and the tree it archives has no
    fence error (the same rule as PRE-W01 for the v1 archive); if it reappears it must have its preflight bytes;
  - a recorded ADDED file may be newer than the run start only while its bytes equal the recorded hash.
Any other new, changed or missing file still fails. selftest() proves those negatives on synthetic inputs and runs inside R27 section A.

Usage: PYTHONPATH=_tools python -B _tools/external_events.py record   (writes EXTERNAL_EVENTS.json once; refuses to overwrite)
       PYTHONPATH=_tools python -B _tools/external_events.py selftest
"""
import json
import os
import sys
from datetime import datetime

from rcommon import OUT, ROOT, read_json, sha256_file, utf8_stdout

FILE = os.path.join(OUT, 'EXTERNAL_EVENTS.json')
REMOVED = [('ENV-01', 'v2_archive', 'stage_A/reconciled/step2_controlled_repair_v2.zip', 'step2_controlled_repair_v2',
            'Protected v2 convenience archive no longer present. The v2 tree it archives is fenced file by file and verified unchanged.')]
ADDED = [('ENV-02', 'stage_A/reconciled/step2_controlled_repair_v3.zip', 'Archive of this run folder made by the user outside this session for an independent interim review. Not written by any v3 tool.'),
         ('ENV-03', 'Stage_A_Step2_V3_Independent_Interim_Review_EN.md', 'Independent interim review written by the user outside this session. Read as data; the user\'s chat message is the instruction.')]


def load():
    if not os.path.exists(FILE):
        return {'removed': [], 'added': []}
    return read_json(FILE)


def record():
    if os.path.exists(FILE):
        sys.exit('EXTERNAL_EVENTS.json exists; events are recorded once')
    snap = read_json(os.path.join(OUT, 'PREFLIGHT_PROTECTED_MANIFEST.json'))
    ev = {'recorded_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 'detected_at': 'V3-D02-MODALITY86 gate, attempt 1 (GATE_ATTEMPTS/V3-D02-MODALITY86.attempt1.log)', 'removed': [], 'added': []}
    for eid, name, rel, tree, note in REMOVED:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        assert not os.path.exists(p), rel
        ev['removed'].append({'id': eid, 'name': name, 'path': rel, 'preflight_sha256': snap['files'][name], 'archived_tree': tree, 'note': note})
    for eid, rel, note in ADDED:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        st = os.stat(p)
        ev['added'].append({'id': eid, 'path': rel, 'sha256': sha256_file(p), 'bytes': st.st_size, 'mtime': datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%dT%H:%M:%S'), 'note': note})
    with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(ev, f, indent=1, ensure_ascii=False)
        f.write('\n')
    print(json.dumps(ev, indent=1))


def protected_file_error(name, now_h, snap_h, tree_errors, events):
    """None when acceptable, else the fence error text. tree_errors: fence errors of the archived tree."""
    if now_h == snap_h:
        return None
    rec = [e for e in events['removed'] if e['name'] == name]
    if now_h is None and rec and rec[0]['preflight_sha256'] == snap_h:
        if tree_errors:
            return 'removed %s and its archived tree %s has errors' % (name, rec[0]['archived_tree'])
        return None
    return 'changed, missing or reappeared %s' % name


def newer_not_allowed(newer_rel, hash_of, events):
    """The newer files outside the run root that are not recorded ADDED files with their recorded bytes."""
    allowed = {e['path']: e['sha256'] for e in events['added']}
    out = []
    for rel in newer_rel:
        key = rel.replace(os.sep, '/')
        if key in allowed and hash_of(rel) == allowed[key]:
            continue
        out.append(rel)
    return out


def selftest():
    """Negative and positive cases on synthetic inputs. Returns a list of (name, ok)."""
    ev = {'removed': [{'name': 'v2_archive', 'preflight_sha256': 'H0', 'archived_tree': 'v2'}], 'added': [{'path': 'a/x.zip', 'sha256': 'HX'}]}
    hashes = {'a/x.zip': 'HX', 'a/y.md': 'HY'}
    rows = [
        ('unchanged protected file passes', protected_file_error('v1_archive', 'H1', 'H1', [], ev) is None),
        ('a recorded removal passes when its tree is clean', protected_file_error('v2_archive', None, 'H0', [], ev) is None),
        ('negative: a recorded removal fails when its tree has errors', protected_file_error('v2_archive', None, 'H0', ['changed step2_controlled_repair_v2/x'], ev) is not None),
        ('negative: the removed file reappearing with other bytes fails', protected_file_error('v2_archive', 'H9', 'H0', [], ev) is not None),
        ('negative: a removal with a different preflight hash fails', protected_file_error('v2_archive', None, 'H7', [], ev) is not None),
        ('negative: an unrecorded missing protected file fails', protected_file_error('v1_archive_other', None, 'H5', [], ev) is not None),
        ('negative: a changed protected file fails', protected_file_error('post_v2_decisions', 'H2', 'H3', [], ev) is not None),
        ('a recorded added file with its bytes is tolerated', newer_not_allowed(['a/x.zip'], hashes.get, ev) == []),
        ('negative: an unrecorded newer file fails', newer_not_allowed(['a/y.md'], hashes.get, ev) == ['a/y.md']),
        ('negative: a recorded added file whose bytes changed fails', newer_not_allowed(['a/x.zip'], {'a/x.zip': 'HZ'}.get, ev) == ['a/x.zip']),
    ]
    return rows


if __name__ == '__main__':
    utf8_stdout()
    if len(sys.argv) > 1 and sys.argv[1] == 'record':
        record()
    else:
        rows = selftest()
        for n, ok in rows:
            print('PASS' if ok else 'FAIL', n)
        sys.exit(0 if all(ok for _, ok in rows) else 1)
