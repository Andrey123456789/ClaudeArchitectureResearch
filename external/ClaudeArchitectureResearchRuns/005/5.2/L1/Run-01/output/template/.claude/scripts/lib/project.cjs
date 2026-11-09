// Level: 3-project | Owns: shared helpers for instruction-system scripts and hooks
// (project-root resolution, capability selection, globbing, manifest parsing).
'use strict';

const fs = require('fs');
const path = require('path');

const SLOTS = {
  architecture: { required: true },
  persistence: { required: true },
  'backend-testing': { required: true },
  frontend: { required: false },
};

const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', 'dist', 'TestResults', 'coverage']);
const VISITED_HIDDEN_DIRS = new Set(['.claude', '.github']);

class EnvironmentError extends Error {}

function isProjectRoot(dir) {
  return fs.existsSync(path.join(dir, '.claude', 'capabilities'))
    && fs.existsSync(path.join(dir, 'CLAUDE.md'));
}

// Resolves the project root from the script location; CLAUDE_PROJECT_DIR is
// honored when it points at a valid root. Fails loudly instead of guessing.
function resolveRoot(scriptDir) {
  const options = [];
  if (process.env.CLAUDE_PROJECT_DIR) options.push(path.resolve(process.env.CLAUDE_PROJECT_DIR));
  if (scriptDir) {
    let dir = path.resolve(scriptDir);
    for (let i = 0; i < 4; i += 1) {
      options.push(dir);
      dir = path.dirname(dir);
    }
  }
  options.push(process.cwd());
  for (const dir of options) {
    if (isProjectRoot(dir)) return dir;
  }
  throw new EnvironmentError(
    'Cannot locate the project root (a directory containing CLAUDE.md and .claude/capabilities). '
    + 'Run from the project root or set CLAUDE_PROJECT_DIR.');
}

function readText(file) {
  return fs.readFileSync(file, 'utf8');
}

function readJson(file) {
  try {
    return JSON.parse(readText(file));
  } catch (error) {
    throw new EnvironmentError(`Cannot read JSON ${file}: ${error.message}`);
  }
}

function listDirs(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

// Selected implementations per slot = implementation directories present (static composition).
function selectedImplementations(root) {
  const result = {};
  for (const slot of Object.keys(SLOTS)) {
    result[slot] = listDirs(path.join(root, '.claude', 'capabilities', slot));
  }
  return result;
}

function moduleDir(root, slot) {
  const impls = selectedImplementations(root)[slot];
  if (impls.length !== 1) return null;
  return path.join(root, '.claude', 'capabilities', slot, impls[0]);
}

function requireModuleJson(root, slot, file) {
  const dir = moduleDir(root, slot);
  if (!dir) {
    if (SLOTS[slot].required) {
      throw new EnvironmentError(`Slot "${slot}" must have exactly one selected implementation.`);
    }
    return null;
  }
  const target = path.join(dir, file);
  if (!fs.existsSync(target)) {
    throw new EnvironmentError(`Selected module ${path.relative(root, dir)} lacks required facet ${file}.`);
  }
  return readJson(target);
}

function walk(dir, predicate, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      const hidden = entry.name.startsWith('.') && !VISITED_HIDDEN_DIRS.has(entry.name);
      if (!SKIP_DIRS.has(entry.name) && !hidden) walk(path.join(dir, entry.name), predicate, out);
    } else if (predicate(entry.name)) {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

function toPosix(p) {
  return p.split(path.sep).join('/');
}

function globToRegExp(glob) {
  let re = '^';
  for (let i = 0; i < glob.length; i += 1) {
    const c = glob[i];
    if (c === '*') {
      if (glob[i + 1] === '*') {
        i += 1;
        if (glob[i + 1] === '/') { i += 1; re += '(?:.*/)?'; } else { re += '.*'; }
      } else {
        re += '[^/]*';
      }
    } else if (c === '?') {
      re += '[^/]';
    } else {
      re += c.replace(/[.+^${}()|[\]\\]/g, '\\$&');
    }
  }
  return new RegExp(`${re}$`);
}

function attr(tag, name) {
  const match = new RegExp(`\\b${name}\\s*=\\s*"([^"]*)"`, 'i').exec(tag);
  return match ? match[1] : null;
}

// Minimal MSBuild parsing: PackageReference / PackageVersion / ProjectReference items.
function parseMsbuild(text) {
  const items = { packageReferences: [], packageVersions: [], projectReferences: [], properties: {} };
  const itemRe = /<(PackageReference|PackageVersion|ProjectReference)\b([^>]*?)(\/>|>([\s\S]*?)<\/\1>)/g;
  let match;
  while ((match = itemRe.exec(text)) !== null) {
    const [, kind, attrs, , body] = match;
    const include = attr(attrs, 'Include') || attr(attrs, 'Update');
    const childVersion = body ? (/<Version>([^<]*)<\/Version>/i.exec(body) || [])[1] : null;
    const version = attr(attrs, 'Version') || childVersion || null;
    const versionOverride = attr(attrs, 'VersionOverride');
    if (kind === 'PackageReference') items.packageReferences.push({ include, version, versionOverride });
    if (kind === 'PackageVersion') items.packageVersions.push({ include, version });
    if (kind === 'ProjectReference') items.projectReferences.push({ include });
  }
  const propRe = /<(ManagePackageVersionsCentrally|TargetFramework|IsTestProject)>([^<]*)<\/\1>/g;
  while ((match = propRe.exec(text)) !== null) items.properties[match[1]] = match[2].trim();
  return items;
}

// Framework-specific dependency commands declared by selected modules (check.json "dependencyCommands").
function moduleDependencyPatterns(root) {
  const patterns = [];
  for (const [slot, impls] of Object.entries(selectedImplementations(root))) {
    for (const impl of impls) {
      const file = path.join(root, '.claude', 'capabilities', slot, impl, 'check.json');
      if (!fs.existsSync(file)) continue;
      for (const entry of readJson(file).dependencyCommands || []) {
        patterns.push({ regex: new RegExp(entry.pattern), description: entry.description });
      }
    }
  }
  return patterns;
}

function readStdinJson() {
  let raw = '';
  try {
    raw = fs.readFileSync(0, 'utf8');
  } catch (error) {
    throw new EnvironmentError(`Cannot read hook input from stdin: ${error.message}`);
  }
  if (!raw.trim()) return {};
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new EnvironmentError(`Hook input is not valid JSON: ${error.message}`);
  }
}

module.exports = {
  SLOTS,
  EnvironmentError,
  resolveRoot,
  readText,
  readJson,
  listDirs,
  selectedImplementations,
  moduleDir,
  requireModuleJson,
  walk,
  toPosix,
  globToRegExp,
  parseMsbuild,
  moduleDependencyPatterns,
  readStdinJson,
};
