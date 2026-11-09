#!/usr/bin/env python3
"""Read-only structural check for experiment 005/5.4 Stage A extraction.

Checks SHA-256 of input snapshot, 196-policy coverage, file coverage,
nonblank-line assignment, evidence references, and unassigned normative spans.
It does NOT prove semantic completeness or rule classification correctness.
"""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

CANDIDATES = ('M', 'M1', 'L0', 'L1', 'K0', 'K1')
NORMATIVE = {'ORACLE_LINKED', 'EXTRA', 'LINK_UNCERTAIN'}
DISPOSITIONS = NORMATIVE | {'MIXED'} | {'NON_NORMATIVE', 'IMPLEMENTATION', 'DUPLICATE'}
STATUS = {'MATCHED', 'PARTIAL', 'NOT_EVIDENCED', 'UNCERTAIN'}


def jlines(p, errors):
    if not p.is_file():
        errors.append(f'MISSING OUTPUT: {p}')
        return []
    out = []
    for n, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError('expected object')
            out.append(obj)
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f'INVALID JSONL: {p.name}:{n}: {exc}')
    return out


def oracle_ids(root, candidate):
    c = root / 'inputs' / candidate / 'source'
    inv = json.loads((c / 'inventory.json').read_text(encoding='utf-8-sig'))
    shared = json.loads((c / 'shared-research-invariants.json').read_text(encoding='utf-8-sig'))
    ids = [p['id'] for g in inv['policygroups'] for p in g['policies']]
    ids.extend(i['id'] for i in shared['invariants'])
    return ids


def verify_snapshot(root, candidate, errors):
    manifest = root / 'inputs' / 'INPUT_MANIFEST_SHA256.csv'
    if not manifest.is_file():
        errors.append(f'MISSING INPUT MANIFEST: {manifest}')
        return
    with manifest.open(encoding='utf-8-sig', newline='') as fp:
        entries = [r for r in csv.DictReader(fp) if r['candidate'] == candidate]
    intended = set()
    for r in entries:
        f = root / 'inputs' / Path(r['relative_path'])
        intended.add(f.resolve())
        if not f.is_file():
            errors.append(f'SNAPSHOT MISSING: {r["relative_path"]}')
        elif hashlib.sha256(f.read_bytes()).hexdigest() != r['sha256'].lower():
            errors.append(f'SNAPSHOT MODIFIED: {r["relative_path"]}')
    actual = {p.resolve() for p in (root / 'inputs' / candidate).rglob('*') if p.is_file()}
    for p in sorted(actual - intended):
        errors.append(f'SNAPSHOT EXTRA FILE: {p}')
    if not entries:
        errors.append(f'MISSING SNAPSHOT MANIFEST ENTRIES: {candidate}')


def validate(root, candidate):
    errors = []
    verify_snapshot(root, candidate, errors)
    try:
        ids = oracle_ids(root, candidate)
        expected = set(ids)
        if len(ids) != 196 or len(expected) != 196:
            errors.append(f'ORACLE POLICY ID COUNT: {len(ids)} / {len(expected)} unique, expected 196')
    except (OSError, KeyError, ValueError) as exc:
        errors.append(f'ORACLE UNAVAILABLE: {exc}')
        expected = set()

    output = root / 'stage_A' / 'replica' / candidate
    file_rows = jlines(output / 'files.jsonl', errors)
    policy_rows = jlines(output / 'policies.jsonl', errors)
    constraints = jlines(output / 'constraints.jsonl', errors)
    spans = jlines(output / 'coverage_ranges.jsonl', errors)
    for name in ('EXTRA_CONSTRAINTS.md', 'EXTRACTION_REPORT.md'):
        if not (output / name).is_file():
            errors.append(f'MISSING OUTPUT: {output / name}')

    tmpl = root / 'inputs' / candidate / 'output' / 'template'
    source_files = {p.relative_to(root / 'inputs' / candidate).as_posix(): p for p in tmpl.rglob('*') if p.is_file()}
    file_by_path = {}
    for row in file_rows:
        p = row.get('path')
        if not p or p in file_by_path:
            errors.append(f'FILE INVENTORY DUPLICATE OR MISSING PATH: {p}')
        file_by_path[p] = row
    for p in source_files.keys() - file_by_path.keys():
        errors.append(f'UNINVENTORIED SOURCE FILE: {p}')
    for p in file_by_path.keys() - source_files.keys():
        errors.append(f'INVENTORY REFERS TO ABSENT FILE: {p}')

    text_by_path = {}
    for p, src in source_files.items():
        try:
            blob = src.read_bytes()
            if b'\x00' in blob:
                raise UnicodeError('contains binary NUL')
            lines = blob.decode('utf-8-sig').splitlines()
            text_by_path[p] = lines
            if file_by_path.get(p, {}).get('type') != 'text':
                errors.append(f'UTF8 TEXT NOT MARKED text: {p}')
        except (UnicodeError, UnicodeDecodeError):
            if file_by_path.get(p, {}).get('type') != 'binary':
                errors.append(f'NON-UTF8/BINARY FILE NOT MARKED binary: {p}')

    p_by_id = {}
    for row in policy_rows:
        pid = row.get('rule_id')
        if not pid or pid in p_by_id:
            errors.append(f'POLICY DUPLICATE OR NO ID: {pid}')
        p_by_id[pid] = row
        if row.get('status') not in STATUS:
            errors.append(f'BAD POLICY STATUS: {pid} {row.get("status")}')
        if not isinstance(row.get('atomic_constraint_ids'), list):
            errors.append(f'MISSING POLICY ATOMIC IDS: {pid}')
        if not isinstance(row.get('evidence_segment_ids'), list):
            errors.append(f'MISSING POLICY EVIDENCE IDS: {pid}')
        if not str(row.get('search_notes', '')).strip():
            errors.append(f'MISSING SEARCH NOTES: {pid}')
    for pid in expected - p_by_id.keys():
        errors.append(f'POLICY NOT COVERED: {pid}')
    for pid in p_by_id.keys() - expected:
        errors.append(f'UNKNOWN POLICY: {pid}')

    c_by_id = {}
    for row in constraints:
        cid = row.get('id')
        if not cid or cid in c_by_id:
            errors.append(f'CONSTRAINT DUPLICATE OR NO ID: {cid}')
        c_by_id[cid] = row
        if row.get('origin') not in NORMATIVE:
            errors.append(f'INVALID CONSTRAINT ORIGIN: {cid}')
        if not isinstance(row.get('policy_ids'), list) or not isinstance(row.get('evidence_segment_ids'), list):
            errors.append(f'INVALID CONSTRAINT LINKS: {cid}')
        else:
            for pid in row['policy_ids']:
                if pid not in expected:
                    errors.append(f'CONSTRAINT UNKNOWN POLICY: {cid} -> {pid}')
        if not str(row.get('normative_action', '')).strip():
            errors.append(f'CONSTRAINT EMPTY ACTION: {cid}')
        if not row.get('evidence_segment_ids'):
            errors.append(f'CONSTRAINT MISSING EVIDENCE: {cid}')
        if row.get('origin') == 'ORACLE_LINKED' and not row.get('policy_ids'):
            errors.append(f'ORACLE-LINKED CONSTRAINT WITH NO ORACLE POLICY: {cid}')
        if row.get('origin') == 'EXTRA':
            if not str(cid).startswith(f'EXTRA-{candidate}-'):
                errors.append(f'EXTRA ID NAMING: {cid}')
            if not str(row.get('why_extra_or_uncertain', '')).strip():
                errors.append(f'EXTRA MISSING JUSTIFICATION: {cid}')
        if row.get('origin') == 'LINK_UNCERTAIN' and not str(row.get('why_extra_or_uncertain', '')).strip():
            errors.append(f'UNCERTAIN CONSTRAINT MISSING QUESTION: {cid}')

    s_by_id, intervals = {}, {}
    for row in spans:
        sid, p = row.get('segment_id'), row.get('path')
        if not sid or sid in s_by_id:
            errors.append(f'SEGMENT DUPLICATE OR NO ID: {sid}')
        s_by_id[sid] = row
        disp = row.get('disposition')
        if disp not in DISPOSITIONS:
            errors.append(f'INVALID SEGMENT DISPOSITION: {sid} {disp}')
        if p not in text_by_path:
            errors.append(f'SEGMENT MISSING/NONTEXT FILE: {sid} -> {p}')
            continue
        try:
            a, b = int(row['start_line']), int(row['end_line'])
            if a < 1 or b < a or b > len(text_by_path[p]):
                raise ValueError('out of source bounds')
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f'INVALID LINE RANGE: {sid} -> {exc}')
            continue
        intervals.setdefault(p, []).append((a, b, sid))
        if disp in NORMATIVE | {'MIXED'}:
            cids = row.get('constraint_ids')
            if not isinstance(cids, list) or not cids:
                errors.append(f'ORPHAN NORMATIVE SEGMENT: {sid}')
            else:
                for cid in cids:
                    if cid not in c_by_id:
                        errors.append(f'SEGMENT UNKNOWN CONSTRAINT: {sid} -> {cid}')
                    elif disp != 'MIXED' and c_by_id[cid].get('origin') != disp:
                        errors.append(f'SEGMENT/CONSTRAINT ORIGIN MISMATCH: {sid} -> {cid}')
            quote = row.get('quote')
            if not str(quote or '').strip():
                errors.append(f'NORMATIVE SEGMENT WITHOUT QUOTE: {sid}')
            elif str(quote) not in '\n'.join(text_by_path[p][a-1:b]):
                errors.append(f'QUOTE NOT EXACT IN SOURCE RANGE: {sid}')
        if disp in {'NON_NORMATIVE', 'IMPLEMENTATION', 'DUPLICATE', 'LINK_UNCERTAIN', 'MIXED'}:
            if not str(row.get('reason', '')).strip():
                errors.append(f'SEGMENT REQUIRES REASON: {sid}')

    uncovered_lines = 0
    for p, lines in text_by_path.items():
        covered = bytearray(len(lines))
        for a, b, sid in intervals.get(p, []):
            for i in range(a-1, b):
                if covered[i]:
                    errors.append(f'OVERLAPPING RANGES: {p}:{i+1} ({sid})')
                covered[i] = 1
        for i, line in enumerate(lines):
            if line.strip() and not covered[i]:
                uncovered_lines += 1
                if uncovered_lines <= 80:
                    errors.append(f'UNCLASSIFIED NONBLANK LINE: {p}:{i+1}')
    if uncovered_lines > 80:
        errors.append(f'... and {uncovered_lines - 80} more unclassified lines')

    for cid, row in c_by_id.items():
        for sid in row.get('evidence_segment_ids') or []:
            if sid not in s_by_id:
                errors.append(f'CONSTRAINT UNKNOWN EVIDENCE: {cid} -> {sid}')
            elif cid not in (s_by_id[sid].get('constraint_ids') or []):
                errors.append(f'CONSTRAINT NOT BACKLINKED BY SEGMENT: {cid} -> {sid}')
    for pid, row in p_by_id.items():
        for cid in row.get('atomic_constraint_ids') or []:
            if cid not in c_by_id:
                errors.append(f'POLICY UNKNOWN CONSTRAINT: {pid} -> {cid}')
            elif pid not in (c_by_id[cid].get('policy_ids') or []):
                errors.append(f'POLICY NOT BACKLINKED: {pid} -> {cid}')
        for sid in row.get('evidence_segment_ids') or []:
            if sid not in s_by_id:
                errors.append(f'POLICY UNKNOWN EVIDENCE: {pid} -> {sid}')
        if row.get('status') == 'MATCHED' and not row.get('atomic_constraint_ids'):
            errors.append(f'MATCHED POLICY WITHOUT CONSTRAINT: {pid}')

    stats = {
        'candidate': candidate,
        'template_files': len(source_files),
        'text_files': len(text_by_path),
        'nonblank_lines': sum(bool(line.strip()) for lines in text_by_path.values() for line in lines),
        'unclassified_nonblank_lines': uncovered_lines,
        'oracle_policies': len(p_by_id),
        'constraints': len(c_by_id),
        'extra_constraints': sum(r.get('origin') == 'EXTRA' for r in constraints),
        'uncertain_constraints': sum(r.get('origin') == 'LINK_UNCERTAIN' for r in constraints),
        'coverage_segments': len(spans),
        'error_count': len(errors),
    }
    return stats, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--candidate', choices=CANDIDATES)
    g.add_argument('--all', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    total = 0
    for cand in CANDIDATES if args.all else (args.candidate,):
        stats, errors = validate(root, cand)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        if errors:
            print(f'FAIL: {cand} — {len(errors)} structural error(s)', file=sys.stderr)
            for e in errors[:140]:
                print(' - ' + e, file=sys.stderr)
            if len(errors) > 140:
                print(f'... plus {len(errors)-140} additional errors', file=sys.stderr)
            total += len(errors)
        else:
            print(f'PASS (STRUCTURE ONLY): {cand}. This is not semantic completeness proof.')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
