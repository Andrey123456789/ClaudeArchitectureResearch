"""Evidence dispositions for C03. Each range was read with the records citing it."""
PS = '.claude/skills/project-structure/SKILL.md'
STARTUP = 'do not wire automatic Production migration at normal application startup'


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


OWNER = 'WF-019 default and duties unchanged; the exception sentence is added.'
SCAFFOLD = 'Credential ban kept; startup migration barred; a separately approved controlled step left open.'
DISPOSITIONS = [
    d('M', '.claude/skills/development-workflow/SKILL.md', 101, 105, 'Do not apply production database migrations automatically from normal application startup by default', OWNER),
    d('M', PS, 109, 112, STARTUP, SCAFFOLD),
    d('M1', PS, 90, 92, STARTUP, SCAFFOLD),
    d('L0', '.claude/skills/delivery-pipeline/SKILL.md', 33, 35, 'Do not apply production database migrations automatically from normal application startup by default — in containers or anywhere else.', OWNER),
    d('L1', '.claude/skills/development-workflow/SKILL.md', 42, 42, 'Do not apply production database migrations automatically from normal application startup by default', 'The unqualified "Never" becomes the shared default; the exception sentence is added.'),
    d('L1', PS, 29, 29, STARTUP, SCAFFOLD),
    d('K0', '.claude/skills/delivery-pipeline/SKILL.md', 26, 26, 'Do not apply production database migrations automatically from normal application startup by default.', OWNER),
    d('K0', '.claude/skills/delivery-pipeline/SKILL.md', 26, 27, 'Do not apply production database migrations automatically from normal application startup by default.', OWNER),
    d('K0', PS, 29, 29, STARTUP, SCAFFOLD),
    d('K1', '.claude/skills/delivery-change/SKILL.md', 34, 34, 'Production database migrations must not run automatically from normal application startup by default.', OWNER),
    d('K1', PS, 40, 40, STARTUP, SCAFFOLD),
]
