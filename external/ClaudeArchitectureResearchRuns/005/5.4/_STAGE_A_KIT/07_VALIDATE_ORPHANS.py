#!/usr/bin/env python3
"""Read-only Stage A orphan-ledger consistency validator (not semantic proof).

For each candidate: ensure all EXTRA and LINK_UNCERTAIN atomic constraints have
traceable orphan candidate records, and validate orphan quotations, resolution
references, identities, and summaries. Unresolved orphan hypotheses are ALLOWED
only when explicitly linked and listed; no silent disappearing constraints.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

CANDIDATES = ('M', 'M1', 'L0', 'L1', 'K0', 'K1')
RESOLUTIONS = {
    'EXTRA_REGISTERED': 'EXTRA',
    'POLICY_LINKED': 'ORACLE_LINKED',
    'LINK_UNCERTAIN': 'LINK_UNCERTAIN',
    'NON_NORMATIVE': None,
    'DUPLICATE': None,
}


def read_jsonl(path, errors):
    if not path.is_file():
        errors.append(f'MISSING REQUIRED LEDGER: {path}')
        return []
    out = []
    for n, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError('expected object')
            out.append(obj)
        except (ValueError, TypeError) as exc:
            errors.append(f'INVALID JSONL {path.name}:{n}: {exc}')
    return out


def check(root, candidate):
    errors = []
    out = root / 'stage_A' / 'primary' / candidate
    snapshot = root / 'inputs' / candidate / 'output' / 'template'
    candidates = read_jsonl(out / 'ORPHAN_CANDIDATES.jsonl', errors)
    constraints = read_jsonl(out / 'constraints.jsonl', errors)
    report = out / 'ORPHAN_SWEEP_REPORT.md'
    if not report.is_file() or not report.read_text(encoding='utf-8-sig').strip():
        errors.append(f'MISSING/EMPTY ORPHAN SWEEP REPORT: {report}')
    by_id = {}
    for c in constraints:
        cid = c.get('id')
        if not cid or cid in by_id:
            errors.append(f'DUPLICATE/MISSING CONSTRAINT ID: {cid}')
        by_id[cid] = c
    referenced = set()
    orphan_ids = set()
    outcomes = Counter()
    quoted_source_cache = {}
    for row in candidates:
        oid = row.get('id')
        if not isinstance(oid, str) or not oid.startswith(f'ORPHAN-{candidate}-'):
            errors.append(f'INVALID ORPHAN ID: {oid}')
        if oid in orphan_ids:
            errors.append(f'DUPLICATE ORPHAN ID: {oid}')
        orphan_ids.add(oid)
        if row.get('candidate') != candidate:
            errors.append(f'BAD CANDIDATE FOR ORPHAN {oid}')
        disposition = row.get('resolution')
        if disposition not in RESOLUTIONS:
            errors.append(f'INVALID RESOLUTION {oid}: {disposition}')
        outcomes[disposition] += 1
        path = row.get('path')
        if not isinstance(path, str) or not path.startswith('output/template/') or '..' in Path(path).parts:
            errors.append(f'INVALID SOURCE PATH {oid}: {path}')
            continue
        full = (root / 'inputs' / candidate / path).resolve()
        if snapshot.resolve() not in full.parents or not full.is_file():
            errors.append(f'SOURCE NOT FOUND {oid}: {path}')
            continue
        if path not in quoted_source_cache:
            try:
                data = full.read_bytes()
                if b'\0' in data:
                    raise UnicodeError('binary NUL')
                quoted_source_cache[path] = data.decode('utf-8-sig').splitlines()
            except (UnicodeError, UnicodeDecodeError) as exc:
                errors.append(f'NON-TEXT ORPHAN EVIDENCE {oid}: {exc}')
                continue
        lines = quoted_source_cache[path]
        try:
            start, end = int(row['start_line']), int(row['end_line'])
            if start < 1 or end < start or end > len(lines):
                raise ValueError('range outside source')
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f'INVALID RANGE {oid}: {exc}')
            continue
        quote = row.get('quote')
        if not isinstance(quote, str) or not quote.strip() or quote not in '\n'.join(lines[start-1:end]):
            errors.append(f'INEXACT OR MISSING QUOTE {oid}: {path}:{start}-{end}')
        reason = row.get('reason')
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f'MISSING JUSTIFICATION {oid}')
        behavior = row.get('specific_behavior')
        if disposition in ('EXTRA_REGISTERED', 'LINK_UNCERTAIN') and not (isinstance(behavior, str) and behavior.strip()):
            errors.append(f'MISSING BEHAVIOR/UNCERTAINTY {oid}')
        cids = row.get('constraint_ids')
        if not isinstance(cids, list):
            errors.append(f'INVALID CONSTRAINT IDS {oid}')
            continue
        if disposition in ('EXTRA_REGISTERED', 'POLICY_LINKED', 'LINK_UNCERTAIN') and not cids:
            errors.append(f'UNLINKED OPERATIVE ORPHAN {oid}')
        if disposition == 'NON_NORMATIVE' and cids:
            errors.append(f'NON_NORMATIVE SHOULD NOT LINK RULES {oid}')
        for cid in cids:
            rule = by_id.get(cid)
            if rule is None:
                errors.append(f'UNKNOWN CONSTRAINT {oid} -> {cid}')
            elif RESOLUTIONS.get(disposition) is not None and rule.get('origin') != RESOLUTIONS.get(disposition):
                errors.append(f'ORIGIN MISMATCH {oid} -> {cid}: {rule.get("origin")}')
            if disposition != 'DUPLICATE':
                referenced.add(cid)
    for cid, c in by_id.items():
        if c.get('origin') in ('EXTRA', 'LINK_UNCERTAIN') and cid not in referenced:
            errors.append(f'UNTRACED {c.get("origin")} CONSTRAINT: {cid}')
    if report.is_file():
        content = report.read_text(encoding='utf-8-sig')
        for row in candidates:
            if row.get('resolution') == 'LINK_UNCERTAIN' and row.get('id') not in content:
                errors.append(f'OPEN ORPHAN NOT MENTIONED IN REPORT: {row.get("id")}')
    stats = {
        'candidate': candidate,
        'orphan_candidates': len(candidates),
        'resolution_counts': dict(sorted(outcomes.items(), key=lambda x: str(x[0]))),
        'extra_constraints': sum(c.get('origin') == 'EXTRA' for c in constraints),
        'uncertain_constraints': sum(c.get('origin') == 'LINK_UNCERTAIN' for c in constraints),
        'error_count': len(errors),
    }
    return stats, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path('.'))
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--candidate', choices=CANDIDATES)
    group.add_argument('--all', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve()
    failures = 0
    for name in CANDIDATES if args.all else (args.candidate,):
        stats, errors = check(root, name)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        if errors:
            print(f'FAIL: {name} — {len(errors)} orphan consistency errors', file=sys.stderr)
            for e in errors[:100]: print(' -', e, file=sys.stderr)
            if len(errors) > 100: print('... more errors omitted', file=sys.stderr)
            failures += 1
        else:
            print(f'PASS (STRUCTURE ONLY): {name}. NOT a semantic exhaustion guarantee.')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
