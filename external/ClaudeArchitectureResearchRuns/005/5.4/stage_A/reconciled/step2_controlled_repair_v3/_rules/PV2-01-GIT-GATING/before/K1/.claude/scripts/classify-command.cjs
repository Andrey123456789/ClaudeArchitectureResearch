// Kind: ENF | Scope: common | Capability: — | Loading: required by .claude/hooks/dispatch.cjs (PreToolUse); pre-execution command classification
// Conforms: .claude/rules/common/dependencies.md, docs/architecture/decision-register.md
'use strict';

// Classifies Bash/PowerShell command text BEFORE execution. It recognizes documented dependency and
// project-reference command forms token by token and never inspects files: what a command actually changed
// is inspected after execution by actual-state.cjs.

const path = require('path');

const MAX_DEPTH = 3;

// ---------- lexing ----------

/** Split command text into segments (word lists) at ; | & && || newlines, parentheses, and braces. */
function lex(command) {
  const s = String(command || '');
  const segments = [];
  let words = [];
  let cur = null;
  const pushWord = () => {
    if (cur !== null) words.push(cur);
    cur = null;
  };
  const endSegment = () => {
    pushWord();
    if (words.length) segments.push(words);
    words = [];
  };
  let i = 0;
  while (i < s.length) {
    const ch = s[i];
    const next = s[i + 1];
    if ((ch === '\\' || ch === '`') && (next === '\n' || (next === '\r' && s[i + 2] === '\n'))) {
      i += next === '\r' ? 3 : 2; // line continuation (Bash backslash, PowerShell backtick)
      continue;
    }
    if (ch === "'") {
      const j = s.indexOf("'", i + 1);
      cur = (cur || '') + s.slice(i + 1, j < 0 ? s.length : j);
      i = j < 0 ? s.length : j + 1;
      continue;
    }
    if (ch === '"') {
      let j = i + 1;
      let buf = '';
      while (j < s.length && s[j] !== '"') {
        if ((s[j] === '\\' || s[j] === '`') && (s[j + 1] === '"' || (s[j] === '\\' && s[j + 1] === '\\'))) {
          buf += s[j + 1];
          j += 2;
          continue;
        }
        buf += s[j];
        j += 1;
      }
      cur = (cur || '') + buf;
      i = j + 1;
      continue;
    }
    if ('\n;|&(){}'.includes(ch)) {
      endSegment();
      i += 1;
      continue;
    }
    if (ch === '<' || ch === '>') {
      if (cur !== null && /^[\d*]*$/.test(cur)) cur = null; // file-descriptor prefix such as 2> or *>
      pushWord();
      let j = i;
      while (j < s.length && /[<>&\d]/.test(s[j])) j += 1;
      const op = s.slice(i, j);
      i = j;
      if (/&\d+$/.test(op)) continue; // descriptor duplication (2>&1) has no target
      while (i < s.length && /[ \t]/.test(s[i])) i += 1;
      if (s[i] === '"' || s[i] === "'") {
        const k = s.indexOf(s[i], i + 1);
        i = k < 0 ? s.length : k + 1;
      } else {
        while (i < s.length && !/[\s;|&(){}<>]/.test(s[i])) i += 1;
      }
      continue;
    }
    if (ch === '#' && cur === null) {
      const j = s.indexOf('\n', i); // comment (Bash and PowerShell)
      i = j < 0 ? s.length : j;
      continue;
    }
    if (/\s/.test(ch)) {
      pushWord();
      i += 1;
      continue;
    }
    cur = (cur || '') + ch;
    i += 1;
  }
  endSegment();
  return segments;
}

function exeName(word) {
  return String(word).split(/[\\/]/).pop().toLowerCase().replace(/\.(exe|cmd|bat|ps1)$/, '');
}

const PREFIX_COMMANDS = new Set(['sudo', 'command', 'exec', 'time', 'nohup', 'env', 'call', 'corepack']);
const CHANGE_DIRECTORY = new Set(['cd', 'chdir', 'pushd', 'set-location', 'sl', 'push-location']);
const POSIX_SHELLS = new Set(['bash', 'sh', 'zsh', 'dash', 'ksh']);

/** Drop environment assignments and transparent prefix commands (sudo, env, time, ...). */
function stripPrefixes(words) {
  let i = 0;
  while (i < words.length) {
    if (/^[A-Za-z_][A-Za-z0-9_]*=/.test(words[i])) {
      i += 1;
      continue;
    }
    const exe = exeName(words[i]);
    if (!PREFIX_COMMANDS.has(exe)) break;
    i += 1;
    while (i < words.length && words[i].startsWith('-')) i += exe === 'sudo' && /^-[ugCDhpRrT]$/.test(words[i]) ? 2 : 1;
  }
  return words.slice(i);
}

/** Inline command text carried by a shell wrapper (bash -c, cmd /c, powershell -Command/-EncodedCommand), else null. */
function wrappedCommand(words) {
  const exe = exeName(words[0]);
  if (POSIX_SHELLS.has(exe)) {
    for (let i = 1; i < words.length; i += 1) {
      if (/^-[A-Za-z]*c[A-Za-z]*$/.test(words[i])) return words[i + 1] || '';
      if (!words[i].startsWith('-')) return null; // script file
    }
    return null;
  }
  if (exe === 'cmd') {
    const i = words.findIndex(w => /^\/[ck]$/i.test(w));
    return i >= 0 ? words.slice(i + 1).join(' ') : null;
  }
  if (exe === 'powershell' || exe === 'pwsh') {
    for (let i = 1; i < words.length; i += 1) {
      const w = words[i].toLowerCase();
      if (/^-(c|com|comm|comma|comman|command)$/.test(w)) return words.slice(i + 1).join(' ');
      if (/^-(ec|enc|enco|encod|encode|encoded|encodedc|encodedco|encodedcom|encodedcomm|encodedcomma|encodedcomman|encodedcommand)$/.test(w)) {
        return Buffer.from(words[i + 1] || '', 'base64').toString('utf16le');
      }
      if (/^-(f|file)$/.test(w)) return null;
      if (/^-(executionpolicy|ep|ex|windowstyle|w|configurationname|workingdirectory|wd)$/.test(w)) {
        i += 1;
        continue;
      }
      if (!w.startsWith('-')) return exe === 'powershell' ? words.slice(i).join(' ') : null;
    }
    return null;
  }
  return null;
}

// ---------- package managers (table-driven) ----------

const NPM_INSTALL = ['install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'isntall', 'add'];
const NPM_RESTORE = ['ci', 'clean-install', 'ic', 'install-clean', 'isntall-clean', 'install-ci-test', 'cit', 'install-test', 'it', 'dedupe', 'ddp', 'prune'];
const verbs = (category, names) => Object.fromEntries(names.map(n => [n, category]));

const MANAGERS = {
  npm: {
    values: ['--prefix', '-C', '--workspace', '-w', '--loglevel', '--registry', '--userconfig', '--globalconfig', '--cache', '--tag', '--otp', '--scope', '--save-prefix', '--omit', '--include', '--install-strategy', '--before', '--location'],
    verbs: {
      ...verbs('install', NPM_INSTALL),
      ...verbs('update', ['update', 'up', 'upgrade', 'udpate']),
      ...verbs('remove', ['uninstall', 'unlink', 'remove', 'rm', 'r', 'un']),
      ...verbs('restore', NPM_RESTORE),
      audit: 'audit',
    },
  },
  pnpm: {
    values: ['--dir', '-C', '--filter', '-F', '--loglevel', '--reporter', '--registry', '--workspace-concurrency', '--store-dir', '--virtual-store-dir'],
    verbs: {
      ...verbs('install', ['add', 'install', 'i']),
      ...verbs('update', ['update', 'up', 'upgrade']),
      ...verbs('remove', ['remove', 'rm', 'uninstall', 'un']),
      ...verbs('restore', ['prune', 'dedupe']),
      audit: 'audit',
    },
  },
  yarn: {
    values: ['--cwd', '--modules-folder', '--cache-folder', '--mutex', '--network-timeout', '--registry'],
    verbs: {
      ...verbs('install', ['add', 'install']),
      ...verbs('update', ['upgrade', 'up', 'upgrade-interactive']),
      remove: 'remove',
      dedupe: 'restore',
      audit: 'audit',
    },
    noVerb: 'restore', // bare `yarn` installs from the manifest
    passThrough: { workspace: 1, global: 0 }, // yarn workspace <name> add x, yarn global add x
  },
};

const EXACT_SEMVER = /^v?\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;
const NON_REGISTRY_SPEC = /^(\.{1,2}[\\/]|[\\/]|~[\\/]|[A-Za-z]:[\\/]|file:|link:|workspace:|portal:|git\+|git:|https?:|github:|gitlab:|bitbucket:)/;

function npmSpecIsExact(spec) {
  if (NON_REGISTRY_SPEC.test(spec) || /\.(tgz|tar\.gz)$/i.test(spec)) return true; // local or URL source pins itself
  const at = spec.indexOf('@', spec.startsWith('@') ? 1 : 0);
  if (at < 0) return false;
  const version = spec.slice(at + 1);
  if (version.startsWith('npm:')) return npmSpecIsExact(version.slice(4));
  return EXACT_SEMVER.test(version.replace(/^=/, ''));
}

const PEER_BYPASS = /^(--force|-f|--legacy-peer-deps)(=(?!false$).*)?$/;

/** DEP-003 exception: the command form of a version the user explicitly requested and that is recorded; the post-change check enforces its manifest. */
function recordedVersion(cwd, ecosystem, id, version) {
  try {
    const lib = require('./lib.cjs');
    const { entries } = require('./check-manifests.cjs').loadVersionExceptions(lib.activeRoot(cwd));
    const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
    return entries.some(e => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted && e.version.trim() === String(version).trim());
  } catch {
    return false;
  }
}

function npmSpecIsRecorded(spec, cwd) {
  const at = spec.indexOf('@', spec.startsWith('@') ? 1 : 0);
  return at > 0 && recordedVersion(cwd, 'npm', spec.slice(0, at), spec.slice(at + 1));
}

function managerFindings(exe, words, segment, cwd) {
  const m = MANAGERS[exe];
  const values = new Set(m.values);
  const options = [];
  const positional = [];
  let verb = null;
  for (let i = 1; i < words.length; i += 1) {
    const w = words[i];
    if (w === '--') break;
    if (w.startsWith('-')) {
      options.push(w);
      if (values.has(w)) i += 1;
      continue;
    }
    if (verb === null) {
      if (m.passThrough && Object.prototype.hasOwnProperty.call(m.passThrough, w)) {
        i += m.passThrough[w];
        continue;
      }
      verb = w.toLowerCase();
      continue;
    }
    positional.push(w);
  }
  let category = verb === null ? m.noVerb || null : m.verbs[verb] || null;
  let specs = positional;
  if (category === 'audit') {
    category = positional[0] === 'fix' ? 'update' : null;
    specs = [];
  }
  if (exe === 'npm' && verb === 'config' && positional[0] === 'set' && /^(legacy-peer-deps|force)(=true)?$/i.test(positional[1] || '') && ((positional[1] || '').includes('=') || positional[2] === 'true')) return [{ kind: 'peer-bypass', segment }];
  if (!category) return [];
  const findings = [];
  if (options.some(o => PEER_BYPASS.test(o))) findings.push({ kind: 'peer-bypass', segment });
  if (category === 'remove') findings.push({ kind: 'dependency-removal', segment, specs });
  else if (category === 'update' && !specs.length) findings.push({ kind: 'dependency-update', segment });
  else if (category === 'install' || category === 'update') {
    const loose = specs.filter(s => !npmSpecIsExact(s) && !npmSpecIsRecorded(s, cwd));
    if (loose.length) findings.push({ kind: 'dependency-version', segment, specs: loose });
  }
  return findings;
}

// ---------- dotnet ----------

const DOTNET_VALUE_OPTIONS = new Set(['-v', '--version', '-f', '--framework', '-s', '--source', '--package-directory', '--project', '--verbosity']);
const EXACT_NUGET = /^\d+(\.\d+){1,3}(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$/;

function projectName(project, cwd) {
  const base = path.basename(String(project || cwd).replace(/[\\/]+$/, '').replace(/\\/g, '/'));
  return base.replace(/\.(cs|fs|vb)proj$/i, '');
}

function dotnetFindings(words, cwd, segment) {
  let i = 1;
  while (i < words.length && words[i].startsWith('-')) i += 1; // host options such as --diagnostics
  const verb = (words[i] || '').toLowerCase();
  const rest = words.slice(i + 1);
  if (rest.some(w => /^(-h|--help|-\?|\/\?)$/.test(w))) return [];
  let kind;
  let action;
  let project = null;
  let args;
  if (verb === 'add' || verb === 'remove') {
    const j = rest.findIndex(w => /^(package|reference)$/i.test(w));
    if (j < 0) return [];
    kind = rest[j].toLowerCase();
    action = verb;
    project = rest.slice(0, j).find(w => !w.startsWith('-')) || null;
    args = rest.slice(j + 1);
  } else if ((verb === 'package' || verb === 'reference') && /^(add|remove|update)$/i.test(rest[0] || '')) {
    kind = verb;
    action = rest[0].toLowerCase();
    args = rest.slice(1);
  } else {
    return [];
  }
  const opts = {};
  const positional = [];
  for (let k = 0; k < args.length; k += 1) {
    const m = /^(--?[A-Za-z][\w-]*)(?:[=:](.*))?$/.exec(args[k]);
    if (m) {
      const name = m[1].toLowerCase();
      let value = m[2];
      if (value === undefined && DOTNET_VALUE_OPTIONS.has(name)) value = args[(k += 1)];
      opts[name] = value === undefined ? true : value;
      continue;
    }
    positional.push(args[k]);
  }
  if (typeof opts['--project'] === 'string') project = opts['--project'];
  if (kind === 'reference') {
    if (action === 'update') return [];
    const from = projectName(project, cwd);
    const edges = positional.map(ref => ({ from, to: projectName(ref, cwd) }));
    return [{ kind: 'reference-change', segment, action, edges }];
  }
  if (action === 'remove') return [{ kind: 'dependency-removal', segment, specs: positional }];
  const [id, inlineVersion] = String(positional[0] || '').split('@');
  if (!id && action === 'update') return [{ kind: 'dependency-update', segment }];
  const version = opts['--version'] || opts['-v'] || inlineVersion;
  if (!id || typeof version !== 'string' || (!EXACT_NUGET.test(version) && !recordedVersion(cwd, 'nuget', id, version))) {
    return [{ kind: 'dependency-version', segment, specs: [id || '(no package id)'] }];
  }
  return [];
}

// ---------- traversal ----------

function visit(command, cwd, depth, findings) {
  let current = cwd;
  for (const raw of lex(command)) {
    const words = stripPrefixes(raw);
    if (!words.length) continue;
    const segment = words.join(' ');
    const exe = exeName(words[0]);
    if (CHANGE_DIRECTORY.has(exe)) {
      const target = words.slice(1).find(w => !w.startsWith('-'));
      if (target && target !== '-') current = path.resolve(current, target);
      continue;
    }
    const inner = wrappedCommand(words);
    if (inner !== null) {
      if (depth < MAX_DEPTH) visit(inner, current, depth + 1, findings);
      else findings.push({ kind: 'unclassifiable', segment });
      continue;
    }
    if (exe === 'dotnet') findings.push(...dotnetFindings(words, current, segment));
    else if (Object.prototype.hasOwnProperty.call(MANAGERS, exe)) findings.push(...managerFindings(exe, words, segment, current));
  }
}

/** Findings for one Bash or PowerShell command; `cwd` resolves implicit project directories. */
function classify(command, options = {}) {
  const findings = [];
  if (/\bnpm_config_(force|legacy_peer_deps)\s*=\s*['\"]?(true|1)\b/i.test(String(command)) && /\bnpm(\.cmd)?\s/i.test(String(command))) findings.push({ kind: 'peer-bypass', segment: String(command).trim() });
  visit(command, options.cwd || process.cwd(), 0, findings);
  return findings;
}

module.exports = { classify, lex };
