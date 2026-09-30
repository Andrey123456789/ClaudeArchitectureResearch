# V3 Requirements

## 1. Purpose

V3 is an experimental evolution of `CleanArchitectureTemplate V2`.

The goal is not merely to reorganize Markdown files. The experiment investigates whether software-architecture principles can be applied to Claude Code instructions in order to make Claude's behavior more predictable, maintainable, modular, and autonomous.

V3 must preserve the useful behavior and constraints of V2 while improving the architecture of the instruction system itself.

---

## 2. Goals

V3 should aim to improve the following characteristics.

### 2.1 Modularity

Instructions should be divided into coherent modules instead of accumulating unrelated concerns in large files.

Large rules and skills should be decomposed where doing so improves cohesion, maintainability, discoverability, and selective loading.

Over-fragmentation should be avoided.

### 2.2 Hierarchy of instructions

The instruction system should distinguish between different levels of abstraction and stability.

Examples of possible levels include:

- fundamental agent and engineering principles;
- architecture-specific policy;
- technology-specific policy;
- project-specific decisions;
- feature-specific requirements;
- task-specific instructions.

This is a design hypothesis, not a mandatory directory structure.

Claude may propose a different hierarchy if it better satisfies the goals of the experiment.

### 2.3 Stable dependencies

More volatile and specific instructions should depend on more stable and fundamental policies, not the reverse.

A task or feature may rely on architectural policy.

Fundamental architectural or agent policy should not depend on a particular feature or task.

### 2.4 Separation of concerns

Different kinds of knowledge and behavior should have clearly defined ownership.

Examples include:

- engineering principles;
- architectural constraints;
- technology-specific conventions;
- project decisions;
- feature requirements;
- workflow/orchestration instructions;
- validation and enforcement.

### 2.5 Single source of truth

Normative rules should not be independently duplicated across multiple locations such as:

- `CLAUDE.md`;
- rules;
- skills;
- reference files;
- project documentation.

Each normative rule should have one authoritative source.

Other artifacts may reference or load that source, but should not maintain independent copies of the same policy.

### 2.6 Explicit scope

Instructions should clearly define where they apply.

The architecture should support separation between concerns such as:

- common rules;
- backend rules;
- frontend rules;
- testing rules;
- architecture-specific rules;
- technology-specific rules.

For the current template, backend development is primarily C#/.NET.

Frontend-specific design should target Angular where frontend concerns are required.

React support is not a goal of this experiment.

### 2.7 Selective loading

Claude should receive relevant instructions when they are needed instead of loading all available guidance into every task.

V3 should evaluate appropriate use of:

- always-loaded instructions;
- path-scoped rules;
- skill-triggered instructions;
- explicit workflows;
- reference files loaded on demand.

Selective loading must not make important rules unreliable or undiscoverable.

### 2.8 Reliable triggering

Modularization must not reduce the reliability with which required rules, skills, or references are activated.

Where possible, V3 should make expected loading and triggering behavior understandable and testable.

### 2.9 Architectural decision control

Claude should distinguish between:

- decisions it is allowed to make autonomously;
- decisions already established by project policy;
- decisions that require explicit human approval.

Claude must not silently introduce major architectural changes merely because they simplify a local task.

Examples include, but are not limited to:

- introducing DDD;
- changing the domain-model style;
- introducing CQRS;
- adding MediatR;
- changing architectural boundaries;
- introducing major libraries or frameworks;
- changing repository or Unit of Work policy;
- adopting a substantially different architectural pattern.

When existing policy does not provide enough guidance for such a decision, Claude should surface the decision instead of silently resolving it.

### 2.10 Policy versus enforcement

V3 should distinguish between rules that require LLM judgment and rules that can be enforced deterministically.

Where appropriate, deterministic mechanisms should be preferred for deterministic constraints.

Possible mechanisms include:

- compiler checks;
- analyzers;
- formatting tools;
- unit tests;
- architecture tests;
- scripts;
- hooks.

Claude instructions should not consume permanent context for constraints that can be reliably enforced elsewhere unless the instruction is still useful for generation quality.

### 2.11 Maintainability

A developer should be able to understand:

- where a rule belongs;
- which file owns it;
- where it applies;
- when it is loaded;
- whether it is guidance or enforced deterministically.

Adding a new technology, policy, or feature should not require editing many unrelated instruction files.

### 2.12 Efficient use of Claude

The architecture should avoid unnecessary context and reasoning overhead where possible.

Different kinds of tasks may justify different:

- effort levels;
- workflows;
- permission modes;
- skills or subagents.

V3 may encode appropriate execution settings into skills or workflows where this improves reliability and reduces manual configuration.

### 2.13 Self-development / dogfooding

Claude should be capable of participating in the evolution of the template itself.

Changes to the instruction architecture should preferably follow a lifecycle such as:

1. analyze the current system;
2. identify relevant constraints;
3. propose a design or migration plan;
4. surface questionable assumptions;
5. implement approved changes;
6. audit the resulting instruction system;
7. validate behavior.

The template should therefore be understandable enough for Claude to reason about and modify safely.

---

## 3. Invariants

The following requirements are stronger than design preferences.

### 3.1 Preserve useful V2 behavior

V3 must not intentionally remove useful constraints, conventions, workflows, or capabilities from V2 unless there is an explicit reason to do so.

When moving or restructuring a rule, its semantic intent must be preserved unless the rule itself is deliberately changed.

### 3.2 No normative duplication

A normative statement should have one authoritative owner.

If the same rule is currently duplicated in V2, V3 should attempt to consolidate ownership rather than copy the duplication into the new architecture.

### 3.3 No silent architectural overrides

A more specific instruction, feature, or task must not silently redefine a more fundamental architectural policy.

Conflicts or missing architectural decisions should be surfaced explicitly.

### 3.4 Scope must be identifiable

It should be possible to determine what part of the project an instruction applies to.

### 3.5 Loading must be intentional

Instructions should not be loaded globally merely because doing so is convenient.

Likewise, critical instructions must not be hidden behind unreliable triggers.

### 3.6 Architecture must remain understandable to humans

The template is not only for Claude.

A developer reviewing the repository should be able to understand the major instruction layers, ownership rules, and extension points without reconstructing the design from dozens of unrelated files.

### 3.7 Claude must challenge questionable requirements

When a requested design change appears likely to:

- increase duplication;
- reduce cohesion;
- harm trigger reliability;
- increase unnecessary context;
- create conflicting instructions;
- reduce maintainability;
- introduce unnecessary complexity;

Claude should explicitly identify the concern and propose an alternative before implementation.

The final decision remains with the human reviewer.

---

## 4. Design hypotheses

The following ideas are intentionally treated as hypotheses rather than fixed implementation requirements.

Claude should evaluate them and may recommend alternatives.

### 4.1 Layered instruction architecture

A hierarchy resembling:

`Core → Architecture → Technology → Project → Feature → Task`

may provide useful separation by stability and abstraction.

Claude should assess whether this exact hierarchy is appropriate.

### 4.2 Smaller coherent modules

Large rules and skills may benefit from decomposition into smaller cohesive units.

However, smaller files are not inherently better.

The design should balance:

- cohesion;
- discoverability;
- context efficiency;
- triggering reliability;
- maintenance overhead.

### 4.3 Skills as orchestration rather than policy duplication

Skills may work better when they coordinate workflows and load authoritative policy rather than independently restating architecture rules.

Claude should assess how far this separation should be taken.

### 4.4 Backend/frontend separation

Common, backend, and frontend instruction scopes may benefit from explicit separation.

The design should consider path-based and other conditional-loading mechanisms where appropriate.

### 4.5 Instruction architecture manifest

A compact manifest or map describing instruction ownership, scope, loading, and enforcement may improve maintainability.

Claude should determine whether this should be a dedicated artifact or represented another way.

### 4.6 Task-specific execution strategy

Different task types may benefit from different effort levels or workflows.

Examples include:

- mechanical changes;
- feature implementation;
- debugging;
- architectural design;
- architectural review.

Claude should determine whether and where this knowledge belongs in the template.

---

## 5. Non-goals

The following are explicitly outside the current experiment.

### 5.1 Agent-agnostic architecture

V3 does not need to support Codex, Gemini, Copilot, or other coding agents.

The current research is specifically focused on Claude Code.

### 5.2 Universal software architecture support

V3 does not need to support every possible application architecture.

The current baseline is Clean Architecture and the initial experiment should remain focused enough to be testable.

The architecture may be designed with future extension in mind, but generalized framework development is not a current goal.

### 5.3 React support

React-specific rules, examples, workflows, or architecture are not required.

The relevant frontend technology for this experiment is Angular.

### 5.4 Maximum automation

The goal is not to eliminate human architectural control.

Claude should automate implementation where appropriate while preserving explicit human control over important architectural decisions.

### 5.5 Minimum token usage at any cost

Token usage is an efficiency metric, not the primary quality metric.

A design that consumes slightly more tokens but materially reduces human intervention or architectural errors may still be preferable.

### 5.6 Perfect V3 in one generation

The first generated V3 is expected to contain weaknesses.

The research process intentionally includes review, correction, intermediate versions, and behavioral testing.

---

## 6. Evaluation principles

V3 will eventually be compared with V2 using a small controlled benchmark.

Primary evaluation areas will include:

- goal completion;
- required human intervention;
- architectural violations;
- unrequested architectural decisions;
- required rework.

Efficiency will also be evaluated using Claude resource usage such as token or cost consumption.

Failures may be classified into categories such as:

- missing policy or instruction gap;
- instruction adherence failure;
- loading or triggering failure;
- conflicting or duplicated instructions;
- unclear or ambiguous instruction.

The detailed benchmark and metric definitions will be created separately and should not constrain the initial V3 design prematurely.

---

## 7. Design freedom

Claude is not expected to mechanically implement the ideas listed above.

Before changing V3, Claude should analyze V2 as a complete instruction system and propose the architecture it believes best satisfies these requirements.

Claude should:

- distinguish mandatory invariants from design hypotheses;
- identify weaknesses in the proposed requirements;
- challenge ideas that appear counterproductive;
- explain significant trade-offs;
- avoid unnecessary complexity;
- propose alternatives where appropriate.

The purpose of the experiment is to discover a better instruction architecture, not merely to implement a predetermined folder structure.