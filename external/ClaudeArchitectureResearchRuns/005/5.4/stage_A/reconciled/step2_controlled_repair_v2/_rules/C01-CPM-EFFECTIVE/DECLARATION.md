# C01-CPM-EFFECTIVE: declaration (contract section 2, step A)

Written before the first edit of this change.

**Change.** All six manifest checkers verify the effective Central Package Management state that MSBuild evaluates for each project. No checker takes literal XML as proof.

**Approval.** User, kit 72 "YES: align ALL SIX"; supersedes the K0-only scope of register item 8.2.

**Policies.** `DEP-006` (owner), `DEP-003` (floating exception interaction), `DEP-004` (no change intended), `DEP-025` (no change intended), `GOV-017` (a new package-management condition is not a new Reserved decision).

**Affected candidates.** M, M1, L0, L1, K0, K1.

## Normative contract

For each scoped project (a `.csproj` the candidate's checker already walks, outside build output, caches and `.claude`), in each evaluation context (default, `Configuration=Release`, and each `TargetFramework` of a multi-targeted project):

1. The MSBuild-evaluated `ManagePackageVersionsCentrally` is `true`. Inheritance from `Directory.Build.props`, an import, or `Directory.Packages.props` is legitimate. A project, condition, later import or `Directory.Build.targets` may turn it off, and that is a violation.
2. A central manifest is actually imported (`CentralPackageVersionsFileImported`). `true` with no imported manifest is a violation. Observed: restore gives NU1015.
3. No evaluated `PackageReference` carries a `Version`, wherever it was set. Observed: NU1008. Implicit SDK references are skipped.
4. Each evaluated `PackageReference` has an evaluated `PackageVersion`, unless it carries `VersionOverride`. Observed: NU1010.
5. A project MSBuild cannot evaluate (for example a malformed central manifest) is a violation. The checker fails closed.
6. If the proof cannot run (no SDK, an SDK too old for `-getProperty`, an SDK resolution gap, a time limit), the outcome is `NOT_RUN`, exit code 3 from the command. It never reads as PASS. No static fallback produces a PASS.
7. With no scoped project there is nothing to evaluate: not applicable, exit 0, and `dotnet` is not called.

**Interactions kept.** A floating central version stays rejected by the existing static checks unless a recorded DEP-003 entry names it. When such an entry exists, NuGet still rejects the version at restore unless `CentralPackageFloatingVersionsEnabled` is true (observed: NU1011 without it, no NU1011 with it). The checker gives a notice, and the add-dependency exception text names the switch. The switch does not widen the exception.

**Routing.** Only `.csproj`, `Directory.Packages.props`, `Directory.Build.props` and `Directory.Build.targets` lead to an evaluation. A `package.json` or source edit never calls `dotnet`. Hooks share a 20-second budget within their host timeouts; running out gives NOT_RUN. The command line has no shared budget.

**Native design kept.** The evaluator lives in each candidate's existing checker file. No file is added. M, M1, K0 and K1 keep their commands. L0 and L1 had no command for a whole-repository manifest check, so each gains an entry point on its existing hook script, and its `verify` names it.

## Competing or adjacent rules

| Item | Risk | Control |
|---|---|---|
| R08 K0 static reading | Replaced by real evaluation; its `UNPROVEN` outcome no longer exists | R08 suite updated with a stated reason, real-MSBuild comparison kept |
| R04 floating exception | Must stay honored | R04 suite replayed unchanged, plus the C01 interaction tests |
| R06 peer bypass | Shares no code path with this change | R06 suite replayed unchanged |
| Hook timeouts (L1 30 s, others 60 s) | Evaluation could exceed them | 20 s shared budget, NOT_RUN beyond it |
| Static version lint in each checker | Stays, because it sees a literal without the SDK | It can only add a violation, never a pass |

## Expected negative cases (run before editing, on v1 bytes)

Inherited `true` is rejected or ignored by the five literal checkers. A literal `true` in a comment or an unimported file, a project-level `false`, a `Directory.Build.targets` `false`, a Release-only `false` and a per-framework `false` are all accepted or missed by them.

## Out of scope for this change

Floating detection on versions that come from an MSBuild property. Candidates differ on this today, and it belongs to DEP-003, not DEP-006. Recorded as a remaining limit.
