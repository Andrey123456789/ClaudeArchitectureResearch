# Architecture

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Clean Architecture boundaries, domain/application/API responsibilities, repositories and decision gates.

## ARC-001 — Dependencies point inward

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Dependency Direction`

Domain depends on no application project; Application depends on Domain; Infrastructure depends on Application/Domain; API may reference Infrastructure only for composition; inner layers never depend on outer layers.

## ARC-002 — Domain is infrastructure independent

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Domain`

Keep Domain independent of EF Core, ASP.NET Core, HTTP, persistence and external-service implementation concerns.

## ARC-003 — Simple domain is default

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Domain`

Use simple domain entities by default; straightforward CRUD/workflow rules normally belong in Application Services.

## ARC-004 — Rich domain requires real invariants

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Domain`

Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation; Rich Domain Model/DDD tactical patterns otherwise require approval.

## ARC-005 — No decorative DDD

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Domain`

Do not add factories, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects or similar DDD constructs merely to appear domain-driven.

## ARC-006 — Application Services are default orchestration

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Application`

Use Application Services as the default orchestration mechanism for use cases.

## ARC-007 — Application owns use-case abstractions

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Application`

Define persistence and external-service abstractions in Application when use cases require them; keep infrastructure implementation details out.

## ARC-008 — No infrastructure/transport types in Application

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Application`

Application must not depend on DbContext, DbSet, EF Core APIs/provider types, or ASP.NET Core transport types.

## ARC-009 — No CQRS/mediator/VSA by default

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** always
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Application`

Do not introduce CQRS handlers, MediatR, Kommand, Vertical Slice Architecture or similar mediator-based organization unless explicitly approved.

## ARC-010 — Controllers are thin HTTP entry points

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#API`

ASP.NET Core Controllers are the default HTTP entry point; they bind/validate input, invoke Application services, and translate outcomes to HTTP responses.

## ARC-011 — Controllers do not own business/persistence

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#API`

Controllers must not contain business logic, access DbContext or concrete repositories, or manually construct infrastructure services.

## ARC-012 — Program is composition root

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#API`

Program.cs is the application composition root and may register Infrastructure implementations.

## ARC-013 — Prefer specific repositories

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Repositories`

Prefer specific repository interfaces representing actual cohesive Application persistence needs rather than table-mirroring generic CRUD contracts.

## ARC-014 — Repository contracts do not leak EF/queryability

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Repositories`

Repository interfaces must not expose IQueryable, DbSet, DbContext, EF expressions, or provider-specific types; EF query construction stays in Infrastructure.

## ARC-015 — Generic repository is Infrastructure-only

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Generic Repository`

Application must not depend on IGenericRepository<T>; any generic repository/base class may exist only as an Infrastructure implementation detail that removes real duplication.

## ARC-016 — Unit of Work is commit boundary

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Unit of Work`

Use IUnitOfWork as the normal commit boundary for an Application use case; repositories stage changes and Application Services decide when to commit.

## ARC-017 — Shared UoW context and no repository container

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Unit of Work`

Repositories in one use case share the same scoped Unit of Work/DbContext; IUnitOfWork must not become a repository container or service locator.

## ARC-018 — Explicit transactions only for real need

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Unit of Work`

Do not introduce explicit transaction APIs until a concrete use case requires control beyond normal SaveChangesAsync.

## ARC-019 — EF Core is Infrastructure detail

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#EF Core Boundary`

Use EF Core normally inside Infrastructure but do not leak EF Core concepts into Application.

## ARC-020 — Consequential architecture changes require approval

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/architecture.md#Consequential Decision Gate`

Consequential choices such as Rich Domain, CQRS/MediatR/VSA, event sourcing, project-wide Result, new layers/projects, multiple DbContexts, new persistence, messaging/background infrastructure, distributed caching, microservices, auth architecture, or replacement of approved baseline technology require explicit approval.
