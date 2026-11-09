# Iteration 005 replica terminology cleanup

Expected base commit:

`9b781dd711f5f63ce701cc4ae154a1c180b4f2a6`

Changes only terminology/documentation:

- `M-1/M-2` → `M-r1/M-r2` (same for L0/L1/K0/K1);
- explicitly states that the two outputs are independent **replicates**, not candidate variants;
- states that at most one canonical runtime template per architecture is carried into later code generation;
- renames two historical Iteration-004 headings so superseded requirements are not mistaken for current blockers.

Apply from any folder inside the Git repository:

```powershell
powershell -ExecutionPolicy Bypass -File "<path>\apply.ps1"
```

Then review:

```powershell
git diff --check
git diff
```
