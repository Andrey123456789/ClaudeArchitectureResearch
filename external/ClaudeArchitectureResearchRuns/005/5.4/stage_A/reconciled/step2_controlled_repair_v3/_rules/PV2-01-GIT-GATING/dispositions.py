"""PV2-01 evidence dispositions. Each range was read with the records citing it (dependency, reference, fail-closed and map records):
every record still holds; the change adds the Git ask next to the unchanged guards."""


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


MAP = 'PV2-01 adds the Git ask to the hook row; the cited ownership, registration and guard statements stand unchanged.'
HOOK = 'PV2-01 adds Git classification and the ask beside the unchanged dependency and project-reference logic; the cited behavior stands.'
DISPOSITIONS = [
    d('K1', '.claude/MAP.md', 96, 114, 'dependency/reference guard (PreToolUse, fails closed), actual-state checks after edits and shell commands (PostToolUse, PostToolUseFailure), co-change reminders (Stop)', MAP),
    d('K1', '.claude/MAP.md', 100, 114, 'dependency/reference guard (PreToolUse, fails closed), actual-state checks after edits and shell commands (PostToolUse, PostToolUseFailure), co-change reminders (Stop)', MAP),
    d('K1', '.claude/hooks/dispatch.cjs', 65, 78, "process.stderr.write(`Blocked before execution (dependency and project-reference guard):\\n- ${findings.map(describe).join('\\n- ')}\\n`);", HOOK + ' Blocking findings still exit 2; Git findings are filtered out of the block and only ask when nothing blocks.'),
    d('K1', '.claude/hooks/dispatch.cjs', 65, 79, "process.stderr.write(`Blocked before execution (dependency and project-reference guard):\\n- ${findings.map(describe).join('\\n- ')}\\n`);", HOOK + ' Blocking findings still exit 2; Git findings are filtered out of the block and only ask when nothing blocks.'),
    d('L0', '.claude/INSTRUCTION_MAP.md', 97, 97, "compares the active worktree's manifests (tracked and untracked, not ignored) with a per-worktree snapshot kept in the Git directory, validates added and changed manifests, reports removals and moves, routes dependency and project-reference changes;", MAP),
    d('L0', '.claude/hooks/claude-hook.mjs', 331, 348, "else if (['bash', 'sh', 'zsh', 'dash'].includes(program)) inner = args.findIndex(arg => /^-[a-z]*c$/.test(arg));", HOOK + ' Nested-shell parsing keeps its depth limit; Git is classified in the same segments.'),
    d('L1', '.claude/hooks/pre-shell-command.mjs', 171, 172, 'Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout (architecture.layout via project-structure);', HOOK + ' The reference ask is unchanged; a Git reason is appended when the same line also changes the repository.'),
    d('L1', '.claude/hooks/pre-shell-command.mjs', 171, 173, 'Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout (architecture.layout via project-structure);', HOOK + ' The reference ask is unchanged; a Git reason is appended when the same line also changes the repository.'),
    d('L1', '.claude/hooks/pre-shell-command.mjs', 176, 193, "const stateFile = path.join(stateDir, 'dependency-commands.json');", HOOK + ' Deny-once and the 30-minute retry window are unchanged; a retried line that also changes the repository now asks instead of passing silently.'),
    d('L1', '.claude/hooks/pre-shell-command.mjs', 185, 190, "const key = command.trim().replace(/\\s+/g, ' ');", HOOK + ' The identity key of a retried command is unchanged.'),
    d('L1', '.claude/hooks/pre-shell-command.mjs', 185, 194, 'Run the add-dependency workflow first (need, approved technology, latest stable compatible version, deprecation, vulnerability and license checks, approval for commercial or unclear licenses).', HOOK + ' The retry still passes without verifying due diligence for a pure dependency command (the reported limit stands).'),
    d('M', '.claude/MAP.md', 113, 113, 'after any other shell command, and after a failed one, checks the manifests whose content changed since the last check (one initial snapshot per worktree) and reports removed manifests', MAP),
    d('M', '.claude/hooks/dependency-guard.mjs', 2, 5, '//   PreToolUse:  blocks npm installs that bypass peer-dependency resolution', HOOK),
    d('M1', '.claude/MAP.md', 123, 135, 'a shell command is judged by its effect on manifests and project files (content state per worktree in its Git directory), so unrecognized commands, branch switches, removals, and moves are checked', MAP),
    d('M1', '.claude/MAP.md', 124, 124, 'denies dependency commands until `add-dependency` was applied and project-reference commands until `project-structure` was applied;', MAP),
]
