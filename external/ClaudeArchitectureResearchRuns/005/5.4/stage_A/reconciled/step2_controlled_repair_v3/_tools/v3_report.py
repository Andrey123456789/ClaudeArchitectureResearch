"""Writes the mechanical v3 deliverables from logs and final files (no judgment here; prose lives in the final report):

  REGRESSION_MATRIX.md                 every gate attempt, its steps and tallies, from GATE_LOG.jsonl
  V2_TO_V3_FILE_CROSSWALK.jsonl        one row per candidate file: v2 hash, v3 hash, changed, rules (from V3_FINAL_MANIFEST.json)
  UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl  open items with reason, risk and owner
  ADJUDICATION_SUMMARY.md              counts from ADJUDICATION_COUNTS.json and UNIQUE_ISSUE_CLUSTERS.jsonl

PYTHONPATH=_tools python -B _tools/v3_report.py
"""
from collections import Counter

from order import V3_ORDER
from rcommon import CANDIDATES, out_path, read_json, read_jsonl, utf8_stdout, write_jsonl, write_text

QUEUE = [
    dict(id='Q-01', kind='USER_DECISION', topic='L0 lacks the "raw HTML in any server-rendered UI" security-scan prompt that M, M1, L1, K0 and K1 carry (CL15).', reason='A candidate-specific extra in five; no approved policy requires it; adding it would be a new shared requirement.', risk='Low: all candidates target an Angular SPA; server-rendered UI is hypothetical.', proposal='Leave as written, or approve adding the sentence to L0 scan-layers.md.'),
    dict(id='Q-02', kind='USER_DECISION', topic='Blank PreToolUse command: L0, K0 and K1 allow it (nothing to run); M, M1 (PV2-02) and L1 block it.', reason='PV2-02 approved fail-closed handling for M and M1 only.', risk='Low: a blank command executes nothing.', proposal='Leave, or approve the same block in L0, K0 and K1.'),
    dict(id='Q-03', kind='USER_DECISION', topic='Event/tool mismatch handling differs: K1 alone blocks a mismatched event; L0 and L1 block a non-shell tool; M1 (PV2-02) blocks a non-PreToolUse event.', reason='Outside PV2-02 scope for L0, L1, K0, K1.', risk='Low: the host sends consistent payloads.', proposal='Leave, or approve one rule for all six.'),
    dict(id='Q-04', kind='OBSERVATION', topic='K0 asks for git appearing after an unrecognized leading word (echo git commit -m x); the other five allow it.', reason='K0 classifies the first recognized tool anywhere in a segment; PV2-01 used each candidate own command-position parsing.', risk='Low: an extra prompt in K0, never a missed mutation in the fixtures.', proposal='Leave (K0 is the reference and is outside PV2-01 edit scope).'),
    dict(id='Q-05', kind='OBSERVATION', topic='M1 check-instructions accepts a section reference whose leading words match a heading (CL21).', reason='Deliberate tolerance of trailing prose; side effect weakens the stated rule.', risk='Low: instruction-maintenance only.', proposal='Leave, or approve a stricter match.'),
    dict(id='Q-06', kind='OPEN_CLASS', topic='"do not" bans stored at a soft modality were not reviewed (the 86-class was found by "never"/"must not" only). Example: L1 FG-L1-34be702ec3 DEFAULT while M (after V3-D02) and M1 store the same NgModules ban MUST_NOT.', reason='Outside the 86-record class kit 74 named.', risk='Medium for any strictness metric: raw MUST_NOT counts stay unusable.', proposal='A separate review of "do not" records before Step 3 metrics use modality.'),
    dict(id='Q-07', kind='OPEN_HYPOTHESIS_RESIDUE', topic='Codex ran three of six strategy families; no saturation is claimed by Codex or here.', reason='Codex Pass 0004+ was paused by the user and not read.', risk='Unknown: clauses no pass surfaced are not covered.', proposal='Further Codex passes only on a new user instruction.'),
    dict(id='Q-08', kind='NOT_RUN', topic='Live host behavior: ask display and answer, deny, exit 2, onFailure, headless meeting ask.', reason='No live Claude Code host in this run.', risk='Medium for Step 3 harness design (headless runs meet Git asks).', proposal='Observe in a Step 3 pilot before metrics.'),
    dict(id='Q-10', kind='RESOLVED', topic='Found by v3 testing, pre-existing: a PackageVersion with no Version passed the M1 and K0 checkers (root and nested) and errored in M, L0, L1 and K1; NuGet warns NU1604 (no lower bound). K0 also accepted an empty Version child element, and M rejected a valid Version child element.', reason='Resolved within approved semantics by V3-Q10-PACKAGEVERSION-VERSION (DEP-006 and DEP-003, frozen oracle MUST; PV2-03 invalid package metadata; each candidate NuGet text). The normative text of no candidate changed.', risk='None left in the fixtures: missing, empty and floating versions error in all six; a valid child-element version is OK in all six.', proposal='None. Kept so the earlier queue entry stays traceable.'),
    dict(id='Q-09', kind='QUALIFIED', topic='L1 FG-L1-5f5febf5c6 (304 catalogue line) kept DEFAULT although the line says "never"; peers say "is not".', reason='Definitional catalogue form; not a proved error.', risk='Low.', proposal='Leave unless a modality convention for catalogue entries is set.'),
    dict(id='Q-11', kind='OBSERVATION', topic='CPM without the .NET SDK: K0 and M keep a static error when no Directory.Packages.props is in an ancestor folder of a project; M1, L0, L1 and K1 report NOT_RUN (exit 3). A valid DirectoryPackagesPropsPath layout therefore errors in K0 and M only when the SDK is missing.', reason='PV2-03B kept the static fallback so no enforcement is relaxed; with the SDK all six agree.', risk='Low: both outcomes are non-pass; the K0 and M message overstates certainty without the SDK.', proposal='Leave, or approve NOT_RUN instead of the static error in K0 and M.'),
    dict(id='Q-12', kind='USER_DECISION', topic='No candidate checks the name of a central file MSBuild imports through DirectoryPackagesPropsPath: all six accept config/Packages.props, and the static per-file version checks (routed by the file name Directory.Packages.props) do not read it; the shared evaluator still proves CPM and reports floating versions as notices.', reason='Uniform across six; the rule texts say versions belong in Directory.Packages.props. Whether a renamed central file is allowed is a policy choice no decision makes.', risk='Low: an unusual layout; NuGet enforces CPM regardless of the name.', proposal='Leave, or approve requiring the name Directory.Packages.props in all six.'),
    dict(id='Q-13', kind='ENVIRONMENT', topic='Outside this session the protected v2 convenience archive stage_A/reconciled/step2_controlled_repair_v2.zip was removed (preflight SHA-256 e1e293ea...), and step2_controlled_repair_v3.zip and Stage_A_Step2_V3_Independent_Interim_Review_EN.md were added (EXTERNAL_EVENTS.json ENV-01 to ENV-03).', reason='The v2 tree itself is fenced file by file and unchanged; the fence and R27 tolerate exactly these recorded events.', risk='Low for research data; the v2 archive is no longer beside the v2 tree.', proposal='Restore the v2 archive from your copy if it should stay beside the tree.'),
]


def regression():
    rows = read_jsonl(out_path('GATE_LOG.jsonl'))
    t = ['# Regression matrix (v3)\n', 'Every gate attempt in order, from `GATE_LOG.jsonl`. A failed attempt wrote no checkpoint; the change was repaired and the whole gate re-run. NOT_RUN is never counted as PASS.\n',
         '| # | Change | Gate | Pass | Fail | Not run | Failed steps / cause |', '|---:|---|---|---:|---:|---:|---|']
    for i, r in enumerate(rows, 1):
        tally = ((r.get('steps') or {}).get('CUMULATIVE') or {}).get('tally') or {}
        failed = [k for k, v in (r.get('steps') or {}).items() if v.get('status') != 'PASS']
        cause = ', '.join(failed) if failed else ''
        if r.get('crash'):
            cause = 'crash: ' + (r.get('note') or r['crash'][-160:].replace('\n', ' '))
        if not failed and r['gate'] == 'FAIL' and not r.get('crash'):
            cause = 'see log'
        fails = ((r.get('steps') or {}).get('CUMULATIVE') or {}).get('failures') or []
        if fails:
            cause += ' (' + '; '.join('%s: %s' % (f['suite'], f['test'][:70]) for f in fails[:2]) + ')'
        t.append('| %d | %s | %s | %s | %s | %s | %s |' % (i, r['rule'], r['gate'], tally.get('PASS', ''), tally.get('FAIL', ''), tally.get('NOT_RUN', ''), cause.replace('|', '/')))
    final = read_json(out_path('FINAL_SUITE_TALLY.json')) if __import__('os').path.exists(out_path('FINAL_SUITE_TALLY.json')) else None
    if final:
        t += ['', '## Cold audit, all suites on final bytes', '', '| Suite | Pass | Fail | Not run |', '|---|---:|---:|---:|']
        for s, v in final['by_suite'].items():
            t.append('| %s | %d | %d | %d |' % (s, v.get('PASS', 0), v.get('FAIL', 0), v.get('NOT_RUN', 0)))
        t.append('| **Total** | **%d** | **%d** | **%d** |' % (final['tally'].get('PASS', 0), final['tally'].get('FAIL', 0), final['tally'].get('NOT_RUN', 0)))
    t += ['', 'Notes on attempts whose cause is not a defect of the change itself:', '',
          '- V3-D02 attempt 1: FENCE and R27 failed only on files changed outside this session (v2 archive removed; v3 archive and interim review added). Recorded as ENV-01 to ENV-03 in `EXTERNAL_EVENTS.json`; `fence.py` and `final_audit.py` tolerate exactly those bytes (V3_ADAPTATIONS rows, selftest negatives). The change itself was unchanged between attempts.',
          '- PV2-04 attempt 1 crashed on a quoting error in `adaptations.py`; V3-0 attempt 1 crashed before logging (bootstrap had not copied v2 rule snapshots). Both are tooling faults, fixed and re-gated.',
          '- Cold audit (`AUDIT_ATTEMPTS/`): attempt 1 had one FAIL, a false positive in the audit\'s own Codex-name scan (prose lines stating the pruning); attempt 2 was stopped after section E because the new behavioral test itself named a later pass literally; attempt 3 is final, with no FAIL.']
    t += ['', 'Suites: 27 v1 rules, 9 v2 changes, and one per v3 change (%s). A v1 or v2 suite changed only with a row in `_tools/adaptations.py`.' % ', '.join(V3_ORDER)]
    write_text('REGRESSION_MATRIX.md', '\n'.join(t) + '\n')


def file_crosswalk():
    man = read_json(out_path('V3_FINAL_MANIFEST.json'))['candidates']
    out = []
    for c in CANDIDATES:
        for rel, v in sorted(man[c]['files'].items()):
            out.append({'candidate': c, 'path': rel, 'v2_sha256': v['v2_sha256'], 'v3_sha256': v['sha256'], 'frozen_sha256': v['frozen_sha256'], 'changed_vs_v2': v['changed_vs_v2'], 'changed_vs_frozen': v['changed_vs_frozen'], 'rules': v['rules']})
    write_jsonl('V2_TO_V3_FILE_CROSSWALK.jsonl', out)
    return Counter((x['candidate'], x['changed_vs_v2']) for x in out)


DECISIONS = [
    ('PV2-01', 'PV2-01-GIT-GATING', 'Git PreToolUse permission parity', [
        ('M, M1, L0, L1, K1 gate repository-changing Git within their own hooks', 'K0 table placed once, byte-identical, in each hook (M dependency-guard.mjs, M1 dependency-commands.js, L0 claude-hook.mjs, L1 pre-shell-command.mjs, K1 classify-command.cjs); K0 untouched', 'source check: block byte-identical to the reference and equal to K0 apart from helper names'),
        ('Read-only git status/diff/log run without a Git prompt', '25 read-only or non-Git fixtures', 'allow in all six'),
        ('Mutations distinguished, incl. global options, wrappers, multi-command lines; no substring heuristic only', '41 Bash + 3 PowerShell mutating fixtures (-C, -c, --git-dir, bash -c, sh -c, cmd /c, pwsh/powershell -Command, env, VAR=, &, quoted git.exe path, ; && |)', 'ask in all six'),
        ('Return ask; an existing more restrictive non-Git guard still denies', '3 combined lines with npm --force/--legacy-peer-deps', 'deny or block in all six; L1 mutation that moves the ask first is caught'),
        ('ask is not authorization; HQ-01/GOV-015, dirty tree, headless, scoped commits, main rewrite preserved', 'ask reason names the explicit-request rule; git-workflow says the prompt is not authorization; R02 and C04 replay', 'R02/C04 suites PASS at every gate; audit interaction rows'),
        ('No unconditional commits; dependency guards not weakened', 'no commit step added; C04 sweep; DEP-025 fixtures', 'PASS'),
        ('Script-level decisions verified for six with common fixtures; live host separate', 'one matrix on six real hooks', 'live host ask display/answer and headless behavior NOT_RUN')]),
    ('PV2-02', 'PV2-02-FAILCLOSED-INPUT', 'Fail-closed malformed shell PreToolUse input for M and M1', [
        ('Block malformed, empty, non-object JSON', 'M readInput(invalidInput) -> exit 2; M1 readStdinJson -> deny', 'malformed, empty, whitespace, BOM-only, array, string, number, null: blocked'),
        ('Block missing, blank, non-string tool_input.command on shell PreToolUse', 'explicit checks in both hooks', 'no tool_input, non-object, no command, blank, empty, number, array, command under another field, PowerShell without command: blocked'),
        ('Block inconsistent event/tool payloads when applicable', 'M: unhandled or missing event, missing tool_name; M1: event other than PreToolUse, missing tool_name', 'blocked'),
        ('Keep valid read-only commands allowed; no command required on unrelated events', 'git status/diff/log, ls, Get-ChildItem, npm ci, BOM+valid JSON allowed; non-shell tool allowed; M PostToolUse without command exit 0', 'PASS'),
        ('Direct execution: exit codes and decision payloads; host onFailure untested', 'adversarial matrix + 5 mutations', 'live host application of exit 2/deny/onFailure NOT_RUN')]),
    ('PV2-03', 'PV2-03-K0-CPM-ROOT', 'Remove the K0-only root requirement for Directory.Packages.props', [
        ('Remove the root-only mandate in checker, D-17 and rule text', 'check-dependencies.cjs nearest-ancestor check per project; D-17 and NuGet rule: root typical, any MSBuild-imported location valid', 'no "missing at the repository root" anywhere in K0; the ancestor check still rejected a non-ancestor file that MSBuild imports (completed by PV2-03B)'),
        ('Nested positive fixtures managing all projects', 'nested file, two areas, nested Directory.Build.props, root (typical)', 'OK in all six (real MSBuild)'),
        ('Negatives: project without effective CPM, overridden/disabled, invalid metadata, mixed layouts', 'project outside the nested file, nested file off, project override false, version in project, malformed XML in the nested file', 'ERROR in all six; a PackageVersion with no Version was OK in M1 and K0 at this gate (pre-existing, recorded as Q-10, resolved by V3-Q10)'),
        ('Do not relax CPM, versions, floating exceptions or other guards', 'C01 evaluator unchanged (byte-identical in six); DEP-003 switch interaction', 'C01/R04/R08 suites PASS; mutation re-adding the root rule is caught'),
        ('Registry restore', 'not available', 'NOT_RUN')]),
    ('PV2-04', 'PV2-04-M-FRONTEND-TESTS', 'Frontend-test placement parity for M', [
        ('Add the ban to M in its normative owner, same scope/authority/modality as peers', 'M project-structure step 7 (the owner named by M solution-layout.md): "Never place frontend tests under `backend/`."', 'text present; record V3A-M-030 MUST_NOT, DEP-024 PARTIAL, PC, as M1 and K0'),
        ('Test acceptable and forbidden layouts', 'workspace colocated, workspace e2e, backend/*.spec.ts, backend ClientApp e2e, backend .cs test', 'same verdicts in all six (text model)'),
        ('No extraneous layout mandates', 'step 7 otherwise unchanged; CLAUDE.md untouched', 'PASS; mutation removing the sentence is caught'),
        ('Enforcement by a checker', 'no candidate has one', 'NOT_RUN in all six (text duty)')]),
    ('PV2-03 (completed)', 'PV2-03B-CPM-IMPORT-PROVEN', 'A central file MSBuild imports from outside the project ancestors is valid (K0, M), found after the interim review', [
        ('Allow otherwise legitimately effective central configurations, validated per project by MSBuild', 'K0 checkRepository and M checkProject: the static ancestor error stands only when MSBuild did not prove CPM on and a central file imported', 'DirectoryPackagesPropsPath layouts (one project, two projects, renamed file, nested Directory.Build.props): OK in all six; MSBuild imported true; NuGet NU1008 for a pinned project version'),
        ('Do not relax effective CPM enforcement', 'evaluator unchanged; no-SDK static fallback kept in K0 and M', 'plain Import (the review example), path to a missing file, CPM off, pinned project version, project outside the covered path: ERROR in all six; NuGet NU1015 for the plain Import'),
        ('Separate gated change, cumulative regression', 'own declaration; suite with 4 mutations; claims reworded (FG-K0-36395ffe06, FG-K0-73dd5d1170, FG-M-7f012a0fe2)', 'see the gate line above'),
        ('Registry restore', 'offline restore against an empty local feed only', 'NOT_RUN')]),
    ('Q-10 (approved semantics)', 'V3-Q10-PACKAGEVERSION-VERSION', 'A PackageVersion version is read as MSBuild reads it; a missing or empty one is an error (M1, K0, M)', [
        ('Within approved semantics only (DEP-006, DEP-003, PV2-03 invalid package metadata)', 'checker enforcement follows the existing NuGet text; no rule text changed', 'source checks: rule texts unchanged'),
        ('Missing or empty version rejected in all six', 'M1 missing-version error; K0 reads the child element and reports a missing version', 'no Version (root, nested), empty attribute, empty or self-closing child: ERROR in all six; NuGet NU1604'),
        ('Valid metadata accepted in all six', 'M and K0 read a Version child element before the attribute, as M1 does', 'Version child element 1.2.3: OK in all six; floating child element: ERROR in all six'),
        ('Separate gated change, cumulative regression', 'own declaration; suite with 4 mutations; the PV2-03 documented-difference row now requires ERROR in all six', 'see the gate line above')]),
]


def decision_matrix():
    t = ['# Approved decision implementation matrix (PV2-01 to PV2-04, and two corrections under approved semantics)\n', 'Authority: kit 74 Part B (approved in the task itself) and `Stage_A_Step2_Post_V2_Approved_Decisions_EN.md`. Each decision is one logical change with its own gate; checkpoints in `CHECKPOINTS/`, every attempt in `GATE_LOG.jsonl` and `GATE_ATTEMPTS/`.\n']
    for pid, change, title, items in DECISIONS:
        rows = read_jsonl(out_path('TEST_RESULTS', change + '.jsonl'))
        mine = Counter(r['status'] for r in rows if r['suite'] == change)
        allt = Counter(r['status'] for r in rows)
        cp = out_path('CHECKPOINTS', change + '.checkpoint.json')
        gate = read_json(cp)['gate'] if __import__('os').path.exists(cp) else 'NO CHECKPOINT'
        attempts = sum(1 for r in read_jsonl(out_path('GATE_LOG.jsonl')) if r['rule'] == change)
        t += ['## %s: %s' % (pid, title), '', 'Change `%s`. Gate: **%s** after %d attempt(s). Own suite: %d pass, %d fail, %d not run. Whole cumulative run at that gate: %d pass, %d fail, %d not run.' % (change, gate, attempts, mine['PASS'], mine['FAIL'], mine['NOT_RUN'], allt['PASS'], allt['FAIL'], allt['NOT_RUN']), '',
              '| Approved requirement | Implementation | Check and outcome |', '|---|---|---|']
        t += ['| %s | %s | %s |' % (a, b.replace('|', '/'), c) for a, b, c in items]
        t.append('')
    write_text('APPROVED_DECISION_IMPLEMENTATION_MATRIX.md', '\n'.join(t) + '\n')


def main():
    utf8_stdout()
    regression()
    decision_matrix()
    print(file_crosswalk())
    write_jsonl('UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl', QUEUE)
    print('queue', len(QUEUE))


if __name__ == '__main__':
    main()
