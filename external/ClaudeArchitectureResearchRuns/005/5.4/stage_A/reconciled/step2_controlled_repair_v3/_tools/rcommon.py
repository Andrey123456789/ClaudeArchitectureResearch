"""Shared helpers for Step 2 v3 (Codex Pass 2+3 integration and post-v2 parity closure). Ported from the v2 tool of the same name.

Upstream trees, including v1 and v2, are read only. Every write goes through out_path(), which refuses a target outside
stage_A/reconciled/step2_controlled_repair_v3/. Writes are atomic (temp file in the same folder, then rename).
The template change history has three levels: v1 and v2 by reference in their own folders, then this run's log.
"""
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from functools import lru_cache

TOOLS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(TOOLS)
REC = os.path.dirname(OUT)
ROOT = os.path.abspath(os.path.join(REC, '..', '..'))
V1 = os.path.join(REC, 'step2_controlled_repair_v1')
V2 = os.path.join(REC, 'step2_controlled_repair_v2')
CODEX = os.path.join(ROOT, 'stage_A', 'codex_iterative_search')
S2 = os.path.join(REC, 'step2_classification')
AUD = os.path.join(REC, 'step2_semantic_audit_v1')
INPUTS = os.path.join(ROOT, 'inputs')
CANDS = os.path.join(OUT, 'candidates')
SCRATCH = os.path.join(OUT, '_scratch')
CANDIDATES = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
EXPECTED_RECORDS = {'M': 1003, 'M1': 1113, 'L0': 972, 'L1': 1037, 'K0': 1077, 'K1': 1200}
VERSION = 'step2-controlled-repair-v3'


def out_path(*p):
    target = os.path.abspath(os.path.join(OUT, *p))
    if not (target == OUT or target.startswith(OUT + os.sep)):
        raise SystemExit('write fence: refused %s' % target)
    return target


def v1_path(*p):
    return os.path.join(V1, *p)


def v2_path(*p):
    return os.path.join(V2, *p)


def run_start():
    """When this run (v3) started: the first preflight attempt, before any v3 output existed beyond the copied tools."""
    first = out_path('PREFLIGHT_HISTORY', 'attempt1_PREFLIGHT_RESULT.json')
    if os.path.exists(first):
        return read_json(first)['started']
    return read_json(out_path('PREFLIGHT_PROTECTED_MANIFEST.json'))['at']


def now():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def rec_hash(obj):
    return sha256_text(canon(obj))


def read_jsonl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def _atomic(p, writer):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.tmp-', dir=os.path.dirname(p))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            writer(f)
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return p


def write_jsonl(name, rows):
    def w(f):
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')
    return _atomic(out_path(name), w)


def append_jsonl(name, row):
    p = out_path(name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n')
        f.flush()
        os.fsync(f.fileno())


def write_json(name, obj):
    def w(f):
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    return _atomic(out_path(name), w)


def write_text(name, text):
    return _atomic(out_path(name), lambda f: f.write(text))


def read_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


@lru_cache(None)
def policies():
    inv = read_json(os.path.join(INPUTS, 'M', 'source', 'inventory.json'))
    out = {}
    for g in inv['policygroups']:
        for p in g['policies']:
            out[p['id']] = dict(p, group=g['id'], origin_file='inventory.json')
    shared = read_json(os.path.join(INPUTS, 'M', 'source', 'shared-research-invariants.json'))
    for p in shared['invariants']:
        out[p['id']] = dict(p, group='shared-research-invariants', origin_file='shared-research-invariants.json')
    assert len(out) == 196
    return out


@lru_cache(None)
def baseline(c):
    rows = read_jsonl(os.path.join(S2, 'per_candidate', c, 'CLASSIFICATIONS.jsonl'))
    return {r['source_key']: r for r in rows}


@lru_cache(None)
def effective(c):
    rows = read_jsonl(os.path.join(AUD, 'EFFECTIVE_CLASSIFICATIONS.jsonl'))
    return {r['source_key']: r for r in rows if r['candidate'] == c}


@lru_cache(None)
def coverage(c):
    rows = read_jsonl(os.path.join(S2, 'per_candidate', c, 'POLICY_COVERAGE.jsonl'))
    return {r['policy_id']: r for r in rows}


def all_change_rows():
    """Template change history at three levels, oldest first: the immutable v1 and v2 logs by reference, then this run's log."""
    return read_jsonl(v1_path('CHANGE_LOG.jsonl')) + read_jsonl(v2_path('CHANGE_LOG.jsonl')) + read_jsonl(out_path('CHANGE_LOG.jsonl'))


def template_root(c):
    return os.path.join(CANDS, c, 'template')


def input_template_root(c):
    return os.path.join(INPUTS, c, 'output', 'template')


def walk_files(root):
    out = []
    for d, sub, files in os.walk(root):
        sub.sort()
        for n in sorted(files):
            full = os.path.join(d, n)
            out.append(os.path.relpath(full, root).replace(os.sep, '/'))
    return out


def wc_path(c, rel):
    return os.path.join(template_root(c), rel.replace('/', os.sep))


def input_path(c, rel):
    return os.path.join(input_template_root(c), rel.replace('/', os.sep))


def read_lines(path):
    with open(path, encoding='utf-8', errors='replace', newline='') as f:
        return f.read().replace('\r\n', '\n').split('\n')


def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip()


def utf8_stdout():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
