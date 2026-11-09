"""R08 regression: item 8.2, K0 checker reads the effective ManagePackageVersionsCentrally. Each fixture is also evaluated by the real MSBuild when the .NET SDK is present (no restore, no network), so the static reading is compared with the real one."""
import os
import shutil
import subprocess

from rcommon import SCRATCH
from sandbox import env_for, fresh_copy, run_node, scratch_dir
from suitelib import mutate_text, post

CHECKER = '.claude/scripts/check-dependencies.cjs'
TRUE_PROP = '<PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup>'
FALSE_PROP = '<PropertyGroup><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup>'
EMPTY = '<Project></Project>'
PROJ = 'backend/App.Api/App.Api.csproj'


def proj(body=''):
    return '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup>%s</Project>' % body


# name, files, expected checker verdict on CPM (OK, ERROR, UNPROVEN), expected MSBuild value or None to skip that comparison
CASES = [
    ('declared true in Directory.Packages.props', {'Directory.Packages.props': '<Project>%s</Project>' % TRUE_PROP}, 'OK', 'true'),
    ('inherited true from Directory.Build.props', {'Directory.Build.props': '<Project>%s</Project>' % TRUE_PROP, 'Directory.Packages.props': EMPTY}, 'OK', 'true'),
    ('Directory.Packages.props overrides true with false', {'Directory.Build.props': '<Project>%s</Project>' % TRUE_PROP, 'Directory.Packages.props': '<Project>%s</Project>' % FALSE_PROP}, 'ERROR', 'false'),
    ('Directory.Packages.props overrides false with true', {'Directory.Build.props': '<Project>%s</Project>' % FALSE_PROP, 'Directory.Packages.props': '<Project>%s</Project>' % TRUE_PROP}, 'OK', 'true'),
    ('project file disables it', {'Directory.Packages.props': '<Project>%s</Project>' % TRUE_PROP, PROJ: proj(FALSE_PROP)}, 'ERROR', 'false'),
    ('Directory.Build.targets disables it', {'Directory.Packages.props': '<Project>%s</Project>' % TRUE_PROP, 'Directory.Build.targets': '<Project>%s</Project>' % FALSE_PROP}, 'ERROR', 'false'),
    ('set nowhere', {'Directory.Packages.props': EMPTY}, 'ERROR', ''),
    ('only a comment names it', {'Directory.Packages.props': '<Project><!-- %s --></Project>' % TRUE_PROP}, 'ERROR', ''),
    ('conditional true is unproven', {'Directory.Packages.props': '<Project><PropertyGroup Condition="\'$(Skip)\' == \'\'"><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup></Project>'}, 'UNPROVEN', 'true'),
    ('conditional false may disable', {'Directory.Packages.props': '<Project>%s<PropertyGroup Condition="\'$(Skip)\' == \'\'"><ManagePackageVersionsCentrally>false</ManagePackageVersionsCentrally></PropertyGroup></Project>' % TRUE_PROP}, 'ERROR', 'false'),
    ('import of Directory.Packages.props switched off', {'Directory.Build.props': '<Project><PropertyGroup><ImportDirectoryPackagesProps>false</ImportDirectoryPackagesProps></PropertyGroup></Project>', 'Directory.Packages.props': '<Project>%s</Project>' % TRUE_PROP}, 'ERROR', ''),
    ('value in another case', {'Directory.Packages.props': '<Project><PropertyGroup><ManagePackageVersionsCentrally>True</ManagePackageVersionsCentrally></PropertyGroup></Project>'}, 'OK', 'true'),
    ('nearer Directory.Build.props disables it', {'Directory.Build.props': '<Project>%s</Project>' % TRUE_PROP, 'Directory.Packages.props': EMPTY, 'backend/Directory.Build.props': '<Project>%s</Project>' % FALSE_PROP}, 'ERROR', 'false'),
    ('nearer Directory.Build.props hides the root value', {'Directory.Build.props': '<Project>%s</Project>' % TRUE_PROP, 'Directory.Packages.props': EMPTY, 'backend/Directory.Build.props': EMPTY}, 'ERROR', ''),
    ('nearer Directory.Build.props chains to the root', {'Directory.Build.props': '<Project>%s</Project>' % TRUE_PROP, 'Directory.Packages.props': EMPTY, 'backend/Directory.Build.props': '<Project><Import Project="../Directory.Build.props" /></Project>'}, 'UNPROVEN', 'true'),
]


def build(files):
    root = fresh_copy('K0', 'cpm')
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


def verdict(output):
    cpm = [l for l in output.splitlines() if 'ManagePackageVersionsCentrally' in l]
    if any(l.lstrip().lower().startswith(('error', 'violation')) or ('must be true' in l) or 'effectively' in l for l in cpm):
        return 'ERROR'
    if any('not proven' in l for l in cpm):
        return 'UNPROVEN'
    return 'OK'


def have_sdk():
    return shutil.which('dotnet') is not None


def msbuild_value(root):
    e = env_for(root)
    home = scratch_dir('dotnethome')
    e.update({'DOTNET_CLI_HOME': home, 'DOTNET_NOLOGO': '1', 'DOTNET_CLI_TELEMETRY_OPTOUT': '1', 'DOTNET_SKIP_FIRST_TIME_EXPERIENCE': '1', 'NUGET_PACKAGES': scratch_dir('nuget'), 'MSBuildEnableWorkloadResolver': 'false'})
    r = subprocess.run(['dotnet', 'msbuild', PROJ.replace('/', os.sep), '-getProperty:ManagePackageVersionsCentrally'], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=e, timeout=180)
    return r.returncode, r.stdout.strip().lower(), r.stderr[-300:]


def run(ctx):
    sdk = have_sdk()
    for name, files, want, real in CASES:
        root = build(files)
        code, out, err = run_node(root, [CHECKER, '--root', root])
        got = verdict(out + err)
        ctx.check('checker: %s' % name, got == want, (out + err)[-260:], 'K0', 'CHECKER', want, got)
        if sdk and real is not None:
            rc, val, e = msbuild_value(root)
            ctx.check('real MSBuild agrees: %s' % name, rc == 0 and val == real, '%s %s' % (val, e), 'K0', 'MSBUILD', real, val)
    if not sdk:
        ctx.not_run('real MSBuild comparison', '.NET SDK not on PATH')
    # Central version policy is retained.
    root = build({'Directory.Packages.props': '<Project>%s<ItemGroup><PackageVersion Include="A.B" Version="1.*" /></ItemGroup></Project>' % TRUE_PROP, PROJ: proj('<ItemGroup><PackageReference Include="A.B" Version="1.0.0" /></ItemGroup>')})
    code, out, err = run_node(root, [CHECKER, '--root', root])
    ctx.check('floating central version still rejected', 'floating' in out + err, (out + err)[-200:], 'K0', 'CHECKER')
    ctx.check('versioned PackageReference still rejected', 'has a version' in out + err, (out + err)[-200:], 'K0', 'CHECKER')
    # The shipped template stays clean.
    root = fresh_copy('K0', 'cpm')
    code, out, err = run_node(root, [CHECKER, '--root', root])
    ctx.check('shipped template passes', code == 0, (out + err)[-200:], 'K0', 'CHECKER')
    # Mutation: treat false as true, or restore the literal-only check.
    m = mutate_text('K0', CHECKER, "function reportCpm(rel, effective, result) {", "function reportCpm(rel, effective, result) { return;")
    if m:
        for rel in ('Directory.Build.props',):
            if os.path.exists(os.path.join(m, rel)):
                os.remove(os.path.join(m, rel))
        with open(os.path.join(m, 'Directory.Packages.props'), 'w', encoding='utf-8') as f:
            f.write('<Project>%s</Project>' % FALSE_PROP)
        code, out, err = run_node(m, [CHECKER, '--root', m])
    ctx.check('mutation: accepting an effective false is caught', m is not None and verdict(out + err) != 'ERROR', candidate='K0', kind='MUTATION')
    post(ctx, 'K0', 'dependency rule names the effective setting', '.claude/rules/common/dependencies.md', ['effective'])
