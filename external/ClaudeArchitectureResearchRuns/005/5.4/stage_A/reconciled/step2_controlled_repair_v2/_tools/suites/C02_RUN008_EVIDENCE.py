"""C02 regression: RUN-008 evidence wording in EF Core technique text, all six. Text tripwires for a reading established in the source review, mutations, and the same hypothetical task across six."""
from rcommon import CANDIDATES
from suitelib import mutate_text, ntext, post

EF = '.claude/skills/ef-core/SKILL.md'
OWNER = {'M': '.claude/rules/performance.md', 'M1': '.claude/rules/performance.md', 'L0': '.claude/rules/0-core/runtime-principles.md', 'L1': '.claude/rules/0-core/backend-code.md', 'K0': '.claude/rules/backend/csharp.md', 'K1': '.claude/rules/backend/runtime.md'}
OWNER_PHRASE = 'measured or clearly demonstrated need'
DEMONSTRATED = {'M': 'measured, or clearly demonstrated, to be material', 'M1': 'measured, or clearly demonstrated, to be material', 'L0': 'measured, or clearly demonstrated, to be material', 'L1': 'measured, or clearly demonstrated, to be material', 'K0': 'measured, or clearly demonstrated, to matter', 'K1': 'measured, or clearly demonstrated, to be material'}
SPECULATIVE = {'M': 'do not add them speculatively', 'M1': 'do not add them speculatively', 'L0': 'do not add it speculatively', 'L1': 'do not add it speculatively', 'K0': 'do not add them speculatively', 'K1': 'do not add them speculatively'}
RAW = 'measured or clearly demonstrated performance need'
OLD = ['only on a measured hot', 'only a measured hot path', 'only when profiling shows', 'belong to measured hot paths', 'where profiling shows', 'Measured extremely hot query', 'or measured performance justifies it', 'or measurement justifies it', 'or a measured performance need']
HAS_TABLE = ('M', 'M1', 'L1', 'K0', 'K1')


def permits(text, demonstrated_phrase):
    """Model of the reading: a query shown hot by design evidence, with no profile yet. Evidence other than measurement is admitted only when the demonstrated wording is present and the narrowing wording is gone."""
    t = text.lower()
    return demonstrated_phrase.lower() in t and not any(o.lower() in t for o in OLD)


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'RUN-008 owner line kept', OWNER[c], [OWNER_PHRASE])
        post(ctx, c, 'compiled queries: measured or clearly demonstrated, no speculation', EF, [DEMONSTRATED[c], SPECULATIVE[c]], OLD)
        post(ctx, c, 'raw SQL: the performance branch admits demonstrated need; the first branch stays', EF, [RAW, 'cannot express'])
        if c in HAS_TABLE:
            post(ctx, c, 'quick table agrees with the section', EF, ['Measured or clearly demonstrated hot query'])
        ctx.check('same task: a query shown hot by design evidence, no profile yet: allowed', permits(ntext(c, EF), DEMONSTRATED[c]), candidate=c, kind='SEMANTIC')
        ctx.check('same task: a frequently run query with no evidence: refused', SPECULATIVE[c].lower() in ntext(c, EF).lower(), candidate=c, kind='SEMANTIC')
        m = mutate_text(c, EF, DEMONSTRATED[c], 'measured to be material')
        ctx.check('mutation: demonstrated need removed is caught', m is not None and not post(None, c, '', EF, [DEMONSTRATED[c]], OLD, m), candidate=c, kind='MUTATION')
        m = mutate_text(c, EF, SPECULATIVE[c], 'add them freely')
        ctx.check('mutation: speculative use allowed is caught', m is not None and not post(None, c, '', EF, [SPECULATIVE[c]], (), m), candidate=c, kind='MUTATION')
        m = mutate_text(c, EF, RAW, 'measured performance')
        ctx.check('mutation: raw SQL narrowed again is caught', m is not None and not post(None, c, '', EF, [RAW], (), m), candidate=c, kind='MUTATION')
        ctx.check('mutation model: narrowing wording makes the same task refused', not permits(ntext(c, EF) + ' only on a measured hot path', DEMONSTRATED[c]), candidate=c, kind='MUTATION')
