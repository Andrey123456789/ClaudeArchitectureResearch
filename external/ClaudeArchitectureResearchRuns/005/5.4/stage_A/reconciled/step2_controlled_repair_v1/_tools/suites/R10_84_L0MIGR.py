"""R10 regression: item 8.4, L0 production migrations aligned with WF-019."""
from suitelib import mutate_text, post

PS = '.claude/skills/project-structure/SKILL.md'
DP = '.claude/skills/delivery-pipeline/SKILL.md'
MUST = ['Never add Production credentials', 'do not wire automatic Production migration at normal application startup', 'separately approved', '`delivery-pipeline`']
NOT = ['Never add Production credentials or Production migration automation']


def run(ctx):
    post(ctx, 'L0', 'scaffold line keeps credentials ban, bars startup migration, leaves a controlled step open', PS, MUST, NOT)
    post(ctx, 'L0', 'WF-019 owner lines kept', DP, ['Do not apply production database migrations automatically from normal application startup by default', 'Production migration is an explicit deployment operation', 'approved credentials', 'Deployment never runs Development seeding in Production'])
    post(ctx, 'L0', 'seeding guarantees kept', '.claude/rules/3-project/data-lifecycle.md', ['The seeder must not call', 'only in the Development en'])
    m = mutate_text('L0', PS, 'do not wire automatic Production migration at normal application startup', 'wire automatic Production migration at normal application startup')
    ctx.check('mutation: startup migration allowed is caught', m is not None and not post(None, 'L0', '', PS, ['do not wire automatic Production migration at normal application startup'], (), m), candidate='L0', kind='MUTATION')
    m = mutate_text('L0', PS, 'Never add Production credentials', 'Add Production credentials')
    ctx.check('mutation: credentials guarantee removed is caught', m is not None and not post(None, 'L0', '', PS, ['Never add Production credentials'], (), m), candidate='L0', kind='MUTATION')
    m = mutate_text('L0', PS, 'do not wire automatic Production migration at normal application startup', 'Never add Production migration automation')
    ctx.check('mutation: blanket ban reinserted is caught', m is not None and not post(None, 'L0', '', PS, MUST, NOT, m), candidate='L0', kind='MUTATION')
    ctx.check('counterexample: an approved explicit deployment step with approved credentials now meets both WF-019 and L0', True, 'The old line refused any automation; WF-019 does not.', 'L0', 'SEMANTIC')
    ctx.check('counterexample: Database.Migrate at Production startup stays refused', True, 'WF-019 and the new line both refuse it.', 'L0', 'SEMANTIC')
