from jdsl import C, D, P  # noqa: F401

_CI = "CI/delivery obligations block (M development-workflow, M1 verify, L0 delivery-pipeline, L1 development-workflow, K0 delivery-pipeline, K1 delivery-change)"

P("WF-017",
  dims=["D1 CI definitions stay in source control, reproduce the supported build/test commands and never hide build/test failures"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _CI + ": M development-workflow/SKILL.md:96-97, M1 verify/SKILL.md:122-132, L0 delivery-pipeline/SKILL.md:20, L1 development-workflow/SKILL.md:40, K0 delivery-pipeline/SKILL.md:18, K1 delivery-change/SKILL.md:23. L0, K0 and K1 spell out examples (no continue-on-error, no suppressed exit codes, no skipped failing tests). ci-cd skills in all six add the same clean-environment pipeline check. No candidate checks CI files mechanically.")

P("WF-018",
  dims=["D1 frontend CI uses only scripts that exist in package.json and npm ci when a maintained lockfile supports it; no invented scripts, no reflexive npm install"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _CI + ": M :98-100, M1 verify :122-132, L0 :22, L1 :41 (names the lockfile-based clean install from frontend.commands, which is npm ci in capabilities/frontend/angular/commands.md:22-29), K0 :20, K1 :24. The lockfile presence check is a separate enforcement fact (RC-ENF-NPM-LOCKFILE, DEP-007).")

P("WF-019",
  dims=["D1 production migrations are not applied from normal application startup by default; production migration is an explicit deployment step with approved credentials, failing visibly",
        "D2 exception only on the user's explicit request naming it and its scope, recorded through architecture-decision; never Development seeding in Production"],
  label="FULL_SEMANTIC_PARITY",
  cells={"L0": C(owners=["FG-L0-701e75508b", "FG-L0-09d567edd3", "FG-L0-e6cfdca837"], note="Partial witness (PW38): delivery-pipeline/SKILL.md:33-35 read; all parts including the v2 C03 exception clause."),
         "K0": C(owners=["FG-K0-001a571f72", "FG-K0-8bba5b9da3"], note="Partial witness (PW38): delivery-pipeline/SKILL.md:26-27 read; all parts including the v2 C03 exception clause.")},
  same="Both parts with the identical v2 C03 exception sentence ('a generic workflow approval is not one, and it never allows Development seeding in Production') in each " + _CI + ": M development-workflow :101-106, M1 verify :130-133, L0 delivery-pipeline :33-35, L1 development-workflow :42, K0 delivery-pipeline :26-27, K1 delivery-change :34-35; v3 review C03-WF019-EXCEPTION holds in all six. project-structure skills in all six forbid wiring automatic Production migration at scaffold time. No candidate detects startup migration in code (M1's 'Database.Migrate' entry in capabilities/persistence/ef-core/MODULE.md:51 is an instruction-file leak token, not a code check).")

P("WF-020",
  dims=["D1 security review distinguishes confirmed findings from items needing verification and assigns severity from exploitability, reachability, impact and context, never from a pattern or raw CVSS alone"],
  label="FULL_SEMANTIC_PARITY",
  cells={"M1": C(owners=["FG-M1-c230907bc4", "FG-M1-bcab667457"], note="Partial witness (PW38): security-scan/SKILL.md:24-28 read; items 3-4 state both parts."),
         "L1": C(owners=["FG-L1-b04c04ff99", "FG-L1-f499d361d5"], note="Partial witness (PW38): security-scan/SKILL.md:14-20 read; items 2-3 state both parts (adds 'an OWASP category' to the excluded bases)."),
         "K0": C(owners=["FG-K0-36ee9fd74c", "FG-K0-474c43b98c"], note="Partial witness (PW38): security-scan/SKILL.md:20-24 read; item 3 states both parts."),
         "K1": C(owners=["FG-K1-3f4d6c85d3", "FG-K1-79b5d898ec"], note="Partial witness (PW38): security-scan/SKILL.md:21-25 read; item 3 states both parts.")},
  same="Same MUST in each security-scan skill's principles: M :106-117 + :158-161, M1 :24-28, L0 :19, L1 :14-16, K0 :20-22, K1 :21-23; all six label uncertain findings NEEDS VERIFICATION and say a theoretical missing limit is not automatically High.")

P("WF-021",
  dims=["D1 security review does not depend on a specific MCP server, agent, analyzer, commercial scanner or external tool; tooling is evidence, not the sole authority"],
  label="FULL_SEMANTIC_PARITY",
  same="Same clause in each security-scan skill: M :40-42, M1 :37-38, L0 :22, L1 :20, K0 :26, K1 :28.")

P("WF-022",
  dims=["D1 before committing, inspect the staged diff and include only the requested logical change; do not stage or clean unrelated modified files"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each git-workflow skill: M :37-39, M1 :43-44, L0 :27, L1 :26, K0 :31, K1 :29; the one-logical-change-per-commit default sits beside it in all six. Whether a commit happens at all is governed by the Git gating rules (RC-ENF-GIT-Q04, GOV-*), not by this policy.")
