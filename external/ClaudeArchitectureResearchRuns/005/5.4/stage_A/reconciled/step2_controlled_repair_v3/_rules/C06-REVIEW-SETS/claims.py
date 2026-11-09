"""C06 dispositions for the per-claim gate: one per flagged record. No classification or modality moves; the flag and its reason follow the reading."""
import importlib.util

from rcommon import norm_ws, out_path, read_jsonl, read_lines, v1_path, wc_path

RULE = 'C06-REVIEW-SETS'
_s = importlib.util.spec_from_file_location('c06_rn', out_path('_rules', RULE, 'review_needed.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
_v1 = {r['source_key']: r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}


def _anchor(key):
    """A short quote at the record's first v1 evidence, re-found on current bytes by the gate."""
    r = _v1[key]
    for e in r.get('current_evidence_refs') or []:
        if e.get('start_line'):
            rel = e['path'].split('/template/')[1]
            c = e['path'].split('/')[1]
            ls = read_lines(wc_path(c, rel))
            for line in ls[e['start_line'] - 1:e['end_line']]:
                if len(norm_ws(line)) > 12:
                    return rel, norm_ws(line)[:70]
            return rel, norm_ws(' '.join(ls))[:70]
    raise KeyError(key)


CLAIMS = []
for i, row in enumerate(_m.ROWS, 1):
    keep = row['status'] in ('NOT_VERIFIED', 'UNRESOLVED')
    try:
        rel, quote = _anchor(row['key'])
    except FileNotFoundError:
        raise
    sets = dict(review_needed=keep, review_reason=row['reason'] if keep else None, review_disposition=row['status'], review_disposition_note=row['reason'])
    CLAIMS.append(dict(id='C06-F%02d' % i, key=row['key'], path=rel, quote=quote, set=sets, claim=None, note=row['reason'], kind='FLAG_' + row['status']))
