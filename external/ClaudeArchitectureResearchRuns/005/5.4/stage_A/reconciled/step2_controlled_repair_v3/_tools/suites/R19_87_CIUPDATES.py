"""R19: item 8.7 CI dependency auto-updates. Rule stays; it is labeled outside practical evaluation; no CI trial."""
from suitelib2 import anchors, check_overlay


def run(ctx):
    anchors(ctx, 'rule kept', {'L0': ('.claude/skills/delivery-pipeline/SKILL.md', ['Do not let CI upgrade packages automatically unless the project adopted automated dependency updates']), 'L1': ('.claude/skills/ci-cd/SKILL.md', ['do not auto-upgrade packages in CI unless automated updates were adopted']),
                               'K0': ('.claude/skills/ci-cd/SKILL.md', ['automatic dependency updates in CI need explicit adoption']), 'K1': ('.claude/skills/delivery-change/SKILL.md', ['no automatic package upgrades unless the project adopted automated updates']),
                               'M': ('.claude/skills/ci-cd/SKILL.md', ['do not upgrade packages automatically in CI unless the project has adopted automated dependency updates']), 'M1': ('.claude/skills/ci-cd/SKILL.md', ['do not upgrade packages automatically in CI unless the project adopted automated dependency updates'])})
    check_overlay(ctx, 'R19-87-CIUPDATES')
    ctx.not_run('CI trial of dependency updates', 'out of study scope by the register; no CI run')
