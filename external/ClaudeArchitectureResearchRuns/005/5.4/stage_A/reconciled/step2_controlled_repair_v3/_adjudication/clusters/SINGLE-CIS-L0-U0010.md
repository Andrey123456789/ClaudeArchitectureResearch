# SINGLE-CIS-L0-U0010 (1 records)

## CIS-L0-U0010 (pass 2) L0 .claude/skills/authentication/SKILL.md:105-105  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When using Angular HttpClient XSRF support for cookie-carried credentials, use a matching cookie/header name configuration.
TRIGGER: State-changing requests with automatically carried browser credentials and Angular HttpClient XSRF support. | EXC: Explicit bearer-header credentials have different CSRF characteristics; no universal browser storage choice or prescribed literal name is inferred. | POL: ['SEC-011']
CODEX WHY: The exact source qualifies Angular XSRF support. A working-protection obligation can semantically subsume this detail, while a registration naming only the library may fail to preserve the configuration condition. Keep the distinction unresolved, not a proven novel norm.
```
 102  
 103  ## Cookies, CSRF, and token storage
 104  
 105> Cookie-carried credentials need antiforgery protection for state-changing requests (ASP.NET Core antiforgery; Angular's `HttpClient` XSRF support with a matching cookie/header name). Bearer tokens sent explicitly i
 106  
 107  ## Testing
 108  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-20a255e385 [105, 105] CANONICAL_ONLY/MUST pol=['SEC-011'] rel=[]: With automatic browser cookie credentials include CSRF protection; a single-page frontend does not remove the risk.
- V2 FG-L0-786eb1d14d [105, 105] CANONICAL_ONLY/MUST_NOT pol=['SEC-012', 'SEC-010'] rel=[]: Do not claim one browser token-storage mechanism is universally secure; choose by threat model; never log tokens.
- V2 FG-L0-cb9a81a22c [105, 105] CANONICAL_ONLY/DEFAULT pol=['SEC-011'] rel=[]: Cookie-carried credentials need antiforgery protection for state-changing requests (ASP.NET Core antiforgery, Angular XSRF support); explicit bearer headers differ.
- V2 FG-L0-d7f4269033 [105, 105] CANONICAL_ONLY/DEFAULT pol=['SEC-012'] rel=[]: Choose browser token storage per the application's threat model.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0288 -> FG-L0-cb9a81a22c [CANONICAL_ONLY] Cookie-carried credentials need antiforgery protection for state-changing requests (ASP.NET Core antiforgery, Angular XSRF support); explicit bearer headers differ.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0551 -> FG-L0-1dde409a11 [CANONICAL_ONLY] Review CSRF protection for state-changing operations when browser credentials are sent automatically; explicit Bearer headers differ.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0053 -> FG-L0-20a255e385 [CANONICAL_ONLY] With automatic browser cookie credentials include CSRF protection; a single-page frontend does not remove the risk.
