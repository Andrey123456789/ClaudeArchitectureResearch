# SINGLE-CIS-K0-U0017 (1 records)

## CIS-K0-U0017 (pass 2) K0 .claude/rules/backend/architecture.md:44-44  [MUST UNCERTAIN_NOVELTY]
CLAIM: Use-case-specific queries stay in concrete repositories when an Infrastructure-only generic repository or base class is used.
TRIGGER: Implementing use-case-specific persistence queries in the path-scoped backend architecture, including use of an Infrastructure-only generic repository/base. | EXC: Generic Infrastructure helpers may remove real duplication; whether delegation to such helpers still counts as queries staying in concrete repositories is unresolved. | POL: ['ARC-015', 'ARC-019']
CODEX WHY: All-three action review of repository/interface/implementation/query records and exact-location coverage/policy records found no separately expressed concrete-repository query-placement clause. Potential independent restriction is source-grounded; whether it adds a meaningful restriction beyond concrete repository ownership while allowing internal helpers remains uncertain.
```
  41  
  42  - Default: specific repository interfaces that represent actual, cohesive Application persistence needs rather than table-mirroring generic CRUD contracts. Define them in Application and implement them in Infrastru
  43  - Repository interfaces must not expose `IQueryable<T>`, `DbSet<T>`, `DbContext`, EF Core expressions or provider-specific types; LINQ-to-EF query construction stays in Infrastructure. Return materialized entities,
  44> - Application must not depend on `IGenericRepository<T>` or another generic CRUD contract. A generic repository or `Repository<TEntity>` base class may exist only as an Infrastructure implementation detail that rem
  45  
  46  ## Unit of Work
  47  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-2f3f94690d [44, 44] CANONICAL_ONLY/MUST_NOT pol=['ARC-015'] rel=[]: Application does not depend on IGenericRepository<T> or another generic CRUD contract; a generic repository/base class may exist only as an Infrastructure detail removing real duplication, not replacing EF Core query capabilities.
- V2 FG-K0-8c3083d5eb [44, 44] CANONICAL_ONLY/MUST_NOT pol=['ARC-015'] rel=[]: Application must not depend on IGenericRepository<T> or another generic CRUD contract; a generic base may exist only in Infrastructure to remove real duplication.
- V2 FG-K0-ad2dbad5c4 [44, 44] CANONICAL_ONLY/MUST_NOT pol=['ARC-015'] rel=['ARC-017']: Application must not depend on IGenericRepository<T> or another generic CRUD contract.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0092 -> FG-K0-8c3083d5eb [CANONICAL_ONLY] Application must not depend on IGenericRepository<T> or another generic CRUD contract; a generic base may exist only in Infrastructure to remove real duplication.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0382 -> FG-K0-648f45fa01 [CANONICAL_ONLY] An Infrastructure-only base class may remove genuine duplication while concrete repositories keep the full EF Core API.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0096 -> FG-K0-c3538d9112 [CANONICAL_ONLY] EF Core is used fully inside Infrastructure and never leaks into Application; do not cripple repository implementations to preserve a generic abstraction.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0040 -> FG-K0-2f3f94690d [CANONICAL_ONLY] Application does not depend on IGenericRepository<T> or another generic CRUD contract; a generic repository/base class may exist only as an Infrastructure detail removing real dupl
- NAMED replica/K0/constraints.jsonl/RULE-K0-0038 -> FG-K0-7ebf687020 [CANONICAL_ONLY] Specific repository interfaces for cohesive Application persistence needs (defined in Application, implemented in Infrastructure), not table-mirroring generic CRUD.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0039 -> FG-K0-c3ac99aefa [CANONICAL_ONLY] Repository interfaces do not expose IQueryable<T>, DbSet<T>, DbContext, EF Core expressions or provider types; LINQ-to-EF stays in Infrastructure; return materialized entities, col
- NAMED replica/K0/constraints.jsonl/RULE-K0-0044 -> FG-K0-c3538d9112 [CANONICAL_ONLY] EF Core is used fully inside Infrastructure and never leaks into Application; do not cripple repository implementations to preserve a generic abstraction.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0087 -> FG-K0-19be5e768e [CANONICAL_ONLY] Repositories are injected explicitly into their consumers.
