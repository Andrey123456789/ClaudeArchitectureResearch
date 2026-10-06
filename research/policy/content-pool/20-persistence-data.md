# Persistence & Data

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

EF Core persistence behavior, development seeding, migration/seeding separation, data lifecycle.

## PST-001 — Development seeding defaults to representative data

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Development Data Seeding`

For an empty Development database, maintain a small deterministic representative seed dataset covering meaningful states and relationships.

## PST-002 — Seeding is Infrastructure/bootstrap concern

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Development Data Seeding`

Development seeding belongs to Infrastructure/bootstrap and may use AppDbContext directly; it need not use Application repositories or IUnitOfWork.

## PST-003 — Seeder is dedicated and internal

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Development Data Seeding`

Keep substantial seed construction in a dedicated internal DbSeeder/Infrastructure initialization surface, not Program.cs, DbContext configuration, entity configurations, or migrations.

## PST-004 — Seeding is Development-only

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Environment`

Automatic development seeding runs only in Development; never automatically seed Production; tests own their own setup.

## PST-005 — Seeder does not migrate schema

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Empty Database Behavior`

The development seeder must not call Database.Migrate(), EnsureCreated(), or otherwise create/upgrade schema; migrations are applied separately before seeding.

## PST-006 — Existing Development data is not auto-synchronized

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Empty Database Behavior`

If representative data already exists, leave it unchanged; do not use the seeder as automatic synchronization, repair, upgrade, overwrite, or recreation of an existing Development database.

## PST-007 — Seed data preserves domain validity

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Seed Dataset`

Seed entities must preserve current Domain invariants and valid relationships; prefer readable deterministic examples over exhaustive/random combinations.

## PST-008 — Seeder co-changes with model

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Keeping Seed Data Current`

Whenever Domain or persistence changes affect seeded entities, update the maintained development seeder in the same change.
