"""Print compact co-location review regions for one candidate (read-only helper).

A region = maximal set of claim-record occurrences in one source file whose line
ranges overlap transitively. Only regions containing records from >= 2 runs are
listed for merge review (a merge is only proposed between records that cite a
shared source span or that the reviewer links explicitly).

Usage:
  python review_view.py M --stats
  python review_view.py M --regions 1-12
  python review_view.py M --show P:RULE-M-0001 X:BF-M-0003
"""
from __future__ import annotations

import argparse
import collections
import sys

from model import Candidate

ABBR = {"ORACLE_LINKED": "OL", "EXTRA": "EX", "LINK_UNCERTAIN": "LU",
        "POTENTIAL_EXTRA": "PE", "AMBIGUOUS": "AM", "POTENTIAL_DIFFERENT_STRENGTH": "DS"}


def regions(cm: Candidate):
    occs = collections.defaultdict(list)    # path -> [(s,e,key)]
    for k in cm.claim_keys():
        for (p, s, e) in cm.locs(k):
            occs[p].append((s, e, k))
    out = []
    for p in sorted(occs):
        items = sorted(occs[p])
        cur = []
        cur_end = -1
        for s, e, k in items:
            if cur and s > cur_end:
                out.append((p, cur))
                cur = []
            cur.append((s, e, k))
            cur_end = max(cur_end, e) if cur else e
        if cur:
            out.append((p, cur))
    res = []
    for p, items in out:
        runs = {cm.records[k]["run"] for _, _, k in items}
        res.append({"path": p, "lo": min(i[0] for i in items), "hi": max(i[1] for i in items),
                    "items": items, "multi_run": len(runs) >= 2})
    return res


def fmt_full(cm, k, here=None):
    r = cm.records[k]
    o = r["raw_record"]
    if r["record_type"] == "CONSTRAINT":
        locs = cm.locs(k)
        hl = [f"{s}-{e}" if s != e else f"{s}" for (p, s, e) in locs if here and p == here]
        other = len(locs) - len(hl)
        return (f"{'P' if r['run']=='PRIMARY' else 'R'} {o['id']} {ABBR.get(o['origin'],o['origin'])}{o['policy_ids']} "
                f"{o['modality']} L{','.join(hl)}{f' (+{other} loc)' if other else ''} :: {o['normative_action']}"
                f" || sc: {o['trigger_scope']} | ex: {o['exceptions']}")
    return (f"X {o['id']} {ABBR.get(o['classification'],o['classification'])}{o['closest_policy_ids']} "
            f"{o['confidence'][0]} L{o['start_line']}-{o['end_line']} :: E: {o['explanation']} | B: {o['behavioral_scenario']}")


def fmt_short(cm, k, first_region, here=None):
    r = cm.records[k]
    o = r["raw_record"]
    txt = o["normative_action"] if r["record_type"] == "CONSTRAINT" else o["explanation"]
    tag = 'P' if r['run'] == 'PRIMARY' else ('R' if r['run'] == 'REPLICA' else 'X')
    lab = ABBR.get(r["original_label"], r["original_label"])
    locs = [f"{s}-{e}" for (p, s, e) in cm.locs(k) if p == here]
    return f"{tag} {o['id']} {lab} L{','.join(locs)} (seen r{first_region:03d}) {txt[:90]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cand")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--regions")
    ap.add_argument("--show", nargs="*")
    ap.add_argument("--src", action="store_true", help="also print source lines of every region")
    a = ap.parse_args()
    cm = Candidate(a.cand)
    regs = regions(cm)
    mr = [g for g in regs if g["multi_run"]]
    if a.show:
        for ref in a.show:
            k = cm.resolve_ref(ref)
            print(fmt_full(cm, k), "\n   locs:", cm.locs(k))
        return
    # deterministic first-seen map over multi-run regions
    first = {}
    for i, g in enumerate(mr, 1):
        for _, _, k in g["items"]:
            first.setdefault(k, i)
    if a.stats:
        tot = 0
        for i, g in enumerate(mr, 1):
            for _, _, k in g["items"]:
                tot += len(fmt_full(cm, k, g["path"]))
        print(f"{a.cand}: regions={len(regs)} multi_run={len(mr)} chars~{tot}")
        solo = collections.Counter()
        inmr = {k for g in mr for _, _, k in g["items"]}
        for k in cm.claim_keys():
            if k not in inmr:
                solo[cm.records[k]["run"]] += 1
        print("claim records never in a multi-run region:", dict(solo))
        return
    lo, hi = (int(x) for x in a.regions.split("-"))
    from union_lib import source_text
    for i, g in enumerate(mr, 1):
        if not (lo <= i <= hi):
            continue
        p = g["path"].replace("output/template/", "")
        cnt = collections.Counter(cm.records[k]["run"][0] for _, _, k in g["items"])
        print(f"=== r{i:03d} {p} L{g['lo']}-{g['hi']} {dict(cnt)}")
        shown = set()
        # source lines for codex quotes (needed to anchor/split codex findings)
        xr = sorted({(s, e) for s, e, k in g["items"] if cm.records[k]["run"] == "CODEX"})
        if xr or a.src:
            text = source_text(a.cand, g["path"]).split("\n")
            want = set()
            for s, e in (xr if not a.src else [(g['lo'], g['hi'])]):
                want.update(range(s, e + 1))
            for ln in sorted(want):
                print(f"  {ln:4}| {text[ln-1].rstrip()[:170]}")
        for s, e, k in g["items"]:
            if k in shown:
                continue
            shown.add(k)
            if first[k] == i:
                print("  " + fmt_full(cm, k, g["path"]))
            else:
                print("  " + fmt_short(cm, k, first[k], g["path"]))


if __name__ == "__main__":
    sys.exit(main())
