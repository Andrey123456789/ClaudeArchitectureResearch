// Instruction-structure checker: validates the structural predicates of this
// instruction system (flat path-scoped rules, headers, imports and the
// always-loaded set, references, skills, the thin reviewer agent, hook commands,
// the human map, and the four capability slots).
// Usage: node .claude/scripts/check-instructions.mjs [--root <dir>]
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  TemplateError, resolveRoot, exists, readText, walk, splitFrontmatter, parseFrontmatter,
  headerLine, capabilityOf, headings, loadSelection, loadCapabilities, resolveRoleTokens,
  termRegExp, report, SLOTS, SELECTION_FILE,
} from './lib/template.mjs';

const GENERIC_FILE_NAMES = new Set([
  'package.json', 'package-lock.json', 'global.json', 'launchSettings.json', 'appsettings.json',
  'appsettings.Development.json', 'Project.csproj', 'SKILL.md', 'MODULE.md', 'CONTRACT.md',
]);
const BUDGET_TOKENS = 6000;

function instructionFiles(root) {
  const files = ['CLAUDE.md'];
  for (const p of walk(root, 'docs')) if (/^docs\/[^/]+\.md$/.test(p)) files.push(p);
  for (const p of walk(root, '.claude')) if (p.endsWith('.md')) files.push(p);
  return files;
}

function runtimeFiles(root) {
  const files = ['CLAUDE.md', '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].filter(f => exists(root, f));
  for (const p of walk(root, 'docs')) if (p.endsWith('.md') && p !== SELECTION_FILE) files.push(p);
  for (const dir of ['.claude/rules', '.claude/skills', '.claude/agents', '.claude/hooks', '.claude/scripts']) files.push(...walk(root, dir));
  if (exists(root, '.claude/settings.json')) files.push('.claude/settings.json');
  return files;
}

function importsOf(text) {
  const out = [];
  let fence = false;
  for (const line of text.split('\n')) {
    if (/^(```|~~~)/.test(line)) { fence = !fence; continue; }
    const m = !fence && /^@(\S+)\s*$/.exec(line);
    if (m) out.push(m[1]);
  }
  return out;
}

function alwaysLoaded(root, errors) {
  const seen = new Set();
  const visit = (rel, chain) => {
    if (chain.includes(rel)) { errors.push(`import cycle: ${[...chain, rel].join(' -> ')}`); return; }
    if (seen.has(rel)) return;
    seen.add(rel);
    for (const imp of importsOf(readText(root, rel))) {
      const target = path.posix.normalize(path.posix.join(path.posix.dirname(rel), imp));
      if (!exists(root, target)) { errors.push(`${rel}: import @${imp} does not resolve`); continue; }
      if (target.startsWith('.claude/rules/')) errors.push(`${rel}: imports rule ${target}; an imported rule becomes always-loaded and loses its path trigger`);
      visit(target, [...chain, rel]);
    }
  };
  visit('CLAUDE.md', []);
  return seen;
}

function skillNames(root) {
  return walk(root, '.claude/skills').filter(p => /^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(p)).map(p => p.split('/')[2]);
}

function resolveFileToken(root, file, token, skills) {
  const clean = token.replace(/^\.\//, '');
  const dir = path.posix.dirname(file);
  const options = [clean, path.posix.join(dir, clean)];
  if (!clean.includes('/')) options.push(`.claude/rules/${clean}`, `docs/${clean}`, `.claude/scripts/${clean}`, `.claude/hooks/${clean}`);
  if (clean.startsWith('references/')) for (const s of skills) options.push(`.claude/skills/${s}/${clean}`);
  return options.find(c => exists(root, c)) ?? null;
}

function checkReferences(root, file, text, skills, errors) {
  const flat = text.replace(/\s+/g, ' ');
  const skillSet = new Set(skills);
  // File-path tokens in backticks.
  for (const m of text.matchAll(/`([\w./-]+\.(?:md|mjs|json|props))`/g)) {
    const token = m[1];
    if (GENERIC_FILE_NAMES.has(path.posix.basename(token)) || /NNNN|[<*{]/.test(token) || token.startsWith('docs/decisions/')) continue;
    if (!resolveFileToken(root, file, token, skills)) errors.push(`${file}: reference \`${token}\` does not resolve`);
  }
  // Named skills and workflows.
  for (const m of flat.matchAll(/`([a-z0-9-]+)` (?:skill|workflow)\b|\b[Rr]un (?:the )?`([a-z0-9-]+)`/g)) {
    const name = m[1] ?? m[2];
    if (!skillSet.has(name)) errors.push(`${file}: skill/workflow \`${name}\` does not exist`);
  }
  // Section references: `target` → Heading
  for (const m of flat.matchAll(/`([\w./-]+)` → ([A-Z][^.,;:)`(]*)/g)) {
    const [, target, captured] = m;
    let rel = null;
    if (skillSet.has(target)) rel = `.claude/skills/${target}/SKILL.md`;
    else if (/\.md$/.test(target)) rel = resolveFileToken(root, file, target, skills);
    if (!rel) { errors.push(`${file}: section reference target \`${target}\` does not resolve`); continue; }
    const wanted = captured.trim();
    if (!headings(readText(root, rel)).some(h => wanted.startsWith(h))) errors.push(`${file}: \`${target}\` → "${wanted}" has no matching heading in ${rel}`);
  }
  // Markdown links.
  for (const m of text.matchAll(/\]\(([^)#\s]+)(?:#[^)]*)?\)/g)) {
    if (/^[a-z]+:/.test(m[1])) continue;
    if (!resolveFileToken(root, file, m[1], skills)) errors.push(`${file}: link ${m[1]} does not resolve`);
  }
}

function checkCapabilities(root, always, instr, errors, warnings) {
  let caps;
  try { caps = loadCapabilities(root); } catch (e) { errors.push(e.message); return; }
  const { rows, contracts, modules, allModules } = caps;
  const bySlot = Object.fromEntries(rows.map(r => [r.slot, r]));
  for (const r of rows) if (!SLOTS.includes(r.slot)) errors.push(`${SELECTION_FILE}: unknown capability slot "${r.slot}" (only ${SLOTS.join(', ')} exist)`);
  for (const slot of SLOTS) {
    const contract = contracts[slot];
    const row = bySlot[slot];
    if (!contract) { errors.push(`missing contract .claude/capabilities/${slot}/CONTRACT.md`); continue; }
    if (rows.filter(r => r.slot === slot).length > 1) errors.push(`${SELECTION_FILE}: slot ${slot} is listed more than once`);
    if (!row) { errors.push(`${SELECTION_FILE}: slot ${slot} has no selection row`); continue; }
    const none = /^none\b/.test(row.selected);
    if (/[,;/+]|\band\b/.test(row.selected)) errors.push(`${SELECTION_FILE}: slot ${slot} selects more than one implementation ("${row.selected}")`);
    if (none && contract.status === 'required') errors.push(`${SELECTION_FILE}: required slot ${slot} has no selected implementation`);
    if (none) continue;
    const mod = modules[slot];
    if (!mod) { errors.push(`slot ${slot}: selected implementation "${row.selected}" has no .claude/capabilities/${slot}/${row.selected}/MODULE.md`); continue; }
    const m = mod.manifest;
    const id = `${slot}/${row.selected}`;
    if (m.capability !== id) errors.push(`${mod.rel}: capability "${m.capability}" does not match selection ${id}`);
    const roles = new Set((m.facets ?? []).map(f => f.role));
    for (const req of contract.requiredFacets ?? []) if (!roles.has(req)) errors.push(`${mod.rel}: required facet "${req}" missing`);
    for (const req of contract.requiredProperties ?? []) if (!(req in (m.properties ?? {}))) errors.push(`${mod.rel}: required property "${req}" missing`);
    for (const f of m.facets ?? []) {
      if (!exists(root, f.path)) { errors.push(`${mod.rel}: facet ${f.role} file ${f.path} does not exist`); continue; }
      const cap = capabilityOf(readText(root, f.path));
      if (cap !== id) errors.push(`${f.path}: header must declare "Capability: ${id}" (found ${cap ?? 'none'})`);
      if (f.loading === 'always' && !always.has(f.path)) errors.push(`${f.path}: always-loaded facet is not imported (expected via ${SELECTION_FILE})`);
      if (f.loading === 'path' && !/^\.claude\/rules\/[^/]+\.md$/.test(f.path)) errors.push(`${f.path}: path-loaded facet must be a flat rule file`);
    }
    for (const b of m.binds ?? []) {
      const [bSlot, bImpl] = String(b.capability ?? '').split('/');
      if (!bySlot[bSlot] || bySlot[bSlot].selected !== bImpl) errors.push(`${mod.rel}: binds ${b.capability} but that implementation is not selected`);
      if (bSlot === slot) errors.push(`${mod.rel}: binds its own slot`);
    }
    const frameRoles = new Set(contracts.architecture?.roles ?? []);
    for (const role of m.usesRoles ?? []) if (!frameRoles.has(role)) errors.push(`${mod.rel}: uses role "${role}" that the architecture contract does not define`);
    try { JSON.stringify(m.properties ?? {}).replace(/<role:[^>]+>/g, t => resolveRoleTokens(t, modules.architecture?.manifest)); }
    catch (e) { errors.push(`${mod.rel}: ${e.message}`); }
  }
  if (modules.architecture && contracts.architecture) {
    const mapped = modules.architecture.manifest.properties?.roleMapping ?? {};
    for (const role of contracts.architecture.roles ?? []) if (!(role in mapped)) errors.push(`${modules.architecture.rel}: role "${role}" is not mapped`);
  }
  // Facet headers must belong to a selected implementation and be listed by it.
  const listed = new Map();
  for (const [slot, mod] of Object.entries(modules)) for (const f of mod.manifest.facets ?? []) listed.set(f.path, `${slot}/${mod.manifest.capability.split('/')[1]}`);
  for (const file of instr) {
    if (file.startsWith('.claude/capabilities/')) continue;
    const cap = capabilityOf(readText(root, file));
    if (!cap) continue;
    const [slot, impl] = cap.split('/');
    if (!bySlot[slot] || bySlot[slot].selected !== impl) errors.push(`${file}: belongs to unselected implementation ${cap}; unselected implementations must not enter the runtime`);
    else if (listed.get(file) !== cap) errors.push(`${file}: declares ${cap} but is not listed as a facet in its MODULE.md`);
  }
  for (const mod of allModules) {
    const cap = mod.manifest.capability ?? '';
    const [slot, impl] = cap.split('/');
    if (bySlot[slot]?.selected === impl) continue;
    for (const f of mod.manifest.facets ?? []) if (exists(root, f.path) && capabilityOf(readText(root, f.path)) === cap) errors.push(`${f.path}: facet of unselected implementation ${cap} is present in the runtime`);
  }
  // Implementation names must not leak outside their own facets and the allow-list.
  const runtime = runtimeFiles(root);
  // Optional-slot facets are referenced by role elsewhere, so disabling the slot leaves no dangling reference.
  for (const [slot, mod] of Object.entries(modules)) {
    if (contracts[slot]?.status !== 'optional') continue;
    const own = new Set((mod.manifest.facets ?? []).map(f => f.path));
    const names = (mod.manifest.facets ?? []).map(f => path.posix.basename(f.path)).filter(n => n !== 'SKILL.md');
    for (const file of runtime) {
      if (own.has(file) || !file.endsWith('.md')) continue;
      const text = readText(root, file);
      for (const n of names) if (text.includes(n)) errors.push(`${file}: names optional-slot facet ${n}; refer to it by role (resolved in ${SELECTION_FILE}) so the slot can be disabled without dangling references`);
    }
  }
  for (const mod of allModules) {
    const own = new Set((mod.manifest.facets ?? []).map(f => f.path));
    const allow = new Set(mod.manifest.allowList ?? []);
    const terms = (mod.manifest.leakTerms ?? []).map(t => [t, termRegExp(t)]);
    for (const file of runtime) {
      if (own.has(file) || allow.has(file)) continue;
      const lines = readText(root, file).split('\n');
      lines.forEach((line, i) => {
        for (const [term, re] of terms) if (re.test(line)) errors.push(`${file}:${i + 1}: implementation term "${term}" of ${mod.manifest.capability} outside its facets (refer to the slot or facet role instead)`);
      });
    }
  }
}

export function runInstructionChecks(root) {
  const errors = [], warnings = [], info = [];
  for (const f of ['CLAUDE.md', 'docs/technology-stack.md', SELECTION_FILE, '.claude/MAP.md', '.claude/settings.json']) if (!exists(root, f)) errors.push(`missing required file ${f}`);
  if (errors.length) return { errors, warnings, info };
  const instr = instructionFiles(root);
  const skills = skillNames(root);

  for (const file of walk(root, '.claude/rules')) {
    if (file.split('/').length > 3) errors.push(`${file}: rules must stay in the flat .claude/rules/ directory`);
    if (!file.endsWith('.md')) continue;
    const fm = parseFrontmatter(splitFrontmatter(readText(root, file)).fm);
    if (!Array.isArray(fm.paths) || fm.paths.length === 0) errors.push(`${file}: rule must declare a non-empty paths: list`);
    if (!/Loading: path/.test(headerLine(readText(root, file)))) errors.push(`${file}: rule header must state "Loading: path"`);
  }

  for (const file of instr) {
    const text = readText(root, file);
    const header = headerLine(text);
    if (!/^> \*\*[^*]+\*\*[^·]* · /.test(header) || !/Loading:/.test(header)) errors.push(`${file}: first body line must be the one-line header "> **<role>** · … · Loading: …"`);
    if (/(^|[\s·>*])(Level|Kind):/m.test(header) || /^\s*(Level|Kind):/m.test(text)) errors.push(`${file}: Level:/Kind: classification is not used in this instruction system`);
    checkReferences(root, file, text, skills, errors);
  }

  const always = alwaysLoaded(root, errors);
  let chars = 0;
  for (const f of always) chars += readText(root, f).length;
  for (const s of skills) {
    const fm = parseFrontmatter(splitFrontmatter(readText(root, `.claude/skills/${s}/SKILL.md`)).fm);
    if (fm.name !== s) errors.push(`.claude/skills/${s}/SKILL.md: frontmatter name "${fm.name}" must equal the directory name`);
    if (!fm.description) errors.push(`.claude/skills/${s}/SKILL.md: description is required`);
    else if (fm.description.length > 1024) errors.push(`.claude/skills/${s}/SKILL.md: description exceeds 1024 characters`);
    if (fm['disable-model-invocation'] !== 'true') chars += (fm.name ?? '').length + (fm.description ?? '').length + 8;
  }
  if (!skills.includes('template-maintenance')) errors.push('missing user-only template-maintenance workflow');
  else if (parseFrontmatter(splitFrontmatter(readText(root, '.claude/skills/template-maintenance/SKILL.md')).fm)['disable-model-invocation'] !== 'true') errors.push('template-maintenance must set disable-model-invocation: true');

  const agentRel = '.claude/agents/code-reviewer.md';
  if (!exists(root, agentRel)) errors.push(`missing ${agentRel}`);
  else {
    const text = readText(root, agentRel);
    const fm = parseFrontmatter(splitFrontmatter(text).fm);
    chars += (fm.description ?? '').length;
    const denied = String(fm.disallowedTools ?? '');
    if (!/\bWrite\b/.test(denied) || !/\bEdit\b/.test(denied)) errors.push(`${agentRel}: reviewer must be read-only (disallowedTools Write, Edit)`);
    if (!(Array.isArray(fm.skills) && fm.skills.includes('code-review'))) errors.push(`${agentRel}: reviewer must preload the code-review skill`);
    if (splitFrontmatter(text).body.length > 1500) errors.push(`${agentRel}: reviewer must stay a thin wrapper over code-review`);
  }

  const tokens = Math.round(chars / 4);
  info.push(`always-loaded surface ≈ ${tokens} tokens (${[...always].join(', ')} + skill and agent descriptions)`);
  if (tokens > BUDGET_TOKENS) warnings.push(`always-loaded surface ≈ ${tokens} tokens exceeds the ${BUDGET_TOKENS}-token guide; move only non-planning content out`);

  try {
    const settings = JSON.parse(readText(root, '.claude/settings.json'));
    for (const [event, groups] of Object.entries(settings.hooks ?? {})) for (const g of groups) for (const h of g.hooks ?? []) {
      const cmd = h.command ?? '';
      const m = /^node (\.claude\/(?:hooks|scripts)\/[\w./-]+\.mjs)$/.exec(cmd);
      if (!m) errors.push(`.claude/settings.json: ${event} hook command "${cmd}" must be "node .claude/<hooks|scripts>/<file>.mjs" (no shell variables or POSIX syntax)`);
      else if (!exists(root, m[1])) errors.push(`.claude/settings.json: ${event} hook script ${m[1]} does not exist`);
    }
  } catch (e) { errors.push(`.claude/settings.json: ${e.message}`); }

  const map = readText(root, '.claude/MAP.md');
  const mapped = [...instr, ...walk(root, '.claude/hooks'), ...walk(root, '.claude/scripts'), '.claude/settings.json', '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props']
    .filter(f => f !== '.claude/MAP.md' && exists(root, f));
  for (const f of mapped) if (!map.includes(f)) errors.push(`.claude/MAP.md does not list ${f}`);

  checkCapabilities(root, always, instr, errors, warnings);
  return { errors, warnings, info };
}

function main() {
  try {
    const i = process.argv.indexOf('--root');
    const root = resolveRoot(i > 0 ? process.argv[i + 1] : undefined);
    const result = runInstructionChecks(root);
    console.log(report('Instruction structure', result));
    process.exit(result.errors.length ? 1 : 0);
  } catch (e) {
    console.error(`check-instructions: ${e instanceof TemplateError ? e.message : e.stack}`);
    process.exit(2);
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
