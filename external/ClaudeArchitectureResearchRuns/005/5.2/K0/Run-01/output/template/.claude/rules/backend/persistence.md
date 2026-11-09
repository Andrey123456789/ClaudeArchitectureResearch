---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: repositories, Unit of Work, EF Core boundary, database access, development seeding | Loads: path-scoped (backend/**) -->
# Backend Persistence Standards

Persistence stack: DEC-DATA-01. Application-side boundary: `rules/backend/architecture.md`.

## Repositories

- **Default:** specific repository interfaces that represent actual, cohesive Application persistence needs rather than table-mirroring generic CRUD contracts. Define them in Application and implement them in Infrastructure; when an approved DDD design has Aggregate Roots, those are natural repository boundaries.
- Repository interfaces **must not** expose `IQueryable<T>`, `DbSet<T>`, `DbContext`, EF Core expressions or provider-specific types; LINQ-to-EF query construction stays in Infrastructure. Return materialized entities, collections, projections or explicit result models.
- Application **must not** depend on `IGenericRepository<T>` or another generic CRUD contract. A generic repository or `Repository<TEntity>` base class may exist only as an Infrastructure implementation detail that removes genuine duplication; it is not a replacement for EF Core query capabilities, and use-case-specific queries stay in concrete repositories.

## Unit of Work

- **Default:** `IUnitOfWork` is the commit boundary of an Application use case — repositories stage changes and do not call `SaveChangesAsync` independently; Application Services decide when the operation is ready to commit.
- Repositories participating in one use case **must** share the same scoped Unit of Work and `DbContext`; `IUnitOfWork` **must not** become a repository container or service locator exposing repositories as properties — repositories are injected explicitly.
- **Default:** no explicit transaction APIs until a concrete use case requires control beyond a normal `SaveChangesAsync`.

## EF Core Boundary

- EF Core **must** remain an Infrastructure implementation detail: use it normally inside Infrastructure, and do not leak EF Core concepts into Application. Do not cripple repository implementations merely to preserve a generic abstraction.

## Database Access

- Database access **must** be parameterized; **never** build SQL by concatenating untrusted input. EF Core LINQ parameterizes values; raw SQL, Dapper and ADO.NET use their supported parameterization mechanisms.
- **Default:** filter and project in the database when practical, avoid unnecessary round trips, over-fetching and N+1 patterns, and paginate potentially large result sets.

## Development Seeding

- **Default:** an empty Development database receives a small, deterministic, representative seed dataset covering meaningful states and relationships.
- Seeding **must** be an Infrastructure/bootstrap concern; it may use `AppDbContext` directly and need not go through Application repositories or `IUnitOfWork`.
- Substantial seed construction **must** live in a dedicated internal `DbSeeder` / Infrastructure initialization surface — not in `Program.cs`, `DbContext` configuration, entity configurations or migrations.
- Automatic seeding **must** run only in Development: **never** seed Production automatically. Tests own their setup and **must not** rely on the development seeder.
- The seeder **must not** call `Database.Migrate()`, `EnsureCreated()` or otherwise create or upgrade schema; migrations are applied separately before seeding.
- When representative data already exists, the seeder **must** leave it unchanged; it is not an automatic synchronization, repair, upgrade, overwrite or recreation mechanism for an existing Development database.
- Seed entities **must** preserve current Domain invariants and valid relationships; prefer readable deterministic examples over exhaustive or random combinations.

Workflow: seeder and migration co-change obligations — `development-workflow` § Co-change Obligations.
Technique: `ef-core` knowledge skill.
