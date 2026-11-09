"""Source review for R09. K1 only."""
EF = '.claude/skills/ef-core/SKILL.md'
RULE = '.claude/rules/backend/runtime.md'
REVIEW = [dict(policy='RUN-008', candidate='K1', verdict='HOLDS', quotes=[(RULE, 'are introduced only for a measured or clearly demonstrated need'), (EF, 'measured, or clearly demonstrated, to be material'), (EF, 'do not add them speculatively')],
               note='The owner line already said measured or clearly demonstrated. The skill line said measured only, which narrowed the policy. Now the two agree and the record can read as canonical.',
               counterexample='A documented throughput target shows the query cost before any profile exists: allowed by the policy, was refused by the old skill line, now allowed. A query that only runs often: refused by both.')]
