---
paths:
  - "backend/**/*"
---

> Level: 3-project · Capability: persistence/ef-core · Facet: persistence.dev-config · Owns: local Development database configuration default · Scope: backend · Loading: path

# Development Database Configuration

Default: `appsettings.Development.json` provides a usable local Development connection string whenever that string contains no secret credentials — on Windows, for example `Server=(localdb)\\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;`. When local SQL Server requires credentials, keep the non-secret structure in configuration and supply the credential-bearing value through user-secrets or another approved local secret mechanism.
