from jdsl import C, D, P  # noqa: F401

P("DEP-015",
  dims=["D1 no NgRx, Axios, Lodash, Bootstrap, Tailwind or extra form/component/state libraries by default; built-in Angular first, extras only for a concrete need"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each always-imported file: M docs/technology-stack.md:48-50, M1 docs/capabilities/frontend.md:11-13, L0 rules/3-project/decisions.md:42, L1 rules/3-project/frontend-stack.md:11, K0 decision-register.md:25 (D-10), K1 decision-register.md:17. All six also flag the named packages mechanically after a manifest edit (M check-manifests.mjs:47-48, M1 frontend/angular/MODULE.md:31, L0 manifest-checks.mjs:39-45, L1 frontend/angular/enforcement.json:6-16, K0 check-dependencies.cjs:31, K1 facets/frontend-framework.cjs:10-11); the lists differ only in extra entries (K0 primeng, L1/K0 @ngxs, K0/K1 ng-bootstrap), which the shared 'additional ... libraries' clause already covers.")

P("DEP-016",
  dims=["D1 Playwright is the approved E2E default when E2E coverage is required; not in the minimal scaffold"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each always-imported file: M technology-stack.md:65-66, M1 frontend.md:14-15, L0 decisions.md:37, L1 frontend-stack.md:12, K0 decision-register.md:33 (D-13), K1 decision-register.md:37.")

P("DEP-017",
  dims=["D1 when Controller API versioning is adopted, use the Asp.Versioning Controller integration; never add the package before adoption"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each add-dependency skill: M :32-35, M1 :25-28, L0 :50, L1 :18, K0 :21 (D-15), K1 :22. Adoption itself is Reserved in all six (Reserved item 9).")

P("DEP-018",
  dims=["D1 do not introduce Docker merely because the application can be containerized; container artifacts only when needed"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each always-imported file: M technology-stack.md:67-69, M1 technology-stack.md:51, L0 decisions.md:38, L1 decisions.md:24, K0 decision-register.md:34 (D-14), K1 decision-register.md:38; ci-cd/docker skills in all six add 'do not add Docker to the pipeline merely because the skill covers it'.")

P("DEP-019",
  dims=["D1 production containers use an appropriate runtime image, not the SDK image for convenience; no switching to root to bypass filesystem problems (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M rules/security.md:123-125, M1 security.md:119-121, L0 rules/2-technology/containers-ci.md:20 (adds 'run as the image's non-root user where supported'), L1 rules/2-technology/backend-libraries.md:14, K0 rules/backend/hosting.md:34, K1 rules/backend/operations.md:28. docker skills in all six add 'find out why permissions are wrong instead of switching users'.")

P("DEP-020",
  dims=["D1 when resilience is required, prefer Microsoft.Extensions.Http.Resilience / Microsoft.Extensions.Resilience; direct Polly is a documented exception",
        "D2 deprecated Polly integrations are not added"],
  label="FULL_SEMANTIC_PARITY",
  same="D1 is the same default in each add-dependency skill: M :25-31, M1 :29-35, L0 :51, L1 :17, K0 :20 (D-12), K1 :23. D2 and the exception flag are enforced alike in all six manifest checks: deprecated Microsoft.Extensions.Http.Polly and Polly.Extensions.Http are denied (M check-manifests.mjs:33-36, M1 check-manifests.js:23-24, L0 manifest-checks.mjs:23-28, L1 manifest-policy.json:5-8, K0 check-dependencies.cjs:20-25, K1 check-manifests.cjs:27-31) and direct Polly is flagged as a documented exception (M :41-42, M1 :28-30, L0 :32, L1 :11, K0 :26-30, K1 :32-35).")

P("DEP-021",
  dims=["D1 when Serilog is configured, use DI-integrated AddSerilog with provider configuration in environment-aware configuration; application code depends on ILogger<T>"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M rules/architecture.md:149-152 (names UseSerilog as the non-default), M1 rules/composition.md:37-40, L0 rules/2-technology/logging.md:14 (also names UseSerilog), L1 backend-libraries.md:13, K0 rules/backend/hosting.md:24, K1 rules/backend/operations.md:20. Serilog references in all six keep Log.Logger/LogContext at composition boundaries.")
