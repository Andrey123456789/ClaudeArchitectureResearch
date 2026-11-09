#!/usr/bin/env python3
r"""One-command, non-destructive setup for Experiment 005 / Phase 5.4 Stage A.

Run from a clean 5.4 folder: py .\SETUP_5_4.py
Verify later:                 py .\SETUP_5_4.py --verify

Reads the sibling 5.3; NEVER modifies it. Copies active template and provenance
into immutable 5.4/inputs and creates source-hash-checked work queues.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import sys
import uuid

CANDIDATE_MAP = {
    'M': 'M', 'M1': 'M1', 'L0': 'L0',
    'L1': 'L1-Restart', 'K0': 'K0', 'K1': 'K1'
}
COPIED_PATHS = (
    'output/template',
    'source/inventory.json',
    'source/shared-research-invariants.json',
    'CANDIDATE.md',
    'REFINEMENT_TASK.md',
    'baseline/TASK.md',
    'output/REFINEMENT_REPORT.md',
)
M1_ARC025_SHA = 'c2040cf8f51e6ec0a00f8b23aabea3fc9fe891557636a1143029bd2992b4537c'
MANIFEST_NAME = 'INPUT_MANIFEST_SHA256.csv'
FIELDS = ['candidate', 'relative_path', 'sha256', 'size_bytes']


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for b in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def oracle_ids(directory: Path):
    src = directory / 'source'
    inv = json.loads((src / 'inventory.json').read_text(encoding='utf-8-sig'))
    shared = json.loads((src / 'shared-research-invariants.json').read_text(encoding='utf-8-sig'))
    ids = [p['id'] for g in inv['policygroups'] for p in g['policies']]
    others = [p['id'] for p in shared['invariants']]
    if len(ids) != 194 or len(others) != 2 or len(set(ids + others)) != 196:
        raise RuntimeError(f'Expected 194 + 2 unique policies in {directory}, got {len(ids)} + {len(others)}, unique={len(set(ids+others))}.')
    if set(others) != {'GOV-017', 'GOV-018'}:
        raise RuntimeError(f'Unexpected extra policy IDs: {others}')
    return ids + others


def validate_paths(root: Path):
    if root.name != '5.4':
        raise RuntimeError(f'Kit must be extracted directly into a directory named 5.4: {root}')
    kit = root / '_STAGE_A_KIT'
    essential = [
        '02_CLAUDE_STAGE_A_ALL_GOAL.txt',
        '02_CLAUDE_STAGE_A_PRIMARY_ALL_EN.md',
        '03_VALIDATE_STAGE_A.py',
        '04_CODEX_STAGE_A_BLIND_ALL_EN.md',
        '05_WORK_QUEUE_AND_PROGRESS.py',
        '06_CODEX_STAGE_A_RECONCILE_ALL_EN.md',
        '07_VALIDATE_ORPHANS.py',
    ]
    for name in essential:
        if not (kit / name).is_file():
            raise RuntimeError(f'Kit is incomplete: {kit / name}')
    return root.parent / '5.3', kit


def preflight(root: Path, source: Path):
    for item in ('inputs', 'stage_A', 'work'):
        if (root / item).exists():
            raise RuntimeError(f'{item}/ already exists. No overwrite. If already set up, run: py .\\SETUP_5_4.py --verify')
    if not source.is_dir():
        raise RuntimeError(f'Missing frozen 5.3 sibling folder: {source}')
    unexpected = [p.name for p in root.iterdir()
                  if p.name not in ('SETUP_5_4.py', 'START_HERE_RU.md', '_STAGE_A_KIT')
                  and not (p.is_file() and p.suffix.lower() == '.zip')]
    if unexpected:
        raise RuntimeError(f'5.4 is not empty apart from the kit: {unexpected}. Refusing to mix prior work.')
    for target, original in CANDIDATE_MAP.items():
        folder = source / original
        for rel in COPIED_PATHS:
            if not (folder / rel).exists():
                raise RuntimeError(f'Missing required {target} source: {folder / rel}')
        policies = oracle_ids(folder)
        print(f'PRECHECK: {target} <- 5.3/{original}: {len(policies)} policies')
        for path in (folder / 'output' / 'template').rglob('*'):
            if path.is_symlink():
                raise RuntimeError(f'Symlink inside input candidate (refusing ambiguous source): {path}')
    m1target = source / 'M1/output/template/.claude/rules/architecture.md'
    if digest(m1target) != M1_ARC025_SHA:
        raise RuntimeError('M1 ARC-025 architecture.md hash differs from independently verified after_codex_audit_1 result. No files copied.')
    print('PRECHECK: M1 corrected ARC-025 verified by SHA-256.')


def snapshot_rows(inputs: Path):
    rows = []
    for candidate in CANDIDATE_MAP:
        base = inputs / candidate
        for file in sorted((p for p in base.rglob('*') if p.is_file()), key=lambda p:p.as_posix()):
            rows.append({
                'candidate': candidate,
                'relative_path': file.relative_to(inputs).as_posix(),
                'sha256': digest(file),
                'size_bytes': str(file.stat().st_size),
            })
    return rows


def write_manifest(inputs: Path):
    rows = snapshot_rows(inputs)
    with (inputs / MANIFEST_NAME).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def verify(root: Path, source: Path, kit: Path, compare_source: bool = True):
    inputs = root / 'inputs'
    manifest = inputs / MANIFEST_NAME
    if not manifest.is_file():
        raise RuntimeError(f'No snapshot manifest found: {manifest}')
    with manifest.open('r', encoding='utf-8-sig', newline='') as f:
        entries = list(csv.DictReader(f))
    if not entries:
        raise RuntimeError('Empty snapshot manifest')
    declared = {}
    for r in entries:
        rel = r.get('relative_path', '')
        path = Path(rel)
        if not rel or path.is_absolute() or '..' in path.parts:
            raise RuntimeError(f'Unsafe manifest path: {rel}')
        candidate = r.get('candidate')
        if candidate not in CANDIDATE_MAP or path.parts[0] != candidate:
            raise RuntimeError(f'Invalid candidate/manifest path: {candidate} {rel}')
        if rel in declared:
            raise RuntimeError(f'Duplicate manifest entry: {rel}')
        declared[rel] = r
        file = inputs / path
        if not file.is_file():
            raise RuntimeError(f'Missing snapshotted file: {file}')
        if file.stat().st_size != int(r['size_bytes']) or digest(file) != r['sha256'].lower():
            raise RuntimeError(f'Changed snapshotted file: {file}')
    present = {p.relative_to(inputs).as_posix() for p in inputs.rglob('*') if p.is_file() and p.name != MANIFEST_NAME}
    if present != set(declared):
        raise RuntimeError(f'Snapshot files differ: unexpected={sorted(present-set(declared))[:10]} missing={sorted(set(declared)-present)[:10]}')
    for target, original in CANDIDATE_MAP.items():
        base = inputs / target
        oracle_ids(base)
        entries_target = [r for r in entries if r['candidate'] == target]
        for rel in COPIED_PATHS:
            if not (base / rel).exists():
                raise RuntimeError(f'Missing expected snapshotted path: {target}/{rel}')
        if compare_source:
            source_base = source / original
            for entry in entries_target:
                relative = Path(entry['relative_path']).relative_to(target)
                original_file = source_base / relative
                if not original_file.is_file() or digest(original_file) != entry['sha256']:
                    raise RuntimeError(f'Snapshot no longer matches frozen 5.3: {target}/{relative}')
        print(f'PASS: {target}: {len(entries_target)} hashed files, 196 policy IDs')
    # Check work queues are up-to-date and stable, no data writes.
    module = runpy.run_path(str(kit / '05_WORK_QUEUE_AND_PROGRESS.py'))
    for target in CANDIDATE_MAP:
        p = root / 'stage_A' / '_control' / f'{target}_WORK_QUEUE.json'
        if not p.is_file():
            raise RuntimeError(f'Missing work queue: {p}')
        existing = json.loads(p.read_text(encoding='utf-8'))
        regenerated = module['generate'](root, target, existing['max_batch_nonblank_lines'])
        if existing != regenerated:
            raise RuntimeError(f'Work queue mismatch: {target}')
        print(f'PASS: {target} queue: {len(existing["files"])} template files, {len(existing["batches"])} batches')
    print(f'VERIFICATION PASS: {len(entries)} files are unchanged; all six candidates covered.')


def setup(root: Path, source: Path, kit: Path):
    preflight(root, source)
    staging = root / ('_inputs_staging_' + uuid.uuid4().hex[:10])
    if staging.exists():
        raise RuntimeError(f'Temporary path collision: {staging}')
    created_inputs = False
    try:
        staging.mkdir()
        for target, original in CANDIDATE_MAP.items():
            src_base = source / original
            dst_base = staging / target
            for rel in COPIED_PATHS:
                src = src_base / rel
                dst = dst_base / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
        rows = write_manifest(staging)
        # Every file copied must match source, not just internal manifest.
        for row in rows:
            candidate = row['candidate']
            relative = Path(row['relative_path']).relative_to(candidate)
            source_file = source / CANDIDATE_MAP[candidate] / relative
            if digest(source_file) != row['sha256']:
                raise RuntimeError(f'Copy corruption: {source_file}')
        staging.rename(root / 'inputs')
        created_inputs = True
        for sub in ('primary', 'independent', 'reconciled', '_control'):
            (root / 'stage_A' / sub).mkdir(parents=True, exist_ok=True)
        (root / 'work').mkdir(exist_ok=True)
        module = runpy.run_path(str(kit / '05_WORK_QUEUE_AND_PROGRESS.py'))
        for target in CANDIDATE_MAP:
            plan = module['generate'](root, target, 500)
            qp = root / 'stage_A' / '_control' / f'{target}_WORK_QUEUE.json'
            qp.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
            (root / 'stage_A' / 'primary' / target).mkdir(parents=True, exist_ok=True)
            (root / 'stage_A' / 'independent' / target / 'blind').mkdir(parents=True, exist_ok=True)
            (root / 'stage_A' / 'reconciled' / target).mkdir(parents=True, exist_ok=True)
        verify(root, source, kit)
    except Exception:
        # Keep successfully created inputs/results instead of deleting anything.
        # A partially built state must be inspected/repaired, never overwritten.
        if staging.exists():
            shutil.rmtree(staging)
        if created_inputs:
            print('SETUP INCOMPLETE: 5.4/inputs exists; do NOT rerun setup until reviewing the reported error.', file=sys.stderr)
        raise
    print('\nSETUP COMPLETE. 5.3 remains untouched.')
    print('Claude: new Code session at 5.4, paste contents of _STAGE_A_KIT/02_CLAUDE_STAGE_A_ALL_GOAL.txt (NO /goal).')
    print('Codex: separate new session at 5.4, next morning use _STAGE_A_KIT/04_CODEX_STAGE_A_BLIND_ALL_EN.md.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='read-only verification after setup')
    parser.add_argument('--root', type=Path, help=argparse.SUPPRESS)
    a = parser.parse_args()
    root = (a.root if a.root else Path(__file__).resolve().parent).resolve()
    source, kit = validate_paths(root)
    if a.verify:
        verify(root, source, kit)
    else:
        setup(root, source, kit)

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
