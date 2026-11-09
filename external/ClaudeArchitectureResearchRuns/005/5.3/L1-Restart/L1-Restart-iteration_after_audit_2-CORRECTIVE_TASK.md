# L1-Restart / Phase 5.3 — `iteration_after_audit_2`

## 1. Decision, provenance, authority

This pass implements a **user-approved intentional contract change** for technology neutrality (P4), harmonizing Candidate L1-Restart with Candidate L0. It is NOT another attempt to extend the bounded natural-language anaphora grammar. The previous strict-P4 implementation's exception for a pure `Technique: docker` pointer is intentionally withdrawn.

**Read, in order:**

1. Current `output/template/.claude/scripts/check-instructions.mjs`, focusing on `TECHNOLOGY_LEXICON`, `PLATFORM_IDENTIFIERS`, `techniquePointerViolations`, `neutralityCheck`, dynamic vocabulary and `frame-terms` restrictions.
2. Current Level-0/Level-1 files, especially `.claude/rules/1-architecture/frame/boundaries.md`, `.claude/rules/0-core/http-api.md`, `.claude/rules/0-core/testing.md`, and `.claude/INSTRUCTION_MAP.md`.
3. `CANDIDATE.md`, `audit/DEFECT_DOSSIER.md`, the existing `output/REFINEMENT_REPORT.md`, and the earlier `L1-Restart-iteration_after_audit_1-CORRECTIVE_TASK.md` **as history only**.
4. Candidate L0's documented rule, if its local read-only reference is available: Levels 0/1 must not name concrete technologies outside its fixed platform. Its checker bans Docker, Swagger, ASP.NET, NuGet, and EF Core on these levels. The L0 code is a comparison oracle for *policy intent*, not source code to copy or a reason to weaken L1's additional checks. Do not leave the L1 workspace to search for L0; all test expectations below are authoritative.

Use the current 86-file `output/template/` from L1-Restart `iteration_after_audit_1`. Do not copy from `baseline/template/` or any other candidate, and do not restore the historical L1 line. Capture a start inventory/tree checksum **before** edits and check all immutable 144 manifest entries. The expected 86-file start-tree digest is `5ef3bc0a2ab1da1b715040ced1ab9f448691f79945712566e8d77e9a7050ed68`, calculated from within `output/template/` by `find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`. If it differs, investigate and stop before modifying any file; do not silently reset.

The earlier Restart contract allowed pure named Level-2 technique references at Levels 0/1. **This task explicitly supersedes that permission**. Old acceptance rows such as ``Technique: `docker``` => PASS, ``See technique: `docker``` => PASS, a ``Containers -> `docker``` route => PASS, and their formatting-invariance derivatives must now become FAIL. Do not report those deliberate oracle changes as regressions against the NEW contract. Equally, do not silently rewrite prior reports or claim the old test suite passed unchanged.

## 2. Final, deliberately conservative P4 contract

- **Level 0 Core and Level 1 Architecture:** no naming of concrete implementation technologies, whether prescribing, defaulting, selecting, recommending, mentioning, routing, or simply linking to them. The spelling, syntax, heading/list/paragraph placement, code formatting, case, and `Technique:`/`See`/arrow wrapper cannot legalize the token.
- **Level 2 Technology and Level 3 Project:** concrete technique definition, API bindings, project selections and package/technology decisions remain allowed where ownership and other constraints permit them. Do **not** remove the Docker/Swagger skills or the user's ability to select those technologies at the appropriate level.
- **Neutral references:** role, capability, facet and generic-procedure references which do NOT identify a concrete implementation remain allowed (e.g. `Use the deployment technique defined at Level 2`, `backend-testing.framework`, generic `HTTP API` guidance / `http-api` knowledge reference). A Level-2 classification alone does NOT make every abstract skill ID a concrete technology; conversely, `docker`, `swagger`, `ef-core`, or an implementation-bearing alias is not excused because it is a skill ID.
- **Fixed platform:** apply the same substantive boundary as Candidate L0 for technologies it distinguishes: .NET/C#/TypeScript and Git may be referred to when genuinely within the fixed platform; ASP.NET and NuGet are NOT exemptions to technology neutrality at Levels 0/1. Neutral HTTP/protocol wording is not automatically a concrete implementation. Keep stable architectural *role* terminology. Do not invent new platform exceptions. L1's pre-existing stronger API-shape, dynamic module-token, package-ID and frame no-legalizing checks remain in force; harmonization must not make them weaker.
- This deterministic lexical/domain check is intentionally conservative and finite: do not promise semantic understanding of all natural-language paraphrases or arbitrary new technologies. Document its threat model and limits without watering down the no-exemption rule for **recognized** concrete technologies.

**Important source data:** `1-architecture/frame/boundaries.md` currently mentions `ASP.NET Core` in Domain/Application policy while Candidate L0's neutrality rule disallows ASP.NET on Levels 0/1. Replace only the specific implementation name with neutral boundary terminology such as `web-framework/transport implementation types`; do NOT drop or weaken the prohibition on inward framework/transport leakage. The `INSTRUCTION_MAP.md` currently describes Level-0/1 pure named technique pointers as allowed and describes ASP.NET Core/NuGet as fixed-platform terms; correct that policy description to reflect this decision. The map is metadata, not a new normative policy owner.

## 3. Authorized persistent changes

- `output/template/.claude/scripts/check-instructions.mjs`: remove or bypass the *technology masking exemption* from the Level-0/1 enforcement path and align the recognized concrete vocabulary and fixed-platform boundary. Keep all other instruction, dependency, capability, frame and API-shape enforcement operational. Remove unused helpers only when safe and locally testable; avoid a wholesale rewrite of `parseBlocks` or the rest of the checker.
- `output/template/.claude/rules/1-architecture/frame/boundaries.md`: narrowly neutralize concrete names where necessary while preserving requirements, triggers, owner and scope.
- `output/template/.claude/INSTRUCTION_MAP.md`: narrowly document the harmonized boundary; ensure its routing instructions remain accurate.
- Any *additional* Level-0/Level-1 Markdown file **only if** the new clean-template check pinpoints an equivalent disallowed concrete name; record precise before/after evidence and preserve intent.
- Append a separate `iteration_after_audit_2` section to **existing** `output/REFINEMENT_REPORT.md` with the explicit protocol change, test oracle changes, file hashes, evidence and remaining limits. Do not edit previous sections to erase experimental history.

No other persistent changes: no settings/hook/worktree code, module/slot/contract/facet selection, Level-2/Level-3 technique rule or skill changes, no new output folders or policy owners, and no modifications to immutable research inputs. Temporary harness/sandboxes only under `output/.work/`, removed last.

## 4. Acceptance matrix (real checker, fresh isolated copies)

Inject into eligible Level-0 and Level-1 rule files, with correct metadata and original content retained. Negative rows must exit nonzero with **a technology-neutrality diagnostic for the injected target token**, not an incidental setup/header/reference failure. Positive rows must pass with zero violations and zero warnings. Include directly embedded heading, list, nested list, paragraph, wrapped line, and inline-code forms where meaningful; use small *finite* variants, not unbounded fuzzing.

| ID | Fixture or invariant | Expected |
| --- | --- | --- |
| N01 | ``Technique: `docker`.`` | FAIL |
| N02 | ``See technique: `docker`.`` | FAIL |
| N03 | ``Containers -> `docker`.`` | FAIL |
| N04 | ``Technique: `docker`. Selected for deployment.`` | FAIL |
| N05 | ``Technique: `docker`. This is the selected deployment technology.`` | FAIL |
| N06 | `### Deployment technique` followed by ``- Technique: `docker`.`` | FAIL |
| N07 | `## Must use Swagger` | FAIL |
| N08 | ``Selected technology: `swagger``` or ``See technique: `swagger``` | FAIL |
| N09 | a concrete known implementation in a Markdown list and nested child, with neutral siblings inserted/removed | FAIL in every form |
| N10 | `ASP.NET Core` or `NuGet` embedded in an eligible Level-0/1 rule | FAIL, matching L0's boundary |
| N11 | `EF Core`, `NUnit`, `Angular`, an API-shaped concrete identifier, or module implementation name in Level 0/1 | FAIL |
| P01 | `Use the deployment technique chosen at Level 3.` | PASS |
| P02 | `See the Level-2 deployment guidance.` | PASS |
| P03 | `Use the implementation selected by the backend-testing capability.` | PASS |
| P04 | `Framework binding: `backend-testing.framework`.` | PASS |
| P05 | generic HTTP response-contract guidance / existing `http-api` neutral skill reference | PASS |
| P06 | independent normative policy such as `Must run unit tests.` | PASS |
| P07 | `TypeScript` used solely as an L0-fixed-platform term; `.NET`, `C#`, and `Git` where permitted | PASS, absent independent other violations |
| P08 | Concrete `docker`, `swagger`, `ef-core` technique content under appropriate Level 2, and approved technology choices under Level 3 | PASS for neutrality (other rules still apply) |
| P09 | Existing clean original L1 template, after minimum necessary Level-0/1 vocabulary normalization | PASS |

Do not physically insert a Markdown table's formatting backslashes into test fixtures. `N01`, `N02`, etc. are labels, not runtime markers. Independently check case changes and inline code spans for at least Docker and Swagger, to prevent a bypass via formatting. Ensure Level-1 frame terms / placement examples never authorize a concrete token. Verify both Level 0 and Level 1 with each applicable fixture.

### Preservation gates

1. Instruction checker on the clean template: zero errors **and** zero warnings; expected artifact count is 68 unless a justified existing rule changes accounting. JavaScript syntax check for all `.mjs`/`.js` runtime files.
2. Level headers/path placement, references, same-or-more-stable dependency directions, 4 static slots (architecture frame, persistence required leaf, backend-testing required leaf, frontend optional leaf), contracts, facet selections, optional frontend clearing and `binds:` negative mutation checks.
3. Preserve D1–D17's non-neutrality mechanics, especially PreToolUse `onFailure: "block"`, PostToolUseFailure, actual-state tracking, worktrees, encodings, Stop deduplication. These runtime files must stay byte-identical. Prefer comparing hashes and reusing valid earlier evidence over expensive unrelated live Windows tests.
4. Preserve source inventory policies: 194 original records + GOV-017/GOV-018 = 196; zero unauthorized changes of owner, trigger, minimum scope, conditionality or strength. Since the architecture boundary text needs a specific technology-to-role wording change, compare that actual policy **semantically**; mere file identity is not sufficient for that edited rule. Do not claim a fresh full 196-item semantic audit without performing one.
5. Verify original immutable files and original candidate identity; enumerate all files changed, prove the rest of template files byte-identical. Verify consistent English-only code/docs and clean `output/` contents (`template/` and `REFINEMENT_REPORT.md` only).
6. Compare the **actual agreed L0 contract**, not L0's checker accuracy on unseen vocabulary. Do not copy L0's finite regex wholesale at the expense of L1's stronger structural guards.

## 5. Bounded execution and stopping

1. Save original tree checksum/inventory and confirm expected source shape. Write ONE finite table-driven harness in `output/.work/` and freeze expected outcomes BEFORE changing code. Explicitly record which older pure-pointer PASS fixtures have become FAIL due to the user-approved change.
2. Reproduce on the unmodified checker: e.g. N01 PASS (old behavior), then implement the smallest safe change. Do not repeatedly inspect previous iterations or reconstruct deleted historical harnesses.
3. Run the fixed matrix in fresh copies; check actual Level-0/1 files and minimal text migration. A FAIL must be the intended neutrality diagnostic. Run only focused preservation tests and one cumulative final audit; if there is a concrete regression, allow ONE directly evidenced correction and ONE reconfirmation.
4. Append a clear report section: reason for the policy change, explicit old/new contract, counts, negative/positive control results, affected rule/map wording, source-policy preservation evidence, file hashes, and methodology note: *this is an evolved acceptance criterion* and must be disclosed when comparing candidates. No claim that original runs used identical P4 semantics.
5. Delete `output/.work/` after reporting. Verify `output/` contains only `template/` and `REFINEMENT_REPORT.md`. If clean, return `READY_TO_FREEZE (contract harmonization complete)` and STOP. If a gate cannot be proved, return `BLOCKED` with exact failures and STOP; do not restart exploratory audit cycles or argue with a Stop hook.

**Research integrity:** Retain previous iterations and their original tests in reports, label deliberate P4/P6 oracle changes separately from bug fixes, and ensure future architecture comparisons use the same harmonized contract. This is a conservative *design trade-off*, not a discovered defect or removal of the Level-2 Docker technique.

