## 01 FG-M-8b2c02178e M CANONICAL_PLUS_DELTA/DEFAULT conf=MEDIUM sv=STRONGER res=None
CLAIM: Ordinary feature development must not introduce NgModules unless an integration or legacy dependency genuinely requires them (reported as a prohibition stronger than the standalone default).
  POL FE-001 [DEFAULT FULL] Use modern standalone Angular APIs for new code and organize application code primarily by feature.
  SRC .claude/rules/angular.md:17-20  - Use modern standalone Angular APIs for new code and organize application code / primarily by feature. Do not introduce NgModules for ordinary feature / development unless an integration or legacy dependency genuinely requires / them.

## 02 FG-M-3d4adb9bb8 M CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Prefer functional interceptors for new code; interceptors stay cross-cutting and never contain feature business logic.
  POL FE-008 [DEFAULT FULL] Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.
  SRC .claude/rules/angular.md:44-46  - Prefer functional interceptors for new code; keep interceptor / responsibilities cross-cutting and never put feature business logic in an / interceptor.

## 03 FG-M-9eb9149a91 M CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Prefer functional interceptors for new code; keep interceptor responsibilities cross-cutting and never put feature business logic in an interceptor.
  POL FE-008 [DEFAULT FULL] Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.
  SRC .claude/rules/angular.md:44-46  - Prefer functional interceptors for new code; keep interceptor / responsibilities cross-cutting and never put feature business logic in an / interceptor.
  SRC .claude/skills/angular/SKILL.md:120-120  Class-based interceptors need a reason.

## 04 FG-M-b3b041caea M CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Use ProblemDetails for non-validation HTTP failures and ValidationProblemDetails for request validation; keep machine-readable error contracts stable and safe; clients must not depend on human-readable messages.
  POL API-002 [DEFAULT FULL] Use ProblemDetails for non-validation HTTP failures and ValidationProblemDetails for request validation; keep machine-readable contracts stable and safe.
  SRC .claude/rules/error-handling.md:15-18  Use `ProblemDetails` for non-validation HTTP failures and / `ValidationProblemDetails` for request validation by default. Keep / machine-readable error contracts (stable error codes or contract fields) stable / and safe; clients must not depend on human-readable exception messages.
  SRC .claude/skills/aspnet-error-handling/SKILL.md:226-237  | Scenario | Default technique | / |---|---| / | Invalid HTTP input | Validation problem response | / | Simple query not found | `null` outcome; API maps to `404` | / | Multiple expected business outcomes | Typed outcome (Result only if adopted) | / | Unexpected exception | Global `IExceptionHandler` | / | API failure contract | `ProblemDetails` |
  SRC .claude/skills/aspnet-error-handling/SKILL.md:218-220  Avoid returning inconsistent anonymous error objects, coupling validation to / Minimal API endpoint filters in a Controller-based project, and putting business / rules only in request validators.

## 05 FG-M-46692dda34 M CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Configure the narrowest CORS policy satisfying actual browser clients; never combine credentials with unrestricted origins.
  POL SEC-009 [DEFAULT FULL] Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/rules/security.md:96-99  Configure CORS to the narrowest policy that satisfies the actual browser-client / requirements by default. Never combine credentialed cross-origin requests with / an unrestricted origin policy. A public unauthenticated API may legitimately / need a different policy than a private browser application.
  SRC .claude/skills/security-scan/references/scan-layers.md:189-194  CORS is a browser-origin policy, not an authorization mechanism. Check whether / configured origins match the actual browser-client model. Potential problems: / unnecessarily broad trusted origins, credentialed requests from untrusted / origins, environment-specific origins accidentally exposed in Production. / `AllowAnyOrigin()` can be valid for a genuinely public non-credentialed API, so / do not report a wildcard origin alone without considering the intended exposure.
  SRC .claude/skills/security-scan/SKILL.md:144-147  Conversely, do not automatically treat as safe: secrets in / `appsettings.Development.json`, sensitive values logged only at Debug level, / client-side Angular route guards, hidden UI buttons, or CORS configuration used / as a substitute for authorization.

## 06 FG-M-cbf3f9c7ca M EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Copy project/build dependency files before the full source for restore caching; update the copy section when structure changes; never trade correctness of the restored project graph for caching.
  SRC .claude/skills/docker/SKILL.md:67-70  Copy project and build dependency files before the full source tree so source / changes do not invalidate NuGet restore layers. Update the project-copy section / when the solution structure changes; do not optimize caching at the cost of a / Dockerfile that no longer restores the actual project graph.

## 07 FG-M-4c6848938a M EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Exclude non-build files from the Docker context (.git, bin, obj, node_modules, etc.); do not exclude tests the image build runs; never exclude files required by restore/build.
  SRC .claude/skills/docker/SKILL.md:138-138  Exclude files that do not belong in the build context:
  SRC .claude/skills/docker/SKILL.md:138-151  Exclude files that do not belong in the build context: /  / ```text / .git / .vs / **/bin / **/obj
  SRC .claude/skills/docker/SKILL.md:150-151  Do not exclude tests when the image build intentionally runs them, and never / exclude files required by restore/build.

## 08 FG-M-5554cb6a56 M EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Use 304 only for conditional requests whose cached representation is still valid; never as a generic 'nothing changed' business response.
  SRC .claude/skills/http-api/SKILL.md:87-89  Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) / when the client's cached representation is still valid. It carries no normal / representation and is not a generic "nothing changed" business response.

## 09 FG-M1-d578d58cec M1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: By default ProblemDetails for non-validation failures and ValidationProblemDetails for request validation; keep the machine-readable contract stable and safe and never make human-readable messages the contract.
  POL API-002 [DEFAULT FULL] Use ProblemDetails for non-validation HTTP failures and ValidationProblemDetails for request validation; keep machine-readable contracts stable and safe.
  SRC .claude/rules/error-handling.md:52-55  - By default use `ProblemDetails` for non-validation HTTP failures and / `ValidationProblemDetails` for request-validation failures; keep the / machine-readable error contract stable and safe, and do not make / human-readable exception messages the machine-readable contract.
  SRC .claude/skills/aspnet-error-handling/SKILL.md:200-206  Check-by-reference against `error-handling.md`: raw exception messages returned / to clients; inconsistent anonymous error objects; Application depending on HTTP / status codes; every method forced to return `Result<T>`; exceptions for every / negative branch; swallowed exceptions; catch/log/rethrow at every layer; / repeated logging; sensitive details in `ProblemDetails`; business rules only in / request validators; Minimal API endpoint filters used for validation in a / Controller-based project.
  SRC .claude/skills/aspnet-error-handling/SKILL.md:210-222  | Scenario | Default | / |---|---| / | Invalid HTTP input | Validation problem response | / | Simple query not found | Explicit Application outcome, often `null`; API maps to `404` | / | Multiple expected business outcomes | Consider typed outcome / Result | / | Unexpected exception | Global `IExceptionHandler` | / | API failure contract | `ProblemDetails` |

## 10 FG-M1-4041e9946d M1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: By default the narrowest CORS policy for actual browser clients; never credentialed requests with unrestricted origins.
  POL SEC-009 [DEFAULT FULL] Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/rules/security.md:91-94  By default configure CORS to the narrowest policy that satisfies the actual / browser-client requirements; a public unauthenticated API may legitimately / differ from a private browser application. Never combine credentialed / cross-origin requests with an unrestricted origin policy.
  SRC .claude/skills/security-scan/references/scan-layers.md:182-187  CORS is a browser-origin policy, not an authorization mechanism. Check whether / configured origins match the actual browser-client model: unnecessarily broad / trusted origins, credentialed requests from untrusted origins, environment / origins accidentally exposed in Production. `AllowAnyOrigin()` can be valid for / a genuinely public non-credentialed API; credentialed cross-origin access / requires restricted origins.
  SRC .claude/skills/security-scan/SKILL.md:137-139  Do not automatically treat as safe: secrets in `appsettings.Development.json`; / sensitive values logged only at Debug level; client-side route guards; hidden / UI buttons; CORS configuration used as a substitute for authorization.

## 11 FG-M1-d40a6d8879 M1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: Copy project/build-dependency files before full source; update the copy section with structure changes; never sacrifice restoring the real project graph for caching.
  SRC .claude/skills/docker/SKILL.md:62-65  Copy project and build-dependency files before the full source tree so source / changes do not invalidate NuGet restore layers. Update the project-copy section / when the solution structure changes; never optimize layer caching at the cost of / a Dockerfile that no longer restores the real project graph.

## 12 FG-M1-817d6aa28e M1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Configure the Testing environment with isolated resources so integration tests never reach development or production databases.
  POL TST-004 [MUST PARTIAL] Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.
  SRC .claude/skills/dotnet-testing/SKILL.md:135-139  Configure the `Testing` environment to use isolated test resources so an / integration test can never reach a development or production database. If / top-level statements make `Program` inaccessible, expose it for / `WebApplicationFactory`, for example with a `public partial class Program` / declaration.

## 13 FG-M1-43f86b8d6e M1 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: 304 only for conditional requests with a still-valid cached representation; never a generic business response.
  SRC .claude/skills/http-api/SKILL.md:87-89  Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) / when the client's cached representation is still valid. It carries no normal / representation and is not a generic "nothing changed" business response.

## 14 FG-M1-9c90b5afe5 M1 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: 429 for rate-limited requests with Retry-After when known; never represent validation failures as rate limiting.
  SRC .claude/skills/http-api/SKILL.md:182-184  Rate limiting rejected the request. Include `Retry-After` when the server knows / when another attempt is appropriate. Do not represent validation failure as / rate limiting.
  SRC .claude/skills/http-api/SKILL.md:180-184  ### 429 Too Many Requests /  / Rate limiting rejected the request. Include `Retry-After` when the server knows / when another attempt is appropriate. Do not represent validation failure as / rate limiting.

## 15 FG-M1-ea0ffa3ad3 M1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Repeated POSTs that must not duplicate effects may use an Idempotency-Key; key reuse with a different payload is 409; idempotency is not claimed merely because duplicates are unlikely.
  POL API-006 [MUST PARTIAL] Use 409 for valid requests conflicting with current state; use 412 when an explicit HTTP precondition such as If-Match fails.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  SRC .claude/skills/http-api/SKILL.md:214-221  ## Idempotency /  / `GET` is safe and idempotent, `PUT` is idempotent, `DELETE` is idempotent in / intended state semantics, `POST` is generally not idempotent. When a repeated / `POST` must not create duplicate effects, consider an `Idempotency-Key` header / whose key the server associates with the request and result; reusing a key with / a materially different payload is reasonably a `409`. Do not claim idempotency

## 16 FG-M1-10e0d3df19 M1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: Publication retries can duplicate delivery; use idempotent consumers/deduplication/outbox when required and never claim exactly-once because of retries.
  SRC .claude/skills/httpclient-factory/references/resilience.md:95-99  Retrying message publication requires understanding the broker and delivery / semantics; a retry may produce duplicate delivery. Use idempotent consumers, / broker-supported deduplication, outbox patterns, or similar mechanisms when the / business requirement needs them, and do not claim exactly-once delivery because / a retry policy exists.

## 17 FG-M1-e454380f27 M1 CANONICAL_ONLY/SHOULD_NOT conf=MEDIUM sv=SAME res=None
CLAIM: Swagger must not be used as a substitute for integration tests.
  POL TST-006 [DEFAULT PARTIAL] Use WebApplicationFactory-based integration testing when routing, binding, middleware, auth, DI, repositories, EF Core or database persistence is what the test must prove.
  POL TST-002 [DEFAULT PARTIAL] Choose the narrowest test level that meaningfully verifies the behavior; use integration tests when framework/persistence/HTTP wiring is the subject; no fixed unit/integration ratio is required.
  SRC .claude/skills/swagger/SKILL.md:127-130  Check-by-reference against `api.md` § Swagger: metadata that disagrees with / runtime responses; Swagger UI exposed publicly without a reason; Swagger used as / a substitute for integration tests; anonymous objects as long-lived API / contracts; a second competing documentation stack without a concrete need.

## 18 FG-L0-43aba8cb71 L0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Respect Retry-After or equivalent guidance where appropriate; never retry indefinitely or aggressively.
  POL RUN-017 [DEFAULT FULL] When a dependency supplies Retry-After or equivalent rate-limit guidance, respect it where appropriate and do not retry indefinitely or aggressively.
  SRC .claude/rules/0-core/runtime-principles.md:29-29  - When a dependency supplies `Retry-After` or equivalent rate-limit guidance, respect it where appropriate; do not retry indefinitely or aggressively (default).
  SRC .claude/skills/httpclient-factory/references/resilience.md:26-26  When a dependency returns `Retry-After`, let the retry policy honor it instead of an independent aggressive schedule.

## 19 FG-L0-e46fe0c51d L0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: CORS is the narrowest policy satisfying actual browser clients; never credentialed requests with unrestricted origins.
  POL SEC-009 [DEFAULT FULL] Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/rules/0-core/security-principles.md:48-48  - Configure CORS to the narrowest policy that satisfies the actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins (default).

## 20 FG-L0-935de5cafe L0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Test against the actual provider when provider behaviour matters; never claim provider fidelity from a different provider.
  POL TST-007 [DEFAULT FULL] Use the actual database provider when relational/provider behavior matters; Testcontainers is optional, and do not claim provider fidelity from a different provider.
  SRC .claude/rules/0-core/testing-principles.md:22-22  - When provider behavior matters, test against the actual database provider; never claim provider fidelity from a test that runs on a different provider (default).
  SRC .claude/skills/dotnet-testing/SKILL.md:135-135  Mocking every class; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing tests pass; Testcontainers without a fidelity need.
  SRC .claude/rules/2-technology/dotnet-testing.md:15-15  - EF Core InMemory is not a relational provider: never use it while claiming to verify relational or SQL Server behavior.

## 21 FG-L0-b82180d4f0 L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=SAME res=None
CLAIM: EF Core InMemory is not relational and never verifies relational or SQL Server behavior.
  POL TST-007 [DEFAULT PARTIAL] Use the actual database provider when relational/provider behavior matters; Testcontainers is optional, and do not claim provider fidelity from a different provider.
  SRC .claude/rules/0-core/testing-principles.md:22-22  - When provider behavior matters, test against the actual database provider; never claim provider fidelity from a test that runs on a different provider (default).
  SRC .claude/skills/dotnet-testing/SKILL.md:135-135  Mocking every class; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing tests pass; Testcontainers without a fidelity need.
  SRC .claude/rules/2-technology/dotnet-testing.md:15-15  - EF Core InMemory is not a relational provider: never use it while claiming to verify relational or SQL Server behavior.

## 22 FG-L0-cb59306d5a L0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Prefer functional interceptors for new code, cross-cutting only; never feature business logic in an interceptor.
  POL FE-008 [DEFAULT FULL] Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.
  SRC .claude/rules/2-technology/angular.md:16-16  - Prefer functional HTTP interceptors for new code and keep interceptor responsibilities cross-cutting; never put feature business logic in an interceptor (default).

## 23 FG-L0-6c42674c92 L0 CANONICAL_PLUS_DELTA/DEFAULT conf=MEDIUM sv=SAME res=None
CLAIM: Physical layout: backend production and test projects under backend/<Name>.<Layer>/, the Angular workspace under frontend/<Name>.Web/ (unit and component tests inside the workspace, E2E under frontend/<Name>.Web/e2e/, never under backend/), maintained documentation under docs/; keep them separated and create no top-level tests/ directory.
  POL DEP-024 [DEFAULT PARTIAL] Keep backend production/test projects, frontend workspace, and documentation clearly separated according to the template's approved layout; do not create a separate top-level tests directory.
  SRC .claude/rules/3-project/decisions.md:49-49  - Physical layout: backend production and test projects under `backend/<Name>.<Layer>/`, the Angular workspace under `frontend/<Name>.Web/`, maintained documentation under `docs/`. Keep them clearly separated and do not create a separate top-level `tests/` directory. Project mapping: `layout.md`.
  SRC .claude/rules/3-project/layout.md:27-27  Create only useful test projects, beside the production projects under `backend/`. Typical narrowest references:
  SRC .claude/rules/3-project/layout.md:38-38  The Angular workspace lives at `frontend/<Name>.Web/` and owns its `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/`, and `public/`. Unit and component tests stay inside the workspace (colocated by Angular convention); E2E tests, when adopted, live in `frontend/<Name>.Web/e2e/`. Never place frontend tests under `backend/`.

## 24 FG-L0-8fdc2119a4 L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: HybridCache is optional; add a distributed backend such as Redis only when deployment requires it, never merely because the application caches.
  POL GOV-013 [MUST_NOT PARTIAL] Do not introduce frameworks, libraries, infrastructure, or architectural patterns without a concrete current need.
  SRC .claude/skills/caching/SKILL.md:22-22  A strong option for local in-memory caching with optional distributed L2, stampede protection, and cache-aside behavior; not mandatory for every project. Add a distributed backend such as Redis only when deployment requires it.
  SRC .claude/skills/caching/SKILL.md:80-80  Caching EF tracked entities across Unit of Work boundaries; Redis added merely because the application caches.

## 25 FG-L0-ffb2b22b51 L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=SAME res=None
CLAIM: Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
  POL RUN-022 [DEFAULT PARTIAL] Prefer strongly typed options for structured service configuration and validate settings at startup when missing/invalid values prevent correct or secure operation; avoid scattering string-based IConfiguration lookups.
  SRC .claude/skills/configuration/SKILL.md:14-14  Direct `IConfiguration` access is normal in `Program.cs`, configuration-provider setup, and infrastructure registration; the problem is ordinary services parsing configuration keys.

## 26 FG-L0-96fb099860 L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Configure the Testing environment so it can never reach a Development or Production database.
  POL TST-004 [MUST PARTIAL] Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.
  SRC .claude/skills/dotnet-testing/SKILL.md:92-92  This exercises routing, binding, serialization, middleware, auth wiring, DI, Application services, repositories, EF Core, and persistence. Configure the `Testing` environment so it can never reach a Development or Production database. If top-level statements hide `Program`, add `public partial class Program;`.

## 27 FG-L0-c3af8cbd51 L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=SAME res=CR
CLAIM: 204 fits a successful DELETE or an update whose representation adds no value; never with a body.
  POL API-003 [MUST PARTIAL] Choose 200/201/202/204 according to actual HTTP semantics; do not return 200 for every outcome, 201 merely for an internal row insert, or 202 for already-completed work.
  SRC .claude/skills/http-api/SKILL.md:31-31  - 204 fits a successful `DELETE` or an update whose representation adds no value. For repeated `DELETE` of an absent resource choose one convention — 204 (desired state holds) or 404 (resource absent) — and use it consistently across equivalent resources.

## 28 FG-L0-8e69addc81 L0 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: 429 with Retry-After when known for rate-limited requests; never for validation failures.
  SRC .claude/skills/http-api/SKILL.md:44-44  | Rate limiting rejected the request | `429` + `Retry-After` when known (never for validation failures) |

## 29 FG-L0-958d10ac79 L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: 409 for uniqueness duplicates, incompatible state transitions, conflicting concurrent operations and reused idempotency keys; never for malformed syntax.
  POL API-006 [MUST PARTIAL] Use 409 for valid requests conflicting with current state; use 412 when an explicit HTTP precondition such as If-Match fails.
  SRC .claude/skills/http-api/SKILL.md:56-56  Typical 409 cases: a duplicate where uniqueness is part of resource state; a state transition incompatible with the current state (order already completed + cancel request); a conflicting concurrent operation; an idempotency key reused with a different payload. 409 is never for malformed syntax.

## 30 FG-L0-fe665ffb2e L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: When a repeated POST must not duplicate effects consider an Idempotency-Key associated with request and result; a reused key with a materially different payload returns 409.
  POL API-006 [MUST PARTIAL] Use 409 for valid requests conflicting with current state; use 412 when an explicit HTTP precondition such as If-Match fails.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  SRC .claude/skills/http-api/SKILL.md:60-60  `GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state; `POST` generally is not. When a repeated `POST` must not duplicate effects, consider an `Idempotency-Key` that the server associates with the request and its result; a reused key with a materially different payload → `409`. Do not claim idempotency merely because duplicates are unlikely.

## 31 FG-L0-08f3f22030 L0 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Transient candidates: selected network failures, temporary unavailability, rate limiting when allowed, transient provider database failures; never retry validation errors, auth failures, permanent 404s or deterministic business rejections.
  SRC .claude/skills/httpclient-factory/references/resilience.md:22-22  Plausibly transient: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Not retried: validation errors, authentication/authorization failures, permanent 404 outcomes, deterministic business rejections, non-idempotent operations without duplicate prevention.

## 32 FG-L0-d98980588e L0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Determine real responses from the whole pipeline; document 201 only when it is the runtime contract and never 204 for an endpoint returning a body; describe ProblemDetails contracts where useful.
  POL API-016 [MUST PARTIAL] Swagger/OpenAPI metadata must describe the API that actually runs, including routes, important response statuses, schemas, and authentication behavior; do not document speculative responses.
  POL API-003 [MUST PARTIAL] Choose 200/201/202/204 according to actual HTTP semantics; do not return 200 for every outcome, 201 merely for an internal row insert, or 202 for already-completed work.
  SRC .claude/skills/swagger/SKILL.md:56-56  When determining real responses consider the whole pipeline — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit branches in the action. Document `201 Created` (with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists) only when that is the runtime contract; never `204` for an endpoint that returns a body. Describe ProblemDetails/ValidationProblemDetails contracts where useful; examples and descriptions never show exception types, stack traces, SQL, connection strings, or paths.

## 33 FG-L1-d3d7aff321 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Respect Retry-After or equivalent guidance; never retry indefinitely or aggressively.
  POL RUN-017 [DEFAULT FULL] When a dependency supplies Retry-After or equivalent rate-limit guidance, respect it where appropriate and do not retry indefinitely or aggressively.
  SRC .claude/rules/0-core/backend-code.md:27-27  - Default: respect `Retry-After` or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively.
  SRC .claude/skills/httpclient-factory/references/resilience.md:40-48  | Scenario | Consider | / | --- | --- | / | External I/O | bounded execution time | / | Safe transient HTTP failure | retry | / | Unsafe write | no retry unless duplicate-safe | / | `429` from dependency | honor `Retry-After` | / | Repeated dependency outage | circuit breaker |
  SRC .claude/skills/httpclient-factory/references/resilience.md:20-20  - **Retry-After** — prefer the server's guidance when the policy supports it instead of an independent aggressive schedule.

## 34 FG-L1-d3d5128af8 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Narrowest CORS policy for actual browser clients; never credentialed requests with unrestricted origins.
  POL SEC-009 [DEFAULT FULL] Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/rules/0-core/security.md:34-34  - Default: configure CORS as the narrowest policy satisfying actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.

## 35 FG-L1-b81a052976 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Security-sensitive checks fail safely; never silently convert lookup/configuration failures into success.
  POL SEC-013 [DEFAULT FULL] Security-sensitive authorization, permission, or required-control checks should fail safely rather than silently convert lookup/configuration failures into success.
  SRC .claude/rules/0-core/security.md:44-44  - Default: security-sensitive authorization, permission, and required-control checks fail safely; never silently convert a lookup or configuration failure into success.
  SRC .claude/skills/security-scan/references/scan-layers.md:58-58  - **Swallowed exceptions** — empty `catch (Exception) { }` or broad catches without deliberate fallback; security-relevant failures must not silently become success.

## 36 FG-L1-7799d8e5a3 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Actual provider when relational/provider behaviour matters (real-provider containers optional); never claim fidelity from a different provider.
  POL TST-007 [DEFAULT FULL] Use the actual database provider when relational/provider behavior matters; Testcontainers is optional, and do not claim provider fidelity from a different provider.
  SRC .claude/rules/0-core/testing.md:15-15  - Default: use the actual database provider when relational or provider behavior matters (an isolated real-provider container is optional, not required); never claim provider fidelity from a test that runs on a different provider.
  SRC .claude/skills/ci-cd/SKILL.md:73-73  Provide external services in CI only when tests require them, matching the selected database provider; keep the environment isolated from Development and Production data (backend test rules).
  SRC .claude/skills/dotnet-testing/SKILL.md:132-132  Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing pass; real-provider containers when fidelity is irrelevant; in-memory providers claimed as relational coverage; keeping temporary probes as permanent tests without review.

## 37 FG-L1-af402598cd L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Prefer functional interceptors for new code; cross-cutting only; never feature business logic.
  POL FE-008 [DEFAULT FULL] Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.
  SRC .claude/rules/2-technology/frontend/framework.md:12-12  - Default: prefer functional interceptors for new code; keep interceptor responsibilities cross-cutting and never put feature business logic in an interceptor.
  SRC .claude/skills/angular/SKILL.md:114-114  New NgModules without a reason; HTTP calls scattered through components; global service folders of unrelated feature services; state frameworks by default; unmanaged manual subscriptions; business logic in interceptors; frontend-only authorization; parsing human-readable backend error strings; giant `shared` directories; converting every Observable to a Signal; choosing Signals or RxJS because one is newer.
  SRC .claude/skills/angular/SKILL.md:69-69  Prefer functional interceptors; add a class-based one only with a reason. When backend errors use `ProblemDetails`, centralize parsing/mapping (for example in an error interceptor plus a small mapping helper).

## 38 FG-L1-5b3d19f6e1 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Keep backend projects (backend/<Name>.<Layer>/), frontend workspace (frontend/<Name>.Web/) and docs/ separated; never a separate top-level tests directory.
  POL DEP-024 [DEFAULT FULL] Keep backend production/test projects, frontend workspace, and documentation clearly separated according to the template's approved layout; do not create a separate top-level tests directory.
  SRC .claude/rules/3-project/decisions.md:23-23  - Default: keep backend production and test projects (`backend/<Name>.<Layer>/`), the frontend workspace (`frontend/<Name>.Web/`), and documentation (`docs/`) clearly separated as approved; never create a separate top-level tests directory.

## 39 FG-L1-0df90c10a3 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Direct IConfiguration access is normal in the composition root, provider setup and infrastructure registration; ordinary services must not parse keys.
  POL RUN-022 [DEFAULT PARTIAL] Prefer strongly typed options for structured service configuration and validate settings at startup when missing/invalid values prevent correct or secure operation; avoid scattering string-based IConfiguration lookups.
  SRC .claude/skills/configuration/SKILL.md:10-10  Rules: typed-options rule (`.claude/rules/0-core/backend-code.md`), secrets and fail-visibly rules (`.claude/rules/0-core/security.md`). Direct `IConfiguration` access is normal in the composition root, configuration-provider setup, and infrastructure registration; the problem is ordinary services parsing keys.

## 40 FG-L1-006f30678e L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=WEAKER res=GR
CLAIM: Configure the Testing environment with isolated resources so tests never reach a Development or Production database.
  POL TST-004 [MUST PARTIAL] Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.
  SRC .claude/skills/dotnet-testing/SKILL.md:102-102  Covers routing, binding, serialization, middleware, auth wiring, DI, use-case units, repositories, and persistence. Configure the `Testing` environment with isolated resources so a test can never reach a Development or Production database. If top-level statements hide `Program`, add `public partial class Program;`.

## 41 FG-L1-2fcae61e4c L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=WEAKER res=GR
CLAIM: Host integration tests configure the Testing environment with isolated resources so they never reach a Development or Production database, exposing Program to the factory where needed.
  POL TST-004 [MUST PARTIAL] Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.
  SRC .claude/skills/dotnet-testing/SKILL.md:102-102  Covers routing, binding, serialization, middleware, auth wiring, DI, use-case units, repositories, and persistence. Configure the `Testing` environment with isolated resources so a test can never reach a Development or Production database. If top-level statements hide `Program`, add `public partial class Program;`.

## 42 FG-L1-17563c1d71 L1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Include only dependencies required for meaningful readiness; keep readiness unhealthy until required asynchronous startup completes; never misuse liveness for that.
  POL API-019 [MUST PARTIAL] Liveness should normally avoid external dependencies that could cause restart loops; readiness may depend on capabilities required to serve traffic and should reflect startup/dependency availability appropriately.
  SRC .claude/skills/health-check/SKILL.md:41-41  Include only dependencies required for meaningful readiness; an optional external service need not make the whole application unready. Keep readiness unhealthy until required asynchronous startup work completes — never misuse liveness for that (restart loops).

## 43 FG-L1-ba40759ad1 L1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Keep readiness unhealthy until required asynchronous startup work completes; liveness never represents that startup state.
  POL API-019 [MUST PARTIAL] Liveness should normally avoid external dependencies that could cause restart loops; readiness may depend on capabilities required to serve traffic and should reflect startup/dependency availability appropriately.
  SRC .claude/skills/health-check/SKILL.md:41-41  Include only dependencies required for meaningful readiness; an optional external service need not make the whole application unready. Keep readiness unhealthy until required asynchronous startup work completes — never misuse liveness for that (restart loops).

## 44 FG-L1-c619ceab7d L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=WEAKER res=GR
CLAIM: 204 for success with no body; a 204 never carries a body.
  POL API-003 [MUST PARTIAL] Choose 200/201/202/204 according to actual HTTP semantics; do not return 200 for every outcome, 201 merely for an internal row insert, or 202 for already-completed work.
  SRC .claude/skills/http-api/SKILL.md:22-22  - **204 No Content** — success with no body (`DELETE`, updates where returning the representation adds nothing); a `204` never carries a body. Choose one convention for repeated `DELETE` of an absent resource — `204` (final state holds) or `404` (resource absent) — and apply it consistently across equivalent resources.

## 45 FG-L1-5f5febf5c6 L1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: 304 only for conditional requests with a still-valid cached representation; never a generic 'nothing changed' business response.
  SRC .claude/skills/http-api/SKILL.md:23-23  - **304 Not Modified** — only for conditional requests (`If-None-Match`/ETag, `If-Modified-Since`) when the cached representation is still valid; never a generic "nothing changed" business response.

## 46 FG-L1-0950048568 L1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: 400 when the request itself is invalid (malformed JSON, shape, binding, formatting, missing transport input); never for authentication failure.
  POL API-010 [MUST PARTIAL] Use FluentValidation for explicit request/use-case validation where appropriate; keep transport validation, Application rules and Domain invariants at their owning boundaries.
  POL API-005 [MUST PARTIAL] Use 401 when authentication is missing/failed and 403 when an authenticated principal is not permitted; deliberate 404 hiding requires a consistent security policy.
  SRC .claude/skills/http-api/SKILL.md:27-27  - **400 Bad Request** — the request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` handles many of these automatically. Never use `400` for authentication failure.

## 47 FG-L1-cc71eb4b32 L1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: 429 for rate-limited requests with Retry-After when known; never for validation failures.
  SRC .claude/skills/http-api/SKILL.md:35-35  - **429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when known. Never use it for validation failures.

## 48 FG-L1-7edf640541 L1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: For a POST that must not duplicate effects consider an Idempotency-Key stored with request/result per the contract.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  SRC .claude/skills/http-api/SKILL.md:46-46  `GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended final state; `POST` generally is not. For a `POST` that must not create duplicate effects, consider an `Idempotency-Key` stored with the request/result per the contract; claim idempotency only when it is implemented.

## 49 FG-L1-56b4faff0f L1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Hedge only operations safe to run several times (typically idempotent reads); never writes by default.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  SRC .claude/skills/httpclient-factory/references/resilience.md:23-23  - **Hedging** — parallel or delayed duplicate attempts, only for operations safe to run several times (typically idempotent reads against interchangeable endpoints); never writes by default.

## 50 FG-L1-d9e53ef77a L1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: Publication retries can duplicate delivery; use idempotent consumers, deduplication or an outbox when needed; never claim exactly-once because a retry exists.
  SRC .claude/skills/httpclient-factory/references/resilience.md:32-32  Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication, or an outbox when the business needs it, and never claim exactly-once delivery because a retry exists.

## 51 FG-L1-695833d819 L1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Use a feature when it makes code clearer, safer or simpler, never to demonstrate newer syntax; consistency and readability beat maximal feature use.
  POL RUN-009 [DEFAULT PARTIAL] Follow repository conventions and .editorconfig; use modern C# when it improves clarity, but do not mechanically modernize working code.
  SRC .claude/skills/modern-csharp/SKILL.md:10-10  Rules: C# convention and scope rules (`.claude/rules/0-core/backend-code.md` § C# conventions); repository `.editorconfig`. Use a feature when it makes code clearer, safer, or simpler — never to demonstrate newer syntax. Consistency and readability beat maximal feature use.

## 52 FG-L1-affc5ed062 L1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Consider the whole pipeline when listing responses; never 201 for a 200 endpoint or 204 for one returning a body; describe ProblemDetails contracts where useful.
  POL API-016 [MUST PARTIAL] Swagger/OpenAPI metadata must describe the API that actually runs, including routes, important response statuses, schemas, and authentication behavior; do not document speculative responses.
  POL API-003 [MUST PARTIAL] Choose 200/201/202/204 according to actual HTTP semantics; do not return 200 for every outcome, 201 merely for an internal row insert, or 202 for already-completed work.
  SRC .claude/skills/swagger/SKILL.md:48-48  Consider the whole pipeline when listing responses — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit action branches. Document `201` with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists; never `201` for an endpoint returning `200` or `204` for one returning a body. Describe `ProblemDetails`/`ValidationProblemDetails` where useful, without internal exception types, stack traces, SQL, connection strings, or paths in examples.

## 53 FG-K0-7e828bca09 K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Use the actual provider when relational/provider behaviour matters (Testcontainers optional); never claim provider fidelity from a different provider such as EF Core InMemory.
  POL TST-007 [DEFAULT FULL] Use the actual database provider when relational/provider behavior matters; Testcontainers is optional, and do not claim provider fidelity from a different provider.
  SRC .claude/rules/backend-tests/testing.md:30-30  - Default: use the actual database provider when relational or provider behavior matters (Testcontainers is optional). Never claim provider fidelity from a different provider, including EF Core InMemory.
  SRC .claude/skills/dotnet-testing/SKILL.md:181-192  | Scenario | Approach | / |---|---| / | Pure business rule | NUnit unit test | / | Application orchestration | Unit test with controlled boundary doubles when useful | / | Full API pipeline | `WebApplicationFactory<Program>` | / | Important EF/provider behavior | Integration test with the actual provider | / | Simple API integration, provider irrelevant | Lightweight isolated relational test DB may suffice |
  SRC .claude/skills/dotnet-testing/SKILL.md:121-121  Provider fidelity matters for provider-specific SQL, constraints, transactions, locking and concurrency, indexes, raw SQL, provider-specific mappings and migrations — use the actual provider; Testcontainers is a good option for an isolated real database. When provider fidelity does not matter (primarily application/API integration), a lighter isolated relational database may be acceptable — state the trade-off. EF Core InMemory is not a relational substitute; for a true unit test a fake repository is often clearer.

## 54 FG-K0-0b760dcf90 K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and staleness requirements, never merely because a value is read often.
  POL RUN-007 [DEFAULT FULL] Caching is not a default architecture requirement; introduce it only for a clear measured/reasoned need and choose implementation according to deployment, consistency and staleness requirements.
  SRC .claude/rules/backend/caching.md:12-12  - Default: caching is an optimization, not an architecture requirement. Introduce it only for a clear measured or reasoned need — expensive repeated work, high read volume, expensive remote calls with acceptable staleness — and choose the implementation by deployment, consistency and staleness requirements, never merely because a value is read often.
  SRC .claude/skills/caching/SKILL.md:12-12  Define consistency semantics first — how stale data may become and how it is invalidated — and measure before adding caching purely for performance.
  SRC .claude/skills/caching/SKILL.md:101-108  | Need | Consideration | / |---|---| / | Entire reusable HTTP response | ASP.NET Core output caching | / | Local application cache | In-memory or HybridCache | / | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) | / | Expensive repeated remote read | Cache in Infrastructure when the contract permits | / | Application-controlled invalidation | Application abstraction + Infrastructure implementation |

## 55 FG-K0-5b5c4399c8 K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Follow existing conventions and .editorconfig; modern C# when it improves clarity, never mechanical modernization.
  POL RUN-009 [DEFAULT FULL] Follow repository conventions and .editorconfig; use modern C# when it improves clarity, but do not mechanically modernize working code.
  SRC .claude/rules/backend/csharp.md:16-16  - Default: follow the repository's existing conventions and `.editorconfig`; use modern C# when it improves clarity, but do not mechanically modernize working code. Consistency and readability matter more than using every language feature.

## 56 FG-K0-a780dcbe8d K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Respect Retry-After or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively.
  POL RUN-017 [DEFAULT FULL] When a dependency supplies Retry-After or equivalent rate-limit guidance, respect it where appropriate and do not retry indefinitely or aggressively.
  SRC .claude/rules/backend/integrations.md:16-16  - Default: when a dependency supplies `Retry-After` or equivalent rate-limit guidance, respect it where appropriate, and never retry indefinitely or aggressively.
  SRC .claude/skills/httpclient-factory/references/resilience.md:69-79  | Scenario | Consideration | / |---|---| / | External I/O | Bounded execution time | / | Safe transient HTTP failure | Consider retry | / | Unsafe write | No retry unless duplicate-safe | / | `429` from dependency | Honor `Retry-After` where appropriate | / | Repeated dependency outage | Consider circuit breaker |
  SRC .claude/skills/httpclient-factory/references/resilience.md:33-33  Prefer the server's retry guidance when the policy supports it instead of an independent aggressive schedule against a rate-limited dependency.

## 57 FG-K0-375972cdb2 K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Narrowest CORS policy satisfying actual browser clients; never credentialed cross-origin requests with an unrestricted origin policy.
  POL SEC-009 [DEFAULT FULL] Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/rules/backend/security.md:32-32  - Default: the narrowest CORS policy that satisfies the actual browser-client requirements. Never combine credentialed cross-origin requests with an unrestricted origin policy.
  SRC .claude/skills/security-scan/references/scan-layers.md:117-117  Rules: `rules/backend/security.md` § CORS. CORS is a browser-origin policy, not authorization. Look for unnecessarily broad trusted origins, credentialed requests from untrusted origins and environment-specific origins exposed in Production. `AllowAnyOrigin()` can be valid for a genuinely public, non-credentialed API; consider intended exposure before reporting a wildcard.
  SRC .claude/skills/security-scan/SKILL.md:78-78  Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug level; Angular route guards; hidden UI buttons; CORS used as a substitute for authorization.

## 58 FG-K0-423d455e8b K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Functional interceptors for new code, limited to cross-cutting concerns; never feature business logic in interceptors.
  POL FE-008 [DEFAULT FULL] Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.
  SRC .claude/rules/frontend/angular.md:26-26  - Default: functional interceptors for new code, limited to cross-cutting concerns; never put feature business logic in an interceptor.
  SRC .claude/skills/angular/SKILL.md:150-150  New NgModules without a reason; HTTP calls throughout components; global service folders of unrelated feature services; state frameworks by default; manual subscriptions without lifecycle handling; business logic in interceptors; frontend-only authorization; parsing human-readable backend error strings; giant `shared` directories; converting every Observable to a Signal; choosing Signals or RxJS because one is newer.

## 59 FG-K0-cad27bd55a K0 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: When Controller API versioning has been explicitly adopted use the Asp.Versioning Controller integration (e.g. Asp.Versioning.Mvc with ApiExplorer); never before adoption.
  POL DEP-017 [DEFAULT FULL] When Controller API versioning is explicitly adopted, use the Controller integration of Asp.Versioning; do not add the package before the project actually adopts versioning.
  SRC .claude/skills/add-dependency/SKILL.md:21-21  - **API versioning** — when Controller API versioning has been explicitly adopted (D-15), use the Controller integration of `Asp.Versioning` (for example `Asp.Versioning.Mvc` with `Asp.Versioning.Mvc.ApiExplorer`); do not add it before the project actually adopts versioning.

## 60 FG-K0-fc38775ad7 K0 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: Unit-test candidates: domain behaviour owned by Domain, calculations, state transitions, validation, Application orchestration with simple fakes; mock architectural boundaries when it clarifies, never every collaborator mechanically, and do not forbid mocking project-owned abstractions.
  SRC .claude/skills/dotnet-testing/SKILL.md:64-64  Good candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, Application orchestration with simple fakes or mocks. Mock or fake architectural boundaries when that clarifies the behavior; do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation helps.
  SRC .claude/skills/dotnet-testing/SKILL.md:177-177  Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing-sensitive tests pass; Testcontainers without a provider-fidelity need; EF InMemory while claiming relational coverage.

## 61 FG-K0-471485d7d2 K0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: GET safe and idempotent, PUT idempotent, DELETE idempotent in intended state, POST generally not; consider an Idempotency-Key for POSTs that must not duplicate effects (reuse with a different payload → 409); unlikely duplicates do not make an operation idempotent.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  POL API-006 [MUST PARTIAL] Use 409 for valid requests conflicting with current state; use 412 when an explicit HTTP precondition such as If-Match fails.
  SRC .claude/skills/http-api/SKILL.md:86-86  `GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state; `POST` generally is not. When a repeated `POST` should not create duplicate effects, consider an `Idempotency-Key` that the server associates with the request and result; reuse of a key with a materially different payload is reasonably `409`. Duplicate requests being unlikely does not make an operation idempotent.

## 62 FG-K0-71837faed7 K0 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Delegating handlers serve genuine HTTP pipeline concerns (authorization headers, correlation, signing), never business decisions.
  SRC .claude/skills/httpclient-factory/SKILL.md:59-59  For genuine HTTP pipeline concerns — authorization header acquisition, correlation/context propagation, request signing — not business decisions:

## 63 FG-K0-50cf5b293c K0 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Stable headers on the client, per-request values (dynamic tokens) on the request or via a handler, never by concurrently mutating shared DefaultRequestHeaders.
  SRC .claude/skills/httpclient-factory/SKILL.md:115-115  Stable headers (media types) can be configured on the client; per-request values such as dynamic access tokens go on the request or through a handler — mutating shared `DefaultRequestHeaders` concurrently for request-specific values is a race. Prefer `System.Net.Http.Json`/`System.Text.Json`, with explicit serializer options when the remote contract differs from the application's defaults. Internal Domain entities are not remote API contracts.
  SRC .claude/skills/httpclient-factory/SKILL.md:132-132  New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them.

## 64 FG-K0-c37a23e0b6 K0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Hedging only for operations safe to execute multiple times (typically idempotent reads against interchangeable endpoints), never writes.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  SRC .claude/skills/httpclient-factory/references/resilience.md:45-45  Hedging sends parallel or delayed duplicate attempts; use it only for operations safe to execute multiple times, typically idempotent reads against interchangeable endpoints — not writes.
  SRC .claude/skills/httpclient-factory/references/resilience.md:71-79  | External I/O | Bounded execution time | / | Safe transient HTTP failure | Consider retry | / | Unsafe write | No retry unless duplicate-safe | / | `429` from dependency | Honor `Retry-After` where appropriate | / | Repeated dependency outage | Consider circuit breaker | / | Optional data unavailable | Consider explicit fallback | / | Latency-sensitive idempotent read | Consider hedging after measurement |

## 65 FG-K0-3e5746d904 K0 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Keep authorization headers and full request/response bodies out of logs (never-log data is owned by the security standard).
  POL RUN-014 [MUST_NOT PARTIAL] Do not serialize arbitrary request bodies, domain objects, or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
  POL SEC-010 [MUST_NOT PARTIAL] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without a concrete permitted operational need.
  SRC .claude/skills/logging/SKILL.md:65-65  Never-log data is defined in `rules/common/security.md`; in practice also keep authorization headers and full request/response bodies out of logs.

## 66 FG-K1-a42b272113 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Actual database provider when relational/provider behaviour matters (Testcontainers optional); never claim provider fidelity from a different provider.
  POL TST-007 [DEFAULT FULL] Use the actual database provider when relational/provider behavior matters; Testcontainers is optional, and do not claim provider fidelity from a different provider.
  SRC .claude/rules/backend-tests/testing.md:17-17  - Default: the actual database provider when relational or provider behavior matters (Testcontainers is optional); never claim provider fidelity from a test that runs against a different provider.
  SRC .claude/skills/dotnet-testing/SKILL.md:105-105  Choose the database strategy by what the test must prove (provider fidelity vs. application/API integration) and be explicit about the trade-off. Start from a known state with a simple strategy: recreate or reset the isolated database, use transactions when their semantics fit, seed only the data the test needs, use unique identifiers to avoid collisions. Never modify production data.
  SRC .claude/skills/ef-core/SKILL.md:225-225  - The EF Core InMemory provider is not a relational database: never use it to claim relational behavior (constraints, transactions, collation, SQL translation). A fake repository is often clearer for a true unit test.

## 67 FG-K1-e0ec24eec3 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Respect Retry-After or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively.
  POL RUN-017 [DEFAULT FULL] When a dependency supplies Retry-After or equivalent rate-limit guidance, respect it where appropriate and do not retry indefinitely or aggressively.
  SRC .claude/rules/backend/runtime.md:30-30  - Default: respect `Retry-After` or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively.
  SRC .claude/skills/httpclient-factory/SKILL.md:99-99  Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior.
  SRC .claude/skills/httpclient-factory/references/resilience.md:26-26  When a dependency returns `Retry-After`, prefer respecting it when the policy supports it; never hammer a rate-limited dependency with an independent aggressive schedule.

## 68 FG-K1-1741d36123 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Narrowest CORS policy for actual browser clients (a public unauthenticated API may differ); never credentialed cross-origin requests with unrestricted origins.
  POL SEC-009 [DEFAULT FULL] Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/rules/backend/security.md:23-23  - Default: CORS is the narrowest policy that satisfies actual browser-client requirements (a public unauthenticated API may legitimately differ from a private browser application); never combine credentialed cross-origin requests with unrestricted origins.
  SRC .claude/skills/security-scan/references/scan-layers.md:107-107  CORS is a browser-origin policy, not an authorization mechanism. Review whether configured origins match the actual browser-client model; potential problems are unnecessarily broad trusted origins, credentialed requests from untrusted origins, and environment-specific origins exposed in Production. `AllowAnyOrigin()` can be valid for a genuinely public non-credentialed API; do not report a wildcard origin without considering intended exposure. Credentialed cross-origin access requires restricted origins.
  SRC .claude/skills/security-scan/SKILL.md:82-82  Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug level; client-side route guards; hidden UI buttons; CORS used as a substitute for authorization.

## 69 FG-K1-b030eec95c K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Security-sensitive authorization, permission and required-control checks fail safely; never silently convert a lookup or configuration failure into success.
  POL SEC-013 [DEFAULT FULL] Security-sensitive authorization, permission, or required-control checks should fail safely rather than silently convert lookup/configuration failures into success.
  SRC .claude/rules/common/security.md:32-32  - Default: security-sensitive authorization, permission, and required-control checks fail safely; never silently convert a lookup or configuration failure into success.
  SRC .claude/skills/security-scan/references/scan-layers.md:147-147  Investigate code that catches an exception and then lets a privileged operation continue: authorization service failed → allow; token validation failed → continue as anonymous but perform a privileged action; permission lookup failed → default to permitted. Security-sensitive checks fail safely.
  SRC .claude/skills/security-scan/references/scan-layers.md:151-151  Review empty `catch (Exception) { }` blocks and broad catches that continue without a deliberate fallback. Not every swallowed exception is a vulnerability, but security-relevant failures must not silently turn into success.

## 70 FG-K1-455f584b69 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Functional HTTP interceptors for new code; interceptors stay cross-cutting and never contain feature business logic.
  POL FE-008 [DEFAULT FULL] Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.
  SRC .claude/rules/frontend/frontend-framework.md:12-12  - Default: functional HTTP interceptors for new code. Interceptors stay cross-cutting and never contain feature business logic.
  SRC .claude/skills/angular/SKILL.md:88-88  Do not introduce class-based interceptors without a reason.
  SRC .claude/skills/angular/SKILL.md:145-145  Avoid NgModules without a reason, global service folders containing unrelated feature services, state frameworks by default, complex business logic in interceptors, giant `shared` directories, and converting every Observable to a Signal.

## 71 FG-K1-44c62bf76d K1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Deprecation is a migration process: mark it (Deprecated = true with ReportApiVersions), document the replacement, the migration period and the removal timing; never remove deprecated versions silently.
  POL API-022 [MUST PARTIAL] When deprecating an externally consumed API version, mark the deprecation in versioning metadata, document the replacement, communicate a realistic migration/removal timeline, and keep the old version working for the promised support period; do not remove it without considering the published support contract.
  SRC .claude/skills/api-versioning/SKILL.md:72-72  Deprecation is a migration process, not merely an attribute: `[ApiVersion("1.0", Deprecated = true)]` with `ReportApiVersions` advertises it; document the replacement, the migration period, and the removal timing (procedure: `development-workflow`).
  SRC .claude/skills/api-versioning/SKILL.md:84-84  Minimal API version-group examples in a Controller-based project, a new version for every implementation change, silently removing deprecated versions.

## 72 FG-K1-27ec97e6b7 K1 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Copy only repository-level build files that exist and restore needs; copy project files explicitly (no flattening wildcards) and update the section when the solution changes; never trade a correct restore graph for layer caching.
  SRC .claude/skills/docker/SKILL.md:46-46  Copy only repository-level build files that exist and are needed for restore; never add them just to satisfy the example. Copy project files explicitly — no wildcard tricks that flatten or rearrange the multi-project structure — and update this section when the solution structure changes. Never optimize layer caching at the cost of restoring the wrong project graph.

## 73 FG-K1-b52915cf19 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=WEAKER res=GR
CLAIM: Configure the Testing environment with isolated test resources so integration tests can never reach a Development or Production database.
  POL TST-004 [MUST PARTIAL] Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.
  SRC .claude/skills/dotnet-testing/SKILL.md:101-101  Configure the `Testing` environment to use isolated test resources so an integration test can never reach a Development or Production database. If top-level statements make `Program` inaccessible, add `public partial class Program;` to the Api project.

## 74 FG-K1-43d346afdf K1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Start from a known state (recreate/reset the isolated database, fitting transactions, only needed data, unique identifiers); never modify production data.
  POL TST-008 [MUST PARTIAL] Tests start from a known state and own their setup; do not depend on development seeding or execution order.
  POL TST-004 [MUST PARTIAL] Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.
  SRC .claude/skills/dotnet-testing/SKILL.md:105-105  Choose the database strategy by what the test must prove (provider fidelity vs. application/API integration) and be explicit about the trade-off. Start from a known state with a simple strategy: recreate or reset the isolated database, use transactions when their semantics fit, seed only the data the test needs, use unique identifiers to avoid collisions. Never modify production data.

## 75 FG-K1-8c2a0fe6ef K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=None
CLAIM: Compiled queries only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; never speculatively.
  POL RUN-008 [DEFAULT PARTIAL] Compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL should normally be introduced only for a measured or clearly demonstrated need.
  SRC .claude/skills/ef-core/SKILL.md:128-128  EF Core already caches query compilation by query shape. `EF.CompileQuery`/`EF.CompileAsyncQuery` fit only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; do not add them speculatively (`.claude/rules/backend/runtime.md`). Before specialized optimization inspect round trips, selected columns, N+1 behavior, indexes, generated SQL, the query plan where necessary, materialized data volume, and tracking overhead.
  SRC .claude/skills/ef-core/SKILL.md:241-241  | Measured or clearly demonstrated hot query | Consider a compiled query |

## 76 FG-K1-79fc01688e K1 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Prefer provider execution strategies (EnableRetryOnFailure) over generic application retry pipelines, wrap explicit transactions in the execution strategy, and never apply HTTP retry policies to database operations.
  SRC .claude/skills/ef-core/SKILL.md:221-221  - Transient faults: prefer provider execution strategies (`options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) over generic application-level retry pipelines; with an execution strategy, wrap explicit transactions in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not apply HTTP retry policies to database operations.

## 77 FG-K1-e64089621e K1 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Database retries prefer provider strategies with wrapped explicit transactions, never HTTP retry policies.
  SRC .claude/skills/ef-core/SKILL.md:221-221  - Transient faults: prefer provider execution strategies (`options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) over generic application-level retry pipelines; with an execution strategy, wrap explicit transactions in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not apply HTTP retry policies to database operations.

## 78 FG-K1-f32882b692 K1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Include only dependencies required for meaningful readiness; keep readiness unhealthy until required startup work completes; never use liveness for this.
  POL API-019 [MUST PARTIAL] Liveness should normally avoid external dependencies that could cause restart loops; readiness may depend on capabilities required to serve traffic and should reflect startup/dependency availability appropriately.
  SRC .claude/skills/health-check/SKILL.md:46-46  Include only dependencies required for meaningful readiness; an optional external service need not make the whole application unready. If initialization is asynchronous or slow, keep readiness unhealthy until required startup work completes — never use liveness for this, it causes restart loops.

## 79 FG-K1-eb9159dea5 K1 EXTRA_PRODUCT/DEFAULT conf=MEDIUM sv=N/A res=None
CLAIM: Status semantics beyond the oracle: 400 for invalid HTTP requests (never authentication failures); 406/415 for content negotiation and unsupported media types; 429 for rate limiting with Retry-After when known (never validation); 502/503/504 for intermediary, unavailability and upstream-timeout cases (not every dependency failure; 503 with Retry-After when meaningful).
  SRC .claude/skills/http-api/SKILL.md:33-33  - **400 Bad Request** — the HTTP request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` handles many of these automatically. Never use `400` for authentication failure.
  SRC .claude/skills/http-api/SKILL.md:40-40  - **415 Unsupported Media Type** — the request body format is unsupported (e.g. `Content-Type: application/xml` on a JSON-only endpoint).
  SRC .claude/skills/http-api/SKILL.md:82-102  | Successful query with representation | `200` | / | Empty collection | `200` + `[]` | / | Resource created | `201` + `Location` when available | / | Processing accepted but incomplete | `202` | / | Successful operation with no body | `204` | / | Conditional cache hit | `304` | / | Malformed/contract-invalid request | `400` |

## 80 FG-K1-baa3231f95 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=SAME res=SL
CLAIM: ProblemDetails for structured HTTP errors, ValidationProblemDetails for validation; clients rely on stable codes or contract fields, never human-readable messages.
  POL API-002 [DEFAULT PARTIAL] Use ProblemDetails for non-validation HTTP failures and ValidationProblemDetails for request validation; keep machine-readable contracts stable and safe.
  POL FE-009 [MUST PARTIAL] Frontend code follows the documented API error contract; centralize reusable ProblemDetails parsing when practical and do not infer business behavior from arbitrary human-readable exception messages.
  SRC .claude/skills/http-api/SKILL.md:76-76  `ProblemDetails` for structured HTTP errors, `ValidationProblemDetails` for request validation failures. Machine-readable clients rely on stable error codes or contract fields, never on human-readable exception messages.

## 81 FG-K1-b120c4d4ff K1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=SAME res=None
CLAIM: Prefer respecting Retry-After when the policy supports it; never hammer a rate-limited dependency with an aggressive schedule.
  POL RUN-017 [DEFAULT PARTIAL] When a dependency supplies Retry-After or equivalent rate-limit guidance, respect it where appropriate and do not retry indefinitely or aggressively.
  SRC .claude/skills/httpclient-factory/references/resilience.md:26-26  When a dependency returns `Retry-After`, prefer respecting it when the policy supports it; never hammer a rate-limited dependency with an independent aggressive schedule.

## 82 FG-K1-797447c104 K1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=GR
CLAIM: Hedging only for operations safe to execute multiple times (typically idempotent reads against interchangeable endpoints); never for state-changing operations by default.
  POL RUN-016 [MUST PARTIAL] Retry only when repeating the operation is safe; do not automatically retry state-changing operations without idempotency or another concrete safety mechanism.
  SRC .claude/skills/httpclient-factory/references/resilience.md:38-38  Hedging issues parallel or delayed duplicate attempts — only for operations safe to execute multiple times, typically idempotent reads against interchangeable endpoints; never for state-changing operations by default.
  SRC .claude/skills/httpclient-factory/references/resilience.md:60-68  | External I/O | Bound execution time | / | Safe transient HTTP failure | Consider retry | / | Unsafe write | No retry unless duplicate-safe | / | `429` from dependency | Respect `Retry-After` where appropriate | / | Repeated dependency outage | Consider circuit breaker | / | Optional data unavailable | Consider explicit fallback | / | Latency-sensitive idempotent read | Consider hedging after measurement |

## 83 FG-K1-b9ca80d31e K1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: Retrying publication may duplicate delivery: use idempotent consumers, broker deduplication or an outbox when the business requires it; never claim exactly-once because a retry policy exists.
  SRC .claude/skills/httpclient-factory/references/resilience.md:46-46  Retrying publication may produce duplicate delivery; use idempotent consumers, broker deduplication, an outbox, or similar mechanisms when the business requires them, and never claim exactly-once delivery merely because a retry policy exists.

## 84 FG-K1-17425a17b2 K1 EXTRA_PRODUCT/DEFAULT conf=HIGH sv=N/A res=None
CLAIM: Choose levels by operational meaning: Trace/Debug diagnostics (never assume sensitive data is safe there), Information meaningful events, Warning recovered/degraded conditions, Error failed operations needing investigation, Critical when the application or a subsystem cannot continue.
  SRC .claude/skills/logging/SKILL.md:26-30  - **Trace/Debug** — detailed troubleshooting diagnostics; never assume sensitive data is safe at these levels. / - **Information** — meaningful application events (a background job completed, an important business operation completed, a lifecycle event); not every internal method call. / - **Warning** — an unexpected or degraded condition the application recovered from (fallback used, retries exhausted but another path succeeded, optional dependency unavailable, unusual handled state). / - **Error** — an operation failed and needs investigation. Expected negative outcomes such as `NotFound` or
  SRC .claude/skills/logging/SKILL.md:26-32  - **Trace/Debug** — detailed troubleshooting diagnostics; never assume sensitive data is safe at these levels. / - **Information** — meaningful application events (a background job completed, an important business operation completed, a lifecycle event); not every internal method call. / - **Warning** — an unexpected or degraded condition the application recovered from (fallback used, retries exhausted but another path succeeded, optional dependency unavailable, unusual handled state). / - **Error** — an operation failed and needs investigation. Expected negative outcomes such as `NotFound` or
  SRC .claude/skills/logging/SKILL.md:32-32  Choose levels by operational meaning, not by how unusual an event feels.

## 85 FG-K1-112ed0f2b3 K1 CANONICAL_ONLY/DEFAULT conf=MEDIUM sv=WEAKER res=CK
CLAIM: Logs must not contain passwords, tokens, keys, auth secrets or full payment credentials; PII per project requirements; prefer technical identifiers; Debug/Trace is not a security boundary.
  POL SEC-010 [MUST_NOT PARTIAL] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without a concrete permitted operational need.
  POL RUN-014 [MUST_NOT PARTIAL] Do not serialize arbitrary request bodies, domain objects, or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
  SRC .claude/skills/security-scan/references/scan-layers.md:129-129  Check for passwords, access/refresh tokens, private keys, authentication secrets, and full payment credentials in logs; review PII against project requirements; prefer technical identifiers over identity data. Debug/Trace level is not a security boundary. Review duplicate or missing security-relevant logging in context; do not demand logs for every successful request.

## 86 FG-K1-de49663227 K1 CANONICAL_ONLY/DEFAULT conf=HIGH sv=WEAKER res=GR
CLAIM: Choose data-at-rest protection from the requirement (password hashing; hashed verification tokens; protected storage for retrievable secrets; platform/database encryption; Data Protection for temporary payloads, not universal database encryption; never custom cryptography).
  POL SEC-008 [MUST_NOT PARTIAL] Do not implement custom cryptography when a well-reviewed platform mechanism is appropriate; do not treat ASP.NET Core Data Protection as universal database encryption.
  POL SEC-016 [MUST_NOT PARTIAL] Do not implement custom token/password security, password hashing, or reset-token cryptography when established ASP.NET Core authentication/Identity facilities cover the requirement.
  SRC .claude/skills/security-scan/references/scan-layers.md:141-141  Choose protection from the requirement: password → one-way password hashing; verification-only token → often a hash rather than reversible encryption; retrievable application secret → protected/encrypted storage; database/storage encryption → platform or database mechanism when suitable; temporary application payload → ASP.NET Core Data Protection may fit. Data Protection is not a universal database-encryption solution, and custom cryptography is never the answer.
