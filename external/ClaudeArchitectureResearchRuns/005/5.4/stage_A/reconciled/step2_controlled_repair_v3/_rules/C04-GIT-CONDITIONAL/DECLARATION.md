# C04-GIT-CONDITIONAL: declaration (contract section 2, step A)

Written before the first edit of this change.

**Change.** Unconditional instructions to commit the npm manifest and lockfile become conditional on an authorized commit. Without one, both files are updated coherently and no Git commit is created. Lockfile consistency and dependency review are unchanged.

**Authority.** `GOV-015`, `HQ-01`, v1 R02 clause: "a workflow step that mentions committing is not that authority". Kit 71 C04. `DEP-007` asks for a consistent `package-lock`; it does not ask for a commit.

**Why change text the Git clause already overrides.** v1 kept the lines and relied on the clause. A reader of a path-scoped rule or a workflow step sees an imperative with no condition, and in a headless run with no standing choice the imperative competes with the pause. Making them conditional removes that conflict and changes no obligation.

## Sites on current v2 bytes

v1 reported 5 lines in M, M1, K0, K1. A wider sweep over all six, including checker messages and passive forms, found 12.

| Candidate | File | Text | v1 listed |
|---|---|---|---|
| M | `rules/dependencies.md` | "Maintain and commit `package.json` and `package-lock.json`" | yes |
| M | `add-dependency` | "2. Commit `package.json` and `package-lock.json` together." | yes |
| M | `scripts/check-manifests.mjs` | "commit the lockfile" | no |
| M1 | `rules/dependencies.md` | "Maintain and commit" | yes |
| M1 | `scripts/check-manifests.js` | "maintain and commit the lockfile" | no |
| L0 | `rules/3-project/package-management.md` | "commit `package.json` and `package-lock.json`" | no |
| L1 | `rules/3-project/package-management.md` | "commit `package.json` and `package-lock.json`" | no |
| K0 | `rules/common/dependencies.md` | "Commit `package.json` and `package-lock.json`" | yes |
| K0 | `scripts/check-dependencies.cjs` | "commit a consistent lockfile" | no |
| K1 | `skills/project-structure/references/frontend-setup.md` | "and commit `package-lock.json`" | yes |
| K1 | `rules/frontend/dependencies.md` | "must be committed and kept consistent" | no |
| K1 | `skills/add-dependency` | "keep `package-lock.json` consistent and committed" | no |

So all six had the defect, not four.

## Reviewed and left as they are

- `git-workflow` in all six ("Before committing", "Prefer one logical change per commit"): they govern how a commit is made when one is authorized, and the skill opens under the Git authority clause.
- "review generated migrations before committing" (`PST-010` text and reminders in M, L0, K0, K1): orders review before a commit that may happen; it asks for no commit.
- "Never hardcode or commit real secrets" (`SEC-001`): a prohibition, not a mutating step.
- "CI definitions stay in source control": a location rule, and CI is out of practical scope. It does not tell the agent to create a commit now.
- Database commits (`IUnitOfWork`, commit boundary): not Git.
- K0's Git hook differs from the other five by delivery, not by obligation. Reported, not homogenized.

## Common obligation after the change

When an authorized commit is part of this task, include `package.json` and `package-lock.json` together. Otherwise update both coherently without creating a Git commit.

## Cases tested

Interactive and headless, with no authority: no commit, files coherent. Named commit authority: both files in it. Generic "approved workflow" meeting the step: no authority. Dirty tree at task start with a package file modified: the R02 check still fires. Read-only task: no check. Lockfile consistency still required in all six. Peer bypass and floating exception unaffected. R02 to R06 replayed.
