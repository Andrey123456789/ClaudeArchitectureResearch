# Design amendments (append-only)

`DESIGN_AND_EXPECTATIONS.md` is left unchanged; its SHA-256 is logged in `STATE.json`. Each amendment below is written before the case it adds is run.

## A1 — 2026-11-08, before any candidate session; after SYN-DX4 only

**Added rows:** `SYN-ASKHOST` and `SYN-ASKHOSTM` (synthetic hook returning `ask`; `git status --short` and the marker command, both with a matching allow rule; `--permission-prompts host --permission-prompt-tool stdio`).

**Why:** the stdio approval surface is new to this harness. Shaking it out on a synthetic hook avoids consuming a candidate case on a harness defect.

**Expected:** for each command the host emits a `can_use_tool` request for that exact command; the harness answers deny; the command is **not executed**; the marker is absent. A matching allow rule must not bypass the request.

## A2 — 2026-11-08, after attempt 1 and before any attempt-2 session

**What attempt 1 showed.** All fault rows behaved as predeclared, but the 7 rows that expected the marker command to run did not: `SYN-DX2M` and `<C>-S-A2` for all six candidates. The host's own permission system refused the command after the hook had passed it: `Output redirection to '…recheck_marker.txt' needs approval`. An exact allow rule for `echo … > file` does not cover output redirection on this host. In `SMOKE` this appeared as a `can_use_tool` request with no hook reason, which the harness denied.

**Attribution.** Test harness design (choice of marker command), through a host permission rule. Not the candidates, and not a hook defect.

**Consequence for evidence.** In attempt 1 the marker command could not have succeeded under these flags whatever the hook did, so "marker absent" in the attempt-1 `D1M`, `D1XM`, `D3M` and `SYN-DX*M` rows does not discriminate. Those rows keep their recorded status and are not used as file-system proof.

**Attempt 2.** New folders `runs/<CASE>__a2/`; attempt-1 folders are never touched and stay in the matrix as superseded records.
- Marker operation becomes `touch recheck_marker.txt`, with an exact allow rule.
- New control `SYN-SHIM` / `SYN-SHIMM`: hook exits 0 with no decision; `npm --version` and the marker command, both with exact allow rules. Expected: both **executed**; `npm_shim_marker.txt` and `recheck_marker.txt` present. It proves that, under these flags, the marker can appear and that the `npm` shim is the program the host's shell runs. It runs first; if the marker cannot be created, the remaining attempt-2 sessions do not run.
- Re-run: `<C>-D1`, `<C>-D1X`, `L1-D3`, `SYN-DX1..5`, `<C>-SMOKE`. All expectations are unchanged. `SYN-DX2M` must now show the marker present. `SYN-ASKNONE` and `SYN-ASKHOST` are not re-run: their refusal comes from the hook's `ask`, recorded with `decision_reason_type: hook` or `permission_denied`.
- Effective result for a row = highest attempt.

**Parser correction.** Hook events are attributed to a tool use by their `hook_started` position. The attempt-1 window also caught the previous command's response when the agent issued both commands in one turn (L1-D3 op 2 showed two `cancelled` responses; the stream shows one per command).
