"""Append metadata-only corrections; preserve committed research records."""
import json, hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
def save(p,v):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');t.replace(p)
s=json.loads((O/'STATE.json').read_text(encoding='utf-8'))
unit='P0001-L1-OPTIONS-POLICY-CORRECTION'
assert not any(u['unit']==unit for u in s['completed_units'])
outputs={}
for fid in ['CIS-L1-U0008','CIS-L1-U0009','CIS-L1-U0010']:
 p=O/'REVISIONS'/f'{fid}-R1.json'
 assert not p.exists()
 rev={'revision_id':fid+'-R1','finding_id':fid,'discovery_pass':1,'previous_status':'UNCERTAIN_NOVELTY','effective_status':'UNCERTAIN_NOVELTY','baseline_keys':['replica/L1/constraints.jsonl/RULE-L1-0062'],'reason':'Metadata correction: the verified typed-options policy is RUN-022. RUN-014 was a mistaken reference, not evidence for the claim. Source, uncertainty and novelty judgment are unchanged.','field_updates':{'closest_policy_ids':['RUN-022']},'count_as_distinct_discovery':False}
 save(p,rev);outputs[p.relative_to(O).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 s.setdefault('finding_revisions',{})[fid]={'effective_status':'UNCERTAIN_NOVELTY','revision':p.relative_to(O).as_posix(),'field_updates':rev['field_updates'],'count_as_distinct_discovery':False}
s['completed_units'].append({'unit':unit,'outputs':outputs});save(O/'STATE.json',s)
with (O/'SEARCH_DECISION_LOG.md').open('a',encoding='utf-8') as f:f.write('\nOptions-selection metadata correction: CIS-L1-U0008..0010 link to RUN-022, as verified in replica RULE-L1-0062; the original mistaken RUN-014 reference is superseded by immutable revisions. No source or classification changed.\n')
print(unit)
