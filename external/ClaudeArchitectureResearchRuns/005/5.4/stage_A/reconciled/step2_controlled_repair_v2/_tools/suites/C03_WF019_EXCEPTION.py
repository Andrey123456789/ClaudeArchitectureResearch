"""C03 regression: WF-019 default and exception, all six. Text anchors for a reading established in the source review, the same scenarios across six, and mutations. No deployment or database runs: execution is NOT_RUN."""
from rcommon import CANDIDATES
from suitelib import mutate_text, ntext, post

PS = '.claude/skills/project-structure/SKILL.md'
OWNER = {'M': '.claude/skills/development-workflow/SKILL.md', 'M1': '.claude/skills/verify/SKILL.md', 'L0': '.claude/skills/delivery-pipeline/SKILL.md', 'L1': '.claude/skills/development-workflow/SKILL.md', 'K0': '.claude/skills/delivery-pipeline/SKILL.md', 'K1': '.claude/skills/delivery-change/SKILL.md'}
DEFAULT = {'M': 'Do not apply production database migrations automatically from normal application startup by default', 'M1': 'production database migrations are not applied automatically from normal application startup by default', 'L0': 'Do not apply production database migrations automatically from normal application startup by default', 'L1': 'Do not apply production database migrations automatically from normal application startup by default', 'K0': 'Do not apply production database migrations automatically from normal application startup by default', 'K1': 'Production database migrations must not run automatically from normal application startup by default'}
EXPLICIT = {'M': 'production migration is an explicit deployment operation', 'M1': 'production migration is an explicit deployment operation', 'L0': 'Production migration is an explicit deployment operation', 'L1': 'production migration is an explicit deployment operation', 'K0': 'A production migration is an explicit deployment operation', 'K1': 'A production migration is an explicit deployment operation'}
CREDS = {'M': 'using approved credentials', 'M1': 'uses approved credentials', 'L0': "using the project's approved credentials", 'L1': 'using approved credentials', 'K0': "using the project's approved credentials", 'K1': "use the project's approved credentials"}
SEED_OWNER = {'M': ('.claude/rules/persistence.md', 'Never seed Production automatically'), 'M1': ('.claude/rules/persistence-technology.md', 'Never seed Production automatically'), 'L0': ('.claude/rules/3-project/data-lifecycle.md', 'never seed Production automatically'), 'L1': ('.claude/rules/2-technology/persistence/seeding.md', 'never seed Production automatically'), 'K0': ('.claude/rules/backend/persistence.md', 'never seed Production automatically'), 'K1': ('.claude/rules/backend/persistence.md', 'never automatically seed Production')}
SEEDER_NO_SCHEMA = {'M': '.claude/rules/persistence.md', 'M1': '.claude/rules/persistence-technology.md', 'L0': '.claude/rules/3-project/data-lifecycle.md', 'L1': '.claude/rules/2-technology/persistence/seeding.md', 'K0': '.claude/rules/backend/persistence.md', 'K1': '.claude/rules/backend/persistence-technology.md'}
SCAFFOLD_CRED = {'M': 'Do not add Production credentials', 'M1': 'Do not add Production credentials', 'L0': 'Never add Production credentials', 'L1': 'no Production credentials', 'K0': 'Add no Production credentials', 'K1': 'Never add Production credentials'}
SCAFFOLD_STARTUP = 'do not wire automatic Production migration at normal application startup'
SCAFFOLD_STEP = 'separately approved, controlled deployment-time migration step'
EXC_A = "An exception needs the user's explicit request naming it and its scope"
EXC_B = 'recorded through `architecture-decision`'
EXC_C = 'a generic workflow approval is not one'
EXC_D = 'it never allows Development seeding in Production'
OLD_SCAFFOLD = ['Production migration automation', 'no automatic production migration step']


def verdict(text, scenario):
    """Model of the reading on normalized text. It ties the scenarios to the wording; it does not show how an agent behaves."""
    t = text.lower()
    has_default = 'by default' in t and 'normal application startup' in t
    has_exc = all(x.lower() in t for x in (EXC_A, EXC_B, EXC_C))
    absolute = 'never apply production database migrations' in t or 'production migration automation' in t or 'no automatic production migration step' in t
    if scenario == 'startup, no approval':
        return 'REFUSED' if has_default else 'ALLOWED'
    if scenario == 'startup, generic approved workflow':
        return 'REFUSED' if has_default and EXC_C.lower() in t else 'ALLOWED'
    if scenario == 'startup, explicit recorded scoped exception':
        return 'REFUSED' if absolute or not has_exc else 'ALLOWED'
    if scenario == 'controlled deployment-time step, approved credentials':
        return 'REFUSED' if absolute else 'ALLOWED'
    raise KeyError(scenario)


SCENARIOS = {'startup, no approval': 'REFUSED', 'startup, generic approved workflow': 'REFUSED', 'startup, explicit recorded scoped exception': 'ALLOWED', 'controlled deployment-time step, approved credentials': 'ALLOWED'}


def joined(c, root=None):
    return ntext(c, OWNER[c], root) + ' ' + ntext(c, PS, root)


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'WF-019 owner keeps the default, explicit operation, credentials', OWNER[c], [DEFAULT[c], EXPLICIT[c], CREDS[c]], ['Never apply production database migrations'])
        post(ctx, c, 'WF-019 owner states what an exception needs and what it never allows', OWNER[c], [EXC_A, EXC_B, EXC_C, EXC_D])
        post(ctx, c, 'scaffolding bars startup migration and credentials, and leaves a controlled step open', PS, [SCAFFOLD_CRED[c], SCAFFOLD_STARTUP, SCAFFOLD_STEP], OLD_SCAFFOLD)
        post(ctx, c, 'Production seeding ban stays absolute', SEED_OWNER[c][0], [SEED_OWNER[c][1]])
        post(ctx, c, 'seeder still does not migrate schema', SEEDER_NO_SCHEMA[c], ['`Database.Migrate()`', '`EnsureCreated()`'])
        for name, want in SCENARIOS.items():
            got = verdict(joined(c), name)
            ctx.check('scenario: %s' % name, got == want, candidate=c, kind='SEMANTIC', expect=want, actual=got)
        ctx.check('scenario: Development seeding in Production stays refused, exception or not', EXC_D.lower() in ntext(c, OWNER[c]).lower() and SEED_OWNER[c][1].lower() in ntext(c, SEED_OWNER[c][0]).lower(), candidate=c, kind='SEMANTIC')
        ctx.check('scenario: Production credentials at scaffold time stay refused', SCAFFOLD_CRED[c].lower() in ntext(c, PS).lower(), candidate=c, kind='SEMANTIC')
        m = mutate_text(c, OWNER[c], EXC_C, 'any approved workflow counts')
        ctx.check('mutation: generic approval accepted is caught', m is not None and verdict(joined(c, m), 'startup, generic approved workflow') == 'ALLOWED', candidate=c, kind='MUTATION')
        m = mutate_text(c, PS, SCAFFOLD_STARTUP, 'never add Production migration automation')
        ctx.check('mutation: blanket scaffold ban reinserted is caught', m is not None and verdict(joined(c, m), 'controlled deployment-time step, approved credentials') == 'REFUSED', candidate=c, kind='MUTATION')
        m = mutate_text(c, OWNER[c], EXC_A, 'An exception is any wish')
        ctx.check('mutation: scope requirement dropped is caught', m is not None and verdict(joined(c, m), 'startup, explicit recorded scoped exception') == 'REFUSED', candidate=c, kind='MUTATION')
        m = mutate_text(c, PS, SCAFFOLD_CRED[c], 'Add Production credentials')
        ctx.check('mutation: credential ban removed is caught', m is not None and not post(None, c, '', PS, [SCAFFOLD_CRED[c]], (), m), candidate=c, kind='MUTATION')
    ctx.not_run('a real deployment-time migration and a real startup migration against a database', 'no database or deployment in this run; the text obligation is reviewed, not executed')
