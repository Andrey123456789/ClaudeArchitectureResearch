"""Review rows for claims added in v3, in the schema of v2 NEW_CLAIMS_42_REVIEW.jsonl, written to V3_NEW_CLAIMS_REVIEW.jsonl.

Each v3 rule's updates.py ADDED entry carries `review_reading` (the source reading the claim rests on) and `review_phrases` (phrases that
must stand in the current file). A row is CONFIRMED only when every phrase stands in the current bytes and the claim anchor resolves.
v2's file is left as v2 data; the gate rebuilds this one in its DATASET step.
"""
import importlib.util
import os

from order import V3_ORDER
from rcommon import norm_ws, out_path, read_jsonl, read_lines, wc_path, write_jsonl


def build():
    rows = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    out = []
    for rule in V3_ORDER:
        p = out_path('_rules', rule, 'updates.py')
        if not os.path.exists(p):
            continue
        spec = importlib.util.spec_from_file_location('v3nc_' + rule.replace('-', '_'), p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for a in getattr(m, 'ADDED', []):
            r = rows.get(a['source_key'])
            ref = next((x for x in (r or {}).get('current_evidence_refs') or [] if x.get('start_line')), None)
            text = norm_ws(' '.join(read_lines(wc_path(a['candidate'], a['path'])))).lower() if os.path.exists(wc_path(a['candidate'], a['path'])) else ''
            phrases = a.get('review_phrases') or [a['quote']]
            missing = [ph for ph in phrases if norm_ws(ph).lower() not in text]
            ok = r is not None and ref is not None and not missing and bool(a.get('review_reading'))
            out.append({'key': a['source_key'], 'candidate': a['candidate'], 'kind': 'ADDED_CLAIM', 'rule': rule, 'classification': a['classification'], 'modality': a['modality'], 'path': a['path'],
                        'anchor': {'path': ref['path'], 'start_line': ref['start_line'], 'end_line': ref['end_line'], 'quote': a['quote']} if ref else None, 'phrases_checked': phrases,
                        'reading': a.get('review_reading') or '', 'status': 'CONFIRMED' if ok else 'NOT_CONFIRMED', 'missing_phrases': missing})
    write_jsonl('V3_NEW_CLAIMS_REVIEW.jsonl', out)
    return out


if __name__ == '__main__':
    print(len(build()))
