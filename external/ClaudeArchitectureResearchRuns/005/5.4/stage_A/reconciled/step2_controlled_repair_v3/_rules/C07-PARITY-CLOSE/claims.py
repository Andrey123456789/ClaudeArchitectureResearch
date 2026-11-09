"""C07 dispositions, in order, for the per-claim gate and the full replay. D rows add a qualifier and move nothing. N rows correct a stored modality where the same marked ban is stored differently across candidates."""
RULE = 'C07-PARITY-CLOSE'
SCAN = '.claude/skills/security-scan/references/scan-layers.md'
QUALIFIER = 'R20-DESER-FORMS: in all six this line sits in the private scan layer of security-scan, in different forms: marked in M, M1, L0, K1; an audit criterion in K0; a list item in L1. No candidate states the prohibition outside that layer. The stored modality reports the form, and the difference between candidates is not a strictness fact. The line states no condition of its own, except where its applicability field says so.'
DESER = [
    ('FG-M-bea4987bb6', 'deserialize untrusted payloads into arbitrary runtime types'),
    ('FG-M1-c6cfdc9dbf', 'deserialize untrusted payloads into arbitrary runtime types'),
    ('FG-L0-009161dd35', 'never deserialize untrusted payloads into arbitrary runtime types'),
    ('FG-L1-d6ab123b1f', 'deserializing untrusted payloads into arbitrary runtime types'),
    ('FG-K0-0ef1e5ed3d', 'Untrusted payloads are not deserialized into arbitrary runtime types'),
    ('FG-K0-6d06b21a93', 'Untrusted payloads are not deserialized into arbitrary runtime types'),
    ('FG-K1-112617f8b3', 'Untrusted payloads must not deserialize into arbitrary runtime types'),
]
CLAIMS = [dict(id='C07-D%d' % i, key=k, path=SCAN, quote=q, set=dict(comparison_qualifier=QUALIFIER), claim=None, note='C07: qualifier only, modality unchanged.', kind='QUALIFIER') for i, (k, q) in enumerate(DESER, 1)]
CLAIMS.append(dict(id='C07-D8', key='FG-L0-29a3230807', path='.claude/skills/delivery-pipeline/SKILL.md', quote='Do not let CI upgrade packages automatically unless the project adopted automated dependency updates', set=dict(evaluation_scope='OUT_OF_PRACTICAL_EVALUATION_CI'), claim=None, note='C07: the v1 report says the CI update rule is labelled out of practical evaluation in all six. L0\'s record had no label. Only the label changes.', kind='LABEL_ADDED'))
BAN = 'Never place frontend tests under `backend/`'
WHY = 'C07: the source says "Never place frontend tests under backend/". M1, L1 and K0 store the same ban as MUST_NOT. A1.3 keeps a marked form, so DEFAULT here was a label difference with no text behind it. Found by the blind reread. No coverage or strength cell moves.'
LAYOUT = '.claude/skills/project-structure/references/solution-layout.md'
CLAIMS += [
    dict(id='C07-N1', key='FG-L0-a2e9e91e8f', path='.claude/rules/3-project/layout.md', quote=BAN, set=dict(modality='MUST_NOT', strength_resolution_code='SL'), claim=None, note=WHY + ' Resolution as for the same compound in L1, FG-L1-75964b0d7f.', kind='MODALITY_CORRECTED'),
    dict(id='C07-N2', key='FG-K1-4767fd97b1', path=LAYOUT, quote=BAN, set=dict(modality='MUST_NOT', strength_resolution_code='PC'), claim=None, note=WHY + ' Resolution as for the same ban in M1 and K0.', kind='MODALITY_CORRECTED'),
    dict(id='C07-N3', key='FG-K1-bc831815a3', path=LAYOUT, quote=BAN, set=dict(modality='MUST_NOT', strength_resolution_code='PC'), claim=None, note=WHY + ' Resolution as for the same ban in M1 and K0.', kind='MODALITY_CORRECTED'),
]
