# SINGLE-CIS-K1-U0011 (1 records)

## CIS-K1-U0011 (pass 2) K1 .claude/rules/backend/architecture-style.md:28-28  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The ordinary justification for moving behavior into Domain requires the benefit of domain-level encapsulation to be independent of a particular use case.
TRIGGER: Considering moving non-trivial invariants or behavior into Domain under the selected architecture frame. | EXC: Source proceeds to an approval requirement for Rich Domain Model or DDD tactical patterns otherwise, with an already-approved specification exception; interpretation must preserve this context. | POL: ['ARC-003', 'ARC-004']
CODEX WHY: Canonical ARC-004 omits the qualifier. All three closest records retain broader domain-placement behavior; semantic entailment, rather than location or wording difference, remains the issue.
```
  25  
  26  - Domain must stay independent of the persistence technology, ASP.NET Core, HTTP, and external-service implementation concerns.
  27  - Default: simple domain entities. Straightforward CRUD and workflow rules, including validation rules, immutable fields, status transitions, and allowed or forbidden edits, belong in Application Services and do no
  28> - Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independent of a particular use case. Otherwise a Rich Domain Model or DDD tactical
  29  - Must not add factories, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects, or similar DDD constructs merely to make a simple model look
  30  - When an approved DDD design contains Aggregate Roots, they are the natural repository-boundary candidates.
  31  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-2c01d236b2 [28, 28] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-004', 'ARC-020'] rel=[]: Rich Domain/DDD tactical patterns require approval unless the approved specification already requires them.
- V2 FG-K1-5953b8f383 [28, 28] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-004'] rel=[]: Move behaviour into Domain only for non-trivial invariants materially benefiting from encapsulation; otherwise Rich Domain/DDD tactical patterns require approval unless the specification requires them.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0088 -> FG-K1-e5222f43b2 [CANONICAL_ONLY] Simple domain entities; straightforward CRUD and workflow rules (validation, immutable fields, status transitions, edit rules) belong in Application Services and do not justify a r
- NAMED primary/K1/constraints.jsonl/RULE-K1-0089 -> FG-K1-5953b8f383 [CANONICAL_ONLY] Move behaviour into Domain only for non-trivial invariants materially benefiting from encapsulation; otherwise Rich Domain/DDD tactical patterns require approval unless the specifi
- NAMED replica/K1/constraints.jsonl/RULE-K1-0034 -> FG-K1-e5222f43b2 [CANONICAL_ONLY] Simple domain entities; straightforward CRUD and workflow rules (validation, immutable fields, status transitions, edit rules) belong in Application Services and do not justify a r
- NAMED replica/K1/constraints.jsonl/RULE-K1-0035 -> FG-K1-5953b8f383 [CANONICAL_ONLY] Move behaviour into Domain only for non-trivial invariants materially benefiting from encapsulation; otherwise Rich Domain/DDD tactical patterns require approval unless the specifi
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0165 -> FG-K1-f7109bf988 [NON_NORMATIVE] In an approved DDD design Aggregate Roots are the natural repository-boundary candidates.
