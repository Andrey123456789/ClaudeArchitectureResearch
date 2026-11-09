"""In-memory model of one candidate's input records and resolved evidence.

Read-only with respect to all inputs. Used by review_view.py and build_candidate.py.
"""
from __future__ import annotations

import collections
from union_lib import (ROOT, input_files, read_jsonl_raw, record_key, sha256_bytes, sha256_text,
                       exact_excerpt, quote_match, occurrence_id, RUN_DIR, load_policy_texts)


class Candidate:
    def __init__(self, cand: str):
        self.cand = cand
        self.records = {}          # record_key -> dict(meta)
        self.order = []            # record keys in input order
        self.by_run_id = {}        # (run, rtype, original_id) -> record_key
        self.coverage = {}         # run -> {segment_id: (ordinal, obj, raw_sha)}
        self.occ = {}              # occurrence_id -> occurrence dict
        self.rec_occ = {}          # claim record_key -> list of evidence entries
        self.issues = []           # source verification issues (dicts)
        self.policy_text = load_policy_texts(cand)
        self._load()

    # ------------------------------------------------------------------ load
    def _load(self):
        c = self.cand
        for run, rtype, rel, idf, labf in input_files(c):
            seen = collections.Counter()
            for ordinal, raw, obj in read_jsonl_raw(rel):
                oid = obj.get(idf)
                seen[oid] += 1
                key = record_key(run, c, rtype, oid)
                if key in self.records:
                    key = f"{key}#L{ordinal}"
                self.records[key] = {
                    "record_key": key, "run": run, "candidate": c, "record_type": rtype,
                    "original_id": oid, "original_label_field": labf,
                    "original_label": obj.get(labf), "input_file": rel, "ordinal": ordinal,
                    "raw_sha256": sha256_bytes(raw), "raw_record": obj,
                }
                self.order.append(key)
                self.by_run_id[(run, rtype, oid)] = key
        for run in ("PRIMARY", "REPLICA"):
            rel = f"stage_A/{RUN_DIR[run]}/{c}/coverage_ranges.jsonl"
            self.coverage[run] = {o["segment_id"]: (i, o, sha256_bytes(raw)) for i, raw, o in read_jsonl_raw(rel)}
        self._resolve()

    def _add_occ(self, path, s, e):
        oid = occurrence_id(self.cand, path, s, e)
        if oid not in self.occ:
            ex, err = exact_excerpt(self.cand, path, s, e)
            self.occ[oid] = {
                "occurrence_id": oid, "candidate": self.cand, "path": path,
                "start_line": s, "end_line": e,
                "exact_excerpt": ex, "excerpt_sha256": sha256_text(ex) if ex is not None else None,
                "location_status": "VERIFIED_RANGE" if err is None else "SOURCE_UNVERIFIED",
                "location_error": err, "citations": [],
            }
        return oid

    def _resolve(self):
        c = self.cand
        for key in self.order:
            r = self.records[key]
            o = r["raw_record"]
            if r["record_type"] == "CONSTRAINT":
                ev = []
                segs = o.get("evidence_segment_ids") or []
                if not segs:
                    self.issues.append({"type": "NO_EVIDENCE_SEGMENTS", "record_key": key,
                                        "detail": "constraint declares no evidence_segment_ids"})
                for sid in segs:
                    hit = self.coverage[r["run"]].get(sid)
                    if hit is None:
                        self.issues.append({"type": "SEGMENT_UNRESOLVED", "record_key": key, "segment_id": sid,
                                            "detail": f"segment not found in {r['run']} coverage_ranges.jsonl"})
                        ev.append({"segment_id": sid, "occurrence_id": None, "status": "SEGMENT_UNRESOLVED"})
                        continue
                    sord, seg, ssha = hit
                    oid = self._add_occ(seg["path"], seg["start_line"], seg["end_line"])
                    occ = self.occ[oid]
                    q = seg.get("quote")
                    qm = quote_match(q, occ["exact_excerpt"]) if occ["exact_excerpt"] is not None else "SOURCE_UNVERIFIED"
                    backlinked = key.split(":")[-1] in (seg.get("constraint_ids") or [])
                    ent = {"segment_id": sid, "segment_ordinal": sord, "segment_raw_sha256": ssha,
                           "occurrence_id": oid, "segment_disposition": seg.get("disposition"),
                           "reported_quote": q if q is not None else None, "quote_match": qm,
                           "segment_backlinks_record": backlinked}
                    ev.append(ent)
                    occ["citations"].append({"record_key": key, "via": f"{r['run']} coverage_ranges.jsonl:{sord} ({sid})",
                                             "quote_match": qm})
                    if qm == "NO_REPORTED_QUOTE":
                        self.issues.append({"type": "INCOMPLETE_CITATION_NO_SEGMENT_QUOTE", "severity": "INFO",
                                            "record_key": key, "segment_id": sid, "occurrence_id": oid,
                                            "detail": "evidence segment carries no quote; location verified by line range only and exact_excerpt cut from the immutable file"})
                    if qm in ("MISMATCH", "SOURCE_UNVERIFIED"):
                        self.issues.append({"type": "QUOTE_MISMATCH" if qm == "MISMATCH" else "SOURCE_UNVERIFIED",
                                            "record_key": key, "segment_id": sid, "occurrence_id": oid,
                                            "detail": occ["location_error"] or "reported segment quote not found in cited lines"})
                    elif qm == "WHITESPACE_NORMALIZED_SUBSTRING":
                        self.issues.append({"type": "QUOTE_WHITESPACE_ONLY_MATCH", "severity": "INFO",
                                            "record_key": key, "segment_id": sid, "occurrence_id": oid,
                                            "detail": "segment quote matches cited lines only after whitespace/line-break normalization; exact_excerpt taken verbatim from file"})
                    if not backlinked:
                        self.issues.append({"type": "SEGMENT_NOT_BACKLINKED", "severity": "INFO", "record_key": key,
                                            "segment_id": sid, "occurrence_id": oid,
                                            "detail": "evidence segment's constraint_ids does not list this constraint (evidence still resolved by segment id)"})
                self.rec_occ[key] = ev
            elif r["record_type"] == "BLIND_FINDING":
                oid = self._add_occ(o["path"], o["start_line"], o["end_line"])
                occ = self.occ[oid]
                qm = quote_match(o.get("quote"), occ["exact_excerpt"]) if occ["exact_excerpt"] is not None else "SOURCE_UNVERIFIED"
                occ["citations"].append({"record_key": key, "via": "BLIND_FINDINGS path/start_line/end_line", "quote_match": qm})
                self.rec_occ[key] = [{"segment_id": None, "occurrence_id": oid, "reported_quote": o.get("quote"),
                                      "quote_match": qm}]
                if qm in ("MISMATCH", "SOURCE_UNVERIFIED"):
                    self.issues.append({"type": "QUOTE_MISMATCH" if qm == "MISMATCH" else "SOURCE_UNVERIFIED",
                                        "record_key": key, "occurrence_id": oid,
                                        "detail": occ["location_error"] or "Codex quote not found in cited lines"})
                elif qm == "WHITESPACE_NORMALIZED_SUBSTRING":
                    self.issues.append({"type": "QUOTE_WHITESPACE_ONLY_MATCH", "severity": "INFO", "record_key": key,
                                        "occurrence_id": oid,
                                        "detail": "Codex quote matches cited lines only after whitespace normalization; exact_excerpt taken verbatim from file"})
            elif r["record_type"] == "ORPHAN":
                if o.get("path") and isinstance(o.get("start_line"), int):
                    oid = self._add_occ(o["path"], o["start_line"], o["end_line"])
                    occ = self.occ[oid]
                    qm = quote_match(o.get("quote"), occ["exact_excerpt"]) if occ["exact_excerpt"] is not None else "SOURCE_UNVERIFIED"
                    occ["citations"].append({"record_key": key, "via": "ORPHAN path/start_line/end_line", "quote_match": qm})
                    self.rec_occ[key] = [{"segment_id": None, "occurrence_id": oid, "reported_quote": o.get("quote"),
                                          "quote_match": qm}]
                    if qm in ("MISMATCH", "SOURCE_UNVERIFIED"):
                        self.issues.append({"type": "QUOTE_MISMATCH" if qm == "MISMATCH" else "SOURCE_UNVERIFIED",
                                            "record_key": key, "occurrence_id": oid,
                                            "detail": occ["location_error"] or "orphan quote not found in cited lines"})

    # --------------------------------------------------------------- helpers
    def claim_keys(self):
        return [k for k in self.order if self.records[k]["record_type"] in ("CONSTRAINT", "BLIND_FINDING")]

    def short(self, key):
        r = self.records[key]
        return f"{r['run'][0] if r['run'] != 'CODEX' else 'X'}:{r['original_id']}"

    def resolve_ref(self, ref: str):
        """'P:RULE-M-0001' / 'R:EXTRA-M-0002' / 'X:BF-M-0001' -> record_key (claim records only)."""
        letter, oid = ref.split(":", 1)
        run = {"P": "PRIMARY", "R": "REPLICA", "X": "CODEX"}[letter]
        rtype = "BLIND_FINDING" if run == "CODEX" else "CONSTRAINT"
        return self.by_run_id.get((run, rtype, oid))

    def locs(self, key):
        out = []
        for e in self.rec_occ.get(key, []):
            if e.get("occurrence_id"):
                o = self.occ[e["occurrence_id"]]
                out.append((o["path"], o["start_line"], o["end_line"]))
        return out
