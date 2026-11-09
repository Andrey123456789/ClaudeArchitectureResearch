from jdsl import C, D, P  # noqa: F401

P("SEC-007",
  dims=["D1 production traffic carrying credentials or sensitive data uses TLS, respecting the actual hosting topology",
        "D2 never disable certificate validation to make an integration work"],
  label="FULL_SEMANTIC_PARITY",
  cells={"K0": C(owners=["FG-K0-115ec9cd66", "FG-K0-95da733d51"], note="Step 2 override: no direct owner; rules/common/security.md:38 (D1) and :39 (D2) read."),
         "K1": C(owners=["FG-K1-ee84e2cbd7", "FG-K1-d0e97026d8"], note="Step 2 override: no direct owner; rules/common/security.md:22 (D1) and :23 (D2) read.")},
  same="Both parts in each security rule: M rules/security.md:80-84, M1 security.md:74-79, L0 rules/0-core/security-principles.md:46, L1 rules/0-core/security.md:33, K0 rules/common/security.md:38-39, K1 rules/common/security.md:22-23. All six say in-app HTTPS redirection is not required when the topology already provides TLS; scan references treat missing redirection the same way.")

P("SEC-008",
  dims=["D1 no custom cryptography when a reviewed platform mechanism fits",
        "D2 ASP.NET Core Data Protection is not universal database encryption"],
  label="FULL_SEMANTIC_PARITY",
  cells={"L0": C(owners=["FG-L0-21c75b5605", "FG-L0-19c7cbab7a"], note="Step 2 override: no direct owner; security-principles.md:47 (D1, plus :38 for custom token/password security) and rules/2-technology/aspnet-core.md:32 (D2) read.")},
  same="Both parts in each owner: M rules/security.md:88-92, M1 security.md:83-87, L0 security-principles.md:47 with aspnet-core.md:32, L1 rules/0-core/security.md:35, K0 rules/backend/security.md:28, K1 rules/backend/security.md:19. Scan references in all six give the same protection-by-requirement table.")

P("SEC-009",
  dims=["D1 CORS is the narrowest policy satisfying actual browser-client requirements (default)",
        "D2 never combine credentialed cross-origin requests with unrestricted origins"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each owner: M security.md:96-99, M1 security.md:91-94, L0 security-principles.md:48, L1 security.md:34, K0 backend/security.md:32, K1 backend/security.md:23. 'CORS is not authorization' is the same scan technique in all six.")

P("SEC-010",
  dims=["D1 never log passwords, tokens, private keys, authentication secrets or full payment credentials",
        "D2 avoid PII without a concrete permitted operational need; log level is not a privacy control"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each owner: M security.md:103-107, M1 security.md:98-102 (v3 reworded claim only; the line itself unchanged in meaning), L0 rules/0-core/logging-principles.md:13, L1 rules/0-core/security.md:39, K0 rules/common/security.md:43, K1 rules/common/security.md:27. logging skills in all six add authorization headers and full bodies to the avoid list.")

P("SEC-011",
  dims=["D1 when cookies automatically carry authentication credentials, include CSRF protection in the design; an Angular/SPA frontend does not remove the risk"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each owner: M security.md:72-73, M1 security.md:66-68, L0 security-principles.md:41, L1 security.md:28, K0 rules/frontend/angular.md:46, K1 rules/frontend/security.md:10. K0 and K1 place it in a frontend-scoped rule while the others use a general security rule; the cookie-authentication design is decided on the backend as well, and the backend authentication skills of K0 (:108) and K1 (:93) state the same, so reach for a cookie-auth task is equivalent.")

P("SEC-012",
  dims=["D1 do not claim one browser token-storage mechanism is universally secure; choose by threat model",
        "D2 never log tokens"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each owner: M security.md:74-76, M1 security.md:69-70 (D2 by its never-log list at :98-102), L0 security-principles.md:42, L1 security.md:29, K0 rules/frontend/angular.md:47, K1 rules/frontend/security.md:11.")
