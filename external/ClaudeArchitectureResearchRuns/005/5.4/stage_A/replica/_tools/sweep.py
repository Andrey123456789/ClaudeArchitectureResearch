#!/usr/bin/env python3
"""Reverse-sweep helper (Run 2): list normative-keyword hits inside NON_NORMATIVE / IMPLEMENTATION /
DUPLICATE spans and summarize large non-normative spans, for adversarial manual review."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

KW = re.compile(r"\b(must|never|do not|don't|only|required?|requires|reserved|always|forbid\w*|prohibit\w*|"
                r"should|shall|blocked?|error|default|approval|approved|not allowed|mandatory)\b", re.I)


def main():
    root = Path(sys.argv[1]).resolve()
    cand = sys.argv[2]
    min_large = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    out = root / 'stage_A' / 'replica' / cand
    segs = [json.loads(l) for l in (out / 'coverage_ranges.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    cache = {}
    hits = 0
    large = []
    for s in segs:
        if s['disposition'] not in ('NON_NORMATIVE', 'IMPLEMENTATION', 'DUPLICATE'):
            continue
        p = s['path']
        if p not in cache:
            cache[p] = (root / 'inputs' / cand / p).read_bytes().decode('utf-8-sig').splitlines()
        lines = cache[p]
        n = s['end_line'] - s['start_line'] + 1
        if n >= min_large:
            large.append((n, p, s['start_line'], s['end_line'], s['disposition'], s['reason'][:110]))
        for i in range(s['start_line'], s['end_line'] + 1):
            t = lines[i - 1]
            if KW.search(t) and not t.strip().startswith(('```', '|---')):
                hits += 1
                print(f"{s['disposition'][:2]} {p.replace('output/template/', '')}:{i}: {t.strip()[:170]}")
    print(f'--- keyword hits in non-normative spans: {hits}')
    print(f'--- large non-normative spans (>= {min_large} lines): {len(large)}')
    for row in sorted(large, reverse=True):
        print('  %4d %s:%d-%d %s | %s' % row)
    print('--- disposition counts:', dict(Counter(s['disposition'] for s in segs)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
