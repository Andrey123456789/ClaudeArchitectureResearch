"""Evidence dispositions for C04. Each range was read with the records citing it. Lockfile consistency and tooling categories stay; only the commit step becomes conditional."""


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


RULE = 'DEP-007 duties kept; the unconditional commit step becomes conditional on an authorized commit.'
MSG = 'Checker message no longer tells the reader to commit; the check, its severity and its trigger are unchanged.'
DISPOSITIONS = [
    d('M', '.claude/rules/dependencies.md', 34, 37, 'Maintain `package.json` and `package-lock.json` together', RULE),
    d('M', '.claude/scripts/check-manifests.mjs', 351, 352, 'keep a consistent lockfile beside it', MSG),
    d('M', '.claude/scripts/check-manifests.mjs', 351, 353, 'keep a consistent lockfile beside it', MSG),
    d('M', '.claude/skills/add-dependency/SKILL.md', 115, 117, 'Update `package.json` and `package-lock.json` together', RULE),
    d('M', '.claude/skills/add-dependency/SKILL.md', 117, 117, 'Update `package.json` and `package-lock.json` together', RULE),
    d('M1', '.claude/rules/dependencies.md', 49, 53, 'Maintain `package.json` and `package-lock.json` together', RULE),
    d('M1', '.claude/scripts/check-manifests.js', 163, 166, 'keep a consistent lockfile beside package.json', MSG),
    d('M1', '.claude/scripts/check-manifests.js', 164, 166, 'keep a consistent lockfile beside package.json', MSG),
    d('L0', '.claude/rules/3-project/package-management.md', 23, 23, 'keep `package.json` and `package-lock.json` together and the lockfile consistent with every change', RULE),
    d('L1', '.claude/rules/3-project/package-management.md', 17, 17, 'keep `package.json` and `package-lock.json` together and the lockfile consistent', RULE),
    d('K0', '.claude/rules/common/dependencies.md', 28, 28, 'Keep `package.json` and `package-lock.json` together and the lockfile consistent with every dependency change', RULE),
    d('K0', '.claude/scripts/check-dependencies.cjs', 206, 208, 'no package-lock.json next to package.json; keep a consistent lockfile beside it', MSG),
    d('K0', '.claude/scripts/check-dependencies.cjs', 206, 209, 'no package-lock.json next to package.json; keep a consistent lockfile beside it', MSG),
    d('K1', '.claude/rules/frontend/dependencies.md', 10, 10, '`package.json` and `package-lock.json` must stay together and consistent', RULE),
    d('K1', '.claude/skills/add-dependency/SKILL.md', 71, 71, 'keep `package.json` and `package-lock.json` together and consistent', RULE),
    d('K1', '.claude/skills/project-structure/references/frontend-setup.md', 18, 18, 'keep `package-lock.json` beside `package.json`', 'The verification step is untouched; the commit step becomes conditional.'),
]
