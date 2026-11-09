from jdsl import C, D, P  # noqa: F401

P("API-001",
  dims=["D1 HTTP status codes and transport response semantics belong to the API layer; Application/Domain return no IActionResult or status codes"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each backend API rule: M rules/api.md:15-17, M1 rules/api.md:16-18, L0 rules/1-architecture/entry-points.md:17, L1 rules/1-architecture/roles.md:28, K0 rules/backend/api.md:16 (adds ProblemDetails), K1 rules/backend/api.md:12.")

P("API-002",
  dims=["D1 ProblemDetails for non-validation failures and ValidationProblemDetails for request validation (default)",
        "D2 machine-readable error contracts stay stable and safe"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each rule: M rules/error-handling.md:15-18, M1 error-handling.md:52-55, L0 rules/2-technology/aspnet-core.md:22 (+ entry-points.md:22), L1 rules/0-core/http-api.md:12 (RFC 9457 wording), K0 rules/backend/api.md:17, K1 rules/backend/api.md:20. Anti-pattern catalogues (anonymous error objects) appear in all six skills.")

P("API-003",
  dims=["D1 choose 200/201/202/204 by actual HTTP semantics; not 200 for everything, 201 for an internal insert, or 202 for completed work"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST with the same three counterexamples in each rule: M api.md:18-21, M1 api.md:19-22, L0 entry-points.md:26, L1 http-api.md:13, K0 api.md:18 (adds consistency across similar endpoints), K1 api.md:13. http-api skills in all six give the same per-status technique.")

P("API-004",
  dims=["D1 a successful collection query with zero matches returns 200 with an empty collection, not 404 (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M api.md:22-23, M1 api.md:23-24, L0 entry-points.md:27, L1 http-api.md:14, K0 api.md:19, K1 api.md:14.")

P("API-005",
  dims=["D1 401 for missing/failed authentication, 403 for an authenticated principal without permission",
        "D2 404 hiding of protected resources only as a deliberate, consistent security policy"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each rule: M api.md:24-26, M1 api.md:25-27, L0 entry-points.md:28, L1 http-api.md:15, K0 api.md:20, K1 api.md:15. http-api skills explain the same semantics.")

P("API-006",
  dims=["D1 409 for a valid request conflicting with current state; 412 when an explicit HTTP precondition such as If-Match fails"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M api.md:27-28, M1 api.md:28-29, L0 entry-points.md:29, L1 http-api.md:16, K0 api.md:21, K1 api.md:16. The idempotency-key and conflict examples are technique in all six skills.")

P("API-007",
  dims=["D1 unexpected failures propagate to centralized IExceptionHandler handling (default)",
        "D2 avoid repetitive catch/log/rethrow blocks"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each rule: M error-handling.md:22-27, M1 error-handling.md:34-41, L0 rules/1-architecture/outcomes.md:20 (+ aspnet-core.md:23 naming IExceptionHandler), L1 http-api.md:22, K0 rules/backend/error-handling.md:16, K1 api.md:21. The 'catch only to recover, translate, fall back, add context or clean up; never swallow' clause sits in the rule for M, M1, L0, K0 and in the aspnet-error-handling skill for L1 (:80) and K1 (:114); it is a related ban, not part of this default.")

P("API-008",
  dims=["D1 public API errors expose no stack traces, SQL, connection strings, internal paths, secrets or sensitive exception details"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT list in each rule: M error-handling.md:28-29, M1 error-handling.md:56-58 (also names raw exception messages, which the other five cover through API-002's 'clients must not depend on human-readable messages' or their anti-pattern lists), L0 rules/0-core/security-principles.md:57, L1 http-api.md:23, K0 error-handling.md:17, K1 api.md:22. swagger skills in all six keep the same details out of examples.")
