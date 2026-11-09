"""Source review for R07."""
VERIFY = '.claude/skills/verify/SKILL.md'
SWAGGER = '.claude/skills/swagger/SKILL.md'
PROBE = {'M': 'represent that behavior in maintained automated test coverage', 'M1': 'Preserve Behavioral Verification', 'L0': 'preserve', 'L1': 'preserve that behavior in maintained automated tests', 'K0': 'preserve', 'K1': 'preserve'}
UI = {'M': 'the Development Swagger UI', 'M1': 'the Development Swagger UI', 'L0': 'the Development Swagger UI', 'L1': 'the Development API documentation UI', 'K0': 'the Development Swagger UI', 'K1': 'the Development Swagger UI'}
REVIEW = []
for c in UI:
    REVIEW.append(dict(policy='WF-006', candidate=c, verdict='HOLDS_WITH_NOTE', quotes=[(VERIFY, 'A successful build alone does not prove runtime composition'), (VERIFY, 'open %s and confirm it loads' % UI[c]), (VERIFY, 'even when startup and composition did not change')],
                       note='WF-006 stays as it was for new applications and substantial changes. The new step is a user-approved workflow remainder (register 8.1), equal in all six. Classification records a remainder, not a canonical entailment: a controller status change with passing tests and no UI opened still meets WF-005, WF-006, API-016 and TST-010.',
                       counterexample='No UI in the project: the step does not apply. App cannot run here: reported NOT RUN, so a green report cannot claim the UI loaded.'))
    REVIEW.append(dict(policy='WF-005', candidate=c, verdict='HOLDS', quotes=[(VERIFY, 'Build' if c in ('M', 'M1', 'K1') else 'Build')], note='Build and test steps untouched.'))
    REVIEW.append(dict(policy='API-016', candidate=c, verdict='HOLDS', quotes=[(SWAGGER, 'metadata')], note='Metadata duty untouched; opening the UI adds no speculative response.'))
    REVIEW.append(dict(policy='TST-010', candidate=c, verdict='HOLDS', quotes=[(VERIFY, PROBE[c])], note='Opening the UI is a check, and the probe-to-test duty is untouched.'))
