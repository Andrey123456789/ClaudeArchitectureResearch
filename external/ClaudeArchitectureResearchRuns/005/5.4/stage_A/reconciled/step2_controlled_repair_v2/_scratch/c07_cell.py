from rcommon import CANDIDATES, out_path, read_jsonl, utf8_stdout
utf8_stdout()
cov={(x['candidate'],x['policy_id']):x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
for c in CANDIDATES:
    x=cov[(c,'DEP-024')]; print(c,'DEP-024',x.get('coverage_status') or x.get('status'),x['strength_status'],'direct',x['direct_source_keys'][:3],'stronger',x.get('stronger_source_keys'))
