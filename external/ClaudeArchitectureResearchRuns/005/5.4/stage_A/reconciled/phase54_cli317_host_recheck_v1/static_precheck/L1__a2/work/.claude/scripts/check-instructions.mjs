#!/usr/bin/env node
// Instruction-structure checker for the level-first instruction system with replaceable capabilities.
// Validates: headers and levels, rule paths, conformance direction, capability selection, slot contracts,
// module manifests (facets, binds, leak tokens, frame terms), facet ownership, always-loaded imports,
// implementation-name leakage, Core/Architecture technology neutrality, references, required
// workflows/knowledge, agent, hook registrations, map coverage.
// Usage (from any directory of the project or a linked worktree):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"   (exit 1 on violations, 2 on setup errors)
import { existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { listFiles, parseSelection, readText, resolveRoot, toPosix } from './lib/project.mjs';

const LEVELS = ['0-core', '1-architecture', '2-technology', '3-project'];
const SLOTS = { architecture: 'required frame', persistence: 'required leaf', 'backend-testing': 'required leaf', frontend: 'optional leaf' };
const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
const REQUIRED_SHARED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration',
  'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication'];
const LEAK_ALLOWED = new Set(['.claude/rules/3-project/decisions.md', '.claude/INSTRUCTION_MAP.md']);

// Core/Architecture neutrality: Levels 0/1 name no concrete implementation technology in any form, from prose to
// a pure pointer (heading, list, table row, code span or fence, link, frontmatter, or wrapper such as
// `Technique: <skill>`, `See <skill>`, `area → <skill>`). There is no pointer or context exemption. Fixed platform
// (allowed): .NET, C#, TypeScript, Git, and HTTP as protocol vocabulary; ASP.NET (Core) and NuGet are NOT exempt.
// Neutral role, capability, facet and topic references stay allowed (`backend-testing.framework`, `http-api`): a
// Level-2 skill name is technology only when it names one (`docker`, `ef-core`, `aspnet-error-handling`).
// Recognized technology = this lexicon + leaf-module leak tokens and enforcement package ids derived from the
// template + deny-by-default API-shaped identifiers. A product name in none of these is left to content review.
const TECHNOLOGY_LEXICON = ['Docker', 'Dockerfile', 'Docker Compose', 'Kubernetes', 'Swagger', 'Swashbuckle', 'OpenAPI', 'NSwag',
  'Serilog', 'NLog', 'log4net', 'FluentValidation', 'Mapster', 'AutoMapper', 'MediatR', 'Kommand', 'Scrutor', 'Polly', 'Testcontainers',
  'xUnit', 'MSTest', 'TUnit', 'Moq', 'NSubstitute', 'FluentAssertions', 'Playwright', 'Jest', 'Redis', 'RabbitMQ', 'Kafka',
  'MassTransit', 'Hangfire', 'Dapper', 'PostgreSQL', 'Npgsql', 'MySQL', 'SQLite', 'MongoDB', 'Elasticsearch', 'GitHub Actions',
  'Azure', 'AWS', 'JavaScript', 'npm', 'pnpm', 'yarn', 'Node.js', 'Blazor', 'SignalR', 'gRPC', 'GraphQL', 'nginx',
  'Kestrel', 'curl', 'PowerShell', 'Minimal API', 'Minimal APIs', 'controller', 'controllers', 'ASP.NET', 'ASP.NET Core',
  'ASP.NET Core Identity', 'ASP.NET Core Data Protection', 'Data Protection API', 'NuGet', 'EF Core', 'Entity Framework',
  'Entity Framework Core', 'NUnit', 'Angular', 'IExceptionHandler', 'ProblemDetails', 'ValidationProblemDetails',
  'IActionResult', 'ActionResult', 'IResult', 'WebApplicationFactory', 'HttpClient', 'IHttpClientFactory', 'HttpResponseMessage',
  'ILogger', 'TimeProvider', 'IConfiguration', 'IOptions', 'CancellationToken', 'ValueTask', 'DbContext', 'DbSet', 'IQueryable'];
// The only fixed-platform name that has an API shape (PascalCase); never extend this to legalize other technology.
const PLATFORM_IDENTIFIERS = new Set(['TypeScript']);

const violations = [];
const warnings = [];
const fail = (file, msg) => violations.push(`${file}: ${msg}`);
const warn = (file, msg) => warnings.push(`${file}: ${msg}`);
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const wordRe = (token, flags = 'i') => new RegExp(`(?<![A-Za-z0-9-])${esc(token)}(?![A-Za-z0-9-])`, flags);

function splitFrontmatter(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) return { fm: '', body: normalized };
  const end = normalized.indexOf('\n---', 4);
  if (end < 0) return { fm: '', body: normalized };
  return { fm: normalized.slice(4, end), body: normalized.slice(end + 4) };
}

function parseHeader(body) {
  const line = body.split('\n').find((l) => l.trim() !== '') || '';
  if (!line.startsWith('> Level: ')) return null;
  const fields = {};
  for (const part of line.slice(2).split(' · ')) {
    const idx = part.indexOf(':');
    if (idx > 0) fields[part.slice(0, idx).trim()] = part.slice(idx + 1).trim();
  }
  return fields;
}

// ---------- Markdown blocks with governors (bounded structure: headings, paragraphs, list items, rows, code) ----------

function parseBlocks(body) {
  const blocks = [];
  const headings = [];
  let para = null;
  let list = null; // { items, leadIn }
  let item = null;
  let fence = null;
  let blankRun = 0;
  let lastPara = null;
  const lines = body.split('\n');
  for (let n = 0; n < lines.length; n++) {
    const line = lines[n];
    if (fence) {
      fence.text += `\n${line}`;
      if (/^\s*```/.test(line)) fence = null;
      continue;
    }
    if (/^\s*```/.test(line)) {
      para = null; item = null;
      fence = { type: 'code', text: line, headings: [...headings], ancestors: [] };
      blocks.push(fence);
      continue;
    }
    if (line.trim() === '') { para = null; blankRun++; continue; }
    const heading = line.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      para = null; item = null; list = null; lastPara = null;
      const level = heading[1].length;
      while (headings.length && headings[headings.length - 1].level >= level) headings.pop();
      const h = { type: 'heading', level, text: heading[2], headings: [...headings], ancestors: [] };
      blocks.push(h);
      headings.push(h);
      blankRun = 0;
      continue;
    }
    if (/^\s*\|/.test(line)) {
      para = null; item = null; list = null;
      blocks.push({ type: 'row', text: line, headings: [...headings], ancestors: [] });
      blankRun = 0;
      continue;
    }
    const li = line.match(/^(\s*)(?:[-*+]|\d+\.)\s+(.*)$/);
    if (li) {
      const indent = li[1].length;
      if (!list) {
        const lead = lastPara && (blankRun === 0 || /:\s*$/.test(lastPara.text)) ? lastPara : null;
        list = { items: [], leadIn: lead };
      }
      const parent = [...list.items].reverse().find((x) => x.indent < indent) || null;
      const ancestors = [];
      for (let p = parent; p; p = p.parent) ancestors.unshift(p);
      if (!parent && list.leadIn) ancestors.unshift(list.leadIn);
      item = { type: 'item', text: li[2], indent, parent, list, ancestors, headings: [...headings] };
      list.items.push(item);
      blocks.push(item);
      para = null; lastPara = null; blankRun = 0;
      continue;
    }
    if (item && /^\s+\S/.test(line) && (blankRun === 0 || /^\s{2,}/.test(line))) { // list-item continuation (form 4)
      item.text += ` ${line.trim()}`;
      blankRun = 0;
      continue;
    }
    if (para && blankRun === 0) { para.text += ` ${line.trim()}`; continue; } // wrapped paragraph (form 6)
    item = null;
    if (blankRun > 0 || !list) list = null;
    para = { type: 'para', text: line.replace(/^>\s?/, '').trim(), headings: [...headings], ancestors: [] };
    blocks.push(para);
    lastPara = para;
    blankRun = 0;
  }
  return blocks;
}

// Formatting cannot hide a term: compatibility forms are folded (NFKC); HTML comments and tags, soft hyphens and
// zero-width characters, emphasis/strike markers, backslash escapes and code-span backticks are removed.
const normalizeForms = (s) => s.normalize('NFKC').replace(/<!--[\s\S]*?-->/g, '').replace(/<\/?[A-Za-z][^>]*>/g, '')
  .replace(/[\u00AD\u200B-\u200D\u2060\uFEFF]/g, '').replace(/[`*~\\]/g, '');
const splitHumps = (s) => s.replace(/([a-z0-9])(?=[A-Z])|([A-Z])(?=[A-Z][a-z])/g, '$1$2 ');

// A term matches case-insensitively with any run of spaces, dots, hyphens or underscores (or none) between its
// alphanumeric chunks (`ASP.NET Core` ~ `aspnet-core` ~ `AspNetCore`; `Docker` ~ `docker-compose`). A term without
// inner capitals also matches as a PascalCase/camelCase component (`Swagger` in `AddSwaggerGen`); inner-capital
// terms such as `HttpClient` match only whole, so generic wording ("HTTP client") stays neutral.
function technologyMatcher(terms) {
  const compiled = terms.map((term) => {
    const chunks = term.split(/[^A-Za-z0-9]+/).filter(Boolean);
    const re = new RegExp(`(?<![A-Za-z0-9])${chunks.map(esc).join('[\\s._-]*')}(?![A-Za-z0-9])`, 'i');
    return { re, humpFree: chunks.every((c) => splitHumps(c) === c) };
  });
  return (normalized) => {
    const humped = splitHumps(normalized);
    return compiled.map(({ re, humpFree }) => (normalized.match(re) || (humpFree && humped.match(re)) || [])[0]).filter(Boolean);
  };
}

const API_SHAPES = [
  /\bI[A-Z][a-z0-9]+[A-Za-z0-9]*\b/g,
  /\b[A-Za-z_][A-Za-z0-9_]*<[A-Za-z0-9_, ]+>/g,
  /\[[A-Z][a-z]+[A-Za-z0-9]*(?:\([^)\]]*\))?\](?!\()/g,
  /(?<![\w.])\.[A-Z][a-z][A-Za-z0-9]*(?:\(\))?/g,
  /\b[A-Za-z_][A-Za-z0-9_]*\(\)/g,
  /\b[A-Z][A-Za-z0-9]*\.[A-Z][a-z][A-Za-z0-9]*\b/g,
  /\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+[A-Za-z0-9]*\b/g,
  /\b[a-z][a-z0-9]*[A-Z][A-Za-z0-9]*\b/g,
];

// Words that are paths, file names, placeholders or naming-convention examples are not API identifiers.
function stripNonIdentifiers(text) {
  return text.split(/(\s+)/).map((tok) => {
    const t = tok.replace(/^[`("'[]+|[`)"'\],.;:!?]+$/g, '');
    if (/^https?:\/\//.test(t) || /\//.test(t) || /(^|[^A-Za-z0-9_])<[A-Za-z-]+>/.test(t) || /_/.test(t)
      || /\.(cs|csproj|json|md|mjs|props|slnx|sln|ts|ya?ml|xml|config|sql|editorconfig|gitignore)$/i.test(t)) return ' '.repeat(tok.length);
    return tok;
  }).join('');
}

function neutralityCheck(p, d, ctx) {
  const blocks = parseBlocks(d.body);
  const description = (d.fm.match(/^description:\s*(.+)$/m) || [])[1];
  if (description) blocks.push({ type: 'para', text: description, headings: [], ancestors: [] });
  const reported = new Set();
  const report = (token, why) => {
    const key = token.toLowerCase();
    if (reported.has(key)) return;
    reported.add(key);
    fail(p, `Level ${d.header.Level} names concrete technology '${token}' (${why}); keep neutral policy here and move the technique to Level 2 or the owning capability facet`);
  };
  // Frontmatter (paths, names, tool lists) is checked for technology vocabulary; its identifiers are harness metadata.
  for (const token of ctx.technologyIn(normalizeForms(d.fm))) report(token, 'technology vocabulary');
  // Every block is checked on its own, headings included (e.g. "## Must use Swagger"). Code spans are unwrapped, so a
  // pointer (`Technique: <skill>`) is checked like any other text: no wrapper, governor or context masks a term.
  for (const block of blocks) {
    for (const token of ctx.technologyIn(normalizeForms(block.text))) report(token, 'technology vocabulary');
    const ids = stripNonIdentifiers(block.text.replace(/`([^`]+)`/g, ' $1 '));
    for (const re of API_SHAPES) {
      for (const m of ids.matchAll(re)) {
        const id = m[0].replace(/^\./, '').replace(/\(\)$/, '');
        const base = id.replace(/<.*$/, '');
        if (PLATFORM_IDENTIFIERS.has(base)) continue;
        if (ctx.frameOwned(p) && id.split('.').every((seg) => ctx.frameTerms.has(seg) || ctx.frameTerms.has(seg.replace(/<.*$/, '')))) continue;
        if (ctx.frameOwned(p) && (ctx.frameTerms.has(id) || ctx.frameTerms.has(base))) continue;
        report(m[0], 'API-shaped identifier outside the platform vocabulary');
      }
    }
  }
}

function main() {
  const root = resolveRoot();
  const rel = (abs) => toPosix(path.relative(root, abs));
  const exists = (p) => existsSync(path.join(root, p));
  const claude = path.join(root, '.claude');

  const artifactPaths = [
    'CLAUDE.md',
    '.claude/INSTRUCTION_MAP.md',
    ...['rules', 'skills', 'agents', 'capabilities'].flatMap((d) => listFiles(path.join(claude, d), (f) => f.endsWith('.md')).map(rel)),
  ].filter((p) => exists(p));
  const docs = new Map();
  for (const p of artifactPaths) {
    const text = readText(path.join(root, p), p);
    const { fm, body } = splitFrontmatter(text);
    docs.set(p, { text, fm, body, header: parseHeader(body) });
  }
  const levelOf = (p) => { const d = docs.get(p); return d && d.header ? LEVELS.indexOf(d.header.Level) : -1; };

  // Headers.
  for (const [p, d] of docs) {
    if (!d.header) { fail(p, 'missing one-line header starting with "> Level: "'); continue; }
    if (!LEVELS.includes(d.header.Level)) fail(p, `unknown Level '${d.header.Level}'`);
    if (!d.header.Owns) fail(p, 'header lacks "Owns:"');
    if (!d.header.Loading) fail(p, 'header lacks "Loading:"');
    if ('Kind' in d.header) fail(p, 'header uses a "Kind:" field; classify by Level and Capability only');
  }

  // Selection record, slot directories, slot contracts.
  const selection = parseSelection(root);
  const selected = {};
  const capDir = path.join(claude, 'capabilities');
  const slotDirs = existsSync(capDir) ? readdirSync(capDir).filter((e) => statSync(path.join(capDir, e)).isDirectory()) : [];
  for (const dir of slotDirs) if (!(dir in SLOTS)) fail(`.claude/capabilities/${dir}`, `unknown capability slot directory (only the four agreed slots exist: ${Object.keys(SLOTS).join(', ')})`);
  const contracts = {};
  for (const [slot, kind] of Object.entries(SLOTS)) {
    const row = selection.find((r) => r.slot === slot);
    if (!row) { fail('.claude/rules/3-project/decisions.md', `selection record lacks slot '${slot}'`); continue; }
    const requirement = kind.startsWith('required') ? (slot === 'architecture' ? 'required frame' : 'required') : 'optional';
    if (row.requirement !== requirement) fail('.claude/rules/3-project/decisions.md', `slot '${slot}' must be recorded as '${requirement}' (found '${row.requirement}')`);
    if (kind.startsWith('required') && !row.selected) fail('.claude/rules/3-project/decisions.md', `required slot '${slot}' has no selected implementation`);
    selected[slot] = row.selected;
    const slotDir = path.join(capDir, slot);
    const contractPath = `.claude/capabilities/${slot}/CONTRACT.md`;
    const contract = docs.get(contractPath);
    if (!contract) fail(`.claude/capabilities/${slot}`, 'missing CONTRACT.md');
    else {
      if (!new RegExp(`^# Slot Contract: ${esc(slot)} \\(${esc(kind)}\\)`, 'm').test(contract.body)) fail(contractPath, `title must declare the slot as '${kind}'`);
      const required = [...contract.body.matchAll(/^\|\s*(?:`([a-z-]+\.[a-z-]+)`|(knowledge skill))\s*\|/gm)].map((m) => m[1] || `${slot}.knowledge`);
      const requiresBinds = (contract.body.match(/^- requires-binds:\s*(\S+)/m) || [])[1] || null;
      contracts[slot] = { path: contractPath, required, requiresBinds };
    }
    const impls = existsSync(slotDir) ? readdirSync(slotDir).filter((e) => statSync(path.join(slotDir, e)).isDirectory()) : [];
    const expected = row.selected ? [row.selected] : [];
    if (impls.sort().join(',') !== expected.join(',')) {
      fail(`.claude/capabilities/${slot}`, `implementations present [${impls.join(', ')}] differ from selection [${expected.join(', ')}] (static composition: only selected modules ship)`);
    }
  }
  for (const row of selection) if (!(row.slot in SLOTS)) fail('.claude/rules/3-project/decisions.md', `unknown slot '${row.slot}' (only the four agreed slots exist)`);

  // Module manifests.
  const modules = [];
  for (const [slot, impl] of Object.entries(selected)) {
    if (!impl) continue;
    const manifestPath = `.claude/capabilities/${slot}/${impl}/MODULE.md`;
    const doc = docs.get(manifestPath);
    if (!doc) { fail(manifestPath, 'missing module manifest'); continue; }
    const capability = `${slot}/${impl}`;
    const line = (key) => (doc.body.match(new RegExp(`^- ${key}:\\s*(.+)$`, 'm')) || [])[1];
    const facets = [...doc.body.matchAll(/^\|\s*`([a-z-]+\.[a-z-]+)`\s*\|\s*`([^`]+)`\s*\|\s*([a-z0-9-]+)\s*\|/gm)]
      .map((m) => ({ facet: m[1], file: m[2], level: m[3] }));
    if (!line('leak-tokens')) fail(manifestPath, 'missing "- leak-tokens:" line');
    if (!line('binds')) fail(manifestPath, 'missing "- binds:" line (use "none" when the module needs no frame-specific binding)');
    if (facets.length === 0) fail(manifestPath, 'facet table is empty or malformed');
    if (doc.header && doc.header.Capability !== capability) fail(manifestPath, `header Capability must be '${capability}'`);
    const tokens = (line('leak-tokens') || '').split(',').map((t) => t.trim()).filter(Boolean);
    const list = (key) => (line(key) || '').split(',').map((t) => t.trim()).filter(Boolean);
    const frameTerms = slot === 'architecture' ? list('frame-terms') : [];
    const placementExamples = slot === 'architecture' ? list('placement-examples') : [];
    if (slot === 'architecture' && frameTerms.length === 0) fail(manifestPath, 'frame manifest lacks "- frame-terms:" (role-realization and placement names its Level 1 facets use)');
    for (const f of facets) {
      if (!f.facet.startsWith(`${slot}.`)) fail(manifestPath, `facet '${f.facet}' does not belong to slot '${slot}'`);
      if (!exists(f.file)) { fail(manifestPath, `facet file missing: ${f.file}`); continue; }
      if (f.file.endsWith('.md')) {
        const fd = docs.get(f.file);
        if (fd && fd.header) {
          if (fd.header.Capability !== capability) fail(f.file, `must declare "Capability: ${capability}" (listed in ${manifestPath})`);
          if (fd.header.Facet !== f.facet) fail(f.file, `must declare "Facet: ${f.facet}"`);
          if (fd.header.Level !== f.level) fail(f.file, `Level '${fd.header.Level}' differs from manifest level '${f.level}'`);
        }
      } else if (f.file.endsWith('.json')) {
        try { JSON.parse(readText(path.join(root, f.file), f.file)); } catch { fail(f.file, 'invalid JSON'); }
      }
    }
    const contract = contracts[slot];
    if (contract) for (const req of contract.required) if (!facets.some((f) => f.facet === req)) fail(manifestPath, `missing required facet '${req}' declared by ${contract.path}`);
    const binds = (line('binds') || '').trim();
    modules.push({ slot, impl, capability, manifestPath, facets, tokens, frameTerms, placementExamples, binds, dir: `.claude/capabilities/${slot}/${impl}/` });
  }
  const frame = modules.find((m) => m.slot === 'architecture');
  const ownerOf = (p) => modules.find((m) => p.startsWith(m.dir) || m.facets.some((f) => f.file === p || (f.file.endsWith('/SKILL.md') && p.startsWith(f.file.replace(/SKILL\.md$/, '')))));
  const moduleFiles = (m) => [...docs.keys()].filter((p) => ownerOf(p) === m && p !== m.manifestPath);

  // Binds: the frame binds nothing; a leaf binds only the selected frame, with a reason; required when the
  // contract says so or when the module's content uses frame-specific vocabulary.
  // Project-name segments come from the frame's own check specification (role project patterns).
  const frameSegments = [];
  const frameCheck = frame && frame.facets.find((f) => f.facet === 'architecture.check');
  if (frameCheck && exists(frameCheck.file)) {
    try {
      const spec = JSON.parse(readText(path.join(root, frameCheck.file), frameCheck.file));
      for (const def of [...Object.values(spec.roles || {}), ...Object.values(spec.testRoles || {})]) {
        for (const seg of String(def.projectPattern || '').match(/[A-Za-z]+/g) || []) if (!frameSegments.includes(seg)) frameSegments.push(seg);
      }
    } catch { /* reported by the manifest check */ }
  }
  const frameVocabulary = frame ? [...frame.tokens, ...frame.frameTerms.filter((t) => /[A-Z].*[A-Z]|[<(]/.test(t) && !frameSegments.includes(t))] : [];
  for (const m of modules) {
    if (m.slot === 'architecture') {
      if (m.binds !== 'none') fail(m.manifestPath, 'the architecture frame must not declare binds: a frame never depends on a leaf (binds: none)');
      continue;
    }
    const target = frame ? `architecture/${frame.impl}` : null;
    const declared = m.binds !== 'none';
    if (declared && (!target || !m.binds.startsWith(target) || !/—\s*\S.{10,}/.test(m.binds))) fail(m.manifestPath, `binds must be "none" or "${target} — <reason>"`);
    const evidence = [];
    for (const p of moduleFiles(m)) {
      const body = docs.get(p).body;
      for (const t of frameVocabulary) if (wordRe(t.replace(/<.*$/, ''), '').test(body)) evidence.push(`${p}: ${t}`);
      for (const seg of frameSegments) if (new RegExp(`<Name>\\.${esc(seg)}\\b`).test(body)) evidence.push(`${p}: <Name>.${seg}`);
    }
    for (const f of m.facets.filter((x) => x.file.endsWith('.json'))) {
      const body = readText(path.join(root, f.file), f.file);
      for (const seg of frameSegments) if (new RegExp(`\\*\\.${esc(seg)}\\b`).test(body)) evidence.push(`${f.file}: *.${seg}`);
    }
    const contract = contracts[m.slot];
    if (contract && contract.requiresBinds && !declared) fail(m.manifestPath, `binds: none, but ${contract.path} requires a binding to the ${contract.requiresBinds} frame`);
    if (evidence.length && !declared) fail(m.manifestPath, `binds: none, but module content uses frame-specific vocabulary (${evidence.slice(0, 3).join('; ')}); declare binds: ${target} — <reason>`);
  }

  // Capability declarations must match manifests.
  for (const [p, d] of docs) {
    if (!d.header || !d.header.Capability) continue;
    const m = modules.find((x) => x.capability === d.header.Capability);
    if (!m) { fail(p, `declares Capability '${d.header.Capability}', which is not a selected module`); continue; }
    if (!(p.startsWith(m.dir) || m.facets.some((f) => f.file === p))) fail(p, `declares Capability '${m.capability}' but is not listed in ${m.manifestPath}`);
  }

  // Rules: level directory, paths, capability subdirectories.
  for (const [p, d] of docs) {
    if (!p.startsWith('.claude/rules/')) continue;
    const parts = p.split('/');
    const levelDir = parts[2];
    if (!LEVELS.includes(levelDir)) fail(p, `rule outside a level directory (${LEVELS.join(', ')})`);
    if (d.header && d.header.Level !== levelDir) fail(p, `header Level '${d.header.Level}' does not match directory '${levelDir}'`);
    const pathsBlock = d.fm.match(/^paths:\s*\n((?:\s+-\s+.+\n?)+)/m);
    if (!pathsBlock || !/-\s+"?[^"\s]+"?/.test(pathsBlock[1])) fail(p, 'rule must declare non-empty "paths:" frontmatter');
    if (parts.length > 4 && d.header && !d.header.Capability) fail(p, 'rule in a capability subdirectory must declare "Capability:"');
  }

  // Conformance direction: a rule may depend only on rules/facets of the same or a more stable level.
  // The only exempt reverse form is a binding pointer ("Framework binding: `<slot>.<facet>` ...").
  const facetLevel = new Map(modules.flatMap((m) => m.facets.map((f) => [f.facet, LEVELS.indexOf(f.level)])));
  for (const [p, d] of docs) {
    if (!p.startsWith('.claude/rules/') || !d.header) continue;
    const own = levelOf(p);
    for (const block of parseBlocks(d.body)) {
      for (const sentence of block.text.split(/(?<=\.)\s+/)) {
        const targets = [
          ...[...sentence.matchAll(/\.claude\/rules\/(\d)-/g)].map((m) => [m[0], Number(m[1])]),
          ...[...sentence.matchAll(/(?<![\w./-])((?:architecture|persistence|backend-testing|frontend)\.[a-z][a-z-]*)(?![\w-])/g)].map((m) => [m[1], facetLevel.has(m[1]) ? facetLevel.get(m[1]) : -1]),
        ].filter(([, lvl]) => lvl > own);
        if (!targets.length) continue;
        if (/^\s*(?:Framework\s+binding|Bindings?)\s*:\s*`(?:architecture|persistence|backend-testing|frontend)\.[a-z-]+`(?:\s*\([^)]*\))?\.?\s*$/i.test(sentence.replace(/\s+[A-Z][^.]*:.*$/, ''))) continue;
        for (const [target, lvl] of targets) fail(p, `conformance dependency on less stable ${LEVELS[lvl]} artifact '${target}'; a rule may depend only on the same or a more stable level`);
      }
    }
  }

  // Always-loaded surface: CLAUDE.md imports.
  const imports = [...docs.get('CLAUDE.md').body.matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]);
  for (const imp of imports) {
    if (!exists(imp)) { fail('CLAUDE.md', `import does not resolve: @${imp}`); continue; }
    const d = docs.get(imp);
    if (d && d.header && !/^always/.test(d.header.Loading)) fail(imp, 'imported by CLAUDE.md but header Loading is not "always"');
  }
  for (const [p, d] of docs) {
    if (p !== 'CLAUDE.md' && d.header && /^always/.test(d.header.Loading) && !imports.includes(p)) fail(p, 'declares "Loading: always" but is not imported by CLAUDE.md');
  }

  // Implementation-name leakage (case-insensitive).
  for (const [p, d] of docs) {
    if (LEAK_ALLOWED.has(p)) continue;
    const owner = ownerOf(p);
    for (const m of modules) {
      if (owner === m) continue;
      for (const token of m.tokens) {
        if (wordRe(token).test(d.body)) fail(p, `names '${token}' from module ${m.capability}; use slot/facet/role vocabulary or move the content into the module`);
      }
    }
  }

  // Core and Architecture neutrality (no pointer exemption; fixed platform only).
  const skillsDir = path.join(claude, 'skills');
  const skills = existsSync(skillsDir) ? readdirSync(skillsDir).filter((e) => existsSync(path.join(skillsDir, e, 'SKILL.md'))) : [];
  const techSkills = new Set(skills.filter((s) => { const d = docs.get(`.claude/skills/${s}/SKILL.md`); return d && d.header && d.header.Level === '2-technology'; }));
  const packageIds = [];
  const collectIds = (obj) => {
    if (Array.isArray(obj)) { for (const x of obj) collectIds(x); return; }
    if (obj && typeof obj === 'object') {
      for (const [k, v] of Object.entries(obj)) {
        if ((k === 'id' || k === 'prefix') && typeof v === 'string') packageIds.push(v.replace(/[/.]+$/, ''));
        else if (/Packages|PackagePrefixes/.test(k) && Array.isArray(v)) v.filter((x) => typeof x === 'string').forEach((x) => packageIds.push(x.replace(/[/.]+$/, '')));
        else collectIds(v);
      }
    }
  };
  for (const f of ['.claude/hooks/manifest-policy.json', ...modules.flatMap((m) => m.facets.filter((x) => x.file.endsWith('.json')).map((x) => x.file))]) {
    if (exists(f)) { try { collectIds(JSON.parse(readText(path.join(root, f), f))); } catch { /* reported elsewhere */ } }
  }
  const leafTokens = modules.filter((m) => m.slot !== 'architecture').flatMap((m) => m.tokens.map((t) => t.replace(/^\[|\]$/g, '')));
  const vocabulary = [...new Set([...TECHNOLOGY_LEXICON, ...leafTokens, ...packageIds].filter((t) => t && t.length > 2))];
  const technologyIn = technologyMatcher(vocabulary);
  const isTechnology = (term) => techSkills.has(term) || technologyIn(normalizeForms(term.replace(/<.*$/, ''))).length > 0;
  // Frame terms and placement examples are allowed only inside frame-owned Level 1 artifacts and can never
  // legalize technology: an entry that is technology vocabulary is itself a violation.
  const frameTerms = new Set(frame ? [...frame.frameTerms, ...frame.placementExamples].flatMap((t) => [t.replace(/\(\)$/, ''), t.replace(/<.*$/, '')]) : []);
  if (frame) {
    for (const [key, terms] of [['frame-terms', frame.frameTerms], ['placement-examples', frame.placementExamples]]) {
      for (const t of terms) {
        if (isTechnology(t) || [...techSkills].some((s) => s.toLowerCase() === t.toLowerCase())) fail(frame.manifestPath, `${key} entry '${t}' is technology vocabulary; frame vocabulary cannot legalize concrete technology at Levels 0/1`);
      }
    }
  }
  const ctx = { technologyIn, frameTerms, frameOwned: (p) => !!frame && ownerOf(p) === frame };
  for (const [p, d] of docs) {
    if (!d.header || !['0-core', '1-architecture'].includes(d.header.Level)) continue;
    neutralityCheck(p, d, ctx);
  }

  // Facet references.
  for (const [p, d] of docs) {
    for (const m of d.body.matchAll(/(?<![\w./-])(architecture|persistence|backend-testing|frontend)\.([a-z][a-z-]*)(?![\w-])/g)) {
      const [ref, slot] = [m[0], m[1]];
      const mod = modules.find((x) => x.slot === slot);
      if (!mod) { if (SLOTS[slot].startsWith('required')) fail(p, `facet reference '${ref}' but slot '${slot}' has no module`); continue; }
      if (!mod.facets.some((f) => f.facet === ref)) fail(p, `facet reference '${ref}' is not declared in ${mod.manifestPath}`);
    }
  }

  // Skills and agents.
  const agents = listFiles(path.join(claude, 'agents'), (f) => f.endsWith('.md')).map((f) => path.basename(f, '.md'));
  const moduleKnowledge = modules.flatMap((m) => m.facets.filter((f) => f.facet.endsWith('.knowledge')).map((f) => f.file.split('/')[2]));
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_SHARED_KNOWLEDGE, ...moduleKnowledge]) {
    if (!skills.includes(name)) fail(`.claude/skills/${name}`, 'required skill is missing');
  }
  for (const name of skills) {
    const p = `.claude/skills/${name}/SKILL.md`;
    const d = docs.get(p);
    const fmName = (d.fm.match(/^name:\s*(.+)$/m) || [])[1];
    const description = (d.fm.match(/^description:\s*(.+)$/m) || [])[1];
    if (fmName !== name) fail(p, `frontmatter name '${fmName}' must equal directory '${name}'`);
    if (!description) fail(p, 'missing description');
    else if (description.length > 360) warn(p, `description is ${description.length} chars; keep skill listings compact`);
    const userOnly = /^disable-model-invocation:\s*true\s*$/m.test(d.fm);
    if (name === 'template-maintenance' && !userOnly) fail(p, 'must set disable-model-invocation: true (user-only workflow)');
    if (name !== 'template-maintenance' && userOnly) fail(p, 'must stay model-invocable');
  }
  const reviewer = docs.get('.claude/agents/code-reviewer.md');
  if (!reviewer) fail('.claude/agents/code-reviewer.md', 'missing code-reviewer agent');
  else {
    const disallowed = (reviewer.fm.match(/^disallowedTools:\s*(.+)$/m) || [])[1] || '';
    if (!/\bWrite\b/.test(disallowed) || !/\bEdit\b/.test(disallowed)) fail('.claude/agents/code-reviewer.md', 'must disallow Write and Edit (read-only reviewer)');
    if (!reviewer.body.includes('`code-review`')) fail('.claude/agents/code-reviewer.md', 'must delegate to the code-review skill');
  }

  // Named skill/agent references.
  const known = new Set([...skills, ...agents]);
  for (const [p, d] of docs) {
    const re = /`([a-z][a-z0-9-]*)`(?=\s+(?:skill|workflow|agent)\b)|(?:\brun|→|->|[Tt]echniques?:|Procedures?:)\s+`([a-z][a-z0-9-]*)`/g;
    for (const m of d.body.matchAll(re)) {
      const name = m[1] || m[2];
      if (!known.has(name)) fail(p, `references unknown skill or agent '${name}'`);
    }
  }

  // Path references.
  for (const [p, d] of docs) {
    for (const m of d.body.matchAll(/`(\.claude\/[^`\s]+|references\/[^`\s]+)`/g)) {
      const target = m[1].replace(/[.,;:]+$/, '');
      if (/[<*>]/.test(target)) continue;
      const resolved = target.startsWith('references/') ? path.posix.join(path.posix.dirname(p), target) : target;
      if (!exists(resolved)) fail(p, `path reference does not resolve: ${target}`);
    }
  }

  // Skill-private references are used only by their owning skill (the map may list them).
  for (const p of docs.keys()) {
    const m = p.match(/^\.claude\/skills\/([^/]+)\/references\/(.+)$/);
    if (!m) continue;
    for (const [other, d] of docs) {
      if (other === p || other === '.claude/INSTRUCTION_MAP.md' || other.startsWith(`.claude/skills/${m[1]}/`)) continue;
      const ownRelative = other.startsWith('.claude/skills/') && d.body.includes(`references/${m[2]}`);
      if (d.body.includes(`${m[1]}/references/${m[2]}`) || ownRelative) fail(other, `depends on private reference ${p} of skill '${m[1]}'`);
    }
  }

  // Human map coverage.
  const map = docs.get('.claude/INSTRUCTION_MAP.md');
  if (!map) fail('.claude/INSTRUCTION_MAP.md', 'missing instruction map');
  else {
    for (const p of docs.keys()) if (p !== '.claude/INSTRUCTION_MAP.md' && !map.body.includes(p)) fail('.claude/INSTRUCTION_MAP.md', `does not list ${p}`);
    if (imports.includes('.claude/INSTRUCTION_MAP.md')) fail('CLAUDE.md', 'the instruction map must not be auto-loaded');
  }

  // Hooks: exec form (command + args, placeholder only as argument data), required registrations, failure semantics.
  const settingsPath = path.join(claude, 'settings.json');
  if (!existsSync(settingsPath)) fail('.claude/settings.json', 'missing');
  else {
    const S = '.claude/settings.json';
    const settings = JSON.parse(readText(settingsPath, S));
    const hooks = settings.hooks || {};
    for (const [event, groups] of Object.entries(hooks)) {
      for (const group of groups) {
        for (const hook of group.hooks || []) {
          const cmd = hook.command || '';
          if (hook.type !== 'command') fail(S, `${event} hook must be of type "command"`);
          if (!cmd || /[\s$%`'"&|;<>]/.test(cmd)) fail(S, `${event} hook command must be a bare executable name (exec form), found: ${cmd}`);
          if (!Array.isArray(hook.args) || hook.args.length === 0) { fail(S, `${event} hook must use exec form with "args" (no shell-form command string)`); continue; }
          const script = hook.args[0];
          if (!/^\$\{CLAUDE_PROJECT_DIR\}\/\.claude\/hooks\/[\w.-]+\.mjs$/.test(script)) fail(S, `${event} hook script argument must be "\${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs", found: ${script}`);
          else if (!exists(script.replace('${CLAUDE_PROJECT_DIR}/', ''))) fail(S, `${event} hook script missing: ${script}`);
          for (const a of hook.args.slice(1)) if (/[$%`]/.test(a)) fail(S, `${event} hook argument relies on expansion: ${a}`);
          if (typeof hook.timeout !== 'number') fail(S, `${event} hook needs a numeric timeout`);
          if (event === 'PreToolUse' && hook.onFailure !== 'block') fail(S, 'critical PreToolUse hook must set onFailure: "block" (fail closed on missing script, crash, malformed input, timeout)');
          if (event !== 'PreToolUse' && hook.onFailure === 'block') fail(S, `${event} hook must stay non-blocking (no onFailure: "block" on advisory post/Stop hooks)`);
        }
      }
    }
    const covered = (event, tool) => (hooks[event] || []).some((g) => (g.hooks || []).length && (tool ? g.matcher && new RegExp(`^(?:${g.matcher})$`).test(tool) : true));
    for (const tool of ['Bash', 'PowerShell']) if (!covered('PreToolUse', tool)) fail(S, `PreToolUse must cover ${tool} (dependency and project-graph gate)`);
    for (const tool of ['Edit', 'Write', 'MultiEdit', 'Bash', 'PowerShell']) if (!covered('PostToolUse', tool)) fail(S, `PostToolUse must cover ${tool} (actual manifest state)`);
    for (const tool of ['Bash', 'PowerShell']) if (!covered('PostToolUseFailure', tool)) fail(S, `PostToolUseFailure must cover ${tool} (partial side effects of failed shell calls)`);
    if (!covered('Stop')) fail(S, 'Stop co-change hook is not registered');
  }

  for (const w of warnings) console.log(`WARNING   ${w}`);
  for (const v of violations) console.log(`VIOLATION ${v}`);
  console.log(`Instruction check: ${violations.length === 0 ? 'PASS' : 'FAIL'} (${docs.size} artifacts, ${violations.length} violation(s), ${warnings.length} warning(s)).`);
  process.exit(violations.length === 0 ? 0 : 1);
}

try {
  main();
} catch (error) {
  console.error(`Instruction check could not run: ${error.message}`);
  process.exit(2);
}
