#!/usr/bin/env python3
"""Run-2 replica report generator: writes EXTRA_CONSTRAINTS.md, ORPHAN_SWEEP_REPORT.md and
EXTRACTION_REPORT.md for one candidate from its ledgers plus hand-written _annotations/NOTES.md
(sections '## Sweep notes' and '## Limitations') and optional _annotations/_validation.txt."""
import json
import sys
from collections import Counter
from pathlib import Path

TP = 'output/template/'


def jl(p):
    return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()] if p.is_file() else []


def section(text, title):
    if f'## {title}' not in text:
        return ''
    part = text.split(f'## {title}', 1)[1]
    nxt = part.find('\n## ')
    return (part if nxt < 0 else part[:nxt]).strip()


def q(text, limit=700):
    t = text.replace('\r', '')
    if len(t) > limit:
        t = t[:limit] + ' […truncated in this report; the exact full quote is in coverage_ranges.jsonl]'
    return t.replace('\n', ' ⏎ ')


def main():
    root = Path(sys.argv[1]).resolve()
    cand = sys.argv[2]
    out = root / 'stage_A' / 'replica' / cand
    ann = out / '_annotations'
    queue = json.loads((root / 'stage_A' / '_control' / f'{cand}_WORK_QUEUE.json').read_text(encoding='utf-8'))
    files = jl(out / 'files.jsonl')
    segs = jl(out / 'coverage_ranges.jsonl')
    cons = jl(out / 'constraints.jsonl')
    pols = jl(out / 'policies.jsonl')
    orph = jl(out / 'ORPHAN_CANDIDATES.jsonl')
    notes = (ann / 'NOTES.md').read_text(encoding='utf-8') if (ann / 'NOTES.md').is_file() else ''
    val = (ann / '_validation.txt').read_text(encoding='utf-8') if (ann / '_validation.txt').is_file() else 'Validators not yet run when this report was generated.'
    seg_by = {s['segment_id']: s for s in segs}
    con_by = {c['id']: c for c in cons}
    prog = json.loads((out / 'PROGRESS.json').read_text(encoding='utf-8'))

    # ---------------- EXTRA_CONSTRAINTS.md
    L = [f'# {cand} — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)', '',
         'Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies '
         '(EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative '
         f'paths under `inputs/{cand}/output/template/` with exact source quotes (newlines shown as ⏎).', '']
    for origin in ('EXTRA', 'LINK_UNCERTAIN'):
        rows = [c for c in cons if c['origin'] == origin]
        L.append(f'## {origin} ({len(rows)})')
        L.append('')
        for c in rows:
            L.append(f'### {c["id"]}')
            L.append(f'- Closest oracle policies: {", ".join(c["policy_ids"]) or "none"}')
            L.append(f'- Modality: {c["modality"]}')
            L.append(f'- Normative action: {c["normative_action"]}')
            L.append(f'- Trigger/scope: {c["trigger_scope"]}')
            L.append(f'- Exceptions: {c["exceptions"]}')
            L.append(f'- {"Why EXTRA" if origin == "EXTRA" else "Open question"}: {c["why_extra_or_uncertain"]}')
            L.append('- Evidence:')
            for sid in c['evidence_segment_ids']:
                s = seg_by[sid]
                L.append(f'  - `{s["path"].replace(TP, "")}:{s["start_line"]}-{s["end_line"]}` ({s["disposition"]}, {sid}): "{q(s.get("quote", ""))}"')
            L.append('')
    (out / 'EXTRA_CONSTRAINTS.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

    # ---------------- ORPHAN_SWEEP_REPORT.md
    rc = Counter(o['resolution'] for o in orph)
    unresolved = [o for o in orph if o['resolution'] == 'LINK_UNCERTAIN']
    L = [f'# {cand} — Orphan sweep report (Claude Run 2, blind replica)', '',
         '## Counts', '',
         f'- Orphan candidates identified: {len(orph)}',
         f'- EXTRA registered: {rc.get("EXTRA_REGISTERED", 0)} (EXTRA constraints in constraints.jsonl: {sum(c["origin"] == "EXTRA" for c in cons)})',
         f'- Mapped to oracle (POLICY_LINKED): {rc.get("POLICY_LINKED", 0)}',
         f'- Non-normative / rejected: {rc.get("NON_NORMATIVE", 0)}',
         f'- Duplicates: {rc.get("DUPLICATE", 0)}',
         f'- Unresolved (LINK_UNCERTAIN): {rc.get("LINK_UNCERTAIN", 0)}', '',
         '## Unresolved items (LINK_UNCERTAIN)', '']
    if not unresolved:
        L.append('None.')
    for o in unresolved:
        cid = o['constraint_ids'][0] if o['constraint_ids'] else ''
        L.append(f'- **{o["id"]}** -> {", ".join(o["constraint_ids"])} at `{o["path"].replace(TP, "")}:{o["start_line"]}-{o["end_line"]}`: "{q(o["quote"], 300)}"')
        L.append(f'  - Question: {con_by[cid]["why_extra_or_uncertain"] if cid in con_by else o["reason"]}')
        L.append(f'  - Ledger reason: {o["reason"]}')
    L += ['', '## Reverse checks conducted', '', section(notes, 'Sweep notes') or '(none recorded)', '',
          '## Full orphan ledger', '', '| ID | Resolution | Location | Constraints | Closest policies | Reason |', '|---|---|---|---|---|---|']
    for o in orph:
        reason = o['reason'].replace('|', '/').replace('\n', ' ')
        L.append(f'| {o["id"]} | {o["resolution"]} | `{o["path"].replace(TP, "")}:{o["start_line"]}-{o["end_line"]}` | '
                 f'{", ".join(o["constraint_ids"]) or "—"} | {", ".join(o["closest_policy_ids"]) or "—"} | {reason[:260]} |')
    L += ['', 'A completed line disposition plus this sweep is not proof of semantic exhaustiveness.']
    (out / 'ORPHAN_SWEEP_REPORT.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

    # ---------------- EXTRACTION_REPORT.md
    qf = queue['files']
    text_files = sum(f['type'] == 'text' for f in qf)
    nonblank = sum(f['nonblank_lines'] for f in qf)
    st = Counter(p['status'] for p in pols)
    oc = Counter(c['origin'] for c in cons)
    dc = Counter(s['disposition'] for s in segs)
    L = [f'# {cand} — Extraction report (Claude Run 2, blind replica)', '',
         '## Scope and method', '',
         f'- Snapshot: `inputs/{cand}/output/template/` ({len(qf)} files, {text_files} UTF-8 text, {len(qf) - text_files} binary/non-UTF-8, {nonblank} nonblank lines); '
         f'queue `stage_A/_control/{cand}_WORK_QUEUE.json` ({len(queue["batches"])} batches) used read-only.',
         f'- Oracle: `inputs/{cand}/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.',
         '- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` '
         '(exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.',
         '- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. '
         'CANDIDATE.md was read for provenance only.', '',
         '## Counts', '',
         f'- Files inventoried: {len(files)}; completed batches: {len(prog["completed_batch_ids"])}/{len(queue["batches"])}',
         f'- Coverage segments: {len(segs)} — ' + ', '.join(f'{k} {v}' for k, v in sorted(dc.items())),
         f'- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)',
         f'- Policies: {len(pols)} — ' + ', '.join(f'{k} {st.get(k, 0)}' for k in ('MATCHED', 'PARTIAL', 'NOT_EVIDENCED', 'UNCERTAIN')),
         f'- Constraints: {len(cons)} — ORACLE_LINKED {oc.get("ORACLE_LINKED", 0)}, EXTRA {oc.get("EXTRA", 0)}, LINK_UNCERTAIN {oc.get("LINK_UNCERTAIN", 0)}',
         f'- Orphan ledger: {len(orph)} rows — ' + ', '.join(f'{k} {v}' for k, v in sorted(Counter(o["resolution"] for o in orph).items())), '',
         '## Policy status detail', '']
    for k in ('PARTIAL', 'NOT_EVIDENCED', 'UNCERTAIN'):
        ids = [p['rule_id'] for p in pols if p['status'] == k]
        L.append(f'- {k}: {", ".join(ids) if ids else "none"}')
    L += ['', '## EXTRA constraints (summary)', '']
    for c in cons:
        if c['origin'] != 'LINK_UNCERTAIN' and c['origin'] != 'EXTRA':
            continue
        L.append(f'- {c["id"]} ({c["origin"]}; closest {", ".join(c["policy_ids"]) or "none"}): {c["normative_action"][:240]}')
    L += ['', '## Unsupported file types', '',
          'None: all template files are UTF-8 text.' if text_files == len(qf) else 'See files.jsonl rows of type binary (not decoded, no line coverage).',
          '', '## Check results', '', '```', val.strip(), '```', '',
          '## Limitations', '', section(notes, 'Limitations') or '(none recorded)', '']
    (out / 'EXTRACTION_REPORT.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('reports written for', cand)


if __name__ == '__main__':
    main()
