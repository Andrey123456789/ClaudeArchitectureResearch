# V2 Policy Inventory Audit — v0.4 proposal

Audited against:

- repository HEAD observed during audit: `343a88472482496f5706248e19fd5691d1abf903`
- frozen V2 baseline tree: `563f575316fd60997b73a91187868459cdb15630`
- source inventory schema: `0.3`
- source policy count: `180`

## Proposed result

- remove 2 non-V2 `research_shared` entries from the V2 oracle;
- add 16 V2-derived policies that were materially underrepresented;
- resulting hidden V2-only oracle: **194 policies**;
- repair 4 broken `verify/SKILL.md` heading references;
- expand traceability for several existing normalized policies;
- make generated-output regeneration cover source-contract changes explicitly;
- add an explicit audited `intentional_non_oracle_material` register;
- change the information boundary so candidate construction and benchmark execution cannot see the inventory.

## Policies moved out of the V2 oracle

- `GOV-017` — Decision control protocol
- `GOV-018` — Challenge questionable instructions

They remain valid shared research constraints but are not derived from V2. The migration script writes them to `shared-research-invariants.proposed.json`.

## V2 policies added

- `GOV-021` — Custom settings changes propagate across affected surfaces
- `ARC-028` — Test-project production references stay narrow
- `ARC-029` — Transport contracts avoid gratuitous duplication
- `PST-009` — Schema-affecting custom settings co-change with persistence artifacts
- `PST-010` — EF Core migrations are reviewed source code
- `API-021` — Normal client cancellation is not a server failure
- `API-022` — API deprecation preserves the promised migration window
- `SEC-016` — Authentication uses established platform mechanisms
- `SEC-017` — Bearer authentication keeps effective token validation
- `SEC-018` — Authentication failures avoid account-enumeration leaks
- `RUN-023` — Cache entries have explicit expiration or invalidation semantics
- `RUN-024` — C# file and async naming conventions remain conventional
- `DEP-025` — npm peer-dependency conflicts are not bypassed by force flags
- `DEP-026` — Local Development database configuration is usable and non-secret
- `FE-011` — Avoid nested manual RxJS subscriptions
- `FE-012` — Manual RxJS subscriptions follow framework lifecycle

## Existing source-reference repairs

- `TST-010`: `#Preserve Behavioral Verification` → `#4. Preserve Behavioral Verification`
- `WF-004`: `#Inspect the Change` → `#1. Inspect the Change`
- `WF-005`: `#Build` → `#2. Build`
- `WF-007`: `#Architecture Check` → `#5. Architecture Check`

## Existing traceability expanded

Additional V2 source references are added to:

- `GOV-012`, `GOV-013`, `ARC-020`
- `API-018`, `API-019`
- `TST-007`
- `DEP-010`, `DEP-011`
- `WF-016`

`WF-016` is also normalized to make regeneration explicit when a generated artifact's source contract/configuration changes.

## How to build the full proposed JSON

From the repository root:

```bash
python build_inventory_v04.py --repo-root .
```

By default this writes:

```text
research/policy/inventory.v0.4.proposed.json
research/policy/shared-research-invariants.proposed.json
```

The source `research/policy/inventory.json` is not overwritten.

The script fails if:

- the source is not the expected v0.3 / 180-policy oracle;
- the baseline tree SHA differs;
- expected policy IDs changed;
- duplicate IDs are produced;
- any policy in the new oracle is not `origin=v2`;
- any policy points outside `templates/v2-baseline/`;
- any source file or Markdown heading reference is missing.
