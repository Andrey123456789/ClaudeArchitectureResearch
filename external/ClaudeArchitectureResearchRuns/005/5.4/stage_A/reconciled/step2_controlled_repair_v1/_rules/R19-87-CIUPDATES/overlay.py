"""R19 labels: evaluation scope on every record of this rule, plus the audit's L0 reading applied to lines with the same content."""
SCOPE = 'OUT_OF_PRACTICAL_EVALUATION_CI'
XP = dict(canonical_coverage=[], classification='EXTRA_PRODUCT', extra_fragment_kind='EXTRA_PRODUCT', oracle_relation='NOT_ENTAILED', related_policy_ids=['WF-018', 'GOV-014'], strength_vs_canonical='N/A', strength_resolution_code=None, evaluation_scope=SCOPE)
OVERLAY = [
    dict(key='FG-L1-52a13bbaa7', set=dict(XP), reading='Same claim as FG-L0-29a3230807: no part follows from WF-018, WF-020 or GOV-014.', quote='do not auto-upgrade packages in CI unless automated updates were adopted'),
    dict(key='FG-K1-5383f42e9b', set=dict(XP), reading='Same content as FG-L0-29a3230807.', quote='no automatic package upgrades unless the project adopted automated updates'),
    dict(key='FG-K0-341d9608ae', set=dict(XP), reading='Same content as FG-L0-29a3230807, at DEFAULT in a knowledge skill.', quote='automatic dependency updates in CI need explicit adoption'),
    dict(key='FG-M-41b087b1e5', set=dict(evaluation_scope=SCOPE), reading='Compound with the security-policy clause; CD stands. Scope label added.', quote='do not upgrade packages automatically in CI'),
    dict(key='FG-K0-90efdf61c4', set=dict(evaluation_scope=SCOPE), reading='Compound with the security-policy clause; CD stands. Scope label added.', quote='automatic dependency updates in CI need explicit adoption'),
    dict(key='FG-M1-cbb81552d7', set=dict(classification='CANONICAL_PLUS_DELTA', oracle_relation='PARTIALLY_ENTAILED', extra_fragment='No automatic package upgrades in CI unless automated updates are adopted.', extra_fragment_kind='EXTRA_PRODUCT', distinguishing_scenario='A pipeline upgrades packages automatically with no adoption decision: the cited policies hold; this line does not.', evaluation_scope=SCOPE), reading='Same compound as M, which is CD; stored CO hid the remainder.', quote='do not upgrade packages automatically in CI'),
]
