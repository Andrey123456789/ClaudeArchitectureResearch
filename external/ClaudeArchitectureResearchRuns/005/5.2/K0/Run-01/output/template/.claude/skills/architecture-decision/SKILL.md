---
name: architecture-decision
description: Use when a choice may be Reserved or is unclear, when the user approves or requests an architecture, stack, convention or public-API change, when recording or changing a decision-register entry, or when deprecating an API version.
---
<!-- Kind: WF | Scope: common | Owns: decision request, recording and propagation procedure; API version deprecation procedure | Loads: workflow invocation -->
# Architecture Decision

Decision classes, the Reserved list, the five-question test and the Decision Request fields: CLAUDE.md § Decisions.

## 1. Classify

Apply the five-question test. Decided → follow the register and stop here. Delegated → proceed and mention the choice in the output. Reserved → continue.

## 2. Prepare the Decision Request

- **Context** — the requirement and why a decision is needed now.
- **Options** — at least the status quo or smallest viable option and the requested alternative, with trade-offs and reversal cost.
- **Recommendation** — one option with the reason.
- **Blocked** — the work that waits for the decision.
- **Proceeding with** — the policy-compliant non-Reserved work that continues meanwhile.

Name the register entries and `Affects` targets that would change.

## 3. Obtain Approval

- Ask the user. An explicit user instruction counts as approval.
- Autonomous or headless run: do not decide; continue only with "Proceeding with" and report the open Decision Request.

## 4. Record

- Add or update the register row in `docs/architecture/decision-register.md`: stable ID (never reused or renumbered), one-line decision summary, `Details in` (owner of detailed policy), `Affects` (every STD, KNW, WF and ENF artifact to update).
- For Reserved decisions add an ADR `docs/decisions/NNNN-<slug>.md` (create the directory with the first ADR):

      # NNNN. <Title>
      Status: Accepted (<date>, approved by <who>)
      Context: <forces and requirement>
      Decision: <what was decided>
      Alternatives considered: <options and why not>
      Consequences: <trade-offs, follow-up work>
      Register entry / affected artifacts: <ID, Affects>

- Keep the register a summary: detailed rules go to their owner — a standard, workflow or knowledge skill — never into the register.

## 5. Propagate

- Update every `Affects` target in the same change. Example: replacing NUnit touches the testing standard, the `dotnet-testing` knowledge skill, scaffolding and verification commands, and the manifest checks listed for DEC-TEST-01.
- Run `node .claude/scripts/check-instructions.mjs` and fix every reported failure.
- Implement the code change through `development-workflow`.

## API Version Deprecation

When deprecating an externally consumed API version, **must**:

1. mark the deprecation in the versioning metadata;
2. document the replacement version;
3. communicate a realistic migration period and removal timeline to consumers;
4. keep the old version working for the promised support period.

**Must not** remove an externally consumed version without considering its published support contract. Removal and breaking changes are themselves Reserved (step 2).

## Output

Decision class; Decision Request (when Reserved); approval status; register/ADR changes; Affects targets updated; checker result.
