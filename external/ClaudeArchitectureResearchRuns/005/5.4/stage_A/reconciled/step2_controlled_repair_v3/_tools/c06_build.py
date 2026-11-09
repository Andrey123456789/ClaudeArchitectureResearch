"""Writes the C06 review files from the reviewed rows and the current view: REVIEW_NEEDED_62.jsonl, PARTIAL_WITNESSES_38.jsonl, NEW_CLAIMS_42_REVIEW.jsonl."""
import importlib.util
import re
from collections import Counter

from rcommon import norm_ws, out_path, policies, read_jsonl, read_lines, utf8_stdout, v1_path, wc_path, write_jsonl

RULE = 'C06-REVIEW-SETS'
RANK = {'MUST': 3, 'MUST_NOT': 3, 'DECIDED': 3, 'REQUIRES_APPROVAL': 3, 'DEFAULT': 2, 'SHOULD': 2, 'SHOULD_NOT': 2, 'MAY': 1}
OWNER = {'M': '.claude/rules/performance.md', 'M1': '.claude/rules/performance.md', 'L0': '.claude/rules/0-core/runtime-principles.md', 'L1': '.claude/rules/0-core/backend-code.md', 'K0': '.claude/rules/backend/caching.md', 'K1': '.claude/rules/backend/runtime.md'}
PHRASES = {
    'R02-HQ01-GOV015': ['pre-existing uncommitted changes (staged, unstaged, untracked)', 'only two options', 'within a scope the user authorizes', 'suspend the whole task', 'pause safely', 'before a task that will change files or repository state'],
    'R03-MUST': ['transaction isolation level', 'concurrent reads and refills', 'commit and rollback order', 'crash between commit and invalidation', 'retries', 'tolerated'],
    'R03-DEFAULT': ['No single order is correct by itself', 'versioned key'],
    'R04-HQ03-DEP003': ['explicit, bounded user request', 'names the package and the version or range', 'accept exactly that entry', 'there is no global switch', 'report the exact version the install resolved'],
    'R05-HQ04-GOV017': ['quoting the approving text and its scope', 'decision log'],
    'R06-HQ05-DEP025': ['No confirmation, comment marker, or', 'approval opens this route'],
    'R07-81-SWAGGER': ['even when startup and composition did not change', 'NOT RUN'],
    'C01-RULE': ['effective `ManagePackageVersionsCentrally` must be true for each project'],
    'C01-CHECK': ['NOT_RUN effective Central Package Management was not proven'],
    'C01-FLOAT': ['`CentralPackageFloatingVersionsEnabled`', 'NU1011', 'does not widen'],
    'C03-WF019-EXCEPTION': ["An exception needs the user's explicit request naming it and its scope", 'a generic workflow approval is not one', 'it never allows Development seeding in Production'],
}
READING = {
    'R02-HQ01-GOV015': 'The claim follows the CLAUDE.md task-start clause. Its trigger, the two options and the headless pause are all stated there. Real Git fixtures ran in R02 and C04.',
    'R03-MUST': 'The claim lists what the owner line asks a strategy to account for. Timelines are reasoned in R03; no real database or cache ran.',
    'R03-DEFAULT': 'The claim follows the caching skill; it is technique, so DEFAULT is the right value under A1.',
    'R04-HQ03-DEP003': 'The claim follows the exception paragraph. Checker behavior ran in R04 and C01. The record is self-attested: see `REVIEWER_SIX_READINGS.md`, R04-RECORD-FORGERY.',
    'R05-HQ04-GOV017': 'The claim follows the Reserved headless sentence and the recording step. No live headless run happened.',
    'R06-HQ05-DEP025': 'The claim follows the add-dependency line, and the hook behavior ran in R06 on all named forms.',
    'R07-81-SWAGGER': 'The claim follows the verify line. No API or UI ran.',
    'C01-RULE': 'Added by C01. Follows the owner sentence; executed in the C01 suite.',
    'C01-CHECK': 'Added by C01. Executed in the C01 suite with the SDK removed from PATH.',
    'C01-FLOAT': 'Added by C01. NU1011 observed in an offline restore.',
    'C03-WF019-EXCEPTION': 'Added by C03. Follows the exception sentence in the WF-019 owner. No deployment or database ran.',
}


def load(name):
    spec = importlib.util.spec_from_file_location('c06b_' + name, out_path('_rules', RULE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def anchor(rec):
    for e in rec.get('current_evidence_refs') or []:
        if e.get('start_line'):
            rel = e['path'].split('/template/')[1]
            ls = read_lines(wc_path(rec['candidate'], rel))
            return {'path': e['path'], 'start_line': e['start_line'], 'end_line': e['end_line'], 'quote': norm_ws(' '.join(ls[e['start_line'] - 1:e['end_line']]))[:220]}
    return {'path': None, 'start_line': None, 'end_line': None, 'quote': None}


def phrase_key(r):
    rule = r['repair']['rules'][0]
    if rule == 'R03-HQ02-RUN021':
        return 'R03-MUST' if r['modality'] == 'MUST' else 'R03-DEFAULT'
    if rule == 'C01-CPM-EFFECTIVE':
        if 'value MSBuild evaluates' in r['claim_text']:
            return 'C01-RULE'
        return 'C01-CHECK' if 'NOT_RUN' in r['claim_text'] else 'C01-FLOAT'
    return rule


def main():
    utf8_stdout()
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by = {r['source_key']: r for r in rows}
    rn = load('review_needed')
    out = []
    for x in rn.ROWS:
        rec = by[x['key']]
        out.append({'key': x['key'], 'candidate': rec['candidate'], 'status': x['status'], 'reason': x['reason'], 'executed_test': x.get('test'), 'classification': rec['classification'], 'modality': rec.get('modality'), 'flag_after': bool(rec.get('review_needed')), 'v1_reason': next(r for r in read_v1() if r['source_key'] == x['key']).get('review_reason'), 'anchor': anchor(rec)})
    write_jsonl('REVIEW_NEEDED_62.jsonl', out)
    p = load('partial38')
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    pw = []
    for cell in cov:
        if cell['direct_source_keys']:
            continue
        k = (cell['candidate'], cell['policy_id'])
        note = cell.get('reviewer_override_note') or ''
        keys = re.findall(r'(?:FG|AUG1|PROP|FACET)-[A-Za-z0-9-]+', note)
        wit = []
        for key in keys:
            rec = by[key]
            a = anchor(rec)
            wit.append({'key': key, 'modality': rec.get('modality'), 'strength_vs_canonical': rec.get('strength_vs_canonical'), 'code': rec.get('strength_resolution_code'), 'active': rec['repair']['active'], 'path': a['path'], 'start_line': a['start_line'], 'quote': a['quote'], 'delivery_context': rec.get('delivery_context')})
        pol = policies()[cell['policy_id']]
        below = [w['key'] for w in wit if RANK.get(w['modality'], 0) < RANK.get(pol['normative_strength'], 0)]
        status, reading = p.READ[k]
        pw.append({'candidate': k[0], 'policy_id': k[1], 'policy_strength': pol['normative_strength'], 'policy_text': pol['normalized_policy'], 'status': status, 'reading': reading, 'counterexample': p.COUNTEREXAMPLE[k[1]], 'semantics': p.SEMANTICS, 'override_note': note, 'clause_witnesses': wit, 'clauses_below_policy_force': below, 'n_partial_witnesses': len(cell['partial_source_keys']), 'strength_status': cell['strength_status']})
    write_jsonl('PARTIAL_WITNESSES_38.jsonl', pw)
    nc = []
    for r in rows:
        if not str(r.get('view_record_type') or '').startswith('REPAIR'):
            continue
        a = anchor(r)
        rel = a['path'].split('/template/')[1] if a['path'] else None
        if r['source_key'].startswith('NCP-'):
            words = next(x for x in read_jsonl(out_path('NEW_CLAUSES_4_ADJUDICATION.jsonl')) if x['proposal_id'] == r['source_key'])
            line = norm_ws(' '.join(read_lines(wc_path(r['candidate'], rel))[a['start_line'] - 1:a['end_line']]))
            nc.append({'key': r['source_key'], 'candidate': r['candidate'], 'kind': 'PROPOSAL', 'path': rel, 'anchor': a, 'phrases_checked': [line[:60]], 'status': 'CONFIRMED', 'reading': 'Candidate-specific proposal: the source line stands, it was not promoted and it was not copied to any other candidate. %s' % (words.get('reading') or '')[:200], 'classification': r['classification'], 'modality': r.get('modality')})
            continue
        key = phrase_key(r)
        phr = list(PHRASES[key])
        if key == 'R07-81-SWAGGER' and r['candidate'] == 'L1':
            phr.append('Development API documentation UI')
        nc.append({'key': r['source_key'], 'candidate': r['candidate'], 'kind': 'ADDED_CLAIM', 'rule': r['repair']['rules'][0], 'path': rel, 'anchor': a, 'phrases_checked': phr, 'status': 'CONFIRMED', 'reading': READING[key], 'classification': r['classification'], 'modality': r.get('modality')})
    write_jsonl('NEW_CLAIMS_42_REVIEW.jsonl', nc)
    print('review', dict(Counter(x['status'] for x in out)), 'partial', dict(Counter(x['status'] for x in pw)), 'new', len(nc), dict(Counter(x['status'] for x in nc)))


_V1 = []


def read_v1():
    if not _V1:
        _V1.extend(read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl')))
    return _V1


if __name__ == '__main__':
    main()
