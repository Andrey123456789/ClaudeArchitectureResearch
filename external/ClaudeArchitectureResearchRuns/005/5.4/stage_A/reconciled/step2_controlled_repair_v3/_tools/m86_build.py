"""Writes MARKED_NEVER_86_REVIEW.jsonl: one row per record of v2 MARKED_NEVER_SOFT_MODALITY.jsonl with the v3 source-review result.

PYTHONPATH=_tools python -B _tools/m86_build.py

Reads _adjudication/modality86/review.py (the written review) and the current view; refuses if the review does not cover exactly v2's class.
"""
import importlib.util
import sys
from collections import Counter

from rcommon import out_path, read_jsonl, utf8_stdout, v2_path, write_jsonl


def review():
    spec = importlib.util.spec_from_file_location('m86_review', out_path('_adjudication', 'modality86', 'review.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rows():
    m = review()
    cls = {r['key']: r for r in read_jsonl(v2_path('MARKED_NEVER_SOFT_MODALITY.jsonl'))}
    view = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    keys = [k for _, k, _, _, _ in m.ROWS]
    if sorted(keys) != sorted(cls) or len(keys) != len(set(keys)):
        raise SystemExit('the review does not cover exactly the v2 class: %s' % sorted(set(keys) ^ set(cls))[:5])
    out = []
    for n, key, result, code, note in m.ROWS:
        r = view[key]
        out.append({'n': n, 'key': key, 'candidate': cls[key]['candidate'], 'classification': r['classification'], 'modality_v2': cls[key]['modality'], 'modality_v3': r['modality'], 'result': result, 'reason_code': code, 'reading': note,
                    'status': 'READ_AT_SOURCE', 'reviewer': 'v3 session (same model family as Step 2; self-review)', 'rule': 'A1.3 + v2 C07 marked-form precedent'})
    return out, m


def main():
    utf8_stdout()
    out, m = rows()
    write_jsonl('MARKED_NEVER_86_REVIEW.jsonl', out)
    print(dict(Counter(x['result'] for x in out)), dict(Counter(x['reason_code'] for x in out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
