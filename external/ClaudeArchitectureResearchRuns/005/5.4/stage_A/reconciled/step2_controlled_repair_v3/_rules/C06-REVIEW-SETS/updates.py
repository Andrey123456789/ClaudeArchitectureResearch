"""C06 updates for the full replay, built from the same dispositions the per-claim gate applied."""
import importlib.util

from rcommon import out_path

RULE = 'C06-REVIEW-SETS'
_spec = importlib.util.spec_from_file_location('c06_claims_for_updates', out_path('_rules', RULE, 'claims.py'))
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
UPDATES = {c['key']: dict(rule=RULE, status='UPDATED', claim=c.get('claim'), note=c['note'], set=c['set'], sub={}) for c in _m.CLAIMS}
