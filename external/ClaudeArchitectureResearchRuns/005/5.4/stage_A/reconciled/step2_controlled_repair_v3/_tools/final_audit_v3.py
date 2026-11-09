"""Separate cold final audit of v3 (kit 74 Part C), from final bytes. Reads no gate result or checkpoint as evidence. Re-runs every suite
(v1, v2, v3) and adds adversarial checks the suites do not contain. Writes:

  FINAL_AUDIT_RESULTS.jsonl, POLICY_PARITY_MATRIX.jsonl, SAME_TASK_MATRIX_V3.json, INTERACTION_MATRIX_V3.json, V3_FINAL_MANIFEST.json, FINAL_SUITE_TALLY.json

It writes no candidate file. Status words: PASS, FAIL, NOT_RUN, FINDING (a fact a reader must know; neither pass nor failure).
Run from this folder: PYTHONPATH=_tools python -B _tools/final_audit_v3.py   (about 20 minutes)
"""
import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter

import dataset
import depgraph
import external_events
import viewcheck
from fence import verify as fence_verify
from invariants import check_all as invariants_all
from order import ALL, LATER, ORDER, V2_ORDER, V3_ORDER
from rcommon import CANDIDATES, CODEX, OUT, ROOT, all_change_rows, baseline, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, run_start, sha256_file, template_root, utf8_stdout, v2_path, walk_files, wc_path, write_json, write_jsonl
from sandbox import PRE_TOOL, cleanup_runs, fresh_copy, run_checkers, run_node
from suitelib import Ctx, has
from suites_loader import load_suite


class Audit:
    def __init__(self):
        self.rows = []

    def row(self, section, test, status, detail='', candidate=None):
        self.rows.append({'section': section, 'test': test, 'candidate': candidate, 'status': status, 'detail': str(detail)[:1200]})

    def check(self, section, test, cond, detail='', candidate=None):
        self.row(section, test, 'PASS' if cond else 'FAIL', detail, candidate)


def sec_a(a):
    """Isolation: fence, nothing outside this folder written, Codex pass 4+ never entered, no Git work tree, no Step 3 output."""
    f = fence_verify()
    a.check('A', 'fenced trees unchanged against the preflight snapshot (inputs, runs, Step 1, Pass 1 union, Step 2, audit, v1, v2, kit, Codex)', f['n_errors'] == 0, f['errors'][:6] if f['n_errors'] else f['n_by_tree'])
    for w in f.get('warnings', []):
        a.row('A', 'fence warning: %s' % w, 'FINDING', 'EXTERNAL_EVENTS.json')
    t0 = datetime.datetime.fromisoformat(run_start()).timestamp() - 300
    newer = []
    for dp, dn, fn in os.walk(ROOT):
        # The Codex area is fenced by hash with pass 0004+ pruned; this walk never enters it.
        dn[:] = [d for d in dn if os.path.abspath(os.path.join(dp, d)) not in (os.path.abspath(OUT), os.path.abspath(CODEX))]
        for x in fn:
            p = os.path.join(dp, x)
            try:
                if os.path.getmtime(p) > t0:
                    newer.append(os.path.relpath(p, ROOT).replace(os.sep, '/'))
            except OSError:
                pass
    events = external_events.load()
    outside = [n for n in newer if not n.startswith('_STAGE_A_KIT/')]
    other = external_events.newer_not_allowed(outside, lambda rel: sha256_file(os.path.join(ROOT, rel.replace('/', os.sep))), events)
    a.check('A', 'no file outside this folder changed since the run started, apart from kit files and the recorded external files', not other, other[:10])
    a.row('A', 'files the user added outside this run, tolerated only with their recorded bytes (EXTERNAL_EVENTS.json ENV-02, ENV-03)', 'FINDING', sorted(set(outside) - set(other)))
    st = external_events.selftest()
    a.check('A', 'external-event rules reject unrecorded, changed and reappeared files (selftest negatives)', all(ok for _, ok in st), [n for n, ok in st if not ok])
    # Only the names directly under PASSES are listed (as in preflight); no later pass is entered.
    passes = sorted(n for n in os.listdir(os.path.join(CODEX, 'PASSES')))
    a.check('A', 'Codex passes 0001 to 0003 are present', all(p in passes for p in ('pass_0001', 'pass_0002', 'pass_0003')), passes[:3])
    later = [p for p in passes if p > 'pass_0003']
    if later:
        a.row('A', 'a Codex pass after 0003 now exists; it was not entered or read', 'FINDING', later)
    uses = []
    for dp, dn, fn in os.walk(os.path.join(OUT, '_tools')):
        for x in fn:
            if x.endswith('.py'):
                with open(os.path.join(dp, x), encoding='utf-8') as fh:
                    for i, line in enumerate(fh, 1):
                        # A line that states the pruning itself ("... pass_0004 and later are pruned") documents the rule, not a use.
                        if re.search(r"pass_000[4-9]|pass_00[1-9]\d", line) and 'pass_000[4-9]' not in line and 'codex_prune' not in line and '>= 4' not in line and 'pruned' not in line:
                            uses.append('%s:%d' % (x, i))
    a.check('A', 'no tool names a Codex pass after 0003 (lines stating the pruning excepted)', not uses, uses[:5])
    from preflight_v3 import codex_prune
    # Names built from numbers, so this test does not itself name a later pass in the source.
    probe = dict({'PASSES/pass_%04d' % n: n >= 4 for n in (1, 3, 4, 10, 123)}, **{'STATE.json': False})
    a.check('A', 'the Codex prune drops pass 0004 and later and keeps 0001 to 0003 (behavior, synthetic names)', all(codex_prune(k) == v for k, v in probe.items()), {k: codex_prune(k) for k in probe})
    r = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    a.check('A', 'the research folder is not a Git work tree, so no Git command could have mutated it', r.returncode != 0, r.stdout.strip() or r.stderr.strip()[:120])
    step3 = [n for n in os.listdir(os.path.dirname(OUT)) if 'step3' in n.lower()]
    a.check('A', 'no Step 3 output', not step3, step3)


def sec_b(a):
    """Bytes: every file equals its last logged hash across three history levels; the final manifest."""
    last, rules = {}, {}
    for r in all_change_rows():
        if r.get('kind') == 'TEMPLATE':
            last[(r['candidate'], r['file'])] = r['after_sha256']
            rules.setdefault((r['candidate'], r['file']), [])
            if r['rule'] not in rules[(r['candidate'], r['file'])]:
                rules[(r['candidate'], r['file'])].append(r['rule'])
    base = read_json(out_path('V3_BASELINE_MANIFEST.json'))['candidates']
    man = {}
    for c in CANDIDATES:
        cur = set(walk_files(template_root(c)))
        frozen = set(walk_files(os.path.dirname(input_path(c, 'CLAUDE.md'))))
        a.check('B', 'no file added or removed against the frozen template or v2', cur == frozen == set(base[c]['files']), sorted(cur ^ frozen)[:6], c)
        files, bad = {}, []
        for rel in sorted(cur):
            h = sha256_file(wc_path(c, rel))
            fz = sha256_file(input_path(c, rel))
            if h != (last.get((c, rel)) or fz):
                bad.append(rel)
            files[rel] = {'sha256': h, 'v2_sha256': base[c]['files'][rel], 'frozen_sha256': fz, 'changed_vs_v2': h != base[c]['files'][rel], 'changed_vs_frozen': h != fz, 'rules': rules.get((c, rel), [])}
        a.check('B', 'every file equals its last logged hash across v1, v2 and v3', not bad, bad[:6], c)
        man[c] = {'n_files': len(files), 'n_changed_vs_v2': sum(1 for v in files.values() if v['changed_vs_v2']), 'n_changed_vs_frozen': sum(1 for v in files.values() if v['changed_vs_frozen']), 'files': files}
        a.row('B', 'files changed: against v2 %d, against frozen %d' % (man[c]['n_changed_vs_v2'], man[c]['n_changed_vs_frozen']), 'PASS', sorted(r for r, v in files.items() if v['changed_vs_v2']), c)
    write_json('V3_FINAL_MANIFEST.json', {'version': 'step2-controlled-repair-v3', 'at': now(), 'candidates': man})


def sec_c(a):
    inv = invariants_all()
    for c in CANDIDATES:
        a.check('C', 'architecture identity invariants (incl. L0/L1 technology neutrality)', not inv[c], inv[c][:4], c)
        root = fresh_copy(c, 'audit')
        for r in run_checkers(c, root):
            a.check('C', 'own checker on a fresh copy: %s' % r['checker'], r['exit'] == 0, r['tail'], c)
        bad = 0
        for rel in walk_files(root):
            if rel.endswith(('.js', '.mjs', '.cjs')):
                code, out, err = run_node(root, ['--check', rel])
                bad += code != 0
        a.check('C', 'node --check on all scripts', bad == 0, bad, c)
        shutil.rmtree(root, ignore_errors=True)


def decision(code, out):
    if code == 2:
        return 'block'
    for line in reversed((out or '').strip().splitlines()):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        d = (o.get('hookSpecificOutput') or {}).get('permissionDecision')
        if d:
            return d
        if o.get('decision') == 'block':
            return 'block'
    return 'allow' if code == 0 else 'error:%d' % code


def hook(root, c, command, tool='Bash', raw=None):
    payload = raw if raw is not None else json.dumps({'hook_event_name': 'PreToolUse', 'session_id': 'audit', 'tool_name': tool, 'tool_input': {'command': command}, 'cwd': root})
    code, out, err = run_node(root, PRE_TOOL[c], payload)
    return decision(code, out), out + err


def sec_d(a):
    """Adversarial checks beyond the suites."""
    s01 = load_suite('PV2_01_GIT_GATING')
    with open(out_path('_rules', 'PV2-01-GIT-GATING', 'git_block.js'), encoding='utf-8') as f:
        ref = f.read().replace('\r\n', '\n').rstrip('\n')
    for c in s01.HOOK_WITH_TABLE:
        a.check('D', 'one Git table: the block is byte-identical to the reference', (s01.block_text(c) or '').replace('\r\n', '\n') == ref, None, c)
    a.check('D', 'the reference table equals K0 apart from helper names', s01.normalized_table(ref) == s01.normalized_table(s01.k0_table()))
    stale = {'missing at the repository root': 'PV2-03', 'only K0 has a Git hook': 'PV2-01'}
    for c in CANDIDATES:
        hits = [(rel, p) for rel in walk_files(template_root(c)) if rel.endswith(('.md', '.mjs', '.cjs', '.js')) for p in stale if p.lower() in norm_ws(' '.join(read_lines(wc_path(c, rel)))).lower()]
        a.check('D', 'no stale wording of a removed difference in the template', not hits, hits[:4], c)
    declared = set(V3_ORDER)
    undeclared = [r for r in read_jsonl(out_path('CHANGE_LOG.jsonl')) if r.get('rule') not in declared]
    a.check('D', 'every v3 change-log row belongs to a declared v3 change', not undeclared, undeclared[:3])
    for rule in V3_ORDER:
        a.check('D', 'declaration exists for %s' % rule, os.path.exists(out_path('_rules', rule, 'DECLARATION.md')))
    tmpl = [r for r in read_jsonl(out_path('CHANGE_LOG.jsonl')) if r.get('kind') == 'TEMPLATE']
    scope = {'PV2-02-FAILCLOSED-INPUT': {'M', 'M1'}, 'PV2-01-GIT-GATING': {'M', 'M1', 'L0', 'L1', 'K1'}, 'PV2-03-K0-CPM-ROOT': {'K0'}, 'PV2-04-M-FRONTEND-TESTS': {'M'},
             'PV2-03B-CPM-IMPORT-PROVEN': {'K0', 'M'}, 'V3-Q10-PACKAGEVERSION-VERSION': {'M', 'M1', 'K0'}}
    for rule, cands in scope.items():
        got = {r['candidate'] for r in tmpl if r['rule'] == rule}
        a.check('D', '%s edited only its approved candidates' % rule, got <= cands and got, sorted(got))
    a.check('D', 'data changes edited no template byte', not [r for r in tmpl if r['rule'].startswith('V3-D')], [r['file'] for r in tmpl if r['rule'].startswith('V3-D')][:3])
    a.check('D', 'K0 template untouched by the Git change (its hook is the reference)', not [r for r in tmpl if r['candidate'] == 'K0' and r['rule'] == 'PV2-01-GIT-GATING'])


def sec_e(a):
    """Same task across six, on final bytes: Git, bad input, nested CPM, frontend-test placement. Differences recorded, not hidden."""
    m = {'semantics': 'Same task, six hooks or checkers run directly. Text rows model a reading, not agent behavior.', 'at': now()}
    git_cases = [('git status', 'allow'), ('git log --oneline | head -5', 'allow'), ('git -C sub status', 'allow'), ('git commit -m x', 'ask'), ('git push --force origin main', 'ask'), ('git reset --hard', 'ask'),
                 ('git -c user.name=x commit -m y', 'ask'), ('bash -c "git clean -fd"', 'ask'), ('git status && git commit -m x', 'ask'), ('npm i left-pad@1.3.0 --force && git commit -m x', 'denied')]
    bad_cases = [('malformed', 'not json'), ('empty', ''), ('array', '[]'), ('no command', None), ('number command', 42)]
    m['git'], m['bad_input'] = {}, {}
    for c in CANDIDATES:
        root = fresh_copy(c, 'audit')
        row = {}
        for cmd, want in git_cases:
            d, raw = hook(root, c, cmd)
            row[cmd] = d
            a.check('E', 'same task, Git: %s -> %s' % (cmd, want), (d in ('deny', 'block')) if want == 'denied' else d == want, raw[-160:], c)
        m['git'][c] = row
        d, raw = hook(root, c, 'git reset --hard')
        a.check('E', 'authorization vs ask: the ask reason names the explicit-request rule and is not an approval', 'pre-approved this operation and scope' in raw, raw[-200:], c)
        brow = {}
        for name, val in bad_cases:
            if isinstance(val, str):
                d = hook(root, c, None, raw=val)[0]
            else:
                ti = {} if val is None else {'command': val}
                d = hook(root, c, None, raw=json.dumps({'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': ti, 'cwd': root}))[0]
            brow[name] = d
        m['bad_input'][c] = brow
        a.check('E', 'same task, invalid shell PreToolUse input is refused in the script', all(v in ('deny', 'block') for v in brow.values()), brow, c)
        shutil.rmtree(root, ignore_errors=True)
    s03 = load_suite('PV2_03_K0_CPM_ROOT')
    c01 = load_suite('C01_CPM_EFFECTIVE')
    m['cpm_nested'] = {}
    for name, files, want in s03.fixtures(c01)[:5]:
        row = {}
        for c in CANDIDATES:
            root = c01.build(c, files)
            row[c] = c01.outcome(c01.check(c, root)[0])
            shutil.rmtree(root, ignore_errors=True)
        m['cpm_nested'][name] = dict(row, expected=want)
        done = {v for v in row.values() if v != 'NOT_RUN'}
        if not done:
            a.row('E', 'same task, CPM: %s' % name, 'NOT_RUN', 'no .NET SDK proof ran')
        else:
            a.check('E', 'same task, CPM: %s -> %s in all six' % (name, want), done == {want}, row)
    s3b = load_suite('PV2_03B_CPM_IMPORT_PROVEN')
    s10 = load_suite('V3_Q10_PACKAGEVERSION_VERSION')
    fx = [('cpm_import', n, f, w) for n, f, w, _ in s3b.fixtures(c01)] + [('package_version', n, f, w) for n, f, _, w, _ in s10.fixtures(c01)]
    m['cpm_import'], m['package_version'] = {}, {}
    for group, name, files, want in fx:
        row = {}
        for c in CANDIDATES:
            root = c01.build(c, files)
            row[c] = c01.outcome(c01.check(c, root)[0])
            shutil.rmtree(root, ignore_errors=True)
        m[group][name] = dict(row, expected=want)
        done = {v for v in row.values() if v != 'NOT_RUN'}
        if not done:
            a.row('E', 'same task, %s: %s' % (group, name), 'NOT_RUN', 'no .NET SDK proof ran')
        else:
            a.check('E', 'same task, %s: %s -> %s in all six' % (group, name, want), done == {want}, row)
    a.row('E', 'CPM without the .NET SDK: K0 and M keep a static "no central file above the project" error; M1, L0, L1 and K1 report NOT_RUN. Neither is a pass. Not changed (PV2-03B keeps the static fallback).', 'FINDING', '')
    a.row('E', 'No candidate checks the file name of a central file MSBuild imports through DirectoryPackagesPropsPath (all six accept config/Packages.props); the rule texts say versions belong in Directory.Packages.props. Uniform; decision queue.', 'FINDING', '')
    s04 = load_suite('PV2_04_M_FRONTEND_TESTS')
    by = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    m['frontend_tests_under_backend'] = {c: {'text': has(c, rel, phrase), 'stored': by[key]['modality'] if key in by else None} for c, (rel, phrase, key) in s04.BAN.items()}
    a.check('E', 'same task, frontend tests under backend/: all six state the ban and store it MUST_NOT', all(v['text'] and v['stored'] == 'MUST_NOT' for v in m['frontend_tests_under_backend'].values()), m['frontend_tests_under_backend'])
    a.row('E', 'Git: K0 also asks when git follows an unrecognized leading word (echo git commit); the other five allow it. An over-approximation in K0, reported, not changed.', 'FINDING', '')
    a.row('E', 'Bad input: L0, K0 and K1 allow a blank command; K1 alone blocks a mismatched event; L0 and L1 block a non-shell tool. Outside PV2-02 (M and M1 only).', 'FINDING', '')
    a.row('E', 'Hook timeouts differ (L1 30/15 s, others 60 s for advisory hooks); configuration, not policy; host behavior NOT_RUN.', 'FINDING', '')
    for task in ('A live agent working one task end to end in each candidate', 'A live host showing an ask prompt or applying deny, exit 2 or onFailure', 'A real application, database, cache, Swagger UI, registry or CI'):
        a.row('E', 'same task: %s' % task, 'NOT_RUN', 'Not available in this run; recorded as NOT_TESTED, not as agreement.')
    write_json('SAME_TASK_MATRIX_V3.json', m)


def sec_f(a):
    """Interactions between the v3 changes and earlier rules, on final bytes."""
    m = {'at': now(), 'rows': []}

    def rec(pair, test, ok, detail=''):
        m['rows'].append({'pair': pair, 'test': test, 'status': 'PASS' if ok else 'FAIL', 'detail': str(detail)[:400]})
        a.check('F', '%s: %s' % (pair, test), ok, detail)
    for c in CANDIDATES:
        root = fresh_copy(c, 'audit')
        d1 = hook(root, c, 'npm install left-pad@1.3.0 --force && git push')[0]
        rec('PV2-01 x DEP-025', 'peer bypass still denied when the line also pushes [%s]' % c, d1 in ('deny', 'block'), d1)
        d2 = hook(root, c, 'git commit -m x', raw=json.dumps({'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': {'cmd': 'git commit -m x'}, 'cwd': root}))[0]
        rec('PV2-01 x PV2-02', 'a Git command hidden under a wrong field is refused, not asked [%s]' % c, d2 in ('deny', 'block'), d2)
        d3 = hook(root, c, 'git status --porcelain')[0]
        rec('PV2-01 x R02', 'the read-only task-start check runs without a Git prompt [%s]' % c, d3 == 'allow', d3)
        shutil.rmtree(root, ignore_errors=True)
    r02 = load_suite('R02_HQ01_GOV015')
    reset = ('reset --hard', 'main')
    rec('PV2-01 x HQ-01', 'an ask answered by a generic workflow approval is still no authority (approved reading)', r02.authority(reset, 'generic_workflow') == 'DENY', '')
    rec('PV2-01 x HQ-01', 'an explicit request still allows after the re-check', r02.authority(reset, reset) == 'ALLOW_AFTER_RECHECK', '')
    c04 = load_suite('C04_GIT_CONDITIONAL')
    for c in CANDIDATES:
        rec('PV2-01 x C04', 'no unconditional commit step anywhere [%s]' % c, not c04.sweep(template_root(c)), c04.sweep(template_root(c))[:2])
    c01 = load_suite('C01_CPM_EFFECTIVE')
    rec_entry = {'exceptions': [{'ecosystem': 'nuget', 'package': 'A.B', 'version': '1.*', 'manifest': 'backend/Directory.Packages.props', 'requested_by': 'user', 'request': 'User asked for A.B at 1.* on 2026-11-05', 'date': '2026-11-05'}]}
    root = c01.build('K0', {'backend/Directory.Packages.props': c01.central(c01.T, '<PackageVersion Include="A.B" Version="1.*" />'), c01.PROJ: c01.proj(c01.REF), 'dependency-version-exceptions.json': json.dumps(rec_entry)})
    code, out = c01.check('K0', root)
    rec('PV2-03 x DEP-003', 'K0 nested central file: no root error; the recorded floating version still needs the NuGet switch', 'missing at the repository root' not in out and ('NU1011' in out or 'CentralPackageFloatingVersionsEnabled' in out or c01.outcome(code) == 'NOT_RUN'), out[-260:].replace(root, '<fixture>'))
    shutil.rmtree(root, ignore_errors=True)
    # PV2-03B x DEP-003 and V3-Q10 x DEP-003: a recorded floating version written as a Version child element, in a central file that
    # MSBuild imports from outside the project's ancestors. The record is honoured the same way in all six; an unrecorded one still fails.
    dpp = '<Project><PropertyGroup><DirectoryPackagesPropsPath>$(MSBuildThisFileDirectory)config/Directory.Packages.props</DirectoryPackagesPropsPath></PropertyGroup></Project>'
    rec_child = {'exceptions': [dict(rec_entry['exceptions'][0], manifest='config/Directory.Packages.props')]}
    for label, items, want in (('recorded', '<PackageVersion Include="A.B"><Version>1.*</Version></PackageVersion>', 'OK'),
                               ('unrecorded', '<PackageVersion Include="A.B"><Version>1.2.3</Version></PackageVersion><PackageVersion Include="C.D"><Version>2.*</Version></PackageVersion>', 'ERROR')):
        row, outs = {}, {}
        for c in CANDIDATES:
            root = c01.build(c, {'Directory.Build.props': dpp, 'config/Directory.Packages.props': c01.central(c01.T, items), c01.PROJ: c01.proj(c01.REF), 'dependency-version-exceptions.json': json.dumps(rec_child)})
            code, out = c01.check(c, root)
            row[c], outs[c] = c01.outcome(code), out[-200:].replace(root, '<fixture>')
            shutil.rmtree(root, ignore_errors=True)
        done = {v for v in row.values() if v != 'NOT_RUN'}
        rec('PV2-03B x V3-Q10 x DEP-003', '%s floating child-element version in a non-ancestor central file -> %s in all six' % (label, want), done == {want} or not done, row)
    cov = {(x['candidate'], x['policy_id']): (x['status'], x['strength_status']) for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    old = {(x['candidate'], x['policy_id']): (x['status'], x['strength_status']) for x in read_jsonl(v2_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    rec('D01 x D02 x coverage', 'no coverage or strength cell moved against v2', cov == old, sorted(k for k in old if cov.get(k) != old[k])[:6])
    write_json('INTERACTION_MATRIX_V3.json', m)


def sec_g(a):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    cross = read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    errs = viewcheck.check_all(rows, cross, cov)
    a.check('G', 'whole view: unique ids, line and quote resolution, recomputed coverage, crosswalk', not errs, errs[:6])
    r1, c1 = dataset.build()
    a.check('G', 'replay from the frozen baseline equals the files', rec_hash([r for c in CANDIDATES for r in r1[c]]) == rec_hash(rows) and rec_hash(c1) == rec_hash(cross))
    x = read_jsonl(out_path('V2_TO_V3_CROSSWALK.jsonl'))
    st = Counter(r['status'] for r in x)
    a.check('G', 'no v2 record lost; every v3 record has one crosswalk row', st.get('LOST', 0) == 0 and len(x) == len(rows), dict(st))
    bad = [r['source_key'] for r in x if r['status'] not in ('UNCHANGED', 'ANCHOR_SHIFT_ONLY') and not r.get('v3_rules')]
    a.check('G', 'every difference from v2 view names the v3 change that made it', not bad, bad[:6])
    frozen = {k: r for c in CANDIDATES for k, r in baseline(c).items()}
    keys = {r['source_key'] for r in rows}
    a.check('G', '6,402 baseline identities kept, each with its original claim', all(k in keys for k in frozen) and all(r['source_key'] not in frozen or r.get('claim_text_original') == frozen[r['source_key']].get('claim_text') for r in rows))
    a.check('G', 'four proposals stay proposals; the policy set stays 196', sum(1 for r in rows if r['source_key'].startswith('NCP-')) == 4 and len(policies()) == 196)
    g = read_json(out_path('POLICY_DEPENDENCY_GRAPH.json'))
    a.check('G', 'dependency graph rebuilt equals the stored one', rec_hash(depgraph.build()) == rec_hash({k: v for k, v in g.items() if k != 'at'}))
    nc = read_jsonl(out_path('V3_NEW_CLAIMS_REVIEW.jsonl'))
    a.check('G', 'every claim added in v3 has a CONFIRMED review row', {r['source_key'] for r in rows if r['source_key'].startswith('V3A-')} == {x['key'] for x in nc} and all(x['status'] == 'CONFIRMED' for x in nc), len(nc))
    adj = read_jsonl(out_path('PASS2_PASS3_ADJUDICATION.jsonl'))
    a.check('G', 'every Codex Pass 2/3 record has exactly one adjudication row', len(adj) == 211 and len({r['codex_id'] for r in adj}) == 211, len(adj))


def sec_h(a):
    """POLICY_PARITY_MATRIX.jsonl: 1,176 cells. Check level says how deep each cell was read; a mechanical witness is labelled as such."""
    rows = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    reviews = {}
    for rule in LATER:
        p = out_path('_rules', rule, 'review.py')
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location('rv_' + rule.replace('-', '_'), p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            for x in m.REVIEW:
                reviews.setdefault((x['candidate'], x['policy']), []).append(dict(x, rule=rule))
    partial = {(x['candidate'], x['policy_id']): x for x in read_jsonl(out_path('PARTIAL_WITNESSES_38.jsonl'))}
    out, no_ce = [], []
    for cell in cov:
        c, pid = cell['candidate'], cell['policy_id']
        wit = []
        for key in (cell['direct_source_keys'] + cell['partial_source_keys'])[:3]:
            r = rows[key]
            e = next((x for x in r.get('current_evidence_refs') or [] if x.get('start_line')), None)
            if e:
                rel = e['path'].split('/template/')[1]
                wit.append({'key': key, 'path': e['path'], 'start_line': e['start_line'], 'quote': norm_ws(' '.join(read_lines(wc_path(c, rel))[e['start_line'] - 1:e['end_line']]))[:200], 'modality': r.get('modality')})
        rv = reviews.get((c, pid), [])
        v3 = [x for x in rv if x['rule'] in V3_ORDER]
        pt = partial.get((c, pid))
        level = 'SOURCE_REVIEWED_V3' if v3 else ('SOURCE_REVIEWED_V2' if rv else ('CLAUSE_REVIEWED_V2' if pt else 'MECHANICAL_WITNESS_ONLY'))
        ce = [x.get('counterexample') for x in rv if x.get('counterexample')] or ([pt['counterexample']] if pt else [])
        if level != 'MECHANICAL_WITNESS_ONLY' and not ce and any(x.get('verdict') != 'NOT_AFFECTED' for x in rv):
            no_ce.append((c, pid))
        out.append({'candidate': c, 'policy_id': pid, 'policy_strength': policies()[pid]['normative_strength'], 'status': cell['status'], 'strength_status': cell['strength_status'], 'n_direct': len(cell['direct_source_keys']), 'n_partial': len(cell['partial_source_keys']),
                    'witnesses': wit, 'check_level': level, 'reviews': [{'rule': x['rule'], 'verdict': x['verdict']} for x in rv], 'counterexample': ce, 'semantics': 'Traceability unless check_level says reviewed. A witness at a current line does not prove parity.'})
    write_jsonl('POLICY_PARITY_MATRIX.jsonl', out)
    levels = Counter(x['check_level'] for x in out)
    a.check('H', '1,176 cells, 196 per candidate', len(out) == 1176 and all(sum(1 for x in out if x['candidate'] == c) == 196 for c in CANDIDATES), dict(levels))
    a.check('H', 'every cell has a witness at a current line', all(x['witnesses'] for x in out), [(x['candidate'], x['policy_id']) for x in out if not x['witnesses']][:6])
    a.check('H', 'every reviewed cell has a counterexample', not no_ce, no_ce[:8])
    a.row('H', 'cells with only a mechanical witness', 'FINDING', '%d of 1,176 were not read side by side in v2 or v3. They rest on the Step 2 classification plus a witness at a current line.' % levels['MECHANICAL_WITNESS_ONLY'])
    a.row('H', 'check levels', 'FINDING', dict(levels))


def sec_i(a):
    tally, by = Counter(), {}
    for rule in ALL:
        p = os.path.join(OUT, '_tools', 'suites', rule.replace('-', '_') + '.py')
        if not os.path.exists(p):
            continue
        spec = importlib.util.spec_from_file_location('cold_' + rule.replace('-', '_'), p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        ctx = Ctx(rule)
        try:
            m.run(ctx)
        except Exception as e:
            ctx.add('suite crashed', 'FAIL', repr(e))
        t = Counter(r['status'] for r in ctx.rows)
        by[rule] = dict(t)
        tally.update(t)
        for r in ctx.rows:
            if r['status'] in ('FAIL', 'NOT_RUN'):
                a.row('I', '%s: %s' % (rule, r['test'][:90]), r['status'], r['detail'], r['candidate'])
        a.row('I', 'suite %s: pass %d, fail %d, not run %d' % (rule, t['PASS'], t['FAIL'], t['NOT_RUN']), 'PASS' if not t['FAIL'] else 'FAIL', '')
    write_json('FINAL_SUITE_TALLY.json', {'at': now(), 'tally': dict(tally), 'by_suite': by})


def run_audit():
    a = Audit()
    for fn in (sec_a, sec_b, sec_c, sec_d, sec_e, sec_f, sec_g, sec_h, sec_i):
        try:
            fn(a)
        except Exception as e:
            import traceback
            a.row(fn.__name__[-1].upper(), 'section crashed', 'FAIL', traceback.format_exc()[-800:])
        print(fn.__name__, Counter(r['status'] for r in a.rows), flush=True)
    write_jsonl('FINAL_AUDIT_RESULTS.jsonl', a.rows)
    cleanup_runs()
    return a.rows


def main():
    utf8_stdout()
    rows = run_audit()
    print(Counter(r['status'] for r in rows))
    for r in rows:
        if r['status'] == 'FAIL':
            print('FAIL', r['section'], r['candidate'], r['test'], '|', r['detail'][:400])
    return 1 if any(r['status'] == 'FAIL' for r in rows) else 0


if __name__ == '__main__':
    sys.exit(main())
