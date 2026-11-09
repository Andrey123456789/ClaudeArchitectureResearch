"""Source review for R05."""
FLOW = '.claude/skills/architecture-decision/SKILL.md'
CANDS = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
DELEG = {'M': 'Delegated', 'M1': 'Delegated', 'L0': 'Delegated', 'L1': 'Delegated', 'K0': 'Delegated', 'K1': 'Delegated'}
REVIEW = []
for c in CANDS:
    REVIEW.append(dict(policy='GOV-017', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', 'explicitly approved that specific change beforehand'), ('CLAUDE.md', 'a broad or vague instruction is not approval'), ('CLAUDE.md', 'Never make or approve a new Reserved decision there'), (FLOW, 'quoting the approving text and its scope')],
                       note='Policy: Reserved changes require explicit approval and headless runs must not silently alter architecture. A specific prior approval is explicit approval, and it is recorded and logged, so nothing happens silently. The word silently, which read as a text difference between candidates, is gone from all six.',
                       counterexample='Headless prompt "do whatever is needed" and the task needs a new DbContext: stop that part. Prompt "add messaging with queue X, approved" and work turns up a choice of a second database: messaging proceeds, the database choice stops.'))
    REVIEW.append(dict(policy='GOV-015', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', 'general task approval, or a workflow step that mentions committing is not that authority')], note='Falsification: does a Reserved approval also authorize a commit? No. A Reserved approval is a task approval, and the Git clause refuses that as Git authority. The reverse does not hold either: a Git request carries no Reserved approval.'))
