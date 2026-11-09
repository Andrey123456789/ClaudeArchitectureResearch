# C03-WF019-EXCEPTION: declaration (contract section 2, step A)

Written before the first edit of this change.

**Change.** Absolute wording about Production migrations no longer makes a precise, user-approved exception impossible, and the owner of `WF-019` in each candidate says what such an exception needs. The default stays: no automatic Production database migration from normal application startup.

**Authority.** `WF-019` (MUST_NOT): "Do not automatically apply production database migrations from normal application startup by default; treat production migration as an explicit deployment operation using approved credentials and never run Development seeding in Production." Register 8.4 and kit 72: "Do not make explicitly authorized exceptions impossible by adding unconditional `never`; retain credential controls and the Production seeding prohibition." Kit 71: generic workflow approval does not authorize startup migrations; explicit exceptions require recorded scope.

**Adjacent policies, unchanged.** `PST-004`, `PST-005`, `PST-006`, `PST-009`, `PST-010`, `SEC-001`, `GOV-017`.

## Line-by-line reading, on current v2 bytes

| Candidate | Line | Reading | Decision |
|---|---|---|---|
| M | `project-structure`: "Do not add Production credentials or Production migration automation." | Scaffolding line, but "migration automation" also bars a controlled deployment-time step that `WF-019` allows | Change, as L0's v1 line |
| M1 | `project-structure`: same | Same | Change |
| L1 | `project-structure`: "no Production credentials or Production migration automation." | Same | Change |
| K1 | `project-structure`: "Never add Production credentials or Production migration automation." | Same | Change |
| K0 | `project-structure`: "Add no Production credentials and no automatic production migration step" | Not named in the contract, but the same defect: "automatic ... step" reads as barring an automated deployment-time step | Change |
| L0 | `project-structure` | Fixed by v1 R10 | No change |
| L1 | `development-workflow`: "Never apply production database migrations automatically from normal application startup:" | The other five say "by default". This one makes an approved exception impossible | Change, add "by default" |
| All six | Owner line of `WF-019` | Says "by default" but not what an exception needs, so a generic approval could be taken for one | Add one sentence |

## No change, with reason

- `ci-cd` and `docker` lists in M1, L1, K0 ("automatic production seeding or startup migrations", "automatic production database migration", "production migrations at application startup"): these are review checks by reference or anti-pattern lists that defer to the owner. They name the default and do not bar a recorded exception, and they are knowledge skills. A review that finds an approved exception reads the owner line. The `ci-cd` skills also stay unchanged because CI is out of scope.
- L1 `ef-core/commands.md`: "Never point these commands at Production; production migration is a deployment step." These are Development-only commands (`dotnet ef database drop` is among them). The ban is about those commands and does not touch a controlled deployment step, which generates scripts or bundles.
- `ef-core` "generated migration scripts are often preferable" in all six: a preference, kept.
- Seeding bans (`PST-004`): "never seed Production automatically" has no exception in `WF-019` or `PST-004`, so the absolute wording is correct and stays.
- Credential bans (`SEC-001`) stay absolute at scaffold time.

## Exception shape (the only new normative text)

An exception is a user's explicit request naming the Production startup-migration exception and its scope, recorded through `architecture-decision`. A generic workflow approval is not one. A headless run can implement it only under the existing rule for an explicitly approved Reserved change. It never authorizes seeding in Production or a credential in source control.

## Scenarios tested in all six

Default startup migration: refused. Explicit, scoped, recorded exception: not refused by any line. Generic "approved workflow": refused. Controlled deployment-time step with approved credentials: allowed. Development seeding in Production: refused, exception or not. Scaffolding with Production credentials: refused. Local Development migrations: unchanged.
