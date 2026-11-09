"""Step 3 extra-obligation inventory (PROTOCOL section 8).

  python -B _tools/extras.py build          # cluster the active extra records, write review chunks
  python -B _tools/extras.py check [XC..]   # validate analyst decisions, write checkpoints
  python -B _tools/extras.py assemble       # write EXTRA_OBLIGATIONS_SIX_WAY.jsonl (all chunks decided)
  python -B _tools/extras.py status

Input universe: active v3 records classified EXTRA_PRODUCT, EXTRA_WORKFLOW, CANONICAL_PLUS_DELTA
(the extra remainder) and MIXED. Codex provenance is attached as recorded (Pass 1 new clauses and
facets, v3 Pass 2/3 ADD/APPEND and the 30 v3 issue clusters); nothing is re-adjudicated.

Clustering is a reading aid. Proposed classes come from simple rules and are never final: every
cluster gets an analyst decision in _extras/decisions/<chunk>.py (accept or override).
"""
import collections
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import CANDS, RECON, S3, V3, read_jsonl, sha256_file, write_json_atomic, write_jsonl_atomic, write_text_atomic  # noqa: E402
from reach import RANK, reach_class  # noqa: E402

XD = S3 / "_extras"
EXTRA = ("EXTRA_PRODUCT", "EXTRA_WORKFLOW", "CANONICAL_PLUS_DELTA", "MIXED")
CLASSES = ("GENUINE_EXTRA_NORM", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "SAME_NORM_DIFFERENT_PACKAGING",
           "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "UNRESOLVED_OR_DECISION_DEPENDENT")
STOP = set("""a an the and or of to in on for by with without from as at is are be been being it its this that these those
not no only when where which who whom whose than then there their them they do does did can could may might must should
would will shall into onto over under about any all each every other such same so if else also more most less least
use used uses using via per e g eg i ie vs own one two first after before between through during within while""".split())
CHUNK = 60  # clusters per review chunk
TH_IN, TH_X = 0.42, 0.62  # Jaccard thresholds: within a policy bucket / across buckets


def toks(s):
    s = re.sub(r"`[^`]*`", lambda m: " " + m.group(0).strip("`").replace(".", " ") + " ", s or "")
    return {w for w in re.findall(r"[a-z0-9][a-z0-9+#\-]*", s.lower()) if w not in STOP and len(w) > 2}


def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def rec_text(r):
    if r["classification"] == "CANONICAL_PLUS_DELTA" and r.get("extra_fragment"):
        return r["extra_fragment"]
    return r.get("claim_text") or r.get("extra_fragment") or ""


def provenance(key, facet_targets, overlay):
    p = []
    if key.startswith("AUG1-NC"):
        p.append("CODEX_PASS1_NEW_CLAUSE")
    elif key.startswith("AUG1-FX"):
        p.append("CODEX_PASS1_FACET_RECORD")
    elif key.startswith("V3A"):
        p.append("CODEX_PASS2_3_ADD")
    elif key.startswith("NCP"):
        p.append("V2_NEW_CLAUSE")
    elif key.startswith("REP"):
        p.append("V1_V2_REPAIR")
    else:
        p.append("STEP1_UNION")
    if key in facet_targets:
        p.append("CODEX_PASS1_FACET_OVERLAY")
    for o in overlay.get(key, []):
        p.append(f"CODEX_PASS{o['pass']}_{o['overlay_action']}:{o['cluster']}")
    return p


def anchor(r):
    ref = (r.get("current_evidence_refs") or [{}])[0]
    path = (ref.get("path") or "").replace(f"candidates/{r['candidate']}/template/", "")
    return f"{path}:{ref.get('start_line')}" + (f"-{ref.get('end_line')}" if ref.get("end_line") not in (None, ref.get("start_line")) else "")


def load():
    recs = read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl")
    active = [r for r in recs if r["repair"]["active"]]
    facets = read_jsonl(RECON / "step1_union_augmented_pass1" / "EXISTING_GROUP_FACETS.jsonl")
    facet_targets = {f["target_group_id"] for f in facets}
    overlay = collections.defaultdict(list)
    for a in read_jsonl(V3 / "PASS2_PASS3_ADJUDICATION.jsonl"):
        if a.get("overlay_target"):
            overlay[a["overlay_target"]].append(a)
    codex_cl = {}
    for a in read_jsonl(V3 / "PASS2_PASS3_ADJUDICATION.jsonl"):
        codex_cl.setdefault(a["cluster"], collections.Counter())[a["verdict"]] += 1
    return active, facet_targets, overlay, codex_cl


def build():
    active, facet_targets, overlay, codex_cl = load()
    ex = [r for r in active if r["classification"] in EXTRA]
    by_cand_all = collections.defaultdict(list)
    for r in active:
        by_cand_all[r["candidate"]].append((r, toks(rec_text(r))))
    items = []
    for r in ex:
        t = rec_text(r)
        items.append({"key": r["source_key"], "cand": r["candidate"], "cls": r["classification"], "domain": r["domain"],
                      "mod": r["modality"], "reach": reach_class(r.get("delivery_context")), "anchor": anchor(r),
                      "rel": r.get("related_policy_ids") or [], "text": t, "tok": toks(t),
                      "prov": provenance(r["source_key"], facet_targets, overlay)})
    buckets = collections.defaultdict(list)
    for it in items:
        buckets[it["rel"][0] if it["rel"] else f"NONE:{it['domain']}"].append(it)
    clusters = []
    for b in sorted(buckets):
        cl = []
        for it in sorted(buckets[b], key=lambda x: (CANDS.index(x["cand"]), x["key"])):
            best, bs = None, 0.0
            for c in cl:
                s = max(jac(it["tok"], m["tok"]) for m in c["m"])
                if s > bs:
                    best, bs = c, s
            if best is not None and bs >= TH_IN:
                best["m"].append(it)
            else:
                cl.append({"bucket": b, "m": [it]})
        clusters.extend(cl)
    # cross-bucket merge of clusters with disjoint candidate sets and very similar text
    merged = True
    while merged:
        merged = False
        for i, a in enumerate(clusters):
            ca = {m["cand"] for m in a["m"]}
            ta = set().union(*(m["tok"] for m in a["m"]))
            for j in range(i + 1, len(clusters)):
                b = clusters[j]
                if a["bucket"] == b["bucket"] or ca & {m["cand"] for m in b["m"]}:
                    continue
                if max(jac(x["tok"], y["tok"]) for x in a["m"] for y in b["m"]) >= TH_X:
                    a["m"].extend(b["m"])
                    a["bucket"] = a["bucket"] + "+" + b["bucket"]
                    del clusters[j]
                    merged = True
                    break
            if merged:
                break
    clusters.sort(key=lambda c: (c["bucket"].split("+")[0].replace("NONE:", "~"), -len({m["cand"] for m in c["m"]}), c["m"][0]["key"]))
    out = []
    for n, c in enumerate(clusters, 1):
        cid = f"X{n:04d}"
        cands = sorted({m["cand"] for m in c["m"]}, key=CANDS.index)
        rep = max(c["m"], key=lambda m: len(m["tok"]))
        # presence of the same text elsewhere in an absent candidate (any active record, any class)
        other = {}
        for a in CANDS:
            if a in cands:
                continue
            bs, bk = 0.0, None
            for r, t in by_cand_all[a]:
                s = jac(rep["tok"], t)
                if s > bs:
                    bs, bk = s, r
            if bk is not None and bs >= 0.5:
                other[a] = {"key": bk["source_key"], "classification": bk["classification"], "sim": round(bs, 2),
                            "anchor": anchor(bk), "modality": bk["modality"]}
        codex = sorted({p.split(":", 1)[1] for m in c["m"] for p in m["prov"] if ":" in p})
        prop, why = propose(c["m"], cands, other, codex, codex_cl)
        out.append({"cluster_id": cid, "bucket": c["bucket"], "candidates": cands,
                    "members": [{k: m[k] for k in ("key", "cand", "cls", "domain", "mod", "reach", "anchor", "rel", "text", "prov")} for m in c["m"]],
                    "rep_key": rep["key"], "present_other_class": other, "codex_clusters": codex,
                    "proposed_class": prop, "proposal_rule": why})
    XD.mkdir(exist_ok=True)
    write_json_atomic(XD / "CLUSTERS.json", {"built_at": datetime.datetime.now().isoformat(timespec="seconds"),
                                             "input_sha256": sha256_file(V3 / "REPAIRED_CLASSIFICATIONS.jsonl"),
                                             "n_records": len(ex), "n_clusters": len(out), "thresholds": [TH_IN, TH_X],
                                             "clusters": out})
    chunks = [out[i:i + CHUNK] for i in range(0, len(out), CHUNK)]
    plan = []
    for k, ch in enumerate(chunks, 1):
        name = f"XC{k:02d}"
        plan.append({"chunk": name, "clusters": [c["cluster_id"] for c in ch]})
        write_text_atomic(XD / "review" / f"{name}.md", render(name, ch))
    write_json_atomic(XD / "CHUNK_PLAN.json", {"chunks": plan})
    print(len(ex), "records", len(out), "clusters", len(chunks), "chunks")
    print(collections.Counter(len(c["candidates"]) for c in out))
    print(collections.Counter(c["proposed_class"] for c in out))


def propose(ms, cands, other, codex, codex_cl):
    present = set(cands) | set(other)
    txt = " ".join(m["text"].lower() for m in ms)
    if any("raw html" in m["text"].lower() or "innerhtml" in m["text"].lower() for m in ms):
        return "UNRESOLVED_OR_DECISION_DEPENDENT", "mentions raw HTML (Q-01)"
    if codex and all(sum(codex_cl.get(x, {}).values()) == codex_cl.get(x, {}).get("NON_NORMATIVE", 0) for x in codex):
        return "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "v3 Codex cluster verdict NON_NORMATIVE"
    if len(present) == 6:
        return "SAME_NORM_DIFFERENT_PACKAGING", "text present in all six (extras or other classes)"
    if re.search(r"\b(capabilit|slot|facet|module manifest|module\.md|contract\.md|selection)\w*", txt) and set(cands) <= {"M1", "L1", "K1"}:
        return "ARCHITECTURE_SPECIFIC_DIVERGENCE", "capability/slot mechanism (M1/L1/K1 only)"
    if all(m["reach"] in ("HOOK", "CHECKER", "SETTINGS", "BUILD_TOOL", "HUMAN_MAP") for m in ms):
        return "ARCHITECTURE_SPECIFIC_DIVERGENCE", "enforcement/meta mechanism text only"
    if all(m["mod"] in ("DEFAULT", "MAY", "SHOULD", "SHOULD_NOT", "NONE", "N/A", None) for m in ms):
        return "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "soft modality only (technique/default)"
    return "GENUINE_EXTRA_NORM", "binding modality in some but not all candidates (needs reading)"


def render(name, ch):
    L = [f"# Extras review {name}", "", "Per cluster: bucket (closest canonical policy), candidates with the extra, "
         "absent candidates with similar text in another class, proposed class (rule). Member lines: cand key class modality reach anchor | text.", ""]
    for c in ch:
        L.append(f"## {c['cluster_id']} [{c['bucket']}] {','.join(c['candidates'])} -> {c['proposed_class']} ({c['proposal_rule']})")
        if c["codex_clusters"]:
            L.append(f"codex: {', '.join(c['codex_clusters'])}")
        rep = next(m for m in c["members"] if m["key"] == c["rep_key"])
        L.append(f"> {rep['text'][:330]}")
        rt = toks(rep["text"])
        for m in c["members"]:
            same = m["key"] == c["rep_key"] or jac(rt, toks(m["text"])) >= 0.8
            tail = "" if same else " | " + m["text"][:200]
            pv = ",".join(p for p in m["prov"] if p != "STEP1_UNION")
            L.append(f"- {m['cand']} {m['key']} {m['cls'][:8]} {m['mod']} {m['reach']} @{m['anchor']}{(' {' + pv + '}') if pv else ''}{tail}")
        for a, o in c["present_other_class"].items():
            L.append(f"- ({a} similar {o['sim']}: {o['key']} {o['classification']} {o['modality']} @{o['anchor']})")
        L.append("")
    return "\n".join(L) + "\n"


# ---- decisions -------------------------------------------------------------------------------

_DEC = {}


def A(ids, note=None):
    """Accept the proposed class for each cluster id (list or 'Xa-Xb' range)."""
    for cid in _expand(ids):
        _DEC[cid] = {"class": None, "accepted": True, "note": note}


def X(cid, cls, note, task=None, affects=None, presence=None, links=None):
    """Analyst decision overriding (or confirming with a note) the proposal."""
    if cls not in CLASSES:
        raise ValueError(f"{cid}: bad class {cls}")
    _DEC[cid] = {"class": cls, "accepted": False, "note": note, "task": task, "affects": affects,
                 "presence": presence, "links": links}


def _expand(ids):
    if isinstance(ids, str):
        ids = [ids]
    out = []
    for i in ids:
        if "-" in i:
            a, b = i.split("-")
            out.extend(f"X{n:04d}" for n in range(int(a[1:]), int(b[1:]) + 1))
        else:
            out.append(i)
    return out


def run_decisions(name):
    _DEC.clear()
    src = XD / "decisions" / f"{name}.py"
    code = compile(src.read_text(encoding="utf-8"), str(src), "exec")
    exec(code, {"A": A, "X": X, "__name__": "decisions"})
    return dict(_DEC), sha256_file(src)


def check(names):
    data = json.loads((XD / "CLUSTERS.json").read_text(encoding="utf-8"))
    byid = {c["cluster_id"]: c for c in data["clusters"]}
    plan = json.loads((XD / "CHUNK_PLAN.json").read_text(encoding="utf-8"))["chunks"]
    names = names or [p["chunk"] for p in plan if (XD / "decisions" / f"{p['chunk']}.py").exists()]
    for name in names:
        ids = next(p["clusters"] for p in plan if p["chunk"] == name)
        dec, h = run_decisions(name)
        errs = [f"missing decision {i}" for i in ids if i not in dec] + [f"foreign id {i}" for i in dec if i not in ids]
        for i, d in dec.items():
            if i in byid and not d["accepted"] and not d["note"]:
                errs.append(f"{i}: override without note")
            if i in byid and (d["class"] or byid[i]["proposed_class"]) == "GENUINE_EXTRA_NORM" and not (d.get("task") or d["accepted"] is False):
                errs.append(f"{i}: GENUINE_EXTRA_NORM needs an analyst decision with a task")
        n = len(list((S3 / "VALIDATION_ATTEMPTS").glob(f"extras_{name}_attempt*"))) + 1
        res = {"chunk": name, "at": datetime.datetime.now().isoformat(timespec="seconds"), "decisions_sha256": h,
               "errors": errs, "n": len(ids), "overrides": sum(1 for d in dec.values() if not d["accepted"])}
        write_json_atomic(S3 / "VALIDATION_ATTEMPTS" / f"extras_{name}_attempt{n}_{'PASS' if not errs else 'FAIL'}.json", res)
        if not errs:
            write_json_atomic(S3 / "CHECKPOINTS" / "extras" / f"{name}.json", res)
        print(name, "PASS" if not errs else "FAIL", len(ids), "clusters", res["overrides"], "overrides", errs[:8])


def assemble():
    data = json.loads((XD / "CLUSTERS.json").read_text(encoding="utf-8"))
    plan = json.loads((XD / "CHUNK_PLAN.json").read_text(encoding="utf-8"))["chunks"]
    dec = {}
    for p in plan:
        if not (S3 / "CHECKPOINTS" / "extras" / f"{p['chunk']}.json").exists():
            raise SystemExit(f"chunk {p['chunk']} not checked")
        d, _ = run_decisions(p["chunk"])
        dec.update(d)
    roots, roots_by_cluster = load_roots()
    rows = []
    for c in data["clusters"]:
        d = dec[c["cluster_id"]]
        cls = d["class"] or c["proposed_class"]
        per = {}
        for a in CANDS:
            ms = [m for m in c["members"] if m["cand"] == a]
            if ms:
                best = min(ms, key=lambda m: RANK.get(m["reach"], 9))
                per[a] = {"presence": "PRESENT_AS_EXTRA", "keys": [m["key"] for m in ms],
                          "force": sorted({m["mod"] for m in ms if m["mod"]}), "delivery": best["reach"],
                          "anchors": [m["anchor"] for m in ms]}
            elif a in c["present_other_class"]:
                o = c["present_other_class"][a]
                per[a] = {"presence": f"SIMILAR_TEXT_IN_{o['classification']}", "keys": [o["key"]], "force": [o["modality"]],
                          "delivery": None, "anchors": [o["anchor"]], "similarity": o["sim"]}
            else:
                per[a] = {"presence": "NO_SIMILAR_RECORD_FOUND_BY_TOOL"}
            per[a]["presence_basis"] = "CLUSTER_TOOL"
        if d.get("presence"):
            for a, v in d["presence"].items():
                per[a] = dict(per.get(a, {}), presence=v, presence_basis="ANALYST_CLUSTER_DECISION")
        root = roots_by_cluster.get(c["cluster_id"])
        if root:
            for a in CANDS:
                if a in root["present"]:
                    per[a] = dict(per.get(a, {}), presence="PRESENT", presence_basis="ANALYST_ROOT_READING", where=root["present"][a])
                elif a in root["absent"]:
                    per[a] = dict(per.get(a, {}), presence="ABSENT", presence_basis="ANALYST_ROOT_READING", where=root["absent"][a])
        rows.append({"cluster_id": c["cluster_id"], "class": cls, "decided_by": "ANALYST_ACCEPTED_PROPOSAL" if d["accepted"] else "ANALYST_OVERRIDE",
                     "proposed_class": c["proposed_class"], "proposal_rule": c["proposal_rule"], "closest_policy_bucket": c["bucket"],
                     "summary": next(m["text"] for m in c["members"] if m["key"] == c["rep_key"])[:400],
                     "candidates_with_extra_record": c["candidates"], "per_candidate": per, "note": d.get("note"),
                     "task_effect": d.get("task"), "affects_comparable_task": d.get("affects"), "links": d.get("links"),
                     "codex_clusters": c["codex_clusters"],
                     "provenance": sorted({p for m in c["members"] for p in m["prov"]}), "n_records": len(c["members"]),
                     "root": root["id"] if root else None})
    write_jsonl_atomic(S3 / "EXTRA_OBLIGATIONS_SIX_WAY.jsonl", rows)
    for r in roots:
        r["cluster_classes"] = {cid: next(x["class"] for x in rows if x["cluster_id"] == cid) for cid in r["clusters"]}
    write_json_atomic(S3 / "EXTRA_GENUINE_ROOTS.json", {"semantics": "Six-way presence of each genuine extra norm (and the Q-01 open-decision extra), established by reading; cluster membership alone is not presence.", "roots": roots})
    print(len(rows), collections.Counter(r["class"] for r in rows))


def load_roots():
    roots = []

    def R(rid, family, title, present, absent, text_norm, evidence, task, clusters):
        if set(present) & set(absent) or set(present) | set(absent) != set(CANDS):
            raise ValueError(f"{rid}: present/absent must partition the six candidates")
        roots.append({"id": rid, "family": family, "title": title, "present": present, "absent": absent,
                      "text_norm": text_norm, "evidence": evidence, "task_effect": task, "clusters": clusters})
    src = XD / "decisions" / "ROOTS.py"
    exec(compile(src.read_text(encoding="utf-8"), str(src), "exec"), {"R": R, "__name__": "roots"})
    by = {}
    for r in roots:
        for cid in r["clusters"]:
            by[cid] = r
    return roots, by


def status():
    plan = json.loads((XD / "CHUNK_PLAN.json").read_text(encoding="utf-8"))["chunks"]
    for p in plan:
        done = (S3 / "CHECKPOINTS" / "extras" / f"{p['chunk']}.json").exists()
        print(p["chunk"], len(p["clusters"]), "DONE" if done else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"build": build, "assemble": assemble, "status": status}.get(cmd, lambda: check(sys.argv[2:]))()
