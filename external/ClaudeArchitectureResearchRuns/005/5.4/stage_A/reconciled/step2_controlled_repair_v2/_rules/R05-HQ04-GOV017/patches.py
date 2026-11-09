"""R05 HQ-04 / GOV-017: one headless rule in each always-loaded owner, one procedure in each architecture-decision workflow."""
REASON = 'HQ-04: headless may implement a specific, previously explicitly approved Reserved change; may not make or approve a new Reserved decision; vague authorization insufficient; approval evidence, scope, decision log, stop on an unexpected Reserved choice'
POLICIES = ['GOV-017', 'GOV-005', 'GOV-015']

RULE = """In an autonomous or headless run, implement a Reserved change only when the user explicitly approved that specific change beforehand, naming the change and its scope; a broad or vague instruction is not approval, and the approval is recorded through `architecture-decision`. Never make or approve a new Reserved decision there: on an unexpected Reserved choice, stop that part of the work, continue only on a policy-compliant non-Reserved path, and report every unresolved Decision Request in the final report, with a decision log of what was implemented under which approval."""
FLOW = """In an autonomous or headless run, proceed with a Reserved change only when the request already holds an explicit approval of that specific change and its scope. Record it as usual, quoting the approving text and its scope, implement only that scope, and list it in a decision log in the final report (approval quote, scope, what was implemented). A broad instruction such as "do whatever is needed" is not approval. A Reserved choice the approval does not cover stops that part of the work: do not decide it, continue with the "Proceeding with" work, and list the Decision Request as unresolved."""


def wrap(s, width=80):
    words, lines, cur = s.split(), [], ''
    for w in words:
        if len(cur) + len(w) + (0 if not cur else 1) > width:
            lines.append(cur)
            cur = w
        else:
            cur = cur + ('' if not cur else ' ') + w
    lines.append(cur)
    return '\n'.join(lines)


PATCHES = [
    ('M', 'CLAUDE.md', """workflow. In an autonomous or headless run, never make a Reserved decision:
proceed only on a policy-compliant non-Reserved path and report every unresolved
Decision Request explicitly.
""", 'workflow.\n\n' + wrap(RULE) + '\n'),
    ('M', '.claude/skills/architecture-decision/SKILL.md', """In an autonomous or headless run, do not wait and do not decide: continue only
with the "Proceeding with" work and list every unresolved Decision Request in
the final report.
""", wrap(FLOW) + '\n'),
    ('M1', 'CLAUDE.md', """explicit user instruction may count as approval but must be recorded there. In
an autonomous or headless run, continue only on a policy-compliant
non-Reserved path and report unresolved Decision Requests; never silently make
a Reserved decision.
""", 'explicit user instruction may count as approval but must be recorded there.\n\n' + wrap(RULE) + '\n'),
    ('M1', '.claude/skills/architecture-decision/SKILL.md', """- Autonomous or headless run: continue only on the non-Reserved path named in
  "Proceeding with", and list every unresolved Decision Request in the final
  report.
""", '- ' + wrap(FLOW, 78).replace('\n', '\n  ') + '\n'),
    ('L0', 'CLAUDE.md', """In an autonomous or headless run, take only a policy-compliant non-Reserved path, never make a Reserved decision silently, and list every unresolved Decision Request explicitly in the final report.
""", RULE + '\n'),
    ('L0', '.claude/skills/architecture-decision/SKILL.md', """Do not implement the Reserved option before approval; headless runs follow CLAUDE.md → Decision control and continue only with the "Proceeding with" work.
""", 'Do not implement the Reserved option before approval.\n\n' + FLOW + '\n'),
    ('L1', 'CLAUDE.md', """- An explicit user instruction counts as approval; record the accepted decision with `architecture-decision`. In autonomous/headless runs, take only a policy-compliant non-Reserved path and report unresolved Decision Requests explicitly.
""", '- An explicit user instruction counts as approval; record the accepted decision with `architecture-decision`.\n- ' + RULE + '\n'),
    ('L1', '.claude/skills/architecture-decision/SKILL.md', """In autonomous or headless runs, list unresolved Decision Requests in the final report instead of deciding.
""", FLOW + '\n'),
    ('K0', 'CLAUDE.md', """- In an autonomous or headless run, take only a policy-compliant non-Reserved path, never make a Reserved decision silently, and list unresolved Decision Requests in the final report.
""", '- ' + RULE.replace('the approval is recorded through `architecture-decision`', 'the approval is recorded (workflow: `architecture-decision`)') + '\n'),
    ('K0', '.claude/skills/architecture-decision/SKILL.md', """An explicit user instruction to adopt a specific option counts as approval. In an autonomous or headless run, continue only with the "Proceeding with" path and report the request as unresolved.
""", 'An explicit user instruction to adopt a specific option counts as approval.\n\n' + FLOW + '\n'),
    ('K1', 'CLAUDE.md', """- In an autonomous or headless run, take only a policy-compliant non-Reserved path, never silently make or alter a Reserved decision, and report every unresolved Decision Request explicitly.
""", '- ' + RULE + '\n'),
    ('K1', '.claude/skills/architecture-decision/SKILL.md', """Headless or autonomous runs follow `CLAUDE.md` (Decision control); the *Proceeding with* field names the compliant path actually taken.
""", FLOW + ' The *Proceeding with* field names the compliant path actually taken.\n'),
]
