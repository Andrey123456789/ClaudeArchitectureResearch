"""Architecture-identity invariants, compared with the frozen baseline. Technology-neutrality terms are the leaf technologies named in the L0 and L1 candidate definitions."""
import os
import re

from rcommon import CANDIDATES, input_template_root, read_lines, sha256_file, template_root, walk_files, wc_path

LEAF_TERMS = re.compile(r'\b(EF Core|Entity Framework|DbContext|DbSet|NUnit|xUnit|Angular|RxJS|Serilog|FluentValidation|Swashbuckle|Swagger|Redis|Polly|HybridCache|MediatR|Docker|SQL Server|SqlServer)\b')
SLOTS = {'architecture', 'persistence', 'backend-testing', 'frontend'}


def text(c, rel):
    with open(wc_path(c, rel), encoding='utf-8', errors='replace') as f:
        return f.read()


def rule_files(c):
    return [r for r in walk_files(template_root(c)) if r.startswith('.claude/rules/') and r.endswith('.md')]


def base_terms(c, rel):
    p = os.path.join(input_template_root(c), rel.replace('/', os.sep))
    if not os.path.exists(p):
        return set()
    with open(p, encoding='utf-8', errors='replace') as f:
        return set(LEAF_TERMS.findall(f.read()))


def check(c):
    errs = []
    root = template_root(c)
    cur, base = set(walk_files(root)), set(walk_files(input_template_root(c)))
    for f in sorted(cur - base):
        errs.append('file added: %s' % f)
    for f in sorted(base - cur):
        errs.append('file removed: %s' % f)
    rules = rule_files(c)
    has_caps = os.path.isdir(os.path.join(root, '.claude', 'capabilities'))
    slots = set(os.listdir(os.path.join(root, '.claude', 'capabilities'))) if has_caps else set()
    heads = {r: (read_lines(wc_path(c, r))) for r in rules}
    level_hdr = [r for r, ls in heads.items() if any(re.match(r'^> .*\bLevel:', x) for x in ls[:60])]
    kind_hdr = [r for r, ls in heads.items() if any(re.match(r'^> .*\bKind:', x) for x in ls[:60])]
    subdirs = {r.split('/')[2] for r in rules if r.count('/') > 2}
    if c in ('M', 'M1'):
        if subdirs:
            errs.append('rules not flat: %s' % sorted(subdirs))
        if level_hdr or kind_hdr:
            errs.append('Level or Kind headers present')
    if c == 'M' and has_caps:
        errs.append('M has capabilities')
    if c in ('L0', 'L1'):
        if not {'0-core', '1-architecture', '2-technology', '3-project'} <= subdirs:
            errs.append('level directories missing')
        if len(level_hdr) != len(rules):
            errs.append('rules without Level header: %s' % sorted(set(rules) - set(level_hdr)))
        if kind_hdr:
            errs.append('Kind header present')
        for r in rules:
            if r.startswith(('.claude/rules/0-core/', '.claude/rules/1-architecture/')):
                new = set(LEAF_TERMS.findall(text(c, r))) - base_terms(c, r)
                if new:
                    errs.append('neutrality: %s newly names %s' % (r, sorted(new)))
    if c in ('K0', 'K1'):
        if not subdirs <= {'common', 'backend', 'backend-tests', 'frontend', 'delivery'}:
            errs.append('rules not scope-first: %s' % sorted(subdirs))
        if len(kind_hdr) != len(rules):
            errs.append('rules without Kind header: %s' % sorted(set(rules) - set(kind_hdr)))
        if level_hdr:
            errs.append('Level header present')
        if not os.path.exists(wc_path(c, 'docs/architecture/decision-register.md')):
            errs.append('decision register missing')
        if '@docs/architecture/decision-register.md' not in text(c, 'CLAUDE.md'):
            errs.append('register import missing')
    if c in ('M1', 'L1', 'K1') and slots != SLOTS:
        errs.append('slots differ: %s' % sorted(slots))
    if c in ('L0', 'K0') and has_caps:
        errs.append('%s has capabilities' % c)
    if c in ('M1', 'K1', 'L1'):
        for s in SLOTS:
            if not os.path.exists(os.path.join(root, '.claude', 'capabilities', s, 'CONTRACT.md')):
                errs.append('contract missing: %s' % s)
    return errs


def check_all(cands=None):
    return {c: check(c) for c in cands or CANDIDATES}
