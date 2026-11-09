# L1 Run-01 vs Run-02

## Structural comparison

The raw implementations have high file-level variance:

- common runtime paths: 58;
- union runtime paths: 123;
- whole-tree path Jaccard: **0.472**;
- skill-name Jaccard: **0.900** (27 common skill names);
- rule-stem Jaccard: **0.184**;
- both contain the same four selected capability implementations:
  - `architecture/clean-architecture`;
  - `persistence/ef-core`;
  - `backend-testing/nunit`;
  - `frontend/angular`.

The low file-path similarity is driven mainly by decomposition/granularity:

- Run-01 uses 12 Core rule files; Run-02 consolidates them into 6.
- Run-01 uses 5 Architecture rules; Run-02 uses 3.
- Run-01 uses 6 Project rules; Run-02 uses 4.
- Run-01 separates `develop` and `delivery`; Run-02 uses one `development-workflow`.
- Run-02 moves several capability facets into clearer role-named subdirectories.

## Shared strengths

Both runs successfully reproduce the defining L1 model:

1. stability-first remains the primary hierarchy;
2. capability does not replace levels;
3. exactly four slots exist;
4. architecture is a frame;
5. composition is static;
6. contracts and module manifests exist;
7. module-owned knowledge skills are preserved;
8. workflows use facet-role vocabulary rather than hardcoding selected implementations;
9. there is no K-style Kind taxonomy or cross-level K decision register.

## Shared systematic weakness

Both runs violate the inherited L0/L1 requirement that Core and Architecture remain free of concrete technology implementation vocabulary except the fixed platform vocabulary.

This is not a one-run accident.

Run-01 contains examples such as:

- `IExceptionHandler` / ASP.NET Core in Core error handling;
- ASP.NET Core authentication / Identity / Data Protection in Core security;
- `WebApplicationFactory` in Core testing;
- ASP.NET Core / `IActionResult` / Controllers in Architecture boundaries.

Run-02 repeats the same class of defect:

- `IExceptionHandler` and concrete problem-details implementation types in Core HTTP policy;
- ASP.NET Core authentication / Identity / Data Protection in Core security;
- `WebApplicationFactory` in Core testing;
- ASP.NET Core / `IActionResult` in neutral Architecture roles;
- ASP.NET Core Controllers in the architecture frame.

Both generated structure checkers report PASS despite those facts, so the checker design is part of the systematic defect.

## Enforcement comparison

Run-01 has a richer package checker and more detailed module-driven enforcement, but:

- its PreToolUse matcher omits PowerShell;
- its BOM-prefixed hook JSON input fails;
- its launcher/root resolver can prefer the original project root, which is unsafe for active worktrees.

Run-02 improves some of this:

- PreToolUse includes Bash and PowerShell;
- hook JSON input tolerates a UTF-8 BOM;
- the helper resolves root from script location.

But Run-02 still has important enforcement holes documented in `DEFECT_DOSSIER.md`.

## Conclusion

The two runs are substantially different as file decompositions, but they are not competing interpretations of L1.

Run-02 is selected as the more maintainable baseline. Run-01 is evidence that useful V2 detail can be retained with a lower always-loaded surface and must inform the *quality bar*, not provide files to copy.
