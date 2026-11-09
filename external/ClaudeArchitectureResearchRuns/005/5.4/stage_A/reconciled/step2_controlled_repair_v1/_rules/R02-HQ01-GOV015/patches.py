"""R02 HQ-01 / GOV-015 and 9.1: one atomic rule across the six working copies. CLAUDE.md is the always-loaded owner, git-workflow holds the procedure."""
REASON = 'HQ-01 / 9.1: specific or bounded authority, task-start check with two options, headless pause, re-check before destructive operations, explicit main rewrite valid'
POLICIES = ['GOV-015', 'GOV-014', 'GOV-016', 'GOV-019', 'GOV-020', 'GOV-017']

AUTH_LONG = """unless the user explicitly requested that operation or pre-approved it with a named operation and scope. A generic "approved workflow", general task approval, or a workflow step that mentions committing is not that authority."""
MAIN = "An explicit request to rewrite a named branch, including `main`, is valid unless another policy forbids it."
START = "Task-start check: before a task that will change files or repository state in a Git working tree, check for pre-existing uncommitted changes (staged, unstaged, untracked). If any exist, ask and offer only two options: commit the identified changes within a scope the user authorizes, or suspend the whole task until the user has cleaned up manually. In a headless or noninteractive run without an already adequate choice, pause safely: change nothing and report the changes found. Changes made during the current task are not this condition."
RECHECK = "Before a destructive Git operation, re-check the authority for it and that changes you did not make are preserved; procedure: `git-workflow`."

DESTRUCTIVE = "under the authority in {owner}; a generic approved workflow is not enough. Immediately before executing one, re-check that authority covers this exact operation and target, inspect what will be lost or rewritten, and confirm that changes you did not make are preserved; otherwise stop and report."
MAINFLOW = "non-rewritable by default: rewriting one needs an explicit user request naming that branch, which is valid unless another policy forbids it."
TASKFLOW = "Run the task-start check ({owner}) with `git status`. Report the identified paths (staged, unstaged, untracked) and the two options; do not stash, reset, clean, or commit them on your own, and commit them only within the scope the user names. The check reads the state before your first change, so files this task changed do not trigger it."


def wrap(s, width=80, indent=''):
    words, lines, cur = s.split(), [], indent
    for w in words:
        if len(cur) + len(w) + (0 if cur == indent else 1) > width:
            lines.append(cur)
            cur = indent + w
        else:
            cur = cur + ('' if cur == indent else ' ') + w
    lines.append(cur)
    return '\n'.join(lines)


PATCHES = [
    # ------------------------------ M
    ('M', 'CLAUDE.md',
     """- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless explicitly requested.
""",
     wrap('- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations ' + AUTH_LONG, 80, '').replace('\n', '\n  ') + '\n'
     + wrap('- ' + MAIN, 80).replace('\n', '\n  ') + '\n' + wrap('- ' + START, 80).replace('\n', '\n  ') + '\n' + wrap('- ' + RECHECK, 80).replace('\n', '\n  ') + '\n'),
    ('M', '.claude/skills/git-workflow/SKILL.md',
     """commit, push, merge, or rewrite history.

## Safety
""",
     """commit, push, merge, or rewrite history.

## Task Start

""" + wrap(TASKFLOW.format(owner='CLAUDE.md § Git')) + """

## Safety
"""),
    ('M', '.claude/skills/git-workflow/SKILL.md',
     """rewriting and the consequences are understood. Treat `main`, `master`, and
other protected or shared branches as non-rewritable.
""",
     """rewriting and the consequences are understood. Treat `main`, `master`, and
other protected or shared branches as """ + wrap(MAINFLOW) + '\n'),
    ('M', '.claude/skills/git-workflow/SKILL.md',
     """high-risk. Perform them only when explicitly requested or clearly required by an
approved workflow, and inspect what will be lost or rewritten before executing
them.
""",
     'high-risk. Perform them only ' + wrap(DESTRUCTIVE.format(owner='CLAUDE.md § Git')) + '\n'),
    ('M', '.claude/MAP.md', '| Git mutations need an explicit request; parallel work isolation | `CLAUDE.md` § Git |',
     '| Git mutations need a specific request or a bounded pre-approval; task-start check; parallel work isolation | `CLAUDE.md` § Git |'),
    # ------------------------------ M1
    ('M1', 'CLAUDE.md',
     """Do not commit, push, merge, rebase, reset, force-push, delete branches, or
perform other repository-changing Git operations unless explicitly requested.
Parallel implementation work""",
     wrap('Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations ' + AUTH_LONG) + '\n\n' + wrap(MAIN) + '\n\n' + wrap(START) + '\n\n' + wrap(RECHECK) + '\n\nParallel implementation work'),
    ('M1', '.claude/skills/git-workflow/SKILL.md',
     """# Git Workflow

## Safety

Perform a repository-changing Git operation only when explicitly requested
(`CLAUDE.md` § Git) — never merely because implementation is complete.
""",
     """# Git Workflow

## Task Start

""" + wrap(TASKFLOW.format(owner='`CLAUDE.md` § Git')) + """

## Safety

Perform a repository-changing Git operation only under the authority in
`CLAUDE.md` § Git — never merely because implementation is complete.
"""),
    ('M1', '.claude/skills/git-workflow/SKILL.md',
     """user explicitly requests history rewriting and the consequences are understood;
treat `main`, `master`, and other protected or shared branches as
non-rewritable.
""",
     """user explicitly requests history rewriting and the consequences are understood;
treat `main`, `master`, and other protected or shared branches as
""" + wrap(MAINFLOW) + '\n'),
    ('M1', '.claude/skills/git-workflow/SKILL.md',
     """Perform them only when explicitly requested or clearly required by an approved
workflow, after inspecting what will be lost or rewritten.
""",
     'Perform them only ' + wrap(DESTRUCTIVE.format(owner='`CLAUDE.md` § Git')) + '\n'),
    # ------------------------------ L0
    ('L0', 'CLAUDE.md',
     """- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform any other repository-changing Git operation unless explicitly requested.
""",
     '- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform any other repository-changing Git operations ' + AUTH_LONG + '\n- ' + MAIN + '\n- ' + START + '\n- ' + RECHECK + '\n'),
    ('L0', '.claude/skills/git-workflow/SKILL.md',
     """When repository-changing Git operations are allowed at all, and parallel-work isolation, are owned by CLAUDE.md → Git safety.

## Safety
""",
     """When repository-changing Git operations are allowed at all, and parallel-work isolation, are owned by CLAUDE.md → Git safety.

## Task start

""" + TASKFLOW.format(owner='CLAUDE.md → Git safety') + """

## Safety
"""),
    ('L0', '.claude/skills/git-workflow/SKILL.md',
     'treat `main`, `master`, and other protected/shared branches as non-rewritable.',
     'treat `main`, `master`, and other protected or shared branches as ' + MAINFLOW),
    ('L0', '.claude/skills/git-workflow/SKILL.md',
     'are high-risk: perform them only when explicitly requested or clearly required by an approved workflow, and inspect what will be lost or rewritten first.',
     'are high-risk: perform them only ' + DESTRUCTIVE.format(owner='CLAUDE.md → Git safety')),
    # ------------------------------ L1
    ('L1', 'CLAUDE.md',
     """- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations unless explicitly requested.
""",
     '- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations ' + AUTH_LONG + '\n- ' + MAIN + '\n- ' + START + '\n- ' + RECHECK + '\n'),
    ('L1', '.claude/skills/git-workflow/SKILL.md',
     """Whether a repository-changing operation may happen at all is governed by `CLAUDE.md` § Git (explicit request only; parallel work on separate branches/worktrees).

## Safety
""",
     """Whether a repository-changing operation may happen at all is governed by `CLAUDE.md` § Git (a specific request or a pre-approval naming operation and scope; parallel work on separate branches/worktrees).

## Task start

""" + TASKFLOW.format(owner='`CLAUDE.md` § Git') + """

## Safety
"""),
    ('L1', '.claude/skills/git-workflow/SKILL.md',
     """rebasing shared history — run only when explicitly requested or required by an approved workflow, and only after inspecting what will be lost or rewritten. Treat `main`, `master`, and other protected or shared branches as non-rewritable.
""",
     'rebasing shared history — run only ' + DESTRUCTIVE.format(owner='`CLAUDE.md` § Git') + ' Treat `main`, `master`, and other protected or shared branches as ' + MAINFLOW + '\n'),
    ('L1', '.claude/INSTRUCTION_MAP.md', '| Git mutations and parallel work | `CLAUDE.md` § Git; procedure: `git-workflow` |', '| Git mutations and their authority, task-start check, parallel work | `CLAUDE.md` § Git; procedure: `git-workflow` |'),
    # ------------------------------ K0
    ('K0', 'CLAUDE.md',
     """- Do not commit, push, merge, rebase, reset, force-push, delete branches or run any other repository-changing Git operation unless explicitly requested.
""",
     '- Do not commit, push, merge, rebase, reset, force-push, delete branches or run any other repository-changing Git operations ' + AUTH_LONG + '\n- ' + MAIN + '\n- ' + START + '\n- ' + RECHECK + '\n'),
    ('K0', '.claude/skills/git-workflow/SKILL.md',
     """Authorization: repository-changing Git operations happen only when explicitly requested, and parallel work uses separate branches or worktrees (CLAUDE.md § Git). Completing an implementation is not a request to commit, push or merge.

Enforced by: the pre-command hook asks the user to confirm Git commands it classifies as repository-changing, unrecognized subcommands included; read-only commands such as `git status`, `git diff` or `git log` run without a prompt. Git run indirectly by scripts or other programs is not classified.
""",
     """Authorization: repository-changing Git operations happen only under the authority in CLAUDE.md § Git (a specific request or a pre-approval naming operation and scope), and parallel work uses separate branches or worktrees. Completing an implementation is not a request to commit, push or merge.

Enforced by: the pre-command hook asks the user to confirm Git commands it classifies as repository-changing, unrecognized subcommands included; read-only commands such as `git status`, `git diff` or `git log` run without a prompt. Git run indirectly by scripts or other programs is not classified.

## Task start

""" + TASKFLOW.format(owner='CLAUDE.md § Git') + '\n'),
    ('K0', '.claude/skills/git-workflow/SKILL.md',
     'treat `main`, `master` and other protected or shared branches as non-rewritable.',
     'treat `main`, `master` and other protected or shared branches as ' + MAINFLOW),
    ('K0', '.claude/skills/git-workflow/SKILL.md',
     'are high-risk: run them only when explicitly requested or required by an approved workflow, and inspect what will be lost or rewritten first.',
     'are high-risk: run them only ' + DESTRUCTIVE.format(owner='CLAUDE.md § Git')),
    ('K0', '.claude/hooks/hook.cjs',
     "'Run it only when the user explicitly requested it (CLAUDE.md § Git); procedure: `git-workflow`.',",
     "'Run it only when the user explicitly requested it or pre-approved this operation and scope (CLAUDE.md § Git); procedure: `git-workflow`.',"),
    ('K0', '.claude/MAP.md', '| Repository-changing Git operations, parallel work isolation | `CLAUDE.md` § Git |', '| Repository-changing Git operations and their authority, task-start check, parallel work isolation | `CLAUDE.md` § Git |'),
    # ------------------------------ K1
    ('K1', 'CLAUDE.md',
     """- Must not commit, push, merge, rebase, reset, force-push, delete branches, or run any other repository-changing Git operation unless explicitly requested; requested operations follow `git-workflow`.
""",
     '- Must not commit, push, merge, rebase, reset, force-push, delete branches, or run any other repository-changing Git operations ' + AUTH_LONG + ' Requested operations follow `git-workflow`.\n- ' + MAIN + '\n- ' + START + '\n- ' + RECHECK + '\n'),
    ('K1', '.claude/skills/git-workflow/SKILL.md',
     """Governing policy: `CLAUDE.md` (Git). This workflow owns how a requested operation is carried out.

## Safety
""",
     """Governing policy: `CLAUDE.md` (Git). This workflow owns how a requested operation is carried out.

## Task start

""" + TASKFLOW.format(owner='`CLAUDE.md` (Git)') + """

## Safety
"""),
    ('K1', '.claude/skills/git-workflow/SKILL.md',
     'as high-risk: perform them only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or rewritten.',
     'as high-risk: perform them only ' + DESTRUCTIVE.format(owner='`CLAUDE.md` (Git)')),
    ('K1', '.claude/skills/git-workflow/SKILL.md',
     'treat `main`, `master`, and other protected/shared branches as non-rewritable.',
     'treat `main`, `master`, and other protected or shared branches as ' + MAINFLOW),
]
