# R07 item 8.1 Swagger UI: baseline and impact

**Target.** On an applicable Development API behavior change, open the Development Swagger UI and confirm it loads. Same obligation and condition in all six, native routing kept. Applicability: the project exposes such a UI. No forced startup where the app cannot run: that verification is reported NOT RUN, not PASS.

**Original differences (`SWAGGER_UI_REVIEW.md`, re-read at source).** Trigger: L0 and K0 said "API changes", M, M1, L1, K1 "API behavior changes". Action: L0 and L1 said "open", the others "open and confirm it loads". Owner: only the knowledge skill, which is not reliably loaded, so the obligation had weak delivery.

**Change.** The obligation goes into each candidate's `verify` workflow, which every candidate already routes before completion. The `swagger` skill states the same trigger and action and points there.

**Architecture-specific.** L1's `verify` is Level 0, where technology names are forbidden, so it says "the Development API documentation UI", exactly as its existing smoke line does; L1's Level 2 `swagger` skill names Swagger. K0 and K1 use their "see also:" routing form. L0 `verify` is Level 3 and may name Swagger.

**Related policies.** WF-005, WF-006, API-016, TST-010. Interaction checked: noninteractive runs cannot satisfy this by claim, only by NOT RUN.

**Classification effect.** The compound and UI records move to `CANONICAL_PLUS_DELTA` with a workflow remainder and now read as MUST at workflow strength, in all six; decided in R25.
