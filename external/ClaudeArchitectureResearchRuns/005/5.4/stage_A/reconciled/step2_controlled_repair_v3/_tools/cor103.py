"""R25: adjudicates all 103 audit corrections against the original quote and the current working copy, and writes CORRECTION_103_ADJUDICATION.jsonl plus the accepted overlay."""
import importlib.util
import os
import sys
from collections import Counter

from rcommon import AUD, CANDIDATES, input_path, norm_ws, out_path, read_jsonl, read_lines, utf8_stdout, wc_path, write_jsonl
from witness import norm_stream

STRIP = ('confidence',)


def load_decisions():
    p = out_path('_rules', 'R25-COR103', 'decisions.py')
    spec = importlib.util.spec_from_file_location('r25d', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def r01_readings():
    rows = {}
    for f in ('PI012_79_REVIEW.jsonl', 'PI012_230_REVIEW.jsonl', 'PI012_EXTENSION_REVIEW.jsonl'):
        for r in read_jsonl(out_path(f)):
            rows[r['key']] = r
    return rows


def current_status(c, q):
    rel = q['path'].split('/template/')[1]
    orig = norm_ws(' '.join(read_lines(input_path(c, rel))[q['start_line'] - 1:q['end_line']]))
    ok_orig = norm_ws(q['quote']) in orig or norm_ws(q['quote'])[:80] in orig
    p = wc_path(c, rel)
    if not os.path.exists(p):
        return ok_orig, {'status': 'REMOVED'}
    ls = read_lines(p)
    if norm_ws(q['quote']) in norm_ws(' '.join(ls[q['start_line'] - 1:q['end_line']])):
        return ok_orig, {'status': 'SAME', 'path': rel, 'start_line': q['start_line'], 'end_line': q['end_line']}
    text, idx = norm_stream(ls)
    i = text.find(norm_ws(q['quote']))
    if i >= 0:
        return ok_orig, {'status': 'MOVED', 'path': rel, 'start_line': idx[i], 'end_line': idx[i + len(norm_ws(q['quote'])) - 1]}
    return ok_orig, {'status': 'REWORDED', 'path': rel}


def main():
    utf8_stdout()
    d = load_decisions()
    r01 = r01_readings()
    cors = read_jsonl(os.path.join(AUD, 'CORRECTION_PROPOSALS.jsonl'))
    out, overlay, problems = [], [], []
    for cor in cors:
        k, c = cor['case_key'], cor['candidate']
        grp = {'PROPOSED_PENDING_METHODOLOGY_PI012': 'PI012_DEPENDENT', 'PROPOSED_SOURCE_SUPPORTED': 'FROZEN_PROTOCOL_SUPPORTED', 'PROPOSED_FIELD_FIX_OPEN_QUESTION_RETAINED': 'PARTIAL_FIELD'}[cor['ratification']]
        ev = [current_status(c, q) for q in cor['quotes']]
        ok_orig = all(e[0] for e in ev)
        cur = [e[1] for e in ev]
        sets = dict(cor['set'])
        reading = r01.get(k)
        if k in d.SPECIAL:
            decision, extra, reason, counter = d.SPECIAL[k]
            if extra:
                sets.update(extra)
        elif grp == 'PI012_DEPENDENT':
            want = sets.get('modality')
            sub = sets.get('subclause_set')
            if k == 'FG-K1-0e4de41164':  # subclause fix, read at source: create only useful ones, same private-reference line as FG-K1-30d330bd66
                decision, reason, counter = 'ACCEPT', 'Unmarked create-only in a private reference: DEFAULT under A2. Same line as FG-K1-30d330bd66.', None
            elif reading and reading['modality_after'] == want:
                decision, reason, counter = 'ACCEPT', 'Equals the independent R01 reading under A2-PI012: %s' % reading['independent_reading'], reading.get('alternative_or_counterexample') or None
            elif reading and reading['result'] in ('UPHOLD',) and reading['modality_after'] != want:
                decision, reason, counter = 'REJECT', 'R01 upheld %s: %s' % (reading['modality_after'], reading['independent_reading']), reading.get('alternative_or_counterexample') or None
            else:
                decision, reason, counter = 'UNRESOLVED', 'No matching R01 reading.', None
                problems.append(k)
        elif k in d.ACCEPT_READ:
            decision, reason, counter = 'ACCEPT', d.ACCEPT_READ[k], None
        else:
            decision, reason, counter = 'UNRESOLVED', 'No decision recorded.', None
            problems.append(k)
        group_verified = grp
        if grp == 'FROZEN_PROTOCOL_SUPPORTED' and reading and reading.get('form') in ('PERMISSION_CONDITION',) and k not in ('FG-M-cf0b72f861',):
            group_verified = 'PI012_DEPENDENT_ON_RECHECK'
        if grp == 'PARTIAL_FIELD':
            group_verified = 'QUESTION_RESOLVED_BY_R02'
        row = {'correction_id': cor['correction_id'], 'case_key': k, 'candidate': c, 'decision': decision, 'group_stated': grp, 'group_after_check': group_verified, 'original_quote_verified': ok_orig, 'original_quotes': cor['quotes'], 'current_source': cur,
               'post_edit_mapping': sorted({x['status'] for x in cur}) or ['NO_QUOTE'], 'proposed_set': cor['set'], 'applied_set': None if decision in ('REJECT', 'UNRESOLVED') else sets, 'reason': reason, 'counterexample': counter, 'audit_rationale': cor['rationale'], 'alternatives_kept': cor.get('alternatives') or []}
        out.append(row)
        if decision in ('ACCEPT', 'ACCEPT_MODIFIED'):
            overlay.append({'key': k, 'candidate': c, 'set': sets, 'rule': 'R25-COR103', 'correction_id': cor['correction_id']})
    write_jsonl('CORRECTION_103_ADJUDICATION.jsonl', out)
    write_jsonl(os.path.join('_rules', 'R25-COR103', 'OVERLAY.jsonl'), overlay)
    print('rows', len(out), Counter(r['decision'] for r in out), 'groups', Counter(r['group_after_check'] for r in out), 'unverified original', sum(1 for r in out if not r['original_quote_verified']))
    print('post-edit', Counter(tuple(r['post_edit_mapping']) for r in out))
    print('problems', problems)


if __name__ == '__main__':
    main()
