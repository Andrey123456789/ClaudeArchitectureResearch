"""Source review for R12. K1 only."""
WF = '.claude/skills/persistence-change/SKILL.md'
TECH = '.claude/rules/backend/persistence-technology.md'
REVIEW = [dict(policy='PST-005', candidate='K1', verdict='HOLDS', quotes=[(TECH, 'must not call `Database.Migrate()`'), (WF, 'apply the migration there before any seeding')], note='Schema before seed is kept in the step and in the rule.'),
          dict(policy='PST-006', candidate='K1', verdict='HOLDS', quotes=[(WF, 'Existing seeded rows are not patched automatically')], note='Existing data untouched by this rule. Dropping a local database stays a choice for when a fresh dataset is needed.'),
          dict(policy='PST-009', candidate='K1', verdict='HOLDS', quotes=[(WF, 'create a **new** migration'), (WF, 'start the API against a freshly recreated Development database when seeding or the schema changed')], note='Migration creation and validation of seeding stay. Section C is the validation duty and stays conditional on schema or seed change, as before.',
               counterexample='Behavior-only entity method change: old step 5 still said Apply locally; new step 5 does not fire. Schema change: migration, review, fresh database check all fire.'),
          dict(policy='PST-010', candidate='K1', verdict='HOLDS', quotes=[(WF, 'Review the generated migration as source code')], note='Review duty untouched.'),
          dict(policy='WF-006', candidate='K1', verdict='HOLDS', quotes=[('.claude/skills/verify/SKILL.md', 'database connectivity and initialization succeed')], note='Runtime smoke default for substantial persistence changes stays.')]
