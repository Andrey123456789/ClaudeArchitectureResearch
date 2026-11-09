"""PV2-01 patches: Git PreToolUse ask in M, M1, L0, L1 and K1, each in its own hook architecture. See DECLARATION.md.
The Git table block is read from git_block.js so the five copies are byte-identical."""
import os

REASON = 'PV2-01 (approved): ask before repository-changing Git commands in M, M1, L0, L1 and K1, with K0 table; read-only Git runs; existing denies win; the ask is not authorization (GOV-015, HQ-01).'
POLICIES = ['GOV-015']
EVIDENCE = 'K0 .claude/hooks/hook.cjs lines 185-234 (table) and 301-306 (ask with the authority text); the other five hooks had no Git classification (direct runs: git commit -m x allowed).'

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'git_block.js'), encoding='utf-8') as _f:
    BLOCK = _f.read()

ENFORCED = ('Enforced by: the pre-command hook asks the user to confirm Git commands it classifies as repository-changing, unrecognized subcommands included; '
            'read-only commands such as `git status`, `git diff` or `git log` run without a prompt. The prompt is not authorization: whether the operation may run at all is still decided by {ref}. '
            'Git run indirectly by scripts or other programs is not classified.')

M_GUARD = '.claude/hooks/dependency-guard.mjs'
M_IO = '.claude/hooks/hook-io.mjs'
M1_PRE = '.claude/hooks/pre-tool-use.js'
M1_DEP = '.claude/scripts/lib/dependency-commands.js'
M1_OUT = '.claude/scripts/lib/hook-output.js'
L0_HOOK = '.claude/hooks/claude-hook.mjs'
L1_HOOK = '.claude/hooks/pre-shell-command.mjs'
K1_DISPATCH = '.claude/hooks/dispatch.cjs'
K1_CLASSIFY = '.claude/scripts/classify-command.cjs'
GW = '.claude/skills/git-workflow/SKILL.md'

PATCHES = [
    # ---------------- M ----------------
    ('M', M_IO,
     """export function blockTool(message) {
  process.stderr.write(`${message}\\n`);
  process.exit(2);
}
""",
     """export function blockTool(message) {
  process.stderr.write(`${message}\\n`);
  process.exit(2);
}

// PreToolUse: ask the user to confirm the tool call; the reason is shown with the prompt (JSON, exit 0).
export function askTool(reason) {
  respond({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: reason } });
}
"""),
    ('M', M_GUARD,
     "import { readInput, startDirectory, activeRepository, manifestChanges, repoRelative, blockTool, postToolBlock, postToolContext, done, fail } from './hook-io.mjs';",
     "import { readInput, startDirectory, activeRepository, manifestChanges, repoRelative, blockTool, askTool, postToolBlock, postToolContext, done, fail } from './hook-io.mjs';"),
    ('M', M_GUARD,
     """//   PreToolUse:  blocks npm installs that bypass peer-dependency resolution
//                (--force, -f, --legacy-peer-deps, or the equivalent npm config
//                and npm_config_* settings).
""",
     """//   PreToolUse:  blocks npm installs that bypass peer-dependency resolution
//                (--force, -f, --legacy-peer-deps, or the equivalent npm config
//                and npm_config_* settings), and asks the user to confirm
//                repository-changing Git commands (K0's table; read-only Git
//                runs; a block always wins over the Git ask).
"""),
    ('M', M_GUARD,
     """        'Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).',
      );
    }
  }
  done();
}
""",
     """        'Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).',
      );
    }
  }
  const gitHits = gitCommands(command);
  if (gitHits.length > 0) askTool(gitAskReason(gitHits));
  done();
}
"""),
    ('M', M_GUARD,
     """const input = readInput(invalidInput);""",
     BLOCK + """
// Quote-aware split for the Git check: segments on unquoted ; | & && || and line
// breaks, then words. (The dependency parsing above stays deliberately minimal.)
function shellSegments(command) {
  const out = [];
  let words = [];
  let word = '';
  let started = false;
  let quote = null;
  const endWord = () => { if (started) words.push(word); word = ''; started = false; };
  const endSegment = () => { endWord(); if (words.length > 0) out.push(words); words = []; };
  const text = command.replace(/[\\\\`]\\r?\\n/g, ' ');
  for (let i = 0; i < text.length; i += 1) {
    const c = text[i];
    if (quote) {
      if (c === quote) quote = null;
      else word += c;
      continue;
    }
    if (c === '"' || c === "'") { quote = c; started = true; continue; }
    if (c === '&' && (text[i - 1] === '>' || text[i + 1] === '>')) { word += c; started = true; continue; } // 2>&1, &> redirections
    if (c === ';' || c === '|' || c === '&' || c === '\\n' || c === '\\r') { endSegment(); continue; }
    if (/\\s/.test(c)) { endWord(); continue; }
    word += c;
    started = true;
  }
  endSegment();
  return out;
}

const GIT_PREFIXES = new Set(['env', 'cross-env', 'sudo', 'time', 'nohup', 'command', 'exec', 'call']);

// Repository-changing Git commands in the command text, inside shell wrappers too: [{ sub, text }].
function gitCommands(command, depth = 0) {
  const hits = [];
  for (let words of shellSegments(command)) {
    while (words.length > 0 && (GIT_PREFIXES.has(executable(words[0])) || /^[A-Za-z_][A-Za-z0-9_]*=/.test(words[0]))) words = words.slice(1);
    if (words.length === 0) continue;
    const tool = executable(words[0]);
    const commandFlag = SHELL_WRAPPERS.get(tool);
    if (commandFlag) {
      const at = words.findIndex((w, i) => i > 0 && commandFlag.test(w));
      if (at > 0 && depth < 3) hits.push(...gitCommands(words.slice(at + 1).join(' '), depth + 1));
      continue;
    }
    if (tool === 'git') {
      const sub = classifyGit(words.slice(1));
      if (sub) hits.push({ sub, text: words.join(' ') });
    }
  }
  return hits;
}

const input = readInput(invalidInput);"""),
    ('M', GW,
     """Which operations require an explicit request, and branch/worktree isolation for
parallel work: CLAUDE.md § Git. Completing an implementation is not a request to
commit, push, merge, or rewrite history.
""",
     """Which operations require an explicit request, and branch/worktree isolation for
parallel work: CLAUDE.md § Git. Completing an implementation is not a request to
commit, push, merge, or rewrite history.

""" + ENFORCED.format(ref='CLAUDE.md § Git') + '\n'),
    ('M', '.claude/MAP.md',
     """| `.claude/hooks/dependency-guard.mjs` | Blocks npm force/legacy-peer-deps installs (also behind npm global options);""",
     """| `.claude/hooks/dependency-guard.mjs` | Blocks npm force/legacy-peer-deps installs (also behind npm global options) and asks the user to confirm repository-changing Git commands (read-only Git runs without a prompt);"""),
    # ---------------- M1 ----------------
    ('M1', M1_OUT,
     """function allow() {""",
     """// PreToolUse: ask the user to confirm the tool call; the reason is shown with the prompt.
function askToolUse(reason) {
  emit({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: reason } });
}

function allow() {"""),
    ('M1', M1_OUT,
     """module.exports = { denyToolUse, denyOnFailure, block, addContext, allow, fail, ascii };""",
     """module.exports = { denyToolUse, askToolUse, denyOnFailure, block, addContext, allow, fail, ascii };"""),
    ('M1', M1_DEP,
     """// Returns { block: boolean, message?: string }.
function analyzeCommand(command, shell) {""",
     BLOCK + """
// Repository-changing Git commands, after wrappers and nested shells: [{ sub, text }]. Kept apart from
// classifyCommand, so changesManifests (the post-command manifest re-check) does not change meaning.
function gitOperations(command, shell, depth = 0) {
  const hits = [];
  for (const segment of segmentsOf(command, shell)) {
    let t = segment.tokens.slice();
    while (t.length && (WRAPPERS.has(t[0].toLowerCase()) || /^[A-Za-z_][A-Za-z0-9_]*=/.test(t[0]) || /^\\$env:/i.test(t[0]))) {
      if (/^\\$env:/i.test(t[0]) && t[1] === '=') t = t.slice(3);
      else t = t.slice(1);
    }
    if (!t.length) continue;
    const exe = exeName(t[0]);
    const args = t.slice(1);
    if (Object.prototype.hasOwnProperty.call(SHELLS, exe)) {
      const flag = args.findIndex((a) => SHELLS[exe].flag.test(a));
      if (flag >= 0 && depth < 3) hits.push(...gitOperations(args.slice(flag + 1).join(' '), SHELLS[exe].shell, depth + 1));
      continue;
    }
    if (exe === 'git') {
      const sub = classifyGit(args);
      if (sub) hits.push({ sub, text: t.join(' ') });
    }
  }
  return hits;
}

// Returns { block: boolean, ask?: boolean, message?: string }. A dependency or reference block always wins;
// otherwise a repository-changing Git command asks.
function analyzeCommand(command, shell) {
  const verdict = dependencyVerdict(command, shell);
  if (verdict.block) return verdict;
  const git = gitOperations(command, shell);
  return git.length ? { block: false, ask: true, message: gitAskReason(git) } : verdict;
}

// Returns { block: boolean, message?: string }.
function dependencyVerdict(command, shell) {"""),
    ('M1', M1_DEP,
     """module.exports = { analyzeCommand, changesManifests, classifyCommand };""",
     """module.exports = { analyzeCommand, changesManifests, classifyCommand, gitOperations, classifyGit };"""),
    ('M1', M1_PRE,
     """// PreToolUse hook entry point (Bash, PowerShell).
// Denies NuGet/npm dependency changes until the add-dependency workflow has been
// applied, project-reference changes until the project-structure procedure has
// been applied, and npm peer-dependency override flags in every case. Only the
// command text is classified (scripts/lib/dependency-commands.js); no repository
// state is read.
""",
     """// PreToolUse hook entry point (Bash, PowerShell).
// Denies NuGet/npm dependency changes until the add-dependency workflow has been
// applied, project-reference changes until the project-structure procedure has
// been applied, and npm peer-dependency override flags in every case. Asks the
// user to confirm repository-changing Git commands (read-only Git runs; a deny
// always wins). Only the command text is classified
// (scripts/lib/dependency-commands.js); no repository state is read.
"""),
    ('M1', M1_PRE,
     """    if (result.block) out.denyToolUse(result.message);
  }
""",
     """    if (result.block) out.denyToolUse(result.message);
    if (result.ask) out.askToolUse(result.message);
  }
"""),
    ('M1', GW,
     """# Git Workflow

## Task Start
""",
     """# Git Workflow

""" + ENFORCED.format(ref='`CLAUDE.md` § Git') + """

## Task Start
"""),
    ('M1', '.claude/MAP.md',
     """stops peer-dependency override flags; fails closed | common | hook | pre-command routing |""",
     """stops peer-dependency override flags; asks the user to confirm repository-changing Git commands (read-only Git runs); fails closed | common | hook | pre-command routing |"""),
    # ---------------- L0 ----------------
    ('L0', L0_HOOK,
     """function feedback(lines) {
  say(lines);
  process.exit(EXIT_FEEDBACK);
}
""",
     """function feedback(lines) {
  say(lines);
  process.exit(EXIT_FEEDBACK);
}

// pre-bash: ask the user to confirm the shell call (hook JSON, exit 0); the reason is shown with the prompt.
function ask(reason) {
  process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: reason } }));
  process.exit(0);
}
"""),
    ('L0', L0_HOOK,
     """  let result = null;
  if (program === 'dotnet') result = classifyDotnet(args);""",
     """  if (program === 'git') {
    const sub = classifyGit(args);
    if (sub) found.push({ text: [...env, ...tokens.slice(i)].join(' '), kind: 'git', sub, bypass: false });
    return;
  }
  let result = null;
  if (program === 'dotnet') result = classifyDotnet(args);"""),
    ('L0', L0_HOOK,
     """function classifyCommand(command) {""",
     BLOCK + """
function classifyCommand(command) {"""),
    ('L0', L0_HOOK,
     """  if (lines.length > 0) feedback(lines);
}
""",
     """  if (lines.length > 0) feedback(lines);
  // Nothing blocked: repository-changing Git commands ask the user to confirm (a block always wins).
  const git = found.filter(entry => entry.kind === 'git');
  if (git.length > 0) ask(gitAskReason(git));
}
"""),
    ('L0', GW,
     """When repository-changing Git operations are allowed at all, and parallel-work isolation, are owned by CLAUDE.md → Git safety.
""",
     """When repository-changing Git operations are allowed at all, and parallel-work isolation, are owned by CLAUDE.md → Git safety.

""" + ENFORCED.format(ref='CLAUDE.md → Git safety') + '\n'),
    ('L0', '.claude/INSTRUCTION_MAP.md',
     """| `.claude/hooks/claude-hook.mjs` | `pre-bash` (fails closed): blocks npm/pnpm/yarn force/legacy-peer flags and `dotnet add/remove … reference` / `dotnet reference add/remove` before they run, also behind global options such as `--prefix`, `--dir`, `--cwd` ·""",
     """| `.claude/hooks/claude-hook.mjs` | `pre-bash` (fails closed): blocks npm/pnpm/yarn force/legacy-peer flags and `dotnet add/remove … reference` / `dotnet reference add/remove` before they run, also behind global options such as `--prefix`, `--dir`, `--cwd`; asks the user to confirm repository-changing Git commands (read-only Git runs) ·"""),
    # ---------------- L1 ----------------
    ('L1', L1_HOOK,
     """// Empty, malformed, or incomplete input and any internal failure block the command (exit 2).""",
     """// - repository-changing Git commands → ask (read-only Git runs without a prompt); a deny always wins;
// Empty, malformed, or incomplete input and any internal failure block the command (exit 2)."""),
    ('L1', L1_HOOK,
     """  if (exe === 'dotnet') dotnetVerdict(rest, out);""",
     """  if (exe === 'git') {
    const sub = classifyGit(rest);
    if (sub) out.git.push({ sub, text: t.join(' ') });
    return;
  }
  if (exe === 'dotnet') dotnetVerdict(rest, out);"""),
    ('L1', L1_HOOK,
     """export function classify(command, cli = { commands: {}, packages: {} }) {
  const out = { dependency: false, reference: false, force: false };""",
     BLOCK + """
export function classify(command, cli = { commands: {}, packages: {} }) {
  const out = { dependency: false, reference: false, force: false, git: [] };"""),
    ('L1', L1_HOOK,
     """  if (verdict.reference) {
    decide('ask', 'Project-reference graph change detected. Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout (architecture.layout via project-structure); confirm only with that approval. The architecture check validates the resulting graph.');
  }
  if (!verdict.dependency) process.exit(0);
""",
     """  const gitReason = verdict.git.length ? gitAskReason(verdict.git) : null;
  if (verdict.reference) {
    decide('ask', ['Project-reference graph change detected. Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout (architecture.layout via project-structure); confirm only with that approval. The architecture check validates the resulting graph.', gitReason].filter(Boolean).join(' '));
  }
  if (!verdict.dependency) {
    if (gitReason) decide('ask', gitReason);
    process.exit(0);
  }
"""),
    ('L1', L1_HOOK,
     """  if (state[key]) {
    delete state[key];
    writeFileSync(stateFile, JSON.stringify(state, null, 2));
    process.exit(0);
  }""",
     """  if (state[key]) {
    delete state[key];
    writeFileSync(stateFile, JSON.stringify(state, null, 2));
    if (gitReason) decide('ask', gitReason);
    process.exit(0);
  }"""),
    ('L1', GW,
     """Whether a repository-changing operation may happen at all is governed by `CLAUDE.md` § Git (a specific request or a pre-approval naming operation and scope; parallel work on separate branches/worktrees).
""",
     """Whether a repository-changing operation may happen at all is governed by `CLAUDE.md` § Git (a specific request or a pre-approval naming operation and scope; parallel work on separate branches/worktrees).

""" + ENFORCED.format(ref='`CLAUDE.md` § Git') + '\n'),
    ('L1', '.claude/INSTRUCTION_MAP.md',
     """peer-dependency bypass flags → denied, with no approval route. Deny-once state lives in the active worktree |""",
     """peer-dependency bypass flags → denied, with no approval route; repository-changing Git commands → ask (read-only Git runs; a deny wins). Deny-once state lives in the active worktree |"""),
    # ---------------- K1 ----------------
    ('K1', K1_CLASSIFY,
     """// Classifies Bash/PowerShell command text BEFORE execution. It recognizes documented dependency and
// project-reference command forms token by token and never inspects files: what a command actually changed
// is inspected after execution by actual-state.cjs.
""",
     """// Classifies Bash/PowerShell command text BEFORE execution. It recognizes documented dependency and
// project-reference command forms token by token and never inspects files: what a command actually changed
// is inspected after execution by actual-state.cjs. Repository-changing Git commands are reported as
// `git-change` findings, which the dispatcher turns into an ask, never a block.
"""),
    ('K1', K1_CLASSIFY,
     """function visit(command, cwd, depth, findings) {""",
     BLOCK + """
function visit(command, cwd, depth, findings) {"""),
    ('K1', K1_CLASSIFY,
     """    if (exe === 'dotnet') findings.push(...dotnetFindings(words, current, segment));""",
     """    if (exe === 'git') {
      const sub = classifyGit(words.slice(1));
      if (sub) findings.push({ kind: 'git-change', segment, sub });
      continue;
    }
    if (exe === 'dotnet') findings.push(...dotnetFindings(words, current, segment));"""),
    ('K1', K1_CLASSIFY,
     """module.exports = { classify, lex };""",
     """module.exports = { classify, lex, classifyGit, gitAskReason };"""),
    ('K1', K1_DISPATCH,
     """  let findings = require('../scripts/classify-command.cjs').classify(command, { cwd });
  if (findings.some(f => f.kind === 'reference-change')) {""",
     """  const classifier = require('../scripts/classify-command.cjs');
  let findings = classifier.classify(command, { cwd });
  const git = findings.filter(f => f.kind === 'git-change');
  findings = findings.filter(f => f.kind !== 'git-change');
  if (findings.some(f => f.kind === 'reference-change')) {"""),
    ('K1', K1_DISPATCH,
     """  if (!findings.length) return 0;
  process.stderr.write(`Blocked before execution (dependency and project-reference guard):\\n- ${findings.map(describe).join('\\n- ')}\\n`);
  return 2;
}""",
     """  if (findings.length) {
    process.stderr.write(`Blocked before execution (dependency and project-reference guard):\\n- ${findings.map(describe).join('\\n- ')}\\n`);
    return 2;
  }
  // Nothing blocked: repository-changing Git commands ask the user to confirm (a block always wins).
  if (git.length) {
    const reason = classifier.gitAskReason(git.map(g => ({ sub: g.sub, text: g.segment })));
    process.stdout.write(`${JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: reason } })}\\n`);
  }
  return 0;
}"""),
    ('K1', GW,
     """Governing policy: `CLAUDE.md` (Git). This workflow owns how a requested operation is carried out.
""",
     """Governing policy: `CLAUDE.md` (Git). This workflow owns how a requested operation is carried out.

""" + ENFORCED.format(ref='`CLAUDE.md` (Git)') + '\n'),
    ('K1', '.claude/MAP.md',
     """| `.claude/scripts/classify-command.cjs` | Pre-execution, token-aware classification of dependency and project-reference commands (Bash and PowerShell text, shell wrappers, chains) |""",
     """| `.claude/scripts/classify-command.cjs` | Pre-execution, token-aware classification of dependency and project-reference commands (Bash and PowerShell text, shell wrappers, chains), and of repository-changing Git commands, which the dispatcher asks the user to confirm (read-only Git runs) |"""),
]
