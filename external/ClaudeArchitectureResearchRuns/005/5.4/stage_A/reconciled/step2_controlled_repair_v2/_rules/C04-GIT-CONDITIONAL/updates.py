"""C04 claim updates. Each record said "commit" as an unconditional duty; its original claim stays in the view. Modality and DEP-007 coverage stay: keeping both files coherent is the same duty, and DEP-007 never asked for a commit."""
RULE = 'C04-GIT-CONDITIONAL'
UPDATES = {}
ADDED = []
COND = 'when an authorized commit is part of this task, include both files, and otherwise update them without creating a Git commit'
NOTE = 'C04: the commit step is conditional on an authorized commit (GOV-015). Lockfile duties unchanged.'
MSG = 'C04: the checker message no longer tells the reader to commit. Same check, same severity.'


def up(key, claim, note=NOTE):
    UPDATES[key] = dict(rule=RULE, status='REWORDED', claim=claim, note=note, set={}, sub={})


up('FG-M-95efcc9a8b', 'Maintain package.json and package-lock.json together; %s.' % COND)
up('FG-M-e25085c076', 'Install npm packages with an explicit version, --save-dev for build/test tooling, and update package.json and package-lock.json together; %s.' % COND)
up('FG-M1-a90b921ef7', 'Maintain package.json and package-lock.json together; %s.' % COND)
up('FG-M1-bbd22299d0', 'A package.json with dependencies but no package-lock.json warns to keep a consistent lockfile beside it.', MSG)
up('FG-L0-cdc94584e5', 'npm for the Angular workspace unless deliberately changed; keep package.json and package-lock.json together and the lockfile consistent; %s.' % COND)
up('FG-L0-f40bf092ce', 'Keep package.json and package-lock.json together and the lockfile consistent with every change; %s.' % COND)
up('FG-L1-1321d671af', 'npm for the frontend unless deliberately changed; keep package.json and package-lock.json together and the lockfile consistent (%s); build/test tooling in devDependencies.' % COND)
up('FG-L1-b7e6a7df31', 'Keep package.json and package-lock.json together; %s.' % COND)
up('FG-K0-0f7b627b11', 'Keep package.json and package-lock.json together and the lockfile consistent with every dependency change; %s.' % COND, 'C04: this record reported the categorical commit line as possibly conflicting with the explicit-request Git rule. The line is now conditional, so that report no longer applies to the current text.')
up('FG-K0-5f145f277d', 'Keep package.json and package-lock.json together and the lockfile consistent with every dependency change; %s.' % COND)
up('FG-K0-76d3c2f793', 'A package.json without a package-lock.json beside it produces a notice to keep a consistent lockfile beside it.', MSG)
up('FG-K1-d74f68ee1a', 'npm is the frontend package manager unless deliberately changed; package.json and package-lock.json stay together and consistent (%s); build/test tooling belongs in devDependencies unless there is a concrete reason.' % COND)
up('FG-K1-5a2b257bee', 'npm: install name@version (--save-dev for build/test tooling) and keep package.json and package-lock.json together and consistent; when an authorized commit is part of this task, include both files, and otherwise do not create a Git commit.')
up('FG-K1-58ebd4b327', 'Keep package-lock.json beside package.json; when an authorized commit is part of this task, include both files, and otherwise do not create a Git commit.')
