"""Probe for the two residual NuGet/CPM checker-parity questions raised after PV2-03 (read-only on the candidates; fixtures in _scratch/runs).

1. A central file outside every ancestor of the project, imported the way the SDK supports (DirectoryPackagesPropsPath), and the
   neighbouring negatives (a plain <Import> the SDK does not count, a path to nothing, CPM off in the imported file).
2. A PackageVersion with no Version, an empty Version, and a Version given as a child element (valid MSBuild item metadata).

For every fixture: MSBuild's own evaluation (no checker), NuGet's own offline restore codes against an empty local feed, and the
outcome of each candidate's repository checker and of its post-edit hook on the relevant file.
Usage: PYTHONPATH=_tools python -B _tools/cpm_residual_probe.py <label>   (writes _investigation/cpm_residual_probe_<label>.json)
Never run while a gate runs (the gate clears _scratch/runs).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor

from rcommon import CANDIDATES, OUT, SCRATCH
from suites_loader import load_suite

c01 = load_suite('C01_CPM_EFFECTIVE')
T, F, PV, REF, PROJ, proj, central = c01.T, c01.F, c01.PV, c01.REF, c01.PROJ, c01.proj, c01.central
PIN = '<ItemGroup><PackageReference Include="A.B" Version="9.9.9" /></ItemGroup>'
DPP = '<Project><PropertyGroup><DirectoryPackagesPropsPath>$(MSBuildThisFileDirectory)%s</DirectoryPackagesPropsPath></PropertyGroup></Project>'

# name, files, the file a post-edit hook is run on, question
FIXTURES = [
    ('Q1-P1 central file outside every project ancestor, imported through DirectoryPackagesPropsPath',
     {'Directory.Build.props': DPP % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, PROJ, 1),
    ('Q1-P2 two projects in different folders, one central file in a sibling folder through DirectoryPackagesPropsPath',
     {'Directory.Build.props': DPP % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF), 'tools/Tool/Tool.csproj': proj(REF)}, 'tools/Tool/Tool.csproj', 1),
    ('Q1-P3 central file with another name, imported through DirectoryPackagesPropsPath',
     {'Directory.Build.props': DPP % 'config/Packages.props', 'config/Packages.props': central(T, PV), PROJ: proj(REF)}, PROJ, 1),
    ('Q1-P4 DirectoryPackagesPropsPath set in a nested Directory.Build.props, central file in a sibling folder of the projects folder',
     {'backend/Directory.Build.props': DPP % '../config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, PROJ, 1),
    ('Q1-N5 the project file itself imports config/Directory.Packages.props (the interim review example)',
     {'config/Directory.Packages.props': central(T, PV), PROJ: proj('<Import Project="../../config/Directory.Packages.props" />' + REF)}, PROJ, 1),
    ('Q1-N1 plain Import of a non-ancestor central file (the SDK does not mark it imported)',
     {'Directory.Build.props': '<Project><Import Project="config/Directory.Packages.props" /></Project>', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(REF)}, PROJ, 1),
    ('Q1-N2 DirectoryPackagesPropsPath names a missing file, CPM set true elsewhere',
     {'Directory.Build.props': '<Project><PropertyGroup><DirectoryPackagesPropsPath>$(MSBuildThisFileDirectory)config/Directory.Packages.props</DirectoryPackagesPropsPath><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup></Project>', PROJ: proj(REF)}, PROJ, 1),
    ('Q1-N3 non-ancestor central file through DirectoryPackagesPropsPath turns CPM off',
     {'Directory.Build.props': DPP % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(F, PV), PROJ: proj(REF)}, PROJ, 1),
    ('Q1-N4 non-ancestor central file through DirectoryPackagesPropsPath, the project pins a version',
     {'Directory.Build.props': DPP % 'config/Directory.Packages.props', 'config/Directory.Packages.props': central(T, PV), PROJ: proj(PIN)}, PROJ, 1),
    ('Q2-V1 PackageVersion with no Version (root central file)',
     {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" />'), PROJ: proj(REF)}, 'Directory.Packages.props', 2),
    ('Q2-V2 PackageVersion with an empty Version attribute',
     {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B" Version="" />'), PROJ: proj(REF)}, 'Directory.Packages.props', 2),
    ('Q2-V3 PackageVersion with the Version as a child element (valid item metadata)',
     {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B"><Version>1.2.3</Version></PackageVersion>'), PROJ: proj(REF)}, 'Directory.Packages.props', 2),
    ('Q2-V4 PackageVersion with an empty Version child element',
     {'Directory.Packages.props': central(T, '<PackageVersion Include="A.B"><Version></Version></PackageVersion>'), PROJ: proj(REF)}, 'Directory.Packages.props', 2),
    ('Q2-V5 PackageVersion with no Version in a nested central file',
     {'backend/Directory.Packages.props': central(T, '<PackageVersion Include="A.B" />'), PROJ: proj(REF)}, 'backend/Directory.Packages.props', 2),
]

PROPS = ['ManagePackageVersionsCentrally', 'CentralPackageVersionsFileImported', 'DirectoryPackagesPropsPath']


def msbuild(root, rel):
    args = ['dotnet', 'msbuild', rel.replace('/', os.sep), '-nologo'] + ['-getProperty:%s' % p for p in PROPS] + ['-getItem:PackageVersion']
    r = subprocess.run(args, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=c01.hermetic(root), timeout=180)
    if r.returncode != 0:
        return {'exit': r.returncode, 'error': (r.stdout + r.stderr)[-300:].replace(root, '<fixture>')}
    s = json.loads(r.stdout)
    pv = [{'id': i.get('Identity'), 'Version': i.get('Version', '')} for i in s.get('Items', {}).get('PackageVersion', [])]
    props = {k: (v.replace(root, '<fixture>') if isinstance(v, str) else v) for k, v in s.get('Properties', {}).items()}
    return {'exit': 0, 'properties': props, 'PackageVersion': pv}


def restore(files, project_body):
    root = os.path.join(SCRATCH, 'runs', 'probe-restore-' + uuid.uuid4().hex[:8])
    allf = {PROJ: proj(REF), 'nuget.config': '<configuration><packageSources><clear /><add key="local" value="feed" /></packageSources></configuration>'}
    allf.update(files)
    if project_body is not None:
        allf[PROJ] = proj(project_body)
    for rel, body in allf.items():
        p = os.path.join(root, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)
    os.makedirs(os.path.join(root, 'feed'), exist_ok=True)
    r = subprocess.run(['dotnet', 'restore', PROJ.replace('/', os.sep), '-nologo', '--configfile', 'nuget.config'], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', env=c01.hermetic(root), timeout=240)
    out = r.stdout + r.stderr
    shutil.rmtree(root, ignore_errors=True)
    lines = sorted({re.sub(r'\s+', ' ', l.split(': ', 2)[-1]).strip()[:220] for l in out.splitlines() if re.search(r'\bNU\d{4}\b', l)})
    return {'codes': sorted(set(re.findall(r'\b(NU\d{4})\b', out))), 'messages': [l.replace(root, '<fixture>') for l in lines][:6]}


def interesting(out, root):
    keep = [l.strip() for l in out.splitlines() if re.search(r'Directory\.Packages|PackageVersion|Version|imported|ManagePackageVersionsCentrally|NOT_RUN|central|A\.B', l)]
    return [l.replace(root, '<fixture>')[:260] for l in keep][:8]


def one(c, fixture):
    name, files, hook_rel, q = fixture
    root = c01.build(c, files)
    code, out = c01.check(c, root)
    hcode, hout = c01.hook_edit(c, root, hook_rel)
    res = {'candidate': c, 'command': {'exit': code, 'outcome': c01.outcome(code), 'lines': interesting(out, root)},
           'hook': {'file': hook_rel, 'exit': hcode, 'lines': interesting(hout, root)}}
    shutil.rmtree(root, ignore_errors=True)
    return name, res


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    report = {'label': label, 'dotnet': shutil.which('dotnet') is not None, 'fixtures': []}
    for name, files, hook_rel, q in FIXTURES:
        root = c01.build('K0', files)
        ev = {rel: msbuild(root, rel) for rel in sorted({PROJ, hook_rel if hook_rel.endswith('.csproj') else PROJ})}
        shutil.rmtree(root, ignore_errors=True)
        report['fixtures'].append({'name': name, 'question': q, 'files': files, 'msbuild': ev,
                                   'restore_versionless': restore(files, None), 'restore_pinned_in_project': restore(files, PIN.replace('9.9.9', '9.9.9'))})
    jobs = [(c, f) for f in FIXTURES for c in CANDIDATES]
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda j: one(*j), jobs))
    by = {}
    for name, res in results:
        by.setdefault(name, {})[res['candidate']] = res
    for fx in report['fixtures']:
        fx['candidates'] = by[fx['name']]
        fx['command_outcomes'] = {c: by[fx['name']][c]['command']['outcome'] for c in CANDIDATES}
    os.makedirs(os.path.join(OUT, '_investigation'), exist_ok=True)
    p = os.path.join(OUT, '_investigation', 'cpm_residual_probe_%s.json' % label)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    for fx in report['fixtures']:
        ev = fx['msbuild'][PROJ]
        props = ev.get('properties', {})
        print(fx['name'])
        print('   msbuild:', ev.get('exit'), {k: props.get(k) for k in PROPS[:2]}, ev.get('PackageVersion'), ev.get('error', ''))
        print('   restore versionless:', fx['restore_versionless']['codes'], '| pinned in project:', fx['restore_pinned_in_project']['codes'])
        print('   checkers:', fx['command_outcomes'])
    print('wrote', p)


if __name__ == '__main__':
    main()
