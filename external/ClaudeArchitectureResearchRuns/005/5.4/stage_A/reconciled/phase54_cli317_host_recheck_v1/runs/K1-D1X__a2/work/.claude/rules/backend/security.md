---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# Backend Security Standard

## Authentication and authorization

- Anonymous access must be deliberate and visible; avoid redundant authorization attributes when a secure global or fallback policy already expresses the intent.
- Must not implement custom token or password security, password hashing, or reset-token cryptography when established ASP.NET Core authentication/Identity facilities cover the requirement.
- Bearer/OIDC authentication must validate what the actual issuer/provider requires — issuer, audience where applicable, signature/signing authority, and lifetime; never disable validation merely to make a token work.
- Authentication failures must not reveal secrets or account state unnecessarily; login behavior avoids account-enumeration leaks where relevant.

## Cryptography and data protection

- Must not implement custom cryptography when a well-reviewed platform mechanism is appropriate, and must not treat ASP.NET Core Data Protection as universal database encryption.

## Browser and upload surfaces

- Default: CORS is the narrowest policy that satisfies actual browser-client requirements (a public unauthenticated API may legitimately differ from a private browser application); never combine credentialed cross-origin requests with unrestricted origins.
- Must not treat client-provided file metadata such as MIME type as authoritative when upload handling or security decisions depend on the actual content.

Technique: `authentication`. Audit procedure: `security-scan`.
