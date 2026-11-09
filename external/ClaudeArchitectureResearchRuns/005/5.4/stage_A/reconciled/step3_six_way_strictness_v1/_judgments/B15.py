from jdsl import C, D, P  # noqa: F401

P("SEC-001",
  dims=["D1 never hardcode or commit real secrets, credentials, private keys, tokens or production connection strings, including example configuration files",
        "D2 repository-level ignore of local secret files (.env, local overrides)"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="D1 is the same MUST_NOT in each security rule, all naming example configuration files: M rules/security.md:31-33, M1 security.md:26-28, L0 rules/0-core/security-principles.md:25, L1 rules/0-core/security.md:12 (paths **/*; also Development configuration), K0 rules/common/security.md:25, K1 rules/common/security.md:12 (paths **/*). v2's C03 review (WF-019) holds in all six. Scan, docker and verify skills repeat it in all six.",
  diffs=[D("D2", "DELIVERY", "DELIVERY_REACHABILITY_VARIANCE", False, [["L0", "L1"], ["M", "M1", "K0", "K1"]],
           "L0 and L1 ship a .gitignore that already excludes .env, .env.* (except .env.example) and appsettings.*.local.json (L0 .gitignore:13-17, L1 :14-18). M, M1, K0 and K1 ship none; their project-structure skills create one during scaffolding (M SKILL:28/:62, M1/K1 solution-layout tree, K0 solution-layout.md:66-68 naming 'local secret/config overrides'). Same rule; only whether the ignore file exists before scaffolding differs. A secret in a tracked file is caught by none of the six mechanically.",
           root="RC-PKG-GITIGNORE",
           evidence={"L0": ["FG-L0-432c1cc507"], "L1": ["FG-L1-6a041ad5cc"]})])

P("SEC-002",
  dims=["D1 local secret mechanism (user-secrets) in development; environment injection or a managed store when deployed; no assumed cloud provider"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each security rule: M security.md:34-37, M1 security.md:29-32, L0 security-principles.md:26, L1 security.md:13, K0 common/security.md:26, K1 common/security.md:13. configuration skills in all six keep appsettings.json non-secret and name Key Vault only as one provider.")

P("SEC-003",
  dims=["D1 data crossing the trusted boundary is untrusted and validated at the owning layer when assumptions matter"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST with the same source list (HTTP, uploads, external responses, message payloads, user identifiers/filters) in each rule: M security.md:41-44, M1 security.md:36-40, L0 security-principles.md:30, L1 security.md:17, K0 common/security.md:30, K1 common/security.md:17.")

P("SEC-004",
  dims=["D1 parameterized database access; never build SQL by concatenating untrusted input"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M security.md:51-53, M1 security.md:44-46, L0 security-principles.md:32, L1 security.md:18, K0 rules/backend/security.md:17, K1 rules/backend/persistence.md:20. v2's C02 review (RUN-008 raw-SQL evidence) is NOT_AFFECTED for this rule in all six; ef-core skills give the same interpolation-parameterizing technique.")

P("SEC-005",
  dims=["D1 authorization is enforced on the server; client guards and hidden buttons are UX only"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M security.md:57-58, M1 security.md:50-51, L0 security-principles.md:36, L1 security.md:23, K0 common/security.md:34, K1 common/security.md:18. Angular and authentication skills in all six restate the UX-only role of frontend checks and the resource-authorization technique.")

P("SEC-006",
  dims=["D1 anonymous access is deliberate and visible; no redundant authorization attributes under a secure global policy"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M security.md:59-61, M1 security.md:52-55, L0 security-principles.md:37, L1 security.md:24, K0 rules/backend/security.md:21, K1 rules/backend/security.md:12. Security-scan skills in all six carry the matching 'do not recommend [Authorize] on every action when a global policy protects them' (approved register item 8.7 security scan: no change).")
