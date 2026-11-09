"""Each blind-reread disagreement, read at source with the stored fields and the policy text. Written after the comparison, so it is not blind. STORED_UPHELD: the stored label stands. CORRECTED: a disposition changed the record. QUALIFIED: the stored label stays, and the reading names a real limit."""


def r(result, why):
    return dict(result=result, why=why)


ROWS = {
    'B02': r('STORED_UPHELD', 'The delta is real: naming user-secrets goes beyond the "appropriate local mechanism" of SEC-002. The blind reader did not have the policy text.'),
    'B07': r('STORED_UPHELD', 'Both subclauses are DEFAULT, the force the reader gave. Top-level MIXED marks a split compound.'),
    'B09': r('STORED_UPHELD', '"Add only the references the layout shows" is stricter than ARC-028, so the delta and STRONGER stand. Force agreed.'),
    'B13': r('CORRECTED', 'The source says "Never place frontend tests under backend/". M1, L1 and K0 store the same ban as MUST_NOT. Corrected by C07-N2, with its sibling by C07-N3 and the L0 record by C07-N1.'),
    'B14': r('STORED_UPHELD', 'Naming the registration package goes beyond DEP-010, so the delta stands. Force agreed.'),
    'B16': r('STORED_UPHELD', 'A marked "do not" keeps its force under A1.3. The reader applied the knowledge-skill default too widely. The links to GOV-013 and TST-004 stand.'),
    'B17': r('STORED_UPHELD', 'No policy says when each DI technique fits; GOV-012 is only a general preference. Force agreed.'),
    'B18': r('STORED_UPHELD', 'A documented reason goes beyond the "normally" of DEP-006, so the delta stands. Force agreed.'),
    'B19': r('STORED_UPHELD', 'The second cited range holds the sentence, so the reader\'s note on the first range was not a defect. Same-commit tests go beyond WF-022.'),
    'B20': r('STORED_UPHELD', 'RUN-018 limits fallback but asks nobody to make this decision, so EXTRA stands. Force agreed.'),
    'B22': r('STORED_UPHELD', 'API-003 and API-010 do not set the 400 and 422 split, so EXTRA stands. Force agreed.'),
    'B24': r('STORED_UPHELD', 'The inventory has no nullable policy. A props value is a default a project can override, so BINDING overread it.'),
    'B26': r('STORED_UPHELD', 'The any-yes test goes beyond GOV-017, so the delta and STRONGER stand. Force agreed.'),
    'B29': r('STORED_UPHELD', 'Both subclauses are DEFAULT, the force the reader gave, and no policy entails them.'),
    'B31': r('STORED_UPHELD', 'Other cited ranges state and enforce it: check-instructions errors when a rule sits outside a level directory or has no paths. The first range misled the reader.'),
    'B33': r('QUALIFIED', 'Stays DEFAULT: the record\'s primary line sits under "Repository defaults" in decisions.md and carries no marked form. Its "never" clause comes from layout.md, and C07-N1 now holds that clause at MUST_NOT.'),
    'B36': r('STORED_UPHELD', 'API-018 does not mention code-quality grading, so EXTRA stands. Force agreed.'),
    'B41': r('QUALIFIED', 'Stays SHOULD: the hook reports and does not block, and DEP-020 is DEFAULT. The JSON key reads "approvalRequired", so an agent may take it as binding. That is a real ambiguity in the delivery.'),
}
