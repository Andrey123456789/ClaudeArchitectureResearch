"""R21: source-verifies the four proposed clauses against the frozen inputs and the current working copies, and writes NEW_CLAUSES_4_ADJUDICATION.jsonl. They stay candidate-specific proposals: no promotion to the 194, no replication."""
import os

from rcommon import AUD, CANDIDATES, input_path, norm_ws, read_jsonl, read_lines, utf8_stdout, wc_path, write_jsonl
from witness import norm_stream

NOTES = {'NCP-M-0001': 'DEFAULT: unmarked imperative in a knowledge skill (A1.3).', 'NCP-M1-0001': 'DEFAULT, same text as NCP-M-0001.',
         'NCP-M1-0002': 'SHOULD at LOW confidence: "useful default" has a direction under A1.4; could read as non-normative under C5.', 'NCP-L0-0001': 'DEFAULT: imperative on scan scope in a private reference (A1.3).'}
ALSO = {'NCP-M-0001': 'caching', 'NCP-M1-0001': 'caching', 'NCP-M1-0002': 'dotnet-testing', 'NCP-L0-0001': 'security-scan/references/scan-layers'}


def locate(c, rel, quote):
    text, idx = norm_stream(read_lines(wc_path(c, rel)))
    i = text.find(norm_ws(quote))
    if i < 0:
        return None
    return idx[i], idx[i + len(norm_ws(quote)) - 1]


def build():
    rows = []
    for p in read_jsonl(os.path.join(AUD, 'NEW_CLAUSE_PROPOSALS.jsonl')):
        e = p['evidence'][0]
        c = p['candidate']
        rel = e['path'].split('/template/')[1]
        orig = norm_ws(' '.join(read_lines(input_path(c, rel))[e['start_line'] - 1:e['end_line']]))
        ok_orig = norm_ws(e['quote']) in orig
        cur = locate(c, rel, e['quote'])
        rows.append({'proposal_id': p['proposal_id'], 'candidate': c, 'decision': 'ACCEPT_AS_CANDIDATE_SPECIFIC_PROPOSAL' if ok_orig and cur else 'UNRESOLVED', 'proposed_clause': p['proposed_clause'], 'classification': p['classification'], 'modality': p['modality'], 'confidence': p['confidence'],
                     'related_policy_ids': p['related_policy_ids'], 'promotion': 'NOT_PROMOTED: not part of the 194 V2 policies plus GOV-017 and GOV-018, not replicated to other candidates', 'original_evidence': {'path': e['path'], 'start_line': e['start_line'], 'end_line': e['end_line'], 'quote': e['quote'], 'verified_in_frozen_input': ok_orig},
                     'current_evidence': {'path': 'candidates/%s/template/%s' % (c, rel), 'start_line': cur[0] if cur else None, 'end_line': cur[1] if cur else None, 'status': ('SAME' if cur and cur[0] == e['start_line'] else 'MOVED') if cur else 'NOT_FOUND'},
                     'reading': NOTES[p['proposal_id']], 'distinguishing_scenario': p['distinguishing_scenario'], 'provenance': p['provenance'], 'status': 'PROPOSAL: separate from the 6,402 identities, a repaired-view addition with its own id',
                     'parity_note': 'Similar text exists in other candidates (%s). Where it stands there it is held by their own records or remains unextracted; this run does not distribute these proposals.' % ALSO[p['proposal_id']]})
    write_jsonl('NEW_CLAUSES_4_ADJUDICATION.jsonl', rows)
    return rows


if __name__ == '__main__':
    utf8_stdout()
    for r in build():
        print(r['proposal_id'], r['decision'], r['current_evidence'])
