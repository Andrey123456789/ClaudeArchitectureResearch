"""R13 source comparison. No template edit."""
REVIEW = [dict(policy='TST-011', candidate=c, verdict='HOLDS_WITH_NOTE', quotes=[(rel, q)], note=n) for c, rel, q, n in [
    ('M', '.claude/skills/dotnet-testing/SKILL.md', 'Prioritize meaningful behavior, important edge cases, and risky integrations', 'Explicit prioritize sentence, DEFAULT in a knowledge skill, already MIXED after the M review.'),
    ('K0', '.claude/skills/dotnet-testing/SKILL.md', 'prioritize meaningful behavior, important edge cases and risky integrations', 'Same sentence; audit proposal FG-K0-9146b82c8d moves it to MIXED (R25).'),
    ('K1', '.claude/skills/dotnet-testing/SKILL.md', 'prioritize meaningful behavior, edge cases, and risky integr', 'Same sentence; audit proposal FG-K1-8a61b0db25 moves it to MIXED (R25).'),
    ('M1', '.claude/rules/testing.md', 'Do not generate low-value tests merely to increase a coverage percentage', 'No prioritize sentence in dotnet-testing. TST-011 holds through the rule. The prioritize sentence is an extra, not a required obligation.'),
    ('L0', '.claude/rules/0-core/testing-principles.md', 'Do not generate low-value tests merely to increase a coverage percentage', 'Same as M1.'),
    ('L1', '.claude/rules/0-core/testing.md', 'Do not generate low-value tests merely to raise a coverage percentage', 'Same as M1.')]]
