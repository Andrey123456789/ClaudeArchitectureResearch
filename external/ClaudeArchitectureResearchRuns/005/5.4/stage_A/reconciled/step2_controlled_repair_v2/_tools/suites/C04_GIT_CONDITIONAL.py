"""C04 regression: conditional npm commit steps, all six. A sweep over every text and script file for the unconditional forms, the conditional clause in each owner, real Git fixtures with package files, K0's hook, and mutations. No live agent ran: agent behavior is NOT_RUN."""
import os
import re
import shutil
import uuid

from rcommon import CANDIDATES, SCRATCH, read_lines, template_root, walk_files, wc_path
from sandbox import fresh_copy, git, pre_tool
from suitelib import mutate_text, ntext, post
from suites_loader import load_suite

OWNER = {'M': '.claude/rules/dependencies.md', 'M1': '.claude/rules/dependencies.md', 'L0': '.claude/rules/3-project/package-management.md', 'L1': '.claude/rules/3-project/package-management.md', 'K0': '.claude/rules/common/dependencies.md', 'K1': '.claude/rules/frontend/dependencies.md'}
CLAUSE = 'when an authorized commit is part of this task, include both files'
NO_COMMIT = 'without creating a Git commit'
CONSISTENT = {'M': 'keep the lockfile consistent when packages change', 'M1': 'keep the lockfile consistent when adding packages', 'L0': 'the lockfile consistent with every change', 'L1': 'the lockfile consistent', 'K0': 'the lockfile consistent with every dependency change', 'K1': 'must stay together and consistent'}
# The unconditional forms: an imperative line, "maintain and commit", "and commit `...`", ": commit `...`", "; commit `...`", passive "must be committed", and checker messages.
UNCONDITIONAL = re.compile(r'^\s*(\d+\.|-)?\s*(\*\*)?Commit\b(?! boundary)|[Mm]aintain and commit\b|\band commit `|[:;] commit `|must be committed\b|consistent and committed\b|commit the lockfile|commit a consistent lockfile')
SKIP = ('.claude/skills/git-workflow/',)


def sweep(root):
    hits = []
    for rel in walk_files(root):
        if rel.startswith(SKIP) or not rel.endswith(('.md', '.mjs', '.cjs', '.js', '.json')):
            continue
        for i, line in enumerate(read_lines(os.path.join(root, rel.replace('/', os.sep))), 1):
            if UNCONDITIONAL.search(line):
                hits.append('%s:%d %s' % (rel, i, line.strip()[:90]))
    return hits


def repo():
    d = os.path.join(SCRATCH, 'runs', 'gitc04-' + uuid.uuid4().hex[:8])
    os.makedirs(d)
    git(d, 'init', '-q')
    for name, body in (('package.json', '{"name":"a","version":"1.0.0"}\n'), ('package-lock.json', '{"name":"a","lockfileVersion":3}\n')):
        with open(os.path.join(d, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)
    git(d, 'add', '.')
    git(d, 'commit', '-q', '-m', 'init')
    return d


def head(d):
    return git(d, 'rev-parse', 'HEAD')[1].strip()


def status(d):
    return git(d, 'status', '--porcelain')[1]


def dependency_task(d, authority):
    """Model of the conditional step on a real repository: both files are updated together; a commit is created only under an authority naming it. The R02 authority model decides."""
    r02 = load_suite('R02_HQ01_GOV015')
    with open(os.path.join(d, 'package.json'), 'a', encoding='utf-8', newline='\n') as f:
        f.write('\n')
    with open(os.path.join(d, 'package-lock.json'), 'a', encoding='utf-8', newline='\n') as f:
        f.write('\n')
    op = ('commit', 'package manifests')
    if r02.authority(op, authority) == 'ALLOW_AFTER_RECHECK':
        git(d, 'add', 'package.json', 'package-lock.json')
        git(d, 'commit', '-q', '-m', 'dependency')


def run(ctx):
    r02 = load_suite('R02_HQ01_GOV015')
    for c in CANDIDATES:
        hits = sweep(template_root(c))
        ctx.check('no unconditional commit step remains in text, scripts or checker messages', not hits, hits[:6], c, 'SWEEP', actual=len(hits))
        post(ctx, c, 'dependency owner carries the conditional clause and keeps lockfile consistency', OWNER[c], [CLAUSE, NO_COMMIT, CONSISTENT[c]])
        post(ctx, c, 'DEP-007 duties kept: npm default and dependency categories', OWNER[c], ['deliberately adopts another', 'devDependencies'])
        post(ctx, c, 'dependency review obligations untouched', '.claude/skills/add-dependency/SKILL.md', ['deprecat', 'vulnerab', 'licens'])
        post(ctx, c, 'Git authority clause kept', 'CLAUDE.md', ['mentions committing is not that authority', 'pre-approved it with a named operation and scope'])
        m = mutate_text(c, OWNER[c], CLAUSE, 'always commit `package.json` and `package-lock.json`')
        ctx.check('mutation: conditional clause removed is caught', m is not None and not post(None, c, '', OWNER[c], [CLAUSE], (), m), candidate=c, kind='MUTATION')
        root = fresh_copy(c, 'c04')
        with open(os.path.join(root, 'CUSTOM_SETTINGS.md'), 'a', encoding='utf-8') as f:
            f.write('\n2. Commit `package.json` and `package-lock.json`.\n')
        ctx.check('mutation: a reinserted imperative is caught by the sweep', any('CUSTOM_SETTINGS.md' in h for h in sweep(root)), candidate=c, kind='MUTATION')
        shutil.rmtree(root, ignore_errors=True)
    # Sweep controls: it must not fire on prohibitions, sequencing or database commits.
    root = os.path.join(SCRATCH, 'runs', 'sweepctl-' + uuid.uuid4().hex[:8])
    os.makedirs(root)
    with open(os.path.join(root, 'control.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('Never hardcode or commit real secrets.\nReview generated migrations before committing them.\nCommit boundary: IUnitOfWork.\nWhen an authorized commit is part of this task, include both files.\n')
    ctx.check('sweep control: prohibitions, sequencing, database commits and the conditional clause do not fire', not sweep(root), sweep(root)[:4], kind='CONTROL')
    # Real Git: no authority, no commit; a named authority, one commit holding both files.
    for name, grant in (('no authority', None), ('generic approved workflow', 'generic_workflow'), ('general task approval', 'task_approval'), ('a workflow step mentioning a commit', 'workflow_step_mentions_commit')):
        d = repo()
        h0 = head(d)
        dependency_task(d, grant)
        s = status(d)
        ctx.check('fixture, %s: no commit is created and both files stay changed together' % name, head(d) == h0 and 'package.json' in s and 'package-lock.json' in s, s, kind='GIT_FIXTURE')
        shutil.rmtree(d, ignore_errors=True)
    d = repo()
    h0 = head(d)
    dependency_task(d, ('commit', 'package manifests'))
    shown = git(d, 'show', '--name-only', '--format=', 'HEAD')[1]
    ctx.check('fixture, named commit authority: one commit that holds both files', head(d) != h0 and 'package.json' in shown and 'package-lock.json' in shown and not status(d).strip(), shown, kind='GIT_FIXTURE')
    shutil.rmtree(d, ignore_errors=True)
    # The R02 task-start check still fires on a dirty package file; a read-only task never reads it.
    d = repo()
    with open(os.path.join(d, 'package-lock.json'), 'a', encoding='utf-8', newline='\n') as f:
        f.write('\n')
    s = status(d)
    ctx.check('dirty lockfile at task start: two options interactively', r02.porcelain_gate(s, 'interactive', None) == 'ASK_TWO_OPTIONS', s, kind='GIT_FIXTURE')
    ctx.check('dirty lockfile at task start: headless with no standing choice pauses', r02.porcelain_gate(s, 'headless', None) == 'PAUSE_SAFELY', s, kind='GIT_FIXTURE')
    shutil.rmtree(d, ignore_errors=True)
    for c in CANDIDATES:
        ctx.check('a read-only task is outside the task-start check', 'before a task that will change files or repository state' in ntext(c, 'CLAUDE.md'), candidate=c, kind='TEXT')
    # K0 is the one candidate with a Git hook: commit steps still ask, and a comment does not change that.
    root = fresh_copy('K0', 'c04')
    for cmd in ('git commit -m lockfile', 'git add package.json package-lock.json && git commit -m lockfile', 'git commit -m lockfile # approved workflow'):
        d0, raw = pre_tool(root, 'K0', cmd)
        ctx.check('K0 hook does not allow: %s' % cmd, d0 != 'allow', raw[:200], 'K0', 'HOOK', actual=d0)
    shutil.rmtree(root, ignore_errors=True)
    ctx.not_run('a live agent follows the conditional step in an interactive and a headless run', 'needs a live Claude runtime; kept as a future experiment')
