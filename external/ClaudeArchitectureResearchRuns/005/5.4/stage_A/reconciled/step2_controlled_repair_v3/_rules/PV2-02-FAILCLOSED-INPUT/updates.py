"""PV2-02 added claims: script-level fail-closed handling of invalid shell PreToolUse input, one per changed candidate. Classified as the
peer records of the same behavior (L0 FG-L0-69195df14f, M FG-M-f268d4b313: EXTRA_WORKFLOW, MUST). Existing records stay true and are unchanged."""
RULE = 'PV2-02-FAILCLOSED-INPUT'
UPDATES = {}
ADDED = [
    dict(source_key='V3A-M-001', candidate='M', rule=RULE, classification='EXTRA_WORKFLOW', modality='MUST', domain='WORKFLOW_ENFORCEMENT',
         claim_text='The shell PreToolUse dependency guard blocks (exit 2) hook input it cannot read or classify: empty or non-JSON input, JSON that is not an object, an event the script does not handle, and a PreToolUse Bash or PowerShell call with no tool_name, no tool_input object or no non-empty command string. A PreToolUse call for another tool is allowed; onFailure block stays the backstop for a crash or timeout.',
         path='.claude/hooks/dependency-guard.mjs', quote='The dependency guard cannot classify this shell call, so it fails closed',
         canonical_coverage=[], related_policy_ids=['DEP-025'], extra_fragment='Script-level fail-closed handling of invalid shell hook input.', extra_fragment_kind='EXTRA_WORKFLOW',
         distinguishing_scenario='A PreToolUse payload for Bash with no command: before PV2-02 the guard exited 0; now it exits 2 with the reason.', trigger='A PreToolUse shell hook payload reaches the guard.', exceptions='Another tool than Bash or PowerShell: nothing to gate, allowed.', confidence='HIGH',
         review_reading='dependency-guard.mjs validates the payload before classification and calls invalidInput (blockTool, exit 2) for each listed case; the PV2_02 suite ran every case directly.',
         review_phrases=['The dependency guard cannot classify this shell call, so it fails closed', "if (!['Bash', 'PowerShell'].includes(input.tool_name)) done();", 'PreToolUse hook input has no non-empty tool_input.command string']),
    dict(source_key='V3A-M1-001', candidate='M1', rule=RULE, classification='EXTRA_WORKFLOW', modality='MUST', domain='WORKFLOW_ENFORCEMENT',
         claim_text='The PreToolUse hook denies a shell call whose hook input is malformed: not a JSON object, an event other than PreToolUse, no tool_name, or for Bash or PowerShell no tool_input object or no non-empty command string. Another tool has nothing to gate and is allowed; onFailure block stays the backstop for a crash or timeout.',
         path='.claude/hooks/pre-tool-use.js', quote="throw new Error('shell hook input has no non-empty tool_input.command string')",
         canonical_coverage=[], related_policy_ids=['DEP-025'], extra_fragment='Script-level fail-closed handling of invalid shell hook input.', extra_fragment_kind='EXTRA_WORKFLOW',
         distinguishing_scenario='A PreToolUse payload for Bash with a blank command: before PV2-02 the hook allowed it; now it returns deny.', trigger='A PreToolUse hook payload reaches pre-tool-use.js.', exceptions='Another tool than Bash or PowerShell: nothing to gate, allowed.', confidence='HIGH',
         review_reading='pre-tool-use.js throws for each listed case and the catch returns denyOnFailure (permissionDecision deny); the PV2_02 suite ran every case directly.',
         review_phrases=["if (input.hook_event_name !== 'PreToolUse') throw new Error(", 'shell hook input has no tool_input object', 'shell hook input has no non-empty tool_input.command string']),
]
