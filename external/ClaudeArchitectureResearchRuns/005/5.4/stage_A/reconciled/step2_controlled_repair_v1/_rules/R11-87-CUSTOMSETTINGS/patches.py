"""R11 item 8.7: read CUSTOM_SETTINGS.md when planning a new application or substantial feature in L0, K0, K1, as M, M1, L1 do."""
REASON = '8.7 CUSTOM_SETTINGS: conditional read aligned to the unconditional read of M, M1, L1, within the planning trigger'
POLICIES = ['GOV-002', 'GOV-007', 'GOV-008', 'GOV-010', 'GOV-011', 'GOV-021']
WF = '.claude/skills/development-workflow/SKILL.md'
PATCHES = [
    ('L0', WF, "read `SPECIFICATION.md` (and any feature specification) before planning or implementing, and read `CUSTOM_SETTINGS.md` when tunable values are involved.",
     "read `SPECIFICATION.md` (and any feature specification) and `CUSTOM_SETTINGS.md` before planning or implementing."),
    ('K0', WF, "read `SPECIFICATION.md` before planning or implementing, and `CUSTOM_SETTINGS.md` when it holds values.",
     "read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` before planning or implementing."),
    ('K1', WF, "read `SPECIFICATION.md` (and `CUSTOM_SETTINGS.md` when tunable values are involved).",
     "read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`."),
]
