"""Source review for R11."""
WF = '.claude/skills/development-workflow/SKILL.md'
READ = {'L0': 'read `SPECIFICATION.md` (and any feature specification) and `CUSTOM_SETTINGS.md` before planning or implementing', 'K0': 'read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` before planning or implementing', 'K1': 'read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`'}
INVENT = {'L0': 'Do not silently invent a tunable value', 'K0': 'Do not silently invent a tunable value', 'K1': 'Must not silently invent a tunable value'}
STORE = {'L0': 'Never store secrets', 'K0': 'must not contain secrets', 'K1': 'Must not store in `CUSTOM_SETTINGS.md`'}
REVIEW = []
for c in READ:
    REVIEW.append(dict(policy='GOV-002', candidate=c, verdict='HOLDS_WITH_NOTE', quotes=[(WF, READ[c])], note='GOV-002 requires reading SPECIFICATION.md only. Reading CUSTOM_SETTINGS.md is a user-approved workflow remainder (register 8.7), now equal in all six within the same trigger. The classification carries it as a remainder.',
                       counterexample='Before: a new feature with no tunable value mentioned: L0, K0 and K1 could skip the file, M, M1 and L1 could not. After: all six read it. The template file has an empty table: nothing to apply, and work goes on.'))
    REVIEW.append(dict(policy='GOV-010', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', INVENT[c])], note='Owner untouched; the workflow adds no second owner.'))
    REVIEW.append(dict(policy='GOV-011', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', STORE[c])], note='Owner untouched.'))
    REVIEW.append(dict(policy='GOV-021', candidate=c, verdict='HOLDS', quotes=[('.claude/skills/custom-settings/SKILL.md', 'custom')], note='Synchronization workflow untouched; reading is not a change.'))
    REVIEW.append(dict(policy='GOV-007', candidate=c, verdict='HOLDS', quotes=[(WF, 'SPECIFICATION.md')], note='Durable source sync untouched.'))
