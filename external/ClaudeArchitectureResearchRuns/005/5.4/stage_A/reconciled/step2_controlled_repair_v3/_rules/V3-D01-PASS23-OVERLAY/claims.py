"""V3-D01 per-claim gate entries: one per facet update, in order (claimgate.py). ADDED records are checked by the full gate."""
import importlib.util
import os

_spec = importlib.util.spec_from_file_location('v3d01_updates', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'updates.py'))
_u = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_u)
CLAIMS = [dict(id='V3-D01-F%02d' % i, key=f['key'], path=f['path'], quote=f['quote'], set={'codex_pass23_ids': f['ids']}, claim=f['claim'], note=f['note'], kind='FACET_WRITTEN_IN') for i, f in enumerate(_u.FACETS, 1)]
