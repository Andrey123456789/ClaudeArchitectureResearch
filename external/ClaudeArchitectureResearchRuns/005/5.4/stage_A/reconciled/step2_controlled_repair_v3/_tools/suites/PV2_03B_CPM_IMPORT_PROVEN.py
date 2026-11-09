"""PV2-03B regression: a central file that MSBuild imports for a project from outside the project's ancestor folders
(DirectoryPackagesPropsPath, the SDK's own mechanism) is accepted by all six checkers when MSBuild proves CPM on and the file imported.
Every configuration that is not effective CPM still errors in all six.

Real MSBuild and the C01 machinery (each candidate's own repository checker and post-edit hook, hermetic .NET SDK, no network).
NuGet's own offline restore against an empty local feed shows which fixtures NuGet itself treats as CPM (NU1008 for a pinned project
version) and which it does not (NU1015). With no SDK, an outcome is NOT_RUN, never a pass.
"""
import json
import os
import shutil
import subprocess

from rcommon import CANDIDATES
from suitelib import has, mutate_text
from suites_loader import load_suite

RULE = 'PV2-03B-CPM-IMPORT-PROVEN'
M_STATIC = 'no Directory.Packages.props was found above this project'
K0_STATIC = 'no Directory.Packages.props in its directory or any parent up to the repository root'
NOT_IMPORTED = 'Directory.Packages.props is not imported'


def fixtures(c01):
    T, F, PV, REF, PROJ, proj, central = c01.T, c01.F, c01.PV, c01.REF, c01.PROJ, c01.proj, c01.central
    dpp = '<Project><PropertyGroup><DirectoryPackagesPropsPath>$(MSBuildThisFileDirectory)%s</DirectoryPackagesPropsPath></PropertyGroup></Project>'
    pin = '<ItemGroup><PackageReference Include="A.B" Version="9.9.9" /></ItemGroup>'
    return [
        ('central file outside every project ancestor, named by DirectoryPackagesPropsPath', {'Directory.Build.props': dpp % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, 'OK', 'NU1008'),
        ('two projects in different folders, one central file in a sibling folder', {'Directory.Build.props': dpp % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF), 'tools/Tool/Tool.csproj': proj(REF)}, 'OK', None),
        ('central file with another name, named by DirectoryPackagesPropsPath', {'Directory.Build.props': dpp % 'config/Packages.props', 'config/Packages.props': central(T, PV), PROJ: proj(REF)}, 'OK', 'NU1008'),
        ('DirectoryPackagesPropsPath set in a nested Directory.Build.props', {'backend/Directory.Build.props': dpp % '../config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, 'OK', None),
        ('the project file itself imports config/Directory.Packages.props (not marked imported by the SDK)', {'config/Directory.Packages.props': central(T, PV), PROJ: proj('<Import Project="../../config/Directory.Packages.props" />' + REF)}, 'ERROR', 'NU1015'),
        ('plain Import of a non-ancestor central file from Directory.Build.props', {'Directory.Build.props': '<Project><Import Project="config/Directory.Packages.props" /></Project>', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, 'ERROR', 'NU1015'),
        ('DirectoryPackagesPropsPath names a missing file, CPM set true elsewhere', {'Directory.Build.props': '<Project><PropertyGroup><DirectoryPackagesPropsPath>$(MSBuildThisFileDirectory)config/Directory.Packages.props</DirectoryPackagesPropsPath><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup></Project>', PROJ: proj(REF)}, 'ERROR', None),
        ('non-ancestor central file turns CPM off', {'Directory.Build.props': dpp % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(F, PV), PROJ: proj(REF)}, 'ERROR', None),
        ('non-ancestor central file, the project pins a version', {'Directory.Build.props': dpp % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(pin)}, 'ERROR', None),
        ('a second project outside the path the central file covers', {'backend/Directory.Build.props': dpp % '../config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF), 'tools/Tool/Tool.csproj': proj(REF)}, 'ERROR', None),
    ]


def place(root, files):
    for rel in ('Directory.Build.props', 'Directory.Packages.props'):
        p = os.path.join(root, rel)
        if os.path.exists(p):
            os.remove(p)
    for rel, body in files.items():
        p = os.path.join(root, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)


def run(ctx):
    c01 = load_suite('C01_CPM_EFFECTIVE')
    if shutil.which('dotnet') is None:
        ctx.not_run('all PV2-03B fixtures', '.NET SDK not on PATH')
        return
    fx = fixtures(c01)
    for name, files, want, nuget in fx:
        root = c01.build('K0', files)
        props = {}
        r = subprocess.run(['dotnet', 'msbuild', c01.PROJ.replace('/', os.sep), '-nologo', '-getProperty:ManagePackageVersionsCentrally', '-getProperty:CentralPackageVersionsFileImported'], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=c01.hermetic(root), timeout=180)
        if r.returncode == 0:
            props = json.loads(r.stdout).get('Properties', {})
        shutil.rmtree(root, ignore_errors=True)
        proven = props.get('ManagePackageVersionsCentrally', '').lower() == 'true' and props.get('CentralPackageVersionsFileImported', '').lower() == 'true'
        if want == 'OK':
            ctx.check('MSBuild directly: CPM on and the central file imported: %s' % name, proven, props, kind='MSBUILD')
        if nuget:
            pinned = nuget == 'NU1008'
            body = '<ItemGroup><PackageReference Include="A.B" Version="9.9.9" /></ItemGroup>' if pinned else None
            files2 = dict(files)
            if body:
                files2[c01.PROJ] = c01.proj(body)
            codes = c01.restore_codes({k: v for k, v in files2.items()})
            ctx.check('NuGet restore (offline, empty feed) shows %s: %s' % (nuget, name), nuget in codes, codes, kind='NUGET', expect=nuget, actual=codes)
    rows = {}
    for name, files, want, _ in fx:
        row = {}
        for c in CANDIDATES:
            root = c01.build(c, files)
            code, out = c01.check(c, root)
            got = c01.outcome(code)
            row[c] = got
            if got == 'NOT_RUN':
                ctx.not_run('%s (expected %s)' % (name, want), 'the .NET SDK proof did not run: %s' % out[-160:].replace(root, '<fixture>'), c, 'RUNTIME')
            else:
                ctx.check('%s: %s' % (name, want), got == want, out[-300:].replace(root, '<fixture>'), c, 'CHECKER', want, got)
            if want == 'OK':
                hcode, hout = c01.hook_edit(c, root, c01.PROJ)
                ctx.check('post-edit hook on the project does not report a missing central file: %s' % name, M_STATIC not in hout and K0_STATIC not in hout and NOT_IMPORTED not in hout, hout[-300:].replace(root, '<fixture>'), c, 'CHECKER')
            if want == 'ERROR' and 'not marked imported' in name:
                ctx.check('the evaluator names the missing import: %s' % name, NOT_IMPORTED in out, out[-300:].replace(root, '<fixture>'), c, 'CHECKER')
            shutil.rmtree(root, ignore_errors=True)
        rows[name] = row
        done = {v for v in row.values() if v != 'NOT_RUN'}
        ctx.check('same task, six candidates: %s' % name, done == {want} or not done, row, kind='PARITY', expect=want, actual=row)
    # No SDK: K0 and M keep their static fallback (an error); the other four report NOT_RUN. Never a pass.
    nofile = {c01.PROJ: c01.proj(c01.REF)}
    for c in CANDIDATES:
        root = c01.build(c, nofile)
        code, out = c01.check(c, root, no_dotnet=True)
        got = c01.outcome(code)
        want = 'ERROR' if c in ('K0', 'M') else 'NOT_RUN'
        ctx.check('no SDK, no central file anywhere: %s, never a pass' % want, got == want, out[-260:].replace(root, '<fixture>'), c, 'CHECKER', want, got)
        if c in ('K0', 'M'):
            ctx.check('no SDK: the static central-file message still names the project', (K0_STATIC if c == 'K0' else M_STATIC) in out, out[-260:].replace(root, '<fixture>'), c, 'CHECKER')
        shutil.rmtree(root, ignore_errors=True)
    # Source: the static check defers to the proof; messages unchanged; evaluator still present.
    ctx.check('K0 static check defers to the MSBuild proof', has('K0', '.claude/scripts/check-dependencies.cjs', '!centralFileAbove(files, project) && !centralImportProven(effectiveCpm(rootDir, project))'), candidate='K0', kind='SOURCE')
    ctx.check('M static check defers to the MSBuild proof', has('M', '.claude/scripts/check-manifests.mjs', 'if (!centralImportProven(effectiveCpm(root, rel)))'), candidate='M', kind='SOURCE')
    ctx.check('K0 D-17 still says any location MSBuild imports for each project is valid', has('K0', 'docs/architecture/decision-register.md', 'any location MSBuild imports for each project is valid'), candidate='K0', kind='SOURCE')
    for c in CANDIDATES:
        ctx.check('the shared CPM evaluator is still present', has(c, c01.CHECKER_FILE[c], 'Effective Central Package Management (DEP-006)'), candidate=c, kind='SOURCE')
    # Mutations: the proof ignored again (the old unconditional check) must make the first positive fixture error; the static
    # fallback removed must make the no-SDK fixture stop erroring in K0 and M.
    name, files, _, _ = fx[0]
    for c, rel, old, new in (('K0', '.claude/scripts/check-dependencies.cjs', '!centralFileAbove(files, project) && !centralImportProven(effectiveCpm(rootDir, project))', '!centralFileAbove(files, project)'),
                             ('M', '.claude/scripts/check-manifests.mjs', 'if (!centralImportProven(effectiveCpm(root, rel)))', 'if (true)')):
        m = mutate_text(c, rel, old, new)
        if not m:
            ctx.check('mutation anchor present', False, old, c, 'MUTATION')
            continue
        place(m, files)
        got = c01.outcome(c01.check(c, m)[0])
        ctx.check('mutation: ignoring the MSBuild proof makes the valid non-ancestor layout error again (caught)', got == 'ERROR', got, c, 'MUTATION', 'ERROR', got)
        shutil.rmtree(m, ignore_errors=True)
    for c, rel, old, new in (('K0', '.claude/scripts/check-dependencies.cjs', '!centralFileAbove(files, project) && !centralImportProven(effectiveCpm(rootDir, project))', 'false'),
                             ('M', '.claude/scripts/check-manifests.mjs', 'if (!centralImportProven(effectiveCpm(root, rel)))', 'if (false)')):
        m = mutate_text(c, rel, old, new)
        if not m:
            ctx.check('mutation anchor present', False, old, c, 'MUTATION')
            continue
        place(m, nofile)
        got = c01.outcome(c01.check(c, m, no_dotnet=True)[0])
        ctx.check('mutation: dropping the static fallback turns the no-SDK error into NOT_RUN (caught)', got == 'NOT_RUN', got, c, 'MUTATION', 'NOT_RUN', got)
        shutil.rmtree(m, ignore_errors=True)
    ctx.not_run('a NuGet restore against a real registry for the non-ancestor layouts', 'no package registry in this run; offline restore against an empty local feed only', None)
