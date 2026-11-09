"""Shared loaders and constants for Stage A / Step 2 classification (protocol step2-v1).

All paths are resolved from this file's location:
  <root>/stage_A/reconciled/step2_classification/_tools/common.py
Only <root>/stage_A/reconciled/step2_classification/ is ever written.
"""
import hashlib
import json
import os
import re
from functools import lru_cache

TOOLS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(TOOLS)
ROOT = os.path.abspath(os.path.join(OUT, '..', '..', '..'))
REC = os.path.join(ROOT, 'stage_A', 'reconciled')
S1 = os.path.join(REC, 'step1_union')
P1 = os.path.join(REC, 'step1_union_augmented_pass1')
AUG = os.path.join(P1, 'AUGMENTED_UNION_VIEW.jsonl')
INPUTS = os.path.join(ROOT, 'inputs')

PROTOCOL_VERSION = 'step2-v1'
CANDIDATES = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
KEY_FIELD = {'ORIGINAL_GROUP': 'group_id', 'PROVISIONAL_NEW_CLAUSE': 'proposal_id',
             'PROVISIONAL_FACET_OVERLAY': 'facet_id'}

CLASS_CODES = {
    'CO': 'CANONICAL_ONLY', 'CD': 'CANONICAL_PLUS_DELTA', 'XP': 'EXTRA_PRODUCT',
    'XW': 'EXTRA_WORKFLOW', 'IA': 'INTERNAL_ARCHITECTURE', 'NN': 'NON_NORMATIVE',
    'MX': 'MIXED', 'UN': 'UNCERTAIN'}
DOMAIN_CODES = {'PE': 'PRODUCT_ENGINEERING', 'WF': 'WORKFLOW_ENFORCEMENT',
                'IA': 'INSTRUCTION_ARCHITECTURE', 'MX': 'MIXED', 'NN': 'NON_NORMATIVE',
                'UN': 'UNCERTAIN'}
ORACLE_CODES = {'FE': 'FULLY_ENTAILED', 'PE': 'PARTIALLY_ENTAILED', 'NE': 'NOT_ENTAILED',
                'NA': 'NOT_APPLICABLE', 'UN': 'UNCERTAIN'}
MODALITY_CODES = {'M': 'MUST', 'MN': 'MUST_NOT', 'S': 'SHOULD', 'SN': 'SHOULD_NOT',
                  'D': 'DEFAULT', 'Y': 'MAY', 'RA': 'REQUIRES_APPROVAL', 'DC': 'DECIDED',
                  'N': 'NONE', 'U': 'UNCERTAIN'}
MODALITIES = set(MODALITY_CODES.values())
CONF_CODES = {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}
FACET_CODES = {'AN': 'ADDITIONAL_NORMATIVE_OBLIGATION',
               'FC': 'FACTUAL_CLARIFICATION_OF_EXISTING_BEHAVIOR', 'UN': 'UNCERTAIN'}
DELTA_KIND = {'P': 'EXTRA_PRODUCT', 'W': 'EXTRA_WORKFLOW', 'A': 'INTERNAL_ARCHITECTURE'}
POLICY_RE = re.compile(r'^(GOV|ARC|PST|API|TST|SEC|RUN|DEP|FE|WF)-\d{3}$')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def read_jsonl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def write_jsonl_atomic(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')
    os.replace(tmp, p)


def write_json_atomic(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    os.replace(tmp, p)


@lru_cache(None)
def policies():
    """Return ordered dict-like list of the 196 canonical policies (194 V2 + GOV-017/018)."""
    inv = json.load(open(os.path.join(INPUTS, 'M', 'source', 'inventory.json'), encoding='utf-8'))
    out = {}
    for g in inv['policygroups']:
        for p in g['policies']:
            out[p['id']] = dict(p, group=g['id'], origin_file='inventory.json')
    shared = json.load(open(os.path.join(INPUTS, 'M', 'source', 'shared-research-invariants.json'),
                            encoding='utf-8'))
    for p in shared['invariants']:
        out[p['id']] = dict(p, group='shared-research-invariants',
                            origin_file='shared-research-invariants.json')
    assert len(out) == 196, len(out)
    return out


WORKFLOW_GOV = {'GOV-001', 'GOV-002', 'GOV-004', 'GOV-006', 'GOV-007', 'GOV-009', 'GOV-010',
                'GOV-014', 'GOV-015', 'GOV-016', 'GOV-017', 'GOV-018', 'GOV-019', 'GOV-020',
                'GOV-021', 'GOV-003', 'GOV-005'}


def policy_default_domain(pid):
    """Default domain suggested by a canonical policy (reviewer may override with d=)."""
    p = policies()[pid]
    if pid.startswith('WF-') or pid in WORKFLOW_GOV:
        return 'WORKFLOW_ENFORCEMENT'
    if p['trigger_class'] == 'workflow' and pid.split('-')[0] in ('DEP', 'TST', 'RUN', 'PST', 'API'):
        return 'WORKFLOW_ENFORCEMENT'
    return 'PRODUCT_ENGINEERING'


@lru_cache(None)
def union_view():
    return read_jsonl(AUG)


def source_key(r):
    return r[KEY_FIELD[r['view_record_type']]]


@lru_cache(None)
def occurrences():
    return {o['occurrence_id']: o for o in read_jsonl(os.path.join(S1, 'SOURCE_OCCURRENCES.jsonl'))}


@lru_cache(None)
def clauses_by_group():
    d = {}
    for c in read_jsonl(os.path.join(S1, 'SOURCE_CLAUSES.jsonl')):
        d.setdefault(c['group_id'], []).append(c)
    return d


@lru_cache(None)
def facets():
    return {f['facet_id']: f for f in read_jsonl(os.path.join(P1, 'EXISTING_GROUP_FACETS.jsonl'))}


@lru_cache(None)
def proposals():
    return {f['proposal_id']: f for f in read_jsonl(os.path.join(P1, 'NEW_CLAUSE_PROPOSALS.jsonl'))}


@lru_cache(None)
def merge_queue_by_group():
    d = {}
    for q in read_jsonl(os.path.join(S1, 'MERGE_REVIEW_QUEUE.jsonl')):
        for side in ('group_ids_a', 'group_ids_b'):
            for g in q.get(side) or []:
                d.setdefault(g, []).append(q)
    return d


def template_path(cand, rel):
    """rel is 'output/template/...' relative to inputs/<cand>/."""
    return os.path.join(INPUTS, cand, rel.replace('/', os.sep))


@lru_cache(None)
def file_lines(cand, rel):
    with open(template_path(cand, rel), encoding='utf-8', errors='replace') as f:
        return f.read().split('\n')


def frontmatter(cand, rel):
    lines = file_lines(cand, rel)
    if not lines or lines[0].strip() != '---':
        return {}, []
    fm, raw = {}, []
    key = None
    for i, l in enumerate(lines[1:60], start=2):
        if l.strip() == '---':
            break
        raw.append((i, l))
        m = re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$', l)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key and l.strip().startswith('-'):
            fm[key] = (fm[key] + ' ' + l.strip()).strip()
    return fm, raw


@lru_cache(None)
def claude_imports(cand):
    """Paths imported by the root CLAUDE.md via '@path' tokens (always loaded with it)."""
    try:
        text = '\n'.join(file_lines(cand, 'output/template/CLAUDE.md'))
    except FileNotFoundError:
        return frozenset()
    return frozenset(m.group(1).strip('`').rstrip('.,;:)') for m in re.finditer(r'(?<![\w`])@([A-Za-z0-9_./-]+\.md)', text))


def loading_context(cand, rel):
    """Mechanical description of how the file reaches the agent/tooling (not a semantic judgment)."""
    p = rel[len('output/template/'):] if rel.startswith('output/template/') else rel
    if p in claude_imports(cand):
        return 'file %s imported by root CLAUDE.md (@import: always loaded)' % p
    try:
        fm, _ = frontmatter(cand, rel)
    except FileNotFoundError:
        return 'MISSING_FILE ' + p
    base = os.path.basename(p)
    if p == 'CLAUDE.md':
        return 'root CLAUDE.md (always loaded)'
    if base == 'CLAUDE.md':
        return 'nested CLAUDE.md %s (loaded when working under that directory)' % p
    if p.startswith('.claude/rules/'):
        if fm.get('paths'):
            return 'rule %s (path-scoped; paths: %s)' % (p, fm['paths'][:160])
        return 'rule %s (no paths frontmatter: always loaded)' % p
    if p.startswith('.claude/skills/'):
        parts = p.split('/')
        name = parts[2]
        if base == 'SKILL.md':
            flags = []
            if fm.get('disable-model-invocation', '').lower() == 'true':
                flags.append('user-invoked only')
            if fm.get('user-invocable', '').lower() == 'false':
                flags.append('not user-invocable')
            return 'skill %s SKILL.md (loaded on invocation%s)' % (name, ('; ' + ', '.join(flags)) if flags else '')
        return 'skill %s private file %s (read on demand from that skill)' % (name, '/'.join(parts[3:]))
    if p.startswith('.claude/agents/'):
        return 'subagent definition %s' % base
    if p.startswith('.claude/hooks/'):
        return 'hook file %s (effective only as registered in .claude/settings.json)' % base
    if p.startswith('.claude/scripts/'):
        return 'checker/helper script %s (effective only when invoked by a hook, skill or user)' % p[len('.claude/scripts/'):]
    if p == '.claude/settings.json':
        return 'Claude Code project settings (harness-applied)'
    if p.startswith('.claude/capabilities/'):
        return 'capability file %s (loading per candidate capability mechanism)' % p[len('.claude/capabilities/'):]
    if base.upper() in ('MAP.MD', 'INSTRUCTION_MAP.MD'):
        return 'human instruction map %s (not auto-loaded)' % p
    if p.startswith('docs/'):
        return 'repository document %s (not auto-loaded)' % p
    if p in ('SPECIFICATION.md', 'CUSTOM_SETTINGS.md'):
        return 'product input file %s' % p
    if base in ('.editorconfig', 'Directory.Build.props', 'Directory.Packages.props', 'global.json',
                'nuget.config', 'NuGet.config', '.gitignore', 'package.json', '.gitattributes'):
        return 'build/tool configuration %s (applied by tooling)' % p
    return 'other file %s' % p


def candidate_template_files(cand):
    base = os.path.join(INPUTS, cand, 'output', 'template')
    out = []
    for dp, dn, fn in os.walk(base):
        for f in fn:
            out.append(os.path.relpath(os.path.join(dp, f), os.path.join(INPUTS, cand)).replace(os.sep, '/'))
    return sorted(out)


def normalize_modality(s):
    """Map a reported modality string to a base token; None when not determinable."""
    if s is None:
        return None
    t = str(s).strip().upper()
    if t.startswith('UNKNOWN') or not t:
        return None
    if t.startswith('MUST NOT') or t.startswith('MUST_NOT') or t.startswith('NEVER'):
        return 'MUST_NOT'
    if t.startswith('MUST'):
        return 'MUST'
    if t.startswith('ENFORCED_DEFAULT') or t.startswith('DEFAULT'):
        return 'DEFAULT'
    if t.startswith('SHOULD NOT') or t.startswith('SHOULD_NOT') or t.startswith('AVOID'):
        return 'SHOULD_NOT'
    if t.startswith('SHOULD') or t.startswith('PREFER'):
        return 'SHOULD'
    if t.startswith('REQUIRES_APPROVAL') or t.startswith('REQUIRES APPROVAL'):
        return 'REQUIRES_APPROVAL'
    if t.startswith('DECIDED'):
        return 'DECIDED'
    if t.startswith('ALLOWED') or t.startswith('MAY') or t.startswith('PERMITTED'):
        return 'MAY'
    return None  # ENFORCED, ENFORCED_ADVISORY, DEFINITION, ... need an explicit reviewer decision


def group_primary_clause(group):
    cls = clauses_by_group().get(group['group_id'], [])
    seed = [c for c in cls if c['claim_unit_id'] == group['seed_claim_unit_id']]
    return (seed or cls or [None])[0]


def record_anchor(r):
    """(path, start_line, end_line) used for batch ordering and primary display."""
    t = r['view_record_type']
    if t == 'ORIGINAL_GROUP':
        c = group_primary_clause(r['original_group'])
        if c:
            return c['path'], c['start_line'], c['end_line']
        o = occurrences()[r['original_group']['occurrence_ids'][0]]
        return o['path'], o['start_line'], o['end_line']
    if t == 'PROVISIONAL_NEW_CLAUSE':
        e = r['evidence']
        return e['path'], e['start_line'], e['end_line']
    f = facets()[r['facet_id']]
    e = f['evidence']
    return e['path'], e['start_line'], e['end_line']


def record_claim_text(r):
    t = r['view_record_type']
    if t == 'ORIGINAL_GROUP':
        return r['original_group']['neutral_claim_text']
    if t == 'PROVISIONAL_NEW_CLAUSE':
        return r['proposed_clause_text']
    return r['facet_text']


def record_evidence_refs(r):
    """Evidence refs into the candidate's immutable inputs (paths relative to the repo root)."""
    cand = r['candidate']
    t = r['view_record_type']
    refs = []
    if t == 'ORIGINAL_GROUP':
        for oid in r['original_group']['occurrence_ids']:
            o = occurrences()[oid]
            refs.append({'path': 'inputs/%s/%s' % (cand, o['path']), 'start_line': o['start_line'],
                         'end_line': o['end_line'], 'occurrence_id': oid,
                         'excerpt_sha256': o.get('excerpt_sha256'),
                         'location_status': o.get('location_status')})
    else:
        e = r['evidence'] if t == 'PROVISIONAL_NEW_CLAUSE' else facets()[r['facet_id']]['evidence']
        refs.append({'path': 'inputs/%s/%s' % (cand, e['path']), 'start_line': e['start_line'],
                     'end_line': e['end_line'], 'occurrence_id': None,
                     'excerpt_sha256': None,
                     'location_status': e.get('quote_verification') or e.get('codex_evidence_verification_status')})
    return refs


# --- Addendum A1 (M independent review): strength axes -------------------------------------------
STRENGTH_RANK = {'MUST': 3, 'MUST_NOT': 3, 'DECIDED': 3, 'REQUIRES_APPROVAL': 3,
                 'DEFAULT': 2, 'SHOULD': 2, 'SHOULD_NOT': 2, 'MAY': 1}
SR_CODES = {
    'SL': 'SECONDARY_LINK_ONLY',            # mismatch only against a secondary cited policy; another cited policy supplies the strength
    'PC': 'POLICY_CLAUSE_EQUIVALENT',       # restates a clause stated inside the policy; the overall policy tag differs, behavior does not
    'CK': 'CHECK_BY_REFERENCE',             # review/verification duty that checks compliance; not itself the policy's owner
    'CR': 'COROLLARY_GUIDANCE',             # lower-strength corollary consistent with the policy; neither restates nor relaxes it
    'PM': 'PERMISSION_WITHIN_POLICY',       # a MAY statement inside what the policy allows
    'AM': 'ADVISORY_MECHANISM',             # weaker: hook/checker/config reminder; the duty itself is not relaxed by it
    'GR': 'GUIDANCE_RESTATEMENT',           # weaker: prefer/avoid/technique wording of a stronger policy
    'CN': 'CONDITIONAL_NARROWING',          # weaker: 'where practical'/'when it benefits' condition absent from the policy
}
WEAKER_CODES = {'AM', 'GR', 'CN', 'PM'}
NOT_OWNER_CODES = {'CK', 'CR'}              # such links never count as direct evidence for a policy


def strength_relation(modality, policy_strength):
    """Mechanical comparison of a record's modality with a policy's tag (not a semantic verdict)."""
    a, b = STRENGTH_RANK.get(modality), STRENGTH_RANK.get(policy_strength)
    if a is None or b is None:
        return 'NOT_COMPARABLE'
    return 'SAME_CLASS' if a == b else ('RECORD_STRONGER' if a > b else 'RECORD_WEAKER')


def is_unknown(v):
    return v is None or str(v).strip().upper().startswith(('UNKNOWN', 'NOT_REPORTED'))
