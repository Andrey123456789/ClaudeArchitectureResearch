"""End-of-run audit of Addendum A1.3 (modality of technique text). Reads only; --write stores the findings.

Finds CO, CD, XP and XW records and subclauses recorded at MUST or MUST_NOT whose evidence lies only in
knowledge skills or private references and whose full evidence text has no must-like marker.

Categories:
  A  MUST with no marker: an unmarked positive imperative or statement; A1.3 makes it DEFAULT.
  B  MUST_NOT with no marker and no negative wording: same.
  C  MUST_NOT resting on 'avoid': SHOULD_NOT, weaker than a stronger policy.
  N  MUST_NOT with a flat negative ('no X', 'not X', 'only when', 'without'): outside A1.3, which addresses
     positive imperatives; kept and listed in COVERAGE_LIMITATIONS.

A record with a marker anywhere in its evidence is not reported, even if the marker belongs to another clause
of a broad group. The audit therefore shows no more than a floor for this defect class.

Usage: python -B _tools/a13_audit.py [--write]
"""
import collections
import json
import os
import re
import sys

from common import CANDIDATES, OUT, ROOT, policies

RANK = {'MUST': 3, 'MUST_NOT': 3, 'DECIDED': 3, 'REQUIRES_APPROVAL': 3, 'DEFAULT': 2, 'SHOULD': 2, 'SHOULD_NOT': 2, 'MAY': 1}
MARKER = re.compile(r"\b(must|mustn't|never|do not|don't|shall|forbid\w*|forbidden|cannot|can't|may not|requires?|required)\b", re.I)
NEGATIVE = re.compile(r"\b(no|not|only|without|rather than|instead of|out of|never|none|nothing|unless)\b", re.I)
AVOID = re.compile(r"\bavoid\w*\b", re.I)
KNOWLEDGE = set('httpclient-factory http-api ef-core swagger caching authentication api-versioning dependency-injection '
                'logging angular health-check docker aspnet-error-handling configuration dotnet-testing modern-csharp '
                'ci-cd'.split())
TARGET = ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW', 'CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA')


def source_kind(path):
    m = re.search(r'\.claude/skills/([^/]+)/(.*)', path)
    if not m:
        return None
    if m.group(1) in KNOWLEDGE:
        return 'KNOWLEDGE_SKILL'
    if m.group(2).startswith('references/'):
        return 'PRIVATE_REFERENCE'
    return None


def evidence_text(refs):
    parts = []
    for ref in refs:
        lines = open(os.path.join(ROOT, ref['path']), encoding='utf-8').read().split('\n')
        parts.append(' '.join(lines[ref['start_line'] - 1:ref['end_line']]))
    return re.sub(r'\s+', ' ', ' // '.join(parts))


def scan():
    pol = policies()
    out = []
    for cand in CANDIDATES:
        for line in open(os.path.join(OUT, 'per_candidate', cand, 'CLASSIFICATIONS.jsonl'), encoding='utf-8'):
            rec = json.loads(line)
            refs = rec.get('evidence_refs') or []
            kinds = {source_kind(r['path']) for r in refs}
            if not kinds or None in kinds:
                continue
            text = evidence_text(refs)
            if MARKER.search(text):
                continue
            objs = [(rec['source_key'], rec)] + [('%s/%s' % (rec['source_key'], s['subclause_id']), s) for s in rec.get('subclauses') or []]
            for key, obj in objs:
                if obj.get('modality') not in ('MUST', 'MUST_NOT') or obj.get('classification') not in TARGET:
                    continue
                if obj['modality'] == 'MUST':
                    cat = 'A'
                elif AVOID.search(text):
                    cat = 'C'
                elif NEGATIVE.search(text):
                    cat = 'N'
                else:
                    cat = 'B'
                ids = [c['policy_id'] for c in obj.get('canonical_coverage') or []]
                res = obj.get('strength_resolution') or {}
                out.append({
                    'candidate': cand, 'key': key, 'category': cat, 'classification': obj['classification'],
                    'modality': obj['modality'], 'strength_vs_canonical': obj.get('strength_vs_canonical'),
                    'strength_code': res.get('code'), 'strength_source': res.get('source'), 'policies': ids,
                    'policy_ranks': [RANK.get(pol[p]['normative_strength'], 0) for p in ids],
                    'source_kinds': sorted(kinds), 'first_path': refs[0]['path'], 'evidence_text': text[:400],
                })
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rows = scan()
    print(sorted(collections.Counter((r['candidate'], r['category']) for r in rows).items()))
    print(sorted(collections.Counter(r['category'] for r in rows).items()))
    if '--write' in sys.argv:
        path = os.path.join(OUT, '_decisions', 'A13_AUDIT_FINDINGS.jsonl')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')
        print('wrote', path, len(rows))


if __name__ == '__main__':
    main()
