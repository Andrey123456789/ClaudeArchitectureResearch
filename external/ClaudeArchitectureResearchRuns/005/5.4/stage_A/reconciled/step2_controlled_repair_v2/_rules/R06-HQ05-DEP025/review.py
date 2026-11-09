"""Source review for R06."""
SKILL = '.claude/skills/add-dependency/SKILL.md'
HOOK = {'M': '.claude/hooks/dependency-guard.mjs', 'M1': '.claude/scripts/lib/dependency-commands.js', 'L0': '.claude/hooks/claude-hook.mjs', 'L1': '.claude/hooks/pre-shell-command.mjs', 'K0': '.claude/hooks/hook.cjs', 'K1': '.claude/scripts/classify-command.cjs'}
QUOTE = {'M': 'bypasses npm peer-dependency resolution', 'M1': 'No confirmation, comment marker, or approval opens this route', 'L0': 'No confirmation, comment marker, or approval opens this route', 'L1': "decide('deny', 'Peer-dependency bypass", 'K0': 'No confirmation, comment marker, or approval opens this route', 'K1': "kind: 'peer-bypass'"}
REVIEW = []
for c in HOOK:
    REVIEW.append(dict(policy='DEP-025', candidate=c, verdict='HOLDS', quotes=[(SKILL, 'resolve the actual compatibility problem'), (SKILL, 'No confirmation, comment marker, or'), (HOOK[c], QUOTE[c])],
                       note='Executed: every listed command form is denied or blocked, with and without markers, and a pinned install still passes. Stronger than the policy word "merely": the hook cannot read intent, so all force installs stop. That is unchanged in M, L0, K1 and is now equal in M1, L1, K0.',
                       counterexample='K0 before this rule: "npm install x --force # add-dependency: reviewed" passed the hook (executed in suite_pre). L1 before: ask. M1 before: "# peer-override: approved-by-user" opened it.'))
    REVIEW.append(dict(policy='DEP-003', candidate=c, verdict='HOLDS', quotes=[(SKILL, 'The entry covers the version only, not any other dependency rule')], note='Falsification of R04 against R06: a recorded floating version plus --force stays denied (executed).'))
