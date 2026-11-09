"""Shared, read-only helpers for Stage A Step 1 (evidence-preserving union).

All functions here only READ immutable inputs and the three completed runs.
Outputs are written exclusively by the build/assemble scripts under
stage_A/reconciled/step1_union/.

Conventions (frozen in MERGE_PROTOCOL.md):
  * raw_sha256  = SHA-256 of the exact bytes of one JSONL physical line with the
                  trailing line terminator ("\r\n" or "\n") removed.
  * ordinal     = 1-based physical line number in the input JSONL file.
  * exact_excerpt = exact substring of the decoded (UTF-8) source file from the
                  first character of start_line up to the end of end_line,
                  excluding the final line terminator; inner terminators are
                  kept verbatim (CRLF files keep "\r\n").
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]          # .../5.4
STAGE_A = ROOT / "stage_A"
INPUTS = ROOT / "inputs"
OUT = STAGE_A / "reconciled" / "step1_union"
CANDIDATES = ["M", "M1", "L0", "L1", "K0", "K1"]
RUNS = ["PRIMARY", "REPLICA", "CODEX"]
RUN_DIR = {"PRIMARY": "primary", "REPLICA": "replica"}
RUN_LETTER = {"PRIMARY": "P", "REPLICA": "R", "CODEX": "X"}
LETTER_RUN = {v: k for k, v in RUN_LETTER.items()}

# input file -> (run, record_type, id_field, label_field)
def input_files(cand: str):
    c = cand
    out = []
    for run in ("PRIMARY", "REPLICA"):
        d = f"stage_A/{RUN_DIR[run]}/{c}"
        out.append((run, "CONSTRAINT", f"{d}/constraints.jsonl", "id", "origin"))
        out.append((run, "POLICY", f"{d}/policies.jsonl", "rule_id", "status"))
        out.append((run, "ORPHAN", f"{d}/ORPHAN_CANDIDATES.jsonl", "id", "resolution"))
    out.append(("CODEX", "BLIND_FINDING", f"stage_A/independent/{c}/blind/BLIND_FINDINGS.jsonl", "id", "classification"))
    return out


def support_files(cand: str):
    """Read-only files used for evidence resolution / context (hashed in checkpoints)."""
    c = cand
    out = []
    for run in ("PRIMARY", "REPLICA"):
        d = f"stage_A/{RUN_DIR[run]}/{c}"
        out += [f"{d}/coverage_ranges.jsonl", f"{d}/files.jsonl"]
    b = f"stage_A/independent/{c}/blind"
    out += [f"{b}/FILE_REVIEW_LEDGER.jsonl", f"{b}/BLIND_COMPLETE.json"]
    return out


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def file_sha256(rel: str) -> str:
    return sha256_bytes((ROOT / rel).read_bytes())


def read_jsonl_raw(rel: str):
    """Yield (ordinal, raw_line_str_without_terminator, obj) for each non-blank line."""
    data = (ROOT / rel).read_bytes()
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    for i, raw in enumerate(lines, 1):
        if raw.endswith(b"\r"):
            raw = raw[:-1]
        if not raw.strip():
            continue
        s = raw.decode("utf-8")
        yield i, raw, json.loads(s)


def record_key(run: str, cand: str, rtype: str, oid: str) -> str:
    return f"{run}:{cand}:{rtype}:{oid}"


# ---------------------------------------------------------------- source files
_FILE_CACHE: dict = {}


def source_text(cand: str, path: str):
    """Decoded text of inputs/<cand>/<path>; None if missing/undecodable."""
    k = (cand, path)
    if k not in _FILE_CACHE:
        p = INPUTS / cand / path
        try:
            _FILE_CACHE[k] = p.read_bytes().decode("utf-8")
        except Exception:
            _FILE_CACHE[k] = None
    return _FILE_CACHE[k]


def line_spans(text: str):
    """List of (start_offset, end_offset_excluding_terminator) per 1-based line."""
    spans = []
    pos = 0
    n = len(text)
    while True:
        j = text.find("\n", pos)
        if j == -1:
            spans.append((pos, n))
            break
        end = j - 1 if j > pos and text[j - 1] == "\r" else j
        spans.append((pos, end))
        pos = j + 1
    return spans


_SPAN_CACHE: dict = {}


def exact_excerpt(cand: str, path: str, start: int, end: int):
    """Return (excerpt, error). Excerpt is verbatim file text for lines start..end."""
    t = source_text(cand, path)
    if t is None:
        return None, "SOURCE_FILE_MISSING_OR_UNDECODABLE"
    k = (cand, path)
    if k not in _SPAN_CACHE:
        _SPAN_CACHE[k] = line_spans(t)
    sp = _SPAN_CACHE[k]
    if not (isinstance(start, int) and isinstance(end, int)) or start < 1 or end < start or end > len(sp):
        return None, f"LINE_RANGE_INVALID({start}-{end} of {len(sp)})"
    return t[sp[start - 1][0]: sp[end - 1][1]], None


def ws_norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\r", "")).strip()


def quote_match(quote: str, excerpt: str) -> str:
    """Classify a reported quote against the verbatim excerpt of its cited lines."""
    if quote is None or quote == "":
        return "NO_REPORTED_QUOTE"
    ex = excerpt.replace("\r\n", "\n")
    q = quote.replace("\r\n", "\n")
    if q == ex:
        return "EXACT_FULL_RANGE"
    if q in ex:
        return "EXACT_SUBSTRING"
    if ws_norm(q) and ws_norm(q) in ws_norm(ex):
        return "WHITESPACE_NORMALIZED_SUBSTRING"
    return "MISMATCH"


_TYPO = {"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
         "−": "-", " ": " ", "…": "..."}


def harmless_norm(s: str) -> str:
    """Normalization allowed for EXACT_DUPLICATE: whitespace, case, typographic punctuation."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    for a, b in _TYPO.items():
        s = s.replace(a, b)
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    s = s.rstrip(".;")
    return s


def occurrence_id(cand: str, path: str, start: int, end: int) -> str:
    return f"OC-{cand}-{sha256_text(f'{cand}|{path}|{start}|{end}')[:12]}"


def clause_id(cand: str, path: str, start: int, end: int, excerpt_sha: str, claim_key: str) -> str:
    span = sha256_text(f"{cand}|{path}|{start}|{end}|{excerpt_sha}")[:10]
    suf = sha256_text(claim_key)[:6]
    return f"CL-{cand}-{span}-{suf}"


def group_id(cand: str, seed_claim_key: str) -> str:
    return f"FG-{cand}-{sha256_text(seed_claim_key)[:10]}"


def load_policy_texts(cand: str) -> dict:
    inv = json.loads((INPUTS / cand / "source" / "inventory.json").read_text(encoding="utf-8"))
    out = {}
    for g in inv["policygroups"]:
        for p in g["policies"]:
            out[p["id"]] = p.get("normalized_policy", "")
    return out


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    os.replace(tmp, path)


def read_jsonl(path: Path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]
