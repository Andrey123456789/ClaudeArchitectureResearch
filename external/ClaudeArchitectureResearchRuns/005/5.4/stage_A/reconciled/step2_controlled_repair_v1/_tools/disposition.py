"""Evidence dispositions after a template edit.

  disposition.py list [C...]     show CHANGED ranges with the records citing them, and the current text near the old line
  disposition.py build           merge _rules/*/dispositions.py into CLAIM_DISPOSITIONS.jsonl, in rule order

A dispositions.py holds DISPOSITIONS = [dict(candidate, path, start_line, end_line, disposition, new_quote, note), ...].
disposition: REWORDED, REMOVED, SPLIT or MOVED. `new_quote` must resolve in the current file (the gate checks this).
"""
import importlib.util
import os
import sys

from order import ORDER
from rcommon import CANDIDATES, baseline, input_path, norm_ws, out_path, read_lines, utf8_stdout, wc_path, write_jsonl
from witness import changed_ranges


def build(upto=None):
    rows = []
    for rule in ORDER[:ORDER.index(upto) + 1] if upto else ORDER:
        p = out_path('_rules', rule, 'dispositions.py')
        if not os.path.exists(p):
            continue
        spec = importlib.util.spec_from_file_location('d' + rule.replace('-', '_'), p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for d in mod.DISPOSITIONS:
            rows.append(dict(d, rule=rule))
    # A later rule's row for the same range supersedes the earlier one; the earlier row stays in its rule file.
    last = {}
    for r in rows:
        last[(r['candidate'], r['path'], r['start_line'], r['end_line'])] = r
    write_jsonl('CLAIM_DISPOSITIONS.jsonl', list(last.values()))
    print('dispositions', len(last))


def show(cands):
    rs = changed_ranges(cands or None)
    n = 0
    for k, row in sorted(rs.items()):
        c, rel, a, b = k
        n += 1
        d = row['disposition']
        print('%s %s:%d-%d keys=%d %s' % (c, rel, a, b, len(row['keys']), ('DISP=' + d['disposition']) if d else 'NO_DISPOSITION'))
        print('   OLD: ' + norm_ws(' '.join(read_lines(input_path(c, rel))[a - 1:b]))[:300])
        print('   keys: ' + ', '.join(row['keys'][:6]))
    print('changed ranges', n)


if __name__ == '__main__':
    utf8_stdout()
    if sys.argv[1] == 'build':
        build(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        show(sys.argv[2:])
