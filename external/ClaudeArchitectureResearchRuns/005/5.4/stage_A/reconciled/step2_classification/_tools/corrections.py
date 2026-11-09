"""Traceable correction overlay (Addendum A1). Checkpointed batch files are never modified.

  python -B corrections.py <C>      compile _decisions/<C>/CORRECTIONS.dec into
                                    per_candidate/<C>/CORRECTIONS.jsonl (ledger with full before record and field diff) and
                                    per_candidate/<C>/CORRECTED_RECORDS.jsonl (after records, read by candidate.py assemble)

Block format (several blocks per key are applied in file order):

  @ COR-<C>-0001 <source_key> <finding_ref> | reason
    set t: trigger text           (t e sc x s r om fhd ce : continuation fields; empty value clears)
    set m: D                      (m d o c k st fa cf rel sr : DSL keys; empty value clears)
    set pols: DEP-006~ WF-005     (replaces the canonical policy tokens; empty value clears)
    set note: rationale text
    = <CODE> [tokens] | note      (replaces the whole decision; DSL continuation and "- " subclause lines follow)
    recheck: what was re-verified against the source after the change
"""
import copy
import json
import os
import re
import sys
import time

from build import (parse_dec, parse_dec_lines, parse_tokens, build_record, by_key, load_plan, DecErr)
from common import OUT, POLICY_RE, policies, write_jsonl_atomic, write_json_atomic, sha256_file, sha256_text

HEAD_RE = re.compile(r'^@\s+(COR-\S+)\s+(\S+)\s+(\S+)\s*\|\s*(.+)$')
SET_RE = re.compile(r'^\s+set\s+([a-z]+):\s?(.*)$')
CONT_KEYS = {'t', 'e', 'sc', 'x', 's', 'r', 'om', 'fhd', 'ce', 'ev'}
KV_KEYS = {'m', 'd', 'o', 'c', 'k', 'st', 'fa', 'cf', 'rel', 'sr'}
CODE_KEYS = {'CO', 'CD', 'XP', 'XW', 'IA', 'NN', 'MX', 'UN'}
VOLATILE = {'decision_src', 'correction_history'}


def locate(cand):
    plan = load_plan(cand)
    where = {}
    for b in plan['batches']:
        for i, rec in enumerate(b['records'], 1):
            where[rec['source_key']] = (b['batch_id'], i)
    return where


def parse_blocks(path):
    blocks, cur = [], None
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    for ln, raw in enumerate(lines, 1):
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        m = HEAD_RE.match(raw)
        if m:
            cur = {'id': m.group(1), 'key': m.group(2), 'finding': m.group(3), 'reason': m.group(4).strip(),
                   'sets': [], 'replace': [], 'recheck': None, 'line': ln}
            blocks.append(cur)
            continue
        if cur is None:
            raise DecErr('%s:%d: content before first @ block' % (os.path.basename(path), ln))
        s = raw.strip()
        if s.startswith('= ') and not cur['replace']:
            cur['replace'].append('1 ' + s[2:])
        elif cur['replace'] and (s.startswith('- ') or re.match(r'^(x|s|t|e|sc|r|om|fhd|ce|ev):', s)):
            cur['replace'].append(raw)
        elif s.startswith('recheck:'):
            cur['recheck'] = s[len('recheck:'):].strip()
        else:
            m = SET_RE.match(raw)
            if not m:
                raise DecErr('%s:%d: unparseable correction line %r' % (os.path.basename(path), ln, raw[:80]))
            cur['sets'].append((m.group(1), m.group(2).strip(), ln))
    return blocks


def apply_sets(dec, sets, where):
    d = copy.deepcopy(dec)
    for key, val, ln in sets:
        if key in CONT_KEYS:
            if val:
                d['cont'][key] = val
            else:
                d['cont'].pop(key, None)
        elif key in KV_KEYS:
            if val:
                d['kv'][key] = val
            else:
                d['kv'].pop(key, None)
        elif key == 'pols':
            tok = parse_tokens(val, '%s:%d' % (where, ln))
            d['pols'], d['partial'] = tok['pols'], tok['partial']
        elif key == 'note':
            d['note'] = val
        elif key == 'code':
            if val not in CODE_KEYS:
                raise DecErr('%s:%d: bad code %s' % (where, ln, val))
            d['code'] = val
        else:
            raise DecErr('%s:%d: unknown set key %s' % (where, ln, key))
    return d


def diff(before, after):
    out = {}
    for k in sorted(set(before) | set(after)):
        if k in VOLATILE:
            continue
        if before.get(k) != after.get(k):
            out[k] = {'before': before.get(k), 'after': after.get(k)}
    return out


def rec_sha(r):
    return sha256_text(json.dumps({k: v for k, v in r.items() if k not in VOLATILE}, ensure_ascii=False, sort_keys=True))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    cand = sys.argv[1]
    path = os.path.join(OUT, '_decisions', cand, 'CORRECTIONS.dec')
    label = cand + '/CORRECTIONS.dec'
    blocks = parse_blocks(path)
    where, bk = locate(cand), by_key()
    ids = [b['id'] for b in blocks]
    if len(ids) != len(set(ids)):
        raise DecErr('duplicate correction ids')
    state, decisions, ledger = {}, {}, []
    batches = {}
    for b in blocks:
        key = b['key']
        if key not in where:
            raise DecErr('%s: %s is not a %s source key' % (b['id'], key, cand))
        if key not in state:
            bid, idx = where[key]
            if bid not in batches:
                batches[bid] = (parse_dec(os.path.join(OUT, '_decisions', cand, bid + '.dec')),
                                {r['source_key']: r for r in map(json.loads, open(
                                    os.path.join(OUT, 'per_candidate', cand, 'batches', bid + '.jsonl'), encoding='utf-8'))})
            decisions[key] = batches[bid][0][idx]
            state[key] = batches[bid][1][key]
        before = state[key]
        if b['replace']:
            newdec = parse_dec_lines(b['replace'], label, b['line'])[1]
            newdec = apply_sets(newdec, b['sets'], label)
        else:
            newdec = apply_sets(decisions[key], b['sets'], label)
        after = build_record(bk[key], newdec, before['batch_id'], '%s:%d' % (label, b['line']))
        changes = diff(before, after)
        if not changes:
            raise DecErr('%s: correction changes nothing' % b['id'])
        hist = list(before.get('correction_history') or [])
        hist.append({'correction_id': b['id'], 'finding_ref': b['finding'], 'classification_before': before['classification'],
                     'classification_after': after['classification']})
        after['correction_history'] = hist
        ledger.append({
            'protocol_version': after['protocol_version'], 'addendum': 'A1', 'candidate': cand,
            'correction_id': b['id'], 'source_key': key, 'finding_ref': b['finding'], 'reason': b['reason'],
            'recheck': b['recheck'], 'fields_changed': changes,
            'classification_before': before['classification'], 'classification_after': after['classification'],
            'before_record_sha256': rec_sha(before), 'after_record_sha256': rec_sha(after),
            'before_record': before, 'batch_id': before['batch_id'], 'correction_src': '%s:%d' % (label, b['line'])})
        state[key], decisions[key] = after, newdec
    write_jsonl_atomic(os.path.join(OUT, 'per_candidate', cand, 'CORRECTIONS.jsonl'), ledger)
    write_jsonl_atomic(os.path.join(OUT, 'per_candidate', cand, 'CORRECTED_RECORDS.jsonl'), list(state.values()))
    write_json_atomic(os.path.join(OUT, 'CHECKPOINTS', cand, 'CORRECTIONS.checkpoint.json'), {
        'candidate': cand, 'addendum': 'A1', 'n_corrections': len(ledger), 'n_records_corrected': len(state),
        'corrections_dec_sha256': sha256_file(path),
        'ledger_sha256': sha256_file(os.path.join(OUT, 'per_candidate', cand, 'CORRECTIONS.jsonl')),
        'corrected_records_sha256': sha256_file(os.path.join(OUT, 'per_candidate', cand, 'CORRECTED_RECORDS.jsonl')),
        'at': time.strftime('%Y-%m-%dT%H:%M:%S')})
    moved = [(l['source_key'], l['classification_before'], l['classification_after']) for l in ledger if l['classification_before'] != l['classification_after']]
    print('%s: %d corrections on %d records; classification changes: %d' % (cand, len(ledger), len(state), len(moved)))
    for m in moved:
        print('  ', *m)


if __name__ == '__main__':
    try:
        main()
    except DecErr as e:
        print('ERROR:', e)
        sys.exit(1)
