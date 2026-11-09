from jdsl import C, D, P  # noqa: F401

P("GOV-001",
  dims=["D1 a non-empty SPECIFICATION.md is the authoritative source for project-specific functional requirements and observable behavior"],
  label="FULL_SEMANTIC_PARITY",
  same="All six state it in root CLAUDE.md (always loaded) with the same non-empty condition and object: M CLAUDE.md:26, M1 :11, L0 :24, L1 :17, K0 :17, K1 :15. The empty-template remark is descriptive. Code-review mirrors (M, L1, K0, K1) restate it and add nothing.")

P("GOV-002",
  dims=["D1 before planning or implementing a new application or substantial feature, read SPECIFICATION.md"],
  label="FULL_SEMANTIC_PARITY",
  same="All six place the step in the development-workflow skill with the same trigger (new application or substantial feature) and timing (before planning or implementing): M :19, M1 :15, L0 :17, L1 :12, K0 :14, K1 :18. All six also name CUSTOM_SETTINGS.md (approved register item 8.7, aligned in v1); L0 adds 'any feature specification', a harmless widening of what to read. Same skill-level delivery in all six; the trigger is the workflow itself.")

P("GOV-003",
  dims=["D1 do not silently weaken, contradict or materially extend approved behavior",
        "D2 do not invent user-visible behavior, limits, defaults, restrictions or workflows"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="All six carry both parts in one root CLAUDE.md sentence (always loaded): M :29-32, M1 :15-18, L0 :25, L1 :18, K0 :18, K1 :16, each adding 'even if reasonable / not forbidden' or 'not defined by the product sources'. Code-review and verify skills in all six check drift in both directions.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["M", "M1", "L0", "L1", "K0", "K1"]],
           "Only advisory reminders exist: post-edit hooks in M, M1, L0, L1, K0 and K1's actual-state checker remind on edits to SPECIFICATION.md/CUSTOM_SETTINGS.md (K0 hook.cjs:466-468 is the one Step 2 linked to GOV-003). None blocks an invented behavior; enforcement is the same advisory level in all six, recorded so the hook link is not read as a K0-only check.",
           evidence={"K0": ["FG-K0-4e26e54678"]})])

P("GOV-004",
  dims=["D1 when an omitted detail must be decided and materially affects observable behavior, propose the smallest reasonable option and ask for approval"],
  label="FULL_SEMANTIC_PARITY",
  same="Same condition (omitted, must be decided, materially affects observable behavior) and the same action (smallest reasonable option, ask) in root CLAUDE.md of all six: M :33-35, M1 :19-20, L0 :26, L1 :19, K0 :19, K1 :17. M, M1, L0, K0 and K1 also list undefined product behavior/tunable values as Reserved item 10; L1's Reserved list (CLAUDE.md:35) covers it through 'change observable behavior' in the unclear-case test (:36). No checker in any.")

P("GOV-005",
  dims=["D1 routine internal choices that do not change observable behavior need no approval (decide and proceed)"],
  label="FULL_SEMANTIC_PARITY",
  cells={c: C(compliance="STRICTER_THAN_CANONICAL", note="Delegated class says decide and proceed / do not ask, a directive rather than the canonical permission; same in all six.")
         for c in ["M", "M1", "L0", "L1", "K0", "K1"]},
  same="All six define Delegated identically in root CLAUDE.md (local, reversible, no boundary/dependency/convention/contract/observable change) and tell the agent to decide without asking: M :106-111 'Decide without asking', M1 :68-70 'Decide it yourself', L0 :38 'do not ask approval for routine decisions', L1 :34+:37, K0 :35 'without asking', K1 :31+:44 'Do not escalate'. The canonical DEFAULT (no approval needed) is turned into a 'do not ask' directive by all six alike, so pairwise the force is the same.")

P("GOV-006",
  dims=["D1 observable string semantics (case, collation, culture/ordinal, normalization, trimming, uniqueness, lookup) are product behavior",
        "D2 when unspecified, do not choose them silently; ask for approval"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="All six list the same seven semantics as product behavior in root CLAUDE.md and require approval when the sources do not define them: M :36-41, M1 :23-28, L0 :27, L1 :20, K0 :20, K1 :19. M1 docs/capability-selection.md:18-22 and K1 ef-core:220 state the SQL Server default collation is a technology default, not an approved semantic, so neither pre-approves a semantic.",
  diffs=[D("D2", "NORMATIVE", "TRUE_NORMATIVE_VARIANCE", False, [["L1", "K0", "K1"], ["M", "M1", "L0"]],
           "M, M1 and L0 add a threshold: ask when the choice 'materially affects equality, uniqueness, lookup, or accepted input'. K0, K1 and L1 ask whenever the semantics are observable and undefined; L1 also names choices made implicitly through database or framework defaults. Only an observable choice that does not materially affect those four effects would separate them, an edge case (canonical also reads 'when observable').",
           evidence={"L1": ["FG-L1-5bc921b585"], "M": ["FG-M-9d4fa64c10"], "M1": ["FG-M1-ebc7b9f82c"], "L0": ["FG-L0-d0cfcf42bd"]})])

P("GOV-007",
  dims=["D1 when a new behavioral rule is approved, update the durable source of truth (SPECIFICATION.md when appropriate)"],
  label="PARTIAL_PARITY_WITH_DELTA",
  cells={"L0": C(owners=["FG-L0-60fa521e22"], note="Step 2 links no direct owner (override); development-workflow:44 states the full rule."),
         "L1": C(compliance="STRICTER_THAN_CANONICAL", note="'in the same change'"),
         "K1": C(compliance="STRICTER_THAN_CANONICAL", note="'in the same change'"),
         "M1": C(note="Owner only in architecture-decision skill:61-62; development-workflow has no restatement."),
         "K0": C(note="Owner only in architecture-decision skill:37; development-workflow step 3 routes approved decisions there.")},
  same="All six require the update in a workflow skill: M development-workflow:37-39 and architecture-decision:54-60, M1 architecture-decision:61-62, L0 development-workflow:44, L1 development-workflow:22, K0 architecture-decision:37, K1 development-workflow:48. All six also have a post-edit reminder when SPECIFICATION.md changes (M file-change.mjs:40-45, M1 post-tool-use.js:72-74, L0 claude-hook.mjs:657-662, L1 post-change-checks.mjs:322-323 (not linked by Step 2), K0 hook.cjs:468, K1 actual-state.cjs:181-183); none detects a missing update.",
  diffs=[D("D1", "NORMATIVE", "TRUE_NORMATIVE_VARIANCE", False, [["L0", "L1", "K1"], ["M", "M1", "K0"]],
           "L0, L1 and K1 require the update 'in the same change'; M, M1 and K0 name no timing. In a single-task study run both end with the source updated; only a multi-change sequence separates them.",
           evidence={"L0": ["FG-L0-60fa521e22"], "L1": ["FG-L1-64120344e7"], "K1": ["FG-K1-68a63438b7"], "M": ["FG-M-b5f7b8480b"]}),
         D("D1", "DELIVERY", "DELIVERY_REACHABILITY_VARIANCE", False, [["M", "L0", "L1", "K1"], ["M1", "K0"]],
           "M1 and K0 carry the rule only in architecture-decision, which their workflows invoke after a Decision Request is approved (K0 development-workflow:16); M, L0, L1 and K1 also state it in development-workflow. Both routes are taken when a behavioral rule is approved, so the reach difference is not material.",
           evidence={"M1": ["FG-M1-c786842d64"], "K0": ["FG-K0-0bd6751e04"]})])
