"""Draft dispositions for changed evidence ranges: for each range with no disposition, the longest fragment of the original text (split at
sentence and clause marks) that still stands in the current file. A draft only; the rule's dispositions.py is written after reading each.

PYTHONPATH=_tools python -B _tools/disp_draft.py <RULE> <C> [<C> ...]
"""
import re
import sys

from rcommon import input_path, norm_ws, read_lines, utf8_stdout, wc_path
from witness import changed_ranges


def main():
    utf8_stdout()
    rule, cands = sys.argv[1], sys.argv[2:]
    out = []
    for (c, rel, a, b), row in sorted(changed_ranges(cands).items()):
        if row['disposition']:
            continue
        orig = norm_ws(' '.join(read_lines(input_path(c, rel))[a - 1:b]))
        cur = norm_ws(' '.join(read_lines(wc_path(c, rel))))
        parts = sorted({p.strip() for p in re.split(r'(?<=[.;:|])\s+|\s\|\s', orig) if len(p.strip()) > 15}, key=len, reverse=True)
        quote = next((p for p in parts if p in cur), None)
        out.append((c, rel, a, b, quote, row['keys']))
        print("    d(%r, %r, %d, %d, %r, NOTE)," % (c, rel, a, b, quote))
        print('      # keys: %s' % ', '.join(row['keys'][:8]))
    missing = [o for o in out if not o[4]]
    print('ranges', len(out), 'without a surviving fragment', len(missing))


if __name__ == '__main__':
    main()
