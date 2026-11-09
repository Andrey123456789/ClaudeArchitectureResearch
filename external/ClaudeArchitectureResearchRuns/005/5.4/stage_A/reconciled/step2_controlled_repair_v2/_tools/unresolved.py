"""Writes UNRESOLVED_DECISIONS.jsonl: dispositions of the audit's open items, plus what stays open after this run. Deterministic."""
import os

from rcommon import AUD, out_path, read_jsonl, utf8_stdout, write_jsonl

BY_QUESTION = {
    'HQ-01': ('R02-HQ01-GOV015', 'Register HQ-01', 'The approved-workflow allowance is gone from the source in all six. Fields follow the current text (R26).'),
    'NON_REWRITABLE_READING': ('R02-HQ01-GOV015', 'Register 9.1', 'Non-rewritable by default, with an explicit request naming the branch as the route. Entailed by GOV-015.'),
    'HQ-02': ('R03-HQ02-RUN021', 'Register HQ-02', 'Pre-mutation invalidation is allowed when correctness is shown. Read as a permission inside RUN-021.'),
    'SCAN_LINE_READING': ('R20-92-K0DESER', 'Register 9.2', 'Read as a scan criterion, not a product prohibition. No SEC-003 obligation invented.'),
    'HQ-04': ('R05-HQ04-GOV017', 'Register HQ-04', 'Same headless rule in all six. The ambiguous sentence is gone.'),
}
DUP = {'non-rewritable': 'NON_REWRITABLE_READING', 'approved-workflow': 'HQ-01', 'run-021': 'HQ-02', 'headless': 'HQ-04', 'same tension': 'HQ-04'}

INTERPRETATIONS = [
    ('R02-TASK-SCOPE', 'R02-HQ01-GOV015', 'Task-start check: "a task" is read as one that will change files or repository state. A read-only review does not trigger it.', 'A reader could apply the check to every task. Cost: a read-only task stops on a dirty tree.'),
    ('R02-HEADLESS-DIRTY', 'R02-HQ01-GOV015', 'A headless run on a dirty tree with no standing choice pauses and changes nothing. An experiment harness must supply a clean tree or a standing choice, or every run stops at the first step.', 'Consequence for Step 3 runs, not a defect.'),
    ('R04-RECORD-FORGERY', 'R04-HQ03-DEP003', 'The exception record can be written by the agent itself. A checker cannot verify who asked; `requested_by` and `request` are self-attested.', 'Enforcement stops accidents and leaves an audit trail, not a determined agent.'),
    ('R01-COMMON-VALUE', 'R01-HQ06-PI012', 'The addendum reads unmarked "only when" as DEFAULT in knowledge text. Option D in PI012_SENSITIVITY.md is the alternative.', 'MUST_NOT counts under each reading are in PI012_SENSITIVITY.md. No coverage or strength cell moves in any reading.'),
    ('R01-TRIGGERED-CLASS', 'R01-HQ06-PI012', 'Form "do not X when Y" stays MUST_NOT. A scan found 21 more lines of this form that were not read individually.', 'Bound, not a census.'),
    ('R22-UNDER-EXTRACTION', 'R22-111-TRIGGER', 'Scope in a parenthesis of the original trigger field is not extracted.', 'The original field keeps the text.'),
]
PARITY_LEADS = [
    ('R10-SCAFFOLD-WORDING', 'R10-84-L0MIGR', ['M', 'M1', 'L1', 'K1'], 'Similar scaffold migration wording. L1 development-workflow says "Never apply" with no "by default". Register 8.4 named only L0.'),
    ('R08-LITERAL-CPM', 'R08-82-K0CPM', ['M', 'M1', 'L0', 'L1', 'K1'], 'Literal CPM checks. Register 8.2 named only K0, so an inherited setting is honored only in K0.'),
    ('R09-MEASURED-LINES', 'R09-83-K1PERF', ['M', 'M1', 'L0', 'L1', 'K0'], '"Measured hot path" technique lines. Register 8.3 named only K1.'),
    ('R13-TEST-PRIORITY', 'R13-87-TESTPRIORITY', ['M', 'K0', 'K1'], 'The test-priority sentence appears only in these three. No obligation differs after classification.'),
    ('R19-CI-RULE-SPREAD', 'R19-87-CIUPDATES', ['M', 'M1', 'L0', 'L1', 'K0', 'K1'], 'The CI auto-update rule is in all six, not the four the task named. Preserved and labeled out of practical evaluation scope.'),
    ('R20-DESER-FORMS', 'R20-92-K0DESER', ['M', 'M1', 'L0', 'L1', 'K0', 'K1'], 'Deserialization forms differ: marked in M, M1, L0, K1; a scan criterion in K0; a list item in L1. All six sit in a scan layer.'),
]


def main():
    utf8_stdout()
    rows = []
    for r in read_jsonl(os.path.join(AUD, 'UNRESOLVED_QUEUE.jsonl')):
        q = r['question_type'].split(' ')[0]
        rule, source, how = BY_QUESTION[q]
        rows.append({'kind': 'ORIGINAL_OPEN_RECORD', 'id': r['key'], 'candidate': r['candidate'], 'question': q, 'status': 'RESOLVED_BY_USER_DECISION', 'resolved_by': rule, 'decision_source': source, 'how': how, 'audit_remaining_ambiguity': r.get('remaining_ambiguity')})
    for r in read_jsonl(os.path.join(AUD, 'AUDIT_LEDGER.jsonl')):
        if r.get('open') and r['case_id'].split(':')[0] in ('ORP', 'QUE'):
            text = (r.get('rationale') or '').lower()
            q = next(v for k, v in DUP.items() if k in text)
            rule, source, how = BY_QUESTION[q]
            rows.append({'kind': 'ORIGINAL_OPEN_DUPLICATE_ITEM', 'id': r['case_id'], 'candidate': r.get('candidate'), 'question': q, 'status': 'RESOLVED_WITH_ITS_QUESTION', 'resolved_by': rule, 'decision_source': source, 'how': 'Duplicates the question. ' + how})
    for f in ('PI012_79_REVIEW.jsonl', 'PI012_230_REVIEW.jsonl'):
        for r in read_jsonl(out_path(f)):
            if r['result'] == 'UNRESOLVED':
                rows.append({'kind': 'PI012_UNRESOLVED', 'id': r['key'], 'candidate': r.get('candidate'), 'list': f, 'status': 'OPEN', 'resolved_by': None, 'reason': r.get('independent_reading'), 'alternative': r.get('alternative_or_counterexample'), 'handling': 'Stored modality kept. Marked repair.open_question in the view. Not a strictness fact.'})
    for i, rule, text, note in INTERPRETATIONS:
        rows.append({'kind': 'INTERPRETATION', 'id': i, 'rule': rule, 'status': 'OPEN_FOR_REVIEW', 'text': text, 'note': note})
    for i, rule, cands, text in PARITY_LEADS:
        rows.append({'kind': 'PARITY_LEAD', 'id': i, 'rule': rule, 'candidates': cands, 'status': 'NOT_CHANGED_NOT_AUTHORIZED', 'text': text})
    write_jsonl('UNRESOLVED_DECISIONS.jsonl', rows)
    from collections import Counter
    print(Counter(r['kind'] for r in rows))


if __name__ == '__main__':
    main()
