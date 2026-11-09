from jdsl import C, D, P  # noqa: F401

P("API-009",
  dims=["D1 represent common expected outcomes explicitly when useful, without forcing a generic Result<T>",
        "D2 no HTTP-named outcome categories in Application"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each rule: M rules/error-handling.md:33-38, M1 error-handling.md:15-23, L0 rules/1-architecture/outcomes.md:14-15, L1 rules/1-architecture/roles.md:29, K0 rules/backend/error-handling.md:22, K1 rules/backend/api.md:28. A project-wide Result model is Reserved in all six (ARC-020 item 7); the skills give the same 'when to consider Result' technique.")

P("API-010",
  dims=["D1 FluentValidation for explicit request/use-case validation where appropriate",
        "D2 transport validation in API, use-case rules in Application, invariants in Domain (each at its owning boundary)"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each rule: M error-handling.md:44-50, M1 error-handling.md:68-76, L0 rules/2-technology/fluentvalidation.md:10 with outcomes.md:25-30, L1 rules/2-technology/backend-libraries.md:10, K0 error-handling.md:27, K1 api.md:29. The 'do not move Domain invariants into FluentValidation merely because the library is available' clause appears in M1, L1, K1 rules and in the M, L0, K0 skills.")

P("API-011",
  dims=["D1 do not establish business exceptions as the default architecture or throw/catch to jump between normal expected branches"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M error-handling.md:39-40, M1 :27-30 (and :15-20), L0 outcomes.md:16, L1 rules/0-core/http-api.md:24, K0 error-handling.md:23, K1 api.md:30. M and M1 add that typed exceptions for selected cases are a project-level decision, consistent with the others' Reserved project-wide conventions.")

P("API-012",
  dims=["D1 log an unexpected exception once at the boundary that handles it, not in every layer"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each owner: M error-handling.md:54-56, M1 :45-48, L0 rules/0-core/logging-principles.md:15, L1 http-api.md:25, K0 error-handling.md:18, K1 api.md:23. logging skills in all six add 'do not add another log when rethrowing without handling'.")

P("API-013",
  dims=["D1 introduce API versioning only for a concrete compatibility need, not because an API exists"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M api.md:33-35, M1 api.md:33-35, L0 entry-points.md:33, L1 http-api.md:30, K0 api.md:25, K1 api-contracts.md:12. Adopting versioning is Reserved in all six (Reserved item 9), so the approval step is uniform.")

P("API-014",
  dims=["D1 once external clients rely on a version, a breaking contract change requires a new version or another explicitly approved compatibility strategy",
        "D2 any breaking public API change is Reserved (approval)"],
  label="FULL_SEMANTIC_PARITY",
  cells={c: C(compliance="STRICTER_THAN_CANONICAL", note="Reserved item 9 requires approval for any breaking public API change, not only for relied-on versions; same in all six.") for c in ["M", "M1", "L0", "L1", "K0", "K1"]},
  same="D1 is the same rule in each API rule: M api.md:36-39 ('by default' with the approved-alternative clause, plus 'not judged only by compilation'), M1 api.md:36-38, L0 entry-points.md:34, L1 http-api.md:31, K0 rules/backend/api.md:26, K1 api-contracts.md:13. D2 is Reserved item 9 in root CLAUDE.md of all six (M :127, M1 :89, L0 :48, L1 :35, K0 :45, K1 :41).",
  challenge="v3 stores STRONGER_AND_WEAKER_EVIDENCE for K0 and K1. Challenged side by side: the 'stronger' evidence is the rule plus Reserved item 9, which all six share; the 'weaker' evidence is a swagger-skill technique line ('treat breaking schema changes seriously', K0 swagger:78, K1 swagger:66) that mirrors the rule for client generation and relaxes nothing. M, M1, L0 and L1 have equivalent skill lines that Step 2 linked differently. Result: the mixed label reflects record linkage, not a K0/K1 difference; full parity holds.")

P("API-015",
  dims=["D1 when explicit versioning is required, use one strategy consistently; URL-segment by default unless requirements justify another"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M api.md:40-42, M1 api.md:39-41, L0 entry-points.md:35, L1 http-api.md:32, K0 api.md:27, K1 api-contracts.md:14. 'Do not mix strategies without a concrete reason' appears in the skills of all six.")

P("API-016",
  dims=["D1 Swagger/OpenAPI metadata describes the running API (routes, important statuses including pipeline-produced ones, schemas, authentication); no speculative responses"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M api.md:47-51, M1 api.md:47-49, L0 entry-points.md:41, L1 backend-libraries.md:11, K0 api.md:32, K1 api-contracts.md:19. The whole-pipeline status list and the 'no 201 for a 200 endpoint' detail sit in the rule (M, L1) or the swagger skill (M1, L0, K0, K1); Bearer security definitions only when authentication is actually used appear in all six skills.")
