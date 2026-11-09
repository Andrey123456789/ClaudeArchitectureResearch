"""Evidence dispositions for C02. Each range was read with the records citing it."""
F = '.claude/skills/ef-core/SKILL.md'


def d(c, a, b, quote, note):
    return {'candidate': c, 'path': F, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


DEM = 'measured, or clearly demonstrated, to be material'
RAW = 'measured or clearly demonstrated performance need'
TAB = 'Measured or clearly demonstrated hot query'
DISPOSITIONS = [
    d('M', 255, 258, DEM, 'Compiled-query line aligned with RUN-008; "not merely because a query runs frequently" kept.'),
    d('M', 404, 406, RAW, 'Performance branch aligned; first branch and parameterization kept.'),
    d('M', 416, 428, TAB, 'Quick table row aligned with the section; other rows unchanged.'),
    d('M1', 258, 260, DEM, 'Compiled-query line aligned with RUN-008.'),
    d('M1', 386, 389, RAW, 'Performance branch aligned; parameterization kept.'),
    d('M1', 424, 440, TAB, 'Quick table row aligned with the section; other rows unchanged.'),
    d('L0', 146, 146, DEM, 'Compiled-query line aligned with RUN-008.'),
    d('L0', 233, 233, RAW, 'Performance branch aligned; parameterization kept.'),
    d('L1', 92, 92, DEM, 'Compiled-query line aligned with RUN-008.'),
    d('L1', 93, 93, RAW, 'Performance branch aligned; parameterization kept.'),
    d('L1', 155, 169, TAB, 'Quick table row aligned with the section; other rows unchanged.'),
    d('K0', 220, 220, 'measured, or clearly demonstrated, to matter', 'Compiled-query line aligned with RUN-008; "not to queries that merely run often" kept.'),
    d('K0', 344, 344, RAW, 'Performance branch aligned; parameterization kept.'),
    d('K0', 352, 365, TAB, 'Quick table row aligned with the section; other rows unchanged.'),
    d('K0', 354, 365, TAB, 'Quick table row aligned with the section; other rows unchanged.'),
    d('K1', 216, 216, RAW, 'Performance branch aligned; parameterization kept.'),
]
