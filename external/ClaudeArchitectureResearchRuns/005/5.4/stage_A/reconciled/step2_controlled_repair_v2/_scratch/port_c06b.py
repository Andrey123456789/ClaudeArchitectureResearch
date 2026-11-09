"""One-off tool port for C06B, applied only after C06's checkpoint. Each replacement must match exactly once, or the port stops."""
import os
import sys

T = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_tools'))


def edit(name, pairs):
    p = os.path.join(T, *name.split('/'))
    with open(p, encoding='utf-8') as f:
        s = f.read()
    for old, new in pairs:
        if s.count(old) != 1:
            sys.exit('no unique match in %s: %s' % (name, old[:120]))
        s = s.replace(old, new)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)


edit('triggers.py', [
    ('''LEAD = re.compile(''', '''# A parenthesis in the original trigger is often real scope ("failing build or tests"), and often delivery ("read by project-structure").
DELIVERY_PAREN = re.compile(r"^(read by|imported|claude\\.md|msbuild|planning-time|\\.editorconfig|post-tool-use|pretooluse|manual run|instruction-change|user-invoked|always|loaded|path-?scoped|on-demand|facet)|hook|\\bread by\\b|\\bimported\\b", re.I)
LEAD = re.compile('''),
    ('''def hint(claim):''', '''def scope_hint(trigger):
    """The non-delivery parentheses of the original trigger, joined. A hint with named provenance, not a verified condition; applicability_status does not change."""
    keep = [p.strip() for p in re.findall(r'\\(([^()]+)\\)', trigger or '') if p.strip() and not DELIVERY_PAREN.search(p.strip())]
    return '; '.join(keep) or None


def hint(claim):'''),
    ('''    else:
        claim = (rec.get('claim_text') or '').strip()
        if LEAD.match(claim):''', '''    else:
        scope = scope_hint(trig)
        if scope:
            out.update(applicability_scope_hint=scope, applicability_scope_source='ORIGINAL_TRIGGER_PARENTHETICAL')
        claim = (rec.get('claim_text') or '').strip()
        if LEAD.match(claim):'''),
    ('''delivery_context comes from the mechanical loading context of the cited file.
''', '''delivery_context comes from the mechanical loading context of the cited file.
applicability_scope_hint (added by v2 C06B): the scope a parenthesis of the original trigger states, when the status above found no condition. Unverified; see the sample reading.
'''),
])
edit('adaptations.py', [
    ('''    {'file': 'triggers.py', 'kind': 'PATH_PORT', 'change': 'C05-PI012-RESIDUAL', 'why': 'A condition a reviewer read at source now reaches applicability_trigger through a separate field, so the original trigger field stays untouched.'},
''', '''    {'file': 'triggers.py', 'kind': 'PATH_PORT', 'change': 'C05-PI012-RESIDUAL', 'why': 'A condition a reviewer read at source now reaches applicability_trigger through a separate field, so the original trigger field stays untouched. C06B adds applicability_scope_hint from a parenthesis of the original trigger; applicability_status is unchanged.'},
'''),
])
print('ported')
