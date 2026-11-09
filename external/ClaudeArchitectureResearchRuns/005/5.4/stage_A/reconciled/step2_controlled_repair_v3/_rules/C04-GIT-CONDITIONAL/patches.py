"""C04: npm manifest and lockfile commit steps become conditional on an authorized commit. One logical rule. No Git permission machinery is added, and lockfile consistency stays."""
POLICIES = ['GOV-015', 'DEP-007']
REASON = 'Kit 71 C04, HQ-01: a workflow step that mentions committing is not Git authority. Make the imperatives conditional; update both files coherently without a commit when none is authorized.'
EVIDENCE = 'inventory.json DEP-007 (package-lock consistent, no commit duty) and GOV-015; v1 report section 6 and a wider sweep on current bytes.'
PATCHES = [
    ('M', '.claude/rules/dependencies.md', """package manager. Maintain and commit `package.json` and `package-lock.json` and
keep the lockfile consistent when packages change. Put""", """package manager. Maintain `package.json` and `package-lock.json` together and
keep the lockfile consistent when packages change; when an authorized commit is
part of this task, include both files, and otherwise update them without creating
a Git commit. Put"""),
    ('M', '.claude/skills/add-dependency/SKILL.md', "2. Commit `package.json` and `package-lock.json` together.", """2. Update `package.json` and `package-lock.json` together. When an authorized
   commit is part of this task, include both files; otherwise do not create a Git
   commit."""),
    ('M', '.claude/scripts/check-manifests.mjs', "no package-lock.json next to package.json - commit the lockfile (", "no package-lock.json next to package.json - keep a consistent lockfile beside it ("),
    ('M1', '.claude/rules/dependencies.md', """project deliberately adopts another package manager. Maintain and commit
`package.json` and `package-lock.json`, and keep the lockfile consistent when
adding packages. Put""", """project deliberately adopts another package manager. Maintain `package.json` and
`package-lock.json` together, and keep the lockfile consistent when adding
packages; when an authorized commit is part of this task, include both files, and
otherwise update them without creating a Git commit. Put"""),
    ('M1', '.claude/scripts/check-manifests.js', "package-lock.json is missing; maintain and commit the lockfile (", "package-lock.json is missing; keep a consistent lockfile beside package.json ("),
    ('L0', '.claude/rules/3-project/package-management.md', "; commit `package.json` and `package-lock.json` and keep the lockfile consistent with every change.", "; keep `package.json` and `package-lock.json` together and the lockfile consistent with every change; when an authorized commit is part of this task, include both files, and otherwise update them without creating a Git commit."),
    ('L1', '.claude/rules/3-project/package-management.md', ": commit `package.json` and `package-lock.json`, keep the lockfile consistent, and place", ": keep `package.json` and `package-lock.json` together and the lockfile consistent (when an authorized commit is part of this task, include both files; otherwise update them without creating a Git commit), and place"),
    ('K0', '.claude/rules/common/dependencies.md', "- Commit `package.json` and `package-lock.json`, and keep the lockfile consistent with every dependency change.", "- Keep `package.json` and `package-lock.json` together and the lockfile consistent with every dependency change; when an authorized commit is part of this task, include both files, and otherwise update them without creating a Git commit."),
    ('K0', '.claude/scripts/check-dependencies.cjs', "no package-lock.json next to package.json; commit a consistent lockfile (", "no package-lock.json next to package.json; keep a consistent lockfile beside it ("),
    ('K1', '.claude/rules/frontend/dependencies.md', "`package.json` and `package-lock.json` must be committed and kept consistent, and build/test", "`package.json` and `package-lock.json` must stay together and consistent (when an authorized commit is part of this task, include both files; otherwise update them without creating a Git commit), and build/test"),
    ('K1', '.claude/skills/add-dependency/SKILL.md', "keep `package-lock.json` consistent and committed.", "keep `package.json` and `package-lock.json` together and consistent; when an authorized commit is part of this task, include both files, and otherwise do not create a Git commit."),
    ('K1', '.claude/skills/project-structure/references/frontend-setup.md', "(`npm run build`, `npm test`) and commit `package-lock.json`.", "(`npm run build`, `npm test`) and keep `package-lock.json` beside `package.json`; when an authorized commit is part of this task, include both files, and otherwise do not create a Git commit."),
]
