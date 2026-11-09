"""V3-D02 modality correction from the individual review of the 86 v2 records (MARKED_NEVER_86_REVIEW.jsonl). One proved error."""
RULE = 'V3-D02-MODALITY86'
UPDATES = {
    'FG-M-8b2c02178e': dict(rule=RULE, status='CLASSIFICATION_CORRECTED', claim=None,
                            note='V3-D02: the record holds only the marked ban "Do not introduce NgModules for ordinary feature development unless ... genuinely requires them" (M rules/angular.md); no default marker governs it; M1 stores the same sentence MUST_NOT; the record was already STRONGER than FE-001. DEFAULT -> MUST_NOT.',
                            set={'modality': 'MUST_NOT'}, sub={}),
}
ADDED = []
