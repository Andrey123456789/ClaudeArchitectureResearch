"""R11 regression: item 8.7 CUSTOM_SETTINGS read duty aligned in L0, K0, K1 with M, M1, L1. No new owner, no always-loaded cost, absence stays harmless."""
from rcommon import CANDIDATES
from suitelib import mutate_text, ntext, post

WF = '.claude/skills/development-workflow/SKILL.md'
MUST = {'M': 'read `SPECIFICATION.md` (and `CUSTOM_SETTINGS.md`) before planning or implementing', 'M1': 'read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`', 'L1': 'read `SPECIFICATION.md` (and `CUSTOM_SETTINGS.md`) before planning or implementing',
        'L0': 'read `SPECIFICATION.md` (and any feature specification) and `CUSTOM_SETTINGS.md` before planning or implementing', 'K0': 'read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` before planning or implementing', 'K1': 'read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`'}
NOT = ['when tunable values are involved', 'when it holds values']


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'workflow reads both product sources for a new application or substantial feature', WF, [MUST[c]], NOT)
        t = ntext(c, 'CLAUDE.md')
        ctx.check('CUSTOM_SETTINGS.md is not imported: no always-loaded cost', '@CUSTOM_SETTINGS.md' not in t, candidate=c, kind='STRUCT')
        ctx.check('the rule owner of settings stays with the operating policy, not the workflow', 'CUSTOM_SETTINGS.md' in t, candidate=c, kind='SEMANTIC')
        post(ctx, c, 'reading adds no duty to create or fill the file', WF, [], ['create `CUSTOM_SETTINGS.md`', 'fill `CUSTOM_SETTINGS.md`'])
    for c in ('L0', 'K0', 'K1'):
        m = mutate_text(c, WF, '`CUSTOM_SETTINGS.md` before planning', '`SETTINGS.md` before planning') if c != 'K1' else mutate_text(c, WF, 'and `CUSTOM_SETTINGS.md`', 'and `SETTINGS.md`')
        ctx.check('mutation: read duty removed is caught', m is not None and not post(None, c, '', WF, [MUST[c]], NOT, m), candidate=c, kind='MUTATION')
    ctx.check('model: empty or absent file means nothing to apply, and planning goes on', True, 'The templates ship an empty table; nothing in the workflow requires values.', kind='SEMANTIC')
