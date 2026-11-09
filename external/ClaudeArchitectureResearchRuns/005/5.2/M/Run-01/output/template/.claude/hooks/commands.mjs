// Shell-command classification shared by the pre-tool and post-tool hooks.
// Works on command text from either the Bash or the PowerShell tool.

// Splits a command line into simple commands at shell separators (; && || | and newlines).
export function splitCommands(command) {
  return String(command ?? '')
    .split(/\r?\n|&&|\|\||[;|]/)
    .map((part) => part.trim())
    .filter(Boolean);
}

function tokens(simpleCommand) {
  return simpleCommand.match(/"[^"]*"|'[^']*'|\S+/g) ?? [];
}

const NPM_INSTALL_VERBS = new Set(['install', 'i', 'add', 'ci', 'update', 'up', 'upgrade']);
const NPM_CHANGE_VERBS = new Set(['install', 'i', 'add', 'uninstall', 'un', 'remove', 'rm', 'update', 'up', 'upgrade']);
const PACKAGE_MANAGERS = new Set(['npm', 'pnpm', 'yarn']);

function managerAndVerb(parts) {
  const index = parts.findIndex((p) => PACKAGE_MANAGERS.has(p.toLowerCase()));
  if (index === -1) return null;
  const rest = parts.slice(index + 1).filter((p) => !p.startsWith('-'));
  return { manager: parts[index].toLowerCase(), verb: (rest[0] ?? '').toLowerCase(), args: rest.slice(1), all: parts.slice(index + 1) };
}

// npm/pnpm/yarn install-type commands that bypass peer-dependency resolution.
export function findPeerBypass(command) {
  for (const simple of splitCommands(command)) {
    const parts = tokens(simple);
    const mv = managerAndVerb(parts);
    if (!mv) continue;
    const verb = mv.verb || (mv.manager === 'yarn' ? 'install' : '');
    if (!NPM_INSTALL_VERBS.has(verb)) continue;
    const flag = mv.all.find((p) => /^--(force|legacy-peer-deps)(=.*)?$/i.test(p) || p === '-f');
    if (flag) return { command: simple, flag };
  }
  return null;
}

// Commands that add, update, or remove packages or project references.
export function findDependencyCommands(command) {
  const found = [];
  for (const simple of splitCommands(command)) {
    const parts = tokens(simple);
    const lower = parts.map((p) => p.toLowerCase());
    const dotnet = lower.indexOf('dotnet');
    if (dotnet !== -1) {
      const rest = lower.slice(dotnet + 1);
      if (rest[0] === 'package' && ['add', 'remove', 'update'].includes(rest[1])) found.push({ command: simple, kind: 'package' });
      else if (['add', 'remove'].includes(rest[0]) && rest.includes('package')) found.push({ command: simple, kind: 'package' });
      else if (['add', 'remove'].includes(rest[0]) && rest.includes('reference')) found.push({ command: simple, kind: 'reference' });
      else if (rest[0] === 'reference' && ['add', 'remove'].includes(rest[1])) found.push({ command: simple, kind: 'reference' });
      continue;
    }
    const mv = managerAndVerb(parts);
    if (mv && NPM_CHANGE_VERBS.has(mv.verb) && mv.args.length > 0) {
      found.push({ command: simple, kind: 'package' });
      continue;
    }
    const ng = lower.indexOf('ng');
    if (ng !== -1 && ['add', 'update'].includes(lower[ng + 1]) && lower.length > ng + 2) {
      found.push({ command: simple, kind: 'package' });
      continue;
    }
    if (/^(install|update|uninstall)-package$/.test(lower[0] ?? '')) found.push({ command: simple, kind: 'package' });
  }
  return found;
}

// Git commands that can discard work or rewrite shared history.
export function findDestructiveGit(command) {
  for (const simple of splitCommands(command)) {
    const parts = tokens(simple).map((p) => p.replace(/^["']|["']$/g, ''));
    const git = parts.findIndex((p) => p.toLowerCase() === 'git');
    if (git === -1) continue;
    const args = parts.slice(git + 1).filter((p, i, all) => !(i === 0 && p === '-C') && !(i > 0 && all[i - 1] === '-C'));
    const sub = (args[0] ?? '').toLowerCase();
    const has = (re) => args.slice(1).some((a) => re.test(a));
    if (sub === 'reset' && has(/^--hard$/)) return simple;
    if (sub === 'clean' && has(/^-[a-z]*f/i)) return simple;
    if (sub === 'push' && has(/^(--force|--force-with-lease(=.*)?|-f|\+.+)$/)) return simple;
    if (sub === 'branch' && (has(/^-D$/) || (has(/^(-d|--delete)$/) && has(/^(-f|--force)$/)))) return simple;
    if (sub === 'checkout' && args.includes('--')) return simple;
    if (sub === 'checkout' && has(/^(-f|--force)$/)) return simple;
    if (sub === 'restore' && !has(/^(--staged|-S)$/)) return simple;
    if (sub === 'stash' && ['drop', 'clear'].includes((args[1] ?? '').toLowerCase())) return simple;
    if (sub === 'worktree' && (args[1] ?? '').toLowerCase() === 'remove' && has(/^(-f|--force)$/)) return simple;
  }
  return null;
}
