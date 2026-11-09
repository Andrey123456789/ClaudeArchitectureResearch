from jdsl import C, D, P  # noqa: F401

_STOP = ("All six register a Stop hook that blocks finishing once per change state with co-change reminders and never re-blocks while stop_hook_active: "
         "M stop-co-change.mjs:28/:104 (decision block), M1 stop.js:87-108 (hook.block), L0 claude-hook.mjs:753-797 (feedback, exit code), "
         "L1 stop-cochange.mjs:41/:85 (decision block), K0 hook.cjs:548/:582 (decision block), K1 dispatch.cjs:126-137 (exit 2). Live-host handling NOT_RUN.")

P("PST-006",
  dims=["D1 existing representative Development data is left unchanged; the seeder is never synchronization, repair, upgrade, overwrite or recreation; developers recreate the database explicitly"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT with the explicit-recreation note in each rule: M persistence.md:33-36, M1 persistence-technology.md:54-57, L0 data-lifecycle.md:20, L1 seeding.md:15 (with the explicit `database drop` command in the capability), K0 persistence.md:30, K1 persistence.md:26. Anchor-entity detection is the same technique in all six ef-core skills.")

P("PST-007",
  dims=["D1 seed entities preserve current Domain invariants and valid relationships",
        "D2 prefer readable deterministic examples over exhaustive/random combinations"],
  label="FULL_SEMANTIC_PARITY",
  cells={"M1": C(owners=["FG-M1-d47eac012e", "FG-M1-da5ec8ca30"], note="Step 2 override: no direct owner; persistence-technology.md:58-59 states D1 and :38-41 states D2.")},
  same="Same two parts in each rule: M persistence.md:37-39, M1 persistence-technology.md:58-59 (D1) with :38-41 (D2), L0 data-lifecycle.md:21, L1 seeding.md:16, K0 persistence.md:31, K1 persistence.md:27. ef-core skills in all six add 'match the current Domain and persistence model'.")

P("PST-008",
  dims=["D1 when Domain/persistence changes affect seeded entities, update the development seeder in the same change",
        "D2 Stop-time reminder when model files change without a seeder change"],
  label="FULL_SEMANTIC_PARITY",
  same="D1 is the same MUST with the same list of affecting changes in each workflow owner: M development-workflow:45-52, M1 persistence-change:46-52, L0 development-workflow:48, L1 capabilities/persistence/ef-core/workflow.md:10, K0 development-workflow:57, K1 persistence-change:44. D2: all six check model-without-seeder at Stop (M stop-co-change.mjs:65-69, M1 stop.js:44-56 with MODULE.md coChange 'seed data', L0 claude-hook.mjs:766-768, L1 stop-cochange.mjs with enforcement.json cochange.seederPathGlobs, K0 hook.cjs:557-562, K1 facets/persistence-technology.cjs:32-39). " + _STOP,
  enforcement="Same reminder class in all six (static source read); live effect NOT_RUN.")

P("PST-009",
  dims=["D1 when a CUSTOM_SETTINGS.md change affects schema metadata: update the EF mapping, create the appropriate migration per the project workflow, verify seeding, update provider-sensitive tests; do not casually alter existing migrations",
        "D2 Stop-time reminder when model files change without a migration"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same four-step procedure with the 'do not casually alter existing migrations' clause in each owner: M custom-settings:54-63, M1 persistence-change:61-68, L0 custom-settings:29-34, L1 ef-core/workflow.md:17-22, K0 custom-settings:30-33, K1 custom-settings:32.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "L1", "K1"], ["M", "L0", "K0"]],
           "Model-without-migration reminder: M1 stop.js:44-56 (MODULE.md coChange companions 'migrations'), L1 stop-cochange.mjs:60, K1 facets/persistence-technology.cjs:40-47 remind at Stop when Domain or entity-configuration files change without a migration; M, L0 and K0 check only model-without-seeder and migration review (searched their Stop hooks). " + _STOP,
           counterexample="Same task: a CUSTOM_SETTINGS.md maximum length changes, the agent updates HasMaxLength in the entity configuration and the validator but adds no migration. M1, L1 and K1 block the first stop with a missing-migration reminder; M, L0 and K0 let it finish (their Stop reminders cover only the seeder). Live effect NOT_RUN.",
           root="RC-ENF-MIGRATION-REMINDER",
           evidence={"M1": ["FG-M1-369fbba378"], "K1": ["FG-K1-8e911dab3a"], "M": ["FG-M-a44f90d9ec"], "L0": ["FG-L0-f8098f7cb8"], "K0": ["FG-K0-a2b3b601f1"], "L1": ["FG-L1-9d31ff8410"]})],
  enforcement="Source-read Stop hook code; not executed.")

P("PST-010",
  dims=["D1 treat EF Core migrations as source code; review each generated migration before committing (destructive changes, column recreation, data migrations, indexes, FKs, delete behavior)",
        "D2 Stop-time reminder to review changed migration files"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same MUST with the same six review points in each owner: M development-workflow:53-58, M1 persistence-change:37-42, L0 development-workflow:49, L1 ef-core/workflow.md:12, K0 development-workflow:58, K1 persistence-change:43.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M", "L0", "K0", "K1"], ["M1", "L1"]],
           "Migration-review reminder when migration files changed: M stop-co-change.mjs:70-72, L0 claude-hook.mjs:769-771, K0 hook.cjs:564-567, K1 facets/persistence-technology.cjs:48-52; M1 stop.js and L1 stop-cochange.mjs remind only about missing migrations, not about reviewing changed ones (searched both). Complementary to PST-009 D2: no candidate has both reminders except K1. " + _STOP,
           counterexample="Same task: the agent adds a migration that drops and recreates a column. M, L0, K0 and K1 block the first stop with 'review the migration before committing'; M1 and L1 let it finish without that reminder. Live effect NOT_RUN.",
           root="RC-ENF-MIGRATION-REMINDER",
           evidence={"M": ["FG-M-8adc7474ce"], "L0": ["FG-L0-5723bbec95"], "K0": ["FG-K0-7264c86b25"], "K1": ["FG-K1-ef88b5c4f7"], "M1": ["FG-M1-98269f98e1"], "L1": ["FG-L1-d8b80ec5b2"]})],
  enforcement="Source-read Stop hook code; not executed.")
