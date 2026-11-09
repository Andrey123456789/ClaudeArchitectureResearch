// Pure functions copied from frozen L1 pre-shell source, lines14..129 and138..142; no hook imports or state writes.
const GRACE_MS = 30 * 60 * 1000;

// Options that consume the following token when written without '='.
const VALUE_OPTIONS = {
  dotnet: new Set(['--additionalprobingpath', '--additional-deps', '--depsfile', '--runtimeconfig', '--fx-version', '--roll-forward', '--roll-forward-on-no-candidate-fx']),
  npm: new Set(['--prefix', '-C', '--workspace', '-w', '--registry', '--cache', '--userconfig', '--globalconfig', '--loglevel', '--tag', '--omit', '--include', '--install-strategy', '--save-prefix', '--otp', '--scope', '--location']),
  pnpm: new Set(['--dir', '-C', '--filter', '-F', '--workspace-dir', '--reporter', '--store-dir', '--virtual-store-dir', '--loglevel', '--registry']),
  yarn: new Set(['--cwd', '--registry', '--cache-folder', '--modules-folder', '--mutex', '--network-timeout']),
};
const FORCE_FLAGS = new Set(['--force', '-f', '--legacy-peer-deps', '--legacy-peer-deps=true']);
const NODE_DEPENDENCY = {
  npm: { add: ['install', 'i', 'in', 'ins', 'inst', 'add', 'isnt'], always: ['uninstall', 'un', 'unlink', 'remove', 'rm', 'r', 'update', 'up', 'upgrade', 'udpate'] },
  pnpm: { add: ['install', 'i'], always: ['add', 'remove', 'rm', 'un', 'uninstall', 'update', 'up', 'upgrade'] },
  yarn: { add: [], always: ['add', 'remove', 'upgrade', 'up', 'upgrade-interactive'] },
};
const INSTALL_LIKE = new Set(['install', 'i', 'in', 'add', 'ci', 'update', 'up', 'upgrade', 'uninstall', 'remove', 'rm', 'un']);

// Splits on unquoted &&, ||, ;, |, & and newlines.
function segments(command) {
  const out = [];
  let cur = '';
  let quote = null;
  for (let i = 0; i < command.length; i++) {
    const c = command[i];
    if (quote) { cur += c; if (c === quote) quote = null; continue; }
    if (c === '"' || c === "'") { quote = c; cur += c; continue; }
    if (c === ';' || c === '\n' || c === '\r' || c === '|' || c === '&') {
      if (c === '&' && cur.trim() === '') { cur += c; continue; } // PowerShell call operator
      out.push(cur); cur = '';
      if ((c === '&' || c === '|') && command[i + 1] === c) i++;
      continue;
    }
    cur += c;
  }
  out.push(cur);
  return out.map((s) => s.trim()).filter(Boolean);
}

function tokens(segment) {
  const out = [];
  const re = /"([^"]*)"|'([^']*)'|(\S+)/g;
  let m;
  while ((m = re.exec(segment))) out.push(m[1] !== undefined ? m[1] : m[2] !== undefined ? m[2] : m[3]);
  return out;
}

function exeName(token) {
  return String(token || '').split(/[\\/]/).pop().toLowerCase().replace(/\.(exe|cmd|bat|ps1)$/, '');
}

function splitArgs(kind, args) {
  const flags = [];
  const positionals = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith('-')) {
      const flag = a.startsWith('--') ? a.toLowerCase() : a; // short options are case-sensitive (-F filter vs -f force)
      flags.push(flag);
      if (!flag.includes('=') && VALUE_OPTIONS[kind] && VALUE_OPTIONS[kind].has(flag)) i++;
    } else positionals.push(a);
  }
  return { flags, positionals };
}

function dotnetVerdict(args, out) {
  const { positionals } = splitArgs('dotnet', args);
  const [sub, a1, a2] = positionals.map((p) => p.toLowerCase());
  if (sub === 'add' || sub === 'remove') {
    const noun = a1 === 'package' || a1 === 'reference' ? a1 : a2;
    if (noun === 'package') out.dependency = true;
    if (noun === 'reference') out.reference = true;
  } else if (sub === 'package' && ['add', 'remove', 'update'].includes(a1)) out.dependency = true;
  else if (sub === 'reference' && ['add', 'remove'].includes(a1)) out.reference = true;
  else if (sub === 'tool' && ['install', 'update', 'uninstall'].includes(a1)) out.dependency = true;
}

function nodeVerdict(kind, args, out) {
  const { flags, positionals } = splitArgs(kind, args);
  let pos = positionals.map((p) => p.toLowerCase());
  if (kind === 'yarn' && pos[0] === 'workspace') pos = pos.slice(2);
  if (kind === 'yarn' && pos[0] === 'global') pos = pos.slice(1);
  const sub = pos[0] || (kind === 'yarn' ? 'install' : '');
  if (kind === 'npm' && sub === 'config' && pos[1] === 'set' && /^(legacy-peer-deps|force)(=true)?$/.test(pos[2] || '') && (pos[2].includes('=') || pos[3] === 'true')) out.force = true;
  if (flags.some((f) => FORCE_FLAGS.has(f)) && (INSTALL_LIKE.has(sub) || (kind === 'yarn' && !pos[0]))) out.force = true;
  const table = NODE_DEPENDENCY[kind];
  if (table.always.includes(sub)) out.dependency = true;
  if (table.add.includes(sub) && pos.length > 1) out.dependency = true;
  if (kind === 'npm' && sub === 'audit' && pos[1] === 'fix') out.dependency = true;
}

function analyze(tks, out, cli, depth = 0) {
  let t = [...tks];
  while (t.length && (/^[A-Za-z_][A-Za-z0-9_]*=/.test(t[0]) || ['&', 'sudo', 'env', 'time', 'call', 'exec', 'command'].includes(t[0].toLowerCase()))) t.shift();
  if (!t.length || depth > 3) return;
  const exe = exeName(t[0]);
  const rest = t.slice(1);
  if (['bash', 'sh', 'zsh', 'pwsh', 'powershell'].includes(exe)) {
    const i = rest.findIndex((a) => /^-(c|command)$/i.test(a));
    if (i >= 0) for (const seg of segments(rest.slice(i + 1).join(' '))) analyze(tokens(seg), out, cli, depth + 1);
    return;
  }
  if (exe === 'cmd') {
    const i = rest.findIndex((a) => /^\/[ck]$/i.test(a));
    if (i >= 0) analyze(rest.slice(i + 1), out, cli, depth + 1);
    return;
  }
  if (exe === 'npx' || exe === 'corepack') {
    const pkg = rest.filter((a) => !a.startsWith('-'));
    analyze(pkg.length && cli.packages[pkg[0].toLowerCase()] ? [cli.packages[pkg[0].toLowerCase()], ...pkg.slice(1)] : pkg, out, cli, depth + 1);
    return;
  }
  if (exe === 'dotnet') dotnetVerdict(rest, out);
  else if (exe === 'npm' || exe === 'pnpm' || exe === 'yarn') nodeVerdict(exe, rest, out);
  else if (cli.commands[exe] && cli.commands[exe].includes((rest[0] || '').toLowerCase())) out.dependency = true;
  else if (['install-package', 'update-package', 'uninstall-package'].includes(exe)) out.dependency = true;
}
function classify(command, cli = { commands: {}, packages: {} }) {
  const out = { dependency: false, reference: false, force: false };
  for (const seg of segments(String(command || ''))) analyze(tokens(seg), out, cli);
  return out;
}
const cases = ["npm install \"file:./local  package\"", "npm install \"file:./local package\""];
console.log(JSON.stringify(cases.map(command => ({command, verdict:classify(command), retryKey:command.trim().replace(/\s+/g, " ")})), null, 2));
