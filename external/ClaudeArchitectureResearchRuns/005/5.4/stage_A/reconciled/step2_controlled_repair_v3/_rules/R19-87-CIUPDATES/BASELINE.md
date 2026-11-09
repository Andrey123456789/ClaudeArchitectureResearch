# R19 item 8.7 CI dependency auto-updates: comparison

**Type.** NO_CHANGE_VERIFIED for templates, CLASSIFICATION_ONLY for labels and scope.

**Six-way source.** The register lists L0, L1, K0, K1. Reading at source shows the rule also stands in M (`ci-cd:124`) and M1 (`ci-cd:107`), so it is present in all six, not four. No deletion in any of them.

**Scope.** Kept, labeled `OUT_OF_PRACTICAL_EVALUATION_CI`. No CI/CD trial (NOT_RUN, out of scope).

**Labels.** The audit moved `FG-L0-29a3230807` to XP (R25). The same content in L1, K1, K0 follows. M, M1 and K0's second record are compound with "treat findings per the project's security policy", so CD stands, and M1's CO was a false label.
