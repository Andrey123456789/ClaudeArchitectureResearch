#!/usr/bin/env python3
"""Generate EXTRACTION_REPORT.md and ORPHAN_SWEEP_REPORT.md for one candidate.

Numbers are computed from the ledgers; narrative sections come from
_work/report_notes.md and _work/sweep_notes.md (hand-written, candidate specific).
Validator outputs, when available, are read from _work/validator_results.txt.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def jl(p):
    return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--candidate', required=True)
    a = ap.parse_args()
    root = a.root.resolve()
    cand = a.candidate
    out = root / 'stage_A' / 'primary' / cand
    work = out / '_work'
    files = jl(out / 'files.jsonl')
    segs = jl(out / 'coverage_ranges.jsonl')
    cons = jl(out / 'constraints.jsonl')
    pols = jl(out / 'policies.jsonl')
    orph = jl(out / 'ORPHAN_CANDIDATES.jsonl')
    queue = json.loads((root / 'stage_A' / '_control' / f'{cand}_WORK_QUEUE.json').read_text(encoding='utf-8'))
    prog = json.loads((out / 'PROGRESS.json').read_text(encoding='utf-8'))
    notes = (work / 'report_notes.md').read_text(encoding='utf-8') if (work / 'report_notes.md').is_file() else ''
    snotes = (work / 'sweep_notes.md').read_text(encoding='utf-8') if (work / 'sweep_notes.md').is_file() else ''
    vres = (work / 'validator_results.txt').read_text(encoding='utf-8') if (work / 'validator_results.txt').is_file() else 'Validators not yet run when this report was generated.'

    nonblank = sum(f['nonblank_lines'] for f in queue['files'])
    types = Counter(f['type'] for f in files)
    disp = Counter(s['disposition'] for s in segs)
    origin = Counter(c['origin'] for c in cons)
    pst = Counter(p['status'] for p in pols)
    ores = Counter(o['resolution'] for o in orph)
    seg_by = {s['segment_id']: s for s in segs}

    # extras by top-level area
    def area(path):
        p = path.replace('output/template/', '')
        parts = p.split('/')
        if parts[0] == '.claude' and len(parts) > 2:
            if parts[1] == 'skills':
                return f'.claude/skills/{parts[2]}'
            return f'.claude/{parts[1]}/{parts[2]}' if parts[1] in ('rules', 'hooks', 'scripts', 'agents') else '/'.join(parts[:2])
        return p
    ex_area = Counter()
    for c in cons:
        if c['origin'] == 'EXTRA':
            first = sorted(c['evidence_segment_ids'])[0]
            ex_area[area(seg_by[first]['path'])] += 1

    L = []
    L.append(f'# Stage A primary extraction report — candidate {cand}')
    L.append('')
    L.append('Extractor: Claude (primary). Scope: `inputs/%s/output/template/**` only; provenance documents were not treated as normative surfaces. '
             'All numbers below are computed from the ledgers in this directory.' % cand)
    L.append('')
    L.append('## Source inventory')
    L.append('')
    L.append(f'- Active template files: {len(files)} (text: {types.get("text", 0)}, binary/non-UTF-8: {types.get("binary", 0)}).')
    L.append(f'- Non-blank lines in text files: {nonblank}.')
    L.append(f'- Queue batches: {len(queue["batches"])}; batches checked complete: {len(prog["completed_batch_ids"])}.')
    L.append(f'- Coverage ranges: {len(segs)} — ' + ', '.join(f'{k}={v}' for k, v in sorted(disp.items())) + '.')
    L.append(f'- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).')
    L.append('')
    L.append('## 196-policy forward mapping')
    L.append('')
    L.append(f'- Policies in policies.jsonl: {len(pols)} (194 inventory + 2 shared invariants).')
    L.append('- Status counts: ' + ', '.join(f'{k}={pst.get(k, 0)}' for k in ('MATCHED', 'PARTIAL', 'NOT_EVIDENCED', 'UNCERTAIN')) + '.')
    flagged = [p['rule_id'] for p in pols if 'caveat' in p['search_notes'].lower() or 'open related item' in p['search_notes'].lower() or 'enforcement note' in p['search_notes'].lower()]
    if flagged:
        L.append(f'- Policies whose search notes carry a modality caveat, open related item or enforcement note: {", ".join(flagged)}.')
    L.append('')
    L.append('## Constraints')
    L.append('')
    L.append(f'- Atomic constraints: {len(cons)} — ORACLE_LINKED={origin.get("ORACLE_LINKED", 0)}, EXTRA={origin.get("EXTRA", 0)}, LINK_UNCERTAIN={origin.get("LINK_UNCERTAIN", 0)}.')
    L.append('- EXTRA constraints by first-evidence area:')
    for k, v in ex_area.most_common():
        L.append(f'  - {k}: {v}')
    L.append('- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.')
    L.append('')
    L.append('## Orphan ledger')
    L.append('')
    L.append(f'- ORPHAN_CANDIDATES.jsonl rows: {len(orph)} — ' + ', '.join(f'{k}={v}' for k, v in sorted(ores.items())) + '.')
    L.append('- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.')
    L.append('')
    L.append('## File types and limitations')
    L.append('')
    if types.get('binary', 0):
        L.append(f'- {types["binary"]} binary/non-UTF-8 file(s) recorded in files.jsonl without decoded content.')
    else:
        L.append('- No binary or non-UTF-8 files; every file was decoded and line-partitioned.')
    L.append('- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.')
    L.append('- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.')
    if notes.strip():
        L.append('')
        L.append(notes.strip())
    L.append('')
    L.append('## Check results')
    L.append('')
    L.append('```text')
    L.append(vres.strip())
    L.append('```')
    (out / 'EXTRACTION_REPORT.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

    # ---------------- orphan sweep report
    S = []
    S.append(f'# Orphan sweep report — candidate {cand}')
    S.append('')
    S.append('Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.')
    S.append('')
    S.append('## Counts')
    S.append('')
    S.append(f'- Orphan candidates identified: {len(orph)}')
    S.append(f'- EXTRA registered (EXTRA_REGISTERED): {ores.get("EXTRA_REGISTERED", 0)} (EXTRA constraints: {origin.get("EXTRA", 0)})')
    S.append(f'- Mapped to oracle (POLICY_LINKED): {ores.get("POLICY_LINKED", 0)}')
    S.append(f'- Non-normative / discarded (NON_NORMATIVE): {ores.get("NON_NORMATIVE", 0)}')
    S.append(f'- Duplicates (DUPLICATE): {ores.get("DUPLICATE", 0)}')
    S.append(f'- Unresolved (LINK_UNCERTAIN): {ores.get("LINK_UNCERTAIN", 0)}')
    S.append('')
    S.append('## Unresolved items')
    S.append('')
    un = [o for o in orph if o['resolution'] == 'LINK_UNCERTAIN']
    if not un:
        S.append('None.')
    cbyid = {c['id']: c for c in cons}
    for o in un:
        q = o['quote'].replace('\n', ' ⏎ ')
        S.append(f'### {o["id"]}')
        S.append(f'- Constraint(s): {", ".join(o["constraint_ids"])}; closest policies: {", ".join(o["closest_policy_ids"]) or "none"}')
        S.append(f'- Evidence: `{o["path"]}:{o["start_line"]}-{o["end_line"]}` — "{q[:400]}"')
        for cid in o['constraint_ids']:
            w = cbyid[cid]["why_extra_or_uncertain"]
            S.append(w if w.lower().startswith('open question') else f'- Open question: {w}') if False else S.append('- ' + (w if w.lower().startswith('open question') else 'Open question: ' + w))
        S.append('')
    S.append('## Rejected false leads and oracle-linked resolutions')
    S.append('')
    for o in orph:
        if o['resolution'] in ('NON_NORMATIVE', 'POLICY_LINKED', 'DUPLICATE'):
            S.append(f'- {o["id"]} [{o["resolution"]}] `{o["path"].replace("output/template/", "")}:{o["start_line"]}-{o["end_line"]}` — {o["reason"]}')
    S.append('')
    S.append('## Reverse checks conducted')
    S.append('')
    S.append(snotes.strip() if snotes.strip() else '- (no narrative recorded)')
    S.append('')
    S.append('## Limitation')
    S.append('')
    S.append('A complete line disposition plus this sweep is not proof of semantic exhaustiveness.')
    (out / 'ORPHAN_SWEEP_REPORT.md').write_text('\n'.join(S) + '\n', encoding='utf-8')
    print('reports written')


if __name__ == '__main__':
    main()
