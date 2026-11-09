import json,shutil
from sandbox import PRE_TOOL, fresh_copy, run_node
from rcommon import CANDIDATES, utf8_stdout
utf8_stdout()
for c in CANDIDATES:
    root=fresh_copy(c,'c06p')
    for name,payload in (('malformed','not json at all'),('empty',''),('no command',json.dumps({'hook_event_name':'PreToolUse','tool_name':'Bash','tool_input':{},'cwd':root})),('empty command',json.dumps({'hook_event_name':'PreToolUse','tool_name':'Bash','tool_input':{'command':''},'cwd':root})),('other field',json.dumps({'hook_event_name':'PreToolUse','tool_name':'Bash','tool_input':{'cmd':'npm install left-pad'},'cwd':root}))):
        code,out,err=run_node(root,PRE_TOOL[c],payload)
        print(c,name,'exit',code,'|',(out+err).strip().replace('\n',' ')[:150])
    shutil.rmtree(root,ignore_errors=True)
