"""Parser for the audit's reader files.

Blind file (one line per record, written before stored fields are shown):
  KEY || cls=CD mod=DEFAULT dom=WF rel=PE pol=WF-005~,API-016 conf=M || actor=..; act=..; trig=..; scope=..; exc=..; time=..; enf=.. || test=..

Decision file (block per case):
  @CASE DECISION conf=M [dep=PI012|HUMAN] [neg=SUBCLASS] [cls=CLASSIFICATION|MODALITY|FIELD|SUBCLAUSE|...]
  why: rationale
  q: PATH:A-B | exact quote           verified against the immutable file at build
  set field=value                     one field per line; subclauses and lists as JSON
  amb: remaining ambiguity
  alt: unresolved alternative reading
  hd: human decision question
"""
import glob
import json
import os
import re

from acommon import CANDIDATES, DEC, ROOT, quote_in_source

CLS = {'CO': 'CANONICAL_ONLY', 'CD': 'CANONICAL_PLUS_DELTA', 'XP': 'EXTRA_PRODUCT', 'XW': 'EXTRA_WORKFLOW', 'IA': 'INTERNAL_ARCHITECTURE',
       'NN': 'NON_NORMATIVE', 'MX': 'MIXED', 'UN': 'UNCERTAIN'}
DOM = {'PE': 'PRODUCT_ENGINEERING', 'WF': 'WORKFLOW_ENFORCEMENT', 'IA': 'INSTRUCTION_ARCHITECTURE', 'MX': 'MIXED', 'NN': 'NON_NORMATIVE', 'UN': 'UNCERTAIN'}
REL = {'FE': 'FULLY_ENTAILED', 'PE': 'PARTIALLY_ENTAILED', 'NE': 'NOT_ENTAILED', 'NA': 'NOT_APPLICABLE', 'UN': 'UNCERTAIN'}
CONF = {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}
DECISIONS = {'UPHOLD', 'CORRECT', 'UNRESOLVED', 'NOT_A_SEPARATE_CLAUSE', 'OVERMERGE_FACET', 'EVIDENCE_CONFLICT'}
FIELDS_KEY = {'actor': 'actor', 'act': 'behavior', 'trig': 'trigger', 'scope': 'scope', 'exc': 'exception', 'time': 'timing', 'enf': 'enforcement'}


def parse_pol(s):
    if not s or s in ('-', '[]'):
        return []
    return [{'policy_id': p.rstrip('~'), 'coverage': 'PARTIAL' if p.endswith('~') else 'FULL'} for p in s.split(',')]


def parse_blind_line(raw, where):
    parts = [p.strip() for p in raw.split('||')]
    if len(parts) != 4:
        raise SystemExit('%s: blind line needs 4 parts: %s' % (where, raw[:120]))
    key, toks, facts, test = parts
    t = dict(x.split('=', 1) for x in toks.split())
    out = {'source_key': key, 'classification': CLS[t['cls']], 'modality': t.get('mod'), 'domain': DOM.get(t.get('dom')), 'oracle_relation': REL.get(t.get('rel')),
           'canonical_coverage': parse_pol(t.get('pol')), 'confidence': CONF[t['conf']]}
    fx = {}
    for m in re.finditer(r'(?:^|;\s*)(actor|act|trig|scope|exc|time|enf)=(.*?)(?=;\s*(?:actor|act|trig|scope|exc|time|enf)=|$)', facts):
        fx[FIELDS_KEY[m.group(1)]] = m.group(2).strip()
    for f in FIELDS_KEY.values():
        if f not in fx:
            raise SystemExit('%s: blind line for %s lacks %s' % (where, key, f))
    out['facts'] = fx
    if not test.startswith('test='):
        raise SystemExit('%s: test= missing for %s' % (where, key))
    out['entailment_test'] = test[5:].strip()
    return out


def load_blind():
    """Key -> blind reading and the batch that holds it."""
    d = {}
    for p in sorted(glob.glob(os.path.join(DEC, '*.blind'))):
        name = os.path.basename(p)[:-6]
        for i, raw in enumerate(open(p, encoding='utf-8'), 1):
            if not raw.strip() or raw.startswith('#'):
                continue
            r = parse_blind_line(raw.rstrip('\n'), '%s:%d' % (name, i))
            if r['source_key'] in d:
                raise SystemExit('duplicate blind reading for %s in %s and %s' % (r['source_key'], d[r['source_key']]['batch'], name))
            r['batch'] = name
            d[r['source_key']] = r
    return d


def parse_value(field, v):
    v = v.strip()
    if field == 'canonical_coverage':
        return parse_pol(v)
    if v == 'null':
        return None
    if v in ('true', 'false'):
        return v == 'true'
    if v[:1] in '[{':
        return json.loads(v)
    return v


def load_decisions():
    """Case -> decision block."""
    d = {}
    for p in sorted(glob.glob(os.path.join(DEC, '*.dec'))):
        name = os.path.basename(p)[:-4]
        cur = None
        for i, raw in enumerate(open(p, encoding='utf-8'), 1):
            line = raw.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            if line.startswith('@'):
                toks = line[1:].split()
                case, dec = toks[0], toks[1]
                if case in d:
                    raise SystemExit('duplicate decision for %s: %s and %s:%d' % (case, d[case]['src'], name, i))
                cur = {'case': case, 'decision': dec, 'src': '%s:%d' % (name, i), 'batch': name, 'why': None, 'quotes': [], 'set': {}, 'amb': None, 'alt': [], 'hd': [], 'extra': {}}
                for t in toks[2:]:
                    k, v = t.split('=', 1)
                    cur['extra'][k] = v
                d[case] = cur
                continue
            if cur is None:
                raise SystemExit('%s:%d: line before first block' % (name, i))
            m = re.match(r'^(why|amb|alt|hd|note):\s*(.*)$', line)
            if m:
                k, v = m.group(1), m.group(2)
                if k in ('alt', 'hd'):
                    cur[k].append(v)
                elif k == 'note':
                    cur['extra'].setdefault('notes', []).append(v)
                else:
                    cur[k] = v
                continue
            m = re.match(r'^q:\s*(\S.*?):(\d+)-(\d+)\s*\|\s*(.+)$', line)
            if m:
                cur['quotes'].append({'path': m.group(1), 'start_line': int(m.group(2)), 'end_line': int(m.group(3)), 'quote': m.group(4)})
                continue
            m = re.match(r'^set\s+([a-z_]+)=(.*)$', line)
            if m:
                cur['set'][m.group(1)] = parse_value(m.group(1), m.group(2))
                continue
            m = re.match(r'^sub\s+(\S+)\s+([a-z_]+)=(.*)$', line)
            if m:
                cur['set'].setdefault('subclause_set', {}).setdefault(m.group(1), {})[m.group(2)] = parse_value(m.group(2), m.group(3))
                continue
            m = re.match(r'^pi\s+(\S+)\s+(\S+)(?:\s+(\S+))?$', line)
            if m:
                cur['set']['modality'] = m.group(1)
                cur['set']['strength_vs_canonical'] = m.group(2)
                if m.group(3):
                    cur['set']['strength_resolution_code'] = None if m.group(3) == 'null' else m.group(3)
                continue
            raise SystemExit('%s:%d: cannot parse: %s' % (name, i, line[:160]))
    return d


def full_path(cand, path):
    """Allow a short template-relative path in q: lines."""
    return path if path.startswith('inputs/') else 'inputs/%s/output/template/%s' % (cand, path)


def verify_quote(cand, q):
    p = full_path(cand, q['path'])
    q = dict(q, path=p)
    if not os.path.exists(os.path.join(ROOT, p.replace('/', os.sep))):
        return q, False
    return q, quote_in_source(p, q['start_line'], q['end_line'], q['quote'])
