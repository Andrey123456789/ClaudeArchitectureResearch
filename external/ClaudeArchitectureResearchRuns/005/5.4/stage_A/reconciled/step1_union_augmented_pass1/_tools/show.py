"""Reviewer context view for pass-1 claims (read-only).

  python -B show.py <C> [claim_id ...] [--ctx N] [--slack N] [--brief]
  python -B show.py --group FG-...            # full group with members and clauses
  python -B show.py --grep <C> <regex>        # search neutral claim texts and member actions in one candidate
  python -B show.py --src <C> <path> <a> <b>  # print source lines a..b
"""
from __future__ import annotations

import re
import sys

from aug_lib import UnionIndex, baseline_key_to_record_key, load_baseline_index, load_queue, source_lines

W = 600


def cut(s, n=W):
    s = "" if s is None else str(s)
    s = s.replace("\n", " / ")
    return s if len(s) <= n else s[:n] + " ..."


def member_line(U, ck):
    rk = ck.split("#")[0]
    r = U.records.get(rk, {})
    raw = r.get("raw_record", {})
    if r.get("record_type") == "BLIND_FINDING":
        return (f"    - {ck} [{raw.get('classification')}|{raw.get('confidence')}] {cut(raw.get('explanation'), 400)}"
                f"\n        scenario={cut(raw.get('behavioral_scenario'), 300)} @{raw.get('start_line')}-{raw.get('end_line')}")
    return (f"    - {ck} [{raw.get('modality')}] {cut(raw.get('normative_action'), 450)}\n"
            f"        scope={cut(raw.get('trigger_scope'), 220)} | exc={cut(raw.get('exceptions'), 220)}")


def group_summary(U, gid, full=False):
    g = U.groups[gid]
    locs = {}
    for c in U.clauses_by_group.get(gid, []):
        locs.setdefault(c["path"].replace("output/template/", ""), set()).add((c["start_line"], c["end_line"]))
    loc_s = "; ".join(f"{p}:{','.join(f'{a}-{b}' for a, b in sorted(v))}" for p, v in sorted(locs.items()))
    out = [f"  {gid} [{g['merge_type']}|{'+'.join(g['supporting_runs'])}] {cut(g['neutral_claim_text'], 900 if full else 450)}",
           f"    @ {cut(loc_s, 900 if full else 300)}"]
    if full:
        for ck in g["claim_unit_ids"]:
            out.append(member_line(U, ck))
        for q in U.queue_rel.get(gid, [])[:30]:
            other = [x for x in (q.get("group_ids_a") or []) + (q.get("group_ids_b") or []) if x != gid]
            out.append(f"    ~ {q['item_type']}:{q.get('subtype')} {other} {cut(q.get('open_question'), 200)}")
    return "\n".join(out)


def show_claim(U, q, bidx, ctx, slack, brief):
    c = q["candidate"]
    print("=" * 110)
    print(f"{q['claim_id']}  orig={q['original_status']} eff={q['effective_status']} rev={q['revision_id']}  "
          f"{q['path']}:{q['start_line']}-{q['end_line']}  codex_conf={q['codex_confidence']}")
    print(f"CLAIM: {q['claim']}")
    print(f"actor={q['actor']} | trigger={q['trigger']} | modality={q['modality']} | domain={q['domain']}")
    print(f"exceptions={q['exceptions']} | enforcement={q['enforcement_effect']} | policies={q['effective_closest_policy_ids']}")
    print(f"REASON: {q['comparison_reason']}")
    print(f"SCENARIO: {q['distinguishing_behavioral_scenario']}")
    if q.get("open_question"):
        print(f"OPEN_Q: {q['open_question']}")
    lines = source_lines(c, q["path"])
    a, b = max(1, q["start_line"] - ctx), min(len(lines), q["end_line"] + ctx)
    print(f"--- source {q['source_file']} [{q['quote_verification']}] lines {a}-{b}")
    for i in range(a, b + 1):
        mark = ">" if q["start_line"] <= i <= q["end_line"] else " "
        print(f"{mark}{i:5d}| {lines[i - 1]}")
    print("--- codex baseline refs")
    shown = set()
    for bc in q["baseline_comparisons"]:
        print(f" * {bc['assessment']}: {cut(bc['reason'], 500)}")
        for k in bc["baseline_keys"]:
            m = baseline_key_to_record_key(k)
            if m[0] == "RECORD":
                rk = m[1]
                acct = U.acct.get(rk)
                gids = acct["group_ids"] if acct else []
                print(f"   {k} -> {rk} -> {acct['disposition'] if acct else 'NOT_IN_UNION'} {gids}")
                if rk.split(":")[2] == "ORPHAN":
                    raw = U.records.get(rk, {}).get("raw_record", {})
                    print(f"      orphan: {cut(raw, 500)}")
                if len(gids) > 4:
                    print("      (record split into >4 groups; summaries suppressed, use --group)")
                    continue
                for gid in gids:
                    if gid not in shown and not brief:
                        print(group_summary(U, gid))
                        shown.add(gid)
            else:
                _, run, cand, sid = m
                br = bidx.get(k)
                raw = (br or {}).get("raw_record", {})
                rks = U.seg_to_records.get((run, cand, sid), [])
                print(f"   {k} seg disp={raw.get('disposition')} cids={raw.get('constraint_ids')} "
                      f"{raw.get('path', '')}:{raw.get('start_line')}-{raw.get('end_line')} reason={cut(raw.get('reason'), 300)}")
                for rk in rks:
                    acct = U.acct.get(rk)
                    for gid in (acct or {}).get("group_ids", []):
                        if gid not in shown and not brief:
                            print(f"     via {rk}:")
                            print(group_summary(U, gid))
                            shown.add(gid)
    print(f"--- co-located groups (slack {slack})")
    hits = U.colocated_groups(c, q["path"], q["start_line"], q["end_line"], slack)
    for gid in sorted(hits, key=lambda g: min(x[0] for x in hits[g])):
        tag = "(also above)" if gid in shown else ""
        if gid in shown and brief:
            continue
        print(group_summary(U, gid) + (" " + tag if tag else ""))


def main():
    args = sys.argv[1:]
    U = UnionIndex()
    if args and args[0] == "--group":
        for gid in args[1:]:
            print(group_summary(U, gid, full=True))
        return
    if args and args[0] == "--grep":
        c, pat = args[1], re.compile(args[2], re.I)
        for gid in U.groups_by_cand[c]:
            g = U.groups[gid]
            texts = [g["neutral_claim_text"]]
            for ck in g["claim_unit_ids"]:
                raw = U.records.get(ck.split("#")[0], {}).get("raw_record", {})
                texts.append(str(raw.get("normative_action") or raw.get("explanation") or ""))
            if any(pat.search(t or "") for t in texts):
                print(group_summary(U, gid))
        return
    if args and args[0] == "--src":
        c, p, a, b = args[1], args[2], int(args[3]), int(args[4])
        lines = source_lines(c, p)
        for i in range(a, min(b, len(lines)) + 1):
            print(f"{i:5d}| {lines[i - 1]}")
        return
    ctx, slack, brief = 6, 2, False
    rest = []
    i = 0
    while i < len(args):
        if args[i] == "--ctx":
            ctx = int(args[i + 1]); i += 2
        elif args[i] == "--slack":
            slack = int(args[i + 1]); i += 2
        elif args[i] == "--brief":
            brief = True; i += 1
        else:
            rest.append(args[i]); i += 1
    cand, ids = rest[0], set(rest[1:])
    queue = [q for q in load_queue() if q["candidate"] == cand and (not ids or q["claim_id"] in ids)]
    keys = [k for q in queue for bc in q["baseline_comparisons"] for k in bc["baseline_keys"]]
    bidx = load_baseline_index(keys)
    for q in queue:
        show_claim(U, q, bidx, ctx, slack, brief)


if __name__ == "__main__":
    main()
