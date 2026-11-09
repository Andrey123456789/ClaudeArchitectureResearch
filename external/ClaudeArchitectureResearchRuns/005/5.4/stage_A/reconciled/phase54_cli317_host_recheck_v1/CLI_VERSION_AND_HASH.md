# Claude Code executable: version and hash

**Result: every live session in this recheck ran on Claude Code 2.1.317, SHA-256 `26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038`.** No session used 2.1.293 or another version.

## Executable used

| Item | Value |
|---|---|
| Path passed to every session | `C:\Users\atonkonog\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\2.1.317\a33aa5518497\claude.exe` |
| Version (`--version`) | `2.1.317 (Claude Code)`, exit code 0 |
| File version resource | `2.1.317.0` |
| SHA-256 | `26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038` |
| Size | 338,187,936 bytes |
| Last write | 2026-11-08 19:29:13 +02:00 |
| Authenticode | `Valid`, signer `Anthropic, PBC` |
| Sidecar `.payload` | same SHA-256 and size as measured |

The packaged-app path above and `%APPDATA%\Claude\claude-code\2.1.317\a33aa5518497\claude.exe` are the same file: both report file ID `0x…9600000003ef4a`. There is no `claude` command on PATH, so PATH resolution played no part.

## How the version was enforced

1. **Pinned, no fallback.** `_tools/recheck.py` has one path, one version and one hash as constants. There is no search and no alternative executable.
2. **Gate before and after every session.** The file is re-hashed and asked for its version. Any mismatch aborts with `BLOCKED`. All 51 sessions recorded `gate: PASS` before and after (`runs/<CASE>/result.json`).
3. **Host's own report.** Each session's `system/init` event has `claude_code_version: 2.1.317`. `RECHECK_TOTALS.json` lists the versions and hashes seen across all rows: exactly one of each.
4. **Update guard.** Child sessions ran with `DISABLE_AUTOUPDATER=1`.

The independent audit (`RAW_EVIDENCE_AUDIT.json`, check R1) re-reads the raw streams for this without using the matrix builder.

## Previous version, for comparison only (not executed in any session)

| Item | Value |
|---|---|
| Path | `C:\Users\atonkonog\AppData\Roaming\Claude\claude-code\2.1.293\83cb0bd7fed4\claude.exe` |
| Version | `2.1.293 (Claude Code)` |
| SHA-256 | `8693c4a02dde7441d0066ede68af8ddfc408bb982d77e12b506286268224e6fa` |
| Size | 256,155,808 bytes |
| Authenticode | `Valid`, signer `Anthropic, PBC` |

This file was only hashed and asked for `--version` by `_tools/host_probe.ps1`.

## Evidence

`cli_identity/HOST_PROBE.txt` (raw probe output) · `cli_identity/IDENTITY.json` (first gate record) · `runs/<CASE>/result.json` (`identity_before`, `identity_after`) · `runs/<CASE>/stdout.jsonl` line 1 (`system/init`).
