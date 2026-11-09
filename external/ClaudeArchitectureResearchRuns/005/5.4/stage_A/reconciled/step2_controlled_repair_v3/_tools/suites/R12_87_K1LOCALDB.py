"""R12 regression: item 8.7, K1 standalone local database duty removed; migration creation and review, schema before seed, and validation retained (negative test required by the register)."""
from suitelib import mutate_text, post

WF = '.claude/skills/persistence-change/SKILL.md'
TECH = '.claude/rules/backend/persistence-technology.md'
KEEP = ['create a **new** migration', 'dotnet ef migrations add', 'Review the generated migration as source code', 'update the maintained development seeder in the same change', 'before any seeding',
        'Add or update persistence/integration tests', 'start the API against a freshly recreated Development database when seeding or the schema changed', 'check-cochange.cjs', 'Create the initial migration (section B), apply it locally, then let Development startup seed the empty database']
NOT = ['5. Apply locally (`dotnet ef database update']


def run(ctx):
    post(ctx, 'K1', 'local apply is conditional; required duties stay', WF, KEEP + ['When this work runs against a local database', 'Changing the local database is not a goal of its own'], NOT)
    post(ctx, 'K1', 'seeder still does not migrate', TECH, ['must not call `Database.Migrate()`'])
    for old, new, name in (('create a **new** migration', 'optionally create a migration', 'migration creation weakened'), ('Review the generated migration as source code', 'Skim the generated migration', 'migration review weakened'), ('before any seeding', 'after any seeding', 'schema-before-seed inverted'),
                           ('start the API against a freshly recreated Development database when seeding or the schema changed', 'optionally start the API', 'validation weakened')):
        m = mutate_text('K1', WF, old, new)
        ctx.check('negative test: %s is caught' % name, m is not None and not post(None, 'K1', '', WF, KEEP, NOT, m), candidate='K1', kind='MUTATION')
    m = mutate_text('K1', WF, 'When this work runs against a local database, apply the migration there before any seeding', 'Apply locally')
    ctx.check('negative test: unconditional local mutation reinserted is caught', m is not None and not post(None, 'K1', '', WF, ['When this work runs against a local database'], NOT, m), candidate='K1', kind='MUTATION')
    ctx.check('scenario: a behavior-only entity change with no schema or seed effect has no local database duty', True, 'No migration exists, section C does not fire, and step 5 is conditional. The old step 5 still said Apply locally.', 'K1', 'SEMANTIC')
    ctx.check('scenario: a schema change still creates and reviews a migration and validates against a fresh database', True, 'Steps 2, 3 and section C fire. PST-009 and PST-010 hold.', 'K1', 'SEMANTIC')
