"""R02 regression: HQ-01 / GOV-015 and register item 9.1.

Executable: real `git status` state detection in disposable repositories, K0's Git hook executed, mutation tests.
Model tests encode the approved reading and tie it to the text postconditions; they do not prove how a live agent behaves (NOT_RUN).
No Git command touches the research repository: every repository is created under _scratch/runs.
"""
import os
import shutil
import uuid

from order import ORDER
from rcommon import CANDIDATES, SCRATCH, input_path, wc_path
from sandbox import fresh_copy, git, pre_tool
from suitelib import mutate_text, ntext, post

CLAUDE_MUST = ['pre-approved it with a named operation and scope', 'generic "approved workflow"', 'mentions committing is not that authority', 'explicit request to rewrite a named branch, including `main`', 'unless another policy forbids it',
               'pre-existing uncommitted changes (staged, unstaged, untracked)', 'only two options', 'within a scope the user authorizes', 'suspend the whole task', 'pause safely', 'change nothing and report the changes found',
               'changes made during the current task are not this condition', 're-check the authority', 'changes you did not make are preserved']
CLAUDE_NOT = ['repository-changing Git operations unless explicitly requested.', 'repository-changing Git operation unless explicitly requested.']
FLOW_MUST = ['task-start check', 'do not stash, reset, clean, or commit them on your own', 'generic approved workflow is not enough', 're-check that authority covers this exact operation and target', 'changes you did not make are preserved',
             'non-rewritable by default', 'explicit user request naming that branch', 'unless another policy forbids it']
FLOW_NOT = ['required by an approved workflow', 'protected or shared branches as non-rewritable.', 'protected/shared branches as non-rewritable.', 'other protected or shared branches as non-rewritable;']


def text_ok(ctx, c, root=None, name=''):
    a = post(ctx, c, 'CLAUDE.md Git authority and task-start clauses' + name, 'CLAUDE.md', CLAUDE_MUST, CLAUDE_NOT, root)
    b = post(ctx, c, 'git-workflow procedure clauses' + name, '.claude/skills/git-workflow/SKILL.md', FLOW_MUST, FLOW_NOT, root)
    return a and b


def porcelain_gate(porcelain, mode, standing_choice):
    """Approved reading of the task-start check, applied to the porcelain state taken before the first change of the task."""
    if not porcelain.strip():
        return 'PROCEED'
    if standing_choice in ('commit_named_scope', 'suspend'):
        return 'FOLLOW_STANDING_CHOICE'
    return 'ASK_TWO_OPTIONS' if mode == 'interactive' else 'PAUSE_SAFELY'


def authority(op, grant):
    """Approved reading of the authority clause. grant: None, 'generic_workflow', 'task_approval', or (operation, target)."""
    if grant is None or grant in ('generic_workflow', 'task_approval', 'workflow_step_mentions_commit'):
        return 'DENY'
    return 'ALLOW_AFTER_RECHECK' if grant == op else 'DENY'


def fixture_repo():
    d = os.path.join(SCRATCH, 'runs', 'gitfx-' + uuid.uuid4().hex[:8])
    os.makedirs(d)
    git(d, 'init', '-q')
    with open(os.path.join(d, 'a.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('one\n')
    with open(os.path.join(d, '.gitignore'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('ignored.txt\n')
    git(d, 'add', '.')
    git(d, 'commit', '-q', '-m', 'init')
    return d


def state(d):
    code, out, err = git(d, 'status', '--porcelain')
    assert code == 0, err
    return out


def run(ctx):
    for c in CANDIDATES:
        text_ok(ctx, c)
    # Executable state detection: the command the rule points to tells these states apart.
    d = fixture_repo()
    ctx.check('clean tree: no gate', porcelain_gate(state(d), 'interactive', None) == 'PROCEED', kind='GIT_FIXTURE', actual=state(d))
    with open(os.path.join(d, 'ignored.txt'), 'w') as f:
        f.write('x')
    ctx.check('ignored file alone: no gate', porcelain_gate(state(d), 'interactive', None) == 'PROCEED', kind='GIT_FIXTURE', actual=state(d))
    with open(os.path.join(d, 'a.txt'), 'a') as f:
        f.write('two\n')
    s = state(d)
    ctx.check('unstaged change: two options', porcelain_gate(s, 'interactive', None) == 'ASK_TWO_OPTIONS' and ' M a.txt' in s, kind='GIT_FIXTURE', actual=s)
    ctx.check('unstaged change, headless: pause', porcelain_gate(s, 'headless', None) == 'PAUSE_SAFELY', kind='GIT_FIXTURE')
    git(d, 'add', 'a.txt')
    s = state(d)
    ctx.check('staged change: two options', porcelain_gate(s, 'interactive', None) == 'ASK_TWO_OPTIONS' and 'M  a.txt' in s, kind='GIT_FIXTURE', actual=s)
    git(d, 'reset', '-q', '--hard')
    ctx.check('fixture restored to clean', state(d).strip() == '', kind='GIT_FIXTURE')
    with open(os.path.join(d, 'foreign.txt'), 'w') as f:
        f.write('x')
    s = state(d)
    ctx.check('untracked foreign file: two options', porcelain_gate(s, 'interactive', None) == 'ASK_TWO_OPTIONS' and '?? foreign.txt' in s, kind='GIT_FIXTURE', actual=s)
    ctx.check('headless with an adequate standing choice follows it', porcelain_gate(s, 'headless', 'suspend') == 'FOLLOW_STANDING_CHOICE', kind='MODEL')
    ctx.check('headless with no standing choice pauses', porcelain_gate(s, 'headless', None) == 'PAUSE_SAFELY', kind='MODEL')
    os.remove(os.path.join(d, 'foreign.txt'))
    start = state(d)
    with open(os.path.join(d, 'a.txt'), 'a') as f:
        f.write('made during the task\n')
    ctx.check('changes made during the task do not retrigger: the check reads the state before the first change', porcelain_gate(start, 'interactive', None) == 'PROCEED' and state(d).strip() != '', kind='GIT_FIXTURE')
    shutil.rmtree(d, ignore_errors=True)
    # Authority table
    reset = ('reset --hard', 'feature/x')
    main_push = ('push --force', 'main')
    ctx.check('generic approved workflow is no authority for reset', authority(reset, 'generic_workflow') == 'DENY', kind='MODEL')
    ctx.check('general task approval is no authority', authority(reset, 'task_approval') == 'DENY', kind='MODEL')
    ctx.check('workflow step mentioning a commit is no authority', authority(('commit', 'lockfile'), 'workflow_step_mentions_commit') == 'DENY', kind='MODEL')
    ctx.check('explicit request allows after re-check', authority(reset, reset) == 'ALLOW_AFTER_RECHECK', kind='MODEL')
    ctx.check('pre-approval for one branch does not leak to main', authority(main_push, ('push --force', 'feature/x')) == 'DENY', kind='MODEL')
    ctx.check('explicit main rewrite is valid unless another policy forbids it', authority(main_push, main_push) == 'ALLOW_AFTER_RECHECK', kind='MODEL')
    # K0 is the only candidate with a Git hook; it asks, and its reason carries the authority text. Others keep text-only delivery (no forced homogenizing).
    root = fresh_copy('K0', 'git')
    for cmd, want in (('git status', 'allow'), ('git diff --cached', 'allow'), ('git log --oneline', 'allow'), ('git commit -m x', 'ask'), ('git reset --hard', 'ask'), ('git push --force origin main', 'ask'), ('git clean -fd', 'ask'),
                      ('git branch -D old', 'ask'), ('bash -c "git reset --hard"', 'ask'), ('pwsh -Command "git push --force"', 'ask')):
        d0, raw = pre_tool(root, 'K0', cmd)
        ctx.check('K0 hook: %s -> %s' % (cmd, want), d0 == want, raw[:200], 'K0', 'HOOK', want, d0)
    d0, raw = pre_tool(root, 'K0', 'git reset --hard')
    ctx.check('K0 hook reason names the approved authority', 'pre-approved this operation and scope' in raw, raw[:300], 'K0', 'HOOK')
    # Mutations prove the checks catch a regression.
    for c in CANDIDATES:
        rel = '.claude/skills/git-workflow/SKILL.md'
        m = mutate_text(c, rel, 'generic approved workflow is not enough', 'clearly required by an approved workflow')
        ctx.check('mutation: approved-workflow authority reinserted is caught', m is not None and not post(None, c, '', rel, FLOW_MUST, FLOW_NOT, m), candidate=c, kind='MUTATION')
        m = mutate_text(c, 'CLAUDE.md', 'pause safely', 'continue')
        ctx.check('mutation: headless pause removed is caught', m is not None and not post(None, c, '', 'CLAUDE.md', CLAUDE_MUST, CLAUDE_NOT, m), candidate=c, kind='MUTATION')
        m = mutate_text(c, 'CLAUDE.md', 'Changes made during the current task are not this condition', 'Changes made during the current task also trigger this')
        ctx.check('mutation: task-made changes exclusion removed is caught', m is not None and not post(None, c, '', 'CLAUDE.md', CLAUDE_MUST, CLAUDE_NOT, m), candidate=c, kind='MUTATION')
        m = mutate_text(c, rel, 'non-rewritable by default', 'non-rewritable')
        ctx.check('mutation: main exception removed is caught', m is not None and not post(None, c, '', rel, FLOW_MUST, FLOW_NOT, m), candidate=c, kind='MUTATION')
    # Disable the K0 Git ask in a copy: the executed hook test must notice.
    m = mutate_text('K0', '.claude/hooks/hook.cjs', 'if (found.git.length > 0) {', 'if (false) {')
    d0, _ = pre_tool(m, 'K0', 'git reset --hard') if m else ('n/a', '')
    ctx.check('mutation: disabled K0 Git ask is caught by the hook test', d0 == 'allow', candidate='K0', kind='MUTATION', actual=d0)
    ctx.not_run('live agent stops on a dirty tree and offers exactly two options', 'needs a live Claude runtime; kept as a future experiment')
    ctx.not_run('host behavior of the K0 "ask" decision in a headless run', 'host semantics not executable here')
