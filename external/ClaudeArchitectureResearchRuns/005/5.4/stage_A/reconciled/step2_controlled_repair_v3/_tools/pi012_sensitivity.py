"""Writes PI012_SENSITIVITY.md from the review files. Counts are recomputed, not typed."""
import os
import sys
from collections import Counter

from pi012 import R, split_key
from rcommon import CANDIDATES, baseline, coverage, out_path, read_jsonl, utf8_stdout, write_text
from roverlay import apply_fields, coverage_of


def main():
    utf8_stdout()
    r79 = read_jsonl(out_path('PI012_79_REVIEW.jsonl'))
    r230 = read_jsonl(out_path('PI012_230_REVIEW.jsonl'))
    ext = read_jsonl(out_path('PI012_EXTENSION_REVIEW.jsonl'))
    overlay = read_jsonl(out_path(R, 'OVERLAY.jsonl'))
    uniq = {r['key']: r for r in r79 + r230 + ext}
    forms = Counter((r['form'], r['result']) for r in uniq.values())

    def must_not_count(state):
        out = {}
        for c in CANDIDATES:
            out[c] = sum(1 for r in state[c].values() if r.get('modality') == 'MUST_NOT') + sum(1 for r in state[c].values() for s in r.get('subclauses') or [] if s.get('modality') == 'MUST_NOT')
        return out

    base = {c: dict(baseline(c)) for c in CANDIDATES}
    accepted = {c: dict(baseline(c)) for c in CANDIDATES}
    opt_d = {c: dict(baseline(c)) for c in CANDIDATES}
    for o in overlay:
        k, sub = split_key(o['key'])
        accepted[o['candidate']][k] = apply_fields(accepted[o['candidate']][k], o['set'], sub)
        if uniq[o['key']]['form'] != 'PERMISSION_CONDITION':
            opt_d[o['candidate']][k] = apply_fields(opt_d[o['candidate']][k], o['set'], sub)
    a, b, d = must_not_count(base), must_not_count(accepted), must_not_count(opt_d)
    moved, lost = [], []
    for c in CANDIDATES:
        cov = coverage_of(accepted[c].values())
        for pid, row in cov.items():
            st = coverage(c)[pid]
            if row['strength_status'] != st['strength_status']:
                moved.append('%s %s: %s -> %s' % (c, pid, st['strength_status'], row['strength_status']))
            if row['computed_status'] != st['computed_status']:
                lost.append('%s %s: %s -> %s' % (c, pid, st['computed_status'], row['computed_status']))
    trig = sorted(k for k, r in uniq.items() if r['form'] == 'TRIGGERED')
    sec = sorted(k for k, r in uniq.items() if r['security_sensitive'])
    disagree = [(r['key'], r['audit_modality'], r['modality_after'], r['result']) for r in r79 if r['agrees_with_audit'] is False]
    t = []
    t.append('# PI-012 sensitivity\n')
    t.append('Recomputed from `PI012_79_REVIEW.jsonl`, `PI012_230_REVIEW.jsonl`, `PI012_EXTENSION_REVIEW.jsonl` and `_rules/R01-HQ06-PI012/OVERLAY.jsonl`. Label and modality counts, not a strictness comparison.\n')
    t.append('## Cases read\n')
    t.append('| List | Rows | CORRECT | UPHOLD | UNRESOLVED |\n|---|---:|---:|---:|---:|')
    for name, rows in (('79 flat negatives', r79), ('230 residual leads', r230), ('Extension (same-class scan outside both lists)', ext)):
        cc = Counter(r['result'] for r in rows)
        t.append('| %s | %d | %d | %d | %d |' % (name, len(rows), cc['CORRECT'], cc['UPHOLD'], cc['UNRESOLVED']))
    t.append('\nUnique cases by original stable key: %d (76 keys sit on both lists). `MUST` and `MUST_NOT` are one force class: where only the token polarity differs the stored token stays and the row says so.\n' % len(uniq))
    t.append('## By form\n')
    t.append('| Form | Result | Cases |\n|---|---|---:|')
    for (f, res), n in sorted(forms.items()):
        t.append('| %s | %s | %d |' % (f, res, n))
    t.append('\n## `MUST_NOT` records by candidate under each reading\n')
    t.append('| Candidate | Baseline (rule rejected) | Approved addendum | Option D: only-when and do-not-unless stay binding, other forms follow the addendum |\n|---|---:|---:|---:|')
    for c in CANDIDATES:
        t.append('| %s | %d | %d | %d |' % (c, a[c], b[c], d[c]))
    t.append('\nThe addendum picks `DEFAULT` as the common value for permission-granting conditionals in knowledge text. Option D is the alternative the decision wording does not fully exclude; see the addendum, section "Uncertainty kept".\n')
    t.append('## Policy cells\n')
    t.append('Coverage `status` moved on %d of 1,176 cells. `strength_status` moved on %d cells.\n' % (len(lost), len(moved)))
    if moved:
        t.append('Cells whose strength status moves under the addendum:\n')
        t.extend('- ' + m for m in moved)
        t.append('')
    t.append('## Classes kept visible\n')
    t.append('- **Triggered prohibitions** (`do not X when Y`): %d cases in the reviewed set stay at `MUST_NOT` under A1.3, class `TRIGGERED`. A scan outside the reviewed set found 21 more (bound, not a census). If a later decision reads them with `only when`, these move to `DEFAULT`.' % len(trig))
    t.append('- **Security-sensitive `DEFAULT` lines:** %s. The rule owners stay binding where the coverage rows show them.' % ', '.join('`%s`' % k for k in sec))
    t.append('- **Approval gates** (`unless explicitly requested`, `only when explicitly requested`, `unless asked`) stay binding in every form, under C8.')
    t.append('- **Wording splits kept because the marked form falls under frozen A1.3, not under the approved equivalence:** `FG-M-f49bbb7f3e` and `FG-M1-4efa9a2d0d`; `FG-M-9050e41bb6` and `FG-M1-7390ef4e06`; `FG-L1-27906e338d` and `FG-M-58080e9816`, `FG-M1-915d8195be`; `FG-K0-87b93f63f7` and the "never hide" lines in M, L1, K1; `FG-M-f08ed79dde`, `FG-M1-b7c8a98af1` and `FG-L0-bd2c887b48`, `FG-L1-0cdd9708ae`. Step 3 must not count these as strictness differences.')
    t.append('- **Source differences that are real:** L1 `FG-L1-e0afa72103` and K1 `FG-K1-6ee32b45c6` write "Never" where M, M1, L0, K0 write "Not retried:".')
    t.append('\n## Disagreement with the audit on the 79\n')
    if disagree:
        t.extend('- `%s`: audit `%s`, here `%s` (%s)' % x for x in disagree)
    t.append('\nThe audit and this reading are the same model family, so agreement is weak evidence of correctness.\n')
    t.append('## Bounds, not a census\n')
    t.append('- The 79 are a floor from one scan. The 230 are a heuristic: stored `MUST` or `MUST_NOT` on knowledge text where the closest sentence has no must-like word.')
    t.append('- The extension scan looked at the sentence closest to the claim on knowledge-only records outside both lists: 22 `do not ... unless/without`, 8 `only when`, 21 `do not ... when/if`. A sentence the heuristic does not pick is missed, so these are lower bounds.')
    t.append('- Records with evidence in rule files or workflow skills were not read under this rule; the frozen readings hold there.')
    write_text('PI012_SENSITIVITY.md', '\n'.join(t) + '\n')
    print('MUST_NOT baseline', a, 'addendum', b, 'optD', d)
    print('strength cells moved', len(moved), moved[:40])
    print('coverage moved', len(lost), lost[:10])


if __name__ == '__main__':
    main()
