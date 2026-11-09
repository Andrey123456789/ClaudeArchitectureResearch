from jdsl import C, D, P  # noqa: F401

_ROUTE = "Root CLAUDE.md routes implementation work to development-workflow in all six (M :178, M1 :142, L0 :81, L1 :47, K0 :65, K1 :69)"

P("WF-001",
  dims=["D1 inspect relevant existing code before a non-trivial change and apply the rules/skills that govern the touched areas"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST as the first development-workflow step in all six: M development-workflow/SKILL.md:21-22, M1 :21-22, L0 :37, L1 :17 (adds 'read path rules that have not loaded yet'), K0 :20, K1 :22. " + _ROUTE + ". Procedure skills in all six (add-dependency, project-structure, security-scan, code-review, ci-cd/delivery) repeat the inspect-first step; L1's capability workflows add 'read the named rules first when they have not loaded'.")

P("WF-002",
  dims=["D1 substantial feature work or a new application runs code-review (or the code-reviewer agent) before final verification"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each development-workflow completion step: M :112-114, M1 :71-73, L0 :54, L1 :46, K0 :76, K1 :52; all six name the read-only code-reviewer agent as the delegate. " + _ROUTE + "; L0's routing row also names 'code review for substantial work, then verification'. No candidate enforces the review mechanically.")

P("WF-003",
  dims=["D1 run verify, scoped to the change's scope and risk, before declaring implementation complete"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each development-workflow skill (M :115-116, M1 :77-78, L0 :55, L1 :50, K0 :77, K1 :56) and in each always-loaded root CLAUDE.md routing table (M :179, M1 :150, L0 :83, L1 :47 'work is not complete until its verify step has run', K0 :66, K1 :70). build-fix, project-structure and custom-settings skills in all six end with verify. Stop hooks in all six are co-change reminders (seed, migration, tests), not a verify gate (settings.json Stop registrations read), so no candidate enforces verify mechanically.")

P("WF-004",
  dims=["D1 verify begins with the final changed-file set/diff: confirm scope, remove accidental artifacts/secrets, determine affected areas before choosing checks"],
  label="FULL_SEMANTIC_PARITY",
  cells={"K0": C(owners=["FG-K0-2f523edf9a", "FG-K0-e1ebc473cf"], note="Partial witness (PW38): verify/SKILL.md:12-23 read; step 1 states all four parts in one paragraph plus the affected-areas list."),
         "K1": C(owners=["FG-K1-82092370d9", "FG-K1-4473c96a85"], note="Partial witness (PW38): verify/SKILL.md:19-27 read; step 1 states all four parts.")},
  same="Same first verify step in all six: M verify/SKILL.md:24-37, M1 :21-31, L0 :16-22, L1 :14-21, K0 :12-23, K1 :19-27 (scope, no artifacts, no secrets, temporary diagnostics removed only after preservation, affected-area table).")

P("WF-005",
  dims=["D1 build affected projects (failure = not complete) and run relevant tests; investigate new relevant failures"],
  label="FULL_SEMANTIC_PARITY",
  cells={"L0": C(owners=["FG-L0-1d83ae1118", "FG-L0-5c333b9e20"], note="Partial witness (PW38): verify/SKILL.md:26-34 read; build, 'build failure means not complete', relevant tests and investigation of new failures are stated."),
         "K0": C(owners=["FG-K0-25fd94767f", "FG-K0-39a148aa2a"], note="Partial witness (PW38): verify/SKILL.md:25-42 read; step 2 'a build failure means the implementation is not complete', step 3 relevant tests and new-failure investigation."),
         "K1": C(owners=["FG-K1-5b25bc3b2f", "FG-K1-0a2dadc8a1"], note="Partial witness (PW38): verify/SKILL.md:29-35 read; same build and test steps.")},
  same="Same build and test steps in each verify skill: M :41-66, M1 :37-44, L0 :26-34, L1 :25-29, K0 :25-42, K1 :29-35; build-fix completion criteria in all six say a task is complete only when the affected scope is green. K0 check-dependencies.cjs:139 is a project-reference check (ARC-028), not a build gate.")

P("WF-006",
  dims=["D1 runtime smoke for a new runnable application or substantial startup/composition/configuration/persistence/full-stack change: API host starts, Development endpoint reachable, Swagger UI loads when exposed, configuration binds, database initializes, frontend dev server starts, base URL/CORS compatible"],
  label="FULL_SEMANTIC_PARITY",
  same="Same trigger, the same seven 'as applicable' surfaces and 'a successful build alone does not prove runtime composition' (M1, L0, K0) in each verify skill: M :68-79, M1 :53-60, L0 :38, L1 :33, K0 :46, K1 :39. Swagger UI loading is part of the list in all six (approved decision 8.1); swagger skills in all six point to this verify obligation.",
  challenge="Stored modality differs (M DEFAULT, M1/L0 MUST, L1/K0/K1 DEFAULT with a 'Default:' label). Read side by side: M, M1 and L0 use the same unlabeled imperative with 'as applicable' as a verify procedure step; L1, K0 and K1 prefix the identical sentence with their house label 'Default:'. Unlike API-019 there is no 'must' vs 'by default' wording contrast, and the trigger and qualifier are identical, so the label is not scored as a force difference. Sensitivity: scoring it would give a non-material NORMATIVE variance [M, M1, L0] over [L1, K0, K1] and the label PARTIAL_PARITY_WITH_DELTA.")

P("WF-007",
  dims=["D1 architecture, formatting/analyzer, dependency and security checks run when relevant to the change, not indiscriminately"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each verify skill: M :106-107, M1 :80-81 ('steps 5-8 are risk-scoped'), L0 :48, L1 :43-51, K0 :56, K1 :49. code-review skills in all six keep the full security-scan for requested audits or security-sensitive changes. The checker each candidate names for the architecture step differs by candidate (enforcement content is scored under ARC-*/DEP-* policies).")

P("WF-008",
  dims=["D1 on failure: smallest appropriate fix, rerun affected checks (and build/tests when code changed), repeat until green or genuine user input is required; never hide a known failure"],
  label="FULL_SEMANTIC_PARITY",
  same="Same loop in each verify skill: M :172-181, M1 :156-161, L0 :62, L1 :61, K0 :71-76, K1 :68; build-fix skills in all six add the same toolchain rule (do not change the declared SDK/Node/framework version because the local machine differs).")
