"""PV2-01 source review on current v3 bytes: GOV-015 in all six. The hooks were run directly on one fixture matrix (PV2_01 suite); no live
host ran. The ask is enforcement of a prompt, not an authorization: the authority clause in CLAUDE.md decides, and R02 and C04 replay that model."""
GIT_FILES = {'M': '.claude/hooks/dependency-guard.mjs', 'M1': '.claude/scripts/lib/dependency-commands.js', 'L0': '.claude/hooks/claude-hook.mjs', 'L1': '.claude/hooks/pre-shell-command.mjs', 'K1': '.claude/scripts/classify-command.cjs', 'K0': '.claude/hooks/hook.cjs'}
REVIEW = []
for c, rel in GIT_FILES.items():
    REVIEW.append(dict(policy='GOV-015', candidate=c, verdict='HOLDS',
                       quotes=[(rel, 'pre-approved this operation and scope'), ('.claude/skills/git-workflow/SKILL.md', 'asks the user to confirm Git commands it classifies as repository-changing'), ('CLAUDE.md', 'is not that authority')],
                       note=('K0 is the reference: its hook already asked; unchanged.' if c == 'K0' else 'The PreToolUse hook now asks before repository-changing Git with the K0 table; read-only Git runs; an existing deny wins; git-workflow names the hook and says the prompt is not authorization.') +
                       ' GOV-015 (do not run repository-changing Git unless explicitly requested) is carried by the CLAUDE.md authority clause in all six; the ask adds a confirmation point, not a permission.',
                       counterexample='git reset --hard in a shell call with no user request: ' + ('K0 asked before and still asks.' if c == 'K0' else 'before PV2-01 the hook allowed it silently; now it asks with the authority rule, and the clause still forbids running it without an explicit request.')))
