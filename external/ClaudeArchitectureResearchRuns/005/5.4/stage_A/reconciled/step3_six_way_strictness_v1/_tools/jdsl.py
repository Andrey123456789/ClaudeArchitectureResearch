"""Judgment DSL for Step 3 batch files (_judgments/<batch>.py).

P(...)  one six-way policy judgment
D(...)  one recorded difference on one atomic dimension
C(...)  a per-candidate cell override (defaults: level FULL, force = canonical force, compliance EQUIVALENT)
"""
_RECORDS = []

LEVELS = {"FULL": "FULL_SOURCE_COMPARED", "PARTIAL": "PARTIAL_SOURCE_COMPARED",
          "MECHANICAL": "MECHANICAL_WITNESS_ONLY", "UNVERIFIED": "UNVERIFIED"}
LABELS = {"FULL_SEMANTIC_PARITY", "PARTIAL_PARITY_WITH_DELTA", "MEANINGFUL_DIVERGENCE", "CONTEXT_DEPENDENT", "UNVERIFIED"}
AXES = {"NORMATIVE", "DELIVERY", "ENFORCEMENT"}
KINDS = {"TRUE_NORMATIVE_VARIANCE", "DELIVERY_REACHABILITY_VARIANCE", "ENFORCED_BEHAVIOR_VARIANCE",
         "CANDIDATE_SPECIFIC_TECHNIQUE", "HARMLESS_PARAPHRASE", "UNCERTAINTY"}
FORCES = {"MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "DEFAULT", "MAY", "REQUIRES_APPROVAL", "CONDITIONAL", "COMPOUND",
          "DECIDED", "NONE"}
COMPLIANCE = {"EQUIVALENT", "STRICTER_THAN_CANONICAL", "WEAKER_THAN_CANONICAL", "PARTIAL", "INCOMPARABLE", "UNVERIFIED"}


def C(level="FULL", force=None, compliance=None, owners=None, note=None, unread=None, conditions=None):
    return {"level": level, "force": force, "compliance": compliance, "owners": owners, "note": note,
            "unread": unread, "conditions": conditions}


def D(dim, axis, kind, material, tiers, what, counterexample=None, evidence=None, incomparable=None, na=None,
      unverified=None, scope=None, decision=None, root=None):
    """root: id of the underlying source fact when one fact shows up under several policies (counted once)."""
    return {"dim": dim, "axis": axis, "kind": kind, "material": material, "tiers": tiers, "what": what,
            "counterexample": counterexample, "evidence": evidence or {}, "incomparable": incomparable or [],
            "na": na or {}, "unverified": unverified or [], "scope": scope, "decision": decision, "root": root}


def P(pid, dims, label, same, diffs=None, cells=None, reach=None, enforcement=None, notes=None, challenge=None):
    _RECORDS.append({"policy_id": pid, "dims": dims, "label": label, "same": same, "diffs": diffs or [],
                     "cells": cells or {}, "reach": reach, "enforcement": enforcement, "notes": notes,
                     "challenge": challenge})


def take():
    out = list(_RECORDS)
    _RECORDS.clear()
    return out
