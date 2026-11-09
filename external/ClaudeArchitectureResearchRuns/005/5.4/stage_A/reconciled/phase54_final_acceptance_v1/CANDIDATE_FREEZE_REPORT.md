# Candidate freeze report — Phase 5.4 final acceptance

**Result: FROZEN and verified.** Six candidates, 448 files, byte-identical to the approved Step 2 v3 templates. No content, structure, line ending or encoding changed.

## 1. Procedure

1. **Source check before copying** (`_tools/freeze_release.py`): each `step2_controlled_repair_v3/candidates/<C>/template/` was re-hashed and compared with `V3_FINAL_MANIFEST.json` (file set and SHA-256). The same check had already passed in step 1 (`predecessor/PREDECESSOR_VERIFICATION.json`, PV-02, PV-06).
2. **Copy**: content-only binary copy (`shutil.copyfile`) to `release/candidates/<C>/template/<same relative path>`. No text-mode handling.
3. **Per-copy verification**: every copy was compared with its source byte for byte (`filecmp.cmp(shallow=False)`) and with the manifest hash; the released tree was listed again to prove no missing or extra file.
4. **Manifest**: `release/CANDIDATE_FREEZE_MANIFEST.json` (per-file SHA-256, bytes, v3 hash, line-ending and BOM profile; per-candidate tree hash; source version; policy-data version; decisions; runtime dependencies) and its sidecar `CANDIDATE_FREEZE_MANIFEST.json.sha256`.
5. **Read-only attribute** set on every released file and on the manifest.
6. **Independent verification**: `release/verify_release.py` (a separate, read-only program that does not import the freeze tool) → PASS, 448/448, v3 byte comparison run (`release_verification/VERIFY_RELEASE_RUN1.json`).
7. **Verifier self-test** (`_tools/verifier_selftest.py`, on copies in the session scratch directory): the untouched copy passes; a flipped bit, an added file, a removed file, an edited manifest and a line-ending conversion each fail; a working copy is created writable and verified; a working copy inside the release is refused; the release still verifies afterwards (`release_verification/VERIFIER_SELFTEST.json`, 9/9 as expected).

## 2. Results

| Candidate | Files (v3 manifest) | Files released | Byte-identical | Missing | Unexpected | Line endings |
|---|---|---|---|---|---|---|
| M | 61 | 61 | 61 | 0 | 0 | 60 LF, 1 empty |
| M1 | 80 | 80 | 80 | 0 | 0 | 79 LF, 1 empty |
| L0 | 71 | 71 | 71 | 0 | 0 | 41 CRLF, 29 LF, 1 empty |
| L1 | 86 | 86 | 86 | 0 | 0 | 85 LF, 1 empty |
| K0 | 63 | 63 | 63 | 0 | 0 | 62 LF, 1 empty |
| K1 | 87 | 87 | 87 | 0 | 0 | 86 LF, 1 empty |

No released file has a UTF-8 BOM (none had one in v3). Architectural identity is preserved because every file is: hooks (M 4, M1 3, L0 2, L1 4, K0 1, K1 1 files under `.claude/hooks/`), checkers and tools, skills, rules, capability modules (M1, L1, K1), agents, root instructions, `settings.json`, `Directory.Build.props`, `Directory.Packages.props`, `.editorconfig`, and L0/L1's `.gitignore`.

## 3. Recorded versions and decisions

Source version, policy-data version, FAIR-01/FAIR-02/CP-01 dispositions and runtime dependencies are recorded in the manifest and summarized in `release/RELEASE_PROVENANCE.md`.

## 4. Independent working copies

Benchmark runs must not run inside `release/`. `release/make_working_copy.py <C> <dest>` verifies the release, copies content only (writable copy), re-hashes the copy and writes `<dest>.provenance.json` outside the copied tree. The self-test confirmed the release is unchanged afterwards.

## 5. Limits

- The freeze proves byte identity with the approved v3 templates. **It does not prove runtime behavior**; that is the subject of `LIVE_HOST_PILOT_REPORT.md`.
- The read-only attribute can be removed by any user; integrity rests on the hashes and `verify_release.py`.
- The two release utilities are not covered by the candidate manifest (they are not candidate files); their hashes are in `RELEASE_PROVENANCE.md` and `FILE_MANIFEST.json`.
- No Git operation of any kind was used.
