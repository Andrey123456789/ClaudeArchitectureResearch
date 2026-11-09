"""R05 regression: HQ-04 / GOV-017 headless Reserved approval. Text postconditions plus a decision table for the approved reading. Live headless behavior is NOT_RUN."""
from rcommon import CANDIDATES
from suitelib import mutate_text, post

SKILL = '.claude/skills/architecture-decision/SKILL.md'
MUST = ['explicitly approved that specific change beforehand', 'naming the change and its scope', 'a broad or vague instruction is not approval', '`architecture-decision`', 'never make or approve a new reserved decision',
        'on an unexpected reserved choice, stop that part of the work', 'policy-compliant non-reserved path', 'every unresolved decision request', 'decision log']
NOT = ['never make a reserved decision silently', 'never silently make', 'never make a reserved decision:']
FLOW_MUST = ['already holds an explicit approval of that specific change and its scope', 'quoting the approving text and its scope', 'implement only that scope', 'decision log in the final report', 'is not approval', 'do not decide it', 'list the decision request as unresolved']


def decide(mode, grant, change, scope_ok=True):
    """Approved reading. grant: None, 'vague', or the specific change approved."""
    if mode == 'interactive':
        return 'IMPLEMENT_RECORD' if grant == change else 'DECISION_REQUEST'
    if grant == change and scope_ok:
        return 'IMPLEMENT_RECORD_LOG'
    return 'STOP_THAT_PART_REPORT'


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'CLAUDE.md headless Reserved clause', 'CLAUDE.md', MUST, NOT)
        post(ctx, c, 'architecture-decision headless procedure', SKILL, FLOW_MUST)
        m = mutate_text(c, 'CLAUDE.md', 'a broad or vague instruction is not approval', 'a broad instruction counts as approval')
        ctx.check('mutation: vague approval accepted is caught', m is not None and not post(None, c, '', 'CLAUDE.md', MUST, NOT, m), candidate=c, kind='MUTATION')
        m = mutate_text(c, 'CLAUDE.md', 'Never make or approve a new Reserved decision there', 'You may make a new Reserved decision there')
        ctx.check('mutation: new Reserved decision permitted is caught', m is not None and not post(None, c, '', 'CLAUDE.md', MUST, NOT, m), candidate=c, kind='MUTATION')
        m = mutate_text(c, SKILL, 'quoting the approving text and its scope', 'noting it')
        ctx.check('mutation: approval evidence dropped is caught', m is not None and not post(None, c, '', SKILL, FLOW_MUST, (), m), candidate=c, kind='MUTATION')
        # Interaction: Reserved approval never carries Git authority, and the reverse.
        post(ctx, c, 'Git authority clause stays independent of Reserved approval', 'CLAUDE.md', ['general task approval, or a workflow step that mentions committing is not that authority'])
    A, B = 'adopt messaging', 'adopt a second database'
    ctx.check('headless, specific prior approval: implement, record, log', decide('headless', A, A) == 'IMPLEMENT_RECORD_LOG', kind='MODEL')
    ctx.check('headless, vague prompt: stop that part', decide('headless', 'vague', A) == 'STOP_THAT_PART_REPORT', kind='MODEL')
    ctx.check('headless, no approval: stop that part', decide('headless', None, A) == 'STOP_THAT_PART_REPORT', kind='MODEL')
    ctx.check('headless, approval for A does not reach B', decide('headless', A, B) == 'STOP_THAT_PART_REPORT', kind='MODEL')
    ctx.check('headless, beyond the approved scope: stop', decide('headless', A, A, scope_ok=False) == 'STOP_THAT_PART_REPORT', kind='MODEL')
    ctx.check('interactive, explicit instruction: implement and record', decide('interactive', A, A) == 'IMPLEMENT_RECORD', kind='MODEL')
    ctx.check('interactive, no approval: Decision Request', decide('interactive', None, A) == 'DECISION_REQUEST', kind='MODEL')
    ctx.not_run('live headless run implements only the approved change and writes the decision log', 'needs a live Claude runtime; kept as a future experiment')
