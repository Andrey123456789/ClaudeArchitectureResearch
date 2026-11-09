"""PV2-02 evidence dispositions. Each changed range was read with the records citing it; every record still holds on the new text."""


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


DISPOSITIONS = [
    d('M', '.claude/MAP.md', 111, 111, 'the PreToolUse guard fails closed (`"onFailure": "block"`, so Node.js must be available, and the guard itself blocks hook input it cannot read or classify), advisory hooks fail open',
      'PV2-02 adds that the guard blocks invalid input itself. Exec form, the PostToolUseFailure registration and onFailure block stand unchanged.'),
    d('M', '.claude/skills/template-maintenance/SKILL.md', 36, 46, 'PreToolUse guard also sets `"onFailure": "block"`, so a guard that cannot run',
      'PV2-02 extends the hook sentence with script-level blocking of invalid input. Exec form, registrations, visible failure and onFailure block stand unchanged.'),
    d('M1', '.claude/hooks/pre-tool-use.js', 19, 30, "if (typeof input.tool_name !== 'string') throw new Error('hook input has no tool_name');",
      'PV2-02 adds event, tool_input and command checks around the unchanged tool_name check; a payload without a tool name still fails closed.'),
]
