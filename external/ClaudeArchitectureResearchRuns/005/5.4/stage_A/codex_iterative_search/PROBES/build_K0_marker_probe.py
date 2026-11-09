"""Copy pure classifier/regex definitions only; never import or execute hooks."""
import json,hashlib,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent.parent;R=O.parent.parent
source=R/'inputs/K0/output/template/.claude/hooks/hook.cjs'
lines=source.read_text(encoding='utf-8-sig').splitlines()
p=O/'PROBES/K0_marker_probe.cjs';result=O/'PROBES/K0_marker_probe.result.json'
assert not p.exists() and not result.exists()
harness=r'''
const cases = [
 {kind:'dependency', command:'npm install example-package --cache "# add-dependency: reviewed"'},
 {kind:'reference', command:'dotnet add reference "dir/# project-references: approved/Other.csproj"'},
];
const results = cases.map(c => ({...c, classification:classifyCommand(c.command), markerMatches:(c.kind==='dependency'?DEPENDENCY_MARKER:REFERENCE_MARKER).test(c.command), markerInsideQuotedArgument:true}));
console.log(JSON.stringify({pureClassifierOnly:true,commandsExecuted:false,results}, null, 2));
'''
p.write_text('// Pure copied definitions from K0 hook lines 18..19 and 72..275. No entry point or filesystem operations.\n'+'\n'.join(lines[17:19]+lines[71:275])+'\n'+harness,encoding='utf-8')
run=subprocess.run(['node',str(p)],capture_output=True,text=True,check=True)
v=json.loads(run.stdout);v['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest();v['copied_source_ranges']=[[18,19],[72,275]]
result.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
state=O/'STATE.json';s=json.loads(state.read_text(encoding='utf-8'));s['completed_units'].append({'unit':'P0001-K0-MARKER-PROBE','outputs':{x.relative_to(O).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,result]}})
t=state.with_suffix('.json.tmp');t.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8');t.replace(state)
print(json.dumps(v,indent=2))
