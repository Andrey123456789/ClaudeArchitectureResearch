"""PV2-02 source review on current v3 bytes. DEP-025 is the policy the shell guard enforces in M and M1; fail-closed input handling is the
architecture that keeps that enforcement from being skipped. Hooks were run directly (suite PV2_02); no live host ran."""
REVIEW = [
    dict(policy='DEP-025', candidate='M', verdict='HOLDS', quotes=[('.claude/hooks/dependency-guard.mjs', 'The dependency guard cannot classify this shell call, so it fails closed'), ('.claude/hooks/dependency-guard.mjs', 'bypasses npm peer-dependency resolution')],
         note='The npm peer-bypass block is unchanged and still fires (suite: npm force install, legacy-peer-deps). A shell payload the guard cannot classify used to exit 0 (allowed) or 1 (host-dependent); it now exits 2 in the script, so the DEP-025 guard cannot be skipped by malformed input.',
         counterexample='Before PV2-02: {"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{}} exited 0 with no check. Now: exit 2.'),
    dict(policy='DEP-025', candidate='M1', verdict='HOLDS', quotes=[('.claude/hooks/pre-tool-use.js', 'shell hook input has no non-empty tool_input.command string'), ('.claude/hooks/pre-tool-use.js', "if (input.hook_event_name !== 'PreToolUse')")],
         note='The dependency and project-reference routing and the peer-bypass deny are unchanged. A shell payload with no command, a blank or non-string command, or a non-PreToolUse event used to be allowed; it is now denied through the existing denyOnFailure path.',
         counterexample='Before PV2-02: a Bash payload with tool_input {"cmd": "npm install x --force"} was allowed (no command field). Now: deny.'),
]
