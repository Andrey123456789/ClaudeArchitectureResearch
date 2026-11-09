---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Level: 0 Core · Owns: dependency need, version selection, due diligence, license approval · Scope: common · Loads: path; read explicitly by `add-dependency`

# Dependency Hygiene

- **Must** add a dependency only for a concrete current requirement — never for hypothetical future use. An approved technology is not a reason to install it before its capability is needed.
- **Must**, for every package addition or update, select the latest **stable** version compatible with the project's target runtime and peer dependencies, verified from the package registry rather than from memory. Do not select preview, alpha, beta, RC, dev, nightly or other prerelease versions, or floating versions such as `*`, unless explicitly requested.
- **Must**, before installation, check whether the exact selected version is deprecated, check known vulnerability information for it, and verify its license from official registry metadata (and the upstream license when necessary).
- **Requires approval:** never install automatically a dependency that requires payment or a commercial license, or whose license has material obligations or cannot be confidently classified (strong copyleft, dual licensing that may require a commercial license, source-available or custom licenses, unclear or missing license). Explain the concern, present reasonable alternatives — or state that none exist — and never silently substitute another package. Do not draw legal conclusions beyond the published license information.

Procedure, commands and the approval presentation: `add-dependency` workflow.
