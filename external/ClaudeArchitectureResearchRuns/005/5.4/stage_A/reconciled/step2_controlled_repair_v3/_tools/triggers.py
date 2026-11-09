"""R22: separates when a rule applies from how it is delivered. Derived fields, original field kept. Not a verification of all records.

applicability_status values:
  STATED_REVIEWED          condition written by a reviewer (trigger_status REVIEWER, AUDIT, REPAIR), not loading context
  STATED_ATTRIBUTED        attributed seed text that does not read as loading context; not re-derived
  CONDITION_IN_CLAIM_TEXT  the trigger field reads as loading context and the claim opens with a condition word.
                           The condition is not separated: a first version cut it by pattern and the sample read showed wrong
                           boundaries. applicability_hint holds the opening words, unverified.
  UNKNOWN_NOT_EXTRACTED    the trigger field reads as loading context and the claim has no opening condition
  NOT_APPLICABLE           non-normative record
delivery_context comes from the mechanical loading context of the cited file.
applicability_scope_hint (added by v2 C06B): the scope a parenthesis of the original trigger states, when the status above found no condition. Unverified; see the sample reading.
"""
import re

LOADING = re.compile(r"(on-demand|knowledge skill|knowledge skills|workflow [a-z-]+|workflow-read|path[- ](scoped|rule)|path-loaded|always[- ]loaded|always \(|loaded|loading|skill [a-z-]+|hook [a-z-]+|hook\.c|private reference|reference of|maintainer map|checker run|invoked|\bgreenfield\b.*\bskill\b"
                     r"|^executable\b|^check-[a-z-]+\.[cm]?js|^(sub)?agent\b|\bagent \(|^repo/meta|^pretooluse|^posttooluse|^stop\b|^all (repository )?files\b|^repository files\b|^editors\b|^manifest files checked by|facet\b|\(MSBuild)", re.I)
# A parenthesis in the original trigger is often real scope ("failing build or tests"), and often delivery ("read by project-structure").
DELIVERY_PAREN = re.compile(r"^(read by|imported|claude\.md|msbuild|planning-time|\.?editorconfig|post-tool-use|pretooluse|manual|instruction-change|user-invoked|always|loaded|path-?scoped|on-demand|registered in|end of (each )?(claude )?turn|on delegation|all sessions|knowledge skill|never (automatic|loaded)|also the )|hook|\bread by\b|\bimported\b|\bpre/post\b|\.(cjs|mjs)\b|check-cochange|\bfacet\b|not auto-loaded", re.I)
LEAD = re.compile(r"^(When|If|Before|After|For|On|Whenever|During|Once|While|Where|Unless|In an?)\b", re.I)


def reads_as_loading(trigger, loading):
    t = (trigger or '').strip()
    if not t or t.upper() == 'NONE':
        return False
    if loading and t.lower() in loading.lower():
        return True
    return bool(LOADING.search(t))


def scope_hint(trigger):
    """The non-delivery parts of the original trigger's parentheses, joined. A parenthesis can mix delivery and scope around a semicolon, so each part is judged alone. A hint with named provenance, not a verified condition; applicability_status does not change."""
    parts = [p.strip() for group in re.findall(r'\(([^()]+)\)', trigger or '') for p in group.split(';')]
    return '; '.join(p for p in parts if p and not DELIVERY_PAREN.search(p)) or None


def hint(claim):
    head = re.split(r'[,:;]', claim, 1)[0]
    return head[:90].strip()


def derive(rec):
    trig, status = rec.get('trigger'), rec.get('trigger_status')
    loading = rec.get('loading_context') or ''
    out = {'trigger_field_original': trig, 'delivery_context': loading or None, 'delivery_status': 'MECHANICAL_FROM_FILE' if loading else 'UNKNOWN', 'applicability_hint': None}
    if rec.get('normativity') == 'NON_NORMATIVE' or rec.get('classification') == 'NON_NORMATIVE':
        out.update(applicability_trigger=None, applicability_status='NOT_APPLICABLE')
        return out
    if rec.get('applicability_override'):
        # A condition a reviewer read at source. The original trigger field stays as it is.
        out.update(applicability_trigger=rec['applicability_override'], applicability_status='STATED_REVIEWED')
        return out
    flagged = reads_as_loading(trig, loading)
    if status in ('REVIEWER', 'AUDIT', 'REPAIR') and not flagged:
        out.update(applicability_trigger=trig, applicability_status='STATED_REVIEWED')
    elif not flagged:
        out.update(applicability_trigger=None if (trig or '').strip().upper() == 'NONE' else trig, applicability_status='STATED_ATTRIBUTED')
    else:
        scope = scope_hint(trig)
        if scope:
            out.update(applicability_scope_hint=scope, applicability_scope_source='ORIGINAL_TRIGGER_PARENTHETICAL')
        claim = (rec.get('claim_text') or '').strip()
        if LEAD.match(claim):
            out.update(applicability_trigger=None, applicability_hint=hint(claim), applicability_status='CONDITION_IN_CLAIM_TEXT')
        else:
            out.update(applicability_trigger=None, applicability_status='UNKNOWN_NOT_EXTRACTED')
    return out
