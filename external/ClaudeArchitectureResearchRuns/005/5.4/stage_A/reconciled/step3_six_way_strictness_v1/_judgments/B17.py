from jdsl import C, D, P  # noqa: F401

P("SEC-013",
  dims=["D1 security-sensitive authorization/permission/required-control checks fail safely; lookup or configuration failures never silently become success (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each security rule: M security.md:114-116, M1 security.md:109-111, L0 security-principles.md:52, L1 rules/0-core/security.md:44, K0 rules/common/security.md:48, K1 rules/common/security.md:32.")

P("SEC-014",
  dims=["D1 when a required security control cannot be configured correctly, fail visibly at startup/configuration rather than fall back insecurely"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="All six place the rule in the same always-relevant security rule: M security.md:117-118, M1 security.md:112-113, L0 security-principles.md:53, L1 security.md:45, K0 common/security.md:49, K1 common/security.md:33; scan references in all six list the same dangerous fallbacks (auth silently disabled, plaintext without a key, allow-all on provider failure).",
  diffs=[D("D1", "NORMATIVE", "TRUE_NORMATIVE_VARIANCE", False, [["K0", "K1"], ["M", "M1", "L0", "L1"]],
           "K0 'must not fall back to an insecure mode; prefer visible ... failure' and K1 'must fail visibly ... instead of falling back' forbid the insecure fallback outright; M, M1, L0 and L1 keep the canonical 'prefer a visible ... failure over an insecure fallback'. A task that tempts a convenience fallback (for example disabling authentication when its configuration is missing in Development) is forbidden in K0/K1 and strongly disfavoured, but not categorically forbidden, in the other four.",
           evidence={"K0": ["FG-K0-8eca386af7"], "K1": ["FG-K1-079264545c"], "M": ["FG-M-a8c546c579"], "L0": ["FG-L0-5846b2de3a"]})],
  cells={"K0": C(force="MUST_NOT", compliance="STRICTER_THAN_CANONICAL"), "K1": C(compliance="STRICTER_THAN_CANONICAL")})

P("SEC-015",
  dims=["D1 client-provided file metadata such as MIME type is not authoritative when handling or security depends on actual content"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M security.md:45-47, M1 security.md:114-115, L0 security-principles.md:31, L1 security.md:19, K0 rules/backend/security.md:36, K1 rules/backend/security.md:24.")

P("SEC-016",
  dims=["D1 no custom token/password security, password hashing or reset-token cryptography when ASP.NET Core authentication/Identity covers the requirement"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M security.md:62-64, M1 security.md:56-58, L0 security-principles.md:38, L1 security.md:25, K0 backend/security.md:22, K1 backend/security.md:13. authentication skills in all six use Identity's hashing, lockout and reset tokens.")

P("SEC-017",
  dims=["D1 Bearer/OIDC validates issuer, audience where applicable, signature/signing authority and lifetime as the issuer requires; never disable validation to make a token work"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M security.md:65-68, M1 security.md:59-62, L0 security-principles.md:39, L1 security.md:26, K0 backend/security.md:23, K1 backend/security.md:14. Scan references in all six add 'do not require setting every TokenValidationParameters property when authority metadata already validates'.")

P("SEC-018",
  dims=["D1 authentication failures do not reveal secrets or account state unnecessarily; login avoids account enumeration where relevant"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M security.md:69-71, M1 security.md:63-65, L0 security-principles.md:40, L1 security.md:27, K0 backend/security.md:24, K1 backend/security.md:15.")
