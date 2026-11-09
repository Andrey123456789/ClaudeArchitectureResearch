from jdsl import C, D, P  # noqa: F401

P("ARC-025",
  dims=["D1 Infrastructure translates remote HTTP responses into Application-facing abstractions; HttpResponseMessage and remote transport concerns do not leak into Application"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M architecture.md:158-160, M1 :135-137, L0 backend-layers.md:40, L1 rules/1-architecture/roles.md:31, K0 rules/backend/integrations.md:13, K1 rules/backend/architecture.md:25. httpclient-factory skills in all six add the same technique (do not blindly EnsureSuccessStatusCode when statuses carry contract meaning).")

P("ARC-026",
  dims=["D1 do not create separate Domain or persistence models merely because the API has several versions; isolate version-specific transport contracts at the API boundary when practical"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT with the same 'when practical' qualifier in each rule: M architecture.md:161-163, M1 :141-143, L0 entry-points.md:36, L1 roles.md:32, K0 rules/backend/api.md:28, K1 rules/backend/api-contracts.md:15. Adopting versioning is Reserved in all six (ARC-020 item 9).")

P("ARC-027",
  dims=["D1 no speculative projects, infrastructure, empty directory trees or generic Common/Helpers/Utils buckets solely to look architectural"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each structure rule: M rules/repository-structure.md:19-25, M1 rules/physical-structure.md:14-18, L0 rules/1-architecture/code-organization.md:15, L1 rules/0-core/engineering.md:11 (paths **/*), K0 rules/common/repository-layout.md:17, K1 rules/common/structure.md:10 (paths **/*). The path globs of M, M1, L0 and K0 cover the backend and frontend trees where structure is created, so the reach difference does not change when the rule is present. Layout references in all six repeat 'create only directories that contain real code'.",
  enforcement="No candidate checks empty trees or Common/Helpers buckets. New production projects get feedback in all six through the Reserved reference-graph checks (see ARC-020 D4, RC-ENF-RESERVED-GRAPH).")

P("ARC-028",
  dims=["D1 backend test projects get no broader production references than their test scope requires, with the production inward discipline",
        "D2 mechanical check of test-project production references"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same MUST_NOT with the same typical map (Domain.Tests->Domain, Application.Tests->Application and Domain as needed, IntegrationTests->Api, optional Infrastructure.Tests->Infrastructure narrower as required) in M architecture.md:37-44, M1 :150-152 with backend-layout.md:174-188, L0 code-organization.md:17 with 3-project/layout.md:31-34, L1 frame/boundaries.md:45, K0 rules/backend-tests/testing.md:34, K1 rules/backend-tests/test-projects.md:10-17.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M", "M1", "L1", "K1"], ["K0"], ["L0"]],
           "M check-manifests.mjs:63-68/:382 (TEST_ALLOWED: the tested layer and inward layers), M1 check-architecture.js:87-99 (capability testProjects mayReference), L1 check-architecture.mjs:85 (testRoles typicalReferences) and K1 facets/architecture-style.cjs:19-26/:65-69 (error outside typical+justified, warn for justified) report an atypical test reference as a finding; K0 check-dependencies.cjs:151-157 only adds a notice; L0 manifest-checks.mjs:406 returns early for test projects, so L0 has no test-reference check. Allowed sets also differ at the edge: M and M1 let Infrastructure.Tests reference Application and Domain without remark, K1 warns.",
           counterexample="Same task: the agent adds <ProjectReference> to the Infrastructure project inside <Name>.Application.Tests. M, M1, L1 and K1 report a violation, K0 a notice, L0 nothing. Live effect of PostToolUse findings NOT_RUN.",
           root="RC-ENF-TEST-REFS",
           evidence={"M": ["FG-M-78984c3bd4"], "M1": ["FG-M1-26d25f0eab"], "L1": ["FG-L1-ac47fb1383"], "K1": ["FG-K1-85a7d13081"], "K0": ["FG-K0-d7bbcbe1c6"], "L0": ["FG-L0-6a331f0397"]})],
  enforcement="Source-read checker code; not executed on a shared fixture. L0's project-structure skill (:50) says its hook blocks `dotnet add/remove reference`, so references are added by editing project files, which its manifest check does not inspect for test projects.")

P("ARC-029",
  dims=["D1 do not duplicate equivalent DTOs across Api and Application merely for layer shape; add transport contracts when separation gives a concrete boundary benefit"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT with the same benefit condition in each rule: M architecture.md:164-166, M1 :144-146, L0 entry-points.md:21, L1 boundaries.md:26, K0 architecture.md:38, K1 architecture-style.md:47.")
