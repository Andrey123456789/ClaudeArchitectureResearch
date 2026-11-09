"""v1 R27 audit, replayed on v2 bytes as a regression inside each gate. Reads no gate result or checkpoint. Re-runs hooks and checkers on fresh copies. Status words: PASS, FAIL, NOT_RUN, FINDING.
The separate v2 cold audit is final_audit_v2.py. Adaptations from v1 are listed in _tools/adaptations.py."""
import copy
import importlib.util
import json
import os
import re
import shutil
import subprocess
import uuid
from collections import Counter

import dataset
import depgraph
import viewcheck
from fence import verify as fence_verify
from invariants import check_all as invariants_all
from rcommon import AUD, CANDIDATES, OUT, SCRATCH, all_change_rows, baseline, coverage, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, sha256_file, template_root, utf8_stdout, walk_files, wc_path, write_json, write_jsonl
from sandbox import CHECKERS, fresh_copy, pre_tool, run_checkers, run_node

DENIED = ('deny', 'block')
ROOT_55 = os.path.abspath(os.path.join(OUT, '..', '..', '..'))
UI = {c: 'Development Swagger UI' for c in CANDIDATES}
UI['L1'] = 'Development API documentation UI'


def load_suite(name):
    spec = importlib.util.spec_from_file_location('aud_' + name, os.path.join(OUT, '_tools', 'suites', name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def tree_text(c, suffix='.md'):
    for rel in walk_files(template_root(c)):
        if rel.endswith(suffix):
            yield rel, read_lines(wc_path(c, rel))


def loading_class(c, rel):
    if rel == 'CLAUDE.md':
        return 'ALWAYS_LOADED'
    if rel.startswith('.claude/skills/'):
        return 'ON_INVOCATION'
    if rel.startswith('.claude/rules/'):
        head = '\n'.join(read_lines(wc_path(c, rel))[:12])
        return 'PATH_RULE' if 'paths:' in head else 'ALWAYS_RULE'
    return 'OTHER'


def find_phrase(c, phrase):
    n = norm_ws(phrase).lower()
    hits = []
    for rel, ls in tree_text(c):
        t = norm_ws(' '.join(ls)).lower()
        if n in t:
            hits.append(rel)
    return hits


class Audit:
    def __init__(self):
        self.rows = []

    def row(self, section, test, status, detail='', candidate=None):
        self.rows.append({'section': section, 'test': test, 'candidate': candidate, 'status': status, 'detail': str(detail)[:900]})

    def check(self, section, test, cond, detail='', candidate=None):
        self.row(section, test, 'PASS' if cond else 'FAIL', detail, candidate)


def sec_a(a):
    f = fence_verify()
    a.check('A', 'immutable trees unchanged (hashes rebuilt)', f['n_errors'] == 0, {k: f[k] for k in f if k != 'errors'} if f['n_errors'] == 0 else f.get('errors'))
    start = read_json(out_path('V2_BASELINE_MANIFEST.json'))['created_at']
    import datetime
    t0 = datetime.datetime.fromisoformat(start).timestamp() - 300
    newer = []
    for dp, dn, fn in os.walk(ROOT_55):
        # The Codex area is pruned before it is entered: never listed, read or stat-ed.
        dn[:] = [d for d in dn if 'codex_iterative_search' not in d and os.path.abspath(os.path.join(dp, d)) != os.path.abspath(OUT)]
        for x in fn:
            if 'codex_iterative_search' in x:
                continue
            p = os.path.join(dp, x)
            try:
                if os.path.getmtime(p) > t0:
                    newer.append(os.path.relpath(p, ROOT_55))
            except OSError:
                pass
    kit = [n for n in newer if n.replace(os.sep, '/').startswith('_STAGE_A_KIT/')]
    other = [n for n in newer if n not in kit]
    a.check('A', 'no file outside the run root is newer than the run start, apart from kit files', not other, other[:12])
    if kit:
        a.row('A', 'kit files newer than the run start: fence hashes unchanged', 'PASS' if f['n_errors'] == 0 else 'FAIL', kit[:8])
    writers = []
    for dp, dn, fn in os.walk(os.path.join(OUT, '_tools')):
        for x in fn:
            if x.endswith('.py') and x != 'final_audit.py':
                with open(os.path.join(dp, x), encoding='utf-8') as fh:
                    t = fh.read()
                if re.search(r'zipfile|make_archive|tarfile', t):
                    writers.append(x)
    a.check('A', 'no tool of this run writes an archive', not writers, writers)
    e = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    r = subprocess.run(['git', '-C', ROOT_55, 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True, env=e)
    if r.returncode != 0:
        a.row('A', 'research folder Git state', 'PASS', 'The research folder is not inside a Git work tree, so no Git mutation could reach it. Git ran only in fixtures under _scratch.')
    else:
        s = subprocess.run(['git', '-C', ROOT_55, 'log', '-1', '--format=%H %cI'], capture_output=True, text=True, env=e)
        a.row('A', 'research folder Git state', 'PASS', s.stdout.strip())
    step3 = [n for n in os.listdir(os.path.join(OUT, '..')) if 'step3' in n.lower()]
    a.check('A', 'no Step 3 output', not step3, step3)
    ls = [x for x in os.listdir(OUT) if x.lower().startswith('step3')]
    a.check('A', 'no Step 3 output in the run root', not ls, ls)


def sec_b(a):
    log = {}
    rules = {}
    for r in all_change_rows():
        if r.get('kind') == 'TEMPLATE':
            log[(r['candidate'], r['file'])] = r['after_sha256']
            rules.setdefault((r['candidate'], r['file']), [])
            if r['rule'] not in rules[(r['candidate'], r['file'])]:
                rules[(r['candidate'], r['file'])].append(r['rule'])
    man = {}
    for c in CANDIDATES:
        cur = set(walk_files(template_root(c)))
        inp_root = os.path.dirname(input_path(c, 'CLAUDE.md'))
        inp = set(walk_files(inp_root))
        extra, gone = sorted(cur - inp), sorted(inp - cur)
        a.check('B', 'no file added or removed against the frozen template, unless logged', all((c, x) in log for x in extra) and not gone, {'extra': extra[:5], 'gone': gone[:5]}, c)
        bad = []
        files = {}
        for rel in sorted(cur):
            h = sha256_file(wc_path(c, rel))
            base = sha256_file(input_path(c, rel)) if rel in inp else None
            if h != base and log.get((c, rel)) != h:
                bad.append(rel)
            if h == base and (c, rel) in log and log[(c, rel)] != h:
                bad.append(rel)
            files[rel] = {'sha256': h, 'input_sha256': base, 'origin': 'UNCHANGED' if h == base else 'MODIFIED', 'rules': rules.get((c, rel), [])}
        a.check('B', 'each changed file matches the last logged hash', not bad, bad[:6], c)
        man[c] = files
        a.row('B', 'changed files', 'PASS', sum(1 for v in files.values() if v['origin'] == 'MODIFIED'), c)
    write_json('WORKING_COPY_MANIFEST.json', {'version': 'step2-controlled-repair-v2', 'at': now(), 'candidates': man})


def sec_c(a):
    inv = invariants_all()
    for c in CANDIDATES:
        a.check('C', 'architecture identity invariants', not inv[c], inv[c][:4], c)
        root = fresh_copy(c, 'audit')
        for r in run_checkers(c, root):
            a.check('C', 'own checker: %s' % r['checker'], r['exit'] == 0, r['tail'], c)
        bad, n = [], 0
        for rel in walk_files(root):
            if rel.endswith(('.js', '.mjs', '.cjs')):
                n += 1
                code, out, err = run_node(root, ['--check', rel])
                if code:
                    bad.append(rel)
        a.check('C', 'node --check on %d scripts' % n, not bad, bad[:5], c)
        st = json.load(open(os.path.join(root, '.claude', 'settings.json'), encoding='utf-8'))
        cmds = [h.get('command', '') for ev in (st.get('hooks') or {}).values() for g in ev for h in g.get('hooks', [])]
        miss = []
        for cmd in cmds:
            for m in re.findall(r'\.claude/[\w./-]+\.(?:mjs|cjs|js)', cmd):
                if not os.path.exists(os.path.join(root, m)):
                    miss.append(m)
        a.check('C', 'all %d registered hook commands resolve' % len(cmds), cmds and not miss, miss[:5], c)
        sk = os.path.join(root, '.claude', 'skills')
        badskill = []
        for d in sorted(os.listdir(sk)):
            p = os.path.join(sk, d, 'SKILL.md')
            if not os.path.exists(p):
                badskill.append(d)
                continue
            m = re.search(r'^name:\s*(\S+)', '\n'.join(read_lines(p)[:6]), re.M)
            if not m or m.group(1) != d:
                badskill.append(d)
        a.check('C', 'every skill folder has a SKILL.md whose name matches', not badskill, badskill[:6], c)
        need = ('verify', 'architecture-decision', 'git-workflow', 'add-dependency', 'caching', 'development-workflow', 'swagger', 'project-structure')
        a.check('C', 'skills named by the changed rules exist', all(os.path.isdir(os.path.join(sk, s)) for s in need), [s for s in need if not os.path.isdir(os.path.join(sk, s))], c)
        imports, stack, gone = set(), ['CLAUDE.md'], []
        while stack:
            rel = stack.pop()
            if rel in imports:
                continue
            imports.add(rel)
            p = os.path.join(root, rel.replace('/', os.sep))
            if not os.path.exists(p):
                gone.append(rel)
                continue
            for line in read_lines(p):
                m = re.match(r'^@(\S+)\s*$', line.strip())
                if m:
                    stack.append(m.group(1)[2:] if m.group(1).startswith('./') else m.group(1))
        a.check('C', 'CLAUDE.md imports resolve (%d files)' % len(imports), not gone, gone[:5], c)
        shutil.rmtree(root, ignore_errors=True)


HOOK_TASKS = [('peer bypass with --force', 'npm install x@1.2.3 --force', 'DENY'), ('peer bypass with --legacy-peer-deps', 'npm install x@1.2.3 --legacy-peer-deps', 'DENY'), ('nested peer bypass', 'bash -c "npm install x@1.2.3 --force"', 'DENY'), ('environment form of the bypass', 'npm_config_force=true npm install x@1.2.3', 'DENY'),
              ('read-only Git', 'git status', 'NOT_DENY'), ('pinned install, first attempt', 'npm install x@1.2.3', 'REPORT'), ('hard reset', 'git reset --hard', 'REPORT'), ('force push to main', 'git push --force origin main', 'REPORT')]
TEXT_TASKS = [('Task starts on a tree with foreign changes', lambda c: 'pause safely: change nothing and report the changes found'), ('Generic approved workflow meets a commit step', lambda c: 'a workflow step that mentions committing is not that authority'), ('User asks to rewrite main', lambda c: 'An explicit request to rewrite a named branch, including `main`, is valid unless another policy forbids it'),
              ('Headless run meets an unexpected Reserved choice', lambda c: 'Never make or approve a new Reserved decision there'), ('Design cache invalidation', lambda c: 'Invalidating before the mutation is not ruled out'), ('User asks for a floating version', lambda c: 'explicit, bounded user request that names the package'), ('Peer conflict during install', lambda c: 'No confirmation, comment marker, or approval opens this route'),
              ('API behavior change, tests pass', lambda c: 'open the %s and confirm it loads, even when startup and composition did not change' % UI[c]), ('Application cannot run here', lambda c: 'report the check as NOT RUN with the reason')]


def sec_d(a):
    matrix = {'hook_tasks': {}, 'manifest_tasks': {}, 'text_tasks': {}, 'semantics': 'Same hypothetical task across six. Hook rows are executed decisions. Text rows locate the required sentence and how it reaches the agent. Different routing or loading is a delivery difference, not a different obligation, unless stated.'}
    for name, cmd, want in HOOK_TASKS:
        row = {}
        for c in CANDIDATES:
            root = fresh_copy(c, 'task')
            first, _ = pre_tool(root, c, cmd)
            second, _ = pre_tool(root, c, cmd)
            row[c] = {'first': first, 'second': second}
            shutil.rmtree(root, ignore_errors=True)
            if want == 'DENY':
                a.check('D', 'same task, %s: denied on first and second attempt' % name, first in DENIED and second in DENIED, row[c], c)
            elif want == 'NOT_DENY':
                a.check('D', 'same task, %s: not denied' % name, first not in DENIED, row[c], c)
        matrix['hook_tasks'][name] = dict(row, command=cmd, expectation=want)
        if want == 'REPORT':
            froz = {}
            for c in CANDIDATES:
                root = os.path.join(SCRATCH, 'runs', '%s-frozen-%s' % (c, uuid.uuid4().hex[:8]))
                shutil.copytree(os.path.dirname(input_path(c, 'CLAUDE.md')), root)
                froz[c] = pre_tool(root, c, cmd)[0]
                shutil.rmtree(root, ignore_errors=True)
            matrix['hook_tasks'][name]['frozen_first'] = froz
            same = all(froz[c] == row[c]['first'] for c in CANDIDATES)
            a.row('D', 'same task, %s: routing recorded and compared with a copy of the frozen template' % name, 'PASS' if same else 'FINDING', {c: {'now': row[c]['first'], 'frozen': froz[c]} for c in CANDIDATES})
    s = load_suite('R04_HQ03_DEP003')
    tasks = {'floating version, no record': None, 'floating version, matching record': [s.entry()], 'record says agent, not user': [s.entry(requested_by='agent')], 'record for another manifest': [s.entry(manifest='frontend/Other/package.json')]}
    for name, rec in tasks.items():
        row = {}
        for c in CANDIDATES:
            root = s.fixture(c, record=rec)
            code, out = s.check(c, root)
            row[c] = {'left_pad_rejected': s.rejected(out, 'left-pad'), 'other_lib_rejected': s.rejected(out, 'other-lib')}
            shutil.rmtree(root, ignore_errors=True)
            a.check('D', 'manifest task, %s: unrelated floating package still rejected' % name, row[c]['other_lib_rejected'], row[c], c)
            want = name != 'floating version, matching record'
            a.check('D', 'manifest task, %s: left-pad %s' % (name, 'rejected' if want else 'accepted'), row[c]['left_pad_rejected'] == want, row[c], c)
        matrix['manifest_tasks'][name] = row
    for name, phrase in TEXT_TASKS:
        row = {}
        for c in CANDIDATES:
            hits = find_phrase(c, phrase(c))
            row[c] = [{'path': h, 'loading': loading_class(c, h)} for h in hits]
            a.check('D', 'text task, %s: required sentence present' % name, bool(hits), row[c], c)
        matrix['text_tasks'][name] = row
    write_json('SAME_TASK_MATRIX.json', dict(matrix, at=now()))


def sec_e(a):
    # (a) Git authority versus headless approvals
    for c in CANDIDATES:
        t = norm_ws(' '.join(read_lines(wc_path(c, 'CLAUDE.md'))))
        m = re.search(r'In an autonomous or headless run, implement a Reserved change.*?decision log[^.]*\.', t, re.I)
        a.check('E', 'Git vs headless: the headless approval sentence grants no Git authority', m and not re.search(r'\b(commit|push|merge|rebase|reset)\b', m.group(0), re.I), (m.group(0)[:160] if m else 'sentence not found'), c)
        a.check('E', 'Git vs headless: the Git clause does not accept a general approval', 'general task approval, or a workflow step that mentions committing is not that authority' in t, candidate=c)
    root = fresh_copy('K0', 'ix')
    for cmd in ('git push --force origin main', 'git push --force origin main # approved workflow', 'git reset --hard # approved by the Reserved decision'):
        d, _ = pre_tool(root, 'K0', cmd)
        a.check('E', 'Git vs headless: K0 hook does not allow: %s' % cmd, d != 'allow', d, 'K0')
    shutil.rmtree(root, ignore_errors=True)
    a.row('E', 'Git vs headless: what an `ask` decision does in a headless host', 'NOT_RUN', 'No live host in this run. The hook decision itself was executed.')
    steps = []
    for c in CANDIDATES:
        for rel, ls in tree_text(c):
            if rel == 'CLAUDE.md' or rel.endswith('git-workflow/SKILL.md'):
                continue
            for i, l in enumerate(ls, 1):
                if re.match(r'^\s*(\d+\.|-)?\s*(\*\*)?Commit\b(?! boundary)', l) or re.search(r'[Mm]aintain and commit\b|\band commit `', l):
                    steps.append('%s %s:%d %s' % (c, rel, i, norm_ws(l)[:80]))
    a.row('E', 'Git vs headless: instruction lines that still say commit', 'FINDING', 'The Git clause names this case: such a step is not authority. %d lines remain as written, in %s. %s' % (len(steps), ', '.join(sorted({s.split()[0] for s in steps})), '; '.join(steps[:6])))
    a.row('E', 'Git vs headless: a headless run with an approved Reserved change on a dirty tree', 'FINDING', 'The task-start pause comes first, so the approved change waits. The two rules do not conflict, but a harness must supply a clean tree or a standing choice.')
    # (b) floating versions versus dependency checks
    s = load_suite('R04_HQ03_DEP003')
    root = s.fixture('K0', record=[s.entry(ecosystem='nuget', package='Float.Package', version='1.*', manifest='Directory.Packages.props')])
    with open(os.path.join(root, 'Directory.Build.props'), 'w', encoding='utf-8') as f:
        f.write('<Project><PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup></Project>')
    with open(os.path.join(root, 'Directory.Packages.props'), 'w', encoding='utf-8') as f:
        f.write('<Project><ItemGroup><PackageVersion Include="Float.Package" Version="1.*" /><PackageVersion Include="Other.Package" Version="2.*" /></ItemGroup></Project>')
    code, out = s.check('K0', root)
    a.check('E', 'floating vs checks: K0 inherited CPM plus a NuGet exception: Float.Package accepted, Other.Package rejected', not s.rejected(out, 'Float.Package') and s.rejected(out, 'Other.Package'), out[-300:], 'K0')
    shutil.rmtree(root, ignore_errors=True)
    root = s.fixture('K1', record=[s.entry()])
    allowed, _ = pre_tool(root, 'K1', 'npm install left-pad@*')
    leak, _ = pre_tool(root, 'K1', 'npm install other-lib@*')
    a.check('E', 'floating vs checks: K1 command classifier honors the record for the named package only', allowed == 'allow' and leak in DENIED, {'named': allowed, 'other': leak}, 'K1')
    shutil.rmtree(root, ignore_errors=True)
    a.row('E', 'floating vs checks: registry lookup and NuGet restore with a floating version', 'NOT_RUN', 'No network in this run. MSBuild property evaluation ran in R08; restore did not.')
    a.row('E', 'floating vs checks: a forged record', 'FINDING', 'An agent can write the record itself. The checker cannot verify who asked. Enforcement stops accidents and leaves a trail.')
    # (c) peer bypass versus approval mechanism
    for c in CANDIDATES:
        root = s.fixture(c, record=[s.entry(package='x', version='^1.0.0')])
        tail = {'M1': ' # add-dependency: checked', 'K0': ' # add-dependency: reviewed'}.get(c, '')
        out = {}
        for cmd in ('npm install x@^1.0.0 --force', 'npm install x@1.2.3 --force # approved by user', 'npm install x@1.2.3 --force%s' % tail, 'npm install x@1.2.3 --legacy-peer-deps # Reserved approval recorded'):
            pre_tool(root, c, cmd)
            out[cmd] = pre_tool(root, c, cmd)[0]
        a.check('E', 'peer vs approval: record, approval text, workflow marker and a retry open nothing', all(v in DENIED for v in out.values()), out, c)
        shutil.rmtree(root, ignore_errors=True)
    # (d) cache semantics versus transaction and logging
    for c in CANDIDATES:
        hits = []
        for rel, ls in tree_text(c):
            t = norm_ws(' '.join(ls))
            for m in re.finditer(r'[^.]*\b(must|always|only)\b[^.]{0,50}\b(invalidat\w*|evict\w*)\b[^.]{0,30}\bafter (the )?(commit|transaction)[^.]*\.', t, re.I):
                hits.append((rel, m.group(0)[:120]))
        a.check('E', 'cache vs transaction: no line demands post-commit invalidation as the only order', not hits, hits[:3], c)
        own = {'M': '.claude/rules/performance.md', 'M1': '.claude/rules/performance.md', 'L0': '.claude/rules/0-core/runtime-principles.md', 'L1': '.claude/rules/0-core/backend-code.md', 'K0': '.claude/rules/backend/caching.md', 'K1': '.claude/rules/backend/runtime.md'}[c]
        t = norm_ws(' '.join(read_lines(wc_path(c, own)))).lower()
        miss = [p for p in ('isolation level', 'concurrent reads and refills', 'commit and rollback order', 'crash between commit and invalidation', 'retries', 'tolerated') if p not in t]
        a.check('E', 'cache vs transaction: the owner names all strategy inputs', not miss, miss, c)
    a.row('E', 'cache vs transaction: timelines against a real database and cache', 'NOT_RUN', 'No server in this run. The semantic timeline tests of R03 are text and reasoning.')
    # (e) migration policy versus seeding and CI scope
    bars = re.compile(r'production (database )?migrations?[^.]{0,40}(must not|are not|is not|never)[^.]{0,30}automatic[^.]{0,40}startup|(do not|never|must not)[^.]{0,20}(apply|run|wire)[^.]{0,20}(automatic )?production (database )?migrations?[^.]{0,40}(automatic|startup)')
    for yes in ('production database migrations must not run automatically from normal application startup by default', 'production database migrations are not applied automatically from normal application startup', 'do not apply production database migrations automatically from normal application startup', 'do not wire automatic production migration at normal application startup'):
        a.check('E', 'migration pattern control, should match: %s' % yes[:50], bool(bars.search(yes)))
    for no in ('production migration is an explicit deployment step', 'apply migrations automatically at startup in development', 'production credentials must not be committed'):
        a.check('E', 'migration pattern control, should not match: %s' % no[:50], not bars.search(no))
    for c in CANDIDATES:
        h = []
        for rel, ls in tree_text(c):
            t = norm_ws(' '.join(ls)).lower()
            if bars.search(t):
                h.append(rel)
        a.check('E', 'migration vs seeding: a text bars automatic Production migration at startup', bool(h), h[:3], c)
        ci = sha256_file(wc_path(c, '.claude/skills/ci-cd/SKILL.md')) == sha256_file(input_path(c, '.claude/skills/ci-cd/SKILL.md'))
        a.check('E', 'migration vs CI scope: the ci-cd skill is unchanged', ci, candidate=c)
    pc = norm_ws(' '.join(read_lines(wc_path('K1', '.claude/skills/persistence-change/SKILL.md')))).lower()
    a.check('E', 'migration vs seeding: K1 keeps schema before seed and migration review after the local change', 'before any seeding' in pc and 'review' in pc, candidate='K1')
    # (f) Swagger UI versus noninteractive verification
    for c in CANDIDATES:
        t = norm_ws(' '.join(read_lines(wc_path(c, '.claude/skills/verify/SKILL.md')))).lower()
        a.check('E', 'Swagger vs noninteractive: NOT RUN is required and PASS is barred when the app cannot run', 'report the check as not run with the reason; never report it as passed' in t and 'not run' in t, candidate=c)
        sw = norm_ws(' '.join(read_lines(wc_path(c, '.claude/skills/swagger/SKILL.md')))).lower()
        a.check('E', 'Swagger vs noninteractive: the swagger skill defers to verify', 'verify' in sw, candidate=c)
    a.row('E', 'Swagger vs noninteractive: real API and real UI', 'NOT_RUN', 'No application runs in this run.')
    # (g) PI-012 modality versus classification strength
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    frozen = {k: r for c in CANDIDATES for k, r in baseline(c).items()}
    bad = []
    for r in rows:
        if not r['repair']['active']:
            continue
        for o in [r] + list(r.get('subclauses') or []) + list(r.get('audit_subclauses') or []):
            if o.get('classification') in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA') and o.get('strength_vs_canonical') == 'SAME' and o.get('strength_mechanical_mismatch') and not o.get('strength_resolution'):
                bad.append(r['source_key'])
    a.check('E', 'PI-012 vs strength: no record says SAME while its modality differs from the policy class with no resolution code', not bad, bad[:8])
    by = {r['source_key']: r for r in rows}
    moved = [k for k in frozen if by[k]['modality'] != frozen[k].get('modality')]
    a.row('E', 'PI-012 vs strength: coverage status cannot show a modality effect', 'FINDING', 'Coverage status does not read modality, so "0 cells moved" is true by construction for modality changes. %d records changed modality. Strength cells depend on strength_vs_canonical; the check above is the real test.' % len(moved))


def sec_f(a):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    cross = read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    by = {r['source_key']: r for r in rows}
    errs = viewcheck.check_all(rows, cross, cov)
    a.check('F', 'whole view: unique ids, line and quote resolution, recomputed coverage, crosswalk', not errs, errs[:8])
    r1, c1 = dataset.build()
    a.check('F', 'overlay replay from the frozen baseline equals the files', rec_hash([r for c in CANDIDATES for r in r1[c]]) == rec_hash(rows) and rec_hash(c1) == rec_hash(cross))
    for f, want in (('PI012_79_REVIEW.jsonl', {'CORRECT': 55, 'UPHOLD': 22, 'UNRESOLVED': 2}), ('PI012_230_REVIEW.jsonl', {'CORRECT': 105, 'UPHOLD': 123, 'UNRESOLVED': 2})):
        rs = read_jsonl(out_path(f))
        got = Counter(r['result'] for r in rs)
        a.check('F', '%s counts' % f, dict(got) == want, dict(got))
        off = []
        for r in rs:
            base, _, sub = r['key'].partition('/')
            if sub or base not in by:
                continue
            if r['result'] == 'CORRECT' and by[base]['modality'] != r['modality_after'] and len(by[base]['repair']['rules']) <= 1:
                off.append(r['key'])
        a.check('F', '%s: each correction is in the view, or a later rule changed the record' % f, not off, off[:6])
    adj = read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))
    a.check('F', '103 corrections: all decided', len(adj) == 103 and not [r for r in adj if r['decision'] == 'UNRESOLVED'], Counter(r['decision'] for r in adj))
    off = []
    for r in adj:
        if r['decision'] in ('ACCEPT', 'ACCEPT_MODIFIED'):
            base, _, sub = r['case_key'].partition('/')
            rec = by[base]
            if sub or not rec['repair']['active']:
                continue
            for f, v in r['applied_set'].items():
                if f in ('subclauses', 'subclauses_add', 'subclause_set'):
                    continue
                if rec.get(f) != v and not any(x != 'R25-COR103:%s' % r['correction_id'] and not x.startswith('R01') for x in rec['repair']['rules'][rec['repair']['rules'].index('R25-COR103:%s' % r['correction_id']) + 1:]):
                    off.append((r['case_key'], f))
    a.check('F', '103 corrections: each accepted field is in the view, or a later rule overrode it', not off, off[:6])
    ncp = read_jsonl(out_path('NEW_CLAUSES_4_ADJUDICATION.jsonl'))
    a.check('F', 'four clauses: present in their own candidate, not promoted', len(ncp) == 4 and all(by[r['proposal_id']]['candidate'] == r['candidate'] for r in ncp) and len(policies()) == 196)
    un = read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
    op = [r for r in un if r['kind'] == 'ORIGINAL_OPEN_RECORD']
    stale = [r['id'] for r in op if by[r['id']]['classification'] == 'UNCERTAIN' or by[r['id']].get('future_human_decision') or any(s.get('classification') == 'UNCERTAIN' for s in by[r['id']].get('subclauses') or [])]
    a.check('F', '31 open records: none left UNCERTAIN or waiting on a human decision in the view', len(op) == 31 and not stale, stale[:6])
    cm = read_jsonl(out_path('CROSS_METHOD_ADJUDICATION.jsonl'))
    q = [r for r in cm if r['kind'] in ('STRENGTH_CELL', 'QUALIFIED_OVERRIDE')]
    cells = {(x['candidate'], x['policy_id']): x for x in cov}
    drift = []
    for r in q:
        c, pid = r['cell'].split()
        if cells[(c, pid)]['strength_status'] != cells[(c, pid)]['baseline_strength_status']:
            drift.append(r['cell'])
    a.check('F', 'qualified cells: 5 plus 3, qualifier kept, strength descriptor unchanged', len(q) == 8 and all(r['result'] == 'QUALIFIER_RETAINED' for r in q) and not drift, drift)
    a.check('F', '1,176 cells accounted for: 196 per candidate', all(sum(1 for x in cov if x['candidate'] == c) == 196 for c in CANDIDATES) and len(cov) == 1176)
    ze = [(x['candidate'], x['policy_id']) for x in cov if not x['direct_source_keys']]
    bz = [(c, p) for c in CANDIDATES for p, v in coverage(c).items() if not v.get('direct_source_keys')]
    a.check('F', 'no cell lost its last direct witness', set(ze) == set(bz), sorted(set(ze) ^ set(bz))[:6])
    a.row('F', 'cells that stand on a written Step 2 override or partial witnesses, as in the baseline', 'FINDING', '%d cells have no FULL direct witness in either view. Each is a qualified traceability cell, not proof of a full owner.' % len(ze))
    moved = [x for x in cov if x['status_changed'] or x['strength_status_changed']]
    a.row('F', 'cells whose status or strength moved', 'PASS', [(x['candidate'], x['policy_id']) for x in moved][:20] or 'none')
    g = read_json(out_path('POLICY_DEPENDENCY_GRAPH.json'))
    a.check('F', 'dependency graph covers 1,176 cells', sum(len(g['per_candidate'][c]) for c in CANDIDATES) == 1176)
    fresh = depgraph.build()
    a.check('F', 'dependency graph rebuilt from the final view and change log equals the stored one', rec_hash(fresh) == rec_hash({k: v for k, v in g.items() if k != 'at'}))
    no_delivery = [(x['candidate'], x['policy_id']) for x in cov if not any(w.get('delivery_context') for w in x['witnesses'])]
    a.check('F', 'every cell separates reachability (witness delivery) from the semantic strength descriptor', not no_delivery and all('strength_status' in x for x in cov), no_delivery[:6])
    a.row('F', 'all conditions and exceptions of all 1,176 cells read by hand', 'NOT_RUN', 'Not feasible in this run. Only the changed policies were read side by side (review.py). The rest got the mechanical witness checks.')


def run_audit():
    a = Audit()
    for fn in (sec_a, sec_b, sec_c, sec_d, sec_e, sec_f):
        try:
            fn(a)
        except Exception as e:  # a crashed section is a failed section
            a.row(fn.__name__[-1].upper(), 'section crashed', 'FAIL', repr(e))
    write_jsonl('R27_AUDIT_REPLAY_RESULTS.jsonl', a.rows)
    return a.rows


def main():
    utf8_stdout()
    rows = run_audit()
    print(Counter(r['status'] for r in rows))
    for r in rows:
        if r['status'] in ('FAIL', 'FINDING', 'NOT_RUN'):
            print(r['status'], r['section'], r['candidate'], r['test'], '|', r['detail'][:400])


if __name__ == '__main__':
    main()
