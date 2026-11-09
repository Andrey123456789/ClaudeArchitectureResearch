from jdsl import C, D, P  # noqa: F401

_INNER_CHECK = ("M1: check-architecture.js reads forbiddenNamespaces (Microsoft.AspNetCore and the persistence technology namespaces) for the core-model and use-case layers from capabilities/architecture/clean-architecture/MODULE.md:49-52, run by its post-tool-use hook. "
                "L1: check-architecture.mjs:90-104 rejects Microsoft.AspNetCore.App (also implied by the Web SDK) and its packages in inner roles (check.json:11-12) and EF Core packages in domain/use-case roles (persistence/ef-core/enforcement.json), run by post-change-checks. "
                "K1: facets/architecture-style.cjs:73-85 errors on the Web SDK, the ASP.NET Core shared framework or Microsoft.AspNetCore.* packages in Domain/Application, and facets/persistence-technology.cjs errors on EF Core packages there. "
                "M, L0 and K0 have no such check (searched every hook and script for AspNetCore/EntityFrameworkCore/framework-reference logic).")

P("ARC-001",
  dims=["D1 production project references point inward: Domain none; Application->Domain; Infrastructure->Application/Domain; Api->Application and Infrastructure only for composition"],
  label="FULL_SEMANTIC_PARITY",
  same="The same reference graph is stated in each backend architecture rule: M rules/architecture.md:17-25 and :32-35 (M also states the adopted style in root CLAUDE.md:80-84), M1 rules/architecture.md:17-25, L0 rules/1-architecture/backend-layers.md:15-21 (style also in the always-imported overview.md:14-18), L1 rules/1-architecture/frame/boundaries.md:12, K0 rules/backend/architecture.md:17, K1 rules/backend/architecture-style.md:21. Path rules load on backend files, which is where the policy applies. All six also carry a mechanical project-reference-graph check (M check-manifests.mjs:55-61, M1 check-architecture.js, L0 manifest-checks.mjs:53-59, L1 clean-architecture/check.json:6-9, K0 check-dependencies.cjs:144-146, K1 facets/architecture-style.cjs).",
  enforcement="Graph check present in all six (source-read). Whether each blocks or reports, and agreement on one fixture, was not compared in v3's same-task matrix: equivalence of outcomes UNVERIFIED.")

P("ARC-002",
  dims=["D1 Domain is free of EF Core, ASP.NET Core, HTTP, persistence and external-service implementation concerns",
        "D2 mechanical detection of Domain depending on ASP.NET Core or persistence technology"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same MUST in each backend architecture rule: M architecture.md:51-52, M1 architecture.md:32-33, L0 backend-layers.md:27, L1 frame/boundaries.md:16, K0 architecture.md:22 (adds mapping-library concerns), K1 architecture-style.md:26. Skill lines ('where practical' for EF configuration placement) are technique advice under the same rule in all six.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "L1", "K1"], ["M", "L0", "K0"]],
           "M1, L1 and K1 check inner-layer framework/package or namespace leakage mechanically; M, L0 and K0 rely on the rule text and code review. " + _INNER_CHECK,
           counterexample="Same task: the agent adds <PackageReference Include=\"Microsoft.AspNetCore.Http.Abstractions\"/> (or <FrameworkReference Include=\"Microsoft.AspNetCore.App\"/>) to the Domain project. Static outcome: L1 and K1 checkers report an error; M1 reports a forbidden-namespace finding once the type is used; M, L0 and K0 report nothing. Whether a PostToolUse finding stops the agent in a live host is NOT_RUN.",
           root="RC-ENF-INNER-LAYER", evidence={"M1": ["FG-M1-f85a80b231"], "L1": ["FG-L1-21ae6647aa"], "K1": ["FG-K1-35ac3364ed"], "M": ["FG-M-74d3d0417b"], "L0": ["FG-L0-48911b59b7"], "K0": ["FG-K0-252eecbe20"]})],
  enforcement="Source-read checker code; not executed on a shared fixture in v3 or in Step 3.")

P("ARC-003",
  dims=["D1 simple domain entities are the default; straightforward CRUD/workflow rules belong in Application Services"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default with the same clarifying list (validation rules, immutable fields, status transitions, allowed/forbidden edits do not by themselves justify a Rich Domain Model) in each backend architecture rule: M architecture.md:53-56, M1 :29-30/:34-37, L0 backend-layers.md:28, L1 boundaries.md:17, K0 architecture.md:23, K1 architecture-style.md:27.")

P("ARC-004",
  dims=["D1 move behavior into Domain only when non-trivial invariants benefit from domain encapsulation; otherwise a Rich Domain Model/DDD tactical pattern requires approval unless the approved specification requires it"],
  label="FULL_SEMANTIC_PARITY",
  same="Same sentence including the 'unless the approved specification already requires it' exception in each rule: M architecture.md:57-61, M1 :38-42, L0 backend-layers.md:29, L1 boundaries.md:18, K0 architecture.md:24, K1 architecture-style.md:28; all six also list Rich Domain Model/DDD tactical patterns as Reserved in root CLAUDE.md (M :94/:115, M1 :74, L0 :41, L1 :35, K0 :38, K1 :34).")

P("ARC-005",
  dims=["D1 do not add factories, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects or similar constructs merely to look domain-driven"],
  label="FULL_SEMANTIC_PARITY",
  same="Same enumerated MUST_NOT in each rule: M architecture.md:62-65, M1 :43-46, L0 backend-layers.md:30, L1 boundaries.md:19, K0 architecture.md:25, K1 architecture-style.md:29. Layout references in M, L0, K0, K1 add that DDD directories appear only for an approved design.")

P("ARC-006",
  dims=["D1 Application Services are the default orchestration mechanism for use cases"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M architecture.md:69-73 (and root CLAUDE.md:80-84), M1 :50-52, L0 backend-layers.md:34, L1 boundaries.md:23, K0 architecture.md:29, K1 architecture-style.md:34; M, L0, K0 and K1 add that a large service is a signal to reconsider responsibilities, not to add a pattern (M1 states the same at architecture.md:58).")

P("ARC-007",
  dims=["D1 define persistence and external-service abstractions in Application when use cases require them; keep infrastructure details out"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M architecture.md:74-76, M1 :53-55 (and repository interfaces :82-83), L0 backend-layers.md:35, L1 boundaries.md:24, K0 architecture.md:30, K1 architecture-style.md:35. Skill lines (HttpClient, caching, caller identity) apply it per technique in all six; K0/K1 httpclient-factory 'may define' is about the optional HTTP abstraction, not the rule.")

P("ARC-008",
  dims=["D1 Application must not depend on DbContext, DbSet, EF Core APIs/provider types or ASP.NET Core transport types",
        "D2 mechanical detection of Application depending on persistence technology or ASP.NET Core"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same MUST_NOT in each rule: M architecture.md:77-78, M1 :56-57 with the type list in persistence-technology.md:21-26, L0 backend-layers.md:36, L1 boundaries.md:25, K0 architecture.md:31, K1 architecture-style.md:36. The technology-neutral wording of L0/L1/K1/M1 names the same type classes.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "L1", "K1"], ["M", "L0", "K0"]],
           "Same asymmetry as ARC-002, for the use-case layer. " + _INNER_CHECK,
           counterexample="Same task: the agent adds Microsoft.EntityFrameworkCore to the Application project to call ToListAsync in a service. Static outcome: L1 (enforcement.json forbiddenInRoles) and K1 (persistence-technology.cjs) report an error, M1 flags the EF Core namespace; M, L0 and K0 report nothing. Live-host effect of the finding NOT_RUN.",
           root="RC-ENF-INNER-LAYER", evidence={"M1": ["FG-M1-f85a80b231"], "L1": ["FG-L1-f0cf2d0f61"], "K1": ["FG-K1-35ac3364ed"], "M": ["FG-M-a8420062f9"], "L0": ["FG-L0-f7d95e5ea0"], "K0": ["FG-K0-9cb4d8f690"]})],
  enforcement="Source-read checker code; not executed on a shared fixture in v3 or in Step 3.")
