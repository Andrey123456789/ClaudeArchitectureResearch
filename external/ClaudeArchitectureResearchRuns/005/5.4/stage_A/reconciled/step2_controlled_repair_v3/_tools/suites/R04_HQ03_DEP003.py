"""R04 regression: HQ-03 / DEP-003. Executes every candidate's real manifest checker on hermetic fixtures. No network: registry verification is NOT_RUN."""
import json
import os
import shutil

from rcommon import CANDIDATES
from sandbox import CHECKERS, fresh_copy, pre_tool, run_node
from suitelib import mutate_text, post

SKILL = '.claude/skills/add-dependency/SKILL.md'
RECORD = 'dependency-version-exceptions.json'
PKG = 'frontend/App.Web/package.json'
FLOAT_NPM = {'left-pad': '*', 'other-lib': 'latest', 'safe-lib': '1.2.3'}
PROPS_BASE = """<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Float.Package" Version="1.*" />
    <PackageVersion Include="Other.Package" Version="2.*" />
    <PackageVersion Include="Pre.Package" Version="1.0.0-beta.1" />
    <PackageVersion Include="Good.Package" Version="3.1.4" />
  </ItemGroup>
</Project>
"""


def fixture(c, record=None, raw_record=None, deps=FLOAT_NPM):
    root = fresh_copy(c, 'dep')
    d = os.path.join(root, 'frontend', 'App.Web')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'package.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'name': 'app', 'version': '1.0.0', 'private': True, 'dependencies': deps}, f)
    with open(os.path.join(d, 'package-lock.json'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('{}')
    with open(os.path.join(root, 'Directory.Packages.props'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(PROPS_BASE)
    if record is not None or raw_record is not None:
        with open(os.path.join(root, 'dependency-version-exceptions.json'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(raw_record if raw_record is not None else json.dumps({'exceptions': record}))
    return root


def entry(ecosystem='npm', package='left-pad', version='*', manifest=PKG, requested_by='user', request='User asked for left-pad at * in this repository on 2026-11-03', date='2026-11-03'):
    return {'ecosystem': ecosystem, 'package': package, 'version': version, 'manifest': manifest, 'requested_by': requested_by, 'request': request, 'date': date}


def check(c, root):
    """Runs the candidate's real checker. Returns (exit, output)."""
    if c == 'M':
        code, out, err = run_node(root, ['.claude/scripts/check-manifests.mjs'])
    elif c == 'M1':
        code, out, err = run_node(root, ['.claude/scripts/check-manifests.js'])
    elif c == 'L0':
        code, out, err = run_node(root, ['--input-type=module', '-e', "import {scanManifests} from './.claude/hooks/manifest-checks.mjs'; const p=scanManifests(process.cwd()); for (const x of p) console.log(x); process.exit(p.length?1:0)"])
    elif c == 'L1':
        out, err, code = '', '', 0
        for rel in (PKG, 'Directory.Packages.props'):
            payload = json.dumps({'hook_event_name': 'PostToolUse', 'tool_name': 'Write', 'tool_input': {'file_path': os.path.join(root, rel)}, 'cwd': root})
            cd, o, e = run_node(root, ['.claude/hooks/post-change-checks.mjs'], payload)
            out, err, code = out + o, err + e, max(code, 1 if cd == 2 else cd)
    elif c == 'K0':
        code, out, err = run_node(root, ['.claude/scripts/check-dependencies.cjs', '--root', root])
    else:
        code, out, err = run_node(root, ['.claude/scripts/check-manifests.cjs'])
    return code, out + err


def rejected(output, name):
    """A blocking finding names the package with a floating version."""
    for line in output.splitlines():
        if name in line and 'floating' in line.lower() and 'approved' not in line.lower():
            return True
    return False


def prerelease_rejected(output, name):
    for line in output.splitlines():
        if name in line and 'prerelease' in line.lower() and 'approved' not in line.lower():
            return True
    return False


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'add-dependency states the bounded exception', SKILL, ['explicit, bounded user request', 'names the package and the version or range', 'dependency-version-exceptions.json at the repository root', 'accept exactly that entry', 'there is no global switch', 'report the exact version the install resolved'])
        root = fixture(c)
        code, out = check(c, root)
        ctx.check('default: floating npm rejected', rejected(out, 'left-pad') and rejected(out, 'other-lib'), out[-300:], c, 'CHECKER')
        ctx.check('default: floating NuGet rejected', rejected(out, 'Float.Package') and rejected(out, 'Other.Package') or code != 0 and rejected(out, 'Float.Package'), out[-300:], c, 'CHECKER')
        ctx.check('default: exit is non-zero', code != 0, code, c, 'CHECKER')
        root = fixture(c, [entry()])
        code, out = check(c, root)
        ctx.check('authorized npm entry accepted', not rejected(out, 'left-pad'), out[-300:], c, 'CHECKER')
        ctx.check('scope: other floating npm package still rejected', rejected(out, 'other-lib'), out[-300:], c, 'CHECKER')
        ctx.check('scope: floating NuGet still rejected', rejected(out, 'Float.Package'), out[-300:], c, 'CHECKER')
        root = fixture(c, [entry(package='different-lib')])
        ctx.check('wrong package does not leak', rejected(check(c, root)[1], 'left-pad'), candidate=c, kind='CHECKER')
        root = fixture(c, [entry(version='^1.0.0')])
        ctx.check('wrong range does not leak', rejected(check(c, root)[1], 'left-pad'), candidate=c, kind='CHECKER')
        root = fixture(c, [entry(manifest='frontend/Other.Web/package.json')])
        ctx.check('wrong manifest does not leak', rejected(check(c, root)[1], 'left-pad'), candidate=c, kind='CHECKER')
        root = fixture(c, [entry(package='*')])
        o = check(c, root)[1]
        ctx.check('wildcard package record is refused and reported', rejected(o, 'left-pad') and 'exception' in o.lower(), o[-300:], c, 'CHECKER')
        root = fixture(c, [entry(requested_by='assistant')])
        ctx.check('record not from the user is refused', rejected(check(c, root)[1], 'left-pad'), candidate=c, kind='CHECKER')
        root = fixture(c, [entry(request='')])
        ctx.check('record without the request text is refused', rejected(check(c, root)[1], 'left-pad'), candidate=c, kind='CHECKER')
        root = fixture(c, raw_record='{not json')
        code, o = check(c, root)
        ctx.check('malformed record fails closed and is reported', rejected(o, 'left-pad') and code != 0 and 'exception' in o.lower(), o[-300:], c, 'CHECKER')
        root = fixture(c, [entry('nuget', 'float.package', '1.*', 'Directory.Packages.props', request='User asked for Float.Package at 1.* on 2026-11-03')])
        o = check(c, root)[1]
        ctx.check('authorized NuGet entry accepted, case-insensitive id', not rejected(o, 'Float.Package'), o[-300:], c, 'CHECKER')
        ctx.check('scope: other NuGet floating still rejected', rejected(o, 'Other.Package'), o[-300:], c, 'CHECKER')
        root = fixture(c, [entry('nuget', 'Pre.Package', '1.0.0-beta.1', 'Directory.Packages.props', request='User asked for the beta of Pre.Package on 2026-11-03')])
        o = check(c, root)[1]
        ctx.check('authorized prerelease entry accepted', not prerelease_rejected(o, 'Pre.Package'), o[-300:], c, 'CHECKER')
        root = fixture(c)
        ctx.check('unapproved prerelease still flagged', prerelease_rejected(check(c, root)[1], 'Pre.Package'), candidate=c, kind='CHECKER')
        code, o2, e2 = run_node(root, CHECKERS[c][0])
        ctx.check('instruction checker passes on the dependency fixture', code == 0, (o2 + e2)[-200:], c, 'CHECKER')
        with_record = fixture(c, [entry()])
        code, o2, e2 = run_node(with_record, CHECKERS[c][0])
        ctx.check('instruction checker accepts a project that has a real exception record', code == 0, (o2 + e2)[-200:], c, 'CHECKER')
        ok_only = fixture(c, deps={'safe-lib': '1.2.3'})
        ctx.check('exact stable version raises nothing', not rejected(check(c, ok_only)[1], 'safe-lib'), candidate=c, kind='CHECKER')
    # K1 is the only candidate whose pre-command hook gates versions, so it must honor the same record.
    root = fixture('K1')
    ctx.check('K1 hook: unapproved floating install blocked', pre_tool(root, 'K1', 'npm install left-pad@^2.0.0')[0] == 'block', candidate='K1', kind='HOOK')
    root = fixture('K1', [entry(version='^2.0.0')])
    ctx.check('K1 hook: recorded floating install allowed', pre_tool(root, 'K1', 'npm install left-pad@^2.0.0')[0] == 'allow', candidate='K1', kind='HOOK')
    ctx.check('K1 hook: other range still blocked', pre_tool(root, 'K1', 'npm install left-pad@^3.0.0')[0] == 'block', candidate='K1', kind='HOOK')
    ctx.check('K1 hook: other package still blocked', pre_tool(root, 'K1', 'npm install other-lib@^2.0.0')[0] == 'block', candidate='K1', kind='HOOK')
    ctx.check('K1 hook: exact version still allowed', pre_tool(root, 'K1', 'npm install left-pad@2.0.0')[0] == 'allow', candidate='K1', kind='HOOK')
    ctx.check('K1 hook: recorded version does not excuse a peer bypass', pre_tool(root, 'K1', 'npm install left-pad@^2.0.0 --force')[0] == 'block', candidate='K1', kind='HOOK')
    root = fixture('K1', [entry('nuget', 'Float.Package', '1.*', 'Directory.Packages.props')])
    ctx.check('K1 hook: recorded NuGet floating allowed', pre_tool(root, 'K1', 'dotnet add package Float.Package --version 1.*')[0] == 'allow', candidate='K1', kind='HOOK')
    ctx.check('K1 hook: unrecorded NuGet floating blocked', pre_tool(root, 'K1', 'dotnet add package Other.Package --version 2.*')[0] == 'block', candidate='K1', kind='HOOK')
    # Mutations: a checker that accepts everything, or a default that never rejects, is caught.
    MUT = {'M': ('.claude/scripts/check-manifests.mjs', 'function approvedVersionException(result, ecosystem, id, version, rel) {', 'function approvedVersionException(result, ecosystem, id, version, rel) {\n  return true;'),
           'M1': ('.claude/scripts/check-manifests.js', 'function approvedVersionException(data, ecosystem, id, version, rel) {', 'function approvedVersionException(data, ecosystem, id, version, rel) {\n  return true;'),
           'L0': ('.claude/hooks/manifest-checks.mjs', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {\n  return true;'),
           'L1': ('.claude/hooks/post-change-checks.mjs', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {\n  return true;'),
           'K0': ('.claude/scripts/check-dependencies.cjs', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {\n  return true;'),
           'K1': ('.claude/scripts/check-manifests.cjs', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {', 'function approvedVersionException(exceptions, ecosystem, id, version, rel) {\n  return true;')}
    for c, (rel, old, new) in MUT.items():
        m = mutate_text(c, rel, old, new)
        ok = False
        if m:
            shutil.copy(os.path.join(fixture(c), 'Directory.Packages.props'), os.path.join(m, 'Directory.Packages.props'))
            os.makedirs(os.path.join(m, 'frontend', 'App.Web'), exist_ok=True)
            with open(os.path.join(m, PKG), 'w', encoding='utf-8') as f:
                json.dump({'name': 'a', 'dependencies': FLOAT_NPM}, f)
            ok = not rejected(check(c, m)[1], 'left-pad')
        ctx.check('mutation: an always-true exception check makes the default test fail', ok, candidate=c, kind='MUTATION')
        m = mutate_text(c, SKILL, 'names the package and the version or range', 'mentions dependencies')
        ctx.check('mutation: unbounded exception wording is caught', m is not None and not post(None, c, '', SKILL, ['names the package and the version or range'], (), m), candidate=c, kind='MUTATION')
    ctx.not_run('registry lookup of the latest stable version and of the resolved install outcome', 'no network in this run; the duty stays in the workflow text and is not claimed as verified')
    ctx.not_run('NuGet restore with a floating version under Central Package Management', 'would need network and a project; MSBuild switches not exercised')
