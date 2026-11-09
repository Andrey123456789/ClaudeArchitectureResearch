from jdsl import C, D, P  # noqa: F401

P("ARC-009",
  dims=["D1 CQRS handlers, MediatR, Kommand, Vertical Slice Architecture or similar mediator-based organization only with explicit approval",
        "D2 mechanical flag when a mediator package is added"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same approval rule, always loaded, in all six: M root CLAUDE.md:91-93, M1 docs/capabilities/architecture.md:41-44 (imported), L0 rules/1-architecture/overview.md:34 (imported), L1 frame/adopted-style.md:24 (imported), K0 decision-register.md:12 (D-02, imported), K1 decision-register.md:14 (imported). All six also list mediator-based organization as Reserved in root CLAUDE.md.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "L0", "L1"], ["M", "K0"], ["K1"]],
           "Package flags: M1 check-manifests.js:45/:85 (reservedPackages MediatR, Kommand from clean-architecture/MODULE.md:34), L0 manifest-checks.mjs:33-34 (mediatr, kommand), L1 post-change-checks.mjs:152 with check.json:26-29 (MediatR, Kommand prefixes); M check-manifests.mjs:40 and K0 check-dependencies.cjs:27 flag MediatR only; K1 has no package flag for mediator libraries (searched check-manifests.cjs and facets). No candidate detects handler trees or vertical slices written without a library.",
           counterexample="Same task: the agent adds <PackageReference Include=\"MediatR\"/> to Application. M, M1, L0, L1 and K0 flag it; K1 does not. With Kommand instead, only M1, L0 and L1 flag it. Severity of each flag and its live-host effect not compared (not executed).",
           root="RC-ENF-MEDIATOR-PKG", evidence={"M": ["FG-M-63c663ab26"], "M1": ["FG-M1-11f66bb3cc"], "L0": ["FG-L0-9d944971ca"], "L1": ["FG-L1-0bb5bc38a8"], "K0": ["FG-K0-32614fa846"], "K1": ["FG-K1-209201ca40"]})],
  enforcement="Source-read checker code; not executed on a shared fixture.")

P("ARC-010",
  dims=["D1 ASP.NET Core Controllers are the default HTTP entry point and stay thin: bind/validate input, invoke Application services, translate outcomes"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each backend rule: M architecture.md:82-85 (adopted style also in root CLAUDE.md:80-84), M1 :63-65, L0 rules/1-architecture/entry-points.md:15, L1 frame/boundaries.md:30, K0 rules/backend/architecture.md:35 (D-01), K1 rules/backend/architecture.md:14. Skill 'avoid' lists (Minimal API filters, versioning examples) are anti-pattern catalogues in all six.")

P("ARC-011",
  dims=["D1 Controllers contain no business logic, do not access DbContext or concrete repositories, do not construct infrastructure services"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M architecture.md:86-87, M1 :67-68, L0 entry-points.md:16, L1 boundaries.md:31, K0 architecture.md:36, K1 rules/backend/architecture.md:15.")

P("ARC-012",
  dims=["D1 Program.cs is the composition root and may register Infrastructure implementations (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M architecture.md:88-90, M1 :70-72, L0 backend-layers.md:45, L1 boundaries.md:32 (with AddApplication/AddInfrastructure in the capability layout:75), K0 architecture.md:37, K1 architecture-style.md:45. M, M1 and K0 add that Controllers do not consume Infrastructure implementation types, which ARC-011 already requires in all six.")

P("ARC-013",
  dims=["D1 prefer specific repository interfaces for cohesive Application persistence needs over table-mirroring generic CRUD contracts"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M architecture.md:94-98 (and root CLAUDE.md:80-84), M1 :78-81, L0 persistence-boundary.md:21, L1 boundaries.md:37, K0 architecture.md:42, K1 rules/backend/persistence.md:14. The approved-DDD Aggregate Root note appears in M, M1, L0, K0 and is conditional on an approved design.")

P("ARC-014",
  dims=["D1 repository interfaces expose no IQueryable, DbSet, DbContext, EF expressions or provider types; EF query construction stays in Infrastructure"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT with the same 'return materialized results' guidance in each rule: M architecture.md:99-102, M1 :84-86 (+:82-83), L0 persistence-boundary.md:22, L1 rules/2-technology/persistence/access.md:11, K0 architecture.md:43, K1 persistence.md:15. No candidate checks it mechanically.")

P("ARC-015",
  dims=["D1 Application does not depend on IGenericRepository<T>; a generic repository/base may exist only in Infrastructure to remove real duplication"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT with the same Infrastructure-only allowance in each rule: M architecture.md:106-111, M1 :103-108, L0 persistence-boundary.md:23 (also listed as not adopted in the imported overview.md:38-41), L1 boundaries.md:38, K0 architecture.md:44, K1 persistence.md:16. The 'MAY' skill lines describe the same allowance (protected helpers in a base class).")

P("ARC-016",
  dims=["D1 IUnitOfWork is the normal commit boundary of a use case; repositories stage changes and Application Services decide when to commit"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M architecture.md:115-119 (and root CLAUDE.md:80-84), M1 :112 with :122-124 ('Repositories stage changes and do not independently commit'), L0 persistence-boundary.md:27, L1 boundaries.md:39, K0 architecture.md:48, K1 architecture-style.md:40. M1's capability manifest phrase 'one SaveChangesAsync per use case' (MODULE.md:34) is a description of the same binding, not read by any checker.")
