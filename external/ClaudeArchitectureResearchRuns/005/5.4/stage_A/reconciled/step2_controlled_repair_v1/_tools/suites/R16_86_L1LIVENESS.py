"""R16: item 8.6 L1 liveness. Nothing weakened or deleted."""
from rcommon import input_path, sha256_file, wc_path
from suitelib2 import anchors


def run(ctx):
    anchors(ctx, 'normative principle kept', {'L1': ('.claude/rules/0-core/http-api.md', ['Liveness avoids external dependencies whose outage could cause restart loops', 'readiness may depend on capabilities required to serve traffic'])})
    anchors(ctx, 'skill example kept', {'L1': ('.claude/skills/health-check/SKILL.md', ['an endpoint that runs no dependency checks', 'Predicate = _ => false'])})
    for f in ('.claude/rules/0-core/http-api.md', '.claude/skills/health-check/SKILL.md'):
        ctx.check('untouched: %s' % f, sha256_file(wc_path('L1', f)) == sha256_file(input_path('L1', f)), candidate='L1', kind='SOURCE')
