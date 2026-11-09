from jdsl import C, D, P  # noqa: F401

P("DEP-022",
  dims=["D1 .slnx solution format by default; legacy .sln only when an external tool or project requirement needs it"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each always-imported decision file: M docs/technology-stack.md:35-36, M1 docs/technology-stack.md:19-20, L0 rules/3-project/decisions.md:47, L1 decisions.md:18, K0 decision-register.md:41 (D-16), K1 decision-register.md:28. Scaffolding skills in all six create `<Name>.slnx`; K0's MUST in project-structure SKILL.md:22 is the scaffold step applying the same default, not a stricter rule.")

P("DEP-023",
  dims=["D1 repository-level Directory.Build.props for genuinely shared build settings and Directory.Packages.props for CPM; project-specific settings stay in their projects"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each always-imported decision file: M technology-stack.md:37-40, M1 technology-stack.md:21-25, L0 decisions.md:48, L1 decisions.md:19, K0 decision-register.md:42 (D-17, v3 rewording adds that any MSBuild-imported location is valid), K1 decision-register.md:29. All six templates ship both files at the repository root (read: each Directory.Build.props holds TargetFramework/Nullable/ImplicitUsings). The extra code-style properties in M and L0 belong to RUN-009/RUN-010; K0 check-dependencies.cjs:122 (version on a PackageReference) belongs to DEP-006.")

P("DEP-024",
  dims=["D1 approved layout: backend production and test projects under backend/<Name>.<Layer>/, Angular workspace under frontend/<Name>.Web/, docs/ for documentation; no separate top-level tests directory",
        "D2 mechanical detection of a top-level tests/ directory"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 in each always-loaded file: M root CLAUDE.md:85-90 (ROOT_ALWAYS), M1 docs/capabilities/architecture.md:27-32, L0 rules/3-project/decisions.md:49, L1 decisions.md:23, K0 decision-register.md:43 (D-18), K1 decision-register.md:42; the project-structure skills in all six scaffold the same tree. M's frontend-test text (PV2-04) holds and is about test placement inside the workspace, not this layout.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["L1"], ["K1"], ["M", "M1", "L0", "K0"]],
           "L1 check.json:4 lists `tests` in forbiddenTopLevelDirectories and check-architecture.mjs:29-33 reports a violation; post-change-checks.mjs:310-326 runs it after every project-file edit and exits 2 (feedback). K1 check-manifests.cjs:326-328 warns on a top-level tests/ directory, but only in checkAll, which runs from the CLI (verify skill :54, project-structure scaffold Verify step :41), not from the manifest hook. M1 check-architecture.js and K0 check-dependencies.cjs:158 inspect only projects under backend/, so a project under tests/ is not seen; M and L0 have no layout check.",
           counterexample="Same task: the agent creates tests/Shop.Tests/Shop.Tests.csproj. L1 reports a violation right after the edit; K1 reports a warning when the agent runs verify; M, M1, L0 and K0 report nothing. Source-read, not executed.",
           root="RC-ENF-TOP-LEVEL-TESTS",
           evidence={"L1": ["FG-L1-222f70a885", "FG-L1-2c84b4d283"], "K1": ["FG-K1-323ece8175"], "M": ["FG-M-0e415dbede"], "M1": ["FG-M1-c25aec0fa1"], "L0": ["FG-L0-5b819872f7"], "K0": ["FG-K0-0a2760ad11"]})],
  enforcement="Source-read checker code and hook wiring (L1 settings.json:15-29 registers post-change-checks.mjs); not executed on a fixture.")

P("DEP-025",
  dims=["D1 npm --force / --legacy-peer-deps (and npm_config_* equivalents) are not used to bypass peer-dependency conflicts; no marker or approval opens the route",
        "D2 detection of a persistent bypass written into an .npmrc file"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same MUST_NOT with the same 'no confirmation, comment marker, or approval opens this route' clause in each add-dependency skill: M :136-138, M1 :115-118, L0 :57, L1 :66, K0 :76-77, K1 :74. PROBE-HOOK-02 (direct PreToolUse runs, each twice) shows all six refuse all seven shell variants before execution: --legacy-peer-deps, --force, `npm i -f`, npm_config_legacy_peer_deps=true, `npm ci --legacy-peer-deps`, --legacy-peer-deps=true and `npm config set legacy-peer-deps true` (M, L0, K1 exit 2; M1, L1, K0 deny; the reason text in M1, L0, L1, K0 and K1 repeats that nothing opens the route). The control (pinned install without a bypass) differs only through the separate install gate (RC-ENF-DEP-INSTALL-GATE, DEP-004).",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["L0"], ["M", "M1", "L1", "K0", "K1"]],
           "Only L0 treats .npmrc as a manifest: manifest-checks.mjs:71 includes it and checkNpmrc (:453-457, called at :495) reports `legacy-peer-deps=true` or `force=true` after the edit (claude-hook.mjs:43 also tracks **/.npmrc). The other five check the shell command only; none of their checkers reads .npmrc (grep: no match in M, M1, L1, K0, K1 .claude/).",
           counterexample="Same task: after the blocked flag, the agent writes `legacy-peer-deps=true` into frontend/Shop.Web/.npmrc and runs a plain `npm install`. L0 reports a peer-dependency bypass after the edit; M, M1, L1, K0 and K1 report nothing about the file (the following plain install is treated as an ordinary install). Source-read, not executed.",
           root="RC-ENF-NPMRC-BYPASS",
           evidence={"L0": ["FG-L0-b8ab3c4a10"], "M": ["FG-M-044fe37163"], "M1": ["FG-M1-159a4ef4c3"], "L1": ["FG-L1-5a6df8a726"], "K0": ["FG-K0-646af0c55c"], "K1": ["FG-K1-23a2f5e23c"]})],
  enforcement="D1 executed statically (PROBE-HOOK-02, HOOK_PROBE2_RESULTS.json); live host NOT_RUN. D2 source-read only.",
  challenge="D2 requires the agent to work around a refused command; it is scored material because the same file edit gets a finding only in L0. Sensitivity: if evasion routes are excluded from materiality, DEP-025 becomes FULL_SEMANTIC_PARITY.")

P("DEP-026",
  dims=["D1 appsettings.Development.json provides a usable non-secret local Development connection string; credential-bearing values via user-secrets or another approved local mechanism"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each persistence rule: M rules/persistence.md:43-46, M1 persistence-technology.md:69-73, L0 rules/3-project/data-lifecycle.md:25, L1 rules/3-project/development-database.md:10, K0 rules/backend/persistence.md:21, K1 rules/backend/persistence-technology.md:26. All six project-structure references say not to ignore the Development configuration contract (M solution-layout.md:121-122, M1 :82-85, L0 :73, L1 :40, K0 :68, K1 :53). The shipped .gitignore of L0 and L1 ignores only appsettings.*.local.json and keeps appsettings.Development.json tracked, which applies the same default (RC-PKG-GITIGNORE, counted at SEC-001).")
