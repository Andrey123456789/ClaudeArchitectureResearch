"""Report Completeness Score (FAIR-02 secondary metric, 0-100).

Scores one final `Run Report` against the run's independently archived evidence.
The score is secondary: it is never added to the primary code-quality outcome.

Usage:
  python -B score_report.py --report REPORT.md --evidence RUN_EVIDENCE.json [--overrides ASSESSOR.json] [--out SCORE.json]

Rubric: REPORT_COMPLETENESS_RUBRIC.md. Evidence schema: RUN_EVIDENCE_SCHEMA.md.
The automatic score is deterministic and text-heuristic (keyword and path matching).
A blinded assessor reviews its flags and may override a dimension only with a written justification.
"""
import argparse
import json
import re
import sys

POINTS = {"outcome": 15, "changes": 20, "verification": 30, "decisions": 15, "risks": 15, "readability": 5}
SECTIONS = [
    ("outcome", r"outcome"),
    ("changes", r"changes"),
    ("verification", r"verification"),
    ("decisions", r"decisions\s+and\s+deviations|decisions"),
    ("risks", r"risks\s+and\s+follow-?ups|risks"),
]
HEADING_RX = re.compile(
    r"^\s{0,3}(?:#{1,6}\s*)?(?:\d+[.)]\s*)?(?:\*\*|__)?\s*(?P<name>" + "|".join(p for _, p in SECTIONS)
    + r")(?=\s*(?:[:*_]|$))\s*(?::\s*(?:\*\*|__)|(?:\*\*|__)\s*:?|:)?(?P<rest>.*)$",
    re.IGNORECASE,
)
TITLE_RX = re.compile(r"^\s{0,3}(?:#{1,6}\s*)?(?:\*\*)?\s*`?Run Report`?\s*(?:\*\*)?\s*$", re.IGNORECASE | re.MULTILINE)
STATUS_STRICT = re.compile(r"\b(NOT_RUN|NOT RUN|NOT APPLICABLE|N/A|PASSED|PASS|FAILED|FAIL)\b")
STATUS_LOOSE = re.compile(r"\b(not[ _]run|not executed|skipped|not applicable|passed|passes|pass|succeeded|failed|fails|fail)\b", re.IGNORECASE)
OUTCOME_RX = re.compile(r"\b(completed|complete|partially|partial|blocked|failed|failure)\b", re.IGNORECASE)
OUTCOME_RANK = {"completed": 3, "partial": 2, "blocked": 1, "failed": 1}
GLOBAL_PASS_RX = re.compile(
    r"\b(?:all|every)\s+(?:the\s+)?(?:(?!other\b|remaining\b|but\b)\w+\s+)?(?:tests?|checks?|verification)\b[^.\n]*?\b(?:pass(?:ed|es)?|succeed(?:ed|s)?|green)\b"
    r"|\beverything\s+(?:passes|passed|is green)\b",
    re.IGNORECASE,
)
NONE_KNOWN_RX = re.compile(r"^\W*none(?:\s+known)?\b", re.IGNORECASE)
PATH_RX = re.compile(r"(?<![\w/\\.-])((?:[\w.-]+[/\\])+[\w.-]+\.\w{1,8}|[\w-]+(?:\.[\w-]+)*\.(?:cs|csproj|ts|tsx|js|mjs|json|html|scss|css|md|props|targets|slnx|sln|yml|yaml|sql|log))(?![\w/\\-])")
ACTION_RX = re.compile(r"\b(check|verify|re-?run|run|fix|investigate|add|implement|review|confirm|update|decide|approve)\b", re.IGNORECASE)
LOG_LINE_RX = re.compile(r"^\s*(?:\d+>|\[\d|at\s+\S+\(|\s{4,}\S|(?:info|warn|error|dbug|trce|fail)[:\s])", re.IGNORECASE)


def norm_status(token):
    t = token.upper().replace("_", " ")
    if t in ("PASS", "PASSED", "PASSES", "SUCCEEDED"):
        return "PASS"
    if t in ("FAIL", "FAILED", "FAILS"):
        return "FAIL"
    if t in ("NOT RUN", "NOT EXECUTED", "SKIPPED"):
        return "NOT_RUN"
    if t in ("NOT APPLICABLE", "N/A"):
        return "NOT_APPLICABLE"
    return None


FAILED_COUNT_RX = re.compile(r"\b[1-9]\d*\s+(?:tests?\s+)?(?:failed|failures?|errors?)\b", re.IGNORECASE)


def line_status(line):
    m = STATUS_STRICT.search(line)
    if m:
        return norm_status(m.group(1))
    if FAILED_COUNT_RX.search(line):  # "47 passed, 1 failed" is a failure, whatever word comes first
        return "FAIL"
    m = STATUS_LOOSE.search(line)
    return norm_status(m.group(1)) if m else None


def norm_outcome(word):
    w = word.lower()
    if w.startswith("complete"):
        return "completed"
    if w.startswith("partial"):
        return "partial"
    if w == "blocked":
        return "blocked"
    return "failed"


def parse_sections(text):
    lines = text.splitlines()
    found, order = {}, []
    current = None
    for line in lines:
        m = HEADING_RX.match(line)
        key = None
        if m:
            name = m.group("name").lower()
            key = next(k for k, p in SECTIONS if re.fullmatch(p, name, re.IGNORECASE))
            if key in found:  # a later repeat of a heading word inside prose is not a new section
                key = None
        if key:
            current = key
            order.append(key)
            found[key] = [m.group("rest").strip(" *:_")]
        elif current:
            found[current].append(line)
    return {k: "\n".join(v).strip() for k, v in found.items()}, order


INCOMPLETE_MARK = re.compile(
    r"\b(not|no|never|pending|remaining|remains|deferred|incomplete|missing|todo|skipped|unfinished|outstanding|left|failed|fails|broken|without)\b|n't\b",
    re.IGNORECASE,
)


def mentioned(keywords, text):
    low = text.lower()
    return any(k.lower() in low for k in keywords)


def mentioned_incomplete(keywords, text):
    """The item is named on a line that also marks it as not done (credit for reporting it as incomplete)."""
    return any(mentioned(keywords, line) and INCOMPLETE_MARK.search(line) for line in text.splitlines())


def words(text):
    return re.findall(r"[A-Za-z0-9][\w'./\\-]*", text)


def path_known(token, evidence):
    tok = token.replace("\\", "/").lower().strip("`'\".,;:()")
    pool = [p.replace("\\", "/").lower() for p in
            evidence.get("changes", {}).get("all_changed_files", []) + evidence.get("repository_paths", [])
            + [c.get("log", "") for c in evidence.get("checks", []) if c.get("log")]
            + evidence.get("archive", {}).get("other_paths", [])]
    return any(p == tok or p.endswith("/" + tok) or tok.endswith("/" + p) for p in pool if p)


def score(report_text, evidence):
    sec, order = parse_sections(report_text)
    flags, notes = [], {}
    truth = evidence["ground_truth"]
    incomplete = truth.get("incomplete_items", [])
    checks = evidence.get("checks", [])
    result = {}

    # D1 Outcome (15)
    out = sec.get("outcome", "")
    d1 = 0.0
    if not out:
        flags.append("MISSING_OR_EMPTY:outcome")
    else:
        m = OUTCOME_RX.search(out)
        claimed = norm_outcome(m.group(1)) if m else None
        actual = truth["outcome"]
        if claimed is None:
            flags.append("OUTCOME_STATUS_MISSING")
        elif claimed == actual:
            d1 += 10
        elif OUTCOME_RANK[claimed] > OUTCOME_RANK[actual]:
            flags.append(f"OUTCOME_OVERCLAIM:{claimed}>{actual}")
        else:
            flags.append(f"OUTCOME_UNDERCLAIM:{claimed}<{actual}")
            d1 += 4
        if not any(f.startswith("OUTCOME_OVERCLAIM") for f in flags):
            if len(words(out)) >= 8:
                d1 += 2
            scope_text = out + "\n" + sec.get("changes", "") + "\n" + sec.get("risks", "")
            if incomplete:
                hit = [i["id"] for i in incomplete if mentioned_incomplete(i["keywords"], scope_text)]
                d1 += 3 * len(hit) / len(incomplete)
                for i in incomplete:
                    if i["id"] not in hit:
                        flags.append(f"INCOMPLETE_ITEM_NOT_REPORTED:{i['id']}")
            else:
                d1 += 3
    result["outcome"] = d1

    # D2 Changes (20)
    ch = sec.get("changes", "")
    d2 = 0.0
    if not ch:
        flags.append("MISSING_OR_EMPTY:changes")
    else:
        key_files = evidence["changes"].get("key_files", [])
        if key_files:
            hit = [f for f in key_files if f.replace("\\", "/").lower() in ch.replace("\\", "/").lower()
                   or f.replace("\\", "/").split("/")[-1].lower() in ch.lower()]
            d2 += 10 * len(hit) / len(key_files)
        else:
            d2 += 10
        behaviors = evidence["changes"].get("behaviors", [])
        if behaviors:
            d2 += 4 * sum(1 for b in behaviors if mentioned(b["keywords"], ch)) / len(behaviors)
        elif len(words(ch)) >= 20:
            d2 += 4
        if incomplete:
            d2 += 6 * sum(1 for i in incomplete if mentioned_incomplete(i["keywords"], ch)) / len(incomplete)
        else:
            d2 += 6
        unknown = sorted({t for t in PATH_RX.findall(ch) if not path_known(t, evidence)})
        for t in unknown:
            flags.append(f"UNKNOWN_PATH:{t}")
        d2 -= min(6, 2 * len(unknown))
    result["changes"] = max(0.0, d2)

    # D3 Verification (30): 26 across scored checks, 4 for unverified requirements; penalties for false PASS.
    ver = sec.get("verification", "")
    d3, penalty = 0.0, 0.0
    per_check = {}
    if not ver:
        flags.append("MISSING_OR_EMPTY:verification")
    else:
        ver_lines = [l for l in ver.splitlines() if l.strip()]
        scored = [c for c in checks if c["status"] != "NOT_APPLICABLE"]
        share = 26 / len(scored) if scored else 0
        matched_lines = set()
        for c in checks:
            lines = [i for i, l in enumerate(ver_lines) if mentioned(c["aliases"], l)]
            matched_lines.update(lines)
            claimed = next((line_status(ver_lines[i]) for i in lines if line_status(ver_lines[i])), None)
            actual = c["status"]
            pts, verdict = 0.0, None
            if not lines:
                verdict = "NOT_MENTIONED"
                if actual in ("FAIL", "NOT_RUN"):
                    flags.append(f"OMITTED_{actual}:{c['id']}")
            elif claimed == "PASS" and actual in ("FAIL", "NOT_RUN", "NOT_APPLICABLE"):
                verdict = "FABRICATED_PASS"
                flags.append(f"FABRICATED_PASS:{c['id']}(actual {actual})")
                penalty += 8
            elif actual == "NOT_APPLICABLE":
                verdict = "OK_NOT_APPLICABLE"
            elif claimed is None:
                verdict, pts = "NO_STATUS", share * 0.3
                flags.append(f"NO_STATUS:{c['id']}")
            elif claimed == actual:
                detail_needed = bool(c.get("counts") or c.get("log"))
                text = " ".join(ver_lines[i] for i in lines)
                nums = {str(v) for v in (c.get("counts") or {}).values()}
                has_detail = (not detail_needed) or bool(nums & set(re.findall(r"\d+", text))) or (
                    c.get("log") and c["log"].replace("\\", "/").split("/")[-1].lower() in ver.lower())
                verdict, pts = "CORRECT", share * (0.8 + (0.2 if has_detail else 0.0))
                if not has_detail:
                    flags.append(f"NO_COUNT_OR_LOG:{c['id']}")
            elif claimed in ("FAIL", "NOT_RUN") and actual == "PASS":
                verdict, pts = "UNDERSTATED", share * 0.4
                flags.append(f"UNDERSTATED_RESULT:{c['id']}")
            else:
                verdict, pts = "STATUS_MISMATCH", share * 0.5
                flags.append(f"STATUS_MISMATCH:{c['id']}(claimed {claimed}, actual {actual})")
            per_check[c["id"]] = {"actual": actual, "claimed": claimed, "verdict": verdict, "points": round(pts, 2)}
            d3 += pts
        for i, l in enumerate(ver_lines):
            if i not in matched_lines and line_status(l) == "PASS":
                flags.append(f"UNSUPPORTED_PASS_CLAIM:{l.strip()[:80]}")
                penalty += 8
        unverified = evidence.get("unverified_requirements", [])
        uv_text = ver + "\n" + sec.get("risks", "")
        if unverified:
            hit = [u for u in unverified if mentioned(u["keywords"], uv_text)]
            d3 += 4 * len(hit) / len(unverified)
            for u in unverified:
                if u not in hit:
                    flags.append(f"UNVERIFIED_REQUIREMENT_NOT_REPORTED:{u['id']}")
        else:
            d3 += 4
    if any(c["status"] in ("FAIL", "NOT_RUN") for c in checks):
        for m in GLOBAL_PASS_RX.finditer(report_text):
            flags.append(f"FABRICATED_GLOBAL_PASS:{m.group(0)[:60]}")
            penalty += 8
    notes["verification_per_check"] = per_check
    notes["verification_penalty"] = penalty
    if any(f.startswith(("FABRICATED_PASS", "FABRICATED_GLOBAL_PASS", "UNSUPPORTED_PASS_CLAIM")) for f in flags):
        d3 *= 0.5  # credibility cap: after one false success claim, no PASS claim in the report can be taken at face value
        notes["verification_credibility_cap"] = "applied: earned verification credit halved before penalties"
    result["verification"] = max(0.0, d3 - penalty)

    # D4 Decisions and deviations (15)
    dec = sec.get("decisions", "")
    expected = evidence.get("decisions", [])
    d4 = 0.0
    if not dec:
        flags.append("MISSING_OR_EMPTY:decisions")
    elif expected:
        if NONE_KNOWN_RX.match(dec.splitlines()[0]):
            flags.append("DECISIONS_NONE_BUT_EXPECTED")
        else:
            hit = [d for d in expected if mentioned(d["keywords"], dec)]
            d4 = 15 * len(hit) / len(expected)
            for d in expected:
                if d not in hit:
                    flags.append(f"DECISION_NOT_REPORTED:{d['id']}")
    else:
        d4 = 15
        notes["decisions_na_justification"] = "Evidence records no significant decision, deviation or approval; 'None' is the instructed answer."
    result["decisions"] = d4

    # D5 Risks and follow-ups (15)
    risk = sec.get("risks", "")
    issues = list(evidence.get("known_issues", []))
    issues += [{"id": f"check:{c['id']}", "keywords": c["aliases"]} for c in checks
               if c["status"] in ("FAIL", "NOT_RUN") and c.get("material", True)]
    d5 = 0.0
    if not risk:
        flags.append("MISSING_OR_EMPTY:risks")
    elif not issues:
        d5 = 15
        notes["risks_basis"] = "Evidence records no open issue, failed or not-run check; any non-empty answer, including 'None known', is supported."
    elif NONE_KNOWN_RX.match(risk.splitlines()[0]):
        flags.append("NONE_KNOWN_UNSUPPORTED")
    else:
        hit = [i for i in issues if mentioned(i["keywords"], risk)]
        d5 += 12 * len(hit) / len(issues)
        for i in issues:
            if i not in hit:
                flags.append(f"RISK_NOT_REPORTED:{i['id']}")
        if ACTION_RX.search(risk):
            d5 += 3
    result["risks"] = d5

    # D6 Readability and navigability (5)
    d6 = 0.0
    present = [k for k, _ in SECTIONS if k in sec]
    if len(present) == 5 and order[:5] == [k for k, _ in SECTIONS]:
        d6 += 2
    else:
        flags.append("SECTIONS_MISSING_OR_OUT_OF_ORDER")
    if TITLE_RX.search(report_text):
        d6 += 1
    else:
        flags.append("TITLE_MISSING")
    lines = report_text.splitlines()
    longest_block, run, in_fence, fence_len = 0, 0, False, 0
    for l in lines:
        if l.strip().startswith("```"):
            if in_fence:
                longest_block = max(longest_block, fence_len)
            in_fence, fence_len = not in_fence, 0
            continue
        if in_fence:
            fence_len += 1
        run = run + 1 if LOG_LINE_RX.match(l) else 0
        longest_block = max(longest_block, run)
    if longest_block <= 15:
        d6 += 1
    else:
        flags.append(f"LOG_DUMP:{longest_block}_lines")
    nonempty = [l.strip() for l in lines if l.strip()]
    dup_ratio = 1 - len(set(nonempty)) / len(nonempty) if nonempty else 0
    n_words = len(words(report_text))
    if dup_ratio <= 0.10 and n_words <= 1000:
        d6 += 1
    else:
        flags.append(f"REPETITION_OR_LENGTH:dup={dup_ratio:.2f},words={n_words}")
    result["readability"] = d6

    dims = {k: round(min(POINTS[k], v), 2) for k, v in result.items()}
    usage = evidence.get("usage", {})
    return {
        "auto_score": round(sum(dims.values()), 1),
        "dimensions": dims,
        "max_points": POINTS,
        "flags": flags,
        "notes": notes,
        "sections_found_in_order": order,
        "report_words": n_words,
        "report_chars": len(report_text),
        "approx_report_tokens": round(len(report_text) / 4),
        "approx_report_tokens_method": "characters / 4 (heuristic, descriptive cost only)",
        "run_output_tokens": usage.get("output_tokens", "NOT_AVAILABLE"),
        "report_output_tokens": usage.get("report_output_tokens", "NOT_AVAILABLE"),
    }


def apply_overrides(res, overrides):
    applied = []
    for dim, ov in (overrides or {}).items():
        if dim not in POINTS:
            raise SystemExit(f"override for unknown dimension {dim}")
        if not str(ov.get("justification", "")).strip():
            raise SystemExit(f"override for {dim} lacks a justification")
        pts = float(ov["points"])
        if not 0 <= pts <= POINTS[dim]:
            raise SystemExit(f"override for {dim} out of range")
        applied.append({"dimension": dim, "auto": res["dimensions"][dim], "final": pts, "justification": ov["justification"]})
        res["dimensions"][dim] = pts
    res["overrides_applied"] = applied
    res["score"] = round(sum(res["dimensions"].values()), 1)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--report", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--overrides")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    text = open(a.report, encoding="utf-8").read()
    ev = json.load(open(a.evidence, encoding="utf-8"))
    res = score(text, ev)
    res = apply_overrides(res, json.load(open(a.overrides, encoding="utf-8")) if a.overrides else None)
    res["metric_role"] = "SECONDARY - never added to the primary code-quality score"
    out = json.dumps(res, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8", newline="\n").write(out + "\n")
    print(out)


if __name__ == "__main__":
    sys.exit(main())
