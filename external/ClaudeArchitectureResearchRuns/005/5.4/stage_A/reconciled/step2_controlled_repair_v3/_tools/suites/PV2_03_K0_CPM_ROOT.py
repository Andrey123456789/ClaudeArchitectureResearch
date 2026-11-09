"""PV2-03 regression: no candidate requires Directory.Packages.props at the repository root; every candidate still requires effective
Central Package Management per project (kit 74 Part B PV2-03).

Fixtures are real MSBuild projects; each candidate's own repository checker runs on them (the C01 machinery: hermetic .NET SDK, no restore).
When the SDK is missing an outcome is NOT_RUN, never a pass.
"""
import os
import re
import shutil

from rcommon import CANDIDATES, norm_ws, read_lines, template_root, walk_files, wc_path
from suitelib import has
from suites_loader import load_suite

RULE = 'PV2-03-K0-CPM-ROOT'


def fixtures(c01):
    T, F, PV, REF, PROJ, proj, central = c01.T, c01.F, c01.PV, c01.REF, c01.PROJ, c01.proj, c01.central
    off = '<PropertyGroup><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup>'
    return [
        ('nested central file manages every project', {'backend/Directory.Packages.props': central(T, PV), PROJ: proj(REF), 'backend/App.Domain/App.Domain.csproj': proj()}, 'OK'),
        ('two areas, each with its own nested central file', {'backend/Directory.Packages.props': central(T, PV), PROJ: proj(REF), 'tools/Directory.Packages.props': central(T, PV), 'tools/Tool/Tool.csproj': proj(REF)}, 'OK'),
        ('nested central file enabled through a nested Directory.Build.props', {'backend/Directory.Build.props': '<Project>%s</Project>' % T, 'backend/Directory.Packages.props': '<Project><ItemGroup>%s</ItemGroup></Project>' % PV, PROJ: proj(REF)}, 'OK'),
        ('root central file, the typical layout', {'Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, 'OK'),
        ('a project outside the nested central file', {'backend/Directory.Packages.props': central(T, PV), PROJ: proj(REF), 'tools/Tool/Tool.csproj': proj(REF)}, 'ERROR'),
        ('nested central file turns CPM off', {'backend/Directory.Packages.props': central(F, PV), PROJ: proj(REF)}, 'ERROR'),
        ('the project overrides CPM with false', {'backend/Directory.Packages.props': central(T, PV), PROJ: proj(off + REF)}, 'ERROR'),
        ('a version in the project file under a nested central file', {'backend/Directory.Packages.props': central(T, PV), PROJ: proj('<ItemGroup><PackageReference Include="A.B" Version="1.2.3" /></ItemGroup>')}, 'ERROR'),
        ('malformed XML in the nested central file', {'backend/Directory.Packages.props': '<Project>%s<ItemGroup><PackageVersion Include="A.B" Version="1.2.3" </ItemGroup></Project>' % T, PROJ: proj(REF)}, 'ERROR'),
    ]


# Found by v3 testing, pre-existing and location-independent: a PackageVersion with no Version passed M1 and K0 and errored in the other
# four (Q-10). Until V3-Q10 this row held that state unchanged by PV2-03; V3-Q10 (approved semantics) removed the difference, so the
# row now requires ERROR in all six, at the root and nested. Stricter; the negative is V3-Q10's mutations.
NO_VERSION_EXPECTED = {c: 'ERROR' for c in CANDIDATES}


def no_version_rows(c01):
    T, REF, PROJ, proj, central = c01.T, c01.REF, c01.PROJ, c01.proj, c01.central
    return [('a PackageVersion with no Version, root file', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" />'), PROJ: proj(REF)}),
            ('a PackageVersion with no Version, nested file', {'backend/Directory.Packages.props': central(T, '<PackageVersion Include="A.B" />'), PROJ: proj(REF)})]


def run(ctx):
    c01 = load_suite('C01_CPM_EFFECTIVE')
    table = {}
    for name, files, want in fixtures(c01):
        row = {}
        for c in CANDIDATES:
            root = c01.build(c, files)
            code, out = c01.check(c, root)
            got = c01.outcome(code)
            row[c] = got
            if got == 'NOT_RUN':
                ctx.not_run('%s (expected %s)' % (name, want), 'the .NET SDK proof did not run: %s' % out[-160:].replace(root, '<fixture>'), c, 'RUNTIME')
            else:
                ctx.check('%s: %s' % (name, want), got == want, out[-260:].replace(root, '<fixture>'), c, 'CHECKER', want, got)
            if c == 'K0':
                ctx.check('%s: K0 never asks for the repository root' % name, 'missing at the repository root' not in out, out[-200:].replace(root, '<fixture>'), 'K0', 'CHECKER')
                if name == 'a project outside the nested central file':
                    ctx.check('K0 names the project that has no central file above it', 'tools/Tool/Tool.csproj: no Directory.Packages.props in its directory or any parent' in out, out[-300:].replace(root, '<fixture>'), 'K0', 'CHECKER')
            shutil.rmtree(root, ignore_errors=True)
        table[name] = row
        done = {v for v in row.values() if v != 'NOT_RUN'}
        ctx.check('same task, six candidates: %s' % name, done == {want} or not done, row, kind='CHECKER', expect=want, actual=row)
    for name, files in no_version_rows(c01):
        row = {}
        for c in CANDIDATES:
            root = c01.build(c, files)
            row[c] = c01.outcome(c01.check(c, root)[0])
            shutil.rmtree(root, ignore_errors=True)
        table[name] = row
        if 'NOT_RUN' in row.values():
            ctx.not_run('documented difference: %s' % name, 'the .NET SDK proof did not run', None, 'RUNTIME')
        else:
            ctx.check('invalid package metadata (no Version) errors in all six since V3-Q10: %s' % name, row == NO_VERSION_EXPECTED, row, kind='CHECKER', expect=NO_VERSION_EXPECTED, actual=row)
    # Authoritative text: root is typical, not required; the CPM obligation stays.
    ctx.check('K0 D-17 says any location MSBuild imports for each project is valid', has('K0', 'docs/architecture/decision-register.md', 'typically at the repository root; any location MSBuild imports for each project is valid'), candidate='K0', kind='SOURCE')
    ctx.check('K0 NuGet rule: nested central file equally valid; effective CPM per project still required', has('K0', '.claude/rules/common/dependencies.md', 'a nested one that MSBuild imports for each project is equally valid') and has('K0', '.claude/rules/common/dependencies.md', 'the effective `ManagePackageVersionsCentrally` must be true for each project'), candidate='K0', kind='SOURCE')
    stale = [rel for rel in walk_files(template_root('K0')) if rel.endswith(('.md', '.cjs', '.json')) and re.search(r'missing at the repository root|must (be|reside|live) at the repository root', norm_ws(' '.join(read_lines(wc_path('K0', rel)))), re.I)]
    ctx.check('no K0 file still states a repository-root mandate for the central file', not stale, stale[:4], 'K0', 'SOURCE')
    for c in CANDIDATES:
        ctx.check('the CPM evaluator from C01 is still present', has(c, c01.CHECKER_FILE[c], 'Effective Central Package Management (DEP-006)'), candidate=c, kind='SOURCE')
    # Mutation: a root-only check put back must be caught by the nested positive fixture.
    name, files, want = fixtures(c01)[0]
    root = c01.build('K0', files)
    p = os.path.join(root, '.claude', 'scripts', 'check-dependencies.cjs')
    with open(p, encoding='utf-8', newline='') as f:
        s = f.read()
    anchor = "  for (const project of files.filter((f) => f.endsWith('.csproj'))) {"
    if anchor in s:
        s = s.replace(anchor, "  if (files.some((f) => f.endsWith('.csproj')) && !files.includes('Directory.Packages.props')) total.errors.push('Directory.Packages.props is missing at the repository root (D-17).');\n" + anchor, 1)
        with open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(s)
        got = c01.outcome(c01.check('K0', root)[0])
        ctx.check('mutation: a root-only requirement put back is caught (nested positive fixture errors)', got == 'ERROR', got, 'K0', 'MUTATION', 'ERROR', got)
    else:
        ctx.check('mutation anchor present in K0 checker', False, anchor, 'K0', 'MUTATION')
    shutil.rmtree(root, ignore_errors=True)
    ctx.not_run('a NuGet restore against a real registry for the nested layouts', 'no package registry in this run; MSBuild evaluation without restore', 'K0')
