from jdsl import C, D, P  # noqa: F401

_FR = "frontend path rule (paths: frontend/**)"

P("FE-007",
  dims=["D1 feature-oriented structure: no application-wide technical buckets or empty architecture folders; feature code stays in its feature; core/shared stay small"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _FR + ": M rules/angular.md:21-24, M1 rules/frontend.md:15-19, L0 rules/1-architecture/frontend-structure.md:14, L1 rules/0-core/frontend.md:12, K0 rules/frontend/angular.md:20, K1 rules/frontend/frontend.md:14. angular skills in all six add the same technique ('create directories only when they contain meaningful code'; shared only for genuinely cross-feature primitives).")

P("FE-008",
  dims=["D1 functional interceptors for new code; interceptors stay cross-cutting and hold no feature business logic"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each " + _FR + ": M angular.md:44-46, M1 rules/frontend-framework.md:18-20, L0 rules/2-technology/angular.md:16, L1 rules/2-technology/frontend/framework.md:12, K0 angular.md:26, K1 rules/frontend/frontend-framework.md:12.")

P("FE-009",
  dims=["D1 follow the documented API error contract; centralize reusable ProblemDetails parsing when practical; never infer business behavior from human-readable messages"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _FR + ": M angular.md:47-49, M1 frontend.md:39-41, L0 frontend-structure.md:25, L1 0-core/frontend.md:15, K0 angular.md:41, K1 frontend.md:22. angular skills in all six place the parsing in one reusable interceptor or mapper; L0 and K1 add 'branch on stable codes or fields'.")

P("FE-010",
  dims=["D1 reactive forms for non-trivial forms when useful",
        "D2 frontend validation is UX and never replaces backend validation, data-integrity or security enforcement"],
  label="FULL_SEMANTIC_PARITY",
  cells={"L0": C(owners=["FG-L0-93a7497c35", "FG-L0-1ffc42f66f"],
                 note="Partial witness (PW38): the two parts sit in two path rules with the same paths: frontend/** frontmatter, so they load together; read rules/2-technology/angular.md:17 (D1) and rules/1-architecture/frontend-structure.md:26 (D2).")},
  same="Both parts in each " + _FR + ": M angular.md:55-58, M1 frontend.md:52-55, L0 angular.md:17 + frontend-structure.md:26, L1 0-core/frontend.md:16, K0 angular.md:42, K1 frontend-framework.md:13. custom-settings skills in all six repeat that backend validation stays authoritative when both sides expose the same constraint.")

P("FE-011",
  dims=["D1 avoid manual nested RxJS subscriptions; prefer composition operators when they express the behavior clearly"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each " + _FR + ": M angular.md:62-63, M1 frontend-framework.md:21-22, L0 2-technology/angular.md:14, L1 framework.md:13, K0 angular.md:32, K1 frontend-framework.md:14.")

P("FE-012",
  dims=["D1 manual subscriptions from framework-managed code are tied to the component/service lifecycle with the project's current Angular facilities"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _FR + ": M angular.md:64-66, M1 frontend-framework.md:23-25, L0 2-technology/angular.md:15, L1 framework.md:14, K0 angular.md:33, K1 frontend-framework.md:15 (names takeUntilDestroyed as the example; L0 and L1 skills name it too).")
