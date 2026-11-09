"""R01 regression: PI-012 methodology (classification and protocol only)."""
import json
import os

from pi012 import R, obj_of, split_key
from rcommon import AUD, CANDIDATES, S2, baseline, input_path, norm_ws, out_path, read_json, read_jsonl, read_lines, rec_hash, sha256_file
from roverlay import apply_fields

# (group name, keys that must read the same under A2 rule 2: equal authority, equivalent form)
EQUIV = [('cache user responses: do-not-unless and only-when', ['FG-M-4afc784153', 'FG-M1-1629ce14d0', 'FG-L0-ff8742f01e', 'FG-L1-a0b4d693e7', 'FG-K0-345276aafe']),
         ('middleware folder only-when', ['FG-M-0948b1b484', 'FG-M1-6e2203908e', 'FG-K0-cb80dd47c6']),
         ('TS domain rules do-not-unless', ['FG-M-f8b45e3e07', 'FG-M1-5bb0673ebe', 'FG-K1-1342a3f3dd', 'FG-K1-d5854a89c3']),
         ('CI upgrades do-not-unless', ['FG-M-41b087b1e5', 'FG-M1-cbb81552d7', 'FG-L1-52a13bbaa7']),
         ('Redis backend only-when', ['FG-L1-7b96317821', 'FG-K0-3f43ebc15f', 'FG-L0-8fdc2119a4', 'FG-K1-f485f3c2e3']),
         ('client idempotency key do-not-unless', ['FG-M-da22ad2d6b', 'FG-M1-e9e298ac5a', 'FG-L1-d1986578bb']),
         ('Minimal API approval gate in both forms', ['FG-M1-16c4da8fc8', 'FG-K0-7ff05eb8e4', 'FG-K0-f4df90486e', 'FG-K1-a5f28f5d0f', 'FG-K1-f939605fbe']),
         ('preview SDK approval gate', ['FG-K0-8312cd07fb', 'FG-K1-5ce317181c'])]


def final_value(rows, key):
    return rows[key]['modality_after']


def pairs_hold(rows):
    bad = []
    for name, keys in EQUIV:
        vals = {final_value(rows, k) for k in keys}
        if len(vals) != 1:
            bad.append((name, {k: final_value(rows, k) for k in keys}))
    return bad


def run(ctx):
    r79 = read_jsonl(out_path('PI012_79_REVIEW.jsonl'))
    r230 = read_jsonl(out_path('PI012_230_REVIEW.jsonl'))
    ext = read_jsonl(out_path('PI012_EXTENSION_REVIEW.jsonl'))
    overlay = read_jsonl(out_path(R, 'OVERLAY.jsonl'))
    want79 = {r['key'] for r in read_jsonl(os.path.join(AUD, 'PI012_NEGATIVE_MODALITY_REVIEW.jsonl'))}
    want230 = {r['source_key'] for r in read_jsonl(os.path.join(AUD, 'A13_RESIDUAL_LEADS.jsonl'))}
    ctx.check('all 79 reviewed by stable key', {r['key'] for r in r79} == want79 and len(r79) == 79, kind='DATA', actual=len(r79))
    keys230 = {split_key(r['key'])[0] for r in r230}
    ctx.check('all 230 reviewed by stable key', keys230 == {split_key(k)[0] for k in want230} and len(r230) == 230, kind='DATA', actual=len(r230))
    all_rows = {r['key']: r for r in r79 + r230 + ext}
    ctx.check('dedup: 233 reviewed keys plus extension', len({r['key'] for r in r79 + r230}) == 233, kind='DATA', actual=len({r['key'] for r in r79 + r230}))
    bad = [r['key'] for r in all_rows.values() if r['result'] not in ('UPHOLD', 'CORRECT', 'UNRESOLVED') or not r['independent_reading'] or r['confidence'] not in ('HIGH', 'MEDIUM', 'LOW')]
    ctx.check('every row has result, reading, confidence', not bad, str(bad[:5]), kind='DATA')
    miss = []
    for r in all_rows.values():
        s = r['source']
        c = r['candidate']
        ls = read_lines(input_path(c, s['path'].split('/template/')[1]))
        if norm_ws(s['quote'])[:200] not in norm_ws(' '.join(ls[s['start_line'] - 1:s['end_line']])):
            miss.append(r['key'])
    ctx.check('every quote re-reads from the frozen input', not miss, str(miss[:5]), kind='DATA')
    b = pairs_hold(all_rows)
    ctx.check('equivalent forms under equal authority read the same', not b, str(b), kind='SEMANTIC')
    mut = {k: dict(v) for k, v in all_rows.items()}
    mut['FG-L1-a0b4d693e7']['modality_after'] = 'MUST_NOT'
    ctx.check('mutation: a wording-only split is caught', bool(pairs_hold(mut)), kind='MUTATION')
    ctx.check('approval gates stay binding', all(all_rows[k]['modality_after'] in ('MUST_NOT', 'REQUIRES_APPROVAL') for k in ('FG-K0-7ff05eb8e4', 'FG-K1-a5f28f5d0f', 'FG-L0-35fef36ce5')), kind='SEMANTIC')
    ctx.check('marked unconditional prohibition stays (A1.3 not widened)', all(all_rows[k]['modality_after'] in ('MUST_NOT', 'MUST') for k in ('FG-M-338112a109', 'FG-M1-05390af6dc', 'FG-L0-f5695d48af', 'FG-K1-7389afbe36')), kind='SEMANTIC')
    ctx.check('obligation-removing text is not a prohibition', all_rows['FG-M1-2a030a5f1e']['modality_after'] == 'NONE', kind='SEMANTIC')
    ctx.check('scan line stays open at R01 and is not forced', all_rows['FG-K0-0ef1e5ed3d']['result'] == 'UNRESOLVED', kind='SEMANTIC')
    per = read_jsonl(out_path('TEST_RESULTS', 'R01_per_record.jsonl'))
    ctx.check('per-record invariants ran for each accepted correction', len(per) == len(overlay) and all(p['status'] == 'PASS' for p in per), 'corrections=%d failed=%d' % (len(overlay), sum(1 for p in per if p['status'] != 'PASS')), kind='DATA')
    state1, state2 = {}, {}
    for st in (state1, state2):
        for c in CANDIDATES:
            st[c] = dict(baseline(c))
        for o in overlay:
            k, sub = split_key(o['key'])
            st[o['candidate']][k] = apply_fields(st[o['candidate']][k], o['set'], sub)
    ctx.check('overlay replay is deterministic', all(rec_hash(state1[c]) == rec_hash(state2[c]) for c in CANDIDATES), kind='DATA')
    touched = {split_key(o['key'])[0] for o in overlay}
    other = [k for c in CANDIDATES for k in baseline(c) if k not in touched and state1[c][k] != baseline(c)[k]]
    ctx.check('no record outside the overlay changed', not other, kind='DATA')
    freeze = read_json(os.path.join(S2, 'PROTOCOL_FREEZE.json'))
    txt = json.dumps(freeze)
    ctx.check('frozen protocol hash still recorded and matching', sha256_file(os.path.join(S2, 'CLASSIFICATION_PROTOCOL.md')) in txt, kind='FENCE')
    add = open(out_path('PROTOCOL_PI012_APPROVED_ADDENDUM.md'), encoding='utf-8').read()
    ctx.check('addendum is derived and quotes the decision', 'derived' in add.lower() and 'A2-PI012' in add and 'только' not in add and 'Логически эквивалентные' in add, kind='PROTOCOL')
    sens = open(out_path('PI012_SENSITIVITY.md'), encoding='utf-8').read()
    ctx.check('sensitivity reports bounds and options', 'Bounds, not a census' in sens and 'Option D' in sens and 'TRIGGERED' in sens, kind='PROTOCOL')
