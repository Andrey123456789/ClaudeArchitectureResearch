# PV2-02-FAILCLOSED-INPUT: declaration

Written before the first edit of this change. Authority: kit 74 Part B PV2-02 and decision D-PV2-02 (approved; no further approval needed).

**Change.** The shell PreToolUse guards of M (`.claude/hooks/dependency-guard.mjs` with `hook-io.mjs`) and M1 (`.claude/hooks/pre-tool-use.js`) block invalid hook input in the script itself, in each candidate's own blocking form: M exits 2 with the reason on stderr (its `blockTool`), M1 returns its `permissionDecision: deny` JSON (its `denyOnFailure`). `onFailure: "block"` in `settings.json` stays as the backstop for a crash or timeout.

**Blocked (PreToolUse on a shell tool):** unreadable stdin; empty or whitespace-only input (a byte-order mark alone included); text that is not JSON; JSON that is not an object (array, string, number, null); a missing or non-string `hook_event_name` (M: an event the script does not handle; M1: any event other than `PreToolUse`); a missing or non-string `tool_name`; a missing or non-object `tool_input`; a missing, non-string or blank `tool_input.command`, including a command under another field.

**Not changed.**

- A well-formed shell call is classified exactly as before. Read-only commands such as `git status`, `ls`, `Get-ChildItem` are allowed, and npm peer-bypass and dependency rules are unchanged.
- A PreToolUse call for a tool other than Bash or PowerShell is allowed, as M1 already did: the guard has nothing to gate, and requiring a command there would be wrong.
- M's PostToolUse and PostToolUseFailure branches still need no command. Malformed or non-object input now exits 2 for them too, because the event cannot be known before parsing; exit 2 after a tool call only returns the reason to Claude.
- M's other hooks (`file-change.mjs`, `stop-co-change.mjs`) keep exit 1 on bad input; they are advisory.
- L0, L1, K0 and K1 are not touched.

**Files.** M: `.claude/hooks/hook-io.mjs` (`readInput` takes the handler for invalid input; exit-code contract comment), `.claude/hooks/dependency-guard.mjs` (validation before classification; header comment), `.claude/skills/template-maintenance/SKILL.md` (hook sentence), `.claude/MAP.md` (settings and hook rows). M1: `.claude/hooks/pre-tool-use.js` (event, tool and command checks; header comment).

**Claims and policies.** No canonical policy names hook input handling; the obligation is architecture (fail closed for critical enforcement) linked to `DEP-025`, the dependency guards it protects. Records affected: M `FG-M-f268d4b313`, `FG-M-ddd9d93ab6` context; one added claim each in M and M1 for script-level blocking of invalid input, classified as the peer records of the same behavior (`FG-L0-69195df14f`: EXTRA_WORKFLOW, MUST).

**Expected behavior.** Direct execution: every case in the "Blocked" list gives exit 2 (M) or a deny decision (M1); valid read-only commands give exit 0 with no decision; non-shell tools give exit 0; M PostToolUse without a command gives exit 0. Live host application of exit 2, deny and `onFailure` stays NOT_RUN.

**Remaining differences, not in scope.** L0, K0 and K1 allow a blank command (there is nothing to run); K1 alone blocks a mismatched event; L0 and L1 block a non-shell tool. These are reported, not changed: PV2-02 approves M and M1 only.

**Regression adaptation.** v2 `C06_REVIEW_SETS.py` recorded M and M1 behavior on bad input as a documented difference (`BAD_INPUT`). That difference is what this change removes, so the test now requires all six to fail closed. Negative test: this change's mutations that remove the new checks.
