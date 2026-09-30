# Goal: Design CleanArchitectureTemplate V3

## Context

This repository is a research environment for evolving
CleanArchitectureTemplate V2 into V3.

Before doing anything else, read:

- `research/hypothesis.md`
- `research/requirements.md`

Then inspect the complete V2 template located at:

- `templates/v2-baseline/`

Treat V2 as an existing working system that must be understood before redesigning it.

Inspect all relevant artifacts, including where present:

- `CLAUDE.md`;
- `.claude/rules`;
- `.claude/skills`;
- subagents;
- hooks;
- commands;
- reference documents;
- project customization files;
- specification files.

Do not assume that the proposed ideas in `requirements.md` are all correct.

Distinguish between:

- mandatory invariants;
- goals;
- design hypotheses;
- non-goals.

You are explicitly expected to challenge design hypotheses when a different solution
would better satisfy the goals and invariants.

---

# Primary Goal

Design a proposed V3 instruction architecture that improves the current V2 system.

The design should focus on:

- modularity;
- clear ownership of instructions;
- single source of truth;
- separation of concerns;
- predictable instruction loading;
- reliable triggering;
- architectural decision control;
- maintainability;
- efficient context usage;
- appropriate deterministic enforcement;
- Claude autonomy without loss of human architectural control.

The goal is NOT to mechanically reorganize files.

The goal is to design a coherent instruction system.

---

# Important constraint

DO NOT modify:

- `templates/v2-baseline/`
- `templates/v3/`

during this task.

This is a design and analysis phase only.

The first output must be reviewed by humans before V3 implementation begins.

---

# Analysis requirements

## 1. Analyze V2 as a system

Build a mental model of how the current template works.

Identify:

- major instruction artifacts;
- their responsibilities;
- overlapping responsibilities;
- duplicated normative rules;
- large or poorly cohesive modules;
- implicit dependencies between instructions;
- unclear ownership;
- potentially conflicting rules;
- places where policy and workflow are mixed;
- places where deterministic enforcement could replace prompt instructions.

Do not report duplication merely because similar words appear in multiple files.

Focus on semantic duplication of policy or responsibility.

Whenever possible, reference concrete V2 file paths when describing a problem.

---

## 2. Analyze instruction loading and triggering

For the current V2 system, identify how you expect instructions to become available
during different types of tasks.

Distinguish where possible between:

- always-loaded context;
- path-dependent rules;
- skill-triggered context;
- explicitly invoked workflows;
- reference material loaded on demand.

Identify situations where:

- a required instruction may fail to load;
- too much unrelated context may load;
- multiple artifacts may compete for the same responsibility;
- a skill or rule may be difficult to trigger reliably.

This is an expected-loading analysis.

Do not claim that a trigger is empirically reliable unless it has actually been tested.

---

## 3. Propose the V3 architecture

Design the architecture you believe best satisfies the research requirements.

You may use ideas from `requirements.md`, modify them, combine them, or reject
design hypotheses when justified.

Do NOT assume that this proposed hierarchy must be used:

`Core → Architecture → Technology → Project → Feature → Task`

Evaluate whether it is useful.

If you propose a different abstraction model, explain why.

The proposed architecture should make clear:

- major instruction categories;
- their responsibilities;
- dependency direction;
- ownership boundaries;
- extension points;
- scope rules;
- loading strategy.

---

## 4. Define normative ownership

For important policy categories, identify the proposed authoritative owner.

The design should minimize normative duplication.

Explain how artifacts such as:

- `CLAUDE.md`;
- rules;
- skills;
- reference files;
- project configuration;
- feature specifications

should interact without independently copying the same policy.

---

## 5. Define skills versus rules versus references

Explain the intended responsibility of each mechanism.

In particular, evaluate whether skills should primarily represent:

- workflows;
- capabilities;
- policy;
- orchestration;
- references;

or some combination.

Explain where V2 currently mixes these responsibilities and what V3 should change.

---

## 6. Define backend/frontend/common scope

Evaluate how instructions should be separated between:

- common engineering concerns;
- C#/.NET backend;
- Angular frontend;
- testing;
- other relevant scopes.

Do not introduce React-specific architecture.

Backend development is the primary focus of the template.

---

## 7. Define architectural decision control

Propose how V3 should distinguish between:

- decisions already defined by policy;
- decisions Claude may make autonomously;
- decisions requiring human approval.

Explain how Claude should behave when a feature requires an architectural decision
that existing policy does not resolve.

---

## 8. Define policy versus enforcement

Identify classes of rules that should remain LLM instructions and classes that
would be better enforced using deterministic mechanisms such as:

- analyzers;
- tests;
- architecture tests;
- hooks;
- scripts;
- formatters;
- compiler checks.

Do not move a rule out of prompt context merely because deterministic validation exists
if knowing the rule during generation still materially improves output quality.

---

## 9. Identify trade-offs and risks

Explicitly look for risks introduced by the proposed architecture, including:

- over-fragmentation;
- unreliable triggering;
- excessive indirection;
- excessive file discovery;
- larger context consumption;
- hidden dependencies;
- harder human navigation;
- unnecessary architectural complexity.

Do not optimize for architectural elegance alone.

---

## 10. Challenge our ideas

Create a dedicated section containing requirements or design hypotheses you disagree
with or would modify.

For each one, explain:

- what the concern is;
- what failure mode it could cause;
- what alternative you recommend.

Do not agree with an idea merely because it appears in the requirements.

---

## 11. Migration strategy

Propose a staged migration from V2 to V3.

The migration should minimize accidental loss of useful V2 behavior.

Identify:

- what should be moved;
- what should be consolidated;
- what should be split;
- what should remain unchanged;
- what should potentially be removed;
- what requires behavioral testing after migration.

Do not perform the migration yet.

---

# Required output

Write the complete analysis and design proposal to:

`research/observations/001-v3-design-proposal.md`

The document should contain at least:

1. Executive summary
2. Current V2 architecture
3. V2 problems and risks
4. Proposed V3 architecture
5. Instruction ownership model
6. Loading and triggering model
7. Skills / rules / references responsibility model
8. Backend / frontend / common scope model
9. Architectural decision-control model
10. Policy versus deterministic enforcement
11. Proposed migration plan
12. Risks and trade-offs
13. Disagreements with the provided design hypotheses
14. Open questions requiring human decisions

Do not modify the V3 template.

Stop after producing the design proposal.