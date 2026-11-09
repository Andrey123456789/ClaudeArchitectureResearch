// Pure expressions copied from frozen M source; no imports/execution of candidate hooks.
// These probes verify lexical predicates, not Claude Code or MSBuild runtime behavior.
import assert from 'node:assert/strict';
const observations=[];
const event='PostToolUse';
const recognizes=(source)=>!/\.hook_event_name\b/.test(source)||new RegExp(`===\\s*'${event}'`).test(source);
assert.equal(recognizes("const event=input.hook_event_name; if(event === 'PostToolUse') {}"),true);
assert.equal(recognizes('const event=input.hook_event_name; if(event === "PostToolUse") {}'),false);
observations.push({probe:'event_literal_quotes',result:'single quoted comparison accepted; equivalent double quoted comparison rejected',source:'output/template/.claude/scripts/check-instructions.mjs:302'});
const tools=['Bash','PowerShell'];const script='dependency-guard.mjs';
const required=(groups)=>groups.some((group)=>{
 const matcher=typeof group?.matcher==='string'&&!['','*'].includes(group.matcher)?group.matcher.split('|'):null;
 return tools.every((tool)=>!matcher||matcher.includes(tool))&&(group.hooks??[]).some((hook)=>hook?.args?.[0]===`\${CLAUDE_PROJECT_DIR}/.claude/hooks/${script}`);
});
const hook={args:['${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs']};
assert.equal(required([{matcher:'Bash|PowerShell',hooks:[hook]}]),true);
assert.equal(required([{matcher:'Bash',hooks:[hook]},{matcher:'PowerShell',hooks:[hook]}]),false);
observations.push({probe:'same_group_requirement',result:'joint matcher accepted; split registrations covering both tools rejected',source:'output/template/.claude/scripts/check-instructions.mjs:318-327'});
const relativeAccepted=(rel)=>!(!rel||rel.startsWith('..'));
assert.equal(relativeAccepted('..cache/package.json'),false);assert.equal(relativeAccepted('cache/package.json'),true);
observations.push({probe:'relative_double_dot_prefix',result:'in-root relative name ..cache/package.json rejected by lexical predicate',source:'output/template/.claude/hooks/hook-io.mjs:101',limitation:'Canonical resolution and callers not executed'});
const statusFailed=null;const state={baseline:true,head:'a'.repeat(40)};let snapshot=!state.baseline;let head=null;
const fields=(statusFailed??'').split('\0');
assert.deepEqual(fields,['']);assert.equal(snapshot,false);assert.equal(Boolean(head&&state.head&&state.head!==head),false);
observations.push({probe:'status_failure_after_baseline',result:'empty fields; no changed-head branch; snapshot remains false',source:'output/template/.claude/hooks/hook-io.mjs:149-173',limitation:'Git and manifest discovery not executed'});
console.log(JSON.stringify({status:'PASS_PURE_PREDICATES_ONLY',candidate:'M',observations,candidate_hooks_executed:false},null,2));
