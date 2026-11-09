"""Shared helpers for the Step 2 semantic audit (v1).

Everything here reads upstream files only. All writes go through out_path(), which refuses a target
outside stage_A/reconciled/step2_semantic_audit_v1/.
"""
import hashlib
import json
import os
import re
import sys
from functools import lru_cache

TOOLS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(TOOLS)
REC = os.path.dirname(OUT)
ROOT = os.path.abspath(os.path.join(REC, '..', '..'))
S2 = os.path.join(REC, 'step2_classification')
S1 = os.path.join(REC, 'step1_union')
P1 = os.path.join(REC, 'step1_union_augmented_pass1')
INPUTS = os.path.join(ROOT, 'inputs')
DEC = os.path.join(OUT, '_decisions')
CANDIDATES = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
EXPECTED_RECORDS = {'M': 1003, 'M1': 1113, 'L0': 972, 'L1': 1037, 'K0': 1077, 'K1': 1200}
AUDIT_VERSION = 'step2-semantic-audit-v1'


def out_path(*p):
    target = os.path.abspath(os.path.join(OUT, *p))
    if not (target == OUT or target.startswith(OUT + os.sep)):
        raise SystemExit('write fence: refused %s' % target)
    return target


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
    with open(p, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def write_jsonl(name, rows):
    p = out_path(name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')
    os.replace(tmp, p)
    return p


def write_json(name, obj):
    p = out_path(name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    os.replace(tmp, p)
    return p


def write_text(name, text):
    p = out_path(name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    os.replace(tmp, p)
    return p


@lru_cache(None)
def policies():
    inv = json.load(open(os.path.join(INPUTS, 'M', 'source', 'inventory.json'), encoding='utf-8'))
    out = {}
    for g in inv['policygroups']:
        for p in g['policies']:
            out[p['id']] = dict(p, group=g['id'], origin_file='inventory.json')
    shared = json.load(open(os.path.join(INPUTS, 'M', 'source', 'shared-research-invariants.json'), encoding='utf-8'))
    for p in shared['invariants']:
        out[p['id']] = dict(p, group='shared-research-invariants', origin_file='shared-research-invariants.json')
    assert len(out) == 196
    return out


@lru_cache(None)
def baseline(c):
    rows = read_jsonl(os.path.join(S2, 'per_candidate', c, 'CLASSIFICATIONS.jsonl'))
    return {r['source_key']: r for r in rows}


@lru_cache(None)
def coverage(c):
    rows = read_jsonl(os.path.join(S2, 'per_candidate', c, 'POLICY_COVERAGE.jsonl'))
    return {r['policy_id']: r for r in rows}


def all_baseline():
    d = {}
    for c in CANDIDATES:
        d.update(baseline(c))
    return d


def cand_of(key):
    m = re.match(r'^FG-([A-Z0-9]+)-', key)
    if m:
        return m.group(1)
    for c in CANDIDATES:
        if key in baseline(c):
            return c
    raise KeyError(key)


@lru_cache(None)
def file_lines_abs(rel):
    """rel is repo-root relative, for example inputs/K1/output/template/CLAUDE.md"""
    with open(os.path.join(ROOT, rel.replace('/', os.sep)), encoding='utf-8', errors='replace', newline='') as f:
        text = f.read()
    return text.replace('\r\n', '\n').split('\n')


def source_range(rel, a, b):
    ls = file_lines_abs(rel)
    return '\n'.join(ls[a - 1:b])


def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip()


def quote_in_source(rel, a, b, quote):
    """True when the quote, whitespace-normalized, is within the stated lines of the immutable file."""
    return norm_ws(quote) in norm_ws(source_range(rel, a, b))


def policy_text(pid):
    p = policies()[pid]
    return {'policy_id': pid, 'name': p['name'], 'normative_strength': p['normative_strength'], 'trigger_class': p['trigger_class'],
            'normalized_policy': p['normalized_policy'], 'origin_file': p['origin_file']}


def utf8_stdout():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
