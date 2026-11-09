"""PV2-01 added claims: the Git ask in the five candidates that gained it, classified as K0's record of its own Git ask
(FG-K0-3a0bdc2375: CANONICAL_ONLY, MUST_NOT, GOV-015 PARTIAL, SAME). Existing records stay true and are unchanged."""
RULE = 'PV2-01-GIT-GATING'
UPDATES = {}
ADDED = []
CLAIM = 'Repository-changing Git commands receive an ask decision from the PreToolUse hook (K0 table, after global options, wrappers and in every segment of a combined line); read-only Git runs without a Git prompt; an existing deny or block wins. The ask is not authorization: run the operation only when the user explicitly requested it or pre-approved this operation and scope.'
WHERE = {'M': ('.claude/hooks/dependency-guard.mjs', 'if (gitHits.length > 0) askTool(gitAskReason(gitHits));'),
         'M1': ('.claude/scripts/lib/dependency-commands.js', 'return git.length ? { block: false, ask: true, message: gitAskReason(git) } : verdict;'),
         'L0': ('.claude/hooks/claude-hook.mjs', 'if (git.length > 0) ask(gitAskReason(git));'),
         'L1': ('.claude/hooks/pre-shell-command.mjs', "if (gitReason) decide('ask', gitReason);"),
         'K1': ('.claude/hooks/dispatch.cjs', "permissionDecision: 'ask', permissionDecisionReason: reason")}
for c, (path, quote) in WHERE.items():
    ADDED.append(dict(source_key='V3A-%s-010' % c, candidate=c, rule=RULE, classification='CANONICAL_ONLY', modality='MUST_NOT', domain='WORKFLOW_ENFORCEMENT', claim_text=CLAIM, path=path, quote=quote,
                      canonical_coverage=[dict(policy_id='GOV-015', coverage='PARTIAL')], related_policy_ids=['GOV-015'], extra_fragment=None, extra_fragment_kind=None,
                      distinguishing_scenario='git commit -m x in a shell call: before PV2-01 this hook allowed it silently; now it asks with the authority rule, as K0 does. git status still runs without a prompt.',
                      trigger='A Bash or PowerShell PreToolUse call containing a repository-changing Git command.', exceptions='Read-only Git commands; a line an existing guard denies or blocks.', confidence='HIGH',
                      review_reading='The hook classifies Git with the K0 table (identical block, PV2_01 source check) and returns ask only when no dependency or reference guard denied the line; the PV2_01 suite ran the common fixture matrix on all six hooks with the same decision classes.',
                      review_phrases=[quote, 'pre-approved this operation and scope', "const GIT_READ_ONLY = new Set(["] if c != 'K1' else [quote, "const GIT_READ_ONLY = new Set(["]))
# K1 keeps the table in its classifier; the reason text lives there.
ADDED[-1]['review_phrases'] = ["permissionDecision: 'ask', permissionDecisionReason: reason", 'classifier.gitAskReason(']
