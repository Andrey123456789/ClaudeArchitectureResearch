"""Reproduces v1's extension scan (v1 _scratch/scan2.py) so the 21 `do not X when Y` leads are a defined, replayable set. Reads the frozen baseline and frozen inputs only.

Scan: knowledge-only records outside the 79 and 230 lists, stored MUST or MUST_NOT; the evidence sentence closest to the claim is matched against three forms, first match wins.
v1 reported 22, 8 and 21. A sentence this heuristic does not pick is missed, so the counts are a bound, not a census.
"""
import re
import sys

from pi012 import R
from rcommon import CANDIDATES, baseline, input_path, norm_ws, out_path, read_json, read_lines, utf8_stdout

KN = set('httpclient-factory http-api ef-core swagger caching authentication api-versioning dependency-injection logging angular health-check docker aspnet-error-handling configuration dotnet-testing modern-csharp ci-cd'.split())
FORMS = {'do_not_unless': re.compile(r"\b(do not|don't)\b[^.;]{0,120}\b(unless|without)\b", re.I), 'only_when': re.compile(r"\bonly (when|if)\b|\bcreated only\b|\badded only\b", re.I), 'do_not_when': re.compile(r"\b(do not|don't)\b[^.;]{0,120}\b(when|if)\b", re.I)}


def knowledge(path):
    m = re.search(r'\.claude/skills/([^/]+)/(.*)', path)
    return bool(m and (m.group(1) in KN or m.group(2).startswith('references/')))


def scan():
    cases = {c['key'].split('/')[0] for c in read_json(out_path(R, 'CASES.json'))['cases']}
    out = {f: [] for f in FORMS}
    for c in CANDIDATES:
        for k, r in baseline(c).items():
            if k in cases or r.get('modality') not in ('MUST_NOT', 'MUST'):
                continue
            refs = r.get('evidence_refs') or []
            if not refs or not all(knowledge(e['path']) for e in refs):
                continue
            claim = set(re.findall(r'\w+', (r.get('claim_text') or '').lower()))
            best, bj = None, 0
            for e in refs:
                ls = read_lines(input_path(c, e['path'].split('/template/')[1]))
                t = norm_ws(' '.join(ls[e['start_line'] - 1:e['end_line']]))
                for s in re.split(r'(?<=[.;])\s+', t):
                    w = set(re.findall(r'\w+', s.lower()))
                    j = len(w & claim) / max(1, len(w | claim))
                    if j > bj:
                        bj, best = j, s
            if not best:
                continue
            for f, rx in FORMS.items():
                if rx.search(best):
                    out[f].append({'candidate': c, 'key': k, 'modality': r['modality'], 'classification': r['classification'], 'sentence': best, 'path': refs[0]['path'].split('/template/')[1], 'start_line': refs[0]['start_line'], 'end_line': refs[0]['end_line']})
                    break
    return out


if __name__ == '__main__':
    utf8_stdout()
    res = scan()
    print({f: len(v) for f, v in res.items()})
    if len(sys.argv) > 1:
        for x in res[sys.argv[1]]:
            print(x['candidate'], x['key'], x['modality'], x['classification'][:8], x['path'].split('.claude/')[-1], x['start_line'])
            print('    ', x['sentence'][:300])
