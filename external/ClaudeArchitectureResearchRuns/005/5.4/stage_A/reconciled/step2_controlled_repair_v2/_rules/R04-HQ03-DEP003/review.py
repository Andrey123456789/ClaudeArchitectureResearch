"""Source review for R04."""
SKILL = '.claude/skills/add-dependency/SKILL.md'
CHECKER = {'M': '.claude/scripts/check-manifests.mjs', 'M1': '.claude/scripts/check-manifests.js', 'L0': '.claude/hooks/manifest-checks.mjs', 'L1': '.claude/hooks/post-change-checks.mjs', 'K0': '.claude/scripts/check-dependencies.cjs', 'K1': '.claude/scripts/check-manifests.cjs'}
CPM = {'M': (CHECKER['M'], 'ManagePackageVersionsCentrally is not enabled'), 'M1': (CHECKER['M1'], 'Central Package Management is not enabled'), 'L0': (CHECKER['L0'], 'ManagePackageVersionsCentrally must be true'), 'L1': (CHECKER['L1'], 'ManagePackageVersionsCentrally must stay true'),
       'K0': (CHECKER['K0'], 'it must be true (D-17'),  # quote moved at R08, which replaced the literal check with the effective reading
       'K1': (CHECKER['K1'], 'ManagePackageVersionsCentrally is not enabled')}
LATEST = {'M': 'Determine the latest stable version compatible', 'M1': 'determine the latest stable version compatible', 'L0': 'Determine the latest **stable** version compatible', 'L1': 'Determine the latest **stable** version compatible', 'K0': 'Determine the latest **stable** version compatible', 'K1': 'Determine the latest **stable** version compatible'}
REVIEW = []
for c in CHECKER:
    REVIEW.append(dict(policy='DEP-003', candidate=c, verdict='HOLDS', quotes=[(SKILL, LATEST[c]), (SKILL, 'explicit, bounded user request that names the package and the version or range'), (SKILL, 'there is no global switch'), (CHECKER[c], 'dependency-version-exceptions.json')],
                       note='Policy default kept: latest stable compatible from the registry, floating and prerelease avoided. The explicit-request exception the policy already grants now reaches the executable checks in all six. M1 previously had no exception for floating versions at all; that text difference is gone.',
                       counterexample='A user asks for left-pad at * in one package.json: accepted only for that entry. A second floating package in the same manifest stays rejected (executed). Without a record nothing changes.'))
    REVIEW.append(dict(policy='DEP-006', candidate=c, verdict='HOLDS', quotes=[CPM[c]], note='Central Package Management check untouched; the exception concerns the version form only.'))
