from jdsl import C, D, P  # noqa: F401

_GATE = ("PROBE-HOOK-01 (HOOK_PROBE_RESULTS.json, direct script runs, same command twice): `dotnet add <Api> package Serilog.AspNetCore --version 8.0.3` -> M allow/allow, L0 allow/allow, K1 allow/allow, "
         "L1 deny/allow (identical retry within 30 minutes passes, pre-shell-command.mjs:7-8), M1 deny/deny and K0 deny/deny until the command carries the self-attested marker `# add-dependency: checked` (M1 dependency-commands.js:15/:528) or `# add-dependency: reviewed` (K0 hook.cjs:18/:294); "
         "without --version K1 also blocks (exit 2, classify-command.cjs:224 'without an exact version'). The same pattern holds for `npm install left-pad@1.3.0` (matches v3 SAME_TASK_MATRIX 'pinned install, first attempt'). "
         "M and L0 rely on PostToolUse reminders to confirm the add-dependency steps (M dependency-guard.mjs:278, L0 claude-hook.mjs:555-557).")

P("DEP-001",
  dims=["D1 add a dependency only for a concrete current requirement; no installs for hypothetical future use ('approved' is not 'install by default')"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each owner: M rules/dependencies.md:20-22 (with docs/technology-stack.md:54 'approved, but added only when needed'), M1 rules/dependencies.md:21-22, L0 rules/0-core/dependency-hygiene.md:15, L1 rules/0-core/engineering.md:10 (paths **/*), K0 rules/common/dependencies.md:18, K1 rules/common/dependencies.md:10 with decision-register.md:33. No checker can test 'current need'; the install-time gates that route to add-dependency are recorded once under DEP-004.")

P("DEP-002",
  dims=["D1 use the approved technology rather than silently selecting an alternative; replacement requires approval",
        "D2 mechanical flag for an alternative to an approved library (for example AutoMapper instead of Mapster)"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is always loaded in all six: M docs/technology-stack.md:5-8 (imported) and Reserved item 6, M1 docs/technology-stack.md:5-7 (imported), L0 rules/3-project/decisions.md:18 (imported), L1 rules/3-project/decisions.md:10 (imported), K0 root CLAUDE.md:34 (Decided) with the decision register, K1 decision-register.md:22 (imported).",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["K0", "L0", "L1"], ["M", "M1", "K1"]],
           "Post-edit approval-required package lists differ by package: AutoMapper is flagged by K0 check-dependencies.cjs:28, L0 manifest-checks.mjs:35 and L1 manifest-policy.json:12, and by none of M, M1, K1 (searched all hooks/scripts); direct Polly is flagged by all six; MediatR by all but K1 (ARC-009). The lists encode each candidate's own approved stack, so the asymmetry is in coverage, not in the rule.",
           counterexample="Same task: 'map the order DTOs'; the agent adds AutoMapper 13.0.1 instead of the approved Mapster. K0, L0 and L1 report a finding that an approved decision is required; M, M1 and K1 accept the manifest (only the text rule applies).",
           root="RC-ENF-PKG-LISTS",
           evidence={"K0": ["FG-K0-32614fa846"], "L0": ["FG-L0-970c60b4fa"], "L1": ["FG-L1-898354570f"], "M": ["FG-M-0ead9af1e3"], "M1": ["FG-M1-c1181b1a3d"], "K1": ["FG-K1-3fcfce11a2"]})],
  enforcement="Package lists source-read; the PreToolUse gate (DEP-004) treats AutoMapper like any package (PROBE-HOOK-01 P8).")

P("DEP-003",
  dims=["D1 verify the latest stable compatible version from the registry at install time; no prerelease or floating versions unless explicitly requested",
        "D2 HQ-03 explicit exception: a bounded user request recorded in dependency-version-exceptions.json; default rejection stays",
        "D3 mechanical rejection of floating versions without a matching record"],
  label="PARTIAL_PARITY_WITH_DELTA",
  cells={c: C(note="Step 2 override: no direct owner; add-dependency version-selection and explicit-exception paragraphs read.") for c in ["L0", "L1", "K0", "K1"]},
  same="D1 and D2 are the same in each add-dependency skill (read): M :41-57, M1 :43-59, L0 :21-24, L1 :25-28, K0 :28-34, K1 :30-36 — prerelease/floating banned unless explicitly requested, the same bounded-request exception recorded as one entry in dependency-version-exceptions.json, 'keep it current' is not a request. D3 is identical in all six on the v3 manifest fixtures (inherited SAME_TASK_MATRIX manifest_tasks: floating without a record rejected, with a matching record accepted, record for another manifest or written by the agent rejected).",
  diffs=[D("D1", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["K1", "M1", "K0", "L1"], ["M", "L0"]],
           "Install-time gate: an install command without an exact version is blocked by K1 and stopped by M1, K0 (marker) and L1 (deny once), and allowed by M and L0, where `dotnet add package` then writes the version NuGet resolves (normally latest stable). The resulting manifest is checked identically in all six, so the effect on this rule is small; the gate is recorded as material under DEP-004. " + _GATE,
           root="RC-ENF-DEP-INSTALL-GATE",
           evidence={"K1": ["FG-K1-e32ee646e0"], "M1": ["FG-M1-fda961832e"], "K0": ["FG-K0-714a017c22"], "L1": ["FG-L1-1001431838"], "M": ["FG-M-6c7da3e62b"], "L0": ["FG-L0-473bfb54f8"]})],
  enforcement="D3 executed in v3 (inherited); install gate executed in PROBE-HOOK-01; live-host application NOT_RUN.")

P("DEP-004",
  dims=["D1 before installation, check deprecation, known vulnerabilities and the exact selected version's license",
        "D2 install-time gate that stops a package command until the add-dependency checks are acknowledged"],
  label="MEANINGFUL_DIVERGENCE",
  cells={c: C(note="Step 2 override: no direct owner; add-dependency due-diligence step read.") for c in ["L1", "K1"]},
  same="D1 is the same three-check step in each add-dependency skill: M :70-79, M1 :72-80, L0 :28, L1 :32-34, K0 :38-42, K1 :40-42.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "K0"], ["L1"], ["K1"], ["M", "L0"]],
           "Strength of the pre-execution gate, strongest first: M1 and K0 deny every package command until it carries a review marker the agent itself writes; L1 denies the first attempt and lets the identical command through within 30 minutes; K1 blocks only commands without an exact version; M and L0 allow and remind afterwards. None verifies that the checks were done (the markers and the retry are self-attested). " + _GATE,
           counterexample="Same task: 'add Serilog logging'. The agent runs `dotnet add src/Api package Serilog.AspNetCore --version 8.0.3` without having checked deprecation, vulnerabilities or license. M1 and K0 refuse it until the agent re-runs with the marker; L1 refuses once; K1, M and L0 execute it immediately, M and L0 then remind. Live-host handling of deny NOT_RUN.",
           root="RC-ENF-DEP-INSTALL-GATE",
           evidence={"M1": ["FG-M1-067405415c"], "K0": ["FG-K0-824844aff7"], "L1": ["FG-L1-1001431838"], "K1": ["FG-K1-e32ee646e0"], "M": ["FG-M-6c7da3e62b"], "L0": ["FG-L0-473bfb54f8"]})],
  enforcement="Executed statically (PROBE-HOOK-01); v3 SAME_TASK_MATRIX 'pinned install' agrees for npm. Deprecated-package deny/notice lists also differ by package (M check-manifests.mjs:33-44, M1 check-manifests.js:23-29, L0 manifest-checks.mjs:23-36, L1 manifest-policy.json:4-8, K0 check-dependencies.cjs:20-30, K1 check-manifests.cjs:27-33) — recorded under RC-ENF-PKG-LISTS.")

P("DEP-005",
  dims=["D1 do not automatically install paid/commercial or materially restrictive/unclear-license dependencies; explain the concern and alternatives; no silent substitution"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="Same REQUIRES_APPROVAL with the same license classes (strong copyleft, dual licensing, source-available/custom, unclear) in each add-dependency skill: M :83-90, M1 :87-93, L0 :32, L1 :38, K0 :48/:62, K1 :46. All six accept common permissive licenses (MIT, Apache-2.0, BSD) without approval.",
  diffs=[D("D1", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["M1", "K0"], ["L1"], ["K1"], ["M", "L0"]],
           "The license check is part of the step the install gate points to (DEP-004, counted there). No candidate inspects a license mechanically.",
           root="RC-ENF-DEP-INSTALL-GATE",
           evidence={"M1": ["FG-M1-fda961832e"], "K0": ["FG-K0-824844aff7"]})])

P("DEP-006",
  dims=["D1 NuGet Central Package Management: versions in Directory.Packages.props, versionless and narrowly scoped PackageReference entries; VersionOverride only with a reason",
        "D2 checker proves per-project effective CPM and rejects versions in project files"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="D1 is the same MUST in each owner: M Directory.Packages.props:3-4 with rules/dependencies.md:30 and add-dependency:112-115, M1 dependencies.md:26-29, L0 rules/3-project/package-management.md:18-19, L1 package-management.md:16, K0 rules/common/dependencies.md:22 (D-17, effective MSBuild value), K1 rules/backend/dependencies.md:12. D2 with the .NET SDK: identical outcomes in all six on the v3 CPM fixtures (root, nested, DirectoryPackagesPropsPath, imported-not-CPM, missing/empty/floating PackageVersion) after PV2-03, PV2-03B and V3-Q10 (inherited SAME_TASK_MATRIX_V3 cpm_nested, cpm_import, package_version).",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["K0", "M"], ["M1", "L0", "L1", "K1"]],
           "Without the .NET SDK (Q-11), K0 and M keep a static error when no Directory.Packages.props is in an ancestor folder, where M1, L0, L1 and K1 report NOT_RUN; with the SDK all six agree. Q-12: none checks the name of a central file imported through DirectoryPackagesPropsPath (uniform). Benchmarks run with the SDK (v3 condition 2), so the difference does not reach a study task.",
           decision="Q-11",
           root="RC-ENF-CPM-NO-SDK",
           evidence={"K0": ["FG-K0-73dd5d1170"], "M": ["FG-M-7f012a0fe2"]})],
  enforcement="Inherited v3 executions with MSBuild 10.0.403 and offline NuGet; registry restore NOT_RUN.")

P("DEP-007",
  dims=["D1 npm by default unless deliberately changed; package.json and package-lock.json kept together and consistent; tooling in the right dependency category",
        "D2 mechanical checks of lockfile presence and dependency category"],
  label="PARTIAL_PARITY_WITH_DELTA",
  cells={"K0": C(owners=["FG-K0-98882cd099", "FG-K0-0f7b627b11", "FG-K0-1b267fb66c"], note="Step 2 override: no direct owner; rules/common/dependencies.md:27-29 states all three parts.")},
  same="D1 in each owner: M rules/dependencies.md:38 and add-dependency:133, M1 dependencies.md:53-54, L0 package-management.md:24-25, L1 package-management.md:17, K0 common/dependencies.md:27-29, K1 rules/frontend/dependencies.md:10; all six add the C04 conditional-commit wording (include both files only when an authorized commit is part of the task). All six check the dependency category of tooling packages (M check-manifests.mjs:49-53, M1 MODULE.md devOnlyPackages, L0 manifest-checks.mjs:47-51, L1 post-change-checks.mjs, K0 check-dependencies.cjs, K1 facets/frontend-framework.cjs).",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["M", "M1", "K0", "K1"], ["L0", "L1"]],
           "A missing package-lock.json is reported by M, M1 (WARN, check-manifests.js:205), K0 (notice, check-dependencies.cjs:355) and K1 (warn, check-manifests.cjs:329-332); L0 and L1 do not check it. `npm install` normally writes the lockfile, so a study task rarely exposes this.",
           root="RC-ENF-NPM-LOCKFILE",
           evidence={"M1": ["FG-M1-bbd22299d0"], "K0": ["FG-K0-76d3c2f793"], "K1": ["FG-K1-03ffa41670"]})])
