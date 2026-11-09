"""R17 label sweep: the audit moved M1's record to CD because the cited policies bind implementation and this line binds what a scan recommends. The same text in the other five stayed CO. The line is read at source in each."""
DELTA = 'Limits on what a security scan may recommend, and a preference for the smallest secure change.'
SCEN = 'A scan report recommends blanket field encryption as optional hardening and nothing is implemented: the cited policies hold; this line does not.'
F = dict(classification='CANONICAL_PLUS_DELTA', confidence='MEDIUM', distinguishing_scenario=SCEN, domain='WORKFLOW_ENFORCEMENT', extra_fragment=DELTA, extra_fragment_kind='EXTRA_WORKFLOW', oracle_relation='PARTIALLY_ENTAILED', strength_vs_canonical='STRONGER')
OVERLAY = [dict(key=k, set=dict(F), reading='Same line as FG-M1-bbde8b1664; the recommendation limit is a workflow remainder.', quote=q) for k, q in [
    ('FG-M-f19c99c143', 'Prefer the smallest secure change'), ('FG-L0-f41b087f2b', 'Prefer the smallest secure change'), ('FG-L1-f1cfb7e9ad', 'Recommend the smallest secure change'), ('FG-K0-7554ba8fd1', 'Recommend the smallest secure change'),
    ('FG-K1-969998d857', 'Prefer the smallest secure change'), ('FG-K1-742e9f74e1', 'Prefer the smallest secure change')]]
