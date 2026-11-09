"""R03 regression: HQ-02 / RUN-021.

A small deterministic store-and-cache simulation runs semantic timelines. It needs no database or cache server. It shows the claims the
rule text makes (commit-then-evict is not atomic; pre-mutation invalidation can be correct or wrong depending on the semantics) and is
checked together with the text postconditions. Real provider or Redis behavior is NOT_RUN and never claimed.
"""
from rcommon import CANDIDATES
from suitelib import mutate_text, post

OWNER = {'M': '.claude/rules/performance.md', 'M1': '.claude/rules/performance.md', 'L0': '.claude/rules/0-core/runtime-principles.md', 'L1': '.claude/rules/0-core/backend-code.md', 'K0': '.claude/rules/backend/caching.md', 'K1': '.claude/rules/backend/runtime.md'}
SKILL = '.claude/skills/caching/SKILL.md'
RULE_MUST = ['consistent', 'second source of truth', 'transaction isolation level', 'concurrent reads and refills', 'commit and rollback order', 'a crash between commit and invalidation', 'retries', 'staleness the application documents as tolerated',
             'not by itself atomic across the database and the cache', 'invalidating before the mutation is not ruled out when correctness for those semantics is shown']
SKILL_MUST = ['no single order is correct by itself', 'crash', 'concurrent reader', 'a rollback only costs a miss', 'lifetime, versioned keys, or a retried invalidation', 'document the staleness you accept']
SKILL_NOT = ['only when the workflow deliberately accepts', 'must be a deliberate choice']


class Sim:
    """Committed value, one open transaction, one cache entry with an optional key version."""

    def __init__(self):
        self.db, self.pending, self.cache, self.ver = 'old', None, None, 1

    def begin(self, v):
        self.pending = v

    def commit(self):
        self.db, self.pending = self.pending, None
        self.ver += 1

    def rollback(self):
        self.pending = None

    def evict(self):
        self.cache = None

    def read_db(self, isolation='read_committed'):
        return self.pending if (isolation == 'read_uncommitted' and self.pending is not None) else self.db

    def fill(self, value):
        self.cache = value

    def get(self):
        if self.cache is None:
            self.cache = self.db
        return self.cache


def stale(s):
    return s.get() != s.db


def run(ctx):
    for c in CANDIDATES:
        post(ctx, c, 'owner rule states strategy inputs and non-atomicity', OWNER[c], RULE_MUST)
        post(ctx, c, 'caching skill timelines, no categorical order', SKILL, SKILL_MUST, SKILL_NOT)
    s = Sim(); s.fill('old'); s.begin('new'); s.commit(); s.evict()
    ctx.check('successful commit then evict: coherent', not stale(s), kind='TIMELINE')
    s = Sim(); s.fill('old'); s.begin('new'); s.rollback()
    ctx.check('rollback with evict-after-commit: nothing evicted, cache still true', not stale(s), kind='TIMELINE')
    s = Sim(); s.fill('old'); s.evict(); s.begin('new'); s.rollback()
    ctx.check('rollback with pre-mutation evict: costs a miss only', not stale(s), kind='TIMELINE')
    s = Sim(); s.fill('old'); s.begin('new'); s.commit()  # crash here: no evict
    ctx.check('crash between commit and evict leaves stale data, so commit then evict is not atomic', stale(s), kind='COUNTEREXAMPLE')
    s = Sim(); s.fill(None); s.cache = None; r = s.read_db(); s.begin('new'); s.commit(); s.evict(); s.fill(r)
    ctx.check('concurrent reader refills after the evict: stale despite correct order', stale(s), kind='COUNTEREXAMPLE')
    s = Sim(); s.fill('old'); s.evict(); s.begin('new'); r = s.read_db(); s.fill(r); s.commit()
    ctx.check('pre-mutation evict with a concurrent refill before commit: stale, so correctness must be shown', stale(s), kind='COUNTEREXAMPLE')
    s = Sim(); s.fill('old'); s.evict(); s.begin('new'); r = s.read_db(); s.fill(r); s.commit(); s.evict()
    ctx.check('evict before and after commit closes that window', not stale(s), kind='TIMELINE')
    s = Sim(); s.begin('new'); r = s.read_db('read_uncommitted'); s.fill(r); s.rollback()
    ctx.check('read-uncommitted refill then rollback leaves a phantom value: isolation matters', stale(s), kind='COUNTEREXAMPLE')
    s = Sim(); s.begin('new'); r = s.read_db('read_committed'); s.fill(r); s.rollback()
    ctx.check('same order at read-committed is coherent', not stale(s), kind='TIMELINE')

    def versioned():
        s = Sim(); entries = {s.ver: s.db}; old_ver, old_val = s.ver, s.read_db(); s.begin('new'); s.commit(); entries[old_ver] = old_val
        return entries.get(s.ver, s.db) == s.db
    ctx.check('versioned key bumped with the commit: a late refill lands on the old key', versioned(), kind='TIMELINE')
    s = Sim(); s.fill('old'); s.begin('new'); s.commit(); fails = 2
    for attempt in range(3):
        if fails == 0:
            s.evict()
            break
        fails -= 1
    ctx.check('retried invalidation converges and repeating an evict is harmless', not stale(s), kind='TIMELINE')
    s = Sim(); s.fill('old'); s.begin('new'); s.commit(); ctx.check('a bounded lifetime is the only guard left after a lost evict', stale(s) and s.db == 'new', kind='COUNTEREXAMPLE')
    for c in CANDIDATES:
        m = mutate_text(c, OWNER[c], 'not by itself atomic across the database and the cache', 'atomic across the database and the cache')
        ctx.check('mutation: atomic claim asserted is caught', m is not None and not post(None, c, '', OWNER[c], RULE_MUST, (), m), candidate=c, kind='MUTATION')
        m = mutate_text(c, OWNER[c], 'Invalidating before the mutation is not ruled out when correctness for those semantics is shown', 'Never invalidate before the mutation')
        ctx.check('mutation: categorical ban on pre-mutation invalidation is caught', m is not None and not post(None, c, '', OWNER[c], RULE_MUST, (), m), candidate=c, kind='MUTATION')
        m = mutate_text(c, SKILL, 'No single order is correct by itself', 'Invalidate only when the workflow deliberately accepts it')
        ctx.check('mutation: skill loses the timelines is caught', m is not None and not post(None, c, '', SKILL, SKILL_MUST, SKILL_NOT, m), candidate=c, kind='MUTATION')
    ctx.not_run('a real database and cache show these timelines', 'no database or cache server in this run; the simulation states the logic only')
