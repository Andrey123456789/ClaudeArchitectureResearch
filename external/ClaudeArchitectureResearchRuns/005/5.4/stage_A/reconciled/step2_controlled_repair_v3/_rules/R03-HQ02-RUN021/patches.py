"""R03 HQ-02 / RUN-021: strategy inputs in each owner rule, timeline technique in each caching skill."""
REASON = 'HQ-02: invalidation coherent with the successful mutation; strategy accounts for isolation, concurrency, commit and rollback order, crash, retries, documented staleness; pre-mutation not excluded when correctness is shown; commit then evict not atomic'
POLICIES = ['RUN-021', 'RUN-007', 'RUN-020', 'ARC-016']

RULE = "The strategy must account for the transaction isolation level, concurrent reads and refills, commit and rollback order, a crash between commit and invalidation, retries, and the staleness the application documents as tolerated. Invalidating after commit is not by itself atomic across the database and the cache. Invalidating before the mutation is not ruled out when correctness for those semantics is shown."
TECH = "No single order is correct by itself ({owner}): evicting after commit leaves stale data if the process crashes between the two, or if a concurrent reader refills a value it read before the commit; evicting before the mutation lets a concurrent reader refill the old value before the commit, while a rollback only costs a miss. Bound these windows with a lifetime, versioned keys, or a retried invalidation, and document the staleness you accept."


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
    ('M', '.claude/rules/performance.md',
     """- Invalidate or update cache entries only in a way consistent with successful
  underlying mutations; the cache must not become a second source of truth.
""",
     """- Invalidate or update cache entries only in a way consistent with successful
  underlying mutations; the cache must not become a second source of truth.
""" + wrap(RULE, 80, '  ') + '\n'),
    ('M', '.claude/skills/caching/SKILL.md',
     """staleness; tag/group invalidation; versioned keys. Invalidating before the
underlying mutation is known to have succeeded is acceptable only when the
workflow deliberately accepts that behavior.
""",
     'staleness; tag/group invalidation; versioned keys.\n\n' + wrap(TECH.format(owner='`.claude/rules/performance.md` § Caching owns the choice')) + '\n'),
    ('M1', '.claude/rules/performance.md',
     """- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.
""",
     """- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.
""" + wrap(RULE, 80, '  ') + '\n'),
    ('M1', '.claude/skills/caching/SKILL.md',
     """TTL with tolerated staleness, tag/group invalidation, versioned keys. Invalidate
before the mutation is known to have succeeded only when the workflow
deliberately accepts that behavior.
""",
     'TTL with tolerated staleness, tag/group invalidation, versioned keys.\n\n' + wrap(TECH.format(owner='`.claude/rules/performance.md` § Caching owns the choice')) + '\n'),
    ('L0', '.claude/rules/0-core/runtime-principles.md',
     '- Invalidate or update cache entries only in a way consistent with successful underlying mutations; the cache must not become a second source of truth.\n',
     '- Invalidate or update cache entries only in a way consistent with successful underlying mutations; the cache must not become a second source of truth. ' + RULE + '\n'),
    ('L0', '.claude/skills/caching/SKILL.md',
     'Invalidation strategies: remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys.\n',
     'Invalidation strategies: remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys.\n\n' + TECH.format(owner='`.claude/rules/0-core/runtime-principles.md` → Caching owns the choice') + '\n'),
    ('L1', '.claude/rules/0-core/backend-code.md',
     '- Invalidate or update cache entries only consistently with successful underlying mutations; the cache is never a second source of truth.\n',
     '- Invalidate or update cache entries only consistently with successful underlying mutations; the cache is never a second source of truth. ' + RULE + '\n'),
    ('L1', '.claude/skills/caching/SKILL.md',
     'versioned keys. Invalidating before the mutation is known to succeed must be a deliberate choice.\n',
     'versioned keys.\n- ' + TECH.format(owner='`.claude/rules/0-core/backend-code.md` § Caching owns the choice') + '\n'),
    ('K0', '.claude/rules/backend/caching.md',
     '- Invalidate or update cache entries consistently with successful underlying mutations; the cache must never become a second source of truth.\n',
     '- Invalidate or update cache entries consistently with successful underlying mutations; the cache must never become a second source of truth. ' + RULE + '\n'),
    ('K0', '.claude/skills/caching/SKILL.md',
     'versioned keys. Invalidation timing relative to the mutation: `rules/backend/caching.md`.\n',
     'versioned keys.\n\n' + TECH.format(owner='`rules/backend/caching.md` owns the choice') + '\n'),
    ('K1', '.claude/rules/backend/runtime.md',
     '- Invalidate or update cache entries only consistently with successful underlying mutations; the cache must never become a second source of truth.\n',
     '- Invalidate or update cache entries only consistently with successful underlying mutations; the cache must never become a second source of truth. ' + RULE + '\n'),
    ('K1', '.claude/skills/caching/SKILL.md',
     'versioned keys. Invalidate before the mutation succeeds only when the workflow deliberately accepts that behavior.\n',
     'versioned keys.\n\n' + TECH.format(owner='`.claude/rules/backend/runtime.md` owns the choice') + '\n'),
]
