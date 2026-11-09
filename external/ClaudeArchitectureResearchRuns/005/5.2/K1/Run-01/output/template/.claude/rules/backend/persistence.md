---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# Persistence Standards (technology-neutral)

Technology bindings and seeder placement: `.claude/rules/backend/persistence-technology.md`. Layer placement: `.claude/rules/backend/architecture-style.md`.

## Data access efficiency

- Default: filter and project in the database when practical, avoid unnecessary round trips, over-fetching and N+1 patterns, and paginate potentially large result sets.

## Development seed data

- Default: an empty Development database receives a small, deterministic, representative seed dataset that covers the meaningful states and relationships, such as newly created, active, completed and archived entities, entities with and without optional values and relationships, and meaningful boundary states. Do not generate every combination or large random data.
- Automatic development seeding runs only in the Development environment. Never seed Production automatically. Tests own their own setup and never use the development seeder.
- When development data already exists, leave it unchanged. The seeder is not an automatic synchronization, repair, upgrade, overwrite or recreation mechanism for an existing Development database; a developer who wants the current dataset recreates the local database explicitly.
- Seed entities must preserve the current Domain invariants and valid relationships. Prefer readable, deterministic examples over exhaustive or random combinations. When the required graph is complex, the task requirements should describe the dataset instead of having it invented.
