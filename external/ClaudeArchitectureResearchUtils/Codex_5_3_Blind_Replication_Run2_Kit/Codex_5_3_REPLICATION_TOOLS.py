#!/usr/bin/env python3
"""Read-only verification and repeatability comparison for experiment 005 Phase 5.3.

Only the explicit --out file may be written. Standard-library Python 3.9+.
"""
import argparse
import csv
import hashlib
import pathlib
from collections import Counter

CANDIDATES = ('M', 'M1', 'L0', 'L1-Restart', 'K0', 'K1')
FIRST_AUDIT_DIGESTS = {
    'M': ('ffc13d60e0400bee0e0d9c39915730a4791ab04be76444d91f88604e0a23807a', 61),
    'M1': ('84e8ca7ad2f147a091dcd3e37ff4d7e5c6d6b23173d0d3521f6a97bf08d2ae44', 80),
    'L0': ('931a64d1f3fede560dc2f8995e1073068f7d715d622784846d18fc4ccdddd40d', 71),
    'L1-Restart': ('e3a4ea25da60caba094b028e477cc265cf334d7a605798294aba798cae4524f7', 86),
    'K0': ('d61218dd4657051cc63f3b0838e8f729ab77cb798712c992ee57d26d4f52a4d1', 63),
    'K1': ('d2f3d1ddf8e3e06269e233339463edc07d8072476b601e8a9acfa09091cd0383', 87),
}
STATUS_COLS = ['M_status', 'M1_status', 'L0_status', 'L1_Restart_status', 'K0_status', 'K1_status']
MATRIX_NAME = '03_REQUIREMENT_PARITY_MATRIX.csv'


def digest_tree(template):
    if not template.is_dir():
        return None, 0
    entries = []
    for p in template.rglob('*'):
        if p.is_symlink():
            raise RuntimeError(f'Symlink found (not following): {p}')
        if not p.is_file():
            continue
        rel = p.relative_to(template).as_posix()
        entries.append((rel, hashlib.sha256(p.read_bytes()).hexdigest()))
    entries.sort(key=lambda v: v[0])
    raw = '\n'.join(f'{digest}  {name}' for name, digest in entries).encode('utf-8')
    return hashlib.sha256(raw).hexdigest(), len(entries)


def verify(root):
    print(f'Research workspace: {root}')
    ok = True
    for candidate in CANDIDATES:
        actual, count = digest_tree(root / candidate / 'output' / 'template')
        expected, n = FIRST_AUDIT_DIGESTS[candidate]
        match = actual == expected and count == n
        ok = ok and match
        print(f'{candidate:11} {"MATCH" if match else "MISMATCH":9} '
              f'files={count}/{n}  actual={actual or "ABSENT"}  expected={expected}')
    print('INPUTS IDENTICAL TO RUN 1' if ok else 'INPUTS DIFFER: DO NOT CALL THIS AN IDENTICAL REPLICATION')
    return ok


def load_matrix(directory):
    file = directory / MATRIX_NAME
    with file.open('r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        required = {'policy_id', 'parity_class', *STATUS_COLS}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'{file}: missing CSV fields: {missing}')
        rows = {}
        for row in reader:
            key = row['policy_id'].strip()
            if key in rows:
                raise ValueError(f'{file}: duplicate policy ID {key}')
            rows[key] = row
        return rows


def compare(root, first, second):
    a = load_matrix(first)
    b = load_matrix(second)
    shared = sorted(a.keys() & b.keys())
    only_a = sorted(a.keys() - b.keys())
    only_b = sorted(b.keys() - a.keys())
    identical_inputs = all(
        digest_tree(root / c / 'output' / 'template') == FIRST_AUDIT_DIGESTS[c]
        for c in CANDIDATES
    )
    status_diffs = []
    class_diffs = []
    other_diffs = []
    per_status_a = Counter()
    per_status_b = Counter()
    for key in shared:
        ra, rb = a[key], b[key]
        for field in STATUS_COLS:
            sa, sb = ra[field].strip().upper(), rb[field].strip().upper()
            per_status_a[sa] += 1
            per_status_b[sb] += 1
            if sa != sb:
                status_diffs.append((key, field.replace('_status', ''), sa, sb))
        ca, cb = ra['parity_class'].strip().upper(), rb['parity_class'].strip().upper()
        if ca != cb:
            class_diffs.append((key, ca, cb))
        for meta in ('group', 'normative_strength', 'trigger_class', 'scope', 'canonical_summary'):
            if (ra.get(meta) or '').strip() != (rb.get(meta) or '').strip():
                other_diffs.append((key, meta))
    examined = len(shared) * 6
    pct = (examined - len(status_diffs)) / examined * 100 if examined else 0.0
    special = ('ARC-025', 'WF-007', 'WF-019', 'DEP-003')
    lines = [
        '# Experiment 005 / Phase 5.3 — Run 1 vs Run 2 comparison',
        '',
        '**Caution:** This is a mechanical CSV comparison, not a third semantic audit.',
        '',
        f'- Input templates identical to the first audit: **{"YES" if identical_inputs else "NO — COMPARISON NOT CONTROLLED"}**.',
        f'- Unique policy IDs: Run 1 **{len(a)}**, Run 2 **{len(b)}**, common **{len(shared)}**.',
        f'- Missing in Run 2: {", ".join(only_a) or "none"}.',
        f'- New in Run 2: {", ".join(only_b) or "none"}.',
        f'- Six-way statuses compared: **{examined}**, exact match **{examined-len(status_diffs)}**, changed **{len(status_diffs)}**.',
        f'- Raw status agreement on shared IDs: **{pct:.2f}%**.',
        f'- Run 1 status distribution: `{dict(per_status_a)}`.',
        f'- Run 2 status distribution: `{dict(per_status_b)}`.',
        f'- Changed parity_class rows: **{len(class_diffs)}**.',
        f'- Changed canonical policy metadata cells: **{len(other_diffs)}**.',
        '',
        '**Interpretation warning:** With mostly SAME values, global agreement may be near 100% even when important rare findings change. Check individual exceptional policies and report text manually.',
        '',
        '## All candidate status differences',
        '',
        '| Policy ID | Candidate | Run 1 | Run 2 |',
        '|---|---|---|---|',
    ]
    lines += [f'| {policy} | {candidate} | {sa} | {sb} |' for policy, candidate, sa, sb in status_diffs] or ['| — | — | — | — |']
    lines += ['', '## All parity-class differences', '', '| Policy ID | Run 1 | Run 2 |', '|---|---|---|']
    lines += [f'| {policy} | {ca} | {cb} |' for policy, ca, cb in class_diffs] or ['| — | — | — |']
    lines += ['', '## Predefined high-priority topics', '']
    for policy in special:
        lines.append(f'### {policy}')
        if policy not in a or policy not in b:
            lines.append('- Policy is absent from one run; investigate.')
            continue
        lines.append(f'- Parity class: `{a[policy]["parity_class"]}` → `{b[policy]["parity_class"]}`')
        for field in STATUS_COLS:
            candidate = field.replace('_status', '')
            lines.append(f'- {candidate}: `{a[policy][field]}` → `{b[policy][field]}`')
        lines.append('')
    if other_diffs:
        lines += ['## Canonical metadata differences', ''] + [f'- `{p}`: `{col}`' for p, col in other_diffs]
    lines += [
        '', '## Manual comparison still required', '',
        '- Six freeze verdicts and any additional blocker IDs (reports 00 and 01).',
        '- Full backlog findings beyond matrix labels, severity, affected candidates, proof and counterevidence (report 02).',
        '- RCH-001/002/003 observations and whether additional reachability risks appeared.',
        '- Whether candidate contexts/hooks produced different coverage and audit limitations (report 04).',
        '- Treat disagreements as hypotheses requiring adjudication; do not automatically declare either audit correct.',
    ]
    return '\n'.join(lines) + '\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('verify', help='Check current six candidate templates against Run 1 tree digests')
    v.add_argument('--root', type=pathlib.Path, required=True)
    c = sub.add_parser('compare', help='Compare the 196-row matrices and verify source inputs')
    c.add_argument('--root', type=pathlib.Path, required=True)
    c.add_argument('--run1', type=pathlib.Path, required=True)
    c.add_argument('--run2', type=pathlib.Path, required=True)
    c.add_argument('--out', type=pathlib.Path, required=True)
    a = p.parse_args()
    if a.cmd == 'verify':
        raise SystemExit(0 if verify(a.root) else 2)
    report = compare(a.root, a.run1, a.run2)
    if a.out.exists():
        raise FileExistsError(f'Refusing to overwrite existing comparison: {a.out}')
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(report, encoding='utf-8')
    print(report[:3200])
    print(f'\nFull report: {a.out}')


if __name__ == '__main__':
    main()
