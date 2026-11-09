"""Shared paths and helpers for Step 3 tools. Read-only toward every predecessor tree."""
import hashlib
import json
import os
from pathlib import Path

S3 = Path(__file__).resolve().parents[1]
ROOT = S3.parents[2]  # .../005/5.4
RECON = ROOT / "stage_A" / "reconciled"
V3 = RECON / "step2_controlled_repair_v3"
V2 = RECON / "step2_controlled_repair_v2"
V1 = RECON / "step2_controlled_repair_v1"
INPUTS = ROOT / "inputs"
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
PAIRS = [(a, b) for i, a in enumerate(CANDS) for b in CANDS[i + 1:]]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def read_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_json_atomic(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=False)
        f.write("\n")
    os.replace(tmp, p)


def write_jsonl_atomic(p, rows):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    os.replace(tmp, p)


def write_text_atomic(p, text):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, p)


def canonical_policies():
    """The frozen oracle: 194 policies from inventory.json plus GOV-017/018. Identical in all six inputs."""
    inv = read_json(INPUTS / "M" / "source" / "inventory.json")
    out = []
    for g in inv["policygroups"]:
        for p in g["policies"]:
            q = dict(p)
            q["group"] = g["id"]
            out.append(q)
    shared = read_json(INPUTS / "M" / "source" / "shared-research-invariants.json")
    for p in shared["invariants"]:
        q = dict(p)
        q["group"] = "shared-research-invariants"
        out.append(q)
    return out


_lines_cache = {}


def cand_lines(rel_path):
    """Lines of a v3 candidate file. rel_path like candidates/M/template/CLAUDE.md (relative to V3)."""
    if rel_path not in _lines_cache:
        p = V3 / rel_path
        with open(p, encoding="utf-8", errors="replace") as f:
            _lines_cache[rel_path] = f.read().split("\n")
    return _lines_cache[rel_path]


def excerpt(rel_path, start, end=None, pad=0):
    lines = cand_lines(rel_path)
    end = end or start
    s = max(1, start - pad)
    e = min(len(lines), end + pad)
    return s, e, lines[s - 1:e]
