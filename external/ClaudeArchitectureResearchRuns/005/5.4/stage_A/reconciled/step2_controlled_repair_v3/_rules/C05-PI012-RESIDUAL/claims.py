"""C05 dispositions, in order, for the per-claim gate and the full replay. Modality changes: none. What changes: two open records close on their source context; one claim gets its lost condition back; each lead records the condition read at source."""
import importlib.util
import os

from pi012_scan import scan
from rcommon import out_path

RULE = 'C05-PI012-RESIDUAL'


def _rows():
    spec = importlib.util.spec_from_file_location('c05_extra21', out_path('_rules', RULE, 'extra21.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.ROWS


SCAN_FILE = '.claude/skills/security-scan/references/scan-layers.md'
DESER_CLAIM = 'A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not deserialized into arbitrary runtime types.'
CLOSE = dict(review_needed=False, review_reason=None, pi012_form='AUDIT_CRITERION', applicability_override='Running security-scan, unsafe deserialization layer: the code deserializes untrusted payloads.')
CLAIMS = [
    dict(id='C05-D01', key='FG-K0-0ef1e5ed3d', path=SCAN_FILE, quote='Investigate polymorphic or type-driven deserialization', set=dict(CLOSE), claim=DESER_CLAIM, note='Register 9.2. The section heading and its Investigate lead make the declarative a scan criterion. No K0 rule owns a product prohibition, and SEC-003 does not name deserialization.', kind='CLOSE_OPEN_RECORD'),
    dict(id='C05-D02', key='FG-K0-6d06b21a93', path=SCAN_FILE, quote='Untrusted payloads are not deserialized into arbitrary runtime types', set=dict(CLOSE), claim=DESER_CLAIM, note='Same line as FG-K0-0ef1e5ed3d.', kind='CLOSE_OPEN_RECORD'),
]
_scan = {x['key']: x for x in scan()['do_not_when']}
for i, row in enumerate(_rows(), 3):
    x = _scan[row['key']]
    # The scan reads frozen input lines; the sentence is unchanged on current bytes for these 21, and the per-claim gate proves it.
    CLAIMS.append(dict(id='C05-D%02d' % i, key=row['key'], path=x['path'], quote=x['sentence'][:110], set=dict(applicability_override=row['condition'], pi012_form=row['kind']), claim=row.get('claim'), note=row['reading'], kind='CONDITION_RECORDED' if row['decision'] == 'KEEP' else 'CLAIM_CONDITION_RESTORED'))
assert os.path.basename(__file__) == 'claims.py' and len(CLAIMS) == 23
