"""R07 regression: register item 8.1, Development Swagger UI on an API behavior change. Text only: no application exists in this run, so opening a real UI is NOT_RUN."""
from rcommon import CANDIDATES
from suitelib import mutate_text, post

VERIFY = '.claude/skills/verify/SKILL.md'
SWAGGER = '.claude/skills/swagger/SKILL.md'
UI = {c: 'the Development Swagger UI' for c in CANDIDATES}
UI['L1'] = 'the Development API documentation UI'  # L1 verify is Level 0: technology-neutral wording is a binding property of the candidate


def must(c):
    return ['when a change alters API behavior', 'in Development', 'open %s and confirm it loads' % UI[c], 'even when startup and composition did not change', 'does not apply when the project exposes no such UI',
            'report the check as NOT RUN with the reason', 'never report it as passed']


SW_MUST = ['API behavior change', 'open the Development Swagger UI and confirm it loads', '`verify`']
SW_NOT = ['## Verification after API changes']
SMOKE = {'M': 'Swagger UI loads when the API is expected to expose it', 'M1': 'Swagger UI is reachable when', 'L0': 'Swagger UI loads when the API exposes it', 'L1': 'the Development API documentation UI loads when the stack exposes one', 'K0': 'Swagger UI loads when the API exposes it', 'K1': 'Swagger UI loads when the API exposes it'}


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'verify owns the UI obligation with its condition', VERIFY, must(c))
        post(ctx, c, 'WF-006 smoke clause untouched', VERIFY, [SMOKE[c], 'A successful build alone does not prove runtime composition'])
        post(ctx, c, 'swagger skill states the same trigger and action and points to verify', SWAGGER, SW_MUST, SW_NOT)
        m = mutate_text(c, VERIFY, 'never report it as passed', 'report it as passed')
        ctx.check('mutation: unavailable runtime reported as passed is caught', m is not None and not post(None, c, '', VERIFY, must(c), (), m), candidate=c, kind='MUTATION')
        m = mutate_text(c, VERIFY, 'even when startup and composition did not change', 'only when startup or composition changed')
        ctx.check('mutation: condition narrowed back to startup changes is caught', m is not None and not post(None, c, '', VERIFY, must(c), (), m), candidate=c, kind='MUTATION')
        m = mutate_text(c, SWAGGER, 'open the Development Swagger UI and confirm it loads', 'open the Development Swagger UI')
        ctx.check('mutation: action weakened to open only is caught', m is not None and not post(None, c, '', SWAGGER, SW_MUST, SW_NOT, m), candidate=c, kind='MUTATION')
    post(ctx, 'L1', 'L1 keeps Level 0 neutrality in verify', VERIFY, must('L1'), ['Swagger'])
    ctx.not_run('a real API starts in Development and Swagger UI loads', 'no application or runtime exists in this research run; the obligation is text, its execution is a future experiment')
