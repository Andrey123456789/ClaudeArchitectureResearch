# Release provenance — phase54-final-v1

This folder is the frozen release of the six normalized Phase 5.4 candidates. The practical C# benchmarks measure these six.

## What was released

| Candidate | Release path | Files | Bytes | Tree SHA-256 |
|---|---|---|---|---|
| M | `candidates/M/template/` | 61 | 401,344 | `e7a6ae1082df120786fcaf77d2bf5967fa31f4febcc69f3912481d2aecac3073` |
| M1 | `candidates/M1/template/` | 80 | 434,179 | `434d3096585c8fa300f1f632b3488048d4facc7577c441f048df5e32e03c6e60` |
| L0 | `candidates/L0/template/` | 71 | 362,128 | `24a5c1ba9c5631bf81a66058d7046aa32a24bd6fa7a21a885a04599c578c24a7` |
| L1 | `candidates/L1/template/` | 86 | 372,163 | `e31d5ab54cf74b94b1cc5f0ad02fb561b0283ff6993ed5ce26473221858fecfa` |
| K0 | `candidates/K0/template/` | 63 | 386,824 | `9764b0729c3f1fa5550ddaa011aa4cad3f9444008fe0451505641c7b9932600c` |
| K1 | `candidates/K1/template/` | 87 | 425,177 | `ef793e9cedbc231c64208b2e8380574afe744b90554fe37a53509c13b71ce76b` |
| **Total** | | **448** | **2,381,815** | |

Tree SHA-256 = SHA-256 over the sorted lines `<relative path>\t<file sha256>\n`. Per-file hashes, sizes, line-ending and BOM profiles are in `CANDIDATE_FREEZE_MANIFEST.json`. The manifest's own hash is in `CANDIDATE_FREEZE_MANIFEST.json.sha256` (`4058f10d670ae1c2f2c02df5e5ab8dba06217d7e0181c02abb0c6a85a1c6537f`).

## Source version

- Source: `stage_A/reconciled/step2_controlled_repair_v3/candidates/<C>/template/`, version `step2-controlled-repair-v3`.
- Source manifest: `step2_controlled_repair_v3/V3_FINAL_MANIFEST.json` (written 2026-11-06T13:52:56, after the last gated change V3-Q10-PACKAGEVERSION-VERSION).
- Every released file equals its v3 source byte for byte and equals the hash in `V3_FINAL_MANIFEST.json`. No file was added, removed, renamed, re-encoded or re-terminated. L0 keeps its 41 CRLF files; the other files keep LF; no file has a BOM.

## Policy-data version

- Canonical policy dataset: `step2-controlled-repair-v3` (`DATASET_MANIFEST.json`), oracle of 196 policies (194 inventory policies + GOV-017/GOV-018; hashes in the manifest's `policy_data_version.oracle`).
- Comparison: `step3-six-way-strictness-v1` — 196 policies, 1,176 cells; `METRICS.json`, `POLICY_SIX_WAY_MATRIX.jsonl` and `POLICY_CELL_INDEX.jsonl` hashes are recorded in the manifest. Step 3's recorded input hashes equal these released files (`PREDECESSOR_VERIFICATION.json`, PV-06).

## Research decisions carried by this release

| Decision | Disposition |
|---|---|
| FAIR-01 | Approved: every enforcement, hook, checker, loading, routing and capability difference is preserved. Nothing harmonized. |
| FAIR-02 | Adopted: one reporting instruction (`benchmark_readiness_fair02_cp01_v1/fair02/RUN_REPORT_INSTRUCTION.txt`, SHA-256 `bb17a883e947b6d259afa683d26a5cbd23343e6a02e26bf93fd239918ffe6710`), appended identically to the task prompt for all six. It is **not** in any template. Report Completeness Score is secondary. |
| CP-01 | Option 0: M keeps IDE0005 detection through `dotnet format`; `GenerateDocumentationFile` not added to M; M comments not patched. |
| Other | CI/CD out of benchmark scope; common engineering contract preserved; Git user-authorization requirements (PV2-01) preserved; no new normative policy. |

## Runtime dependencies (needed to run a candidate as designed)

- **Claude Code host** that runs project hooks from `.claude/settings.json`. The hooks use the exec form `{"command": "node", "args": ["${CLAUDE_PROJECT_DIR}/..."]}` and `onFailure: "block"` on PreToolUse. Host behavior for these keys is recorded in `../LIVE_HOST_PILOT_REPORT.md`, not assumed here.
- **Node.js** on PATH (all hooks and checkers). No candidate declares a minimum version; Step 3 and this task used v26.13.0.
- **.NET SDK 10** (all six target `net10.0` with Central Package Management); checkers call `dotnet` for MSBuild evaluation. CP-01 used SDK 10.0.403.
- **Git** on PATH and a work tree (change detection; commit/push gating).
- No network is needed by the hooks. Package restore by an agent needs a feed; that is a benchmark decision.

## Immutability and use

- Every released file carries the read-only attribute (a guard, not a security boundary). Integrity is proven by hashes, not by the attribute.
- Verify: `python -B verify_release.py` (read-only; exit 0 = PASS). It checks the manifest sidecar, every hash and size, unexpected and missing files, tree hashes, and, when `../../step2_controlled_repair_v3/` is reachable, byte identity with the v3 source.
- Working copy for a run: `python -B make_working_copy.py <C> <empty destination outside this folder>`. It verifies the release first, copies content only (the copy is writable), re-hashes the copy and writes the provenance record next to the destination, never inside it.
- Utility hashes: `verify_release.py` `6fd875440aced485287bf18504084866980c16987e4d8e46163d279d1818d643`, `make_working_copy.py` `56badb894ee625293e3803d7cd456ccf28779cc0a9179f0f559213043f067b41`.
- No Git commit, tag, branch, push or reset was made (the 5.4 folder is not a Git repository).

## What this release does not prove

Byte identity with the approved templates only. It does not prove that any hook stops, prompts or corrects a running agent; see `../LIVE_HOST_PILOT_REPORT.md`.
