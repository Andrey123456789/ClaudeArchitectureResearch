"""R15: item 8.5 HTTP timeout. Markdown must stay as it was: the suite checks the lines are byte-identical to the frozen inputs and that the label sweep is well-formed."""
from rcommon import CANDIDATES, input_path, sha256_file, wc_path
from suitelib2 import anchors, check_overlay


def run(ctx):
    f = '.claude/skills/http-api/SKILL.md'
    for c in CANDIDATES:
        ctx.check('http-api skill untouched', sha256_file(wc_path(c, f)) == sha256_file(input_path(c, f)), candidate=c, kind='SOURCE')
    anchors(ctx, 'three timeout cases distinguished', {'M': (f, ['distinguish a client-cancelled request, our own operation timing out, and an upstream dependency timing out']), 'M1': (f, ['Not for every internal `TaskCanceledException`']),
                                                      'L0': (f, ['the client cancelled the incoming request; our own operation timed out; an upstream dependency timed out']), 'L1': (f, ['Distinguish client cancellation, our own timeout, and upstream timeout']),
                                                      'K0': (f, ['distinguish a client-cancelled request, our own operation timing out, and an upstream dependency timing out']), 'K1': (f, ['Distinguish client cancellation of the incoming request, our own operation timing out, and an upstream timeout'])})
    check_overlay(ctx, 'R15-85-HTTPTIMEOUT')
