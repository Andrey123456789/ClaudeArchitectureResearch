from jdsl import C, D, P  # noqa: F401

P("RUN-009",
  dims=["D1 follow repository conventions and .editorconfig; modern C# when it improves clarity; no mechanical modernization of working code",
        "D2 build-time surfacing of .editorconfig code-style diagnostics"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="D1 is the same default in each C# rule: M rules/coding-style.md:15-18, M1 coding-style.md:12-15, L0 rules/2-technology/csharp.md:14, L1 rules/0-core/backend-code.md:47, K0 rules/backend/csharp.md:16, K1 rules/backend/coding-style.md:10. All six ship .editorconfig and Directory.Build.props (Nullable enabled in all six).",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["M", "L0"], ["M1", "L1", "K0", "K1"]],
           "Only M (Directory.Build.props:13) and L0 (:9) set EnforceCodeStyleInBuild, so warning-severity .editorconfig style rules appear in `dotnet build`; in M1, L1, K0 and K1 they show only in an IDE. Most style rules are suggestion-level in all six, so the effect on this default is small; the one consequential case is IDE0005 (RUN-010).",
           root="RC-ENF-CODESTYLE-BUILD",
           evidence={"M": ["FG-M-8b4225ae62"], "L0": ["FG-L0-03300112d0"]})],
  enforcement="Source-read build configuration; no build executed.")

P("RUN-010",
  dims=["D1 remove unused/redundant usings from C# files created or modified by the task, without unrelated repository-wide cleanup",
        "D2 build-time report of IDE0005 (unused usings)"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same MUST in each verify skill: M verify:163-168, M1 verify:145-149, L0 verify:58, L1 verify:57, K0 verify:64, K1 verify:64, including implicit/global usings and 'verify the changed files rather than assuming tooling did it'.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["L0"], ["M", "L1", "K0"], ["M1", "K1"]],
           "L0 is the only candidate whose command-line build reports IDE0005: IDE0005 = warning (.editorconfig:27), EnforceCodeStyleInBuild and GenerateDocumentationFile in Directory.Build.props:9/:11 with CS1591 suppressed (:12). M sets warning and EnforceCodeStyleInBuild but not GenerateDocumentationFile, which its own .editorconfig:32-33 says is also required, so the CLI build does not report it; L1 and K0 set warning without EnforceCodeStyleInBuild (IDE only); M1 and K1 set suggestion (hidden). Tiers order how visible the leftover using is.",
           counterexample="Same task: the agent edits OrderService.cs and leaves `using System.Linq;` unused, then runs `dotnet build`. L0 prints an IDE0005 warning for the file; M, M1, L1, K0 and K1 print nothing, so only the verify step's manual check catches it. (MSBuild behavior per M's own configuration note; no build executed.)",
           root="RC-ENF-IDE0005-BUILD",
           evidence={"L0": ["FG-L0-054876afbc", "FG-L0-03300112d0"], "M": ["FG-M-4996dc61c4"], "L1": ["FG-L1-61e69c1ad5"], "K0": ["FG-K0-40a590a8c4"], "M1": ["FG-M1-72ecf968b2"], "K1": ["FG-K1-10226653e1"]})],
  enforcement="Source-read .editorconfig and Directory.Build.props; no build executed.")

P("RUN-011",
  dims=["D1 no style-only rewrites outside the requested change unless explicitly asked"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M coding-style.md:62-64, M1 coding-style.md:85-87, L0 csharp.md:15, L1 backend-code.md:49, K0 csharp.md:17, K1 coding-style.md:12; all but L1 add 'avoid mixing large formatting or modernization changes with functional work', which L1's modern-csharp skill (:62) states.")

P("RUN-012",
  dims=["D1 a performance-motivated change identifies the bottleneck, preserves behavior, uses the simplest effective optimization, keeps tests, and benchmarks/profiles non-obvious optimizations"],
  label="FULL_SEMANTIC_PARITY",
  same="Same five-step procedure in each development-workflow skill: M :68-72, M1 :61-67, L0 :43, L1 :30-35, K0 :63-67, K1 :43.")

P("RUN-013",
  dims=["D1 ILogger<T> with structured templates and stable property names; no string interpolation of structured values"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M coding-style.md:57-58, M1 rules/composition.md:35-36, L0 rules/2-technology/logging.md:13, L1 backend-code.md:43 ('injected logging abstraction', ILogger<T> in backend-platform.md:30), K0 rules/backend/hosting.md:23, K1 rules/backend/operations.md:19.")

P("RUN-014",
  dims=["D1 do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum useful non-sensitive context"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M security.md:108-110, M1 security.md:103-105, L0 rules/0-core/logging-principles.md:14, L1 rules/0-core/security.md:40, K0 rules/common/security.md:44, K1 rules/common/security.md:28. logging skills and Serilog references in all six add destructuring limits.")

P("RUN-015",
  dims=["D1 external I/O calls have a bounded execution time appropriate to the operation; avoid overlapping timeout mechanisms with unclear combined behavior"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M rules/error-handling.md:68-70 (also 'distinguish per-attempt from total-operation timeouts'), M1 performance.md:38-40, L0 runtime-principles.md:27, L1 backend-code.md:25, K0 rules/backend/integrations.md:14, K1 runtime.md:28. Approved register item 8.5 (HTTP timeout: no Markdown change) is respected; httpclient-factory skills in all six distinguish attempt and total timeouts.")

P("RUN-016",
  dims=["D1 retry only when repeating is safe; never automatically retry state-changing operations without idempotency or another duplicate-prevention mechanism"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M error-handling.md:71-74, M1 performance.md:41-43, L0 runtime-principles.md:28, L1 backend-code.md:26, K0 integrations.md:15, K1 runtime.md:29. Resilience references in all six add the same technique (no hedging of writes, no client-invented Idempotency-Key).")
