# EF-DECISION-GUIDE (10 records)

## CIS-M-U0046 (pass 3) M .claude/skills/ef-core/SKILL.md:420-420  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For primary-key entity lookup, the EF Core decision guide selects FindAsync when its semantics fit.
TRIGGER: primary-key entity lookup requiring the entity where returning an already tracked entity is desirable (186-187) | EXC: Default technique conditional on fit/appropriateness, not blanket mandatory API use. Knowledge surface owns technique only. Existing U0008 independently concerns additional-query-shaping LINQ branch;  | POL: []
CODEX WHY: Table heading supplies possible default force absent from broad EF capability/safety claims; conditional technique status may defeat independent normativity, so preserve uncertainty.
```
 417  |---|---|
 418  | Read-only entity query | `AsNoTracking()` when useful |
 419  | Read model | Database-side projection |
 420> | Primary-key entity lookup | `FindAsync` when its semantics fit |
 421  | Complex entity graph | Explicit `Include` / projection |
 422  | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 423  | Normal query | Ordinary LINQ |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M-80dc960cad [416, 428] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: Do not introduce explicit transaction APIs until a concrete use case needs control beyond SaveChangesAsync.
- V2 FG-M-143eb070c2 [416, 428] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter/project in the database when practical, avoid round trips/over-fetching/N+1, paginate potentially large result sets.
- V2 FG-M-f8687a2ba9 [416, 428] CANONICAL_ONLY/DEFAULT pol=['PST-001'] rel=[]: Maintain a small deterministic representative seed dataset for an empty Development database covering meaningful states and relationships.
- V2 FG-M-f2da52455f [416, 428] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: If representative data exists leave it unchanged; no seeder-driven synchronization/repair/upgrade/overwrite/recreation; developers recreate the local database explicitly.
- V2 FG-M-e46a9b2ab9 [416, 428] CANONICAL_ONLY/MUST pol=['PST-010'] rel=[]: Treat EF Core migrations as source code: review every generated migration before committing it (destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys, delete behavior).
- NAMED primary/M/constraints.jsonl/RULE-M-0426 -> FG-M-ce2b47c048 [CANONICAL_ONLY] Concrete repositories may use the full EF Core API; do not force complex queries through a generic CRUD abstraction.
- NAMED primary/M/constraints.jsonl/EXTRA-M-0125 -> FG-M-4bea98b9d6 [EXTRA_PRODUCT] Do not casually mix ExecuteUpdateAsync/ExecuteDeleteAsync with tracked entities for the same rows; understand their transaction and consistency implications.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0073 -> FG-M-cf9e144959 [CANONICAL_ONLY] Avoid lazy loading by default because it hides database access and causes N+1 queries.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0075 -> FG-M-e2cfa4d43d [CANONICAL_ONLY] Normal LINQ is default; compiled queries only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material, not merely because a query runs frequ

## CIS-M-U0047 (pass 3) M .claude/skills/ef-core/SKILL.md:422-422  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For set-based mass update/delete, the EF Core decision guide selects ExecuteUpdateAsync or ExecuteDeleteAsync when appropriate.
TRIGGER: choosing a technique for set-based mass update/delete where the named operations are appropriate | EXC: Default technique conditional on fit/appropriateness, not blanket mandatory API use. Knowledge surface owns technique only. Existing U0008 independently concerns additional-query-shaping LINQ branch;  | POL: []
CODEX WHY: Table heading supplies possible default force absent from broad EF capability/safety claims; conditional technique status may defeat independent normativity, so preserve uncertainty.
```
 419  | Read model | Database-side projection |
 420  | Primary-key entity lookup | `FindAsync` when its semantics fit |
 421  | Complex entity graph | Explicit `Include` / projection |
 422> | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 423  | Normal query | Ordinary LINQ |
 424  | Measured extremely hot query | Consider a compiled query |
 425  | Multiple commits requiring atomicity | Explicit transaction |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M-80dc960cad [416, 428] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: Do not introduce explicit transaction APIs until a concrete use case needs control beyond SaveChangesAsync.
- V2 FG-M-143eb070c2 [416, 428] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter/project in the database when practical, avoid round trips/over-fetching/N+1, paginate potentially large result sets.
- V2 FG-M-f8687a2ba9 [416, 428] CANONICAL_ONLY/DEFAULT pol=['PST-001'] rel=[]: Maintain a small deterministic representative seed dataset for an empty Development database covering meaningful states and relationships.
- V2 FG-M-f2da52455f [416, 428] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: If representative data exists leave it unchanged; no seeder-driven synchronization/repair/upgrade/overwrite/recreation; developers recreate the local database explicitly.
- V2 FG-M-e46a9b2ab9 [416, 428] CANONICAL_ONLY/MUST pol=['PST-010'] rel=[]: Treat EF Core migrations as source code: review every generated migration before committing it (destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys, delete behavior).
- NAMED primary/M/constraints.jsonl/RULE-M-0426 -> FG-M-ce2b47c048 [CANONICAL_ONLY] Concrete repositories may use the full EF Core API; do not force complex queries through a generic CRUD abstraction.
- NAMED primary/M/constraints.jsonl/EXTRA-M-0125 -> FG-M-4bea98b9d6 [EXTRA_PRODUCT] Do not casually mix ExecuteUpdateAsync/ExecuteDeleteAsync with tracked entities for the same rows; understand their transaction and consistency implications.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0073 -> FG-M-cf9e144959 [CANONICAL_ONLY] Avoid lazy loading by default because it hides database access and causes N+1 queries.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0075 -> FG-M-e2cfa4d43d [CANONICAL_ONLY] Normal LINQ is default; compiled queries only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material, not merely because a query runs frequ

## CIS-M1-U0036 (pass 3) M1 .claude/skills/ef-core/SKILL.md:431-431  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For primary-key entity lookup, prefer FindAsync when its semantics fit.
TRIGGER: Choosing a primary-key lookup requiring an entity and where returning an already tracked entity is desirable | EXC: When semantics fit/when appropriate; nonexclusive technique guidance, not mandatory use. Explicit tracking and transaction cautions still apply. | POL: []
CODEX WHY: Decision-guide default may independently guide selection, but technique-only ownership and descriptive suitability make normativity/equivalence uncertain.
```
 428  | Repository implementation | EF Core inside the adapter layer |
 429  | Read-only entity query | `AsNoTracking()` when useful |
 430  | Read model | Database-side projection |
 431> | Primary-key entity lookup | `FindAsync` when its semantics fit |
 432  | Complex entity graph | Explicit `Include` / projection |
 433  | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 434  | Measured extremely hot query | Consider a compiled query |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M1-15c9830bda [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=[]: Prefer specific repository interfaces representing cohesive use-case persistence needs over table-mirroring generic CRUD contracts; Aggregate Roots of an approved DDD design are natural repository boundaries.
- V2 FG-M1-21f7520922 [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is the default commit boundary; repositories stage and do not commit; Application Services decide when to commit.
- V2 FG-M1-22a15863db [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is implemented in Infrastructure over the scoped persistence session.
- V2 FG-M1-e5881edfc1 [424, 440] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter/project in the database, avoid unnecessary round trips/over-loading, watch N+1, paginate potentially large results.
- V2 FG-M1-6e11403581 [424, 440] CANONICAL_ONLY/MUST pol=['ARC-019', 'ARC-008'] rel=[]: Do not leak EF Core concepts (DbContext/AppDbContext, DbSet<T>, EF APIs, EF-backed IQueryable<T>, query expressions, provider types) into the use-case layer.
- V2 FG-M1-873b923d44 [424, 440] CANONICAL_ONLY/MUST pol=['ARC-019', 'ARC-015'] rel=[]: EF Core is an adapter-layer detail used directly with full capabilities; do not cripple repositories to preserve a generic abstraction.
- V2 FG-M1-39a99df6bc [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-018', 'ARC-016'] rel=[]: One SaveChangesAsync is the normal transaction boundary; no explicit transaction APIs until a concrete use case needs more.
- V2 FG-M1-da5ec8ca30 [424, 440] CANONICAL_ONLY/DEFAULT pol=['PST-001', 'PST-007'] rel=[]: Maintain a small deterministic representative seed dataset for an empty Development database; readable deterministic examples over exhaustive/random combinations.
- V2 FG-M1-9ce20ef00c [424, 440] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: Leave existing representative data unchanged; no seeder-based synchronization/repair/upgrade/overwrite/recreation; developers recreate explicitly.
- V2 FG-M1-ecc5908b85 [424, 440] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state, own setup, and do not depend on development seed data or execution order.
- V2 FG-M1-82c91ef815 [424, 440] CANONICAL_ONLY/DEFAULT pol=['WF-019'] rel=[]: When deployment performs database migrations make the migration step explicit, use the project's approved credentials, run it at a controlled point and fail visibly; no automatic production seeding or startup migrations.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0149 -> FG-M1-d7f60f00c0 [EXTRA_PRODUCT] Do not casually mix ExecuteUpdateAsync/ExecuteDeleteAsync with tracked entities for the same rows; understand transaction/consistency implications.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0098 -> FG-M1-873b923d44 [CANONICAL_ONLY] EF Core is an adapter-layer detail used directly with full capabilities; do not cripple repositories to preserve a generic abstraction.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0099 -> FG-M1-39a99df6bc [CANONICAL_ONLY] One SaveChangesAsync is the normal transaction boundary; no explicit transaction APIs until a concrete use case needs more.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0095 -> FG-M1-77e103cfd2 [EXTRA_PRODUCT] Keep entity configuration separate with IEntityTypeConfiguration<T>.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0097 -> FG-M1-ee7328fafc [NON_NORMATIVE] Paged queries must use a deterministic order, yet the skill's own sample orders only by a possibly non-unique timestamp (reported inconsistency).

## CIS-M1-U0037 (pass 3) M1 .claude/skills/ef-core/SKILL.md:433-433  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For set-based mass updates or deletes, prefer ExecuteUpdateAsync or ExecuteDeleteAsync when appropriate.
TRIGGER: Choosing an EF mechanism for a set-based mass update/delete | EXC: When semantics fit/when appropriate; nonexclusive technique guidance, not mandatory use. Explicit tracking and transaction cautions still apply. | POL: []
CODEX WHY: Decision-guide default may independently guide selection, but technique-only ownership and descriptive suitability make normativity/equivalence uncertain.
```
 430  | Read model | Database-side projection |
 431  | Primary-key entity lookup | `FindAsync` when its semantics fit |
 432  | Complex entity graph | Explicit `Include` / projection |
 433> | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 434  | Measured extremely hot query | Consider a compiled query |
 435  | Multiple commits requiring atomicity | Explicit transaction |
 436  | Production schema change | Reviewed migration / controlled deployment |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M1-15c9830bda [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=[]: Prefer specific repository interfaces representing cohesive use-case persistence needs over table-mirroring generic CRUD contracts; Aggregate Roots of an approved DDD design are natural repository boundaries.
- V2 FG-M1-21f7520922 [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is the default commit boundary; repositories stage and do not commit; Application Services decide when to commit.
- V2 FG-M1-22a15863db [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is implemented in Infrastructure over the scoped persistence session.
- V2 FG-M1-e5881edfc1 [424, 440] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter/project in the database, avoid unnecessary round trips/over-loading, watch N+1, paginate potentially large results.
- V2 FG-M1-6e11403581 [424, 440] CANONICAL_ONLY/MUST pol=['ARC-019', 'ARC-008'] rel=[]: Do not leak EF Core concepts (DbContext/AppDbContext, DbSet<T>, EF APIs, EF-backed IQueryable<T>, query expressions, provider types) into the use-case layer.
- V2 FG-M1-873b923d44 [424, 440] CANONICAL_ONLY/MUST pol=['ARC-019', 'ARC-015'] rel=[]: EF Core is an adapter-layer detail used directly with full capabilities; do not cripple repositories to preserve a generic abstraction.
- V2 FG-M1-39a99df6bc [424, 440] CANONICAL_ONLY/DEFAULT pol=['ARC-018', 'ARC-016'] rel=[]: One SaveChangesAsync is the normal transaction boundary; no explicit transaction APIs until a concrete use case needs more.
- V2 FG-M1-da5ec8ca30 [424, 440] CANONICAL_ONLY/DEFAULT pol=['PST-001', 'PST-007'] rel=[]: Maintain a small deterministic representative seed dataset for an empty Development database; readable deterministic examples over exhaustive/random combinations.
- V2 FG-M1-9ce20ef00c [424, 440] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: Leave existing representative data unchanged; no seeder-based synchronization/repair/upgrade/overwrite/recreation; developers recreate explicitly.
- V2 FG-M1-ecc5908b85 [424, 440] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state, own setup, and do not depend on development seed data or execution order.
- V2 FG-M1-82c91ef815 [424, 440] CANONICAL_ONLY/DEFAULT pol=['WF-019'] rel=[]: When deployment performs database migrations make the migration step explicit, use the project's approved credentials, run it at a controlled point and fail visibly; no automatic production seeding or startup migrations.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0149 -> FG-M1-d7f60f00c0 [EXTRA_PRODUCT] Do not casually mix ExecuteUpdateAsync/ExecuteDeleteAsync with tracked entities for the same rows; understand transaction/consistency implications.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0098 -> FG-M1-873b923d44 [CANONICAL_ONLY] EF Core is an adapter-layer detail used directly with full capabilities; do not cripple repositories to preserve a generic abstraction.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0099 -> FG-M1-39a99df6bc [CANONICAL_ONLY] One SaveChangesAsync is the normal transaction boundary; no explicit transaction APIs until a concrete use case needs more.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0095 -> FG-M1-77e103cfd2 [EXTRA_PRODUCT] Keep entity configuration separate with IEntityTypeConfiguration<T>.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0097 -> FG-M1-ee7328fafc [NON_NORMATIVE] Paged queries must use a deterministic order, yet the skill's own sample orders only by a possibly non-unique timestamp (reported inconsistency).

## CIS-L1-U0025 (pass 3) L1 .claude/skills/ef-core/SKILL.md:161-161  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a primary-key entity lookup, use FindAsync by default when its semantics fit.
TRIGGER: Applicable decision-guide scenario under on-demand skill | EXC: Only when semantics fit/when appropriate; not compulsory for all queries or mutations. | POL: []
CODEX WHY: Independently falsifiable positive default absent from nearby baseline cautions. Existing U0012 concerns LINQ predicates/projection/related-data branch, not key-lookup default.
```
 158  | Commit | `IUnitOfWork.SaveChangesAsync` |
 159  | Read-only entity query | `AsNoTracking()` when useful |
 160  | Read model | database-side projection |
 161> | Primary-key entity lookup | `FindAsync` when its semantics fit |
 162  | Complex graph | explicit `Include` or projection |
 163  | Set-based update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 164  | Measured extremely hot query | consider a compiled query |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-L1-e85072de36 [155, 169] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative Development data already exists it is left unchanged: migrating an existing Development database does not require the seeder to patch rows, and developers recreate the local database explicitly when they need a
- V2 FG-L1-5996f6c2c9 [155, 169] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Never point database update/drop commands at Production; production migration is a deployment step.
- V2 FG-L1-d8b80ec5b2 [155, 169] CANONICAL_ONLY/MUST pol=['PST-010'] rel=[]: Review every generated migration before committing (destructive changes, column recreation, data migrations, indexes, FKs, delete behaviour).
- V2 FG-L1-3738f1d139 [155, 169] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, allocation-reducing return types, pooling, custom serialization, aggressive caching or raw SQL for performance only for a measured or demonstrated need.
- V2 FG-L1-d7441df401 [155, 169] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter/project in the database, avoid round trips, over-fetching and N+1, paginate large result sets.
- V2 FG-L1-2652efc4ba [155, 169] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state and own their setup; never depend on development seed data or test order.
- V2 FG-L1-6c4b0a3757 [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=['ARC-007']: Prefer specific cohesive repository interfaces over table-mirroring generic CRUD; interfaces in Application, implementations in Infrastructure.
- V2 FG-L1-89d11db995 [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork (in Application) is the normal commit boundary; repositories stage, Application Services commit.
- V2 FG-L1-93b26f4ec8 [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: The IUnitOfWork implementation delegates to AppDbContext.SaveChangesAsync and staged changes are the shared context's tracked changes.
- V2 FG-L1-3a3269e45b [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: No explicit transaction APIs until a use case needs more than a single commit.
- V2 FG-L1-42f404a88e [155, 169] CANONICAL_ONLY/DEFAULT pol=['PST-001', 'PST-007'] rel=[]: For an empty Development database maintain a small deterministic representative dataset (new, active, completed, archived; with/without optional values and relationships; boundary states); no every-combination or random bulk data.
- V2 FG-L1-93a72dc5e5 [155, 169] CANONICAL_ONLY/MUST_NOT pol=['PST-004', 'TST-008'] rel=[]: Automatic seeding only in Development; never Production; tests never use the seeder.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0135 -> FG-L1-8c82eb1d4f [EXTRA_PRODUCT] ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand their transaction semantics.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0114 -> FG-L1-690fbe0db4 [CANONICAL_ONLY] Start with clear LINQ; before optimizing inspect round trips, columns, N+1, indexes, SQL, plans, materialized volume and tracking.

## CIS-L1-U0026 (pass 3) L1 .claude/skills/ef-core/SKILL.md:163-163  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a set-based update/delete, use ExecuteUpdateAsync or ExecuteDeleteAsync by default when appropriate.
TRIGGER: Applicable decision-guide scenario under on-demand skill | EXC: Only when semantics fit/when appropriate; not compulsory for all queries or mutations. | POL: []
CODEX WHY: Independently falsifiable positive default absent from nearby baseline cautions. Existing U0012 concerns LINQ predicates/projection/related-data branch, not key-lookup default.
```
 160  | Read model | database-side projection |
 161  | Primary-key entity lookup | `FindAsync` when its semantics fit |
 162  | Complex graph | explicit `Include` or projection |
 163> | Set-based update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 164  | Measured extremely hot query | consider a compiled query |
 165  | Several commits that must be atomic | explicit transaction |
 166  | Production schema change | reviewed migration, controlled deployment |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-L1-e85072de36 [155, 169] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative Development data already exists it is left unchanged: migrating an existing Development database does not require the seeder to patch rows, and developers recreate the local database explicitly when they need a
- V2 FG-L1-5996f6c2c9 [155, 169] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Never point database update/drop commands at Production; production migration is a deployment step.
- V2 FG-L1-d8b80ec5b2 [155, 169] CANONICAL_ONLY/MUST pol=['PST-010'] rel=[]: Review every generated migration before committing (destructive changes, column recreation, data migrations, indexes, FKs, delete behaviour).
- V2 FG-L1-3738f1d139 [155, 169] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, allocation-reducing return types, pooling, custom serialization, aggressive caching or raw SQL for performance only for a measured or demonstrated need.
- V2 FG-L1-d7441df401 [155, 169] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter/project in the database, avoid round trips, over-fetching and N+1, paginate large result sets.
- V2 FG-L1-2652efc4ba [155, 169] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state and own their setup; never depend on development seed data or test order.
- V2 FG-L1-6c4b0a3757 [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=['ARC-007']: Prefer specific cohesive repository interfaces over table-mirroring generic CRUD; interfaces in Application, implementations in Infrastructure.
- V2 FG-L1-89d11db995 [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork (in Application) is the normal commit boundary; repositories stage, Application Services commit.
- V2 FG-L1-93b26f4ec8 [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: The IUnitOfWork implementation delegates to AppDbContext.SaveChangesAsync and staged changes are the shared context's tracked changes.
- V2 FG-L1-3a3269e45b [155, 169] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: No explicit transaction APIs until a use case needs more than a single commit.
- V2 FG-L1-42f404a88e [155, 169] CANONICAL_ONLY/DEFAULT pol=['PST-001', 'PST-007'] rel=[]: For an empty Development database maintain a small deterministic representative dataset (new, active, completed, archived; with/without optional values and relationships; boundary states); no every-combination or random bulk data.
- V2 FG-L1-93a72dc5e5 [155, 169] CANONICAL_ONLY/MUST_NOT pol=['PST-004', 'TST-008'] rel=[]: Automatic seeding only in Development; never Production; tests never use the seeder.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0135 -> FG-L1-8c82eb1d4f [EXTRA_PRODUCT] ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand their transaction semantics.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0114 -> FG-L1-690fbe0db4 [CANONICAL_ONLY] Start with clear LINQ; before optimizing inspect round trips, columns, N+1, indexes, SQL, plans, materialized volume and tracking.

## CIS-K0-U0038 (pass 3) K0 .claude/skills/ef-core/SKILL.md:356-356  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The EF Core decision guide recommends FindAsync when its semantics fit for a primary-key entity lookup; possible independent selection guidance.
TRIGGER: Implementing a primary-key entity lookup under the EF Core skill | EXC: Only when semantics fit / when appropriate; no exclusive method mandate. | POL: []
CODEX WHY: An instruction may guide implementation choice without a different product outcome; table modality and entailment by general EF guidance remain uncertain.
```
 353  |---|---|
 354  | Read-only entity query | `AsNoTracking()` when useful |
 355  | Read model | Database-side projection |
 356> | Primary-key entity lookup | `FindAsync` when its semantics fit |
 357  | Complex entity graph | Explicit `Include` / projection |
 358  | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 359  | Normal query | Ordinary LINQ |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K0-f4e23fe60f [354, 365] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state, own their setup and never depend on development seeding or execution order.
- V2 FG-K0-f4e23fe60f [352, 365] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state, own their setup and never depend on development seeding or execution order.
- V2 FG-K0-0ed7381eeb [352, 365] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: No explicit transaction APIs until a concrete use case needs control beyond SaveChangesAsync.
- V2 FG-K0-9078fc279e [352, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, ValueTask<T>, ArrayPool/MemoryPool and manual pooling, custom serialization, aggressive caching and raw SQL for performance only for a measured or clearly demonstrated need.
- V2 FG-K0-9046d6f731 [352, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter and project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results.
- V2 FG-K0-8bd3972a30 [354, 365] CANONICAL_ONLY/DEFAULT pol=['PST-001'] rel=[]: An empty Development database receives a small deterministic representative seed dataset covering meaningful states and relationships.
- V2 FG-K0-8bd3972a30 [352, 365] CANONICAL_ONLY/DEFAULT pol=['PST-001'] rel=[]: An empty Development database receives a small deterministic representative seed dataset covering meaningful states and relationships.
- V2 FG-K0-08059989ef [354, 365] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K0-08059989ef [352, 365] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K0-001a571f72 [354, 365] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Do not apply production migrations automatically from normal application startup by default; a production migration is an explicit deployment step at a controlled point with approved credentials; scripts/bundles may be generated e
- V2 FG-K0-001a571f72 [352, 365] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Do not apply production migrations automatically from normal application startup by default; a production migration is an explicit deployment step at a controlled point with approved credentials; scripts/bundles may be generated e
- V2 FG-K0-fe2f331388 [352, 365] CANONICAL_ONLY/MUST pol=['WF-019'] rel=[]: The production migration step fails visibly.
- V2 FG-K0-8bba5b9da3 [352, 365] CANONICAL_ONLY/MUST_NOT pol=['PST-004', 'WF-019'] rel=[]: Development seeding never runs in Production.
- V2 FG-K0-3800bc6808 [354, 365] CANONICAL_ONLY/MUST pol=['PST-010'] rel=[]: Treat EF Core migrations as source code and review every generated migration before committing (destructive changes, column recreation, data migrations, indexes, foreign keys, delete behaviour).
- V2 FG-K0-a402cbbf97 [354, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Project in the database for read-only queries needing selected data; projection is not mandatory when the use case needs the entity, but avoid loading a whole aggregate for a few fields.
- V2 FG-K0-f9aeaa440b [354, 365] EXTRA_PRODUCT/DEFAULT pol=[] rel=['RUN-006']: Use tracking queries when loaded entities will be modified and committed through the current Unit of Work and AsNoTracking() for read-only entity queries where tracking adds nothing; projections need no AsNoTracking().
- V2 FG-K0-09d2e24e6d [354, 365] CANONICAL_ONLY/SHOULD_NOT pol=['RUN-006'] rel=[]: Avoid lazy loading by default; it hides database access and invites N+1 queries.
- V2 FG-K0-b37e120890 [354, 365] EXTRA_PRODUCT/MUST_NOT pol=[] rel=['ARC-016', 'ARC-019']: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows and understand their transaction and consistency implications.
- V2 FG-K0-20afde86e9 [354, 365] CANONICAL_ONLY/DEFAULT pol=['ARC-018', 'ARC-016'] rel=[]: One SaveChangesAsync is the transaction boundary of an operation; an explicit transaction fits a concrete case where several operations or SaveChangesAsync calls succeed or fail together; EF transactions do not solve distributed t
- V2 FG-K0-4622d88e39 [354, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Normal LINQ is the default; compiled queries belong where compilation or cache-lookup overhead is measured, or clearly demonstrated, to matter, not to queries that merely run often; not speculatively.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0147 -> FG-K0-b37e120890 [EXTRA_PRODUCT] ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows and understand their transaction and consistency impl
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0026 -> FG-K0-8babc55112 [EXTRA_PRODUCT] Keep entity configuration in IEntityTypeConfiguration<T> classes.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0028 -> FG-K0-87b93f63f7 [EXTRA_PRODUCT] EF Core interceptors fit infrastructure-level cross-cutting behaviour with a clear benefit (e.g. auditing); business behaviour does not belong in them.

## CIS-K0-U0039 (pass 3) K0 .claude/skills/ef-core/SKILL.md:358-358  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The EF Core decision guide recommends ExecuteUpdateAsync or ExecuteDeleteAsync when appropriate for a set-based mass update or delete; possible independent selection guidance.
TRIGGER: Implementing a set-based mass update or delete under the EF Core skill | EXC: Only when semantics fit / when appropriate; no exclusive method mandate. | POL: []
CODEX WHY: An instruction may guide implementation choice without a different product outcome; table modality and entailment by general EF guidance remain uncertain.
```
 355  | Read model | Database-side projection |
 356  | Primary-key entity lookup | `FindAsync` when its semantics fit |
 357  | Complex entity graph | Explicit `Include` / projection |
 358> | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 359  | Normal query | Ordinary LINQ |
 360  | Measured extremely hot query | Consider a compiled query |
 361  | Several commits that succeed or fail together | Explicit transaction |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K0-f4e23fe60f [354, 365] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state, own their setup and never depend on development seeding or execution order.
- V2 FG-K0-f4e23fe60f [352, 365] CANONICAL_ONLY/MUST pol=['TST-008'] rel=[]: Tests start from a known state, own their setup and never depend on development seeding or execution order.
- V2 FG-K0-0ed7381eeb [352, 365] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: No explicit transaction APIs until a concrete use case needs control beyond SaveChangesAsync.
- V2 FG-K0-9078fc279e [352, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, ValueTask<T>, ArrayPool/MemoryPool and manual pooling, custom serialization, aggressive caching and raw SQL for performance only for a measured or clearly demonstrated need.
- V2 FG-K0-9046d6f731 [352, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter and project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results.
- V2 FG-K0-8bd3972a30 [354, 365] CANONICAL_ONLY/DEFAULT pol=['PST-001'] rel=[]: An empty Development database receives a small deterministic representative seed dataset covering meaningful states and relationships.
- V2 FG-K0-8bd3972a30 [352, 365] CANONICAL_ONLY/DEFAULT pol=['PST-001'] rel=[]: An empty Development database receives a small deterministic representative seed dataset covering meaningful states and relationships.
- V2 FG-K0-08059989ef [354, 365] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K0-08059989ef [352, 365] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K0-001a571f72 [354, 365] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Do not apply production migrations automatically from normal application startup by default; a production migration is an explicit deployment step at a controlled point with approved credentials; scripts/bundles may be generated e
- V2 FG-K0-001a571f72 [352, 365] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Do not apply production migrations automatically from normal application startup by default; a production migration is an explicit deployment step at a controlled point with approved credentials; scripts/bundles may be generated e
- V2 FG-K0-fe2f331388 [352, 365] CANONICAL_ONLY/MUST pol=['WF-019'] rel=[]: The production migration step fails visibly.
- V2 FG-K0-8bba5b9da3 [352, 365] CANONICAL_ONLY/MUST_NOT pol=['PST-004', 'WF-019'] rel=[]: Development seeding never runs in Production.
- V2 FG-K0-3800bc6808 [354, 365] CANONICAL_ONLY/MUST pol=['PST-010'] rel=[]: Treat EF Core migrations as source code and review every generated migration before committing (destructive changes, column recreation, data migrations, indexes, foreign keys, delete behaviour).
- V2 FG-K0-a402cbbf97 [354, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Project in the database for read-only queries needing selected data; projection is not mandatory when the use case needs the entity, but avoid loading a whole aggregate for a few fields.
- V2 FG-K0-f9aeaa440b [354, 365] EXTRA_PRODUCT/DEFAULT pol=[] rel=['RUN-006']: Use tracking queries when loaded entities will be modified and committed through the current Unit of Work and AsNoTracking() for read-only entity queries where tracking adds nothing; projections need no AsNoTracking().
- V2 FG-K0-09d2e24e6d [354, 365] CANONICAL_ONLY/SHOULD_NOT pol=['RUN-006'] rel=[]: Avoid lazy loading by default; it hides database access and invites N+1 queries.
- V2 FG-K0-b37e120890 [354, 365] EXTRA_PRODUCT/MUST_NOT pol=[] rel=['ARC-016', 'ARC-019']: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows and understand their transaction and consistency implications.
- V2 FG-K0-20afde86e9 [354, 365] CANONICAL_ONLY/DEFAULT pol=['ARC-018', 'ARC-016'] rel=[]: One SaveChangesAsync is the transaction boundary of an operation; an explicit transaction fits a concrete case where several operations or SaveChangesAsync calls succeed or fail together; EF transactions do not solve distributed t
- V2 FG-K0-4622d88e39 [354, 365] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Normal LINQ is the default; compiled queries belong where compilation or cache-lookup overhead is measured, or clearly demonstrated, to matter, not to queries that merely run often; not speculatively.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0147 -> FG-K0-b37e120890 [EXTRA_PRODUCT] ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows and understand their transaction and consistency impl
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0026 -> FG-K0-8babc55112 [EXTRA_PRODUCT] Keep entity configuration in IEntityTypeConfiguration<T> classes.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0028 -> FG-K0-87b93f63f7 [EXTRA_PRODUCT] EF Core interceptors fit infrastructure-level cross-cutting behaviour with a clear benefit (e.g. auditing); business behaviour does not belong in them.

## CIS-K1-U0022 (pass 3) K1 .claude/skills/ef-core/SKILL.md:238-238  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For primary-key entity lookup, the EF decision guide recommends FindAsync as the default technique when its semantics fit.
TRIGGER: Selecting EF Core technique for the named query or mutation scenario | EXC: When semantics fit/when appropriate; FindAsync entity and already-tracked behavior qualified at107; bulk consistency cautions at119 apply. No mandatory universal API use inferred. | POL: []
CODEX WHY: Recommendation may constrain choice independently of safe-use caveats, but could be merely illustrative technique summary. Preserve uncertainty.
```
 235  | Commit application changes | `IUnitOfWork.SaveChangesAsync` |
 236  | Read-only entity query | `AsNoTracking()` when useful |
 237  | Read model | Database-side projection |
 238> | Primary-key entity lookup | `FindAsync` when its semantics fit |
 239  | Complex entity graph | Explicit `Include` / projection |
 240  | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 241  | Measured extremely hot query | Consider a compiled query |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K1-bc691cb4b4 [234, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is the use-case commit boundary; repositories stage changes and Application Services decide when to commit.
- V2 FG-K1-bc691cb4b4 [232, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is the use-case commit boundary; repositories stage changes and Application Services decide when to commit.
- V2 FG-K1-e59b8b53bf [232, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: No explicit transaction APIs until a concrete use case needs control beyond a single SaveChangesAsync.
- V2 FG-K1-063940565c [234, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=['ARC-007']: Specific repository interfaces for cohesive Application persistence needs, defined in Application and implemented in Infrastructure, not table-mirroring generic CRUD.
- V2 FG-K1-063940565c [232, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=['ARC-007']: Specific repository interfaces for cohesive Application persistence needs, defined in Application and implemented in Infrastructure, not table-mirroring generic CRUD.
- V2 FG-K1-8e4adfba7a [234, 244] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never use the seeder to synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K1-8e4adfba7a [232, 244] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never use the seeder to synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K1-493b0ae5c9 [232, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL for performance only for a measured or clearly demonstrated need.
- V2 FG-K1-3dc413b20e [232, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter and project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results.
- V2 FG-K1-c7083cf7b9 [232, 244] CANONICAL_ONLY/DEFAULT pol=['WF-019', 'WF-017'] rel=['PST-004']: The deployment migration step fails visibly on error.
- V2 FG-K1-23e78316b6 [232, 244] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Production migrations must not run automatically from normal startup by default; they are an explicit deployment step at a controlled point with approved credentials.
- V2 FG-K1-76d9731ca9 [232, 244] CANONICAL_ONLY/MUST_NOT pol=['PST-004', 'WF-019'] rel=[]: Development seeding never runs in Production.
- V2 FG-K1-f695c03d8f [234, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Project in the database for read-only queries needing selected data; projection not mandatory when the entity is needed; avoid loading a complete aggregate for a few fields.
- V2 FG-K1-d5b0cad1de [234, 244] EXTRA_PRODUCT/DEFAULT pol=[] rel=['RUN-006']: Tracking queries when entities will be modified and committed through the Unit of Work; AsNoTracking() for read-only entity queries; no mechanical AsNoTracking() on DTO projections.
- V2 FG-K1-e7367e0055 [234, 244] EXTRA_PRODUCT/MUST_NOT pol=[] rel=['ARC-016', 'ARC-019']: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand transaction and consistency implications.
- V2 FG-K1-b07a85cbaf [234, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-018', 'ARC-016'] rel=[]: One SaveChangesAsync is normally the transaction boundary; explicit transactions only when several operations or SaveChangesAsync calls must succeed atomically; EF transactions do not solve distributed transactions.
- V2 FG-K1-8c2a0fe6ef [234, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; never speculatively.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0388 -> FG-K1-270fbe87cc [CANONICAL_ONLY] An Infrastructure-only base class may remove genuine duplication without becoming a generic CRUD contract; concrete repositories keep the full EF Core API.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0152 -> FG-K1-e7367e0055 [EXTRA_PRODUCT] ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand transaction and consistency implications.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0082 -> FG-K1-3dc413b20e [CANONICAL_ONLY] Filter and project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0081 -> FG-K1-887f01e3e5 [EXTRA_PRODUCT] Never fire-and-forget EF Core asynchronous operations; a DbContext is not thread-safe.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0082 -> FG-K1-b19d37ab35 [EXTRA_PRODUCT] EF Core interceptors only for infrastructure-level cross-cutting behaviour with a clear benefit (e.g. auditing); never hide business behaviour in them.

## CIS-K1-U0023 (pass 3) K1 .claude/skills/ef-core/SKILL.md:240-240  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For set-based mass update/delete, the EF decision guide recommends ExecuteUpdateAsync or ExecuteDeleteAsync when appropriate.
TRIGGER: Selecting EF Core technique for the named query or mutation scenario | EXC: When semantics fit/when appropriate; FindAsync entity and already-tracked behavior qualified at107; bulk consistency cautions at119 apply. No mandatory universal API use inferred. | POL: []
CODEX WHY: Recommendation may constrain choice independently of safe-use caveats, but could be merely illustrative technique summary. Preserve uncertainty.
```
 237  | Read model | Database-side projection |
 238  | Primary-key entity lookup | `FindAsync` when its semantics fit |
 239  | Complex entity graph | Explicit `Include` / projection |
 240> | Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
 241  | Measured extremely hot query | Consider a compiled query |
 242  | Multiple commits requiring atomicity | Explicit transaction (inside the execution strategy) |
 243  | Production schema change | Reviewed migration, scripted deployment |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K1-bc691cb4b4 [234, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is the use-case commit boundary; repositories stage changes and Application Services decide when to commit.
- V2 FG-K1-bc691cb4b4 [232, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-016'] rel=[]: IUnitOfWork is the use-case commit boundary; repositories stage changes and Application Services decide when to commit.
- V2 FG-K1-e59b8b53bf [232, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-018'] rel=[]: No explicit transaction APIs until a concrete use case needs control beyond a single SaveChangesAsync.
- V2 FG-K1-063940565c [234, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=['ARC-007']: Specific repository interfaces for cohesive Application persistence needs, defined in Application and implemented in Infrastructure, not table-mirroring generic CRUD.
- V2 FG-K1-063940565c [232, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-013'] rel=['ARC-007']: Specific repository interfaces for cohesive Application persistence needs, defined in Application and implemented in Infrastructure, not table-mirroring generic CRUD.
- V2 FG-K1-8e4adfba7a [234, 244] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never use the seeder to synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K1-8e4adfba7a [232, 244] CANONICAL_ONLY/MUST_NOT pol=['PST-006'] rel=[]: When representative data exists leave it unchanged; never use the seeder to synchronize, repair, upgrade, overwrite or recreate an existing Development database; developers recreate explicitly.
- V2 FG-K1-493b0ae5c9 [232, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL for performance only for a measured or clearly demonstrated need.
- V2 FG-K1-3dc413b20e [232, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Filter and project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results.
- V2 FG-K1-c7083cf7b9 [232, 244] CANONICAL_ONLY/DEFAULT pol=['WF-019', 'WF-017'] rel=['PST-004']: The deployment migration step fails visibly on error.
- V2 FG-K1-23e78316b6 [232, 244] CANONICAL_ONLY/MUST_NOT pol=['WF-019'] rel=[]: Production migrations must not run automatically from normal startup by default; they are an explicit deployment step at a controlled point with approved credentials.
- V2 FG-K1-76d9731ca9 [232, 244] CANONICAL_ONLY/MUST_NOT pol=['PST-004', 'WF-019'] rel=[]: Development seeding never runs in Production.
- V2 FG-K1-f695c03d8f [234, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-006'] rel=[]: Project in the database for read-only queries needing selected data; projection not mandatory when the entity is needed; avoid loading a complete aggregate for a few fields.
- V2 FG-K1-d5b0cad1de [234, 244] EXTRA_PRODUCT/DEFAULT pol=[] rel=['RUN-006']: Tracking queries when entities will be modified and committed through the Unit of Work; AsNoTracking() for read-only entity queries; no mechanical AsNoTracking() on DTO projections.
- V2 FG-K1-e7367e0055 [234, 244] EXTRA_PRODUCT/MUST_NOT pol=[] rel=['ARC-016', 'ARC-019']: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand transaction and consistency implications.
- V2 FG-K1-b07a85cbaf [234, 244] CANONICAL_ONLY/DEFAULT pol=['ARC-018', 'ARC-016'] rel=[]: One SaveChangesAsync is normally the transaction boundary; explicit transactions only when several operations or SaveChangesAsync calls must succeed atomically; EF transactions do not solve distributed transactions.
- V2 FG-K1-8c2a0fe6ef [234, 244] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; never speculatively.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0388 -> FG-K1-270fbe87cc [CANONICAL_ONLY] An Infrastructure-only base class may remove genuine duplication without becoming a generic CRUD contract; concrete repositories keep the full EF Core API.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0152 -> FG-K1-e7367e0055 [EXTRA_PRODUCT] ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand transaction and consistency implications.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0082 -> FG-K1-3dc413b20e [CANONICAL_ONLY] Filter and project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0081 -> FG-K1-887f01e3e5 [EXTRA_PRODUCT] Never fire-and-forget EF Core asynchronous operations; a DbContext is not thread-safe.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0082 -> FG-K1-b19d37ab35 [EXTRA_PRODUCT] EF Core interceptors only for infrastructure-level cross-cutting behaviour with a clear benefit (e.g. auditing); never hide business behaviour in them.
