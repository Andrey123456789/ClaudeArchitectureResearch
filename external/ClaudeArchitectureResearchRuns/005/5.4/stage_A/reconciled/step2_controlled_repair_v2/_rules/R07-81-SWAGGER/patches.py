"""R07 item 8.1: one obligation and one condition, owned by each candidate's verify workflow; the swagger knowledge skill states the same trigger and action and points there."""
REASON = '8.1: on an applicable Development API behavior change open Development Swagger UI and confirm it loads; not applicable without such a UI; an unrunnable application is reported NOT RUN'
POLICIES = ['WF-005', 'WF-006', 'API-016', 'TST-010']

STEP = "API behavior change: when a change alters API behavior and the project exposes {ui} in Development, also start the API in Development, open {ui} and confirm it loads, even when startup and composition did not change. The step does not apply when the project exposes no such UI. If the application cannot run in this environment, report the check as NOT RUN with the reason; never report it as passed."
ANCHOR = 'A successful build alone does not prove runtime composition.'


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


SW = 'the Development Swagger UI'
PATCHES = [
    ('M', '.claude/skills/verify/SKILL.md', ANCHOR + '\n', ANCHOR + '\n\n' + wrap(STEP.format(ui=SW)) + '\n'),
    ('M', '.claude/skills/swagger/SKILL.md', """4. open the Development Swagger UI and confirm it loads;
""", """4. open the Development Swagger UI and confirm it loads (obligation and its
   condition: `verify`);
"""),
    ('M1', '.claude/skills/verify/SKILL.md', 'A successful build\nalone does not prove runtime composition.\n', 'A successful build\nalone does not prove runtime composition.\n\n' + wrap(STEP.format(ui=SW)) + '\n'),
    ('M1', '.claude/skills/swagger/SKILL.md', """open the Development Swagger UI and confirm it loads, exercise representative
""", """open the Development Swagger UI and confirm it loads (obligation and its
condition: `verify`), exercise representative
"""),
    ('L0', '.claude/skills/verify/SKILL.md', ANCHOR + '\n', ANCHOR + '\n\n' + STEP.format(ui=SW) + '\n'),
    ('L0', '.claude/skills/swagger/SKILL.md', """## Verification after API changes

Verify controller behavior and integration tests, verify the response metadata, start the API when startup/composition changed, open the Development Swagger UI, exercise representative endpoints""",
     """## Verification after API behavior changes

Verify controller behavior and integration tests, verify the response metadata, start the API when startup/composition changed, open the Development Swagger UI and confirm it loads (obligation and its condition: `verify`), exercise representative endpoints"""),
    ('L1', '.claude/skills/verify/SKILL.md', ANCHOR + '\n', ANCHOR + '\n\n' + STEP.format(ui='the Development API documentation UI') + '\n'),
    ('L1', '.claude/skills/swagger/SKILL.md', "start the API when startup/composition changed, open the Development Swagger UI, exercise representative endpoints when meaningful,",
     "start the API when startup/composition changed, open the Development Swagger UI and confirm it loads (obligation and its condition: `verify`), exercise representative endpoints when meaningful,"),
    ('K0', '.claude/skills/verify/SKILL.md', ANCHOR + '\n', ANCHOR + '\n\n' + STEP.format(ui=SW) + '\n'),
    ('K0', '.claude/skills/swagger/SKILL.md', """## Verification after API changes
""", """## Verification after API behavior changes
"""),
    ('K0', '.claude/skills/swagger/SKILL.md', """5. Open the Development Swagger UI and confirm it loads.
""", """5. Open the Development Swagger UI and confirm it loads (see also: `verify`, which owns this obligation and its condition).
"""),
    ('K1', '.claude/skills/verify/SKILL.md', ANCHOR + '\n', ANCHOR + '\n\n' + STEP.format(ui=SW) + '\n'),
    ('K1', '.claude/skills/swagger/SKILL.md', "open the Development Swagger UI and confirm it loads, exercise representative endpoints when that is a meaningful check,",
     "open the Development Swagger UI and confirm it loads (see also: `verify`, which owns this obligation and its condition), exercise representative endpoints when that is a meaningful check,"),
]
