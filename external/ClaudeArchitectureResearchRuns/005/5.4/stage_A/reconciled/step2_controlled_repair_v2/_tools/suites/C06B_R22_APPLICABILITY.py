"""C06B regression: scope hints from the original trigger field. Logic checks, whole-view checks and the sample reading."""
import importlib.util
import os
import re
from collections import Counter

import c06b_census
from rcommon import out_path, read_json, read_jsonl, v1_path
from triggers import derive, scope_hint


def run(ctx):
    ctx.check('a real scope in a parenthesis becomes a hint', scope_hint('skill build-fix (failing build or tests)') == 'failing build or tests', kind='LOGIC')
    for t in ('skill x (read by project-structure)', 'rule (imported by CLAUDE.md)', 'always (CLAUDE.md is always loaded)', 'hook (post-tool-use after edits)', 'file (MSBuild import)', 'hook (registered in settings.json)', 'hook (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop)', 'script (actual-state.cjs via dispatch.cjs)', 'script (check-cochange)', 'script (dependency-guard.mjs:97-114)', 'stop (end of each Claude turn)', 'stop (end of turn)', 'agent (on delegation)', 'map (MAP.md, not auto-loaded)', 'settings (all sessions in this project)', 'x (knowledge skill dotnet-testing)', 'x (frontend.commands facet)', 'x (EditorConfig: IDE, dotnet format, build diagnostics)', 'x (EditorConfig)', 'x (hooks after edits/commands; manual/verify runs)'):
        ctx.check('a delivery phrase is not a hint: %s' % t, scope_hint(t) is None, scope_hint(t), kind='LOGIC')
    for t, want in (('skill x (read by project-structure; new applications)', 'new applications'), ('skill x (instruction-system changes; user-invoked only)', 'instruction-system changes'), ('skill x (instruction-system maintenance; never automatic)', 'instruction-system maintenance'), ('skill x (reviews of completed changes; also the code-reviewer agent)', 'reviews of completed changes'), ('rule (.editorconfig; C# rules for *.cs)', 'C# rules for *.cs')):
        ctx.check('a parenthesis that mixes delivery and scope keeps only the scope: %s' % t, scope_hint(t) == want, scope_hint(t), kind='LOGIC', actual=scope_hint(t))
    for t, want in (('rule (excluding .claude, node_modules, bin, obj, dist, etc.)', 'excluding .claude, node_modules, bin, obj, dist, etc.'), ('rule (backend)', 'backend'), ('skill (delegated review)', 'delegated review'), ('rule (csproj, Directory.Build.props, Directory.Packages.props, package.json, .npmrc)', 'csproj, Directory.Build.props, Directory.Packages.props, package.json, .npmrc')):
        ctx.check('real scope stays a hint: %s' % t, scope_hint(t) == want, scope_hint(t), kind='LOGIC', actual=scope_hint(t))
    ctx.check('no parenthesis, no hint', scope_hint('workflow verify') is None, kind='LOGIC')
    a = derive({'trigger': 'workflow build-fix (failing build or tests)', 'loading_context': 'workflow build-fix', 'trigger_status': 'ATTRIBUTED', 'claim_text': 'Repair it.', 'classification': 'CANONICAL_ONLY', 'normativity': 'NORMATIVE'})
    ctx.check('the hint does not change the status or fill the condition', a['applicability_status'] == 'UNKNOWN_NOT_EXTRACTED' and a['applicability_trigger'] is None and a['applicability_scope_hint'] == 'failing build or tests' and a['applicability_scope_source'] == 'ORIGINAL_TRIGGER_PARENTHETICAL', a, kind='LOGIC')
    b = derive({'trigger': 'A change alters API behavior (backend)', 'loading_context': 'workflow verify', 'trigger_status': 'REPAIR', 'claim_text': 'x', 'classification': 'EXTRA_WORKFLOW', 'normativity': 'NORMATIVE'})
    ctx.check('a reviewed condition gets no hint in its place', b['applicability_status'] == 'STATED_REVIEWED' and 'applicability_scope_hint' not in b, b, kind='LOGIC')
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    v1 = {r['source_key']: r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    orig = [r['source_key'] for r in rows if r['source_key'] in v1 and r.get('trigger_field_original') != v1[r['source_key']].get('trigger_field_original')]
    ctx.check('the original trigger field is untouched on every v1 record', not orig, orig[:5], kind='DATA')
    hinted = [r for r in rows if r.get('applicability_scope_hint')]
    ctx.check('real scope from a parenthesis of the original trigger now reaches the view', len(hinted) > 0, kind='DATA', actual=len(hinted))
    # A claim another change reworded can derive a new status from its own text, so only records with the v1 claim text compare.
    same_text = [r for r in hinted if r['source_key'] in v1 and r.get('claim_text') == v1[r['source_key']].get('claim_text')]
    moved = [r['source_key'] for r in same_text if r['applicability_status'] != v1[r['source_key']]['applicability_status'] or r.get('applicability_trigger') != v1[r['source_key']].get('applicability_trigger')]
    ctx.check('a hint moves no applicability status and fills no condition', same_text and not moved, moved[:5], kind='DATA', actual={'compared': len(same_text), 'moved': len(moved)})
    ctx.check('hints sit only on records with no extracted condition', all(r['applicability_status'] in ('UNKNOWN_NOT_EXTRACTED', 'CONDITION_IN_CLAIM_TEXT') for r in hinted), kind='DATA', actual=len(hinted))
    ctx.check('every hint names its source', all(r.get('applicability_scope_source') == 'ORIGINAL_TRIGGER_PARENTHETICAL' for r in hinted), kind='DATA')
    ctx.check('no hint came from a delivery phrase', not [r['source_key'] for r in hinted if re.search(r'read by|imported|always loaded', r['applicability_scope_hint'], re.I)], kind='DATA')
    census = read_json(out_path('_rules', 'C06B-R22-APPLICABILITY', 'PARENTHESIS_CENSUS.json'))
    now_parts = c06b_census.parts(rows)
    ctx.check('every distinct parenthesis part on the current view was read in the census', now_parts == census, sorted(set(now_parts['kept']) ^ set(census['kept']))[:5], kind='DATA', actual={k: len(v) for k, v in now_parts.items()})
    exists = os.path.exists(out_path('_rules', 'C06B-R22-APPLICABILITY', 'sample.py'))
    ctx.check('the sample reading exists', exists, kind='DOC')
    if not exists:
        return
    spec = importlib.util.spec_from_file_location('c06b_sample', out_path('_rules', 'C06B-R22-APPLICABILITY', 'sample.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    by = {r['source_key']: r for r in rows}
    ctx.check('the sample has 30 rows, 5 per candidate, each with a verdict and a reason', len(m.SAMPLE) == 30 and set(Counter(by[x['key']]['candidate'] for x in m.SAMPLE).values()) == {5} and all(x['verdict'] in ('RIGHT', 'WRONG', 'DEBATABLE') and x['why'] for x in m.SAMPLE), Counter(x['verdict'] for x in m.SAMPLE), kind='SEMANTIC')
    spec = importlib.util.spec_from_file_location('r22s_c06b', out_path('_rules', 'R22-111-TRIGGER', 'sample.py'))
    r22 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r22)
    ctx.check('the sample does not reuse the R22 sample', not {x['key'] for x in m.SAMPLE} & {x['key'] for x in r22.SAMPLE}, kind='DATA')
    wrong = [x['key'] for x in m.SAMPLE if x['verdict'] == 'WRONG']
    ctx.check('wrong sample rows are reported, not hidden', 'WRONG' in open(out_path('_rules', 'C06B-R22-APPLICABILITY', 'SAMPLE_READING.md'), encoding='utf-8').read() or not wrong, wrong[:6], kind='DOC', actual=len(wrong))
