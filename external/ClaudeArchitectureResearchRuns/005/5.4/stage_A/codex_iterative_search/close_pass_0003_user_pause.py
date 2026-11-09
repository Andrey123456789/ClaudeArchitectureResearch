"""Finalize only Pass 0003 and the user-directed pause. Never initialize a later pass."""
import json,hashlib,subprocess,sys
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent
C=['M','M1','L0','L1','K0','K1']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');t.replace(p)
def write(p,text):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(text,encoding='utf-8');t.replace(p)
def validate():
 p=subprocess.run([sys.executable,str(O/'VALIDATE_ITERATIVE_SEARCH.py')],capture_output=True,text=True,encoding='utf-8')
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 v=json.loads(p.stdout);assert v['status']=='PASS_STRUCTURAL_ONLY' and not v['errors'];return v
s=read(O/'STATE.json');d=O/'PASSES/pass_0003'
assert s['current_pass_id']==3 and s['last_completed_pass']==2 and s['user_directed_stop_after_pass']==3
assert not (d/'PASS_VALIDATION.json').exists()
# Frozen baseline/input hashes, exact quotes, completed-unit hashes, receipt history and semantic-reference keys.
validation=validate()
src=jl(O/'SOURCE_FILE_INDEX.jsonl');cov=jl(d/'FILE_COVERAGE.jsonl');claims=jl(d/'CANDIDATE_CLAIMS.jsonl');cmps=jl(d/'NOVELTY_COMPARISONS.jsonl')
assert len(cov)==len(src)==448
assert {(x['candidate'],x['path']) for x in cov}=={(x['candidate'],x['path']) for x in src}
assert len(claims)==len(cmps) and {x['id'] for x in claims}=={x['claim_id'] for x in cmps}
base={x['index_key']:x for x in jl(O/'BASELINE_RECORD_INDEX.jsonl')}
for row in cov:
 for k in ['read_index_status','inspected_ranges','hotspots','deferred_deeper_reread','review_notes']:assert k in row,(row['path'],k)
 assert row['read_index_status'] and row['review_notes']
for x in claims:
 for k in ['actor','trigger','modality','domain','exceptions','enforcement_effect','closest_policy_ids','baseline_comparisons','comparison_reason','distinguishing_behavioral_scenario','confidence','status','open_question','next_evidence_strategy']:
  assert k in x,(x['id'],k)
 runs={base[k]['run'] for comp in x['baseline_comparisons'] for k in comp['baseline_keys']}
 assert runs=={'primary','replica','independent'},(x['id'],runs)
 assert all(base[k]['candidate']==x['candidate'] for comp in x['baseline_comparisons'] for k in comp['baseline_keys'])
counts={}
for c in C:
 assert any(u['unit']==f'P0003-{c}-COMPLETE' for u in s['completed_units'])
 checkpoint=read(d/(c+'_CANDIDATE_CHECKPOINT.json'))
 cc=[x for x in cov if x['candidate']==c];fc=[x for x in claims if x['candidate']==c]
 assert checkpoint['source_files']==len(cc)==s['counts']['source_files'][c]
 assert checkpoint['coverage']==cc and set(checkpoint['claim_ids'])=={x['id'] for x in fc}
 counts[c]=dict(Counter(s.get('finding_revisions',{}).get(x['id'],{}).get('effective_status',x['comparison_status']) for x in fc))
new=sum(x.get('NOVEL_CLAUSE',0)+x.get('RECLASSIFICATION_CANDIDATE',0) for x in counts.values())
unc=sum(x.get('UNCERTAIN_NOVELTY',0) for x in counts.values())
assert new==0 and unc==148
revisions={x['id']:s['finding_revisions'][x['id']] for x in claims if x['id'] in s.get('finding_revisions',{})}
# Check effective canonical references without changing original append-only findings.
for c in C:
 root=O.parent.parent/'inputs'/c/'source'
 inv=read(root/'inventory.json');valid={p['id'] for g in inv['policygroups'] for p in g['policies']}
 valid.update(p['id'] for p in read(root/'shared-research-invariants.json')['invariants'])
 for x in claims:
  if x['candidate']!=c:continue
  eff={**x,**revisions.get(x['id'],{}).get('field_updates',{})}
  assert set(eff['closest_policy_ids'])<=valid,(x['id'],eff['closest_policy_ids'])
record=dict(status='COMPLETE',pass_id=3,strategy_family=3,strategy='ORPHAN_NON_NORMATIVE_CHALLENGE',baseline_fingerprint=s['baseline_fingerprint'],source_files=448,new_distinct_claims=new,new_plausible_unresolved=unc,effective_counts_by_candidate=counts,structural_validation_before_close=validation,full_pass_checks=dict(all_six_candidates_complete=True,full_source_file_accounting=True,candidate_checkpoint_reconciliation=True,exact_source_quotes_verified=True,same_candidate_all_three_baseline_references_verified=True,append_only_receipts_and_revisions_verified=True,effective_policy_references_valid=True,semantic_judgments_recorded=True),applied_finding_revisions=revisions,semantic_completeness_proven=False,original_convergence_protocol_completed=False,next_pass_started=False,termination='USER_DIRECTED_PAUSE_AFTER_PASS_0003',limits=['Structural validation verifies evidence and accounting, not semantic completeness.','All 148 new records remain unresolved hypotheses, not verified novel clauses or proven EXTRA.','Only strategy families 1, 2 and 3 have been completed. No six-strategy convergence or saturation claim.','No candidate hooks were executed and no reconciliation output was read.'])
report='# Pass 0003 — Orphan / non-normative challenge\n\nCOMPLETE AND VALIDATED. Frozen after review of all six candidates and all 448 active source files. Candidate order: L0, M, K1, M1, L1, K0. The user directed a pause immediately after this third pass; Pass 0004 was not initialized or started.\n\nThe pass independently challenged previously NON_NORMATIVE, IMPLEMENTATION, ORACLE_LINKED and unregistered contexts, including procedures in knowledge/reference files and code branches. Source-first readings and file-level notes are preserved in FILE_COVERAGE.jsonl and batch receipts. Candidate claims were compared semantically against the same-candidate union of all three frozen baselines, including composite and uncertain records. Existing classifications were not treated as truth.\n\n| Candidate | Files reviewed | New verified clauses | New unresolved hypotheses |\n|---|---:|---:|---:|\n'
for c in C:report+=f"| {c} | {s['counts']['source_files'][c]} | {counts[c].get('NOVEL_CLAUSE',0)+counts[c].get('RECLASSIFICATION_CANDIDATE',0)} | {counts[c].get('UNCERTAIN_NOVELTY',0)} |\n"
report+='| **Total** | **448/448** | **0** | **148** |\n\nAll new hypotheses have exact source quotations, explicit trigger/modality/domain, a distinguishing scenario, and comparisons naming records from all three prior runs. These are source-verified quotations, not verified normative novelty. Typical open questions concern optional error fields, conditional technique selections, configuration and logging tables, security-inspection subduties, and configured hook budgets. General prior records may already subsume some narrow actions, and descriptive or illustrative passages may not impose independent obligations.\n\nConservative deduplication examples: K0 replica0169 already states the two-to-three Decision Request options including keeping the current decision; K0 primary0541 already specifies CreatedAtAction/CreatedAtRoute; K0 BF0042 explicitly records audit/log-storage defaults, so those rows were not rediscovered solely because its claim is composite. Bodyless304, AAA comment permission, selective private-reference loading, and previously retained local-account review duties were not counted again. Candidate-specific differences in this review are not evidence of cross-candidate parity differences.\n\nPre-close validation checked all 933 immutable input/baseline hashes, the 33987-record baseline index, exact quotations, stable IDs, all completed output hashes, append-only batch receipts, global/pass consistency and prior frozen pass hashes. Additional full-pass checks reconciled all six candidate checkpoints, 448 file entries, 148 claims and comparisons, three-baseline references and effective canonical links. Twelve K0 closest-policy metadata corrections are preserved as append-only revisions; original records remain unchanged. CHECKPOINT_HASHES.json freezes all files in this pass. A final read-only closure check is saved in VALIDATION_SNAPSHOTS/P0003-FROZEN.json.\n\nThis is a nonzero-discovery pass because 148 plausible unresolved hypotheses were surfaced. The original minimum-six-strategy and two-consecutive-different-zero-pass protocol has NOT been completed. Search saturation and semantic completeness are NOT claimed. The remaining research is intentionally paused by the user; no subsequent pass is authorized. No sources, earlier findings or reconciliation outputs were modified.\n'
write(d/'PASS_REPORT.md',report);save(d/'PASS_VALIDATION.json',record)
save(d/'CHECKPOINT_HASHES.json',{p.name:sha(p) for p in sorted(d.iterdir()) if p.is_file() and p.name!='CHECKPOINT_HASHES.json'})
s['completed_units'].append(dict(unit='P0003-COMPLETE',outputs={'PASSES/pass_0003/CHECKPOINT_HASHES.json':sha(d/'CHECKPOINT_HASHES.json')}))
s['convergence_history'].append({k:record[k] for k in ['pass_id','strategy_family','new_distinct_claims','new_plausible_unresolved','baseline_fingerprint']})
s.update(last_completed_pass=3,current_pass_id=3,current_strategy='ORPHAN_NON_NORMATIVE_CHALLENGE',candidate=None,next_file_batch='STOP. User-directed pause after validated Pass 0003. No Pass 0004 work is authorized.',current_candidate_findings=[],final_status='PAUSED_BY_USER',original_convergence_protocol_completed=False,pass_0004_started=False,scheduled_task=dict(id='run-iterative-clause-search',status='PAUSED',observed_source='Existing automation.toml; read-only schedule check before closure',note='Already paused. Preserve this status after successful completion.'))
s['pause_checkpoint']=dict(pass_id=3,files_reviewed=448,total_files=448,new_verified_findings=0,new_unresolved_hypotheses=148,report='PASSES/pass_0003/PASS_REPORT.md',validation='PASSES/pass_0003/PASS_VALIDATION.json')
save(O/'STATE.json',s)
resume='''# Resume: Experiment 005 / Phase 5.4 — PAUSED BY USER

Authoritative search specification: `_STAGE_A_KIT/21_CODEX_ITERATIVE_SEARCH_TASK_EN.md`, with the later explicit user directive overriding automatic continuation: complete Pass 0003 and STOP before Pass 0004.

State truth: STATE.json. Passes 0001, 0002 and 0003 are complete and frozen. Pass 0003 reviewed 448/448 source files across M 61, M1 80, L0 71, L1 86, K0 63 and K1 87; it added 0 verified new clauses and 148 unresolved hypotheses. No unfinished unit remains within Pass 0003. Pass 0004 has NOT been initialized, inspected, planned in detail or executed.

Next ONE action: STOP. Preserve the user-directed pause. A scheduled heartbeat or old automatic-continuation instruction does not authorize another pass. Resume research only after a fresh explicit user directive changes this pause.

Read boundaries for any authorized recovery: immutable inputs/**; stage_A/primary/**, stage_A/replica/**, stage_A/independent/**; this specification and this output subtree. NEVER read, modify, or wait for stage_A/reconciled/step1_union/**. Write ONLY stage_A/codex_iterative_search/**. Never execute candidate hooks. Protected source and baseline files, earlier findings and completed pass artifacts stay unchanged.

Final Pass 0003 artifacts: PASSES/pass_0003/PASS_REPORT.md, PASS_VALIDATION.json and CHECKPOINT_HASHES.json. Closure validation: VALIDATION_SNAPSHOTS/P0003-FROZEN.json. Reviewer snapshot: HANDOFF_TO_CLAUDE.md and FINAL_REPORT.md. Apply STATE.json finding_revisions / REVISIONS before interpreting effective metadata; original claims remain append-only.

Validation command: python stage_A/codex_iterative_search/VALIDATE_ITERATIVE_SEARCH.py
Accepted evidence schema: specification section 4; UTF-8 JSONL, candidate-relative source paths, stable IDs, exact quotations with newline normalization only, actor/action/trigger/modality/domain/exceptions, semantic baseline comparisons, distinguishing scenarios and open questions. Never count a hypothesis as proven EXTRA or a cross-candidate difference.

Only three of the six required strategy families were completed. The original convergence and final unattributed-review protocol is unfinished; no saturation or semantic completeness is claimed. The stop is intentional, not a convergence result or quota block. No automatic restart is promised. The existing scheduled task was observed PAUSED and must remain paused.
'''
write(O/'RESUME.md',resume)
novel=jl(O/'NOVEL_FINDINGS.jsonl');unresolved=jl(O/'UNRESOLVED_FINDINGS.jsonl');effective=[x for x in novel if s.get('finding_revisions',{}).get(x['id'],{}).get('effective_status',x['comparison_status']) in ['NOVEL_CLAUSE','RECLASSIFICATION_CANDIDATE']]
summary='# Iterative search — user-directed pause after Pass 0003\n\nThree full passes are complete and frozen. Pass 0003 reviewed all 448 source files and recorded 0 verified new clauses plus 148 unresolved hypotheses. The original six-strategy convergence protocol remains incomplete; search saturation and semantic completeness are not claimed. Pass 0004 was not started.\n\n| Pass | Strategy family | Files | New verified | New unresolved |\n|---|---|---:|---:|---:|\n| 0001 | Reverse normative-clause sweep | 448 | 59 effective | 72 |\n| 0002 | Canonical-policy boundary sweep | 448 | 0 | 63 |\n| 0003 | Orphan / non-normative challenge | 448 | 0 | 148 |\n\n'
summary+=f'Cumulative queues: {len(novel)} original novel/reclassification records, {len(effective)} effective after revisions, and {len(unresolved)} unresolved hypotheses. CIS-M1-0004 remains withdrawn as already covered; all originals and revisions are preserved. These are extraction-relative candidates, not adjudicated EXTRA findings.\n\n'
summary+='Validation checked the 933 frozen files, baseline fingerprint, 33987 indexed baseline records, quotes, IDs, references, receipts and completed hashes. See PASSES/pass_0003/PASS_VALIDATION.json and VALIDATION_SNAPSHOTS/P0003-FROZEN.json. Structural PASS is evidence of accounting and provenance, not proof of complete semantic extraction. All research changes remain inside this output subtree; no reconciliation output was accessed.\n\nThe user explicitly required STOP after Pass 0003. STATE.json and RESUME.md record PAUSED_BY_USER. The existing run-iterative-clause-search schedule was observed PAUSED.\n'
write(O/'FINAL_REPORT.md',summary)
handoff='# Handoff snapshot — paused after Pass 0003\n\nThe user intentionally stopped this independent search after three completed full passes. All 448 files were accounted for in each pass. Pass 0003 adds 148 unresolved hypotheses and no verified new clauses. The original six-strategy convergence protocol is incomplete; this is not saturation. Pass 0004 was not started.\n\nReview NOVEL_FINDINGS.jsonl and UNRESOLVED_FINDINGS.jsonl against exact inputs and same-candidate baseline keys in BASELINE_RECORD_INDEX.jsonl. Apply STATE.json finding_revisions and their REVISIONS files first. CIS-M1-0004 is withdrawn as already covered; do not import its original status. Twelve Pass 0003 K0 metadata corrections do not alter source quotations, claims or counts. No reconciliation file was read or changed; any later import is a separate adjudication task.\n\nNew records may overlap broad prior claims, or describe illustrative techniques and permissions rather than independent duties. Read trigger, exceptions, counter-scenario and comparison reasons; do not convert uncertainty into proven EXTRA or a parity difference. No runtime behavior was proved by executing candidate hooks.\n\n'
handoff+='## Effective novel/reclassification queue from completed passes\n\n'
for x in effective:handoff+=f"- **{x['id']}** ({x['comparison_status']}): {x['claim']} Evidence: `inputs/{x['candidate']}/{x['path']}:{x['start_line']}-{x['end_line']}`.\n"
handoff+='\n## Preserved unresolved queue\n\n'
for x in unresolved:handoff+=f"- **{x['id']}**, pass {x['discovery_pass']}: {x['claim']} Open question: {x.get('open_question','See record.')} Evidence: `inputs/{x['candidate']}/{x['path']}:{x['start_line']}-{x['end_line']}`.\n"
write(O/'HANDOFF_TO_CLAUDE.md',handoff)
with (O/'SEARCH_DECISION_LOG.md').open('a',encoding='utf-8') as f:f.write('\n## Pass 0003 closure — user-directed pause\nAll six candidate checkpoints and 448 file entries reconciled; 0 verified new clauses and 148 newly surfaced unresolved hypotheses. Three-baseline references, exact quotes, immutable fingerprint and append-only receipts validated. Pass0003 frozen. No Pass0004 initialization or work. Original convergence protocol explicitly incomplete. Scheduled task observed PAUSED.\n')
# Final required validation of the frozen pass; no further exploratory work follows success.
post=validate();assert post['checks']['completed_passes']==3 and post['checks']['source_files']==448
snap=O/'VALIDATION_SNAPSHOTS/P0003-FROZEN.json';assert not snap.exists();save(snap,post)
s=read(O/'STATE.json');s['completed_units'].append(dict(unit='P0003-FROZEN-VALIDATION',outputs={snap.relative_to(O).as_posix():sha(snap)}));s['last_validation']=dict(status=post['status'],snapshot=snap.relative_to(O).as_posix(),completed_passes=3);save(O/'STATE.json',s)
# Verify the final pause/checkpoint write without redoing the full search or touching any later pass.
assert read(O/'STATE.json')['final_status']=='PAUSED_BY_USER'
assert sha(snap)==s['completed_units'][-1]['outputs'][snap.relative_to(O).as_posix()]
print(json.dumps(dict(closed_pass=3,status='COMPLETE_AND_VALIDATED',files_reviewed=448,new_verified=0,new_unresolved=148,final_status='PAUSED_BY_USER',pass_0004_started=False,validation=post),indent=2))
