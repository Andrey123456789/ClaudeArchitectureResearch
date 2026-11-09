> Kind: — (slot contract) | Scope: repo/meta | Capability: persistence | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Slot Contract: persistence

- Slot type: required leaf
- Cardinality: exactly one implementation, with one provider variant
- Binds: architecture (Infrastructure role implements the Application persistence and commit-boundary contracts)

A provider change (for example to another relational database) is a variant change inside this slot, not a new slot. Replacing the implementation (for example with a micro-ORM) requires every item below; an item the proposed implementation cannot provide — such as a migration mechanism — is surfaced as *Blocked* in the Decision Request instead of being dropped.

## Required items

| Item | An implementation must provide |
|---|---|
| `technology-boundary` | Which technology types exist only in Infrastructure and how they stay out of Application |
| `commit-boundary-binding` | How the Application commit-boundary contract is implemented |
| `migration-mechanism` | How schema changes are created, reviewed, and applied |
| `seeding-mechanism` | How Development seed data is constructed and invoked |
| `provider-variant` | The selected provider and its variant-specific configuration |
| `declared-properties` | Observable properties such as string comparison and case sensitivity |
| `testing-implications` | Provider-fidelity guidance for tests |
| `change-workflow` | The workflow for setup, model, migration, and seed changes |
| `knowledge` | The knowledge facet for implementation technique |
| `enforcement` | Deterministic checks for boundary leaks and co-change reminders |
