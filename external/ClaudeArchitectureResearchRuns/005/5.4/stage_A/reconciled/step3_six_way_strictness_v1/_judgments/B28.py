from jdsl import C, D, P  # noqa: F401

P("WF-009",
  dims=["D1 report what was actually run with PASS / NOT RUN / NOT APPLICABLE; never imply an unchecked area passed"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each verify report section: M verify/SKILL.md:185-197, M1 :167-168, L0 :66-78, L1 :65-76, K0 :80 (adds FAIL), K1 :72. build-fix report templates (PASS / NOT RUN / NOT APPLICABLE), git-workflow ('do not claim checks were run if they were not') and security-scan reporting carry the same rule in all six.")

P("WF-010",
  dims=["D1 the code-reviewer is an independent, read-only reviewer that runs code-review as the canonical procedure without redefining policy",
        "D2 mechanical read-only boundary of the code-reviewer agent (disallowedTools frontmatter)"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="D1 in each agent file and code-review skill: M agents/code-reviewer.md:7-18 + code-review/SKILL.md:15-18, M1 :7-22, L0 :6-17, L1 :4-16, K0 :4-15, K1 :7-16. Five preload the skill through `skills:` frontmatter; L0's agent body (line 15) instructs it to read code-review/SKILL.md first, which delivers the same procedure on the first step. All six check-instructions scripts fail when the agent does not disallow Write and Edit or does not delegate to code-review (M check-instructions.mjs:185-186, M1 check-instructions.js:110-119, L0 tools/check-instructions.mjs:221-227, L1 :486-492, K0 :257, K1 :245).",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["M1", "L1", "K0"], ["M", "L0", "K1"]],
           "M1, L1 and K0 disallow Write, Edit, MultiEdit and NotebookEdit; M, L0 and K1 disallow Write, Edit and NotebookEdit only. No candidate disallows the shell tool, so in all six a reviewer that ignored the text could still change files through the shell; the frontmatter is therefore a partial guard everywhere, and the read-only obligation rests on the same instruction text in all six. Whether the intended host still offers a separate MultiEdit tool is UNVERIFIED (live host NOT_RUN); if it does not, the difference disappears.",
           root="RC-ENF-REVIEWER-MULTIEDIT",
           evidence={"M1": ["FG-M1-89077067b5"], "L1": ["FG-L1-0df36200a2"], "K0": ["FG-K0-7b0458f4b5"], "M": ["FG-M-7fbfeb8233"], "L0": ["FG-L0-25a6e19865"], "K1": ["FG-K1-031dab0b4e"]})],
  enforcement="Frontmatter and check-instructions code read; agent tool restriction in a live host NOT_RUN.")

P("WF-011",
  dims=["D1 review priorities: correctness, security/authorization, data integrity, architecture, concurrency/integration, meaningful tests, maintainability, credible performance; style never above defects"],
  label="FULL_SEMANTIC_PARITY",
  same="Same ordered list and the same style clause in each code-review skill: M :25-37, M1 :19-23, L0 :17, L1 :14, K0 :14, K1 :20.")

P("WF-012",
  dims=["D1 no findings invented to populate categories; when none exist, say so and name important unverifiable areas"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each code-review skill: M :186-188, M1 :159-161, L0 :72, L1 :71, K0 :66, K1 :93; M, M1, K0 and K1 add 'no filler praise' (L0 :72 also). security-scan references in all six add 'do not invent exploitability'.")

P("WF-013",
  dims=["D1 reproduce and diagnose the actual failure before editing; fix root causes before downstream symptoms"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each build-fix skill's principles and in the same seven-step backend/frontend loops: M :28-30 + :96-116, M1 :24 + :85-105, L0 :16 + :36-42, L1 :14 + :40-46, K0 :14 + :61-79, K1 :20 + :41-46. Cross-stack contract failures are handled the same way in all six ('determine which contract is authoritative').")

P("WF-014",
  dims=["D1 small bounded repair iterations; rerun the narrowest failing check after each meaningful fix; widen only after the focused failure is resolved; stop and reassess on the same listed conditions"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each build-fix skill: M :31 + :195-205, M1 :26-28 + :196, L0 :17 + :66, L1 :15 + :72, K0 :15 + :123, K1 :22 + :72 (same stop-and-reassess list: surviving root failure, growing unrelated failures, incompatible toolchain, unavailable infrastructure, unresolvable package compatibility, product decision needed).")

P("WF-015",
  dims=["D1 never weaken, delete, skip or suppress relevant tests or compiler/TypeScript/lint/analyzer failures to make verification pass"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each build-fix skill: M :34-35 (and :148-152 on weak assertions), M1 :29-30, L0 :18, L1 :54, K0 :16, K1 :23. Frontend invalid shortcuts (any, disabling strict mode, suppressing template diagnostics) are listed in all six.")

P("WF-016",
  dims=["D1 fix generated output at its authoritative source and regenerate; do not manually patch disposable generated output unless the workflow treats it as maintained source (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each build-fix (or development-workflow) skill: M development-workflow/SKILL.md:76-84, M1 build-fix :187-192, L0 build-fix :62, L1 :62, K0 :119, K1 :68; angular skills in all six apply it to OpenAPI clients ('regenerate when the contract changes').")
