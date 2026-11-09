#!/usr/bin/env node
'use strict';
// Instruction-structure checker for this template's instruction system:
// flat path rules, ownership headers, skills and agent, imports and internal
// references, the four capability slots (selection, manifests, facets,
// implementation-name leaks, workflow facet roles, binds), hook commands, the
// human map, and the always-loaded size.
// Procedure owner: template-maintenance workflow.
// Usage: node .claude/scripts/check-instructions.js [--quiet]

const common = require('./lib/common.js');

const SLOTS = ['architecture', 'persistence', 'backend-testing', 'frontend'];
const REQUIRED_SLOTS = ['architecture', 'persistence', 'backend-testing'];
const REQUIRED_WORKFLOWS = [
  'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow',
  'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance', 'development-workflow',
];
const REQUIRED_EMBEDDED_KNOWLEDGE = [
  'http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration', 'dependency-injection',
  'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication',
];
const USER_ONLY_SKILLS = ['template-maintenance'];
const BUDGET_TOKENS = 6500;
const ALLOW_ALL_TOKENS = [common.SELECTION_FILE, '.claude/MAP.md'];

const findings = [];
const add = (level, file, message) => findings.push({ level, file, message });

// Instruction artifacts: CLAUDE.md, the files it imports, and everything under .claude/.
// Other docs/ content (project documentation, ADRs) is not an instruction layer.
function instructionFiles() {
  const files = ['CLAUDE.md', ...claudeImports().filter((f) => f.endsWith('.md'))];
  files.push(...common.walk('.claude').filter((f) => f.endsWith('.md')));
  return [...new Set(files)].filter((f) => common.exists(f));
}

function isInstructionPath(rel) {
  return rel === 'CLAUDE.md' || rel.startsWith('.claude/') || claudeImports().includes(rel);
}

// Template enforcement code is scanned for implementation-name leaks; root project
// configuration (.editorconfig, Directory.*.props) legitimately names packages and is not.
function enforcementFiles() {
  return common.walk('.claude').filter((f) => /\.(js|json)$/.test(f));
}

const ROOT_CONFIG = ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'];

function stripCode(text) {
  return text.replace(/```[\s\S]*?```/g, '');
}

function flatten(text) {
  return stripCode(common.parseFrontMatter(text).body).replace(/\r?\n(?!\r?\n)/g, ' ');
}

// ---------- headers and classification ----------
function checkHeaders(files) {
  for (const f of files) {
    const text = common.readText(f);
    const header = common.firstContentLine(text);
    if (!header.startsWith('> ')) add('ERROR', f, 'missing one-line classification/ownership header (first content line must start with "> ").');
    if (/(^|\n)\s*>?\s*(Level|Kind):/.test(text) || /·\s*(Level|Kind):/.test(header)) {
      add('ERROR', f, 'uses a Level:/Kind: classification, which this instruction system does not use.');
    }
  }
}

// ---------- rules ----------
function checkRules() {
  for (const f of common.walk('.claude/rules')) {
    if (f.split('/').length > 3) add('ERROR', f, 'rules must stay flat in .claude/rules/ (no level- or scope-first subdirectories).');
    if (!f.endsWith('.md')) continue;
    const fm = common.parseFrontMatter(common.readText(f));
    const paths = fm.data.paths;
    if (!fm.hasFrontMatter || !Array.isArray(paths) || paths.length === 0) add('ERROR', f, 'rule file must declare a non-empty paths: list.');
  }
}

// ---------- skills and agent ----------
function skillNames() {
  return common.walk('.claude/skills').filter((f) => /^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(f)).map((f) => f.split('/')[2]);
}

function checkSkills(modules) {
  const names = skillNames();
  for (const name of names) {
    const file = `.claude/skills/${name}/SKILL.md`;
    const fm = common.parseFrontMatter(common.readText(file));
    if (fm.data.name !== name) add('ERROR', file, `front-matter name "${fm.data.name || ''}" must equal the directory name "${name}".`);
    if (!fm.data.description || String(fm.data.description).length < 20) add('ERROR', file, 'skill needs a concrete description.');
    if (USER_ONLY_SKILLS.includes(name) && fm.data['disable-model-invocation'] !== 'true') {
      add('ERROR', file, 'user-only workflow must set disable-model-invocation: true.');
    }
  }
  for (const f of common.walk('.claude/skills')) {
    const parts = f.split('/');
    if (parts.length > 4 && parts[3] !== 'references') add('ERROR', f, 'skill-private files belong in the skill\'s references/ directory.');
  }
  for (const w of REQUIRED_WORKFLOWS) if (!names.includes(w)) add('ERROR', '.claude/skills', `required workflow skill missing: ${w}`);
  for (const k of REQUIRED_EMBEDDED_KNOWLEDGE) if (!names.includes(k)) add('ERROR', '.claude/skills', `required knowledge skill missing: ${k}`);
  for (const m of modules) {
    for (const facet of [...(m.manifest.facets.knowledge || []), ...(m.manifest.facets.workflow || [])]) {
      if (!common.exists(facet)) add('ERROR', m.file, `facet skill missing: ${facet}`);
    }
  }
  const agent = '.claude/agents/code-reviewer.md';
  if (!common.exists(agent)) {
    add('ERROR', '.claude/agents', 'code-reviewer agent missing.');
  } else {
    const fm = common.parseFrontMatter(common.readText(agent));
    const disallowed = String(fm.data.disallowedTools || '');
    if (!/\bWrite\b/.test(disallowed) || !/\bEdit\b/.test(disallowed)) add('ERROR', agent, 'code-reviewer must be read-only (disallowedTools includes Write and Edit).');
    const skills = Array.isArray(fm.data.skills) ? fm.data.skills : String(fm.data.skills || '').split(',').map((s) => s.trim());
    if (!skills.includes('code-review')) add('ERROR', agent, 'code-reviewer must preload the code-review workflow (skills: code-review).');
  }
}

// ---------- imports and references ----------
function claudeImports() {
  return common.readText('CLAUDE.md').split(/\r?\n/).filter((l) => /^@\S+/.test(l.trim())).map((l) => l.trim().slice(1));
}

function checkImports(files) {
  for (const imp of claudeImports()) {
    if (!common.exists(imp)) add('ERROR', 'CLAUDE.md', `import does not resolve: @${imp}`);
  }
  for (const f of files) {
    if (f === 'CLAUDE.md') continue;
    const body = stripCode(common.readText(f));
    for (const line of body.split(/\r?\n/)) {
      if (/^@[\w./-]+\.md\s*$/.test(line.trim())) add('ERROR', f, `nested import "${line.trim()}": import always-loaded files directly from CLAUDE.md.`);
    }
  }
}

function resolveRef(token, fromFile) {
  const clean = token.replace(/#.*$/, '').replace(/\/$/, '');
  const dir = fromFile.includes('/') ? fromFile.slice(0, fromFile.lastIndexOf('/')) : '.';
  const candidates = [clean, `${dir}/${clean}`, `.claude/rules/${clean}`];
  const skillDir = /^\.claude\/skills\/[^/]+/.exec(fromFile);
  if (skillDir) candidates.push(`${skillDir[0]}/${clean}`);
  return candidates.find((c) => common.exists(c)) || null;
}

function looksLikeInstructionRef(token) {
  if (/[<>*\s]|NNNN|\.\.\.|^https?:|=|\(|::/.test(token)) return false;
  if (/^(\.claude|docs)\//.test(token)) return !token.startsWith('docs/decisions/');
  if (/^references\/.+/.test(token)) return true;
  if (/^(CLAUDE|SPECIFICATION|CUSTOM_SETTINGS)\.md$/.test(token)) return true;
  return /^[a-z][a-z0-9-]*\.md$/.test(token);
}

function skillTarget(name) {
  const skill = `.claude/skills/${name}/SKILL.md`;
  if (common.exists(skill)) return skill;
  const agent = `.claude/agents/${name}.md`;
  return common.exists(agent) ? agent : null;
}

function hasHeading(file, wanted) {
  const target = common.normalizeHeading(wanted);
  return common.headings(common.readText(file)).some((h) => common.normalizeHeading(h) === target);
}

// Role-named facet locations of a disabled optional slot. Embedded instructions refer to
// them only for work in that slot's scope, so clearing the selection leaves them inactive
// rather than broken.
function inactiveFacetLocations() {
  const inactive = new Set();
  let rows = [];
  try {
    rows = common.readSelection();
  } catch {
    return inactive;
  }
  for (const row of rows) {
    if (row.status !== 'disabled') continue;
    const file = `.claude/capabilities/${row.slot}/CONTRACT.md`;
    if (!common.exists(file)) continue;
    const contract = common.extractJsonBlock(common.readText(file)) || {};
    for (const location of Object.values(contract.requiredFacets || {})) {
      if (location) {
        inactive.add(location);
        inactive.add(location.split('/').pop());
      }
    }
  }
  return inactive;
}

function checkReferences(files) {
  const names = skillNames();
  const inactive = inactiveFacetLocations();
  const isInactive = (t) => inactive.has(t.replace(/#.*$/, ''));
  for (const f of files) {
    const raw = common.readText(f);
    const flat = flatten(raw);
    const tokens = [...flat.matchAll(/`([^`\n]+)`/g)].map((m) => m[1]);
    for (const t of tokens) {
      if (looksLikeInstructionRef(t) && !resolveRef(t, f) && !isInactive(t)) add('ERROR', f, `reference does not resolve: ${t}`);
    }
    for (const m of flat.matchAll(/`([a-z][a-z0-9-]*)`\s+(workflow|skill|agent)\b/g)) {
      if (!skillTarget(m[1])) add('ERROR', f, `${m[2]} reference does not resolve: ${m[1]}`);
    }
    for (const m of flat.matchAll(/`([^`\n]+)`(?:\s+(?:workflow|skill|rule))?\s+§\s+([^.;:,)`§]+)/g)) {
      const target = names.includes(m[1]) ? `.claude/skills/${m[1]}/SKILL.md` : resolveRef(m[1], f);
      if (!target) {
        if (!isInactive(m[1])) add('ERROR', f, `section reference target does not resolve: ${m[1]}`);
        continue;
      }
      const words = m[2].trim().split(/\s+/);
      let ok = false;
      for (let n = words.length; n > 0 && !ok; n--) ok = hasHeading(target, words.slice(0, n).join(' '));
      if (!ok) add('ERROR', f, `section reference does not resolve: ${m[1]} § ${m[2].trim()}`);
    }
  }
  const routing = /## Workflow Routing([\s\S]*?)(\n## |$)/.exec(common.readText('CLAUDE.md'));
  if (!routing) {
    add('ERROR', 'CLAUDE.md', 'missing the Workflow Routing section.');
  } else {
    for (const m of routing[1].matchAll(/`\/?([a-z][a-z0-9-]*)`/g)) {
      if (!skillTarget(m[1])) add('ERROR', 'CLAUDE.md', `routing target does not exist: ${m[1]}`);
    }
  }
}

function checkAnchor(ref, fromFile) {
  const [file, anchor] = ref.split('#');
  if (!common.exists(file)) {
    add('ERROR', fromFile, `manifest path does not resolve: ${file}`);
    return;
  }
  if (anchor && !common.headings(common.readText(file)).some((h) => common.slugify(h) === anchor)) {
    add('ERROR', fromFile, `manifest anchor does not resolve: ${ref}`);
  }
}

// ---------- capabilities ----------
function tokenRegex(token) {
  const esc = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pre = /^[A-Za-z0-9]/.test(token) ? '(?<![A-Za-z0-9])' : '';
  const post = /[A-Za-z0-9]$/.test(token) ? '(?![A-Za-z0-9])' : '';
  return new RegExp(`${pre}${esc}${post}`);
}

function findTokens(text, tokens) {
  const hits = [];
  text.split(/\r?\n/).forEach((line, i) => {
    for (const t of tokens) if (tokenRegex(t).test(line)) hits.push({ line: i + 1, token: t });
  });
  return hits;
}

function checkCapabilities(files) {
  let rows;
  try {
    rows = common.readSelection();
  } catch (e) {
    add('ERROR', common.SELECTION_FILE, `cannot read the capability selection record: ${e.message}`);
    return [];
  }
  const contractDirs = common.walk('.claude/capabilities').filter((f) => /\/CONTRACT\.md$/.test(f)).map((f) => f.split('/')[2]);
  for (const slot of contractDirs) if (!SLOTS.includes(slot)) add('ERROR', `.claude/capabilities/${slot}`, 'only the four agreed capability slots are allowed.');
  for (const slot of SLOTS) if (!contractDirs.includes(slot)) add('ERROR', `.claude/capabilities/${slot}`, 'slot contract missing.');
  for (const row of rows) if (!SLOTS.includes(row.slot)) add('ERROR', common.SELECTION_FILE, `unknown slot in selection: ${row.slot}`);

  const modules = [];
  for (const slot of SLOTS) {
    const slotRows = rows.filter((r) => r.slot === slot);
    if (slotRows.length !== 1) {
      add('ERROR', common.SELECTION_FILE, `slot ${slot} must appear exactly once (found ${slotRows.length}).`);
      continue;
    }
    const row = slotRows[0];
    const impl = common.selectedImplementation(row);
    if (/[,;]|\band\b|\//.test(row.implementation)) add('ERROR', common.SELECTION_FILE, `slot ${slot} lists more than one implementation.`);
    if (REQUIRED_SLOTS.includes(slot) && !impl) add('ERROR', common.SELECTION_FILE, `required slot ${slot} has no selected implementation.`);
    if (!REQUIRED_SLOTS.includes(slot) && !impl && row.status !== 'disabled') add('ERROR', common.SELECTION_FILE, `optional slot ${slot} must be selected or disabled.`);
    if (!impl) continue;
    const contractFile = `.claude/capabilities/${slot}/CONTRACT.md`;
    const moduleFile = `.claude/capabilities/${slot}/${impl}/MODULE.md`;
    if (!common.exists(moduleFile)) {
      add('ERROR', moduleFile, 'manifest of the selected implementation is missing.');
      continue;
    }
    let contract;
    let manifest;
    try {
      contract = common.extractJsonBlock(common.readText(contractFile));
      manifest = common.extractJsonBlock(common.readText(moduleFile));
    } catch (e) {
      add('ERROR', moduleFile, `cannot parse manifest/contract JSON: ${e.message}`);
      continue;
    }
    if (!contract || !manifest) {
      add('ERROR', moduleFile, 'contract or manifest JSON block missing.');
      continue;
    }
    if (manifest.slot !== slot || manifest.implementation !== impl) add('ERROR', moduleFile, 'manifest slot/implementation does not match its location.');
    const module = { slot, implementation: impl, file: moduleFile, manifest };
    modules.push(module);
    const facets = manifest.facets || {};
    for (const [facet, location] of Object.entries(contract.requiredFacets || {})) {
      const listed = facets[facet] || [];
      if (!listed.length) add('ERROR', moduleFile, `required facet missing: ${facet}`);
      if (location && !listed.includes(location)) add('ERROR', moduleFile, `facet ${facet} must use the role-named location ${location}`);
    }
    for (const [facet, list] of Object.entries(facets)) {
      for (const file of list) {
        if (!common.exists(file)) {
          add('ERROR', moduleFile, `facet ${facet} file missing: ${file}`);
          continue;
        }
        const cap = common.capabilityOf(common.readText(file));
        if (!cap || cap.slot !== slot || cap.implementation !== impl) add('ERROR', file, `facet header must declare Capability: ${slot}/${impl}`);
      }
    }
    for (const p of contract.requiredProperties || []) if (!(manifest.properties || {})[p]) add('ERROR', moduleFile, `required property missing: ${p}`);
    for (const e of contract.requiredEnforcement || []) if (!(manifest.enforcement || {})[e]) add('ERROR', moduleFile, `required enforcement data missing: ${e}`);
    for (const v of Object.values(manifest.properties || {})) if (/^[.\w/-]+\.md#[\w-]+$/.test(v)) checkAnchor(v, moduleFile);
    for (const ref of manifest.providerVariantSections || []) checkAnchor(ref, moduleFile);
  }

  // Facet ownership: every Capability header belongs to a selected module and is listed in its manifest.
  for (const f of files) {
    const cap = common.capabilityOf(common.readText(f));
    if (!cap) continue;
    const m = modules.find((x) => x.slot === cap.slot && x.implementation === cap.implementation);
    if (!m) {
      add('ERROR', f, `declares Capability: ${cap.slot}/${cap.implementation}, which is not selected (unselected implementations must not enter runtime).`);
      continue;
    }
    const listed = Object.values(m.manifest.facets || {}).flat();
    if (f !== m.file && !listed.includes(f) && !f.startsWith(`.claude/capabilities/${cap.slot}/${cap.implementation}/`)) {
      add('ERROR', f, `capability-owned file is not listed in ${m.file}.`);
    }
  }

  // Planning facets are imported from CLAUDE.md exactly for the selected slots.
  const imports = claudeImports();
  for (const slot of SLOTS) {
    const planning = `docs/capabilities/${slot}.md`;
    const m = modules.find((x) => x.slot === slot);
    if (m && !imports.includes(planning)) add('ERROR', 'CLAUDE.md', `planning facet of selected slot ${slot} is not imported: @${planning}`);
    if (!m && imports.includes(planning)) add('ERROR', 'CLAUDE.md', `planning facet of unselected slot ${slot} is still imported.`);
    if (!m && common.exists(planning)) add('ERROR', planning, `slot ${slot} is not selected; remove its planning facet.`);
  }

  // Implementation-name leaks, workflow facet roles, and binds.
  const frame = modules.find((m) => m.slot === 'architecture');
  const detailTokens = (frame && frame.manifest.enforcement && frame.manifest.enforcement.detailTokens) || [];
  const scanned = [...files, ...enforcementFiles()].filter((f) => !ALLOW_ALL_TOKENS.includes(f) && !f.startsWith('.claude/capabilities/'));
  const usedBinds = new Map();
  for (const f of scanned) {
    const text = common.readText(f);
    const owner = common.capabilityOf(text);
    const isWorkflow = /^>\s*Workflow\b/.test(common.firstContentLine(text));
    for (const m of modules) {
      if (owner && owner.slot === m.slot) continue;
      for (const hit of findTokens(text, m.manifest.leakTokens || [])) {
        if (owner) {
          const binds = ((modules.find((x) => x.slot === owner.slot) || {}).manifest || {}).binds || [];
          if (binds.some((b) => b.target === `${m.slot}/${m.implementation}`)) continue;
          add('ERROR', `${f}:${hit.line}`, `"${hit.token}" names ${m.slot}/${m.implementation} without a declared binds entry.`);
        } else {
          const what = isWorkflow ? 'workflow bypasses the facet role and hardcodes' : 'names';
          add('ERROR', `${f}:${hit.line}`, `${what} the selected ${m.slot} implementation ("${hit.token}"); refer to the slot or facet role instead.`);
        }
      }
    }
    if (owner && owner.slot !== 'architecture') {
      const hits = findTokens(text, detailTokens);
      if (hits.length) usedBinds.set(owner.slot, true);
      const m = modules.find((x) => x.slot === owner.slot);
      const bindsFrame = m && (m.manifest.binds || []).some((b) => frame && b.target === `architecture/${frame.implementation}`);
      if (hits.length && !bindsFrame) add('ERROR', `${f}:${hits[0].line}`, `uses frame-specific names ("${hits[0].token}") without declaring binds to the architecture frame.`);
    }
  }
  for (const m of modules) {
    for (const b of m.manifest.binds || []) {
      const [slot, impl] = String(b.target).split('/');
      if (!modules.some((x) => x.slot === slot && x.implementation === impl)) add('ERROR', m.file, `binds target is not selected: ${b.target}`);
      if (!b.reason) add('ERROR', m.file, `binds entry needs a reason: ${b.target}`);
      if (slot === 'architecture' && !usedBinds.get(m.slot)) add('WARN', m.file, 'declares binds to the frame but no facet uses frame-specific names.');
    }
  }
  return modules;
}

// ---------- hooks, map, budget ----------
function checkSettings() {
  const file = '.claude/settings.json';
  if (!common.exists(file)) {
    add('ERROR', file, 'settings file missing.');
    return;
  }
  let settings;
  try {
    settings = JSON.parse(common.readText(file));
  } catch (e) {
    add('ERROR', file, `invalid JSON: ${e.message}`);
    return;
  }
  for (const [event, groups] of Object.entries(settings.hooks || {})) {
    for (const group of groups) {
      for (const hook of group.hooks || []) {
        const cmd = String(hook.command || '');
        if (/\$\{?[A-Za-z_]|%[A-Za-z_]+%/.test(cmd)) add('ERROR', file, `${event} hook command relies on shell variable expansion: ${cmd}`);
        const script = /'(\.claude\/hooks\/[\w.-]+\.js)'/.exec(cmd);
        if (!script) add('ERROR', file, `${event} hook command does not name a .claude/hooks script: ${cmd}`);
        else if (!common.exists(script[1])) add('ERROR', file, `${event} hook script missing: ${script[1]}`);
      }
    }
  }
}

function checkMap(files) {
  const mapFile = '.claude/MAP.md';
  if (!common.exists(mapFile)) {
    add('ERROR', mapFile, 'human map missing.');
    return;
  }
  const map = common.readText(mapFile);
  const listed = [...files, ...enforcementFiles(), ...ROOT_CONFIG.filter((f) => common.exists(f)), 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md'];
  for (const f of listed) {
    if (f === mapFile) continue;
    const short = f.replace(/^\.claude\//, '');
    if (!map.includes(f) && !map.includes(short)) add('ERROR', mapFile, `map does not list ${f}`);
  }
}

function alwaysLoadedTokens() {
  let chars = common.readText('CLAUDE.md').length;
  for (const imp of claudeImports()) if (common.exists(imp)) chars += common.readText(imp).length;
  for (const name of skillNames()) {
    const fm = common.parseFrontMatter(common.readText(`.claude/skills/${name}/SKILL.md`));
    if (fm.data['disable-model-invocation'] === 'true') continue;
    chars += name.length + String(fm.data.description || '').length + 8;
  }
  for (const f of common.walk('.claude/agents')) {
    const fm = common.parseFrontMatter(common.readText(f));
    chars += String(fm.data.description || '').length + 16;
  }
  return Math.round(chars / 4);
}

function main() {
  common.projectRoot();
  const files = instructionFiles();
  checkHeaders(files);
  checkRules();
  checkImports(files);
  checkReferences(files);
  const modules = checkCapabilities(files);
  checkSkills(modules);
  checkSettings();
  checkMap(files);
  const tokens = alwaysLoadedTokens();
  if (tokens > BUDGET_TOKENS) add('WARN', 'CLAUDE.md', `always-loaded surface is about ${tokens} tokens (target ${BUDGET_TOKENS}).`);
  return { tokens, files: files.length };
}

module.exports = {
  isInstructionPath,
  run: () => {
    findings.length = 0;
    const r = main();
    return { ...r, findings: [...findings] };
  },
};

if (require.main === module) {
  try {
    const { tokens, files } = main();
    const quiet = process.argv.includes('--quiet');
    if (findings.length) console.log(common.formatFindings(findings));
    const errors = findings.filter((f) => f.level === 'ERROR').length;
    if (!quiet || errors) console.log(`check-instructions: ${files} instruction file(s), always-loaded ~${tokens} tokens, ${errors} error(s), ${findings.length - errors} warning(s)`);
    process.exit(errors ? 1 : 0);
  } catch (e) {
    console.error(`check-instructions: cannot run: ${e.message}`);
    process.exit(2);
  }
}
