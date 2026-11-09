from jdsl import C, D, P  # noqa: F401

P("GOV-008",
  dims=["D1 approved project-level tunable limits and defaults live in CUSTOM_SETTINGS.md",
        "D2 SPECIFICATION.md owns behavioral intent"],
  label="FULL_SEMANTIC_PARITY",
  same="All six state both parts in root CLAUDE.md with the same examples (maximum lengths, page sizes, retention, numeric thresholds): M :45-48, M1 :30-32, L0 :28, L1 :21, K0 :21, K1 :20 ('never overrides SPECIFICATION.md'). The custom-settings skill in each records the value with a stable name and purpose.")

P("GOV-009",
  dims=["D1 SPECIFICATION.md and CUSTOM_SETTINGS.md must not contradict each other",
        "D2 on conflict, stop and resolve which source must be corrected (with the user)"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="All six state the no-contradiction rule and a stop on conflict in root CLAUDE.md: M :49-50, M1 :34-35, L0 :29, L1 :21, K0 :21, K1 :21. Each has a post-edit or Stop reminder on edits to either file (M file-change.mjs:33-45, M1 stop.js:65-73 and post-tool-use.js:72-74, L0 claude-hook.mjs:657-662, L1 post-change-checks.mjs:315-336 and stop-cochange.mjs:68-69, K0 hook.cjs:466-468, K1 actual-state.cjs:183); none detects a contradiction.",
  diffs=[D("D2", "NORMATIVE", "TRUE_NORMATIVE_VARIANCE", False, [["M", "M1", "L1", "K0", "K1"], ["L0"]],
           "M, M1, L1, K0 and K1 say 'stop and ask which source must be corrected' (K1: 'never choose one silently'). L0 :29 says 'stop and resolve which source must be corrected before continuing', the canonical wording, which alone does not name the user. Choosing which product source wins is product behavior that L0 routes to approval elsewhere (CLAUDE.md:25-26 and Reserved item 10 at :49), so the combined L0 text requires approval too; the difference is wording at this owner only.",
           root="RC-TXT-L0-CONFLICT-WORDING", evidence={"L0": ["FG-L0-4b96b1b4d1"], "M": ["FG-M-5bd1278f35"], "K1": ["FG-K1-78ad9454cb"]})])

P("GOV-010",
  dims=["D1 do not silently invent a tunable value that materially changes accepted input or observable behavior",
        "D2 propose it, get approval, record it in CUSTOM_SETTINGS.md and synchronize it"],
  label="FULL_SEMANTIC_PARITY",
  same="All six carry the same sentence with the same four steps in root CLAUDE.md: M :51-55, M1 :36-39, L0 :30, L1 :22, K0 :22, K1 :22, plus the Reserved item 'product behavior or tunable values not defined by product sources' (M :128, M1 :90-91, L0 :49, K0 :46, K1 :42; L1 via its unclear-case test :36). The configuration skills in all six add that example numbers are illustrative.")

P("GOV-011",
  dims=["D1 never store secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers or incidental constants in CUSTOM_SETTINGS.md"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="The canonical exclusion list is identical in root CLAUDE.md of all six: M :56-58, M1 :40-43, L0 :31, L1 :23, K0 :23, K1 :23.",
  diffs=[D("D1", "NORMATIVE", "TRUE_NORMATIVE_VARIANCE", False, [["M", "M1", "L1", "K0", "K1"], ["L0"]],
           "Five candidates also exclude framework defaults the project has not intentionally overridden (M1 in root CLAUDE.md:40-43; M, L1, K0, K1 in the custom-settings skill). L0 has no such exclusion (searched CLAUDE.md and custom-settings). This is an extra beyond the canonical list, not part of GOV-011; it is carried to the extras inventory.",
           root="RC-TXT-FRAMEWORK-DEFAULT-EXCLUSION", evidence={"M1": ["FG-M1-f9c4a7a40d"], "K0": ["FG-K0-1b6bd25ab4"], "L1": ["FG-L1-90541afb64"], "K1": ["FG-K1-3ee4b79f21"]})])

P("GOV-012",
  dims=["D1 prefer simple maintainable solutions with complexity proportional to current requirements and no speculative abstractions (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in root CLAUDE.md of all six: M :62-64, M1 :51-52, L0 :63, L1 :27, K0 :27, K1 :50. The many partial links are applications inside technique skills (DI registration, HttpClient models, test harness size, Angular Material); they are compared under their own policies and in the extras inventory, not as parts of this default.")

P("GOV-013",
  dims=["D1 do not introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need"],
  label="FULL_SEMANTIC_PARITY",
  same="Verbatim the same MUST_NOT in root CLAUDE.md of all six: M :65-66, M1 :53-54, L0 :64, L1 :28, K0 :28, K1 :51. Skill-level applications (snapshot libraries, Identity, formatters, resilience, scaffolding) restate it per technique; K1 project-structure:65 lists patterns that 'require an approved need', which all six already reserve under ARC-020.")

P("GOV-014",
  dims=["D1 keep changes within the requested scope",
        "D2 preserve existing behavior unless the task or approved specification requires a change"],
  label="FULL_SEMANTIC_PARITY",
  same="Same sentence in root CLAUDE.md of all six: M :67-68, M1 :55-56, L0 :65, L1 :29, K0 :29, K1 :52. Skill-level applications (restructuring steps, build-fix, style-only rewrites, dependency cleanup, git workflow) restate it in all six and are compared under their own policies.")
