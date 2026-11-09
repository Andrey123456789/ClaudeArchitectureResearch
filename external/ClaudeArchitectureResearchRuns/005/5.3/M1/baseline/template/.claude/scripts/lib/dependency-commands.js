'use strict';
// Classifies shell commands that add, update, or remove NuGet/npm dependencies.
// Used by .claude/hooks/pre-tool-use.js to route such commands to the
// add-dependency workflow; messages point to the owner and do not restate policy.

const WORKFLOW = '.claude/skills/add-dependency/SKILL.md';
const CHECKED = /#\s*add-dependency:\s*checked\b/i;
const PEER_OVERRIDE = /#\s*peer-override:\s*approved-by-user\b/i;

const SIMPLE_PATTERNS = [
  { re: /\bdotnet\s+add\s+(?:\S+\s+)?package\s+[^\s-]\S*/i, kind: 'NuGet package addition' },
  { re: /\bdotnet\s+package\s+(?:add|update|remove)\b/i, kind: 'NuGet package change' },
  { re: /\bdotnet\s+remove\s+(?:\S+\s+)?package\s+\S+/i, kind: 'NuGet package removal' },
  { re: /\b(?:Install|Update|Uninstall)-Package\b/i, kind: 'NuGet package change' },
  { re: /\bnuget(?:\.exe)?\s+(?:install|update)\b/i, kind: 'NuGet package change' },
  { re: /\bng\s+(?:add|update)\s+\S+/i, kind: 'frontend package change' },
  { re: /\b(?:yarn|pnpm)\s+(?:add|remove|up|upgrade|update)\b/i, kind: 'package change' },
];

function npmChange(command) {
  const re = /\bnpm\s+(install|i|add|update|up|upgrade|uninstall|remove|rm|un|r)\b([^\n;&|]*)/gi;
  let m;
  while ((m = re.exec(command))) {
    const verb = m[1].toLowerCase();
    const args = m[2].replace(/#.*$/, '').trim().split(/\s+/).filter(Boolean);
    const packages = args.filter((a) => !a.startsWith('-'));
    if (['install', 'i', 'add'].includes(verb)) {
      if (packages.length) return 'npm package addition';
    } else {
      return 'npm package change';
    }
  }
  return null;
}

// Returns { block: boolean, message?: string }.
function analyzeCommand(command) {
  const text = String(command || '');
  const forceFlag = /\b(?:npm|npx|pnpm|yarn)\b[^\n;&|]*?\s(--force|--legacy-peer-deps)\b/i.exec(text);
  if (forceFlag && !PEER_OVERRIDE.test(text)) {
    return {
      block: true,
      message:
        `Peer-dependency override flag detected (${forceFlag[1]}).\n` +
        `Resolve the actual compatibility problem instead (${WORKFLOW}, Install).\n` +
        'Only when the user explicitly approved the override, re-run the same command with the trailing comment: # peer-override: approved-by-user\n',
    };
  }
  let kind = null;
  for (const p of SIMPLE_PATTERNS) {
    if (p.re.test(text)) {
      kind = p.kind;
      break;
    }
  }
  kind = kind || npmChange(text);
  if (!kind || CHECKED.test(text)) return { block: false };
  const notes = [];
  if (/--prerelease\b|@(?:next|canary|beta|alpha|rc)\b/i.test(text)) notes.push('The command requests a prerelease version.');
  if (/--version\s+["']?\*|@\*(?:\s|$)|@latest\b/i.test(text)) notes.push('The command requests a floating or unresolved version.');
  return {
    block: true,
    message:
      `Dependency change detected (${kind}).\n` +
      `Run the add-dependency workflow first (${WORKFLOW}): need and approval check, package choice, latest stable compatible version, deprecation, vulnerability, and license checks.\n` +
      (notes.length ? `${notes.join(' ')}\n` : '') +
      'After completing it, re-run the same command with the trailing comment: # add-dependency: checked\n',
  };
}

// Commands after which manifests or project references may have changed.
function changesManifests(command) {
  return /\bdotnet\s+(?:add|remove|new|sln|package)\b|\b(?:npm|pnpm|yarn)\s+(?:install|i|add|update|up|upgrade|uninstall|remove|rm|un)\b|\bng\s+(?:add|update|new)\b/i.test(
    String(command || '')
  );
}

module.exports = { analyzeCommand, changesManifests };
