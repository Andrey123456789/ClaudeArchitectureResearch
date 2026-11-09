"""Runs the FAIR-02 synthetic report checks and records the ACTUAL outcomes.

Scores every fixture with ../score_report.py, evaluates its pre-declared expected.json and the
cross-fixture expectations, checks determinism and assessor-override validation, and writes
results/attempt_NNN/ (never overwriting an earlier attempt) plus results/LATEST.json.

Run from fair02/validation: python -B run_synthetic_checks.py
"""
import datetime
import hashlib
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
RES = os.path.join(HERE, "results")
SCORER = os.path.join(HERE, "..", "score_report.py")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_scorer():
    spec = importlib.util.spec_from_file_location("score_report", SCORER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    sr = load_scorer()
    names = sorted(d for d in os.listdir(FIX) if os.path.isdir(os.path.join(FIX, d)))
    scores, checks = {}, []
    for n in names:
        d = os.path.join(FIX, n)
        text = open(os.path.join(d, "report.md"), encoding="utf-8").read()
        ev = json.load(open(os.path.join(d, "evidence.json"), encoding="utf-8"))
        exp = json.load(open(os.path.join(d, "expected.json"), encoding="utf-8"))
        r1 = sr.apply_overrides(sr.score(text, ev), None)
        r2 = sr.apply_overrides(sr.score(text, ev), None)
        scores[n] = r1
        checks.append({"id": f"{n}:deterministic", "pass": json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)})
        if "score_min" in exp:
            checks.append({"id": f"{n}:score>={exp['score_min']}", "pass": r1["score"] >= exp["score_min"], "actual": r1["score"]})
        if "score_max" in exp:
            checks.append({"id": f"{n}:score<={exp['score_max']}", "pass": r1["score"] <= exp["score_max"], "actual": r1["score"]})
        for dim, mx in exp.get("dimension_max", {}).items():
            checks.append({"id": f"{n}:{dim}<={mx}", "pass": r1["dimensions"][dim] <= mx, "actual": r1["dimensions"][dim]})
        for pref in exp.get("flags_required_prefix", []):
            checks.append({"id": f"{n}:flag_required:{pref}", "pass": any(f.startswith(pref) for f in r1["flags"])})
        for pref in exp.get("flags_forbidden_prefix", []):
            hits = [f for f in r1["flags"] if f.startswith(pref)]
            checks.append({"id": f"{n}:flag_forbidden:{pref}", "pass": not hits, "actual": hits})

    for x in json.load(open(os.path.join(FIX, "CROSS_EXPECTATIONS.json"), encoding="utf-8")):
        a, b = scores[x["a"]], scores[x["b"]]
        kind = x.get("kind", "score_gap")
        if kind == "score_gap":
            gap = a["score"] - b["score"]
            checks.append({"id": f"{x['id']}:{x['rule']}", "pass": gap >= x["min_gap"], "actual": round(gap, 1)})
        elif kind == "words_ratio":
            ratio = a["report_words"] / b["report_words"]
            checks.append({"id": f"{x['id']}:{x['rule']}", "pass": ratio >= x["min_ratio"], "actual": round(ratio, 2)})
        elif kind == "abs_diff":
            diff = abs(a["score"] - b["score"])
            checks.append({"id": f"{x['id']}:{x['rule']}", "pass": diff <= x["max_diff"], "actual": round(diff, 1)})
        elif kind == "dimension_gap":
            gap = a["dimensions"][x["dimension"]] - b["dimensions"][x["dimension"]]
            checks.append({"id": f"{x['id']}:{x['rule']}", "pass": gap >= x["min_gap"], "actual": round(gap, 2)})
        elif kind == "abs_min_both":
            checks.append({"id": f"{x['id']}:{x['rule']}", "pass": min(a["score"], b["score"]) >= x["min"],
                           "actual": [a["score"], b["score"]]})

    # Assessor overrides: a justification is mandatory; a justified override is applied and recorded.
    base = sr.score(open(os.path.join(FIX, names[0], "report.md"), encoding="utf-8").read(),
                    json.load(open(os.path.join(FIX, names[0], "evidence.json"), encoding="utf-8")))
    try:
        sr.apply_overrides(json.loads(json.dumps(base)), {"risks": {"points": 10}})
        refused = False
    except SystemExit:
        refused = True
    checks.append({"id": "override:without_justification_refused", "pass": refused})
    ok = sr.apply_overrides(json.loads(json.dumps(base)), {"risks": {"points": 10, "justification": "assessor test"}})
    checks.append({"id": "override:justified_applied_and_recorded", "pass": ok["dimensions"]["risks"] == 10 and len(ok["overrides_applied"]) == 1})

    os.makedirs(RES, exist_ok=True)
    n_prev = len([d for d in os.listdir(RES) if d.startswith("attempt_")])
    out_dir = os.path.join(RES, f"attempt_{n_prev + 1:03d}")
    os.makedirs(out_dir)
    for n, r in scores.items():
        json.dump(r, open(os.path.join(out_dir, f"{n}.score.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    summary = {
        "attempt": n_prev + 1,
        "run_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "scorer_sha256": sha(SCORER),
        "fixture_sha256": {f"{n}/{f}": sha(os.path.join(FIX, n, f)) for n in names for f in ("report.md", "evidence.json", "expected.json")},
        "cross_expectations_sha256": sha(os.path.join(FIX, "CROSS_EXPECTATIONS.json")),
        "scores": {n: {"score": r["score"], "dimensions": r["dimensions"], "flags": r["flags"], "report_words": r["report_words"],
                       "approx_report_tokens": r["approx_report_tokens"], "run_output_tokens": r["run_output_tokens"]} for n, r in scores.items()},
        "checks": checks,
        "checks_total": len(checks),
        "checks_passed": sum(1 for c in checks if c["pass"]),
        "verdict": "ALL_PASS" if all(c["pass"] for c in checks) else "FAILURES",
    }
    json.dump(summary, open(os.path.join(out_dir, "SYNTHETIC_CHECK_RESULTS.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    json.dump(summary, open(os.path.join(RES, "LATEST.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    print(f"attempt {summary['attempt']}: {summary['checks_passed']}/{summary['checks_total']} {summary['verdict']}")
    for n, s in summary["scores"].items():
        print(f"  {n:24s} {s['score']:5.1f}  {s['dimensions']}  words={s['report_words']}")
    for c in checks:
        if not c["pass"]:
            print("  FAIL", c)


if __name__ == "__main__":
    main()
