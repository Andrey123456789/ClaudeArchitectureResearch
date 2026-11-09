"""R13: item 8.7 test priority. No template edit: comparison shows no required obligation missing. Anchors guard the compared text."""
from suitelib2 import anchors


def run(ctx):
    anchors(ctx, 'explicit prioritize sentence where it exists', {'M': ('.claude/skills/dotnet-testing/SKILL.md', ['Prioritize meaningful behavior, important edge cases, and risky integrations']),
                                                                  'K0': ('.claude/skills/dotnet-testing/SKILL.md', ['prioritize meaningful behavior, important edge cases and risky integrations']),
                                                                  'K1': ('.claude/skills/dotnet-testing/SKILL.md', ['prioritize meaningful behavior, edge cases, and risky integr'])})
    anchors(ctx, 'canonical coverage rule (TST-011) in the rest', {'M1': ('.claude/rules/testing.md', ['Do not generate low-value tests merely to increase a coverage percentage']), 'L0': ('.claude/rules/0-core/testing-principles.md', ['Do not generate low-value tests merely to increase a coverage percentage']),
                                                                   'L1': ('.claude/rules/0-core/testing.md', ['Do not generate low-value tests merely to raise a coverage percentage'])})
    t = 'missing meaningful tests'
    anchors(ctx, 'review priority', {c: ('.claude/skills/code-review/SKILL.md', [t]) for c in ('M1', 'L0', 'L1', 'K0', 'K1')})
