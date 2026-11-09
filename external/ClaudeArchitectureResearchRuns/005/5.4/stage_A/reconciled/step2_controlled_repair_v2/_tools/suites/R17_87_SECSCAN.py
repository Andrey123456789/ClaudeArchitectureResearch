"""R17: item 8.7 security scan minimality. No template change; label sweep only."""
from rcommon import CANDIDATES, input_path, sha256_file, wc_path
from suitelib2 import anchors, check_overlay


def run(ctx):
    f = '.claude/skills/security-scan/SKILL.md'
    for c in CANDIDATES:
        ctx.check('security-scan skill untouched', sha256_file(wc_path(c, f)) == sha256_file(input_path(c, f)), candidate=c, kind='SOURCE')
    anchors(ctx, 'smallest secure change', {'M': (f, ['Prefer the smallest secure change']), 'M1': (f, ['Prefer the smallest secure change']), 'L0': (f, ['Prefer the smallest secure change']), 'L1': (f, ['Recommend the smallest secure change']), 'K0': (f, ['Recommend the smallest secure change']), 'K1': (f, ['Prefer the smallest secure change'])})
    check_overlay(ctx, 'R17-87-SECSCAN')
