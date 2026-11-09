"""Source review for R02 (contract steps D and E). Quotes are re-checked mechanically on current bytes at every later gate."""
CANDS = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
FLOW = '.claude/skills/git-workflow/SKILL.md'
REVIEW = []
GOV020 = {'M': 'inspect the relevant repository state', 'M1': 'inspect the relevant repository', 'L0': 'inspect the relevant repository state', 'L1': 'inspect the relevant state', 'K0': 'inspect the relevant repository state', 'K1': 'inspect the relevant state'}
GOV019 = {'M': 'Never discard, overwrite, reset, clean, or otherwise destroy user work', 'M1': 'Never discard, overwrite, reset, clean, or otherwise destroy user work', 'L0': 'Never discard, overwrite, reset, clean, or otherwise destroy user work',
          'L1': 'Never discard, overwrite, reset, clean, stash away, or otherwise destroy user work', 'K0': 'Never discard, overwrite, reset, clean or otherwise destroy user work', 'K1': 'Never discard, overwrite, reset, clean, stash away, or otherwise destroy user work'}
GOV014 = {'M': 'Keep changes focused on the requested scope', 'M1': 'Keep changes focused on the requested scope', 'L0': 'Keep changes focused on the requested scope', 'L1': 'Keep changes focused on the requested scope', 'K0': 'Keep changes focused on the requested scope', 'K1': 'Changes must stay within the requested scope'}
# Quote narrowed at R05, which rewords the headless sentence; the clause it anchors stays.
GOV017 = {c: 'policy-compliant non-Reserved path' for c in CANDS}
for c in CANDS:
    REVIEW.append(dict(policy='GOV-015', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', 'pre-approved it with a named operation and scope'), ('CLAUDE.md', 'is not that authority'), (FLOW, 'generic approved workflow is not enough')],
                       note='Permits only what the policy permits: a pre-approval naming operation and scope is an explicit request made in advance. The former approved-workflow branch is gone.',
                       counterexample='A pipeline step labelled approved runs git reset --hard with no named request: forbidden now, was arguably allowed before. A request to force-push feature/x does not reach main.'))
    REVIEW.append(dict(policy='GOV-015', candidate=c, verdict='HOLDS_WITH_NOTE', quotes=[('CLAUDE.md', 'pre-existing uncommitted changes (staged, unstaged, untracked)'), ('CLAUDE.md', 'pause safely'), ('CLAUDE.md', 'Changes made during the current task are not this condition')],
                       note='User-approved addition beyond the policy text (register HQ-01). Stronger than GOV-015 in all six alike; classification records it as a workflow remainder, not a strictness difference between candidates. Scoped to tasks that change files or repository state; see UNRESOLVED_DECISIONS.jsonl.'))
    REVIEW.append(dict(policy='GOV-016', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', 'Parallel implementation work must use separate branches or worktrees')], note='Line untouched.'))
    REVIEW.append(dict(policy='GOV-019', candidate=c, verdict='HOLDS', quotes=[(FLOW, GOV019[c]), (FLOW, 'do not stash, reset, clean, or commit them on your own')], note='Task-start step adds no route that discards user work; option (a) commits only inside the scope the user names.'))
    REVIEW.append(dict(policy='GOV-020', candidate=c, verdict='HOLDS', quotes=[(FLOW, GOV020[c])], note='Inspection duty untouched; destructive operations add a re-check before execution.'))
    REVIEW.append(dict(policy='GOV-014', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', GOV014[c])], note='Option (a) never widens scope on its own: it needs the user to name the scope.'))
    REVIEW.append(dict(policy='GOV-017', candidate=c, verdict='HOLDS', quotes=[('CLAUDE.md', GOV017[c]), ('CLAUDE.md', 'pause safely')], note='Headless pause on a dirty tree is a stop, not a Reserved decision. Neither clause grants authority for the other (R05 repeats this check).'))
