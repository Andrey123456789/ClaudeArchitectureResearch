"""Run one rule's suite only, to see tests fail before a patch (contract step B). Writes nothing except a pre-change result file."""
import importlib.util
import json
import os
import sys
from collections import Counter

from rcommon import OUT, utf8_stdout, write_jsonl
from sandbox import cleanup_runs
from suitelib import Ctx


def main():
    utf8_stdout()
    rule = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else 'pre'
    p = os.path.join(OUT, '_tools', 'suites', rule.replace('-', '_') + '.py')
    spec = importlib.util.spec_from_file_location('s', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ctx = Ctx(rule)
    mod.run(ctx)
    write_jsonl(os.path.join('_rules', rule, 'suite_%s.jsonl' % label), ctx.rows)
    print(dict(Counter(r['status'] for r in ctx.rows)))
    for r in ctx.rows:
        if r['status'] == 'FAIL':
            print('FAIL', r['candidate'], r['test'], '|', r['detail'][:200])
    cleanup_runs()


if __name__ == '__main__':
    main()
