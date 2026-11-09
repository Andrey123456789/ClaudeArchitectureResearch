"""Source review for R03."""
OWNER = {'M': '.claude/rules/performance.md', 'M1': '.claude/rules/performance.md', 'L0': '.claude/rules/0-core/runtime-principles.md', 'L1': '.claude/rules/0-core/backend-code.md', 'K0': '.claude/rules/backend/caching.md', 'K1': '.claude/rules/backend/runtime.md'}
SKILL = '.claude/skills/caching/SKILL.md'
KEYS = {'M': 'Cache keys must uniquely represent', 'M1': 'Cache keys must uniquely represent', 'L0': 'Cache keys must uniquely represent', 'L1': 'Cache keys must uniquely represent', 'K0': 'Cache keys must uniquely represent', 'K1': 'Cache keys must uniquely represent'}
NEED = {'M': 'Introduce it only for a clear measured or reasoned need', 'M1': 'caching', 'L0': 'Introduce it only for a clear measured or reasoned need', 'L1': 'introduce it only for a clear measured or reasoned need', 'K0': 'Introduce it only for a clear measured or reasoned need', 'K1': 'no caching without a clear measured or reasoned need'}
UOW = {'M': ('.claude/skills/caching/SKILL.md', 'Do not bypass'), 'M1': ('.claude/skills/caching/SKILL.md', 'Do not bypass repositories'), 'L0': ('.claude/skills/caching/SKILL.md', 'Mutations still follow the normal repository/Unit of Work flow'),
       'L1': ('.claude/skills/caching/SKILL.md', 'Use cases keep their normal repository/commit-boundary flow'), 'K0': ('.claude/skills/caching/SKILL.md', 'keep their normal repository/Unit of Work flow'), 'K1': ('.claude/skills/caching/SKILL.md', 'keep their normal repository/Unit of Work workflow')}
REVIEW = []
for c in OWNER:
    REVIEW.append(dict(policy='RUN-021', candidate=c, verdict='HOLDS', quotes=[(OWNER[c], 'second source of truth'), (OWNER[c], 'not by itself atomic across the database and the cache'), (OWNER[c], 'is not ruled out when correctness for those semantics is shown'), (SKILL, 'No single order is correct by itself')],
                       note='Policy sentence kept verbatim in the owner. Added strategy inputs are the user-approved reading (register HQ-02). The former skill-level gate (only when the workflow accepts it, or a deliberate choice) is replaced by the same correctness condition in all six, and L0 and K0 no longer differ by having no such sentence.',
                       counterexample='Evict after commit plus a concurrent refill leaves stale data with the old sentence fully satisfied; the new text requires that window to be considered. Evict before commit with a refill before commit is stale, so it needs shown correctness (executed in the suite).'))
    REVIEW.append(dict(policy='RUN-020', candidate=c, verdict='HOLDS', quotes=[(OWNER[c], KEYS[c])], note='Key rule untouched.'))
    REVIEW.append(dict(policy='ARC-016', candidate=c, verdict='HOLDS', quotes=[UOW[c]], note='Commit boundary ownership untouched; the rule speaks about timing relative to commit and does not move the commit.'))
    REVIEW.append(dict(policy='RUN-007', candidate=c, verdict='HOLDS', quotes=[(OWNER[c], NEED[c])], note='Need rule untouched.'))
