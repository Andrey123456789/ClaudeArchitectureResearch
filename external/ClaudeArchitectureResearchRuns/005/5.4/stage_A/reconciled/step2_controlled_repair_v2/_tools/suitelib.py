"""Shared test vocabulary for rule suites.

A suite is _tools/suites/<rule key>.py with run(ctx) returning nothing and calling ctx.add(...). Status is PASS, FAIL or NOT_RUN; NOT_RUN never counts as PASS.
Text postconditions are small semantic anchors: normalized must-have and must-not-have phrases in named files. They are regression tripwires
for a reading established in the rule's semantic review, not a proof of meaning by themselves.
"""
import os
import re
import shutil

from rcommon import norm_ws, read_lines, wc_path
from sandbox import fresh_copy


class Ctx:
    def __init__(self, rule):
        self.rule = rule
        self.rows = []

    def add(self, test, status, detail='', candidate=None, kind='TEXT', expect=None, actual=None):
        self.rows.append({'suite': self.rule, 'test': test, 'candidate': candidate, 'kind': kind, 'status': status, 'detail': str(detail)[:800], 'expect': expect, 'actual': actual})

    def check(self, test, cond, detail='', candidate=None, kind='TEXT', expect=None, actual=None):
        self.add(test, 'PASS' if cond else 'FAIL', detail, candidate, kind, expect, actual)

    def not_run(self, test, why, candidate=None, kind='RUNTIME'):
        self.add(test, 'NOT_RUN', why, candidate, kind)


def ntext(c, rel, root=None):
    p = os.path.join(root, rel.replace('/', os.sep)) if root else wc_path(c, rel)
    return norm_ws(' '.join(read_lines(p)))


def has(c, rel, phrase, root=None):
    return norm_ws(phrase).lower() in ntext(c, rel, root).lower()


def post(ctx, c, name, rel, must=(), must_not=(), root=None):
    """One text postcondition. Returns True when it holds."""
    t = ntext(c, rel, root).lower()
    miss = [m for m in must if norm_ws(m).lower() not in t]
    bad = [m for m in must_not if norm_ws(m).lower() in t]
    ok = not miss and not bad
    if ctx is not None:
        ctx.check(name, ok, 'missing=%s forbidden=%s' % (miss, bad), c, 'TEXT')
    return ok


def mutate_text(c, rel, old, new):
    """Fresh copy of the candidate with one replacement. Returns the copy root, or None when `old` is absent."""
    root = fresh_copy(c, 'mut')
    p = os.path.join(root, rel.replace('/', os.sep))
    with open(p, encoding='utf-8', newline='') as f:
        s = f.read()
    # Words of `old` may be wrapped across lines in the file.
    rx = re.compile(r'\s+'.join(re.escape(w) for w in old.split()), re.I)
    if not rx.search(s):
        shutil.rmtree(root, ignore_errors=True)
        return None
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(rx.sub(lambda m: new, s, count=1))
    return root
