"""Source review for R10. L0 only."""
PS = '.claude/skills/project-structure/SKILL.md'
DP = '.claude/skills/delivery-pipeline/SKILL.md'
REVIEW = [dict(policy='WF-019', candidate='L0', verdict='HOLDS', quotes=[(PS, 'do not wire automatic Production migration at normal application startup'), (PS, 'a separately approved, controlled deployment-time migration step belongs to `delivery-pipeline`'), (DP, 'Do not apply production database migrations automatically from normal application startup by default'), (DP, 'Deployment never runs Development seeding in Production')],
               note='WF-019 bars automatic application at normal startup by default and treats production migration as an explicit deployment operation with approved credentials. The old scaffold line barred all automation, so a deliberate deployment step broke L0 while meeting WF-019 (audit counterexample, verified at source). The word approved comes from the register.',
               counterexample='An explicit deployment step generated at scaffold time with approved credentials: allowed now, refused before. Database.Migrate at Production startup: refused before and now.'),
          dict(policy='SEC-001', candidate='L0', verdict='HOLDS', quotes=[(PS, 'Never add Production credentials')], note='Credentials ban kept in the same sentence.')]
