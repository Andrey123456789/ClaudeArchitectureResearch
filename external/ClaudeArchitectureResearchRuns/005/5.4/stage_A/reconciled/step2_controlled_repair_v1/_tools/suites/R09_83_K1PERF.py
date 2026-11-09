"""R09 regression: item 8.3, K1 compiled-query technique aligned with RUN-008."""
from suitelib import mutate_text, post

EF = '.claude/skills/ef-core/SKILL.md'
RULE = '.claude/rules/backend/runtime.md'
MUST = ['measured, or clearly demonstrated, to be material', 'do not add them speculatively', 'Measured or clearly demonstrated hot query']
NOT = ['fit only a measured hot path', 'Measured extremely hot query']


def run(ctx):
    post(ctx, 'K1', 'ef-core allows measured or demonstrated need, no speculation', EF, MUST, NOT)
    post(ctx, 'K1', 'RUN-008 owner line kept', RULE, ['compiled queries', 'are introduced only for a measured or clearly demonstrated need'])
    post(ctx, 'K1', 'other specialized performance checks kept', EF, ['inspect round trips, selected columns, N+1 behavior, indexes'])
    m = mutate_text('K1', EF, 'measured, or clearly demonstrated, to be material', 'measured to be material')
    ctx.check('mutation: demonstrated need removed is caught', m is not None and not post(None, 'K1', '', EF, MUST, NOT, m), candidate='K1', kind='MUTATION')
    m = mutate_text('K1', EF, 'do not add them speculatively', 'add them freely')
    ctx.check('mutation: speculative use allowed is caught', m is not None and not post(None, 'K1', '', EF, MUST, NOT, m), candidate='K1', kind='MUTATION')
    ctx.check('counterexample: a query known hot from design data, no profile yet, meets RUN-008 and now also the skill', True, 'A documented throughput requirement shows the cost. RUN-008 allows it; the old line required a measurement.', 'K1', 'SEMANTIC')
    ctx.check('counterexample: a frequently run query with no evidence stays out', True, 'No measurement and no demonstration: neither text allows it.', 'K1', 'SEMANTIC')
