"""Every distinct part of a parenthesis in the original trigger, on records with no extracted condition, split into scope and delivery as scope_hint splits it. Writes _rules/C06B-R22-APPLICABILITY/PARENTHESIS_CENSUS.json. Each part was read; the file pins that reading to the data."""
import os
import re
from collections import Counter

from rcommon import out_path, read_jsonl, utf8_stdout, write_json
from triggers import DELIVERY_PAREN


def parts(rows):
    kept, dropped = Counter(), Counter()
    for r in rows:
        if r.get('applicability_status') not in ('UNKNOWN_NOT_EXTRACTED', 'CONDITION_IN_CLAIM_TEXT'):
            continue
        for group in re.findall(r'\(([^()]+)\)', r.get('trigger_field_original') or r.get('trigger') or ''):
            for p in group.split(';'):
                p = p.strip()
                if p:
                    (dropped if DELIVERY_PAREN.search(p) else kept)[p] += 1
    return {'kept': dict(sorted(kept.items())), 'dropped': dict(sorted(dropped.items()))}


def main():
    utf8_stdout()
    out = parts(read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl')))
    write_json(os.path.join('_rules', 'C06B-R22-APPLICABILITY', 'PARENTHESIS_CENSUS.json'), out)
    print({k: (len(v), sum(v.values())) for k, v in out.items()})


if __name__ == '__main__':
    main()
