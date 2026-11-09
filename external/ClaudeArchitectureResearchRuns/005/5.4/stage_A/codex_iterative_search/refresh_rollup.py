"""Regenerate explicitly provisional reviewer reports from committed records."""
import json
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def save(p,text):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(text,encoding='utf-8');t.replace(p)
s=read(O/'STATE.json'); revisions=s.get('finding_revisions',{})
novel=jl(O/'NOVEL_FINDINGS.jsonl'); unresolved=jl(O/'UNRESOLVED_FINDINGS.jsonl')
effective=[r for r in novel if revisions.get(r['id'],{}).get('effective_status',r['comparison_status']) in ['NOVEL_CLAUSE','RECLASSIFICATION_CANDIDATE']]
counts=Counter(r['candidate'] for r in effective); uc=Counter(r['candidate'] for r in unresolved)
header=f"# Provisional handoff — IN_PROGRESS\n\nThis is a durable recovery and reviewer snapshot, not the final frozen handoff. Completed full passes: {len(s['convergence_history'])}. Do not infer saturation or semantic completeness. Never label these hypotheses proven EXTRA or a proven cross-candidate difference.\n\n"
header+='Compare exact source quotations in NOVEL_FINDINGS.jsonl and UNRESOLVED_FINDINGS.jsonl against the specific same-candidate baseline keys in BASELINE_RECORD_INDEX.jsonl. Apply REVISIONS before importing. CIS-M1-0004 is withdrawn as already covered by replica EXTRA-M1-0012; the original is retained for audit. This task has not read or modified Claude reconciliation.\n\n'
lines=[header,'## Candidate hypotheses\n\n']
for r in effective:
 lines.append(f"- **{r['id']}** ({r['comparison_status']}): {r['claim']} Evidence: `inputs/{r['candidate']}/{r['path']}:{r['start_line']}-{r['end_line']}`.\n")
lines.append('\n## Open questions\n\n')
for r in unresolved:
 lines.append(f"- **{r['id']}**: {r.get('open_question',r['claim'])} Evidence: `inputs/{r['candidate']}/{r['path']}:{r['start_line']}-{r['end_line']}`.\n")
lines.append('\nRisks: technical prerequisites may not be separate norms; broad prior records may subsume narrow actions; source labels and header technique disclaimers do not settle effective obligations. Review each counter-scenario and loading condition independently. Do not import withdrawn or unresolved hypotheses as adjudicated constraints.\n')
save(O/'HANDOFF_TO_CLAUDE.md',''.join(lines))
coverage=jl(O/'PASSES'/f"pass_{s['current_pass_id']:04d}"/'FILE_COVERAGE.jsonl')
cc=Counter(r['candidate'] for r in coverage)
report='# Iterative search progress — IN_PROGRESS\n\n'
report+=f"Current strategy: {s['current_strategy']}; pass {s['current_pass_id']:04d}. Completed full passes: {len(s['convergence_history'])}. Mandatory six-family search and convergence criteria remain unfinished.\n\n"
policy_ledger=O/'PASSES'/f"pass_{s['current_pass_id']:04d}"/'POLICY_BOUNDARY_REVIEW.jsonl'
if policy_ledger.exists():
 pc=Counter(r['candidate'] for r in jl(policy_ledger))
 report+='Current-pass canonical boundary reviews: '+', '.join(f'{c} {pc[c]}/196' for c in ['K1','L1','M1','K0','L0','M'])+'. Relevant source contexts are checkpointed in policy receipts; file-level accounting is finalized after policy review and source-index reconciliation.\n\n'
report+='| Candidate | Files inspected in current pass | Effective novel/reclassification candidates | Open hypotheses |\n|---|---:|---:|---:|\n'
for c in ['M','M1','L0','L1','K0','K1']:report+=f"| {c} | {cc[c]}/{s['counts']['source_files'][c]} | {counts[c]} | {uc[c]} |\n"
report+=f"\nOriginal append-only novel queue: {len(novel)}; effective retained: {len(effective)}; unresolved: {len(unresolved)}. Counts reflect auditable revisions; they are not adjudicated EXTRA totals.\n\nNext action: {s['next_file_batch']}\n\nThe read-only validator checks frozen input hashes and structural integrity; it does not prove semantic completeness. See VALIDATION_SNAPSHOTS for saved actual results. Search saturation has not been reached. All source and baseline inputs remain immutable; no reconciliation data has been accessed.\n"
save(O/'FINAL_REPORT.md',report)
print(json.dumps({'effective_candidates':len(effective),'unresolved':len(unresolved),'coverage':dict(cc),'status':'IN_PROGRESS'}))
