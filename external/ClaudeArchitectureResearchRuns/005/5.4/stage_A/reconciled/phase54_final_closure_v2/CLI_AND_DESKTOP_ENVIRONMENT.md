# CLI and Desktop environment — Phase 5.4 final closure

All observations below come from recorded evidence. The environment probe ran on 2026-11-09 at 12:53 local and is saved as `evidence/ENVIRONMENT_PROBE.txt`. It is static and did not launch the CLI.

## Claude Desktop 4.23118.0.0

| Item | Value | Evidence |
|---|---|---|
| Package | `Claude`, version `4.23118.0.0`, family `Claude_pzs8sxrjxfjjc` | `Get-AppxPackage`, probe |
| Manifest identity | `4.23118.0.0` | `AppxManifest.xml`, SHA-256 `b16bd54990b369d68e8f481e6c912eb9e53a40bb4df5d8bc3b1c17bb361b6d33` |
| Application file version | `4.23118.0` | `app\claude.exe` version resource |
| Install folder created | 2026-11-08 19:21:20 local | Before both Desktop tests |
| Desktop processes | Started 2026-11-09 10:43:26 to 10:45:11 local, all from that package, still running at the probe | Probe process list |

**How this applies to the test window.** v1 ran from 11:26 and v2 from 12:10 local. The Desktop processes started before both and were still running afterwards, from a folder specific to this version.

**Limit.** This is a binding by time. No Desktop log was available (the logs folder is empty), and neither transcript records the Desktop version.

## Claude Code CLI 2.1.317

| Item | Value | Evidence |
|---|---|---|
| Recorded SHA-256 | `26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038` | `phase54_cli317_host_recheck_v1/cli_identity/IDENTITY.json` |
| Size | 338,187,936 bytes | Same record and probe |
| Version output | `2.1.317 (Claude Code)` | Recheck gate, 2026-11-08 |
| File version resource | `2.1.317.0` | Probe |
| Authenticode | `Valid`, `Anthropic, PBC` | Probe |
| Path during the recheck | `...\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\2.1.317\a33aa5518497\claude.exe` | Recheck |
| Path at closure | `...\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\claude-code\2.1.317\a33aa5518497\claude.exe` | Probe |
| On PATH | No `claude` command | Probe |

The path changed, while hash, size and write time did not. Both older recorded paths no longer exist. Identify this binary by hash.

**Headless recheck.** All 51 sessions passed the identity gate before and after the session, with one hash and one version seen. Each session's `system/init` event reports 2.1.317.

**Previous version, for comparison only.** CLI 2.1.293, SHA-256 `8693c4a02dde7441d0066ede68af8ddfc408bb982d77e12b506286268224e6fa`. It is where HOST-01 occurred. It was not executed in this task.

## Auto mode

| Session | Transcript | Mode evidence | Applies to |
|---|---|---|---|
| v1, Allow | `41e9d77f-7c86-43f6-9462-5848bdaa0cfb`, SHA-256 `49454562257a9949e84789ca88d76430254360e910803c1ad77aaea94776403e` | `permissionMode: auto` (6 of 6 values); entrypoint `claude-desktop`; operator confirmed | K0 |
| v2, Deny | `9fe6ddea-d2e5-442a-b5b3-d50708fcc695`, SHA-256 `fad0f2050948dc2cbc431d0608b97fff716873ae81b7f4cfddf4352181ca5cac` | `permissionMode: auto` (2 of 2 values); entrypoint `claude-desktop`; `Auto` visible in the screenshot | K0 |

Headless recheck sessions were not in Auto mode. They used `--permission-prompts none` or the SDK stdio surface, with Haiku 5.5. The v2 screenshot shows Opus 5.5 selected for the Desktop session.

## Explicit limits of host and process verification

- **No process record names a test session.** Four 2.1.317 CLI processes from the hashed path were running at the probe, started 10:45, 11:25, 12:09 and 12:39 local. The 11:25 and 12:09 starts are consistent with v1 and v2, but no process command line contains either session id. This is consistent, not proven.
- **What does show the Desktop sessions' CLI.** Each transcript reports version 2.1.317, and the only 2.1.317 binary present has the recorded hash and the 2026-11-08 write time. The hash was not captured per session in Desktop as it was in the headless gate.
- **Whether a person saw or clicked something is not in any transcript.** It comes from the screenshot and the operator's statements in chat.
- **Permission overrides.** The `no_local_permission_rule_file` check covers `.claude/settings.local.json` in the work folder only. User-level settings were not examined.
- **Environment probe timing.** The probe describes the machine at closure. It is not a recording made during the tests.
- **Single platform.** Windows 11 Pro 10.0.26200 only.
- **Host dependence.** Fail-closed hook behavior is a property of CLI 2.1.317 and must be re-checked whenever the version changes.
