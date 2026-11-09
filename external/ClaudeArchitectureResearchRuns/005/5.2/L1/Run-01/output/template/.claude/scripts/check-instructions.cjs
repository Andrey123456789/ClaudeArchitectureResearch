#!/usr/bin/env node
// Level: 3-project | Owns: instruction-structure checker for the level + capability model
// (headers, levels, rule paths, always-loaded imports, slots/modules/facets, selection
// record, leak and platform-vocabulary rules, references, skills, hooks, hygiene).
// Usage: node .claude/scripts/check-instructions.cjs [--verbose]
// Exit codes: 0 pass, 1 violations, 2 environment error.
'use strict';

const fs = require('fs');
const path = require('path');
const lib = require('./lib/project.cjs');

const LEVELS = ['0-core', '1-architecture', '2-technology', '3-project'];
const REQUIRED_WORKFLOWS = ['project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
// Embedded knowledge skills; module-owned knowledge skills are required through `<slot>.knowledge` facets.
const REQUIRED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration',
  'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd',
  'modern-csharp', 'authentication'];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];

// Concrete non-platform technology names forbidden at Levels 0 and 1 (the selected modules'
// leak terms are added at run time).
const NON_PLATFORM = [/\bxUnit\b/, /\bMSTest\b/, /\bnpm\b/i, /Node\.js/, /FluentValidation/, /Serilog/, /Swashbuckle/,
  /\bSwagger\b/, /Mapster/, /\bPolly\b/, /MediatR/, /Kommand/, /\bDocker\b/i, /Kubernetes/, /\bRedis\b/,
  /Testcontainers/, /Playwright/, /Vitest/, /\bRxJS\b/, /TypeScript/, /\bDapper\b/, /PostgreSQL/, /\bSeq\b/,
  /Elasticsearch/, /GitHub Actions/, /Scrutor/, /Newtonsoft/, /WireMock/, /Asp\.Versioning/];
// Instruction artifacts are English-only and carry no Kind taxonomy field.
const CYRILLIC = new RegExp('[' + String.fromCharCode(0x400) + '-' + String.fromCharCode(0x4ff) + ']');
const HYGIENE = [CYRILLIC, /^\s*>?.*\bKind:/m];

function termPattern(term) {
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(?<![A-Za-z0-9])${escaped}`, 'i');
}

function manifestTerms(text, label) {
  const m = new RegExp(`^- ${label}[^:]*:([\\s\\S]*?)(?=\\n- |\\n\\n|\\n#)`, 'm').exec(text);
  return m ? [...m[1].matchAll(/`([^`]+)`/g)].map((x) => x[1]).filter((t) => !t.endsWith('.json') && t !== 'architecture') : [];
}

const violations = [];
const warnings = [];
const fail = (file, message) => violations.push(`${file}: ${message}`);
const warn = (file, message) => warnings.push(`${file}: ${message}`);

function splitFrontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  return m ? { frontmatter: m[1], body: text.slice(m[0].length) } : { frontmatter: null, body: text };
}

function headerOf(text) {
  const { body } = splitFrontmatter(text);
  const line = body.split(/\r?\n/).find((l) => l.trim() !== '') || '';
  return line;
}

function parseHeader(line) {
  const level = /Level: ([0-9a-z-]+)/.exec(line);
  const cap = /Capability: ([a-z-]+)(?:\/([a-z-]+))? \(([^)]+)\)/.exec(line);
  return {
    level: level ? level[1] : null,
    capability: cap ? { slot: cap[1], impl: cap[2] || null, facet: cap[3] } : null,
    loads: (/Loads: ([^|]+)/.exec(line) || [])[1] || '',
  };
}

function frontmatterValue(frontmatter, key) {
  const m = new RegExp(`^${key}:\\s*(.*)$`, 'm').exec(frontmatter || '');
  return m ? m[1].trim() : null;
}

function rulePaths(frontmatter) {
  const m = /^paths:\s*\r?\n((?:\s+-\s+.*\r?\n?)+)/m.exec(frontmatter || '');
  if (!m) return [];
  return m[1].split(/\r?\n/).map((l) => l.trim()).filter((l) => l.startsWith('-'))
    .map((l) => l.replace(/^-\s*/, '').replace(/^["']|["']$/g, ''));
}

function main() {
  const verbose = process.argv.includes('--verbose');
  let root;
  try {
    root = lib.resolveRoot(__dirname);
  } catch (error) {
    console.error(`Instruction check could not run: ${error.message}`);
    process.exit(2);
  }
  const claudeDir = path.join(root, '.claude');
  const rel = (file) => lib.toPosix(path.relative(root, file));
  const read = (file) => lib.readText(file);

  // ---------- artifact list ----------
  const mdFiles = [path.join(root, 'CLAUDE.md'), ...lib.walk(claudeDir, (n) => n.endsWith('.md'))];
  const jsonFiles = lib.walk(claudeDir, (n) => n.endsWith('.json')).filter((f) => path.basename(f) !== 'settings.json');
  const scriptFiles = lib.walk(claudeDir, (n) => n.endsWith('.cjs'));
  const skillDirs = lib.listDirs(path.join(claudeDir, 'skills'));
  const info = new Map(); // rel -> { level, capability, text }

  for (const file of mdFiles) {
    const text = read(file);
    const header = headerOf(text);
    if (!/^> Level: /.test(header) || !/Owns: /.test(header) || !/Scope: /.test(header) || !/Loads: /.test(header)) {
      fail(rel(file), 'missing one-line header "> Level: … | Owns: … | Scope: … | Loads: …".');
    }
    const parsed = parseHeader(header);
    if (!LEVELS.includes(parsed.level)) fail(rel(file), `invalid Level "${parsed.level}".`);
    info.set(rel(file), { ...parsed, text, file });
  }
  for (const file of jsonFiles) {
    const text = read(file);
    let json;
    try { json = JSON.parse(text); } catch (e) { fail(rel(file), `invalid JSON: ${e.message}`); continue; }
    const comment = json.$comment || '';
    const parsed = parseHeader(comment);
    if (!LEVELS.includes(parsed.level) || !/Owns: /.test(comment)) fail(rel(file), '$comment must declare Level and Owns.');
    info.set(rel(file), { ...parsed, text, file });
  }
  for (const file of scriptFiles) {
    const text = read(file);
    const head = text.split(/\r?\n/).slice(0, 3).join('\n');
    const parsed = parseHeader(head);
    if (!LEVELS.includes(parsed.level) || !/Owns: /.test(head)) fail(rel(file), 'first comment lines must declare Level and Owns.');
    info.set(rel(file), { ...parsed, text, file });
  }

  // ---------- rules ----------
  for (const file of lib.walk(path.join(claudeDir, 'rules'), (n) => n.endsWith('.md'))) {
    const r = rel(file);
    const levelDir = r.split('/')[2];
    if (!LEVELS.includes(levelDir)) { fail(r, 'rule is not inside a level directory.'); continue; }
    const { frontmatter } = splitFrontmatter(read(file));
    if (rulePaths(frontmatter).length === 0) fail(r, 'rule must declare a non-empty `paths` list.');
    if (info.get(r).level !== levelDir) fail(r, `header Level ${info.get(r).level} does not match directory ${levelDir}.`);
  }

  // ---------- capabilities ----------
  const capDir = path.join(claudeDir, 'capabilities');
  const slotDirs = lib.listDirs(capDir);
  for (const slot of slotDirs) if (!lib.SLOTS[slot]) fail(`.claude/capabilities/${slot}`, 'unknown slot (only the four agreed slots are allowed).');
  const selected = lib.selectedImplementations(root);
  const modules = {}; // slot -> { impl, facets: Map(facet -> path), binds }
  const contractFacets = {};
  for (const [slot, def] of Object.entries(lib.SLOTS)) {
    const contract = path.join(capDir, slot, 'CONTRACT.md');
    if (!fs.existsSync(contract)) { fail(`.claude/capabilities/${slot}`, 'missing CONTRACT.md.'); continue; }
    contractFacets[slot] = [...read(contract).matchAll(new RegExp(`^\\|\\s*\`(${slot}\\.[a-z-]+)\``, 'gm'))].map((m) => m[1]);
    const impls = selected[slot];
    if (def.required && impls.length !== 1) fail(`.claude/capabilities/${slot}`, `required slot must have exactly one implementation (found ${impls.length}).`);
    if (!def.required && impls.length > 1) fail(`.claude/capabilities/${slot}`, `optional slot may have at most one implementation (found ${impls.length}).`);
    for (const impl of impls) {
      const manifest = path.join(capDir, slot, impl, 'MODULE.md');
      if (!fs.existsSync(manifest)) { fail(`.claude/capabilities/${slot}/${impl}`, 'missing MODULE.md.'); continue; }
      const text = read(manifest);
      const rows = [...text.matchAll(/^\|\s*`([a-z-]+\.[a-z-]+)`\s*\|\s*`([^`]+)`\s*\|\s*([0-9—-]+)\s*\|/gm)];
      const facets = new Map(rows.map((m) => [m[1], m[2]]));
      for (const [, facet, target, lvl] of rows) {
        const facetInfo = info.get(lib.toPosix(target));
        if (facetInfo && /^\d$/.test(lvl) && facetInfo.level !== LEVELS[Number(lvl)]) {
          fail(rel(manifest), `facet ${facet} is listed at level ${lvl} but ${target} declares ${facetInfo.level}.`);
        }
      }
      const bindsLine = (/^- binds: (.*)$/m.exec(text) || [])[1];
      if (!bindsLine) fail(rel(manifest), 'must declare `binds:`.');
      const leakTerms = manifestTerms(text, 'leak terms');
      if (leakTerms.length === 0) fail(rel(manifest), 'must declare `leak terms:`.');
      modules[slot] = { impl, facets, binds: bindsLine || '', leakTerms, bindingTerms: manifestTerms(text, 'binding terms') };
      for (const facet of contractFacets[slot]) {
        if (!facets.has(facet)) fail(rel(manifest), `missing required facet ${facet} (CONTRACT.md).`);
      }
      for (const [facet, target] of facets) {
        if (!facet.startsWith(`${slot}.`)) fail(rel(manifest), `facet ${facet} does not belong to slot ${slot}.`);
        const abs = path.join(root, target);
        if (!fs.existsSync(abs)) { fail(rel(manifest), `facet ${facet} points to missing ${target}.`); continue; }
        const facetInfo = info.get(lib.toPosix(target));
        if (facetInfo && (!facetInfo.capability || facetInfo.capability.slot !== slot || facetInfo.capability.impl !== impl)) {
          fail(target, `must declare "Capability: ${slot}/${impl}".`);
        }
      }
      for (const file of lib.walk(path.join(capDir, slot, impl), () => true)) {
        const i = info.get(rel(file));
        if (i && (!i.capability || i.capability.slot !== slot || i.capability.impl !== impl)) fail(rel(file), `module file must declare "Capability: ${slot}/${impl}".`);
      }
    }
  }
  // every artifact declaring an implementation capability must be listed in that module
  for (const [r, i] of info) {
    if (!i.capability) continue;
    const { slot, impl } = i.capability;
    if (!lib.SLOTS[slot]) { fail(r, `unknown slot in Capability header: ${slot}.`); continue; }
    if (!impl) { if (r !== `.claude/capabilities/${slot}/CONTRACT.md`) fail(r, 'slot-level Capability header is reserved for CONTRACT.md.'); continue; }
    if (!modules[slot] || modules[slot].impl !== impl) { fail(r, `belongs to unselected implementation ${slot}/${impl}.`); continue; }
    const listed = [...modules[slot].facets.values()].includes(r)
      || r.startsWith(`.claude/capabilities/${slot}/${impl}/`)
      || [...modules[slot].facets.values()].some((p) => r.startsWith(path.posix.dirname(p) + '/references/'));
    if (!listed) fail(r, `not listed in .claude/capabilities/${slot}/${impl}/MODULE.md.`);
  }

  // ---------- selection record ----------
  const selectionFile = '.claude/rules/3-project/capability-selection.md';
  const selection = info.get(selectionFile);
  if (!selection) fail(selectionFile, 'missing capability selection record.');
  else {
    const rows = [...selection.text.matchAll(/^\|\s*([a-z-]+)\s*\|\s*(required frame|required leaf|optional leaf)\s*\|\s*([a-z-]+|—)\s*\|\s*(`[a-z-]+`|—)\s*\|/gm)];
    const recorded = new Map(rows.map((m) => [m[1], { impl: m[3], skill: m[4].replace(/`/g, '') }]));
    for (const slot of Object.keys(lib.SLOTS)) {
      const actual = modules[slot] ? modules[slot].impl : '—';
      const row = recorded.get(slot);
      if (!row && actual !== '—') fail(selectionFile, `no row for selected slot ${slot}.`);
      if (row && row.impl !== actual) fail(selectionFile, `${slot} records "${row.impl}" but the shipped implementation is "${actual}".`);
      if (row && modules[slot]) {
        const knowledge = modules[slot].facets.get(`${slot}.knowledge`);
        const skill = knowledge ? knowledge.split('/')[2] : '—';
        if (row.skill !== skill) fail(selectionFile, `${slot} knowledge skill "${row.skill}" does not match module facet "${skill}".`);
      }
    }
  }

  // ---------- always-loaded imports ----------
  const claudeMd = read(path.join(root, 'CLAUDE.md'));
  const imports = [...claudeMd.matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1].replace(/^\.\//, ''));
  for (const imp of imports) {
    if (!fs.existsSync(path.join(root, imp))) { fail('CLAUDE.md', `import does not resolve: ${imp}.`); continue; }
    const i = info.get(imp);
    if (!i || !/always/.test(i.loads)) fail(imp, 'imported by CLAUDE.md but header does not say "Loads: always".');
  }
  for (const [r, i] of info) {
    if (r.startsWith('.claude/rules/') && /always/.test(i.loads) && !imports.includes(r)) fail(r, 'declares "Loads: always" but is not imported by CLAUDE.md.');
  }
  for (const [slot, m] of Object.entries(modules)) {
    const decision = m.facets.get(`${slot}.decision`);
    if (decision && !imports.includes(decision)) fail('CLAUDE.md', `must import the selected decision facet ${decision}.`);
  }
  for (const imp of imports) {
    const i = info.get(imp);
    if (i && i.capability && i.capability.impl && !/\.decision$/.test(i.capability.facet)) fail(imp, 'only decision facets of modules may be always-loaded.');
  }

  // ---------- skills and agent ----------
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_KNOWLEDGE]) {
    if (!skillDirs.includes(name)) fail('.claude/skills', `missing required skill ${name}.`);
  }
  for (const name of FORBIDDEN_SKILLS) if (skillDirs.includes(name)) fail(`.claude/skills/${name}`, 'standalone skill duplicates a private reference of another skill.');
  for (const name of skillDirs) {
    const file = path.join(claudeDir, 'skills', name, 'SKILL.md');
    if (!fs.existsSync(file)) { fail(`.claude/skills/${name}`, 'missing SKILL.md.'); continue; }
    const { frontmatter } = splitFrontmatter(read(file));
    if (frontmatterValue(frontmatter, 'name') !== name) fail(rel(file), 'frontmatter name must equal the directory name.');
    if (!/^description:/m.test(frontmatter || '')) fail(rel(file), 'missing description.');
  }
  const tm = path.join(claudeDir, 'skills', 'template-maintenance', 'SKILL.md');
  if (fs.existsSync(tm) && frontmatterValue(splitFrontmatter(read(tm)).frontmatter, 'disable-model-invocation') !== 'true') {
    fail(rel(tm), 'must set disable-model-invocation: true (user-only).');
  }
  const agent = path.join(claudeDir, 'agents', 'code-reviewer.md');
  if (!fs.existsSync(agent) || !/code-review\/SKILL\.md/.test(read(agent))) fail('.claude/agents/code-reviewer.md', 'thin reviewer agent must exist and delegate to the code-review skill.');
  // skill-private references are used only by their owning skill
  for (const name of skillDirs) {
    for (const ref of lib.walk(path.join(claudeDir, 'skills', name, 'references'), (n) => n.endsWith('.md'))) {
      const needle = `references/${path.basename(ref)}`;
      for (const [r, i] of info) {
        if (r.startsWith(`.claude/skills/${name}/`) || r === '.claude/INSTRUCTION-MAP.md') continue;
        if (i.text.includes(needle)) fail(r, `depends on skill-private reference ${name}/${needle}.`);
      }
    }
  }

  // ---------- leak, frame terms, platform vocabulary, references, hygiene ----------
  const skillNames = new Set(skillDirs);
  const ruleBasenames = new Map();
  for (const file of lib.walk(path.join(claudeDir, 'rules'), (n) => n.endsWith('.md'))) ruleBasenames.set(path.basename(file), rel(file));
  const knownMd = new Set(['SPECIFICATION.md', 'CUSTOM_SETTINGS.md', 'CLAUDE.md', 'MODULE.md', 'CONTRACT.md', 'SKILL.md', 'INSTRUCTION-MAP.md']);
  const bindsArchitecture = new Set(Object.entries(modules).filter(([, m]) => /architecture/.test(m.binds)).map(([s, m]) => `${s}/${m.impl}`));
  const unknownTokens = new Set();

  const implementationPatterns = {};
  for (const [slot, m] of Object.entries(modules)) implementationPatterns[`${slot}/${m.impl}`] = m.leakTerms.map(termPattern);
  const frame = modules.architecture;
  const frameTerms = frame ? frame.bindingTerms.map(termPattern) : [];
  if (frame) {
    const spec = lib.readJson(path.join(capDir, 'architecture', frame.impl, 'check.json'));
    const layers = [...spec.projects, ...spec.testProjects].map((p) => p.suffix.replace(/^\./, '').replace(/\./g, '\\.'));
    frameTerms.push(new RegExp(`(?:<Name>|MyApp|ProjectName)\\.(?:${layers.join('|')})\\b`));
  }
  const allLeakPatterns = Object.values(implementationPatterns).flat();
  const self = '.claude/scripts/check-instructions.cjs';
  for (const [r, i] of info) {
    const owner = i.capability && i.capability.impl ? `${i.capability.slot}/${i.capability.impl}` : null;
    const exempt = r === selectionFile || r === '.claude/INSTRUCTION-MAP.md';
    // strip inline references to skill names before vocabulary checks
    const scrubbed = i.text.replace(/`([a-z0-9-]+)`/g, (m, token) => (skillNames.has(token) ? '`skill`' : m))
      .replace(/\.claude\/[^\s`)]+/g, '');
    if (!exempt) {
      for (const [impl, patterns] of Object.entries(implementationPatterns)) {
        if (owner === impl || (r.startsWith('.claude/capabilities/') && r.includes(`/${impl}/`))) continue;
        for (const p of patterns) if (p.test(scrubbed)) fail(r, `names implementation ${impl} outside its module (${p}).`);
      }
      const frameOwner = frame ? `architecture/${frame.impl}` : null;
      if (owner !== frameOwner && !bindsArchitecture.has(owner)) {
        for (const p of frameTerms) if (p.test(i.text)) fail(r, `uses architecture-frame term outside the frame (${p}).`);
      }
    }
    if ((i.level === '0-core' || i.level === '1-architecture') && !r.endsWith('.json') && !r.endsWith('.cjs') && r !== '.claude/INSTRUCTION-MAP.md') {
      const owned = owner ? implementationPatterns[owner] || [] : [];
      for (const p of [...NON_PLATFORM, ...allLeakPatterns.filter((x) => !owned.includes(x))]) {
        if (p.test(scrubbed)) fail(r, `Level ${i.level} names a non-platform technology (${p}).`);
      }
    }
    for (const p of HYGIENE) {
      if (r !== self && p.test(i.text)) fail(r, `hygiene: non-English script or Kind taxonomy field (${p}).`);
    }

    if (!r.endsWith('.md')) continue;
    for (const m of i.text.matchAll(/\.claude\/[\w./-]*[\w/]/g)) {
      const target = path.join(root, m[0]);
      if (!fs.existsSync(target)) fail(r, `path reference does not resolve: ${m[0]}.`);
    }
    for (const m of i.text.matchAll(/`([^`\n]+)`/g)) {
      const token = m[1].trim();
      if (token.includes('<') || token.includes('*') || /\s/.test(token)) continue;
      if (/^\.claude\//.test(token) || /^(rules|skills|capabilities|agents|hooks|scripts)\//.test(token)) {
        const target = token.startsWith('.claude/') ? path.join(root, token) : path.join(claudeDir, token);
        if (!fs.existsSync(target.replace(/\/$/, ''))) fail(r, `reference does not resolve: ${token}.`);
      } else if (/^\d-[a-z]+\/[\w.-]+\.md$/.test(token)) {
        if (!fs.existsSync(path.join(claudeDir, 'rules', token))) fail(r, `rule reference does not resolve: ${token}.`);
      } else if (/^[\w.-]+\.md$/.test(token)) {
        if (!knownMd.has(token) && !ruleBasenames.has(token)
          && !fs.existsSync(path.join(path.dirname(i.file), token))
          && !fs.existsSync(path.join(path.dirname(i.file), 'references', token))) fail(r, `file reference does not resolve: ${token}.`);
      } else if (/^[\w.-]+\.cjs$/.test(token)) {
        if (!fs.existsSync(path.join(claudeDir, 'scripts', token)) && !fs.existsSync(path.join(claudeDir, 'hooks', token))) fail(r, `script reference does not resolve: ${token}.`);
      } else if (/^(architecture|persistence|backend-testing|frontend)\.[a-z-]+$/.test(token)) {
        const slot = token.split('.')[0];
        if (!(contractFacets[slot] || []).includes(token)) fail(r, `facet reference ${token} is not defined by the slot contract.`);
      } else if (/^[a-z][a-z0-9]*(-[a-z0-9]+)+$/.test(token) && !skillNames.has(token)) {
        unknownTokens.add(token);
      }
    }
  }

  // routing table in CLAUDE.md must name existing skills
  for (const m of claudeMd.matchAll(/^\|[^|\n]+\|\s*`([a-z-]+)`/gm)) {
    if (!skillNames.has(m[1])) fail('CLAUDE.md', `routes to unknown skill ${m[1]}.`);
  }

  // ---------- hooks ----------
  let settings;
  try { settings = JSON.parse(read(path.join(claudeDir, 'settings.json'))); } catch (e) { fail('.claude/settings.json', `invalid JSON: ${e.message}`); }
  if (settings) {
    for (const groups of Object.values(settings.hooks || {})) {
      for (const group of groups) {
        for (const hook of group.hooks || []) {
          const cmd = hook.command || '';
          if (/[$%]/.test(cmd)) fail('.claude/settings.json', `hook command relies on shell variable expansion: ${cmd}`);
          if (/[|&<>^]/.test(cmd)) fail('.claude/settings.json', `hook command contains shell metacharacters: ${cmd}`);
          const script = (/(\.claude\/hooks\/[\w.-]+\.cjs)/.exec(cmd) || [])[1];
          if (!script || !fs.existsSync(path.join(root, script))) fail('.claude/settings.json', `hook script missing or not referenced: ${cmd}`);
        }
      }
    }
  }

  if (verbose && unknownTokens.size) warn('(info)', `kebab-case tokens that are not skills: ${[...unknownTokens].sort().join(', ')}`);
  for (const w of warnings) console.log(`warning: ${w}`);
  if (violations.length) {
    console.log(`Instruction structure check: ${violations.length} violation(s)`);
    for (const v of violations) console.log(`  - ${v}`);
    process.exit(1);
  }
  console.log(`Instruction structure check: PASS (${info.size} artifacts, ${skillDirs.length} skills, ${Object.keys(modules).length} selected modules)`);
}

main();
