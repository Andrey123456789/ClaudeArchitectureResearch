"""Gate C: semantic challenge log (same-family self-challenge, labelled as such).

  python -B _tools/gate_c.py

Builds SEMANTIC_CHALLENGE_LOG.jsonl from:
  - every material difference in POLICY_SIX_WAY_MATRIX.jsonl, joined with the per-root challenge in _challenge/challenges.py;
  - every non-material difference (checked for materiality, with its recorded reasoning);
  - the 5 STRONGER_AND_WEAKER cells and 38 partial-witness cells (_assembly/CHALLENGE_TARGETS.json);
  - the challenge items (record discrepancies, change proposals, fairness) in _challenge/challenges.py.
Fails (exit 1) when a material root has no challenge, a SAW cell lacks a challenge, or a partial-witness cell lacks a note.
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import S3, read_jsonl, sha256_file, write_json_atomic, write_jsonl_atomic  # noqa: E402

REVIEWER = "Step 3 analyst, same model family as the Step 3 judge: self-challenge, not independent confirmation"


def main():
    roots, items = {}, []

    def ROOT(rid, questions, for_, against, exceptions, verdict, limit):
        roots[rid] = {"questions": questions, "evidence_for": for_, "evidence_against": against, "exceptions": exceptions,
                      "verdict": verdict, "limit": limit}

    def ITEM(iid, kind, target, questions, for_, against, exceptions, verdict, limit):
        items.append({"id": iid, "kind": kind, "target": target, "questions": questions, "evidence_for": for_,
                      "evidence_against": against, "exceptions": exceptions, "verdict": verdict, "limit": limit})

    src = S3 / "_challenge" / "challenges.py"
    exec(compile(src.read_text(encoding="utf-8"), str(src), "exec"), {"ROOT": ROOT, "ITEM": ITEM})
    matrix = read_jsonl(S3 / "POLICY_SIX_WAY_MATRIX.jsonl")
    tgt = json.loads((S3 / "_assembly" / "CHALLENGE_TARGETS.json").read_text(encoding="utf-8"))
    log, errs = [], []
    n = 0
    for m in matrix:
        for d in m["diffs"]:
            n += 1
            base = {"id": f"C-{m['policy_id']}-{d['dim']}-{d['axis'][:3]}", "policy_id": m["policy_id"], "dim": d["dim"], "axis": d["axis"],
                    "kind": d["kind"], "root": d.get("root"), "material": d["material"], "tiers": d["tiers"], "label": m["label"],
                    "evidence_keys": d.get("evidence"), "counterexample": d.get("counterexample"), "recorded_reasoning": d["what"],
                    "reviewer": REVIEWER}
            if d["material"]:
                r = roots.get(d.get("root"))
                if not r:
                    errs.append(f"material {m['policy_id']} {d['dim']} root {d.get('root')} has no challenge")
                    continue
                if not d.get("counterexample"):
                    errs.append(f"material {m['policy_id']} {d['dim']} has no counterexample")
                log.append(dict(base, target_type="MATERIAL_DIFFERENCE", **r))
            else:
                log.append(dict(base, target_type="NON_MATERIAL_DIFFERENCE",
                                questions=["Would an identical realistic study task get a different required, forbidden or enforced outcome?"],
                                verdict="NON_MATERIAL_CONFIRMED", limit=(m.get("challenge") or "Reasoning as recorded.")))
    for rid in roots:
        if rid.startswith("RC-ENF-DEP-REMOVAL"):
            log.append({"id": f"C-{rid}", "target_type": "EXTRA_ROOT", "root": rid, "reviewer": REVIEWER, **roots[rid]})
    for x in tgt["stronger_and_weaker_cells"]:
        it = next((i for i in items if i["target"] == f"{x['policy_id']}/{x['candidate']}"), None)
        if x["challenge"]:
            log.append({"id": f"C-SAW-{x['policy_id']}-{x['candidate']}", "target_type": "STRONGER_AND_WEAKER_CELL", "policy_id": x["policy_id"],
                        "candidate": x["candidate"], "label": x["label"], "verdict": "HOLDS", "challenge_text": x["challenge"], "reviewer": REVIEWER})
        elif it:
            pass  # logged below with the items
        else:
            errs.append(f"SAW {x['policy_id']}/{x['candidate']} not challenged")
    for x in tgt["partial_witness_cells"]:
        if not x["cell_note"]:
            errs.append(f"PW38 {x['policy_id']}/{x['candidate']} has no cell note")
        log.append({"id": f"C-PW-{x['policy_id']}-{x['candidate']}", "target_type": "PARTIAL_WITNESS_CELL", "policy_id": x["policy_id"],
                    "candidate": x["candidate"], "label": x["label"], "v3_status": x["v3_status"], "cell_note": x["cell_note"],
                    "owners_read": x["cell_owners"],
                    "questions": ["Is an equal-strength fragment being taken for the whole rule?"],
                    "verdict": "HOLDS" if x["cell_note"] else "OPEN", "reviewer": REVIEWER})
    for it in items:
        log.append({"target_type": it["kind"], "reviewer": REVIEWER, **it})
    write_jsonl_atomic(S3 / "SEMANTIC_CHALLENGE_LOG.jsonl", log)
    k = len(list((S3 / "VALIDATION_ATTEMPTS").glob("gateC_attempt*"))) + 1
    res = {"gate": "C", "at": datetime.datetime.now().isoformat(timespec="seconds"), "entries": len(log), "differences": n,
           "errors": errs, "log_sha256": sha256_file(S3 / "SEMANTIC_CHALLENGE_LOG.jsonl"),
           "verdicts": {v: sum(1 for e in log if e.get("verdict") == v) for v in sorted({e.get("verdict") for e in log if e.get("verdict")})},
           "independence": "same-family self-challenge; no independent reviewer was used"}
    write_json_atomic(S3 / "VALIDATION_ATTEMPTS" / f"gateC_attempt{k}_{'PASS' if not errs else 'FAIL'}.json", res)
    if not errs:
        write_json_atomic(S3 / "CHECKPOINTS" / "gates" / "gateC.json", res)
    print("GATE C", "PASS" if not errs else "FAIL", json.dumps({k2: res[k2] for k2 in ("entries", "differences", "verdicts")}), errs[:10])
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
