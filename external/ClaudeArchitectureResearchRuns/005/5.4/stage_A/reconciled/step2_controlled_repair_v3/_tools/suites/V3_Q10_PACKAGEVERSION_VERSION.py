"""V3-Q10 regression: a PackageVersion version is read as MSBuild reads it (Version attribute or Version child element). A missing or
empty version is an error in all six, and a valid child-element version is accepted in all six.

Each candidate's own repository checker and post-edit hook run on identical fixtures (C01 machinery, hermetic .NET SDK, no network).
MSBuild's own evaluation and NuGet's offline restore against an empty local feed are recorded beside them (NU1604: no lower bound).
"""
import json
import os
import shutil
import subprocess

from rcommon import CANDIDATES
from suitelib import has, mutate_text
from suites_loader import load_suite

RULE = 'V3-Q10-PACKAGEVERSION-VERSION'


def fixtures(c01):
    T, REF, PROJ, proj, central = c01.T, c01.REF, c01.PROJ, c01.proj, c01.central
    return [
        ('no Version at all, root central file', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" />'), PROJ: proj(REF)}, 'Directory.Packages.props', 'ERROR', ''),
        ('no Version at all, nested central file', {'backend/Directory.Packages.props': central(T, '<PackageVersion Include="A.B" />'), PROJ: proj(REF)}, 'backend/Directory.Packages.props', 'ERROR', ''),
        ('empty Version attribute', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" Version="" />'), PROJ: proj(REF)}, 'Directory.Packages.props', 'ERROR', ''),
        ('empty Version child element', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B"><Version></Version></PackageVersion>'), PROJ: proj(REF)}, 'Directory.Packages.props', 'ERROR', ''),
        ('self-closing Version child element', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B"><Version /></PackageVersion>'), PROJ: proj(REF)}, 'Directory.Packages.props', 'ERROR', ''),
        ('pinned Version child element', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B"><Version>1.2.3</Version></PackageVersion>'), PROJ: proj(REF)}, 'Directory.Packages.props', 'OK', '1.2.3'),
        ('floating Version child element', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B"><Version>1.*</Version></PackageVersion>'), PROJ: proj(REF)}, 'Directory.Packages.props', 'ERROR', '1.*'),
        ('pinned Version attribute (control)', {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" Version="1.2.3" />'), PROJ: proj(REF)}, 'Directory.Packages.props', 'OK', '1.2.3'),
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


def complaint(out):
    return [l for l in out.splitlines() if 'A.B' in l and any(w in l for w in ('no Version', 'empty', 'missing', 'floating'))]


def run(ctx):
    c01 = load_suite('C01_CPM_EFFECTIVE')
    if shutil.which('dotnet') is None:
        ctx.not_run('all V3-Q10 fixtures', '.NET SDK not on PATH')
        return
    fx = fixtures(c01)
    for name, files, edited, want, msb in fx:
        root = c01.build('K0', files)
        r = subprocess.run(['dotnet', 'msbuild', c01.PROJ.replace('/', os.sep), '-nologo', '-getItem:PackageVersion'], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=c01.hermetic(root), timeout=180)
        shutil.rmtree(root, ignore_errors=True)
        items = json.loads(r.stdout).get('Items', {}).get('PackageVersion', []) if r.returncode == 0 else None
        got = items[0].get('Version', '') if items else None
        ctx.check('MSBuild directly: the evaluated Version of A.B is "%s": %s' % (msb, name), got == msb, items, kind='MSBUILD', expect=msb, actual=got)
    for name, files, want in ((fx[0][0], fx[0][1], 'NU1604'), (fx[5][0], fx[5][1], None)):
        codes = c01.restore_codes(files)
        if want:
            ctx.check('NuGet restore (offline) warns NU1604, no lower bound: %s' % name, want in codes, codes, kind='NUGET', expect=want, actual=codes)
        else:
            ctx.check('NuGet restore (offline) has no version complaint: %s' % name, 'NU1604' not in codes, codes, kind='NUGET', actual=codes)
    for name, files, edited, want, _ in fx:
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
            if want == 'ERROR':
                ctx.check('the checker names the package and the version problem: %s' % name, bool(complaint(out)), out[-300:].replace(root, '<fixture>'), c, 'CHECKER')
            hcode, hout = c01.hook_edit(c, root, edited)
            if want == 'ERROR':
                ctx.check('post-edit hook on the central file reports it: %s' % name, bool(complaint(hout)), hout[-300:].replace(root, '<fixture>'), c, 'CHECKER')
            else:
                ctx.check('post-edit hook on the central file raises no version complaint: %s' % name, not complaint(hout), hout[-300:].replace(root, '<fixture>'), c, 'CHECKER')
            shutil.rmtree(root, ignore_errors=True)
        done = {v for v in row.values() if v != 'NOT_RUN'}
        ctx.check('same task, six candidates: %s' % name, done == {want} or not done, row, kind='PARITY', expect=want, actual=row)
    # Source: rule text unchanged; the readers.
    ctx.check('M1 reports a PackageVersion with no version', has('M1', '.claude/scripts/check-manifests.js', 'PackageVersion has no Version; select the latest stable compatible version'), candidate='M1', kind='SOURCE')
    ctx.check('K0 reads a child Version element and reports a missing version', has('K0', '.claude/scripts/check-dependencies.cjs', 'a child <Version> element wins over the attribute') and has('K0', '.claude/scripts/check-dependencies.cjs', 'has no Version; pin the verified stable version'), candidate='K0', kind='SOURCE')
    ctx.check('M reads a child Version element', has('M', '.claude/scripts/check-manifests.mjs', 'a child <Version> element wins over the attribute'), candidate='M', kind='SOURCE')
    for c, rel in (('M', '.claude/rules/dependencies.md'), ('M1', '.claude/rules/dependencies.md'), ('K0', '.claude/rules/common/dependencies.md')):
        ctx.check('the NuGet rule text still places versions in Directory.Packages.props (contract unchanged)', has(c, rel, 'versions belong in'), candidate=c, kind='SOURCE')
    # Mutations: each fix removed on a copy; the fixture that proves it must notice.
    muts = [
        ('M1', '.claude/scripts/check-manifests.js', "findings.push(finding('ERROR', file, `${id}: PackageVersion has no Version;", "findings.push(finding('WARN', file, `${id}: PackageVersion has no Version;", 0, 'OK', 'the missing-version error turned into a warning lets <PackageVersion Include="A.B" /> through'),
        ('K0', '.claude/scripts/check-dependencies.cjs', 'result.errors.push(`${rel}: ${include} has no Version;', 'result.notices.push(`${rel}: ${include} has no Version;', 0, 'OK', 'the missing-version error turned into a notice lets it through'),
        ('K0', '.claude/scripts/check-dependencies.cjs', "const version = child ? (child[1] || '').trim() : element.attributes.get('Version');", "const version = element.attributes.get('Version');", 5, 'ERROR', 'reading the attribute only rejects a valid child version'),
        ('M', '.claude/scripts/check-manifests.mjs', "child ? decodeReferences(child.body ?? '') : attrs.version", 'attrs.version', 5, 'ERROR', 'reading the attribute only rejects a valid child version'),
    ]
    for c, rel, old, new, i, expect, label in muts:
        m = mutate_text(c, rel, old, new)
        if not m:
            ctx.check('mutation anchor present: %s' % label, False, old, c, 'MUTATION')
            continue
        place(m, fx[i][1])
        got = c01.outcome(c01.check(c, m)[0])
        ctx.check('mutation: %s (caught)' % label, got == expect, got, c, 'MUTATION', expect, got)
        shutil.rmtree(m, ignore_errors=True)
    ctx.not_run('restore against a real registry for these fixtures', 'no package registry in this run; offline restore against an empty local feed only', None)
