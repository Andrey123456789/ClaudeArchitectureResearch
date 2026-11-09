"""C01 claim updates and new claims. Same entry format as v1 R26. Each reworded record was read against the current source; its original claim stays in the view."""
RULE = 'C01-CPM-EFFECTIVE'
CANDS = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
UPDATES = {}
ADDED = []


def up(keys, claim, note, sets=None):
    for k in keys:
        UPDATES[k] = dict(rule=RULE, status='REWORDED', claim=claim, note=note, set=sets or {}, sub={})


EFFECTIVE = 'The effective ManagePackageVersionsCentrally that MSBuild evaluates must be true for each project in each evaluated context; a false or unset value, a central manifest that is not imported, an evaluated PackageReference with a version or with no PackageVersion, and a project MSBuild cannot evaluate are errors. When the proof cannot run the outcome is NOT_RUN, never a pass.'
NOTE = 'C01: the checker reads the evaluated value, not literal XML.'
up(['FG-K0-66fb97489b', 'FG-K0-641844cc06', 'FG-K0-6bc04e6316', 'FG-K1-ad9966e3b7', 'FG-K1-2d6d3a491b', 'FG-K1-47231ec703', 'FG-L0-79ba8dd753', 'FG-M1-84fb4b149e'], EFFECTIVE, NOTE)
up(['FG-L0-9551e9cc12', 'FG-L1-f2ee786a8d'], EFFECTIVE, NOTE, dict(modality='MUST', strength_vs_canonical='SAME', strength_resolution_code=None))
up(['FG-M-7f012a0fe2'], 'Violations when the effective ManagePackageVersionsCentrally MSBuild evaluates for a project is not true, when no central manifest is imported, when package references exist without Directory.Packages.props, when a PackageVersion lacks Version, or when a project declares or evaluates to a version; an evaluated reference with no PackageVersion is a violation. When the proof cannot run the outcome is NOT_RUN, never a pass.', NOTE)
up(['FG-M-13fef4cca8'], 'A NuGet version declared in a project and an effective opt-out of Central Package Management are hard violations; the opt-out is read from what MSBuild evaluates, including conditions and imports.', NOTE)
up(['FG-M-85437e0f8a'], 'After editing a .csproj, Directory.Packages.props, Directory.Build.props, Directory.Build.targets or package.json, run check-manifests on it; violations are returned as a blocking reason to fix. Only the .NET files lead to an MSBuild evaluation.', NOTE)
up(['FG-M1-29f43fdad5'], 'The version checks match literal text; the Central Package Management setting is read from what MSBuild evaluates, and when that proof cannot run the check reports NOT_RUN.', 'C01: the literal CPM reading this record described is gone. A descriptive record.')
up(['FG-L0-9c2f9a364d'], 'Central Package Management is recognized from the value MSBuild evaluates for each project, so an imported or inherited setting counts and a literal one that does not evaluate does not.', 'C01: the reported false "missing CPM" for imported settings is fixed. A descriptive record.')
up(['FG-L1-eda5a833fc'], 'The post-change hook recognizes .csproj, Directory.Packages.props, Directory.Build.props, Directory.Build.targets and package.json as manifests. Other imported props or targets and npm configuration are not watched, though MSBuild still evaluates imported props when a watched file changes.', 'C01: chain files added. A descriptive record.')
up(['FG-L1-9d49d68ec8'], 'The project parser reads .csproj XML without evaluating conditions or imports (reported accuracy limit for conditional references); the effective Central Package Management setting is evaluated by MSBuild in the post-change check instead.', 'C01: imported central settings are now evaluated. A descriptive record.')
up(['FG-K1-475b4d42b1'], 'Manifest coverage is limited to .csproj, package.json, central props and Directory.Build.props/targets; a top-level tests/ directory and a missing adjacent package-lock.json only warn.', 'C01: chain files added. A descriptive record.')
up(['FG-K1-7d8a86c09f'], 'Per-file manifest-checker arguments must resolve inside the active root; warnings alone yield success, except that an unproven effective Central Package Management state exits 3, and missing selected files return no findings (reported uncertainty).', 'C01: exit code 3 added. A descriptive record.')

N_V1 = {'M': 7, 'M1': 7, 'L0': 7, 'L1': 7, 'K0': 7, 'K1': 7}
RULE_FILE = {'M': '.claude/rules/dependencies.md', 'M1': '.claude/rules/dependencies.md', 'L0': '.claude/rules/3-project/package-management.md', 'L1': '.claude/rules/3-project/package-management.md', 'K0': '.claude/rules/common/dependencies.md', 'K1': '.claude/rules/backend/dependencies.md'}
CHECKER = {'M': '.claude/scripts/check-manifests.mjs', 'M1': '.claude/scripts/check-manifests.js', 'L0': '.claude/hooks/manifest-checks.mjs', 'L1': '.claude/hooks/post-change-checks.mjs', 'K0': '.claude/scripts/check-dependencies.cjs', 'K1': '.claude/scripts/check-manifests.cjs'}
RULE_QUOTE = {c: 'effective `ManagePackageVersionsCentrally` must be true for each project' for c in CANDS}


def add(c, n, claim, classification, modality, path, quote, domain='WORKFLOW_ENFORCEMENT', policies=None, related=None, extra=None, kind=None, scenario=None, trigger=None, exceptions='None.', confidence='HIGH'):
    ADDED.append(dict(source_key='REP-%s-%03d' % (c, n), candidate=c, rule=RULE, claim_text=claim, classification=classification, modality=modality, path=path, quote=quote, domain=domain, canonical_coverage=policies or [], related_policy_ids=related or [], extra_fragment=extra, extra_fragment_kind=kind, distinguishing_scenario=scenario, trigger=trigger, exceptions=exceptions, confidence=confidence))


for c in CANDS:
    n = N_V1[c] + 1
    add(c, n, 'What counts is the value MSBuild evaluates: the effective ManagePackageVersionsCentrally must be true for each project, whether set in the central manifest or inherited, and no project, condition or later file may turn it off.', 'CANONICAL_PLUS_DELTA', 'MUST', RULE_FILE[c], RULE_QUOTE[c], policies=[dict(policy_id='DEP-006', coverage='PARTIAL')], related=['DEP-006'],
        extra='The obligation is stated on the evaluated value for each project.', kind='EXTRA_WORKFLOW', scenario='True written in a comment and CPM off: DEP-006 is plainly unmet; this line names the reason.', trigger='A .NET project is in scope.')
    add(c, n + 1, 'When the MSBuild proof of effective Central Package Management cannot run, the manifest check reports NOT_RUN (exit code 3 from the command) and never reads as passed; verification reports it as NOT RUN. There is no static fallback that passes.', 'EXTRA_WORKFLOW', 'MUST', CHECKER[c], 'NOT_RUN effective Central Package Management was not proven', related=['DEP-006'],
        extra='The honest outcome when the proof is unavailable.', kind='EXTRA_WORKFLOW', scenario='No .NET SDK on the machine and a project in scope: the check exits 3, not 0.', trigger='A .NET project is in scope and the SDK cannot evaluate it.', exceptions='No project in scope: not applicable, and dotnet is not called.')
    add(c, n + 2, 'A recorded floating NuGet version also needs CentralPackageFloatingVersionsEnabled set to true, because restore rejects it otherwise (NU1011); that property does not widen the exception, and the manifest checks keep rejecting every other floating version.', 'EXTRA_WORKFLOW', 'MUST', '.claude/skills/add-dependency/SKILL.md', '`CentralPackageFloatingVersionsEnabled`', related=['DEP-003', 'DEP-006'],
        extra='The NuGet switch a recorded floating version needs.', kind='EXTRA_WORKFLOW', scenario='A recorded 1.* passes the checker, and restore fails with NU1011 until the switch is on.', trigger='A recorded floating NuGet version under Central Package Management.')
