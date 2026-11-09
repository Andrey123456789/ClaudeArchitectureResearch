"""C01 regression: all six checkers verify the effective CPM state. Identical fixtures through each candidate's real checker, real MSBuild, no restore, no network.

Each fixture is also evaluated directly by MSBuild, independent of any checker, so a checker cannot agree with itself by mistake.
A separate offline restore against an empty local feed observes NuGet's own CPM errors. It needs no package and no registry.
"""
import json
import os
import re
import shutil
import subprocess
import uuid
from concurrent.futures import ThreadPoolExecutor

from rcommon import CANDIDATES, SCRATCH, sha256_file, walk_files
from sandbox import env_for, fresh_copy, scratch_dir
from suitelib import mutate_text, post

PROJ = 'backend/App.Api/App.Api.csproj'
PROJ2 = 'backend/App.Application/App.Application.csproj'
T = '<PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup>'
F = '<PropertyGroup><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup>'
EMPTY = '<Project></Project>'
RUN = {'M': ['.claude/scripts/check-manifests.mjs'], 'M1': ['.claude/scripts/check-manifests.js'], 'L0': ['.claude/hooks/manifest-checks.mjs'], 'L1': ['.claude/hooks/post-change-checks.mjs', '--scan'], 'K0': ['.claude/scripts/check-dependencies.cjs', '--root', '{root}'], 'K1': ['.claude/scripts/check-manifests.cjs']}
HOOK = {'M': ['.claude/hooks/file-change.mjs'], 'M1': ['.claude/hooks/post-tool-use.js'], 'L0': ['.claude/hooks/claude-hook.mjs', 'post-edit'], 'L1': ['.claude/hooks/post-change-checks.mjs'], 'K0': ['.claude/hooks/hook.cjs', 'post-tool-use'], 'K1': ['.claude/hooks/dispatch.cjs', 'PostToolUse']}
CHECKER_FILE = {'M': '.claude/scripts/check-manifests.mjs', 'M1': '.claude/scripts/check-manifests.js', 'L0': '.claude/hooks/manifest-checks.mjs', 'L1': '.claude/hooks/post-change-checks.mjs', 'K0': '.claude/scripts/check-dependencies.cjs', 'K1': '.claude/scripts/check-manifests.cjs'}
RULE = {'M': '.claude/rules/dependencies.md', 'M1': '.claude/rules/dependencies.md', 'L0': '.claude/rules/3-project/package-management.md', 'L1': '.claude/rules/3-project/package-management.md', 'K0': '.claude/rules/common/dependencies.md', 'K1': '.claude/rules/backend/dependencies.md'}
SKILL = '.claude/skills/add-dependency/SKILL.md'
VERIFY = '.claude/skills/verify/SKILL.md'
EVAL_ERR = 'effective ManagePackageVersionsCentrally is'


def proj(body=''):
    return '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup>%s</Project>' % body


def central(prop=T, items=''):
    return '<Project>%s%s</Project>' % (prop, ('<ItemGroup>%s</ItemGroup>' % items) if items else '')


REF = '<ItemGroup><PackageReference Include="A.B" /></ItemGroup>'
PV = '<PackageVersion Include="A.B" Version="1.2.3" />'
COND = "'$(Unset)' == ''"
COND_OFF = "'$(Unset)' == 'x'"
MT = '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFrameworks>net8.0;net10.0</TargetFrameworks></PropertyGroup>%s</Project>'

# name, files, expected outcome, phrases the output must hold, value the default-context evaluation must give (None: skip)
CASES = [
    ('true set in the central manifest', {'Directory.Packages.props': central()}, 'OK', [], 'true'),
    ('inherited true from Directory.Build.props', {'Directory.Build.props': '<Project>%s</Project>' % T, 'Directory.Packages.props': EMPTY}, 'OK', [], 'true'),
    ('inherited true through an import', {'Directory.Build.props': '<Project><Import Project="shared/cpm.props" /></Project>', 'shared/cpm.props': '<Project>%s</Project>' % T, 'Directory.Packages.props': EMPTY}, 'OK', [], 'true'),
    ('false at the parent, central manifest evaluates later and sets true', {'Directory.Build.props': '<Project>%s</Project>' % F, 'Directory.Packages.props': central()}, 'OK', [], 'true'),
    ('false at the parent with nothing after it', {'Directory.Build.props': '<Project>%s</Project>' % F, 'Directory.Packages.props': EMPTY}, 'ERROR', [EVAL_ERR, '"false"'], 'false'),
    ('project overrides true with false', {'Directory.Packages.props': central(), PROJ: proj(F)}, 'ERROR', [EVAL_ERR, '"false"', 'App.Api'], 'false'),
    ('Directory.Build.targets turns it off after the project', {'Directory.Packages.props': central(), 'Directory.Build.targets': '<Project>%s</Project>' % F}, 'ERROR', [EVAL_ERR, '"false"'], 'false'),
    ('conditional true that evaluates true', {'Directory.Packages.props': '<Project><PropertyGroup Condition="%s"><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup></Project>' % COND}, 'OK', [], 'true'),
    ('conditional true that evaluates false', {'Directory.Packages.props': '<Project><PropertyGroup Condition="%s"><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup></Project>' % COND_OFF}, 'ERROR', [EVAL_ERR, '"unset"'], ''),
    ('conditional false that evaluates true disables it', {'Directory.Packages.props': '<Project>%s<PropertyGroup Condition="%s"><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup></Project>' % (T, COND)}, 'ERROR', [EVAL_ERR, '"false"'], 'false'),
    ('conditional false that evaluates false stays true', {'Directory.Packages.props': '<Project>%s<PropertyGroup Condition="%s"><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup></Project>' % (T, COND_OFF)}, 'OK', [], 'true'),
    ('conflicting imports: the later import wins and disables it', {'Directory.Build.props': '<Project><Import Project="shared/on.props" /><Import Project="shared/off.props" /></Project>', 'shared/on.props': '<Project>%s</Project>' % T, 'shared/off.props': '<Project>%s</Project>' % F, 'Directory.Packages.props': EMPTY}, 'ERROR', [EVAL_ERR, '"false"'], 'false'),
    ('conflicting imports: the later import wins and enables it', {'Directory.Build.props': '<Project><Import Project="shared/off.props" /><Import Project="shared/on.props" /></Project>', 'shared/on.props': '<Project>%s</Project>' % T, 'shared/off.props': '<Project>%s</Project>' % F, 'Directory.Packages.props': EMPTY}, 'OK', [], 'true'),
    ('central declaration with a versionless PackageReference', {'Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, 'OK', [], 'true'),
    ('version incorrectly pinned in a project', {'Directory.Packages.props': central(T, PV), PROJ: proj('<ItemGroup><PackageReference Include="A.B" Version="9.9.9" /></ItemGroup>')}, 'ERROR', ['A.B'], 'true'),
    ('version pinned through an inherited file only MSBuild can see', {'Directory.Packages.props': central(T, PV), 'Directory.Build.targets': '<Project><ItemGroup><PackageReference Update="A.B" Version="9.9.9" /></ItemGroup></Project>', PROJ: proj(REF)}, 'ERROR', ['effective PackageReference A.B has version 9.9.9'], 'true'),
    ('versionless reference with no central declaration', {'Directory.Packages.props': central(), PROJ: proj(REF)}, 'ERROR', ['effective PackageReference A.B has no PackageVersion'], 'true'),
    ('missing central manifest with true inherited', {'Directory.Build.props': '<Project>%s</Project>' % T}, 'ERROR', ['Directory.Packages.props is not imported'], 'true'),
    ('central manifest import switched off', {'Directory.Build.props': '<Project><PropertyGroup><ImportDirectoryPackagesProps>false</ImportDirectoryPackagesProps></PropertyGroup></Project>', 'Directory.Packages.props': central()}, 'ERROR', [EVAL_ERR], ''),
    ('malformed central manifest fails closed', {'Directory.Packages.props': '<Project><PropertyGroup><Manage'}, 'ERROR', ['could not be evaluated by MSBuild'], None),
    ('multiple projects evaluate differently', {'Directory.Packages.props': central(), PROJ2: proj(F)}, 'ERROR', ['App.Application', EVAL_ERR], 'true'),
    ('literal true in a comment is ineffective', {'Directory.Packages.props': '<Project><!-- %s --></Project>' % T}, 'ERROR', [EVAL_ERR, '"unset"'], ''),
    ('literal true in a file MSBuild never imports is ineffective', {'Directory.Packages.props': EMPTY, 'docs/old/Directory.Packages.props': central()}, 'ERROR', [EVAL_ERR, '"unset"'], ''),
    ('release-only false is found', {'Directory.Packages.props': '<Project>%s<PropertyGroup Condition="\'$(Configuration)\' == \'Release\'"><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup></Project>' % T}, 'ERROR', [EVAL_ERR, 'Configuration=Release'], 'true'),
    ('one target framework turns it off', {'Directory.Packages.props': central(), PROJ: MT % '<PropertyGroup Condition="\'$(TargetFramework)\' == \'net8.0\'"><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup>'}, 'ERROR', [EVAL_ERR, 'TargetFramework=net8.0'], 'true'),
    ('value in another case', {'Directory.Packages.props': '<Project><PropertyGroup><ManagePackageVersionsCentrally>True</ManagePackageVersionsCentrally></PropertyGroup></Project>'}, 'OK', [], 'true'),
]


def hermetic(root, no_dotnet=False):
    e = env_for(root)
    e.update({'DOTNET_CLI_HOME': scratch_dir('dotnethome'), 'DOTNET_NOLOGO': '1', 'DOTNET_CLI_TELEMETRY_OPTOUT': '1', 'DOTNET_SKIP_FIRST_TIME_EXPERIENCE': '1', 'NUGET_PACKAGES': scratch_dir('nuget'), 'MSBuildEnableWorkloadResolver': 'false'})
    if no_dotnet:
        e['PATH'] = os.pathsep.join(p for p in e.get('PATH', '').split(os.pathsep) if p and not os.path.exists(os.path.join(p, 'dotnet.exe')) and not os.path.exists(os.path.join(p, 'dotnet')))
    return e


NODE = shutil.which('node')


def node(root, args, stdin=None, no_dotnet=False, timeout=420):
    feed = {'input': stdin} if stdin is not None else {'stdin': subprocess.DEVNULL}
    r = subprocess.run([NODE] + args, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=hermetic(root, no_dotnet), timeout=timeout, **feed)
    return r.returncode, r.stdout + r.stderr


def build(c, files):
    root = fresh_copy(c, 'cpm')
    for rel in ('Directory.Build.props', 'Directory.Packages.props'):
        p = os.path.join(root, rel)
        if os.path.exists(p):
            os.remove(p)
    all_files = {PROJ: proj()}
    all_files.update(files)
    for rel, body in all_files.items():
        p = os.path.join(root, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)
    return root


def check(c, root, no_dotnet=False):
    args = [a.replace('{root}', root) for a in RUN[c]]
    return node(root, args, None, no_dotnet)


def outcome(code):
    return {0: 'OK', 1: 'ERROR', 3: 'NOT_RUN'}.get(code, 'EXIT_%s' % code)


def msbuild_value(root, rel=PROJ):
    r = subprocess.run(['dotnet', 'msbuild', rel.replace('/', os.sep), '-nologo', '-getProperty:ManagePackageVersionsCentrally'], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=hermetic(root), timeout=180)
    return r.returncode, r.stdout.strip().lower()


def one_case(c, case):
    name, files, want, must, real = case
    root = build(c, files)
    before = {rel: sha256_file(os.path.join(root, rel.replace('/', os.sep))) for rel in walk_files(root)}
    code, out = check(c, root)
    after = {rel: sha256_file(os.path.join(root, rel.replace('/', os.sep))) for rel in walk_files(root)}
    miss = [m for m in must if m not in out]
    res = {'c': c, 'name': name, 'want': want, 'got': outcome(code), 'miss': miss, 'out': out[-500:], 'tree_same': before == after}
    if real is not None:
        rc, val = msbuild_value(root)
        res['real'] = (rc, val, real)
    shutil.rmtree(root, ignore_errors=True)
    return res


def hook_edit(c, root, rel, tool='Edit', no_dotnet=False):
    payload = json.dumps({'hook_event_name': 'PostToolUse', 'session_id': 'fixture', 'tool_name': tool, 'tool_input': {'file_path': os.path.join(root, rel.replace('/', os.sep)), 'old_string': 'x', 'new_string': 'y'}, 'tool_response': {'success': True}, 'cwd': root})
    return node(root, HOOK[c], payload, no_dotnet, 180)


def restore_codes(files):
    root = os.path.join(SCRATCH, 'runs', 'restore-' + uuid.uuid4().hex[:8])
    all_files = {PROJ: proj(REF), 'nuget.config': '<configuration><packageSources><clear /><add key="local" value="feed" /></packageSources></configuration>'}
    all_files.update(files)
    for rel, body in all_files.items():
        p = os.path.join(root, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)
    os.makedirs(os.path.join(root, 'feed'), exist_ok=True)
    r = subprocess.run(['dotnet', 'restore', PROJ.replace('/', os.sep), '-nologo', '--configfile', 'nuget.config'], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=hermetic(root), timeout=240)
    shutil.rmtree(root, ignore_errors=True)
    return sorted(set(re.findall(r'\b(NU\d{4})\b', r.stdout + r.stderr)))


def run(ctx):
    if shutil.which('dotnet') is None:
        ctx.not_run('all effective-state fixtures', '.NET SDK not on PATH')
        return
    jobs = [(c, case) for c in CANDIDATES for case in CASES]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda j: one_case(*j), jobs))
    verdicts = {}
    for r in results:
        ok = r['got'] == r['want'] and not r['miss']
        ctx.check('fixture: %s' % r['name'], ok, 'missing=%s output=%s' % (r['miss'], r['out']), r['c'], 'CHECKER', r['want'], r['got'])
        ctx.check('evaluation left the fixture tree unchanged: %s' % r['name'], r['tree_same'], candidate=r['c'], kind='CHECKER')
        if 'real' in r:
            rc, val, real = r['real']
            ctx.check('MSBuild directly agrees: %s' % r['name'], rc == 0 and val == real, '%s %s' % (rc, val), r['c'], 'MSBUILD', real, val)
        verdicts.setdefault(r['name'], {})[r['c']] = r['got']
    for name, row in verdicts.items():
        ctx.check('six-way parity: %s' % name, len(set(row.values())) == 1, row, kind='PARITY', actual=row)

    def per_candidate(c):
        rows = []
        # No SDK: never a pass, no static fallback.
        root = build(c, {'Directory.Packages.props': central(T, PV), PROJ: proj(REF)})
        code, out = check(c, root, no_dotnet=True)
        rows.append(('no SDK: exit 3, NOT_RUN, not a pass', outcome(code) == 'NOT_RUN' and 'NOT_RUN' in out, out[-300:]))
        rows.append(('no SDK: the output tells the reader not to count it as passed', 'NOT RUN' in out and 'not as passed' in out, out[-300:]))
        # A real violation is still found without the SDK when it is literal in the project: static checks stay.
        root2 = build(c, {'Directory.Packages.props': central(T, PV), PROJ: proj('<ItemGroup><PackageReference Include="A.B" Version="9.9.9" /></ItemGroup>')})
        code, out = check(c, root2, no_dotnet=True)
        rows.append(('no SDK: a literal version in a project is still a violation', outcome(code) == 'ERROR', out[-300:]))
        # No project at all: not applicable, no SDK needed. The shipped template is this case.
        root3 = fresh_copy(c, 'cpm')
        code, out = check(c, root3, no_dotnet=True)
        rows.append(('no project in scope: exit 0 and dotnet is not needed', outcome(code) == 'OK' and 'NOT_RUN' not in out, out[-300:]))
        # Routing: an unrelated edit never requires dotnet.
        root4 = build(c, {'Directory.Packages.props': central()})
        for rel, body in (('src/note.txt', 'x'), ('backend/App.Api/Foo.cs', 'class Foo {}'), ('frontend/App.Web/package.json', '{"name":"a","private":true}')):
            p = os.path.join(root4, rel.replace('/', os.sep))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(body)
            code, out = hook_edit(c, root4, rel, no_dotnet=True)
            rows.append(('routing: editing %s does not ask for dotnet' % rel.split('/')[-1], 'NOT_RUN' not in out, out[-300:]))
        # Routing: chain files do reach the evaluator.
        root5 = build(c, {'Directory.Packages.props': central()})
        for rel, body in (('Directory.Build.targets', '<Project>%s</Project>' % F),):
            with open(os.path.join(root5, rel), 'w', encoding='utf-8', newline='\n') as f:
                f.write(body)
            code, out = hook_edit(c, root5, rel)
            rows.append(('routing: editing %s reaches the evaluator and reports the effective false' % rel, EVAL_ERR in out and re.search(r'is \\*"false', out) is not None, out[-400:]))
        root6 = build(c, {'Directory.Packages.props': central(), PROJ: proj(F)})
        code, out = hook_edit(c, root6, PROJ)
        rows.append(('routing: editing the project reports its effective false', EVAL_ERR in out, out[-400:]))
        root7 = build(c, {'Directory.Packages.props': central()})
        code, out = hook_edit(c, root7, PROJ)
        rows.append(('routing: editing a compliant project reports no violation', EVAL_ERR not in out and 'not imported' not in out, out[-300:]))
        code, out = hook_edit(c, root7, PROJ, no_dotnet=True)
        rows.append(('routing: a hook without the SDK reports NOT_RUN instead of passing silently', 'NOT_RUN' in out, out[-300:]))
        # DEP-003 interaction: the default still rejects; the recorded entry is honored; the switch is named, and does not widen anything.
        rec = {'exceptions': [{'ecosystem': 'nuget', 'package': 'A.B', 'version': '1.*', 'manifest': 'Directory.Packages.props', 'requested_by': 'user', 'request': 'User asked for A.B at 1.* on 2026-11-03', 'date': '2026-11-03'}]}
        floatv = '<PackageVersion Include="A.B" Version="1.*" /><PackageVersion Include="C.D" Version="2.*" />'
        root8 = build(c, {'Directory.Packages.props': central(T, floatv), PROJ: proj(REF), 'dependency-version-exceptions.json': json.dumps(rec)})
        code, out = check(c, root8)
        low = out.lower()
        rows.append(('DEP-003: recorded floating version is accepted by the static check', not any('A.B' in l and 'floating' in l.lower() and 'approved' not in l.lower() for l in out.splitlines()), out[-400:]))
        rows.append(('DEP-003: an unrecorded floating version stays rejected under effective CPM', any('C.D' in l and 'floating' in l.lower() for l in out.splitlines()) and outcome(code) == 'ERROR', out[-400:]))
        rows.append(('DEP-003: the checker names the NuGet switch the recorded version needs', 'CentralPackageFloatingVersionsEnabled' in out and 'NU1011' in out, out[-400:]))
        switch = '<PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally><CentralPackageFloatingVersionsEnabled>true</CentralPackageFloatingVersionsEnabled></PropertyGroup>'
        root9 = build(c, {'Directory.Packages.props': central(switch, floatv), PROJ: proj(REF), 'dependency-version-exceptions.json': json.dumps(rec)})
        code, out = check(c, root9)
        rows.append(('DEP-003: with the switch on, the notice stops and the unrecorded version is still rejected', 'NU1011' not in out and any('C.D' in l and 'floating' in l.lower() for l in out.splitlines()) and outcome(code) == 'ERROR', out[-400:]))
        for root_x in (root, root2, root3, root4, root5, root6, root7, root8, root9):
            shutil.rmtree(root_x, ignore_errors=True)
        return c, rows
    with ThreadPoolExecutor(max_workers=6) as ex:
        for c, rows in ex.map(per_candidate, CANDIDATES):
            for name, cond, detail in rows:
                ctx.check(name, cond, detail, c, 'CHECKER')
    # Text owners and the route to the proof.
    for c in CANDIDATES:
        post(ctx, c, 'dependency owner states the effective setting', RULE[c], ['effective `ManagePackageVersionsCentrally`'])
        post(ctx, c, 'add-dependency names the NuGet switch for a recorded floating version, without widening the exception', SKILL, ['`CentralPackageFloatingVersionsEnabled`', 'NU1011', 'does not widen'])
        post(ctx, c, 'verify says exit 3 is NOT RUN', VERIFY, ['exit code 3', 'NOT RUN'])
    # Mutations: each checker loses the behavior on a copy, and the fixtures notice.
    def mutation(c):
        rows = []
        rel = CHECKER_FILE[c]
        m = mutate_text(c, rel, "if (value !== 'true') {", "if (false) {")
        if m:
            for p in ('Directory.Build.props',):
                if os.path.exists(os.path.join(m, p)):
                    os.remove(os.path.join(m, p))
            for relp, body in ((PROJ, proj(F)), ('Directory.Packages.props', central())):
                fp = os.path.join(m, relp.replace('/', os.sep))
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(body)
            code, out = check(c, m)
            rows.append(('mutation: ignoring an effective false lets a disabled project through', m is not None and outcome(code) == 'OK', out[-200:]))
        else:
            rows.append(('mutation: ignoring an effective false lets a disabled project through', False, 'mutation anchor not found'))
        m = mutate_text(c, rel, "if (run.error) return { notRun:", "if (run.error) return { state: { Properties: { ManagePackageVersionsCentrally: 'true', CentralPackageVersionsFileImported: 'true' }, Items: {} } }; if (run.error) return { notRun:")
        if m:
            for p in ('Directory.Build.props',):
                if os.path.exists(os.path.join(m, p)):
                    os.remove(os.path.join(m, p))
            for relp, body in ((PROJ, proj()), ('Directory.Packages.props', central())):
                fp = os.path.join(m, relp.replace('/', os.sep))
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(body)
            code, out = check(c, m, no_dotnet=True)
            rows.append(('mutation: a permissive fallback with no SDK reads as a pass, which the NOT_RUN fixture rejects', outcome(code) == 'OK', out[-200:]))
        else:
            rows.append(('mutation: a permissive fallback with no SDK reads as a pass, which the NOT_RUN fixture rejects', False, 'mutation anchor not found'))
        m = mutate_text(c, rel, "if ((props.CentralPackageVersionsFileImported || '').trim().toLowerCase() !== 'true') {", "if (false) {")
        if m:
            for p in ('Directory.Packages.props',):
                if os.path.exists(os.path.join(m, p)):
                    os.remove(os.path.join(m, p))
            for relp, body in ((PROJ, proj()), ('Directory.Build.props', '<Project>%s</Project>' % T)):
                fp = os.path.join(m, relp.replace('/', os.sep))
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(body)
            code, out = check(c, m)
            rows.append(('mutation: dropping the central-manifest check accepts true with no manifest', 'not imported' not in out, out[-200:]))
        else:
            rows.append(('mutation: dropping the central-manifest check accepts true with no manifest', False, 'mutation anchor not found'))
        return c, rows
    with ThreadPoolExecutor(max_workers=6) as ex:
        for c, rows in ex.map(mutation, CANDIDATES):
            for name, cond, detail in rows:
                ctx.check(name, cond, detail, c, 'MUTATION')
    # NuGet itself, offline: the facts the contract rests on. Empty local feed; no package is downloaded.
    pv = central(T, PV)
    facts = [('floating central version without the switch', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" Version="1.*" />')}, 'NU1011'), ('version in a project under CPM', {'Directory.Packages.props': pv, PROJ: proj('<ItemGroup><PackageReference Include="A.B" Version="1.2.3" /></ItemGroup>')}, 'NU1008'), ('reference with no central declaration', {'Directory.Packages.props': central()}, 'NU1010'), ('CPM true with no central file', {'Directory.Build.props': '<Project>%s</Project>' % T}, 'NU1015')]
    for name, files, code in facts:
        got = restore_codes(files)
        ctx.check('offline NuGet restore: %s gives %s' % (name, code), code in got, got, kind='NUGET_OFFLINE', expect=code, actual=got)
    got = restore_codes({'Directory.Packages.props': central('<PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally><CentralPackageFloatingVersionsEnabled>true</CentralPackageFloatingVersionsEnabled></PropertyGroup>', '<PackageVersion Include="A.B" Version="1.*" />')})
    ctx.check('offline NuGet restore: with the switch on, NU1011 is gone', 'NU1011' not in got, got, kind='NUGET_OFFLINE', actual=got)
    ctx.not_run('a restore that resolves a real floating package from a registry', 'no network in this run; the offline restore observes the CPM errors only')
