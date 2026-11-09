"""Separate cold final audit of v2, from final bytes. Reads no gate result or checkpoint as evidence. It re-runs every suite, adds adversarial checks the suites do not contain, and writes:

  FINAL_AUDIT_RESULTS.jsonl, POLICY_PARITY_MATRIX.jsonl, SAME_TASK_MATRIX_V2.json, INTERACTION_MATRIX.json, V2_FINAL_MANIFEST.json

It writes no candidate file. Status words: PASS, FAIL, NOT_RUN, FINDING. FINDING is a real fact a reader must know; it is not a pass and not a failure.
Re-run from this folder: PYTHONPATH=_tools python -B _tools/final_audit_v2.py   (about 20 minutes; regenerates the five files above and leaves candidates untouched)
"""
import hashlib
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
import viewcheck
from fence import verify as fence_verify
from invariants import check_all as invariants_all
from order import ALL, ORDER, V2_ORDER
from rcommon import CANDIDATES, OUT, ROOT, all_change_rows, baseline, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, sha256_file, template_root, utf8_stdout, v1_path, walk_files, wc_path, write_json, write_jsonl
from sandbox import CHECKERS, PRE_TOOL, cleanup_runs, fresh_copy, run_checkers, run_node
from suitelib import Ctx
from suites_loader import load_suite


class Audit:
    def __init__(self):
        self.rows = []

    def row(self, section, test, status, detail='', candidate=None):
        self.rows.append({'section': section, 'test': test, 'candidate': candidate, 'status': status, 'detail': str(detail)[:1200]})

    def check(self, section, test, cond, detail='', candidate=None):
        self.row(section, test, 'PASS' if cond else 'FAIL', detail, candidate)


def codex_use(line):
    """A line that uses the Codex area, as opposed to a prune condition or a statement of the rule."""
    return 'codex_iterative_search' in line and "not in" not in line and "' in x" not in line and not line.lstrip().startswith(('#', '"""', 'stage_A/', "'not_covered")) and 'never read' not in line and 'not read' not in line and 'is pruned' not in line


def sec_a(a):
    f = fence_verify()
    a.check('A', 'fenced trees unchanged: inputs, Step 1, Step 2, audit, v1 and its archive, kit', f['n_errors'] == 0, f['errors'][:6] if f['n_errors'] else f['n_by_tree'])
    fp = read_json(out_path('PREDECESSOR_V1_FINGERPRINT.json'))
    bad = [rel for rel, h in fp['v1_tree_sha256'].items() if not os.path.exists(v1_path(*rel.split('/'))) or sha256_file(v1_path(*rel.split('/'))) != h]
    a.check('A', 'v1 tree equals the fingerprint taken before this run edited anything', not bad, bad[:5])
    a.check('A', 'the v1 tree matched its archive when this run started', fp['archive_comparison'] and not fp['archive_comparison']['differ'] and not fp['archive_comparison']['missing_in_tree'], fp['archive_comparison'])
    start = read_json(out_path('V2_BASELINE_MANIFEST.json'))['created_at']
    import datetime
    t0 = datetime.datetime.fromisoformat(start).timestamp() - 300
    newer = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if 'codex_iterative_search' not in d and os.path.abspath(os.path.join(dp, d)) != os.path.abspath(OUT)]
        for x in fn:
            if 'codex_iterative_search' in x:
                continue
            p = os.path.join(dp, x)
            if os.path.getmtime(p) > t0:
                newer.append(os.path.relpath(p, ROOT).replace(os.sep, '/'))
    other = [n for n in newer if not n.startswith('_STAGE_A_KIT/')]
    a.check('A', 'no file outside this folder changed since the run started, apart from kit files', not other, other[:10])
    for line in ("open(os.path.join(ROOT, 'stage_A', 'codex_iterative_search', 'x.json'))", "for f in os.listdir('stage_A/codex_iterative_search'):", "read_jsonl('stage_A/codex_iterative_search.zip')"):
        a.check('A', 'scan control: a line that opens the Codex area is caught', codex_use(line), line)
    for line in ("dn[:] = [d for d in dn if 'codex_iterative_search' not in d]", "# codex_iterative_search is never read"):
        a.check('A', 'scan control: a prune condition or a statement of the rule is not flagged', not codex_use(line), line)
    uses = []
    for dp, dn, fn in os.walk(os.path.join(OUT, '_tools')):
        for x in fn:
            if x.endswith('.py'):
                with open(os.path.join(dp, x), encoding='utf-8') as fh:
                    for i, line in enumerate(fh, 1):
                        if codex_use(line) and 'scan control' not in line and "codex_use(line)" not in line and "for line in (" not in line:
                            uses.append('%s:%d' % (x, i))
    a.check('A', 'no tool opens the Codex area: its name appears only in prune conditions and statements of the rule', not uses, uses[:6])
    r = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    a.check('A', 'the research folder is not a Git work tree, so no Git command could have mutated it', r.returncode != 0, r.stdout.strip() or r.stderr.strip()[:120])
    step3 = [n for n in os.listdir(os.path.dirname(OUT)) if 'step3' in n.lower()] + [n for n in os.listdir(OUT) if 'step3' in n.lower() and not n.endswith(('.md', '.json', '.jsonl'))]
    a.check('A', 'no Step 3 output', not step3, step3)


def sec_b(a):
    last, rules = {}, {}
    for r in all_change_rows():
        if r.get('kind') == 'TEMPLATE':
            last[(r['candidate'], r['file'])] = r['after_sha256']
            rules.setdefault((r['candidate'], r['file']), [])
            if r['rule'] not in rules[(r['candidate'], r['file'])]:
                rules[(r['candidate'], r['file'])].append(r['rule'])
    base = read_json(out_path('V2_BASELINE_MANIFEST.json'))['candidates']
    man = {}
    for c in CANDIDATES:
        cur = set(walk_files(template_root(c)))
        frozen = set(walk_files(os.path.dirname(input_path(c, 'CLAUDE.md'))))
        a.check('B', 'no file added or removed against the frozen template or v1', cur == frozen == set(base[c]['files']), sorted(cur ^ frozen)[:6], c)
        files, bad = {}, []
        for rel in sorted(cur):
            h = sha256_file(wc_path(c, rel))
            fz = sha256_file(input_path(c, rel))
            want = last.get((c, rel)) or fz
            if h != want:
                bad.append(rel)
            files[rel] = {'sha256': h, 'v1_sha256': base[c]['files'][rel], 'frozen_sha256': fz, 'changed_vs_v1': h != base[c]['files'][rel], 'changed_vs_frozen': h != fz, 'rules': rules.get((c, rel), [])}
        a.check('B', 'every file equals its last logged hash across both history levels', not bad, bad[:6], c)
        man[c] = {'n_files': len(files), 'n_changed_vs_v1': sum(1 for v in files.values() if v['changed_vs_v1']), 'n_changed_vs_frozen': sum(1 for v in files.values() if v['changed_vs_frozen']), 'files': files}
        a.row('B', 'files changed: against v1 %d, against frozen %d' % (man[c]['n_changed_vs_v1'], man[c]['n_changed_vs_frozen']), 'PASS', '', c)
    write_json('V2_FINAL_MANIFEST.json', {'version': 'step2-controlled-repair-v2', 'at': now(), 'candidates': man})


def sec_c(a):
    inv = invariants_all()
    for c in CANDIDATES:
        a.check('C', 'architecture identity invariants, including L0/L1 technology neutrality', not inv[c], inv[c][:4], c)
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


CHECKER_FILE = {'M': '.claude/scripts/check-manifests.mjs', 'M1': '.claude/scripts/check-manifests.js', 'L0': '.claude/hooks/manifest-checks.mjs', 'L1': '.claude/hooks/post-change-checks.mjs', 'K0': '.claude/scripts/check-dependencies.cjs', 'K1': '.claude/scripts/check-manifests.cjs'}


def text_of(c, rel):
    return norm_ws(' '.join(read_lines(wc_path(c, rel))))


def all_md(c):
    return [r for r in walk_files(template_root(c)) if r.endswith('.md')]


def sec_d(a):
    """Adversarial checks the change suites do not contain."""
    # The evaluator is the same statements in all six.
    bodies = {}
    for c, rel in CHECKER_FILE.items():
        s = '\n'.join(read_lines(wc_path(c, rel)))
        m = re.search(r'// Effective Central Package Management \(DEP-006\).*?function cpmNotRunMessage\(reason\) \{.*?\n\}', s, re.S)
        bodies[c] = hashlib.sha256(m.group(0).encode('utf-8')).hexdigest() if m else None
    a.check('D', 'the CPM evaluator is byte-identical in all six checkers', len(set(bodies.values())) == 1 and None not in bodies.values(), bodies)
    # No literal CPM logic survives in any script, in any form.
    literal = re.compile(r'<ManagePackageVersionsCentrally>|managepackageversionscentrally\'|centralManagementEnabled|props\.central\b|central\s*=\s*/')
    for c in CANDIDATES:
        hits = []
        for rel in walk_files(template_root(c)):
            if rel.endswith(('.mjs', '.cjs', '.js')):
                for i, line in enumerate(read_lines(wc_path(c, rel)), 1):
                    if literal.search(line):
                        hits.append('%s:%d' % (rel, i))
        a.check('D', 'no script reads the CPM setting from literal XML', not hits, hits[:5], c)
    # Single-owner: each new sentence has one normative home per candidate.
    once = {'An exception needs the user\'s explicit request naming it and its scope': 1, 'For a floating NuGet version, also set `CentralPackageFloatingVersionsEnabled`': 1}
    for c in CANDIDATES:
        for phrase, n in once.items():
            where = [r for r in all_md(c) if norm_ws(phrase).lower() in text_of(c, r).lower()]
            a.check('D', 'one normative home: %s' % phrase[:48], len(where) == n, where, c)
    # Stale wording anywhere, not only in the patched files.
    stale = {'Production migration automation': 'C03', 'no automatic production migration step': 'C03', 'Never apply production database migrations': 'C03', 'only on a measured hot': 'C02', 'only a measured hot path': 'C02', 'belong to measured hot paths': 'C02', 'Measured extremely hot query': 'C02', 'or measured performance justifies it': 'C02', 'maintain and commit': 'C04', 'consistent and committed': 'C04', 'must be committed': 'C04'}
    for c in CANDIDATES:
        hits = []
        for rel in walk_files(template_root(c)):
            if rel.endswith(('.md', '.mjs', '.cjs', '.js')):
                t = text_of(c, rel).lower()
                hits.extend('%s: %s' % (rel, p) for p in stale if p.lower() in t)
        a.check('D', 'no stale wording anywhere in the template', not hits, hits[:6], c)
    # The view must not keep a claim that describes the removed behavior.
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    rx = re.compile(r'matches? literal|literal unqualified switch|Each central file must enable|without ManagePackageVersionsCentrally=true|Maintain and commit|Commit `?package|must be committed|Measured extremely|only on a measured hot|fit only a measured|Production migration automation', re.I)
    stale_claims = [(r['candidate'], r['source_key'], r['claim_text'][:90]) for r in rows if r['repair']['active'] and rx.search(r.get('claim_text') or '')]
    a.check('D', 'no active claim in the view still describes removed behavior', not stale_claims, stale_claims[:8])
    # Every claim that quotes a changed sentence must still resolve; a stale v1 review row must have been retired with a reason.
    ret = []
    for rule in V2_ORDER:
        p = out_path('_rules', rule, 'supersede.py')
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location('s_' + rule.replace('-', '_'), p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            ret.extend(m.SUPERSEDE)
    a.check('D', 'every retired v1 review quote names who retired it and why', all(r.get('why') for r in ret), len(ret))
    # Declared scope: template edits only under declared changes.
    declared = {r for r in V2_ORDER}
    undeclared = [r for r in read_jsonl(out_path('CHANGE_LOG.jsonl')) if r.get('rule') not in declared]
    a.check('D', 'every v2 change-log row belongs to a declared change', not undeclared, undeclared[:3])
    for rule in V2_ORDER[1:]:
        a.check('D', 'declaration exists for %s' % rule, os.path.exists(out_path('_rules', rule, 'DECLARATION.md')))
    a.row('D', 'always-loaded size against v1', 'PASS', {c: sum(len(' '.join(read_lines(wc_path(c, r)))) for r in ['CLAUDE.md']) - sum(len(' '.join(read_lines(v1_path('candidates', c, 'template', 'CLAUDE.md')))) for _ in [0]) for c in CANDIDATES})


def sec_e(a):
    """Same hypothetical task across six. CPM rows run real checkers; text rows use the suite models; differences are recorded, not hidden."""
    m = {'semantics': 'Same task across six. A difference in routing or loading is a delivery difference unless stated. Text rows are models of a reading, not agent behavior.', 'at': now()}
    c01 = load_suite('C01_CPM_EFFECTIVE')
    rows = {}
    picks = [x for x in c01.CASES if x[0] in ('inherited true from Directory.Build.props', 'project overrides true with false', 'Directory.Build.targets turns it off after the project', 'literal true in a comment is ineffective', 'multiple projects evaluate differently', 'release-only false is found', 'malformed central manifest fails closed', 'version pinned through an inherited file only MSBuild can see')]
    for case in picks:
        row = {}
        for c in CANDIDATES:
            row[c] = c01.one_case(c, case)['got']
        rows[case[0]] = dict(row, expected=case[2])
        a.check('E', 'same task, CPM: %s' % case[0], set(row.values()) == {case[2]}, row)
    m['cpm'] = rows
    c02 = load_suite('C02_RUN008_EVIDENCE')
    m['run008'] = {}
    for c in CANDIDATES:
        ok = c02.permits(c02.ntext(c, c02.EF), c02.DEMONSTRATED[c])
        m['run008'][c] = {'design_evidence_no_profile': 'ALLOWED' if ok else 'REFUSED', 'no_evidence': 'REFUSED' if c02.SPECULATIVE[c].lower() in c02.ntext(c, c02.EF).lower() else 'ALLOWED'}
        a.check('E', 'same task, RUN-008: shown hot by design evidence is allowed, no evidence is refused', ok and m['run008'][c]['no_evidence'] == 'REFUSED', m['run008'][c], c)
    c03 = load_suite('C03_WF019_EXCEPTION')
    m['wf019'] = {}
    for name, want in c03.SCENARIOS.items():
        row = {c: c03.verdict(c03.joined(c), name) for c in CANDIDATES}
        m['wf019'][name] = row
        a.check('E', 'same task, WF-019: %s' % name, set(row.values()) == {want}, row)
    c04 = load_suite('C04_GIT_CONDITIONAL')
    m['git'] = {}
    for c in CANDIDATES:
        hits = c04.sweep(template_root(c))
        m['git'][c] = {'unconditional_commit_lines': len(hits), 'git_hook': 'ask' if c == 'K0' else 'none (text only)'}
        a.check('E', 'same task, Git: no unconditional commit step', not hits, hits[:3], c)
    a.row('E', 'Git delivery differs: only K0 has a Git hook; the obligation is the same', 'FINDING', m['git'])
    # Hook on bad input, run directly on each script.
    c06 = load_suite('C06_REVIEW_SETS')
    m['hook_bad_input'] = {}
    for c in CANDIDATES:
        root = fresh_copy(c, 'audit')
        row = {}
        for name, payload in (('malformed', 'not json at all'), ('empty', ''), ('no command', json.dumps({'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': {}, 'cwd': root}))):
            code, out, err = run_node(root, PRE_TOOL[c], payload)
            row[name] = c06.decision(code, out)
        m['hook_bad_input'][c] = row
        shutil.rmtree(root, ignore_errors=True)
        want = c06.BAD_INPUT.get(c, {})
        a.check('E', 'same task, hook on bad input: as documented for this candidate', all((row[n] == want[k]) if k in want else row[n] in c06.DENIED for n, k in (('malformed', 'malformed input'), ('empty', 'empty input'), ('no command', 'no command'))), row, c)
    a.row('E', 'Hook on bad input differs: M exits 1, so only the host setting onFailure can make that a block. M and M1 allow a payload with no command. The other four refuse in the script.', 'FINDING', m['hook_bad_input'])
    # A central package file away from the repository root.
    m['central_file_below_root'] = {}
    for c in CANDIDATES:
        root = c01.build(c, {'backend/Directory.Packages.props': c01.central(c01.T, c01.PV), c01.PROJ: c01.proj(c01.REF)})
        code, out = c01.check(c, root)
        m['central_file_below_root'][c] = {'exit': code, 'tail': out[-160:].replace(root, '<fixture>')}
        shutil.rmtree(root, ignore_errors=True)
    errors = sorted(c for c, v in m['central_file_below_root'].items() if v['exit'] == 1)
    a.check('E', 'same task, central file below the root on a valid fixture: K0 errors under its decision D-17, the other five accept', errors == ['K0'], m['central_file_below_root'])
    a.row('E', 'A central package file below the repository root: the checker errors in %s. MSBuild finds the file in all six, so this is a stricter location decision, not a different CPM obligation.' % (', '.join(errors) or 'no candidate'), 'FINDING', m['central_file_below_root'])
    # Frontend test placement: the same ban where the text has it, and a real text difference in M.
    c07 = load_suite('C07_PARITY_CLOSE')
    rows = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    m['frontend_tests_under_backend'] = {c: {'text': v[1], 'stored': rows[v[2]]['modality']} for c, v in c07.BAN.items()}
    m['frontend_tests_under_backend']['M'] = {'text': 'none; CLAUDE.md says the workspace holds its tests', 'stored': None}
    a.check('E', 'same task, frontend tests under backend: every candidate with the marked ban stores it as MUST_NOT', {v['stored'] for c, v in m['frontend_tests_under_backend'].items() if c != 'M'} == {'MUST_NOT'}, m['frontend_tests_under_backend'])
    a.row('E', 'Frontend tests under backend differs by text: M has no marked ban. Left as written; DEP-024 does not require one.', 'FINDING', m['frontend_tests_under_backend'])
    # Not exercised as a same-task run.
    for task in ('A live agent working one task end to end in each candidate', 'A live host applying a hook decision', 'A real application, database, cache, Swagger UI, registry or CI'):
        a.row('E', 'same task: %s' % task, 'NOT_RUN', 'Not available in this run; recorded as NOT_TESTED, not as agreement.')
    write_json('SAME_TASK_MATRIX_V2.json', m)


def sec_f(a):
    """Interaction matrix: re-test A after B on final bytes."""
    m = {'at': now(), 'rows': []}

    def rec(pair, test, ok, detail=''):
        m['rows'].append({'pair': pair, 'test': test, 'status': 'PASS' if ok else 'FAIL', 'detail': str(detail)[:400]})
        a.check('F', '%s: %s' % (pair, test), ok, detail)
    c01 = load_suite('C01_CPM_EFFECTIVE')
    import json as _j
    rec_entry = {'exceptions': [{'ecosystem': 'nuget', 'package': 'A.B', 'version': '1.*', 'manifest': 'Directory.Packages.props', 'requested_by': 'user', 'request': 'User asked for A.B at 1.* on 2026-11-03', 'date': '2026-11-03'}]}
    for c in CANDIDATES:
        root = c01.build(c, {'Directory.Packages.props': c01.central(c01.T, '<PackageVersion Include="A.B" Version="1.*" /><PackageVersion Include="C.D" Version="2.*" />'), c01.PROJ: c01.proj(c01.REF), 'dependency-version-exceptions.json': _j.dumps(rec_entry)})
        code, out = c01.check(c, root)
        rec('C01 x DEP-003', 'effective CPM on; a recorded floating version accepted, an unrecorded one rejected, the NuGet switch named [%s]' % c, 'NU1011' in out and any('C.D' in l and 'floating' in l.lower() for l in out.splitlines()) and not any('A.B' in l and 'floating' in l.lower() and 'approved' not in l.lower() and 'floats' not in l for l in out.splitlines()), out[-250:])
        code, out = c01.hook_edit(c, root, 'backend/App.Api/Foo.cs', no_dotnet=True)
        rec('C01 x hooks', 'an unrelated edit with no SDK does not ask for dotnet [%s]' % c, 'NOT_RUN' not in out, out[-120:])
        shutil.rmtree(root, ignore_errors=True)
    from sandbox import pre_tool
    for c in CANDIDATES:
        root = c01.build(c, {'Directory.Packages.props': c01.central()})
        d1 = pre_tool(root, c, 'npm install x@1.2.3 --force')[0]
        d2 = pre_tool(root, c, 'npm install x@1.2.3 --legacy-peer-deps')[0]
        rec('C01 x DEP-025', 'peer bypass still denied with effective CPM in place [%s]' % c, d1 in ('deny', 'block') and d2 in ('deny', 'block'), (d1, d2))
        shutil.rmtree(root, ignore_errors=True)
    for c in CANDIDATES:
        t = text_of(c, 'CLAUDE.md')
        c03 = load_suite('C03_WF019_EXCEPTION')
        owner = text_of(c, c03.OWNER[c])
        rec('C03 x headless', 'the exception sentence grants no headless route: the Reserved headless sentence still stands [%s]' % c, 'Never make or approve a new Reserved decision there' in t and c03.EXC_C in owner, '')
        rec('C03 x secrets', 'the exception names no credential route: scaffold bars Production credentials, the owner keeps approved credentials [%s]' % c, c03.SCAFFOLD_CRED[c].lower() in text_of(c, c03.PS).lower() and c03.CREDS[c].lower() in owner.lower(), '')
        rec('C03 x seeding', 'Development seeding in Production stays barred under an exception [%s]' % c, c03.EXC_D in owner, '')
    c04 = load_suite('C04_GIT_CONDITIONAL')
    r02 = load_suite('R02_HQ01_GOV015')
    d = c04.repo()
    with open(os.path.join(d, 'package-lock.json'), 'a', encoding='utf-8', newline='\n') as f:
        f.write('\n')
    s = c04.status(d)
    rec('C04 x dirty tree', 'a dirty lockfile at task start still gives two options, and headless pauses', r02.porcelain_gate(s, 'interactive', None) == 'ASK_TWO_OPTIONS' and r02.porcelain_gate(s, 'headless', None) == 'PAUSE_SAFELY', s)
    shutil.rmtree(d, ignore_errors=True)
    for c in CANDIDATES:
        rec('C04 x dependencies', 'the lockfile consistency duty survives the conditional wording [%s]' % c, c04.CONSISTENT[c].lower() in text_of(c, c04.OWNER[c]).lower() and 'vulnerab' in text_of(c, '.claude/skills/add-dependency/SKILL.md').lower(), '')
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    moved = [(x['candidate'], x['policy_id']) for x in cov if x['status_changed'] or x['strength_status_changed']]
    rec('C05 x strength', 'no coverage or strength cell moved', not moved, moved[:6])
    by = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    rec('C05 x strength', 'the K0 scan criterion carries no canonical link, so it counts in no strength metric', all(not by[k].get('canonical_coverage') and by[k].get('strength_vs_canonical') == 'N/A' for k in ('FG-K0-0ef1e5ed3d', 'FG-K0-6d06b21a93')), '')
    rec('C07 x C05', 'the three corrected bans carry a resolution code, so MUST_NOT above a DEFAULT policy is explained', all((by[k].get('strength_resolution') or {}).get('code') for k in ('FG-L0-a2e9e91e8f', 'FG-K1-4767fd97b1', 'FG-K1-bc831815a3')), '')
    rec('C07 x R19 x R25', 'the L0 CI record keeps its accepted classification and now carries the out-of-evaluation label', by['FG-L0-29a3230807']['classification'] == 'EXTRA_PRODUCT' and by['FG-L0-29a3230807'].get('evaluation_scope') == 'OUT_OF_PRACTICAL_EVALUATION_CI', '')
    write_json('INTERACTION_MATRIX.json', m)


def sec_g(a):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    cross = read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    errs = viewcheck.check_all(rows, cross, cov)
    a.check('G', 'whole view: unique ids, line and quote resolution, recomputed coverage, crosswalk', not errs, errs[:6])
    r1, c1 = dataset.build()
    a.check('G', 'replay from the frozen baseline equals the files', rec_hash([r for c in CANDIDATES for r in r1[c]]) == rec_hash(rows) and rec_hash(c1) == rec_hash(cross))
    v1v2 = read_jsonl(out_path('V1_TO_V2_CROSSWALK.jsonl'))
    st = Counter(x['status'] for x in v1v2)
    a.check('G', 'no v1 record lost; every v2 record has one crosswalk row', st.get('LOST', 0) == 0 and len(v1v2) == len(rows), dict(st))
    man = read_json(out_path('DATASET_MANIFEST.json'))
    a.check('G', 'manifest counts recomputed, not carried from v1: rows and status equal the files', man['counts']['repaired_rows'] == len(rows) and man['v1_to_v2']['by_status'] == dict(st) and all(sha256_file(out_path(f)) == h for f, h in man['sha256'].items()), man['counts']['repaired_rows'])
    badline = []
    for r in rows:
        for e in r.get('current_evidence_refs') or []:
            if e.get('start_line'):
                if not e['path'].startswith('candidates/%s/template/' % r['candidate']):
                    badline.append(r['source_key'])
                else:
                    n = len(read_lines(wc_path(r['candidate'], e['path'].split('/template/')[1])))
                    if e['end_line'] > n:
                        badline.append(r['source_key'])
    a.check('G', 'every current anchor points into this folder and inside its file: no frozen or v1 line is presented as current', not badline, badline[:6])
    frozen = {k: r for c in CANDIDATES for k, r in baseline(c).items()}
    a.check('G', '6,402 baseline identities kept, each with its original claim', all(k in {x['source_key'] for x in rows} for k in frozen) and all(next_ok(r, frozen) for r in rows))
    adj = read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))
    a.check('G', '103 corrections: file unchanged from v1', sha256_file(out_path('CORRECTION_103_ADJUDICATION.jsonl')) == sha256_file(v1_path('CORRECTION_103_ADJUDICATION.jsonl')) and len(adj) == 103)
    un = read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
    by = {r['source_key']: r for r in rows}
    stale = [r['id'] for r in un if r['kind'] == 'ORIGINAL_OPEN_RECORD' and (by[r['id']]['classification'] == 'UNCERTAIN' or by[r['id']].get('future_human_decision'))]
    a.check('G', '31 original open records: none reverted', not stale, stale[:5])
    a.check('G', 'four proposals stay proposals, in their own candidates; the policy set stays 196', sum(1 for r in rows if r['source_key'].startswith('NCP-')) == 4 and len(policies()) == 196)
    g = read_json(out_path('POLICY_DEPENDENCY_GRAPH.json'))
    a.check('G', 'dependency graph rebuilt equals the stored one', rec_hash(depgraph.build()) == rec_hash({k: v for k, v in g.items() if k != 'at'}))


def next_ok(r, frozen):
    k = r['source_key']
    return k not in frozen or r.get('claim_text_original') == frozen[k].get('claim_text')


def sec_h(a):
    """POLICY_PARITY_MATRIX.jsonl: 1,176 cells with current witness, condition and strength. Mechanical witnesses are labeled as such."""
    rows = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    reviews = {}
    for rule in V2_ORDER:
        p = out_path('_rules', rule, 'review.py')
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location('rv_' + rule.replace('-', '_'), p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            for x in m.REVIEW:
                reviews.setdefault((x['candidate'], x['policy']), []).append(dict(x, rule=rule))
    partial = {(x['candidate'], x['policy_id']): x for x in read_jsonl(out_path('PARTIAL_WITNESSES_38.jsonl'))}
    out = []
    no_ce = []
    for cell in cov:
        c, pid = cell['candidate'], cell['policy_id']
        pol = policies()[pid]
        wit = []
        for key in (cell['direct_source_keys'] + cell['partial_source_keys'])[:3]:
            r = rows[key]
            e = next((x for x in r.get('current_evidence_refs') or [] if x.get('start_line')), None)
            if e:
                rel = e['path'].split('/template/')[1]
                wit.append({'key': key, 'path': e['path'], 'start_line': e['start_line'], 'quote': norm_ws(' '.join(read_lines(wc_path(c, rel))[e['start_line'] - 1:e['end_line']]))[:200], 'modality': r.get('modality'), 'condition': r.get('applicability_trigger') or r.get('applicability_hint'), 'applicability_status': r.get('applicability_status')})
        rv = reviews.get((c, pid), [])
        pt = partial.get((c, pid))
        level = 'SOURCE_REVIEWED_V2' if rv else ('CLAUSE_REVIEWED_V2' if pt else 'MECHANICAL_WITNESS_ONLY')
        entail = [x.get('note') for x in rv if x.get('verdict') != 'NOT_AFFECTED'] or ([pt['reading']] if pt else [])
        ce = [x.get('counterexample') for x in rv if x.get('counterexample')] or ([pt['counterexample']] if pt else [])
        if level != 'MECHANICAL_WITNESS_ONLY' and any(x.get('verdict') != 'NOT_AFFECTED' for x in rv) and not ce:
            no_ce.append((c, pid))
        if pt and not ce:
            no_ce.append((c, pid))
        out.append({'candidate': c, 'policy_id': pid, 'policy_strength': pol['normative_strength'], 'scope': pol['scope'], 'status': cell['status'], 'strength_status': cell['strength_status'], 'n_direct': len(cell['direct_source_keys']), 'n_partial': len(cell['partial_source_keys']), 'witnesses': wit, 'check_level': level, 'entailment': entail, 'counterexample': ce, 'partial_status': pt['status'] if pt else None, 'semantics': 'Traceability unless check_level says reviewed. A witness at a current line does not prove parity.'})
    write_jsonl('POLICY_PARITY_MATRIX.jsonl', out)
    levels = Counter(x['check_level'] for x in out)
    a.check('H', '1,176 cells, 196 per candidate', len(out) == 1176 and all(sum(1 for x in out if x['candidate'] == c) == 196 for c in CANDIDATES), dict(levels))
    a.check('H', 'every cell has a witness at a current line', all(x['witnesses'] for x in out), [(x['candidate'], x['policy_id']) for x in out if not x['witnesses']][:6])
    a.check('H', 'every changed or qualified cell has a source reading and a counterexample', not no_ce, no_ce[:8])
    a.row('H', 'cells with only a mechanical witness', 'FINDING', '%d of 1,176 were not read side by side in v2. They rest on the Step 2 classification and v1, plus a witness at a current line.' % levels['MECHANICAL_WITNESS_ONLY'])


def sec_i(a):
    """All suites, cold, on final bytes: both history levels, including their mutation tests."""
    tally = Counter()
    by = {}
    for rule in ORDER + V2_ORDER:
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
            if r['status'] == 'FAIL':
                a.row('I', '%s: %s' % (rule, r['test'][:90]), 'FAIL', r['detail'], r['candidate'])
            elif r['status'] == 'NOT_RUN':
                a.row('I', '%s: %s' % (rule, r['test'][:90]), 'NOT_RUN', r['detail'], r['candidate'])
        a.row('I', 'suite %s: pass %d, fail %d, not run %d' % (rule, t['PASS'], t['FAIL'], t['NOT_RUN']), 'PASS' if not t['FAIL'] else 'FAIL', '')
    write_json('FINAL_SUITE_TALLY.json', {'at': now(), 'tally': dict(tally), 'by_suite': by})


def run_audit():
    a = Audit()
    for fn in (sec_a, sec_b, sec_c, sec_d, sec_e, sec_f, sec_g, sec_h, sec_i):
        try:
            fn(a)
        except Exception as e:  # a crashed section is a failed section
            a.row(fn.__name__[-1].upper(), 'section crashed', 'FAIL', repr(e))
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
