> Level: 2-technology · Capability: persistence/ef-core · Facet: persistence.workflow · Owns: persistence change procedure — model/seed co-change, migration review, schema-affecting setting changes · Scope: backend · Loading: read by `development-workflow`, `custom-settings`, `verify`, `code-review`

# Persistence Change Workflow (EF Core)

Rules applied here: `persistence.access` and `persistence.seeding` — read `.claude/rules/2-technology/persistence/access.md` and `.claude/rules/2-technology/persistence/seeding.md` first when they have not loaded with backend files. Commands: `persistence.commands`. Technique: `ef-core` skill.

## A. Domain-model or persistence model change

1. Update the entity configurations (`IEntityTypeConfiguration<T>`) and the repository implementations affected by the change.
2. Whenever the domain-model or persistence change affects seeded entities — new required properties, removed or renamed properties, changed relationships, new required related entities, changed enum/status values, new meaningful states, changed domain invariants — update the maintained `DbSeeder` in the same change.
3. When the schema changes, add a migration from the implementation-layer project with the entry-point project as startup project.
4. Treat migrations as source code: review every generated migration before committing it, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys, and delete behavior.
5. When a migration changes entities represented in seed data, review `DbSeeder` together with it. Recreating an empty Development database at this revision must produce seed data valid for the migrated schema and current domain model; migrating an existing Development database does not require the seeder to patch existing rows.

## B. Schema-affecting `CUSTOM_SETTINGS.md` change

When an approved setting change affects schema constraints, indexes, column lengths, or other persistence metadata:

1. update the EF Core mapping;
2. create a new migration when the change requires a schema change — regenerate or edit an uncommitted migration only when that matches the project's normal migration workflow, and do not casually alter existing migrations;
3. verify Development seeding remains valid;
4. add or update persistence/integration tests when provider-specific behavior matters.

## C. Verification

- Build the affected projects and list or script the pending migrations to confirm the expected schema change.
- Apply migrations to a local Development database explicitly, then start the API in Development and confirm the seeder populates an empty database (or leaves an existing one unchanged).
- Production schema changes stay an explicit deployment step (`development-workflow`, delivery changes); a generated idempotent SQL script is often the better artifact for controlled deployment.

## Output

Report model changes, migration names with review notes (destructive operations called out), whether `DbSeeder` was updated or unaffected, and the tests added or updated.
