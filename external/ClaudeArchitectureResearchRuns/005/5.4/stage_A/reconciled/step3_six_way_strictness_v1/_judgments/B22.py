from jdsl import C, D, P  # noqa: F401

_DEC = "always-imported decision file"

P("DEP-008",
  dims=["D1 .NET 10 LTS (latest stable servicing), C# 14, ASP.NET Core, Controllers; preview/RC requires approval"],
  label="FULL_SEMANTIC_PARITY",
  same="Same Decided platform with the same preview/RC approval clause in each " + _DEC + ": M docs/technology-stack.md:12-14, M1 docs/technology-stack.md:16-18, L0 rules/3-project/decisions.md:22, L1 decisions.md:14, K0 decision-register.md:18 (D-03), K1 decision-register.md:24. Directory.Build.props sets net10.0 in all six; modern-csharp skills defer LangVersion changes to approval (register item 8.7, settled in v1).")

P("DEP-009",
  dims=["D1 EF Core with SQL Server (Microsoft.EntityFrameworkCore.SqlServer); provider concerns out of Application and Domain"],
  label="FULL_SEMANTIC_PARITY",
  same="Same Decided persistence in each " + _DEC + ": M technology-stack.md:15-17, M1 docs/capabilities/persistence.md:5-8, L0 decisions.md:23, L1 decisions.md:33, K0 decision-register.md:19 (D-04), K1 decision-register.md:15. ef-core skills in all six add 'do not add a provider because an example shows it'. Mechanical checks of EF Core placement belong to ARC-008/ARC-019 (RC-ENF-INNER-LAYER).")

P("DEP-010",
  dims=["D1 FluentValidation is the standard explicit validation library",
        "D2 application logging through ILogger<T> with Serilog as provider"],
  label="FULL_SEMANTIC_PARITY",
  cells={"K1": C(owners=["FG-K1-c522be25d4", "FG-K1-aad27ece18"], note="Step 2 override: no direct owner; decision-register.md:25-26 states both parts (read).")},
  same="Both parts in each " + _DEC + ": M technology-stack.md:18-25, M1 technology-stack.md:29-32, L0 decisions.md:24-25, L1 decisions.md:15, K0 decision-register.md:20-21 (D-05, D-06), K1 decision-register.md:25-26. All six forbid the deprecated automatic-validation integration package; which deprecated packages a checker flags differs by package (RC-ENF-PKG-LISTS, DEP-002/DEP-004).")

P("DEP-011",
  dims=["D1 manual mapping for simple cases; Mapster only when mapping volume warrants it",
        "D2 Microsoft resilience packages only when a real integration needs resilience"],
  label="FULL_SEMANTIC_PARITY",
  cells={"M1": C(owners=["FG-M1-0e47f338d1", "FG-M1-bc137ebac7"], note="Step 2 override: docs/technology-stack.md:48-49 states both parts."),
         "L0": C(owners=["FG-L0-d01e762c12", "FG-L0-43a1341bff"], note="Step 2 override: decisions.md:34-35 state both parts."),
         "K0": C(owners=["FG-K0-71e7d5360d", "FG-K0-c8aea32c31"], note="Step 2 override: decision-register.md:31-32 state both parts."),
         "K1": C(owners=["FG-K1-f9b790ecaf", "FG-K1-022c5bf960"], note="Step 2 override: decision-register.md:35-36 state both parts.")},
  same="Both conditional approvals in each " + _DEC + ": M technology-stack.md:54-63, M1 technology-stack.md:48-49, L0 decisions.md:34-35, L1 decisions.md:17, K0 decision-register.md:31-32, K1 decision-register.md:35-36. 'No other mapping framework without approval' is part of the same files in all six (its mechanical flag differs: DEP-002).")

P("DEP-012",
  dims=["D1 Swashbuckle Swagger UI is the default Development interactive documentation/testing surface; exposed elsewhere only when justified"],
  label="FULL_SEMANTIC_PARITY",
  same="Same Decided baseline in each " + _DEC + ": M technology-stack.md:26-30, M1 technology-stack.md:38-40, L0 decisions.md:26 (exposure via aspnet-core.md:27), L1 decisions.md:16, K0 decision-register.md:22 (D-07), K1 decision-register.md:27. M and K1 add that built-in AddOpenApi/MapOpenApi is not the default; the other four's swagger skills say the developer-facing surface is Swagger UI.")

P("DEP-013",
  dims=["D1 NUnit; backend test projects under backend/ beside production projects; WebApplicationFactory baseline; Testcontainers conditional"],
  label="FULL_SEMANTIC_PARITY",
  same="Same Decided stack in each " + _DEC + ": M technology-stack.md:31-34 (and root CLAUDE.md:85-90 layout), M1 docs/capabilities/backend-testing.md:5-8, L0 decisions.md:27, L1 decisions.md:34, K0 decision-register.md:23 (D-08), K1 decision-register.md:16.")

P("DEP-014",
  dims=["D1 current stable Angular via the current CLI with compatible TypeScript/RxJS, standalone APIs, strict mode, routing, zoneless when supported, SCSS, Angular Material/CDK, Vitest"],
  label="FULL_SEMANTIC_PARITY",
  same="Same Decided baseline in each always-imported file: M technology-stack.md:44-47, M1 docs/capabilities/frontend.md:5-10, L0 decisions.md:28, L1 rules/3-project/frontend-stack.md:10, K0 decision-register.md:24 (D-09), K1 decision-register.md:17 (also lists what is not added by default). Scaffolding skills/references in all six apply it.")
