"""Deterministic sample of reviewer-narrowed Codex anchors for manual source inspection.

Usage: python spotcheck.py M [n]   -> prints the sample and writes _review/<C>/anchor_spotcheck_sample.jsonl
The reviewer's verdicts are recorded in _review/<C>/anchor_spotcheck_verdicts.txt (one 'OK|ISSUE <clause_id> <note>' per line).
"""
import json, random, sys
from union_lib import OUT, read_jsonl
c = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
cl = read_jsonl(OUT / "per_candidate" / c / "SOURCE_CLAUSES.jsonl")
nar = sorted((x for x in cl if x["anchor_basis"] == "NARROWED_BY_REVIEWER_WITHIN_CODEX_QUOTE"), key=lambda x: x["clause_id"])
random.seed(f"spotcheck-{c}")
sample = random.sample(nar, min(n, len(nar)))
rows = [{"clause_id": x["clause_id"], "claim_unit_id": x["claim_unit_id"], "path": x["path"], "start_line": x["start_line"],
         "end_line": x["end_line"], "claim": x["normalized_claimed_action"], "excerpt": x["exact_excerpt"]} for x in sample]
p = OUT / "_review" / c / "anchor_spotcheck_sample.jsonl"
with open(p, "w", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"{c}: {len(nar)} narrowed anchors, sample {len(rows)} -> {p.name}")
for r in rows:
    print("---", r["clause_id"], r["claim_unit_id"].split(":")[-1], r["path"][-40:], r["start_line"], r["end_line"])
    print("  CLAIM:", r["claim"][:220])
    print("  TEXT :", r["excerpt"].replace("\r", "").replace("\n", " / ")[:320])
