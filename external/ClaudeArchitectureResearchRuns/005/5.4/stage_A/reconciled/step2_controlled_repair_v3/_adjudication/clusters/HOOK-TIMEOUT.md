# HOOK-TIMEOUT (14 records)

## CIS-M-U0031 (pass 2) M .claude/hooks/hook-io.mjs:213-218  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The helper for manifest-state Git status/diff queries configures execFileSync timeout=15000 and converts a thrown execution error to null.
TRIGGER: Executing manifest-state Git status/diff queries | EXC: Only these helper calls, not every Git command; no claim that all child processes are guaranteed to terminate at precisely 15 seconds. | POL: []
CODEX WHY: A finite helper budget is source-grounded, separate from the host advisory-hook budget and broad product external-I/O guidance. Normative significance versus implementation safeguard remains unresolved.
```
 210    return line.slice(at);
 211  }
 212  
 213> function gitOutput(cwd, args) {
 214>   try {
 215>     return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 15000, windowsHide: true });
 216>   } catch {
 217>     return null;
 218>   }
 219  }
 220  
 221  function manifestStatePath(repo) {
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0019 -> FG-M-15220a3812 [NON_NORMATIVE] Hook state is persisted in an override directory, the Git directory or a temp folder, and failure to persist it is swallowed.

## CIS-M-U0032 (pass 2) M .claude/scripts/repo-root.mjs:110-122  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The helper for repository-root Git work-tree/common-dir queries configures execFileSync timeout=15000 and converts a thrown execution error to null.
TRIGGER: Executing repository-root Git work-tree/common-dir queries | EXC: Only these helper calls, not every Git command; no claim that all child processes are guaranteed to terminate at precisely 15 seconds. | POL: []
CODEX WHY: A finite helper budget is source-grounded, separate from the host advisory-hook budget and broad product external-I/O guidance. Normative significance versus implementation safeguard remains unresolved.
```
 107    return common ? canonical(resolve(top, common)) : null;
 108  }
 109  
 110> function git(cwd, args) {
 111>   try {
 112>     const output = execFileSync('git', args, {
 113>       cwd,
 114>       encoding: 'utf8',
 115>       stdio: ['ignore', 'pipe', 'ignore'],
 116>       timeout: 15000,
 117>       windowsHide: true,
 118>     });
 119>     return output.trim() || null;
 120>   } catch {
 121>     return null; // Git missing, not a working tree, or an unusable repository
 122>   }
 123  }
 124  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0022 -> FG-M-85f08867c3 [NON_NORMATIVE] Repository-root resolution scopes checks through the common Git directory and template offset; nested unrelated repositories inside the template resolve to the template root.

## CIS-M-U0027 (pass 2) M .claude/settings.json:11-15  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUse for Bash or PowerShell registration of dependency-guard.mjs configures timeout=60.
TRIGGER: PostToolUse for Bash or PowerShell | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
   8          ]
   9        }
  10      ],
  11>     "PostToolUse": [
  12>       {
  13>         "matcher": "Bash|PowerShell",
  14>         "hooks": [
  15>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 60 }
  16          ]
  17        },
  18        {
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-80646b7ff3 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Hooks are registered in exec form (node plus the script path anchored at CLAUDE_PROJECT_DIR, no shell).
- V2 FG-M-e42de1aa43 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: The dependency guard is registered for PostToolUseFailure.
- V2 FG-M-ddd9d93ab6 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=['DEP-025']: PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED primary/M/constraints.jsonl/RULE-M-0227 -> FG-M-d05bc59108 [CANONICAL_ONLY] dependency-guard.mjs runs as a PreToolUse hook on every Bash/PowerShell call (timeout 30 s) to block npm peer-dependency bypass flags.
- NAMED primary/M/constraints.jsonl/EXTRA-M-0041 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED replica/M/constraints.jsonl/EXTRA-M-0006 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0012 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0028 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- PASS1 CIS-P0001-M-C0004 ALREADY_REPRESENTED [3, 9]: PreToolUse Bash/PowerShell guard has a 30-second timeout with block-on-failure.

## CIS-M-U0028 (pass 2) M .claude/settings.json:18-21  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUse for Edit, Write or MultiEdit registration of file-change.mjs configures timeout=60.
TRIGGER: PostToolUse for Edit, Write or MultiEdit | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
  15            { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 60 }
  16          ]
  17        },
  18>       {
  19>         "matcher": "Edit|Write|MultiEdit",
  20>         "hooks": [
  21>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/file-change.mjs"], "timeout": 60 }
  22          ]
  23        }
  24      ],
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-80646b7ff3 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Hooks are registered in exec form (node plus the script path anchored at CLAUDE_PROJECT_DIR, no shell).
- V2 FG-M-e42de1aa43 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: The dependency guard is registered for PostToolUseFailure.
- V2 FG-M-ddd9d93ab6 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=['DEP-025']: PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED primary/M/constraints.jsonl/RULE-M-0227 -> FG-M-d05bc59108 [CANONICAL_ONLY] dependency-guard.mjs runs as a PreToolUse hook on every Bash/PowerShell call (timeout 30 s) to block npm peer-dependency bypass flags.
- NAMED primary/M/constraints.jsonl/EXTRA-M-0041 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED replica/M/constraints.jsonl/EXTRA-M-0006 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0012 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0028 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.

## CIS-M-U0029 (pass 2) M .claude/settings.json:25-29  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUseFailure for Bash or PowerShell registration of dependency-guard.mjs configures timeout=60.
TRIGGER: PostToolUseFailure for Bash or PowerShell | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
  22          ]
  23        }
  24      ],
  25>     "PostToolUseFailure": [
  26>       {
  27>         "matcher": "Bash|PowerShell",
  28>         "hooks": [
  29>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 60 }
  30          ]
  31        }
  32      ],
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-80646b7ff3 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Hooks are registered in exec form (node plus the script path anchored at CLAUDE_PROJECT_DIR, no shell).
- V2 FG-M-e42de1aa43 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: The dependency guard is registered for PostToolUseFailure.
- V2 FG-M-ddd9d93ab6 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=['DEP-025']: PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED primary/M/constraints.jsonl/RULE-M-0227 -> FG-M-d05bc59108 [CANONICAL_ONLY] dependency-guard.mjs runs as a PreToolUse hook on every Bash/PowerShell call (timeout 30 s) to block npm peer-dependency bypass flags.
- NAMED primary/M/constraints.jsonl/EXTRA-M-0041 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED replica/M/constraints.jsonl/EXTRA-M-0006 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0012 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0028 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.

## CIS-M-U0030 (pass 2) M .claude/settings.json:33-36  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The Stop registration of stop-co-change.mjs configures timeout=60.
TRIGGER: Stop | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
  30          ]
  31        }
  32      ],
  33>     "Stop": [
  34>       {
  35>         "hooks": [
  36>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/stop-co-change.mjs"], "timeout": 60 }
  37          ]
  38        }
  39      ]
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-80646b7ff3 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Hooks are registered in exec form (node plus the script path anchored at CLAUDE_PROJECT_DIR, no shell).
- V2 FG-M-e42de1aa43 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: The dependency guard is registered for PostToolUseFailure.
- V2 FG-M-ddd9d93ab6 [3, 39] INTERNAL_ARCHITECTURE/MUST pol=[] rel=['DEP-025']: PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED primary/M/constraints.jsonl/RULE-M-0227 -> FG-M-d05bc59108 [CANONICAL_ONLY] dependency-guard.mjs runs as a PreToolUse hook on every Bash/PowerShell call (timeout 30 s) to block npm peer-dependency bypass flags.
- NAMED primary/M/constraints.jsonl/EXTRA-M-0041 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED replica/M/constraints.jsonl/EXTRA-M-0006 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0012 -> FG-M-f268d4b313 [EXTRA_WORKFLOW] The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is bloc
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0028 -> FG-M-ddd9d93ab6 [INTERNAL_ARCHITECTURE] PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.

## CIS-L0-U0028 (pass 3) L0 .claude/settings.json:11-15  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUse for Bash or PowerShell registration of claude-hook.mjs post-bash configures timeout=60.
TRIGGER: PostToolUse for Bash or PowerShell | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
   8          ]
   9        }
  10      ],
  11>     "PostToolUse": [
  12>       {
  13>         "matcher": "Bash|PowerShell",
  14>         "hooks": [
  15>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-bash"], "timeout": 60 }
  16          ]
  17        },
  18        {
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-5d2fbbf043 [15, 15] CANONICAL_ONLY/SHOULD pol=['DEP-006', 'DEP-003', 'DEP-007'] rel=[]: After successful and failed shell calls and after edits, added/changed manifests of the active worktree are validated with the manifest checks (first observation validates all; outside Git only after a recognized dependency comman
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0031 -> FG-L0-69195df14f [EXTRA_WORKFLOW] pre-bash fails closed: unreadable/malformed payload, missing command, unknown event or internal error exits 2 and blocks the shell call; settings.json adds onFailure block for laun
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0198 -> FG-L0-a9a5a79d44 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node, args [launcher placeholder, event]), a positive timeout and known handled events; PreToolUse/PostToolUse/PostToolUseFailure/Sto
- NAMED replica/L0/constraints.jsonl/EXTRA-L0-0007 -> FG-L0-5c6a0474f4 [INTERNAL_ARCHITECTURE] Hook registration form: hooks are registered in exec form (command node, args with the ${CLAUDE_PROJECT_DIR} placeholder, no shell); PreToolUse Bash|PowerShell runs pre-bash with o
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0034 -> FG-L0-29b2fd6409 [EXTRA_WORKFLOW] Bash/PowerShell calls run the pre-bash hook through node with a 30-second timeout and onFailure block (fail closed).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0112 -> FG-L0-385914fe20 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node with [launcher, event] args), a positive timeout, a literal handler map with known events and the required registrations; onFail

## CIS-L0-U0029 (pass 3) L0 .claude/settings.json:18-21  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUse for Edit, Write or MultiEdit registration of claude-hook.mjs post-edit configures timeout=60.
TRIGGER: PostToolUse for Edit, Write or MultiEdit | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
  15            { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-bash"], "timeout": 60 }
  16          ]
  17        },
  18>       {
  19>         "matcher": "Edit|MultiEdit|Write",
  20>         "hooks": [
  21>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-edit"], "timeout": 60 }
  22          ]
  23        }
  24      ],
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-5d2fbbf043 [21, 21] CANONICAL_ONLY/SHOULD pol=['DEP-006', 'DEP-003', 'DEP-007'] rel=[]: After successful and failed shell calls and after edits, added/changed manifests of the active worktree are validated with the manifest checks (first observation validates all; outside Git only after a recognized dependency comman
- V2 FG-L0-18eacd2f3a [21, 21] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: After editing CLAUDE.md or .claude/**/*.md|json|mjs (except settings.local), check-instructions runs and its errors are returned as feedback (template-maintenance); a missing checker is reported as unavailable.
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0031 -> FG-L0-69195df14f [EXTRA_WORKFLOW] pre-bash fails closed: unreadable/malformed payload, missing command, unknown event or internal error exits 2 and blocks the shell call; settings.json adds onFailure block for laun
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0198 -> FG-L0-a9a5a79d44 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node, args [launcher placeholder, event]), a positive timeout and known handled events; PreToolUse/PostToolUse/PostToolUseFailure/Sto
- NAMED replica/L0/constraints.jsonl/EXTRA-L0-0007 -> FG-L0-5c6a0474f4 [INTERNAL_ARCHITECTURE] Hook registration form: hooks are registered in exec form (command node, args with the ${CLAUDE_PROJECT_DIR} placeholder, no shell); PreToolUse Bash|PowerShell runs pre-bash with o
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0034 -> FG-L0-29b2fd6409 [EXTRA_WORKFLOW] Bash/PowerShell calls run the pre-bash hook through node with a 30-second timeout and onFailure block (fail closed).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0112 -> FG-L0-385914fe20 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node with [launcher, event] args), a positive timeout, a literal handler map with known events and the required registrations; onFail

## CIS-L0-U0030 (pass 3) L0 .claude/settings.json:25-29  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUseFailure for Bash or PowerShell registration of claude-hook.mjs post-bash configures timeout=60.
TRIGGER: PostToolUseFailure for Bash or PowerShell | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
  22          ]
  23        }
  24      ],
  25>     "PostToolUseFailure": [
  26>       {
  27>         "matcher": "Bash|PowerShell",
  28>         "hooks": [
  29>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-bash"], "timeout": 60 }
  30          ]
  31        }
  32      ],
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-5d2fbbf043 [29, 29] CANONICAL_ONLY/SHOULD pol=['DEP-006', 'DEP-003', 'DEP-007'] rel=[]: After successful and failed shell calls and after edits, added/changed manifests of the active worktree are validated with the manifest checks (first observation validates all; outside Git only after a recognized dependency comman
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0031 -> FG-L0-69195df14f [EXTRA_WORKFLOW] pre-bash fails closed: unreadable/malformed payload, missing command, unknown event or internal error exits 2 and blocks the shell call; settings.json adds onFailure block for laun
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0198 -> FG-L0-a9a5a79d44 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node, args [launcher placeholder, event]), a positive timeout and known handled events; PreToolUse/PostToolUse/PostToolUseFailure/Sto
- NAMED replica/L0/constraints.jsonl/EXTRA-L0-0007 -> FG-L0-5c6a0474f4 [INTERNAL_ARCHITECTURE] Hook registration form: hooks are registered in exec form (command node, args with the ${CLAUDE_PROJECT_DIR} placeholder, no shell); PreToolUse Bash|PowerShell runs pre-bash with o
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0034 -> FG-L0-29b2fd6409 [EXTRA_WORKFLOW] Bash/PowerShell calls run the pre-bash hook through node with a 30-second timeout and onFailure block (fail closed).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0112 -> FG-L0-385914fe20 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node with [launcher, event] args), a positive timeout, a literal handler map with known events and the required registrations; onFail

## CIS-L0-U0031 (pass 3) L0 .claude/settings.json:33-36  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The Stop registration of claude-hook.mjs stop configures timeout=60.
TRIGGER: Stop | EXC: Advisory hook; no onFailure:block. Host interpretation of timeout, units and termination behavior are not implemented in the allowed snapshot. | POL: []
CODEX WHY: Configured value and trigger are exact. Whether this is an independently effective constraint depends on host interpretation absent from the frozen evidence; preserve the hypothesis.
```
  30          ]
  31        }
  32      ],
  33>     "Stop": [
  34>       {
  35>         "hooks": [
  36>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "stop"], "timeout": 60 }
  37          ]
  38        }
  39      ]
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-51c4f99ca7 [36, 36] CANONICAL_ONLY/SHOULD pol=['PST-008'] rel=[]: At Stop, Domain/persistence model changes without a seeder change prompt confirming seeded entities are unaffected or updating the seeder.
- V2 FG-L0-04ac048096 [36, 36] CANONICAL_ONLY/SHOULD pol=['TST-009', 'TST-010'] rel=[]: At Stop, production backend/frontend code changes without any test change prompt confirming equivalent coverage or adding tests.
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0031 -> FG-L0-69195df14f [EXTRA_WORKFLOW] pre-bash fails closed: unreadable/malformed payload, missing command, unknown event or internal error exits 2 and blocks the shell call; settings.json adds onFailure block for laun
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0198 -> FG-L0-a9a5a79d44 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node, args [launcher placeholder, event]), a positive timeout and known handled events; PreToolUse/PostToolUse/PostToolUseFailure/Sto
- NAMED replica/L0/constraints.jsonl/EXTRA-L0-0007 -> FG-L0-5c6a0474f4 [INTERNAL_ARCHITECTURE] Hook registration form: hooks are registered in exec form (command node, args with the ${CLAUDE_PROJECT_DIR} placeholder, no shell); PreToolUse Bash|PowerShell runs pre-bash with o
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0034 -> FG-L0-29b2fd6409 [EXTRA_WORKFLOW] Bash/PowerShell calls run the pre-bash hook through node with a 30-second timeout and onFailure block (fail closed).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0112 -> FG-L0-385914fe20 [INTERNAL_ARCHITECTURE] Hook registrations must use exec form (command node with [launcher, event] args), a positive timeout, a literal handler map with known events and the required registrations; onFail

## CIS-L1-U0017 (pass 3) L1 .claude/settings.json:15-29  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUse edit/shell and PostToolUseFailure shell hook registrations configure a timeout value of 30.
TRIGGER: The registered PostToolUse edit/shell and PostToolUseFailure shell event invokes its checker | EXC: No onFailure block on these registrations; no observed host timeout or elapsed-time execution is asserted. Candidate scripts were not executed. | POL: []
CODEX WHY: Event-specific configured numeric limit differs from generic timeout presence and blocking pre-tool gate; independent normative significance and actual host effect remain uncertain.
```
  12        {
  13          "matcher": "Edit|Write|MultiEdit",
  14          "hooks": [
  15>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-change-checks.mjs"], "timeout": 30 }
  16>         ]
  17>       },
  18>       {
  19>         "matcher": "Bash|PowerShell",
  20>         "hooks": [
  21>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-change-checks.mjs"], "timeout": 30 }
  22>         ]
  23>       }
  24>     ],
  25>     "PostToolUseFailure": [
  26>       {
  27>         "matcher": "Bash|PowerShell",
  28>         "hooks": [
  29>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-change-checks.mjs"], "timeout": 30 }
  30          ]
  31        }
  32      ],
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-b6b14303cc [21, 21] CANONICAL_ONLY/SHOULD pol=['DEP-006', 'DEP-003', 'DEP-007'] rel=[]: After edits and after successful or failed shell calls the actual manifest state of the active worktree is validated (per-worktree snapshot; first observation validates all, later only added/changed/removed/moved manifests incl. H
- V2 FG-L1-b6b14303cc [29, 29] CANONICAL_ONLY/SHOULD pol=['DEP-006', 'DEP-003', 'DEP-007'] rel=[]: After edits and after successful or failed shell calls the actual manifest state of the active worktree is validated (per-worktree snapshot; first observation validates all, later only added/changed/removed/moved manifests incl. H
- V2 FG-L1-b6b14303cc [15, 15] CANONICAL_ONLY/SHOULD pol=['DEP-006', 'DEP-003', 'DEP-007'] rel=[]: After edits and after successful or failed shell calls the actual manifest state of the active worktree is validated (per-worktree snapshot; first observation validates all, later only added/changed/removed/moved manifests incl. H
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0067 -> FG-L1-ff84ccd35a [INTERNAL_ARCHITECTURE] Hooks must be exec form (bare command, args with the ${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs launcher, no expansion), have numeric timeouts; only PreToolUse sets onFailure
- NAMED replica/L1/constraints.jsonl/EXTRA-L1-0014 -> FG-L1-d395ecdcdc [INTERNAL_ARCHITECTURE] Hooks are registered in exec form (command node with the script path as argument data, no shell); the critical PreToolUse gate sets onFailure block so a missing script, crash, time
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0076 -> FG-L1-ff84ccd35a [INTERNAL_ARCHITECTURE] Hooks must be exec form (bare command, args with the ${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs launcher, no expansion), have numeric timeouts; only PreToolUse sets onFailure
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0078 -> FG-L1-a73c9ece78 [EXTRA_WORKFLOW] Bash/PowerShell calls run the pre-shell hook through node with a 15-second timeout and onFailure block (fail closed).

## CIS-L1-U0018 (pass 3) L1 .claude/settings.json:36-36  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The Stop co-change hook registrations configure a timeout value of 15.
TRIGGER: The registered Stop co-change event invokes its checker | EXC: No onFailure block on these registrations; no observed host timeout or elapsed-time execution is asserted. Candidate scripts were not executed. | POL: []
CODEX WHY: Event-specific configured numeric limit differs from generic timeout presence and blocking pre-tool gate; independent normative significance and actual host effect remain uncertain.
```
  33      "Stop": [
  34        {
  35          "hooks": [
  36>           { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/stop-cochange.mjs"], "timeout": 15 }
  37          ]
  38        }
  39      ]
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-3b25c1f9c9 [36, 36] CANONICAL_ONLY/SHOULD pol=['PST-008'] rel=[]: At Stop, Domain/persistence model changes without a seeder change prompt confirming seeded entities are unaffected or updating the seeder.
- V2 FG-L1-674df3dc2f [36, 36] CANONICAL_ONLY/SHOULD pol=['TST-009', 'TST-010'] rel=[]: At Stop, backend production code changes without test changes prompt confirming coverage, regression tests and probe preservation.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0067 -> FG-L1-ff84ccd35a [INTERNAL_ARCHITECTURE] Hooks must be exec form (bare command, args with the ${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs launcher, no expansion), have numeric timeouts; only PreToolUse sets onFailure
- NAMED replica/L1/constraints.jsonl/EXTRA-L1-0014 -> FG-L1-d395ecdcdc [INTERNAL_ARCHITECTURE] Hooks are registered in exec form (command node with the script path as argument data, no shell); the critical PreToolUse gate sets onFailure block so a missing script, crash, time
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0076 -> FG-L1-ff84ccd35a [INTERNAL_ARCHITECTURE] Hooks must be exec form (bare command, args with the ${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs launcher, no expansion), have numeric timeouts; only PreToolUse sets onFailure
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0078 -> FG-L1-a73c9ece78 [EXTRA_WORKFLOW] Bash/PowerShell calls run the pre-shell hook through node with a 15-second timeout and onFailure block (fail closed).

## CIS-K0-U0027 (pass 3) K0 .claude/settings.json:25-49  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The PostToolUse edit/shell and PostToolUseFailure shell hook registrations configure a timeout value of 60.
TRIGGER: PostToolUse edit/shell and PostToolUseFailure shell event invokes hook.cjs | EXC: No onFailure:block on these registrations; exact timeout unit and runtime handling not asserted. | POL: []
CODEX WHY: Potential numeric event limit not equivalent to presence of a positive timeout or pre-gate duration. Normative significance and frozen host contract remain open.
```
  22              "type": "command",
  23              "command": "node",
  24              "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "post-tool-use"],
  25>             "timeout": 60
  26>           }
  27>         ]
  28>       },
  29>       {
  30>         "matcher": "Bash|PowerShell",
  31>         "hooks": [
  32>           {
  33>             "type": "command",
  34>             "command": "node",
  35>             "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "post-tool-use"],
  36>             "timeout": 60
  37>           }
  38>         ]
  39>       }
  40>     ],
  41>     "PostToolUseFailure": [
  42>       {
  43>         "matcher": "Bash|PowerShell",
  44>         "hooks": [
  45>           {
  46>             "type": "command",
  47>             "command": "node",
  48>             "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "post-tool-use-failure"],
  49>             "timeout": 60
  50            }
  51          ]
  52        }
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0042 -> FG-K0-2e9713cb57 [INTERNAL_ARCHITECTURE] settings.json hooks are exec-form command hooks (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>], existing script handling the event, no varia
- NAMED replica/K0/constraints.jsonl/EXTRA-K0-0017 -> FG-K0-a39d75cc3a [INTERNAL_ARCHITECTURE] Hook configuration: every hook is a command hook in exec form (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>] with the script present and han
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0129 -> FG-K0-55a87d9705 [INTERNAL_ARCHITECTURE] settings.json hooks must be exec-form command hooks with a fixed script/event structure and a positive timeout; the required registrations must exist and the PreToolUse policy hook
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0132 -> FG-K0-dad9dffcde [EXTRA_WORKFLOW] Every Bash/PowerShell call runs through a Node command hook with a 30-second timeout and fail-closed onFailure (reported dependency on Node).

## CIS-K0-U0028 (pass 3) K0 .claude/settings.json:61-61  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The Stop hook registrations configure a timeout value of 60.
TRIGGER: Stop event invokes hook.cjs | EXC: No onFailure:block on these registrations; exact timeout unit and runtime handling not asserted. | POL: []
CODEX WHY: Potential numeric event limit not equivalent to presence of a positive timeout or pre-gate duration. Normative significance and frozen host contract remain open.
```
  58              "type": "command",
  59              "command": "node",
  60              "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "stop"],
  61>             "timeout": 60
  62            }
  63          ]
  64        }
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-28c2ddca25 [54, 65] CANONICAL_ONLY/SHOULD pol=['GOV-021'] rel=[]: At Stop a CUSTOM_SETTINGS.md change triggers a reminder to confirm the synchronization.
- V2 FG-K0-c150fa04bb [54, 65] CANONICAL_ONLY/SHOULD pol=['GOV-021'] rel=[]: A CUSTOM_SETTINGS.md change triggers the instruction to run the custom-settings workflow to synchronize every affected surface.
- V2 FG-K0-17c78607b6 [54, 65] CANONICAL_ONLY/SHOULD pol=['PST-008'] rel=[]: At stop, Domain/persistence model changes without a seeder change (when a DbSeeder exists) produce a reminder to confirm seeded entities are unaffected or update the development seeder.
- V2 FG-K0-7264c86b25 [54, 65] CANONICAL_ONLY/SHOULD pol=['PST-010'] rel=[]: At stop, added or changed migrations produce a reminder to review them before committing.
- V2 FG-K0-f23bafd9e3 [54, 65] CANONICAL_ONLY/SHOULD pol=['TST-009', 'TST-010'] rel=[]: When production code (backend .cs or frontend .ts, excluding tests, .spec.ts and migrations) changed without any test change, the agent is stopped once to confirm existing coverage or add tests.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0042 -> FG-K0-2e9713cb57 [INTERNAL_ARCHITECTURE] settings.json hooks are exec-form command hooks (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>], existing script handling the event, no varia
- NAMED replica/K0/constraints.jsonl/EXTRA-K0-0017 -> FG-K0-a39d75cc3a [INTERNAL_ARCHITECTURE] Hook configuration: every hook is a command hook in exec form (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>] with the script present and han
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0129 -> FG-K0-55a87d9705 [INTERNAL_ARCHITECTURE] settings.json hooks must be exec-form command hooks with a fixed script/event structure and a positive timeout; the required registrations must exist and the PreToolUse policy hook
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0132 -> FG-K0-dad9dffcde [EXTRA_WORKFLOW] Every Bash/PowerShell call runs through a Node command hook with a 30-second timeout and fail-closed onFailure (reported dependency on Node).
