"""Shared helpers for the Pass 0001 adjudication / non-destructive union augmentation.

Read-only access to: inputs/, stage_A/reconciled/step1_union/, Codex pass_0001 and its
pinned revisions. Writes happen only under stage_A/reconciled/step1_union_augmented_pass1/.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "stage_A" / "reconciled" / "step1_union_augmented_pass1"
UNION = ROOT / "stage_A" / "reconciled" / "step1_union"
CIS = ROOT / "stage_A" / "codex_iterative_search"
PASS1 = CIS / "PASSES" / "pass_0001"
INPUTS = ROOT / "inputs"
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
AUG_VERSION = "step1-union-augmented-pass1/v1"

DISPOSITIONS = [
    "ALREADY_REPRESENTED",
    "EXISTING_GROUP_NEEDS_EXPLICIT_FACET",
    "DISTINCT_UNREPRESENTED_CLAUSE",
    "NOT_AN_INDEPENDENT_CONSTRAINT",
    "UNRESOLVED",
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(p: Path):
    """Return list of (raw_line_without_terminator, parsed_obj)."""
    out = []
    with open(p, "rb") as f:
        for n, raw in enumerate(f, 1):
            s = raw.rstrip(b"\r\n")
            if not s.strip():
                continue
            out.append((s, json.loads(s.decode("utf-8"))))
    return out


def load_jsonl(p: Path):
    return [o for _, o in read_jsonl(p)]


def rel(p: Path) -> str:
    return p.resolve().relative_to(ROOT).as_posix()


def atomic_write_text(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=".tmp_", suffix=p.suffix)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, p)


def dumps(o) -> str:
    return json.dumps(o, ensure_ascii=False, sort_keys=True)


def atomic_write_jsonl(p: Path, rows):
    atomic_write_text(p, "".join(dumps(r) + "\n" for r in rows))


def atomic_write_json(p: Path, o):
    atomic_write_text(p, json.dumps(o, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


def source_lines(candidate: str, path: str):
    """Lines of inputs/<C>/<path> with newline normalization (CRLF/CR -> LF), 1-based list."""
    p = INPUTS / candidate / path
    txt = p.read_bytes().decode("utf-8-sig")
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    lines = txt.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return lines


def verify_quote(candidate, path, start, end, quote):
    p = INPUTS / candidate / path
    if not p.is_file():
        return "MISSING_FILE", None
    lines = source_lines(candidate, path)
    if start < 1 or end < start or end > len(lines):
        return "INVALID_RANGE", None
    seg = "\n".join(lines[start - 1:end])
    q = (quote or "").replace("\r\n", "\n").replace("\r", "\n")
    if q == seg:
        return "EXACT_FULL_RANGE_NEWLINES_NORMALIZED", seg
    if q and q in seg:
        return "EXACT_SUBSTRING_NEWLINES_NORMALIZED", seg
    if q and " ".join(q.split()) in " ".join(seg.split()):
        return "WHITESPACE_NORMALIZED_SUBSTRING", seg
    return "MISMATCH", seg


# ---------------------------------------------------------------- union index
class UnionIndex:
    def __init__(self):
        self.groups = {}            # group_id -> obj
        self.groups_raw_sha = {}    # group_id -> sha256 of raw line
        self.groups_by_cand = {c: [] for c in CANDS}
        for raw, g in read_jsonl(UNION / "MERGED_FINDINGS.jsonl"):
            self.groups[g["group_id"]] = g
            self.groups_raw_sha[g["group_id"]] = sha256_bytes(raw)
            self.groups_by_cand[g["candidate"]].append(g["group_id"])
        self.clauses_by_group = {}
        self.clauses_by_path = {}
        for c in load_jsonl(UNION / "SOURCE_CLAUSES.jsonl"):
            self.clauses_by_group.setdefault(c["group_id"], []).append(c)
            self.clauses_by_path.setdefault((c["candidate"], c["path"]), []).append(c)
        self.acct = {}
        for r in load_jsonl(UNION / "RECORD_ACCOUNTING.jsonl"):
            self.acct[r["record_key"]] = r
        self.records = {}
        for r in load_jsonl(UNION / "SOURCE_RECORD_INDEX.jsonl"):
            self.records[r["record_key"]] = r
        self.seg_to_records = {}  # (run, candidate, segment_id) -> [record_key]
        for rk, r in self.records.items():
            for ev in r.get("resolved_evidence") or []:
                sid = ev.get("segment_id")
                if sid:
                    self.seg_to_records.setdefault((r["run"], r["candidate"], sid), []).append(rk)
        self.queue_rel = {}
        for q in load_jsonl(UNION / "MERGE_REVIEW_QUEUE.jsonl"):
            for gid in (q.get("group_ids_a") or []) + (q.get("group_ids_b") or []):
                self.queue_rel.setdefault(gid, []).append(q)

    def group_records(self, gid):
        return self.groups[gid]["claim_unit_ids"]

    def colocated_groups(self, cand, path, start, end, slack=0):
        hits = {}
        for c in self.clauses_by_path.get((cand, path), []):
            if c["start_line"] <= end + slack and c["end_line"] >= start - slack:
                hits.setdefault(c["group_id"], []).append((c["start_line"], c["end_line"], c["record_key"]))
        return hits


BASELINE_RUN = {"primary": "PRIMARY", "replica": "REPLICA", "independent": "CODEX"}
BASELINE_TYPE = {
    "constraints.jsonl": "CONSTRAINT",
    "BLIND_FINDINGS.jsonl": "BLIND_FINDING",
    "ORPHAN_CANDIDATES.jsonl": "ORPHAN",
    "policies.jsonl": "POLICY",
}


def baseline_key_to_record_key(key: str):
    """'primary/M/constraints.jsonl/EXTRA-M-0016' -> 'PRIMARY:M:CONSTRAINT:EXTRA-M-0016'.
    Coverage segments return ('SEGMENT', run, cand, seg_id)."""
    run, cand, kind, oid = key.split("/", 3)
    if kind == "coverage_ranges.jsonl":
        return ("SEGMENT", BASELINE_RUN[run], cand, oid)
    return ("RECORD", f"{BASELINE_RUN[run]}:{cand}:{BASELINE_TYPE[kind]}:{oid}")


def load_baseline_index(keys):
    keys = set(keys)
    out = {}
    with open(CIS / "BASELINE_RECORD_INDEX.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["index_key"] in keys:
                out[r["index_key"]] = r
    return out


def load_queue():
    return load_jsonl(OUT / "REVIEW_QUEUE.jsonl")
