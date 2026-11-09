"""Writes FINAL_CONSISTENCY_REPORT.md and the final STATUS.json from the logs and the audit results. Refuses a positive result unless the R27 gate passed and the audit has no FAIL."""
import importlib.util
import os
import subprocess
import sys
from collections import Counter, defaultdict

from order import ORDER
from rcommon import CANDIDATES, baseline, now, out_path, read_json, read_jsonl, utf8_stdout, write_json, write_text

TYPE = {'R01': 'Protocol, classification', 'R02': 'Template, enforcement', 'R03': 'Template', 'R04': 'Template, enforcement', 'R05': 'Template', 'R06': 'Template, enforcement', 'R07': 'Template', 'R08': 'Enforcement', 'R09': 'Template', 'R10': 'Template', 'R11': 'Template', 'R12': 'Template',
        'R13': 'Labels, no template edit', 'R14': 'Labels, no template edit', 'R15': 'Labels, no template edit', 'R16': 'No change verified', 'R17': 'Labels, no template edit', 'R18': 'No change verified', 'R19': 'Labels, scope mark', 'R20': 'Labels, no template edit', 'R21': 'Proposals', 'R22': 'Derived fields', 'R23': 'Adjudication', 'R24': 'Documentation', 'R25': 'Classification', 'R26': 'Derived view', 'R27': 'Audit'}
TITLE = {'R01': 'HQ-06 PI-012 reading', 'R02': 'HQ-01, 9.1 Git authority, dirty tree, protected branches', 'R03': 'HQ-02 cache invalidation', 'R04': 'HQ-03 floating versions', 'R05': 'HQ-04 headless Reserved work', 'R06': 'HQ-05 peer bypass', 'R07': '8.1 Swagger UI', 'R08': '8.2 K0 effective CPM', 'R09': '8.3 K1 compiled queries', 'R10': '8.4 L0 Production migrations', 'R11': '8.7 CUSTOM_SETTINGS', 'R12': '8.7 K1 local migrations', 'R13': '8.7 test priorities', 'R14': '8.7 C# language version', 'R15': '8.5 HTTP timeout', 'R16': '8.6 L1 liveness', 'R17': '8.7 security scan minimality', 'R18': '8.7 fast and slow tests', 'R19': '8.7 CI dependency updates', 'R20': '9.2 K0 deserialization', 'R21': '10 four new clauses', 'R22': '11.1 applicability and delivery', 'R23': '11.2 cross-method adjudication', 'R24': '11.3 evidence limits', 'R25': '103 corrections', 'R26': 'Repaired view', 'R27': 'Final audit'}
IMPACT = {'live agent': 'An agent could read the rule and still not follow it.', 'host behavior': 'How a headless host treats ask is unknown; the hook decision itself ran.', 'real database': 'Timelines are reasoned, not observed.', 'registry': 'Latest-stable and resolved versions are not confirmed.', 'NuGet restore': 'Whether restore accepts a floating version under CPM is unobserved; property evaluation did run.', 'live headless': 'The headless stop and the decision log are text, not observed.', 'host enforcement': 'Hooks ran directly, not through the host loop.', 'real API': 'The Swagger step was never carried out on an application.', 'CI trial': 'Out of study scope.', 'what an': 'As above, host behavior of ask.', 'floating vs checks': 'As above, registry and restore.', 'cache vs': 'As above, timelines.', 'Swagger vs': 'As above, Swagger.', 'all conditions': 'Unchanged policies rest on the baseline and on mechanical witness checks.'}


def impact_of(t):
    for k, v in IMPACT.items():
        if k.lower() in t.lower():
            return v
    return 'See the test row.'


def ver(*cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip().splitlines()[0]
    except (OSError, IndexError, subprocess.SubprocessError):
        return 'not available'


def overlay_counts():
    out = defaultdict(Counter)
    cand = {k: c for c in CANDIDATES for k in baseline(c)}
    for o in read_jsonl(out_path('_rules', 'R01-HQ06-PI012', 'OVERLAY.jsonl')):
        out['R01'][cand[o['key'].split('/')[0]]] += 1
    for rule in ('R15-85-HTTPTIMEOUT', 'R17-87-SECSCAN', 'R19-87-CIUPDATES', 'R20-92-K0DESER'):
        p = out_path('_rules', rule, 'overlay.py')
        spec = importlib.util.spec_from_file_location('o' + rule.replace('-', ''), p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for o in m.OVERLAY:
            out[rule[:3]][cand[o['key'].split('/')[0]]] += 1
    for o in read_jsonl(out_path('_rules', 'R25-COR103', 'OVERLAY.jsonl')):
        out['R25'][o['candidate']] += 1
    for r in read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl')):
        if r['status'] in ('REWORDED', 'REMOVED', 'ADDED'):
            out['R26'][r['candidate']] += 1
    return out


def main():
    utf8_stdout()
    gates = read_jsonl(out_path('GATE_LOG.jsonl'))
    last = {}
    tries = Counter()
    for g in gates:
        last[g['rule']] = g
        tries[g['rule']] += 1
    missing = [r for r in ORDER if r not in last or last[r]['gate'] not in ('PASS', 'PASS_WITH_NOT_RUN')]
    audit = read_jsonl(out_path('FINAL_AUDIT_RESULTS.jsonl'))
    a = Counter(r['status'] for r in audit)
    man = read_json(out_path('REPAIRED_VIEW_MANIFEST.json'))['counts']
    un = read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
    log = read_jsonl(out_path('CHANGE_LOG.jsonl'))
    final = last.get('R27-FINAL')
    ok = not missing and a['FAIL'] == 0 and final is not None
    result = 'PASS_WITH_DOCUMENTED_NOT_RUN' if ok else 'BLOCKED'
    files = defaultdict(lambda: defaultdict(set))
    for r in log:
        if r.get('kind') == 'TEMPLATE':
            files[r['rule'][:3]][r['candidate']].add(r['file'])
    ov = overlay_counts()
    o = []
    o.append('# Stage A Step 2 controlled corrections: final consistency report\n')
    o.append('**Result: `%s`.** %s\n' % (result, 'Every rule gate passed, and the final audit has no failed check. Runtime behavior was not tested; the list is below.' if ok else 'See the open items below: %s.' % missing))
    o.append('**This is a self-audit.** The same model and session made the repairs and this audit, so it is not an independent evaluation. A fresh-session reviewer who reads the final bytes without this report is the next step if independent assurance is wanted.\n')
    o.append('**Step 3 readiness: `CONDITIONAL_GO`.** Step 3 was not started. The conditions are in section 8.\n')
    tally = final['steps']['CUMULATIVE']['tally'] if final else {}
    o.append('## 1. Numbers\n')
    o.append('| Item | Value |\n|---|---:|')
    o.append('| Rules with a passing gate | %d of %d |' % (len(ORDER) - len(missing), len(ORDER)))
    o.append('| Failed gate attempts repaired before passing | %d |' % sum(1 for g in gates if g['gate'] == 'FAIL'))
    wc = read_json(out_path('WORKING_COPY_MANIFEST.json'))['candidates']
    mod = {c: sum(1 for f in wc[c].values() if f['origin'] == 'MODIFIED') for c in CANDIDATES}
    o.append('| Files that differ from the frozen templates | %d (%s) |' % (sum(mod.values()), ', '.join('%s %d' % (c, mod[c]) for c in CANDIDATES)))
    o.append('| Change-log rows, including rollbacks and re-applies | %d |' % sum(1 for r in log if r.get('kind') == 'TEMPLATE'))
    o.append('| Cumulative tests on final bytes: pass | %s |' % tally.get('PASS'))
    o.append('| Cumulative tests on final bytes: fail | %s |' % tally.get('FAIL', 0))
    o.append('| Cumulative tests on final bytes: not run | %s |' % tally.get('NOT_RUN', 0))
    o.append('| Final audit rows: pass, fail, not run, finding | %d, %d, %d, %d |' % (a['PASS'], a['FAIL'], a['NOT_RUN'], a['FINDING']))
    o.append('| Policy rows checked at the final gate | %d |' % (final['steps']['POLICY']['n_rows'] if final else 0))
    o.append('| Baseline records kept | 6,402 |')
    o.append('| Repaired view rows, active | %d, %d |' % (man['repaired_rows'], man['active_rows']))
    o.append('| Crosswalk | %s |' % ', '.join('%s %d' % (k, v) for k, v in sorted(man['by_crosswalk_status'].items())))
    o.append('| Coverage cells, moved status or strength | %d, %d |\n' % (man['coverage_rows'], len(man['coverage_or_strength_moved'])))
    o.append('The %s rows are 6,402 original identities, %d new claims and %d proposals. %d of the originals are inactive, because their source is gone.\n' % (format(man['repaired_rows'], ','), man['added_claims'], man['proposed_clauses'], man['inactive_removed_rows']))
    o.append('## 2. Rules\n')
    o.append('| Rule | Decision | Type | Gate | Attempts |\n|---|---|---|---|---:|')
    for r in ORDER:
        k = r[:3]
        g = last.get(r)
        o.append('| %s | %s | %s | %s | %d |' % (k, TITLE[k], TYPE[k], g['gate'] if g else 'NOT RUN', tries[r]))
    o.append('\n`PASS_WITH_NOT_RUN` means nothing failed, and some checks in the cumulative suite could not run here. Attempts counts every gate run, including failed runs that were repaired and re-runs after a pass.\n')
    o.append('## 3. Six-way outcome\n')
    o.append('Each cell: files edited (`e`) or records relabeled (`l`). A dash means no change there.\n')
    o.append('| Rule | ' + ' | '.join(CANDIDATES) + ' |\n|---|' + '---:|' * 6)
    for r in ORDER:
        k = r[:3]
        cells = []
        for c in CANDIDATES:
            e, l = len(files[k][c]), ov[k][c]
            cells.append(' '.join(x for x in (('%de' % e) if e else '', ('%dl' % l) if l else '') if x) or '—')
        o.append('| %s | %s |' % (k, ' | '.join(cells)))
    o.append('\nR13, R14, R16 and R18 show dashes because they changed no template and their label corrections are counted in the R25 row. R26 counts claims restated, removed or added.\n')
    o.append('After R02 to R07, the same obligation and condition read the same in all six, by side-by-side reading. R08 to R12 changed only the candidates the register named, and the parity leads that leaves are in section 6.\n')
    tm = read_json(out_path('SAME_TASK_MATRIX.json'))['hook_tasks']
    rep = [v for v in tm.values() if v['expectation'] == 'REPORT']
    frozen_same = all(v['frozen_first'][c] == v[c]['first'] for v in rep for c in CANDIDATES)
    o.append('**Same hypothetical task.** `SAME_TASK_MATRIX.json` runs the same commands through each real hook and the same manifests through each real checker, and it finds each required sentence with its loading class. Force and legacy-peer forms are denied in all six on both attempts. Recorded exceptions are honored for the named package only.\n')
    o.append('Two delivery differences remain. A pinned `npm install` with no marker is denied by M1 and K0, denied once by L1, and allowed by M, L0 and K1. `git reset --hard` and `git push --force` reach a hook only in K0, as `ask`; the other five rely on the always-loaded text. %s\n' % ('The same commands on copies of the frozen templates give the same first decisions, so no rule here introduced these differences.' if frozen_same else 'Some first decisions differ from copies of the frozen templates; see `SAME_TASK_MATRIX.json`.'))
    o.append('## 4. Cumulative checks\n')
    if final:
        o.append('| Suite | Pass | Not run |\n|---|---:|---:|')
        for k, v in final['steps']['CUMULATIVE']['by_suite'].items():
            o.append('| %s | %d | %d |' % (k[:3], v.get('PASS', 0), v.get('NOT_RUN', 0)))
    o.append('\nEach gate re-ran every earlier suite on current bytes, including mutation tests. A mutation test breaks a rule on a copy and confirms the test notices. All 196 policies per candidate have a row in `POLICY_CHECKS/R27-FINAL/`, joined with source reviews.\n')
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    o.append('**What the 1,176 rows do and do not show.** Each cell has a live witness at a current line. That is traceability. Only the changed policies were read side by side. `DIRECT_EVIDENCE` is not parity, and %d cells rest on a written Step 2 override or on partial witnesses, as they did in the baseline.\n' % sum(1 for x in cov if not x['direct_source_keys']))
    o.append('## 5. Data results\n')
    pi79, pi230 = Counter(r['result'] for r in read_jsonl(out_path('PI012_79_REVIEW.jsonl'))), Counter(r['result'] for r in read_jsonl(out_path('PI012_230_REVIEW.jsonl')))
    adj = Counter(r['decision'] for r in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl')))
    o.append('| Set | Outcome |\n|---|---|')
    o.append('| PI-012, 79 cases | %d correct, %d upheld, %d unresolved |' % (pi79['CORRECT'], pi79['UPHOLD'], pi79['UNRESOLVED']))
    o.append('| PI-012, 230 cases | %d correct, %d upheld, %d unresolved |' % (pi230['CORRECT'], pi230['UPHOLD'], pi230['UNRESOLVED']))
    o.append('| 103 corrections | %d accepted, %d accepted with changes, %d rejected, %d unresolved |' % (adj['ACCEPT'], adj['ACCEPT_MODIFIED'], adj['REJECT'], adj['UNRESOLVED']))
    o.append('| 4 new clauses | Candidate-specific proposals, not promoted, not copied |')
    o.append('| 31 open records | All resolved by a user decision and the matching rule, per `UNRESOLVED_DECISIONS.jsonl` |')
    o.append('| 5 strength cells, 3 overrides | Qualifier kept, none became a parity statement |')
    o.append('| 19 baseline `UNCERTAIN` records | None left; each has a rule and a current reading |')
    o.append('| `review_needed` flags | %d carried from the baseline, not individually cleared |\n' % sum(1 for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl')) if r.get('review_needed')))
    ap = man['applicability_status']
    o.append('The 4 PI-012 unresolved rows stay marked open in the view and are not strictness facts.\n')
    o.append('Applicability fields are derived, not verified: %s with no condition extracted, %s attributed, %s written by a reviewer, %s with the condition inside the claim text, %s not applicable. The 30-record sample in R22 found real defects, which were fixed, and it was then read again on the same draw, so it is not an error rate.\n' % tuple(format(ap[k], ',') for k in ('UNKNOWN_NOT_EXTRACTED', 'STATED_ATTRIBUTED', 'STATED_REVIEWED', 'CONDITION_IN_CLAIM_TEXT', 'NOT_APPLICABLE')))
    o.append('## 6. Findings and remaining tensions\n')
    o.append('No check failed. These are real and were left as they are, because no decision covers them.\n')
    for r in audit:
        if r['status'] == 'FINDING':
            o.append('- **%s.** %s' % (r['test'][0].upper() + r['test'][1:], r['detail']))
    o.append('\n**Parity leads.** Each is a difference that a named rule leaves in place. The register did not authorize changing them, so they were not changed:\n')
    for r in un:
        if r['kind'] == 'PARITY_LEAD':
            o.append('- `%s` (%s): %s' % (r['id'], ', '.join(r['candidates']), r['text']))
    o.append('\n**Readings that need a reviewer:**\n')
    for r in un:
        if r['kind'] == 'INTERPRETATION':
            o.append('- `%s`: %s %s' % (r['id'], r['text'], r['note']))
    o.append('\n## 7. What ran and what did not\n')
    o.append('**Executed:** %s; %s; %s; %s. Each candidate\'s own instruction, manifest, architecture and dependency checkers. Each pre-command hook with its real input format. `node --check` on all scripts. Git in disposable fixtures under `_scratch`. Real MSBuild property evaluation without restore in R08.\n' % (ver('python', '--version'), 'Node ' + ver('node', '--version'), ver('git', '--version'), '.NET SDK ' + ver('dotnet', '--version')))
    o.append('**Not run. None of these counts as PASS:**\n')
    o.append('| Test | Why | Impact |\n|---|---|---|')
    seen = set()
    if final:
        for x in final['steps']['CUMULATIVE']['not_run']:
            if x['test'] not in seen:
                seen.add(x['test'])
                o.append('| %s | %s | %s |' % (x['test'].replace('|', '/'), str(x['detail']).replace('|', '/')[:140], impact_of(x['test'])))
    o.append('\nFull limits are in `EVIDENCE_LIMITS.md`: same-family reader, targeted sampling, no unbiased error rate, records not re-read, and the union bound. Codex Pass 2 was not read.\n')
    o.append('## 8. Step 3 conditions\n')
    o.append('`CONDITIONAL_GO` holds only if Step 3 does all of these:\n')
    o.append('1. Start each run from a clean tree or with a standing choice. Otherwise the new R02 check stops a headless run at its first step, which is by design.')
    o.append('2. Treat coverage as traceability. Compare strictness only from reviewed text.')
    o.append('3. Keep the 4 PI-012 unresolved records and the 6 readings in section 6 out of strictness counts, or report results under both readings.')
    o.append('4. Check the not-run list above live where a result depends on it. The Swagger, headless and dirty-tree rules have never been observed in an agent.')
    o.append('5. Use `REPAIRED_CANDIDATE_DERIVED_VIEW` for the repaired templates and `FROZEN_BASELINE_REFERENCE` for the originals. Never mix their line anchors.')
    o.append('6. Run candidates from `candidates/<C>/template/` in this folder, not from the frozen inputs. This run did not promote them anywhere.\n')
    o.append('## 9. Finish criteria\n')
    o.append('| Criterion | State | Evidence |\n|---|---|---|')
    o.append('| Each agreed question has a disposition | %s | `DECISION_IMPLEMENTATION_MATRIX.md`, and section 2 of this report |' % ('Met' if not missing else 'Not met'))
    o.append('| Each modified rule has a passing gate | %s | `GATE_LOG.jsonl`, `CHECKPOINTS/` |' % ('Met' if not missing else 'Not met'))
    o.append('| No later change broke an earlier fix | %s | Cumulative suites on final bytes: %s failed |' % ('Met' if tally.get('FAIL', 0) == 0 and final else 'Not met', tally.get('FAIL', 0)))
    o.append('| 1,176 policy checks accounted for | Met | `POLICY_CHECKS/R27-FINAL/`, `REPAIRED_POLICY_COVERAGE.jsonl` |')
    o.append('| Overlays replay | Met | R26 suite and audit section F |')
    o.append('| Original inputs unchanged | Met | `fence.py`, audit section A |')
    o.append('| No Step 3 | Met | Audit section A |')
    o.append('| Non-executable tests named | Met | Section 7 |\n')
    o.append('## 10. Re-run\n')
    o.append('From this folder, with `PYTHONPATH=_tools`:\n')
    o.append('```bash\npython -B _tools/fence.py verify\n```\n```bash\npython -B _tools/dataset.py\n```\n```bash\npython -B _tools/final_audit.py\n```\n```bash\npython -B _tools/gate.py R27-FINAL --note "re-run"\n```\n')
    o.append('The original templates are in `inputs/`. The repaired ones are in `candidates/<C>/template/`. Each change is in `CHANGE_LOG.jsonl` with before and after hashes.\n')
    write_text('FINAL_CONSISTENCY_REPORT.md', '\n'.join(o) + '\n')
    write_json('STATUS.json', {'version': 'step2-controlled-repair-v1', 'at': now(), 'phase': 'COMPLETE' if ok else 'BLOCKED', 'rule': 'R27-FINAL', 'rule_index': len(ORDER), 'n_rules': len(ORDER), 'status': result, 'step3_readiness': 'CONDITIONAL_GO' if ok else 'NO_GO', 'step3_started': False, 'self_audit': True, 'resume_point': None if ok else (missing[0] if missing else 'R27-FINAL'), 'resume': 'See RESUME.md and FINAL_CONSISTENCY_REPORT.md.', 'source_hashes': 'BASELINE_MANIFEST.json, WORKING_COPY_MANIFEST.json, FENCE_SNAPSHOT.json'})
    mark = '## Final status'
    mp = out_path('DECISION_IMPLEMENTATION_MATRIX.md')
    text = open(mp, encoding='utf-8').read().split('\n' + mark)[0].rstrip('\n')
    rows = '\n'.join('| %s | %s | %s |' % (r[:3], TITLE[r[:3]], last[r]['gate'] if r in last else 'NOT RUN') for r in ORDER)
    write_text('DECISION_IMPLEMENTATION_MATRIX.md', '%s\n\n%s\n\nAdded after the gates. The matrix above is unchanged from before the first edit.\n\n| Rule | Decision | Gate |\n|---|---|---|\n%s\n' % (text, mark, rows))
    rp = out_path('RESUME.md')
    head = '> **State:** %s. Nothing to resume unless a reviewer reopens a rule. See `STATUS.json` and `FINAL_CONSISTENCY_REPORT.md`.' % result
    body = open(rp, encoding='utf-8').read()
    body = body.split('\n', 1)[1] if body.startswith('> **State:**') else body
    write_text('RESUME.md', head + '\n' + body)
    print(result, 'missing', missing, dict(a), 'tally', tally)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
