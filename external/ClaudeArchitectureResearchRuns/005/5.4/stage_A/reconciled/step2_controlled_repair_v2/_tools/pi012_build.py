"""Compile R01 decisions into the review files and the modality overlay, running whole-dataset invariants after each accepted correction."""
import copy
import os
import re
import sys
from collections import Counter

from pi012 import R, cand_of, locate, obj_of, role, split_key
from pi012_compare import load_blind
from rcommon import AUD, CANDIDATES, baseline, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, utf8_stdout, write_json, write_jsonl, write_text
from roverlay import STRENGTH_RANK, apply_fields, target_of, validate_candidate

CLASS = {'MUST': 3, 'MUST_NOT': 3, 'DECIDED': 3, 'REQUIRES_APPROVAL': 3, 'DEFAULT': 2, 'SHOULD': 2, 'SHOULD_NOT': 2, 'MAY': 1, 'NONE': 0, 'MIXED': -1}
SECURITY_SENSITIVE = {'FG-M-4afc784153', 'FG-M1-1629ce14d0', 'FG-L0-ff8742f01e', 'FG-L1-a0b4d693e7', 'FG-K0-345276aafe', 'FG-K0-0cf8d7ed7b', 'FG-K1-c7d26b5b93'}
AUDIT_NN = {'FG-M1-2a030a5f1e'}


def load_final():
    rows = {}
    p = out_path(R, 'final.dec')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if line.strip():
                k, m, note = [x.strip() for x in line.rstrip('\n').split('|', 2)]
                rows[k] = {'modality': m, 'note': note}
    return rows


def form_of(reading):
    t = reading.lower()
    for tag, rx in (('APPROVAL_GATE', r'approval gate'), ('BY_REFERENCE', r'check-by-reference|by reference|by name|names its owners|points to'), ('EXCEPTION_DENIED', r'denies an exception'), ('TRIGGERED', r'class triggered|triggered prohibition'),
                    ('EXPLICIT_DEFAULT', r'by default|by-default'), ('PERMISSION_CONDITION', r'only-when|do-not-unless|do-not-without|only when|permission-granting'), ('LABEL', r'label "not retried'), ('CHARACTERIZATION', r'characterization|evaluative|avoid'),
                    ('ELLIPTICAL', r'elliptical'), ('OBLIGATION_REMOVED', r'removes an obligation'), ('MARKED', r'marked|marker|explicit "'), ('NEG_DECLARATIVE', r'declarative|contrastive'), ('POSITIVE_IMPERATIVE', r'imperative')):
        if re.search(rx, t):
            return tag
    return 'OTHER'


def strength_fields(rec, obj, new):
    """Derived A1.2 fields after a modality change, read against the first cited policy."""
    cov = obj.get('canonical_coverage') or []
    out = {'modality': new}
    if not cov or obj.get('classification') not in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA', 'MIXED'):
        return out
    first = policies()[cov[0]['policy_id']]['normative_strength']
    a, b = STRENGTH_RANK.get(new), STRENGTH_RANK.get(first)
    code = obj.get('strength_resolution_code')
    if a is None or b is None:
        return out
    if a == b:
        out['strength_vs_canonical'] = 'SAME'
        mism = [c for c in cov if STRENGTH_RANK.get(policies()[c['policy_id']]['normative_strength']) != a]
        out['strength_resolution_code'] = 'SL' if mism else (code if code in ('PC', 'SL') else None)
    elif a < b:
        out['strength_vs_canonical'] = 'WEAKER'
        out['strength_resolution_code'] = code if code in ('CK', 'CR', 'AM', 'GR', 'CN', 'PM') else 'GR'
    else:
        out['strength_vs_canonical'] = 'STRONGER'
    return out


def main():
    utf8_stdout()
    cases = read_json(out_path(R, 'CASES.json'))['cases']
    blind = load_blind()
    final = load_final()
    ext = load_blind('extension.dec')
    audit = {r['key']: r for r in read_jsonl(os.path.join(AUD, 'PI012_NEGATIVE_MODALITY_REVIEW.jsonl'))}
    rows79, rows230, ext_rows, overlay = [], [], [], []
    state = {c: dict(baseline(c)) for c in CANDIDATES}
    per = []
    all_cases = [(c['key'], c.get('lists', []), blind[c['key']], c) for c in cases] + [(k, ['EXT'], v, {'closest': None}) for k, v in sorted(ext.items())]
    tally = Counter()
    for key, lists, b, c0 in all_cases:
        rec, obj = obj_of(key)
        c = rec['candidate']
        base_key, sub = split_key(key)
        before = obj.get('modality')
        fin = final.get(key)
        after = (fin or b)['modality']
        if after == 'UNRESOLVED':
            result = 'UNRESOLVED'
        elif CLASS.get(after) == CLASS.get(before):
            result = 'UPHOLD'
        else:
            result = 'CORRECT'
        ref, ls = locate(rec, c0.get('closest') or c0.get('closest_230') or (obj.get('claim_text') or ''))
        quote = norm_ws(' '.join(ls[ref['start_line'] - 1:ref['end_line']]))
        a = audit.get(key)
        row = {'key': key, 'candidate': c, 'lists': sorted(set(lists)), 'source': {'path': ref['path'], 'start_line': ref['start_line'], 'end_line': ref['end_line'], 'quote': quote[:600], 'verified_by': 'mechanical re-read of the frozen input'},
               'claim': (obj.get('claim_text') or rec.get('claim_text') or '')[:400], 'source_role': role(ref['path']), 'form': form_of(b['reading']), 'canonical_policies': [{'id': p, 'strength': policies()[p]['normative_strength']} for p in obj.get('canonical_policy_ids') or []],
               'independent_reading': b['reading'], 'alternative_or_counterexample': b['counterexample'], 'blind_modality': b['modality'], 'modality_before': before, 'modality_after': before if result in ('UPHOLD', 'UNRESOLVED') else after, 'token_note': ('Same force class; stored token kept (%s, read %s)' % (before, after)) if result == 'UPHOLD' and before != after else None,
               'result': result, 'confidence': b['confidence'], 'post_reveal_note': fin['note'] if fin else None, 'audit_outcome': a['outcome'] if a else None, 'audit_modality': a['modality_suggested'] if a else None, 'agrees_with_audit': (a['modality_suggested'] == after) if a else None,
               'security_sensitive': base_key in SECURITY_SENSITIVE, 'addendum': 'A2-PI012'}
        tally[(tuple(row['lists']), result)] += 1
        if 'N79' in lists:
            rows79.append(row)
        if 'L230' in lists:
            rows230.append(row)
        if lists == ['EXT']:
            ext_rows.append(row)
        if result == 'CORRECT':
            if base_key in AUDIT_NN:
                fields = {'classification': 'NON_NORMATIVE', 'normativity': 'NON_NORMATIVE', 'domain': 'NON_NORMATIVE', 'oracle_relation': 'NOT_APPLICABLE', 'canonical_coverage': [], 'modality': 'NONE', 'strength_vs_canonical': 'N/A', 'strength_resolution_code': None}
            else:
                fields = strength_fields(rec, obj, after)
            cur = state[c][base_key]
            new = apply_fields(cur, fields, sub)
            state[c][base_key] = new
            errs = validate_candidate(c, state[c])
            per.append({'key': key, 'candidate': c, 'fields': fields, 'before_sha256': rec_hash(cur), 'after_sha256': rec_hash(new), 'invariant_errors': errs, 'status': 'PASS' if not errs else 'FAIL'})
            overlay.append({'key': key, 'candidate': c, 'set': fields, 'rule': 'R01-HQ06-PI012', 'basis': 'A2-PI012', 'reading': b['reading'], 'lists': sorted(set(lists))})
    write_jsonl('PI012_79_REVIEW.jsonl', rows79)
    write_jsonl('PI012_230_REVIEW.jsonl', rows230)
    write_jsonl('PI012_EXTENSION_REVIEW.jsonl', ext_rows)
    write_jsonl(os.path.join(R, 'OVERLAY.jsonl'), overlay)
    write_jsonl(os.path.join('TEST_RESULTS', 'R01_per_record.jsonl'), per)
    print('79:', len(rows79), Counter(r['result'] for r in rows79), '| 230:', len(rows230), Counter(r['result'] for r in rows230), '| ext:', len(ext_rows), Counter(r['result'] for r in ext_rows))
    print('corrections', len(overlay), 'invariant failures', sum(1 for p in per if p['status'] != 'PASS'))
    print('audit agreement on 79:', Counter(r['agrees_with_audit'] for r in rows79))
    bad = [p for p in per if p['status'] != 'PASS'][:5]
    for b in bad:
        print(b['key'], b['invariant_errors'][:3])
    return 0


if __name__ == '__main__':
    sys.exit(main())
