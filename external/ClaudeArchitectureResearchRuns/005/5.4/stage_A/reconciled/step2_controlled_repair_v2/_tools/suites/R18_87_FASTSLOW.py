"""R18: item 8.7 fast and slow external tests. No template change; present in all six, L1 line kept."""
from suitelib2 import anchors


def run(ctx):
    f = '.claude/skills/dotnet-testing/SKILL.md'
    anchors(ctx, 'slow external tests kept out of fast runs', {'M': (f, ['Keep slow or unreliable external-system tests separate from ordinary fast runs']), 'M1': (f, ['Keep slow or unreliable external-system tests separate from ordinary fast runs']), 'L0': (f, ['keep slow or unreliable external tests out of the fast run']),
                                                               'L1': (f, ['keep slow or flaky external tests out of the fast run']), 'K0': (f, ['Keep slow or unreliable external-system']), 'K1': (f, ['Keep slow or unreliable external-system tests out of ordinary fast runs'])})
