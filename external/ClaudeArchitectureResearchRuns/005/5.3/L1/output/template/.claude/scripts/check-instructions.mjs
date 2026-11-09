#!/usr/bin/env node
// Instruction-structure checker for the level-first instruction system with replaceable capabilities.
// Validates: headers and levels, rule paths and minimum scopes, Level 0/1 technology neutrality,
// conformance-dependency direction, decision stratification, the four static capability slots,
// selection record, module manifests, contracts and facets, frame terms and binds:, implementation-name
// leakage, always-loaded imports, facet/path/skill references, private references, required
// workflows/knowledge, agent, exec-form hook registrations, and map coverage.
// Usage (from any directory of the project or worktree to check):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"   (exit 1 on violations, 2 on setup errors)
import { existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { listFiles, parseSelection, readText, requireConfigRoot, resolveContext, toPosix } from './lib/project.mjs';

const LEVELS = ['0-core', '1-architecture', '2-technology', '3-project'];
const RANK = Object.fromEntries(LEVELS.map((l, i) => [l, i]));
const SLOTS = {
  architecture: { requirement: 'required', role: 'frame', selection: 'required frame' },
  persistence: { requirement: 'required', role: 'leaf', selection: 'required' },
  'backend-testing': { requirement: 'required', role: 'leaf', selection: 'required' },
  frontend: { requirement: 'optional', role: 'leaf', selection: 'optional' },
};
const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
const REQUIRED_SHARED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration',
  'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication'];
const LEAK_ALLOWED = new Set(['.claude/rules/3-project/decisions.md', '.claude/INSTRUCTION_MAP.md']);
const SCOPE_GLOBS = { common: '**/*', backend: 'backend/**/*', 'backend-tests': 'backend/**/*Tests/**/*', frontend: 'frontend/**/*' };

// ---- Level 0/1 technology neutrality -------------------------------------------------------------
// Fixed platform vocabulary: the platform names, their CLIs and project-file conventions, base-runtime
// types, and protocol/standard terms. Everything else concrete is a Technology binding. Detection is
// layered so that no single hand-maintained list decides the result:
//  1. code identifiers in Level 0/1 artifacts must be in BASE_VOCABULARY or — in frame artifacts — anchored
//     frame code names, or placement examples at the positions where the placement facet places them
//     (fail closed, frame artifacts included; see "Frame vocabulary classes");
//  2. API-shaped prose identifiers in Level 0/1 artifacts follow the same rule (fail closed);
//  3. identifiers and framework nouns declared in Level 2 binding sections (code spans and binding prose),
//     package identifiers from enforcement data and package tables, and module leak-tokens (all harvested
//     from the template itself) must not appear, singular or plural;
//  4. a platform name followed by anything but a generic word ("ASP.NET Core Identity", "ASP.NET Core
//     controllers") must not appear;
//  5. mid-sentence capitalized words in Level 0/1 prose must be fixed-platform, stable architecture/process
//     (STABLE_PHRASES, STABLE_WORDS), or — in frame artifacts — frame vocabulary (fail closed);
//  6. well-known technology names (TECHNOLOGY_NAMES) must not appear;
//  7. allow-lists and frame-terms must not contain technology vocabulary (no legalizing by allow-listing).
// Names (technology, product, package, implementation) match case-insensitively. Case is significant only
// where the spelling itself carries the meaning: single-word code identifiers ("Include") and
// COMMON_WORD_NAMES, whose lowercase forms are ordinary prose. A logical Markdown statement that is wholly a
// routing pointer to Level 2+ skills ("Technique: `docker`.") is routing, not technology use; a statement that
// adds normative wording anywhere in its governing chain, its own text, or its governed content is checked
// unchanged (see "Logical Markdown statements").
const PLATFORM_NAMES = ['.NET', 'C#', 'ASP.NET Core', 'NuGet', 'HTTP', 'Git'];
// Generic words that may follow a platform name ("an ASP.NET Core backend").
const PLATFORM_FOLLOWERS = new Set(['backend', 'application', 'applications', 'app', 'apps', 'project', 'projects', 'platform', 'solution',
  'solutions', 'service', 'services', 'code', 'version', 'versions', 'release', 'releases', 'runtime', 'and', 'or', 'with', 'for', 'to', 'in',
  'on', 'is', 'are', 'as', 'that', 'the', 'a', 'an', 'of', 'when', 'where', 'only']);
const GENERIC_NOUNS = new Set([...PLATFORM_FOLLOWERS, 'transport', 'types', 'type', 'feature', 'features', 'primitives', 'conventions', 'api', 'apis']);
// Stable, technology-free capitalized vocabulary of Core and Architecture.
const STABLE_PHRASES = [
  // architecture patterns (adopted or not adopted)
  'Rich Domain Model', 'Vertical Slice Architecture', 'Unit of Work', 'Aggregate Roots', 'Domain Events', 'Domain Services', 'Value Objects',
  // decision control and process conventions
  'Decision Requests', 'Decision Request', 'Conventional Commits', 'Central Package Management',
  // OWASP Top 10 category names (security taxonomy)
  'Broken Access Control', 'Security Misconfiguration', 'Software Supply Chain Failures', 'Cryptographic Failures', 'Insecure Design',
  'Authentication Failures', 'Software or Data Integrity Failures', 'Security Logging & Alerting Failures', 'Mishandling of Exceptional Conditions', 'Top 10'];
const STABLE_WORDS = new Set([
  // decision classes and Decision Request fields
  'Decided', 'Delegated', 'Reserved', 'Context', 'Options', 'Recommendation', 'Blocked', 'Proceeding',
  // pattern and taxonomy words used alone
  'Specifications', 'Injection',
  // level names, environments, log levels
  'Level', 'Core', 'Architecture', 'Technology', 'Project', 'Development', 'Production', 'Testing', 'Debug', 'Trace',
  // standards, platform names, and shells
  'Bearer', 'OpenAPI', 'PowerShell', 'Git', 'NuGet']);
// Acronyms are protocol/standard/process vocabulary unless they name an implementation.
const TECHNOLOGY_ACRONYMS = new Set(['EF', 'MVC', 'WPF', 'WCF', 'IIS', 'SPA', 'NPM']);
const BASE_VOCABULARY = new Set([
  // .NET base runtime and C# language
  'Task', 'ValueTask', 'CancellationToken', 'TimeProvider', 'HttpClient', 'HttpResponseMessage', 'DateTime', 'DateTimeOffset', 'Result', 'Wait',
  // platform names and shells used for commands
  'NuGet', 'PowerShell',
  // stable role vocabulary: expected-outcome category examples
  'BadRequest', 'NotFound',
]);
const TECHNOLOGY_NAMES = ['FluentValidation', 'Serilog', 'Swashbuckle', 'Swagger', 'Mapster', 'AutoMapper', 'Polly', 'Scrutor',
  'Testcontainers', 'MediatR', 'Kommand', 'Redis', 'RabbitMQ', 'Kafka', 'Docker', 'Kubernetes', 'npm', 'pnpm', 'yarn', 'npx', 'Node.js',
  'node_modules', 'package.json', 'package-lock.json', 'TypeScript', 'JavaScript', 'Playwright', 'Cypress', 'Jest', 'Dapper', 'NHibernate',
  'xUnit', 'MSTest', 'TUnit', 'Moq', 'NSubstitute', 'React', 'Vue', 'Svelte', 'Blazor', 'Razor', 'SignalR', 'Minimal API', 'Minimal APIs',
  'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'Elasticsearch', 'OpenTelemetry', 'HybridCache', 'Azure', 'AWS', 'GitHub Actions',
  // framework constructs and hosts named as plain nouns
  'Controller', 'Controllers', 'Kestrel', 'Identity', 'Data Protection', 'Razor Pages', 'Web API', 'Hangfire', 'Quartz.NET', 'Orleans', 'Dapr'];
// Technology names whose lowercase spelling is an ordinary word with a technology-free meaning ("external
// identity"): only the capitalized proper noun names the technology. Never a selected implementation name.
const COMMON_WORD_NAMES = new Set(['Identity']);
const ROUTING_LABEL = /(^|[\s(.;])(Technique|Techniques|Commands|Procedures?|Co-change procedure|Framework binding|Bindings?|Mechanical check|Example seeder|Examples?|Full status-code reference|Audits|Adding or updating packages|Dependency vulnerability and license checks|Server-side authorization|Role vocabulary|Boundary rules|placement details|Platform-specific examples)\s*(:|load)/;

const violations = [];
const warnings = [];
const fail = (file, msg) => violations.push(`${file}: ${msg}`);
const warn = (file, msg) => warnings.push(`${file}: ${msg}`);

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

const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
function tokenRegex(token) {
  return new RegExp(`(?<![A-Za-z0-9_-])${escapeRe(token)}(?![A-Za-z0-9_-])`);
}
const contains = (text, token) => (/^[\w.# -]+$/.test(token) && /[\w]$/.test(token) ? tokenRegex(token).test(text) : text.includes(token));

const codeSpans = (text) => [...text.matchAll(/```[^\n]*\n([\s\S]*?)```/g)].map((m) => m[1])
  .concat([...text.replace(/```[^\n]*\n[\s\S]*?```/g, '').matchAll(/`([^`\n]+)`/g)].map((m) => m[1]));
const proseOf = (text) => text.replace(/```[^\n]*\n[\s\S]*?```/g, ' ').replace(/`[^`\n]+`/g, ' ');

// Identifiers shaped like framework/library APIs: interfaces, compound PascalCase types, attributes,
// generic types, method calls, dotted package identifiers.
function apiIdentifiers(source) {
  const out = new Set();
  const text = source.replace(/<[A-Za-z][\w.-]*>/g, ' '); // placeholders such as <Name> or <TestProject>
  for (const m of text.matchAll(/\[([A-Z][a-z][A-Za-z0-9]*)(?:\([^\]]*\))?\]/g)) out.add(m[1]);
  for (const m of source.matchAll(/\b([A-Z][A-Za-z0-9]*)[<(]/g)) if (/[a-z]/.test(m[1])) out.add(m[1]);
  for (const m of text.matchAll(/(?<![\w.])(I[A-Z][a-z0-9]+[A-Za-z0-9]*|[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+)(?![\w])/g)) out.add(m[1]);
  for (const m of text.matchAll(/(?<![\w.])([A-Z][A-Za-z0-9]+(?:\.[A-Z][A-Za-z0-9]+)+)(?![\w])/g)) out.add(m[1]);
  return [...out].filter((t) => !PLATFORM_NAMES.includes(t) && t !== 'ASP.NET');
}

// Template tooling paths and invocations are not technology vocabulary.
const stripTooling = (text) => text
  .replace(/node\s+"?\$\(git rev-parse --show-toplevel\)\/\.claude\/[^"\s`]+"?/g, ' ')
  .replace(/@?\.claude\/[^\s`)'"]*/g, ' ');

// ---- Logical Markdown statements ------------------------------------------------------------------
// Routing is classified per logical statement, never per physical line, so that reformatting one statement
// cannot change its classification. A bounded builder (not a Markdown parser) groups lines into statements
// and records which statement governs which. Supported forms, and nothing else:
//  1. a single line;
//  2. consecutive lines of one paragraph (soft-wrapped continuation);
//  3. a list item with its continuation lines (lazy or indented, also indented lines after a blank line);
//  4. a heading governing the next block, with or without a blank line between ("#" headings, and a block-
//     starting line of emphasized text only, the template's pseudo-heading convention);
//  5. a statement ending with ":" governing the next block, and a paragraph directly followed by a list
//     governing that list;
//  6. a list item governing its nested items.
// A "block" is the next paragraph, table, quote line, or list (all of its top-level items). Fenced code is
// opaque and ends governance; table rows and quote lines are single statements. Blank-line-separated
// paragraphs are never joined, and nothing is governed beyond these immediate relations.
const LIST_ITEM = /^(\s*)(?:[-*+]|\d+[.)])\s+/;
const statementText = (s) => s.parts.map((p) => p.text).join(' ');
function logicalStatements(lines) {
  const stmts = [];
  let fence = false, blank = true, open = null, items = [], listGovernor = null, tableGovernor = null, inTable = false;
  const blockGovernor = (listStart) => {
    const prev = stmts[stmts.length - 1];
    if (!prev || prev.kind === 'code') return null;
    if (prev.kind === 'heading' || /:\s*$/.test(statementText(prev)) || (listStart && !blank && prev.kind === 'para')) return prev;
    return null;
  };
  const add = (kind, line, col, text, governor) => {
    const s = { kind, parts: [{ line, col, text }], governors: governor ? [governor] : [], governs: [] };
    if (governor) governor.governs.push(s);
    stmts.push(s);
    return s;
  };
  lines.forEach((line, i) => {
    if (/^\s*```/.test(line)) {
      if (!fence) stmts.push({ kind: 'code', parts: [], governors: [], governs: [] });
      fence = !fence; open = null; inTable = false; blank = false;
      return;
    }
    if (fence) return;
    if (!line.trim()) { blank = true; if (open && open.kind !== 'item') open = null; inTable = false; return; }
    const indent = line.match(/^\s*/)[0].length;
    const heading = line.match(/^( {0,3}#{1,6}\s+)(.*)$/);
    const quote = line.match(/^(\s*>\s?)(.*)$/);
    const item = line.match(LIST_ITEM);
    if (heading) { items = []; open = null; inTable = false; add('heading', i, heading[1].length, heading[2], null); }
    else if (quote) { items = []; open = null; inTable = false; add('quote', i, quote[1].length, quote[2], blockGovernor(false)); }
    else if (/^\s*\|/.test(line)) {
      if (!inTable) { tableGovernor = blockGovernor(false); inTable = true; }
      items = []; open = null; add('row', i, 0, line, tableGovernor);
    } else if (item) {
      if (!items.length) listGovernor = blockGovernor(true);
      while (items.length && items[items.length - 1].indent >= item[1].length) items.pop();
      open = add('item', i, item[0].length, line.slice(item[0].length), items.length ? items[items.length - 1].stmt : listGovernor);
      items.push({ indent: item[1].length, stmt: open });
      inTable = false;
    } else if ((blank || !open) && /^\s*(\*\*|__)[^*_]+\1\s*$/.test(line)) {
      items = []; open = null; inTable = false; add('heading', i, indent + 2, line.trim().slice(2, -2), null);
    } else if (open && (open.kind === 'item' ? !blank || indent >= 2 : open.kind === 'para' && !blank)) {
      open.parts.push({ line: i, col: indent, text: line.slice(indent) });
    } else { items = []; inTable = false; open = add('para', i, indent, line.slice(indent), blockGovernor(false)); }
    blank = false;
  });
  return stmts.filter((s) => s.kind !== 'code');
}
const governingChain = (s, seen = new Set()) => s.governors.flatMap((g) => (seen.has(g) ? [] : (seen.add(g), [...governingChain(g, seen), g])));
const governedContent = (s, seen = new Set()) => s.governs.flatMap((c) => (seen.has(c) ? [] : (seen.add(c), [c, ...governedContent(c, seen)])));
const locate = (s, k) => {
  let startAt = 0;
  for (const p of s.parts) { if (k < startAt + p.text.length) return { line: p.line, col: p.col + k - startAt }; startAt += p.text.length + 1; }
  return null;
};

// Routing pointers — positive reference proof. A technology-named skill is masked only when its pointer is
// proven to be a pure reference to Level 2+ technique; a statement that cannot be proven so is checked
// unchanged (fail closed). The proof runs over the statement prefixed by the governors that label it:
//  1. Targets: every listed name is an existing Level 2+ skill.
//  2. Shape: nothing but the skill list (and an optional "skill(s)") stands in the clause, which is either
//       a technique label "[title] technique(s): <skills>" — the title is empty, the cross-reference words
//         "see"/"also", or subject words — or
//       a subject route "<subject> → (or ->) <skills>".
//  3. Position: the clause is
//       the whole statement — preceded only by ":"-separated labels, ending its statement, and any content the
//         statement governs is itself pointer content (otherwise that content continues the pointer); or
//       an aside "<title> (technique: <skills>)" ending its statement — content the statement governs lies
//         outside the self-contained aside; or
//       a routing-map entry — a ";"-separated entry of a map whose first clause introduces skills and whose
//         other clauses are all "<subject> → <skills>" entries; the other clauses stay independent; or
//       a footnote — a bare "Technique: <skills>." final sentence annotating the rule it ends: every target's
//         core subject (name, "Owns:") occurs in that rule, and the sentence right before it neither refers
//         to it (this, that, it, following, ...) nor carries normative wording; a fragment of up to three
//         words right before it is a label, like the text before ":".
//  4. Labels: each ":"-separated label before the clause, an aside's title, and each governor that labels the
//     statement is a technique title or a subject phrase. A governor labels the statement when the statement
//     it governs on the path down to it is pointer content or a title, whatever else it governs: a selecting
//     heading or parent item stays a label when siblings are added, and a neutral one ("Deployment technique")
//     stays a label over mixed children.
//  5. Binding: no obligation in the statement's bounded block — siblings under its direct governor or under a
//     label, with their continuation and nested items, and content the statement governs — explicitly refers
//     to an indicated technique ("Must use this technique", "the above technique"). Such a reference binds
//     every pointer it may refer to; with several it is ambiguous, which fails closed the same way. An
//     obligation without such a reference ("Must run unit tests") binds nothing.
//  6. Secondary defense: no normative wording in any governor, label, or the rest of the statement.
// Subject words are the engineering subjects the Level 2+ technique catalog itself declares (skill names,
// descriptions, "Owns:"). Selection, assignment, and predication wording ("selected", "technology", "is",
// "will run with") is not subject vocabulary, so a label made of it proves nothing and the pointer stays
// visible. A governor of a statement that is not itself a pointer (a rule embedding a map entry or footnote)
// is a section title, not a label of the pointer. Not modeled: pronoun reference ("it must be used") from a
// sibling, and siblings of an ungoverned list, which have no common governor.
const POINTER_LIST = /^(?:\s*(?:,|\/|\band\b|\bor\b)?\s*`[a-z][a-z0-9-]*`)+/i;
const NORMATIVE = /\b(must|should|shall|requires?|required|mandatory|defaults?|prefer(?:s|red)?|recommended|always|never|only|use[sd]?|using|needs?|standard|approved|decided|replaced?)\b/i;
const boundaryBefore = (before, marks) => {
  for (let i = before.length - 1; i >= 0; i--) if (marks.includes(before[i]) || (before[i] === '.' && /\s/.test(before[i + 1] || ''))) return i;
  return -1;
};
const clauseStart = (before) => boundaryBefore(before, '(;:');
const governingStart = (before) => boundaryBefore(before, ';');
const REFERENCE_WORDS = new Set(['see', 'also']);
const REFERRING = /\b(this|these|that|those|following|below|it|they|them)\b/i;
const JOINERS = new Set(['technique', 'and', 'or', 'of', 'the', 'for', 'to', 'with']);
const stem = (w) => (w.length > 3 && w.endsWith('ies') ? `${w.slice(0, -3)}y` : w.length > 3 && /[^s]s$/.test(w) ? w.slice(0, -1) : w);
const subjectWords = (text) => (text.toLowerCase().match(/[a-z0-9]+/g) || []).map(stem);
const isSubject = (phrase, subject) => { const w = subjectWords(phrase); return w.length > 0 && w.every((x) => subject.has(x)); };
const isTechniqueTitle = (phrase, subject) => {
  const m = phrase.match(/^(.*?)\s*\btechniques?$/i);
  const title = m ? m[1].trim() : null;
  return title !== null && title.split(/\s+/).filter(Boolean).length <= 3 && subjectWords(title).every((x) => REFERENCE_WORDS.has(x) || subject.has(x));
};
const isLabel = (phrase, subject) => {
  const p = phrase.replace(/[*_]/g, ' ').replace(/\s+/g, ' ').trim();
  return !p || isTechniqueTitle(p, subject) || isSubject(p, subject);
};
const SKILL_SPANS = '`[a-z][a-z0-9-]*`(?:\\s*(?:,|\\/|\\band\\b|\\bor\\b)\\s*`[a-z][a-z0-9-]*`)*';
const POINTER_CONTENT = new RegExp(`^(?:[^;:()]+:\\s*)*(?:[^;:()]*?(?:techniques?:|→|->)\\s*)?${SKILL_SPANS}(?:\\s+skills?)?\\s*\\.?$|^[^;()]*\\(\\s*techniques?:\\s*${SKILL_SPANS}\\s*\\)\\s*\\.?$`, 'i');
const ownText = (s) => statementText(s).replace(/[*_]/g, '').trim();
// A title: a heading, or a lead-in ending with ":" that holds no clause of its own.
const isTitle = (s) => s.kind === 'heading' || (/:$/.test(ownText(s)) && !/[;()]|\.\s/.test(ownText(s)));
// Pointer content: a statement shaped as a pointer (or a bare skill list), or a label/heading introducing only such.
const pointerContent = (s) => POINTER_CONTENT.test(ownText(s)) || (isTitle(s) && s.governs.length > 0 && s.governs.every(pointerContent));
// An explicit local reference to an indicated technique: a demonstrative or positional determiner before
// "technique"/"technology" ("this technique", "the above technique", "the following deployment technique",
// "the technique above"). Bare pronouns ("it", "they") are not resolved.
const TECHNIQUE_REFERENCE = /\b(?:this|that|these|those|the\s+(?:above|following|preceding))\s+(?:[a-z-]+\s+){0,2}?(?:techniques?|technolog(?:y|ies))(?![\w-])|\bthe\s+techniques?\s+(?:above|below)\b/i;
const isRoutingMap = (own) => {
  const clauses = own.split(';');
  return clauses.length >= 3 && /\bskills?\b/i.test(clauses[0]) && clauses.slice(1).every((c) => /^\s*[^;:()`]*?(?:→|->)\s*`/.test(c));
};
function routingClause(text, at, marker, targets, scope) {
  const list = text.slice(at + marker.length).match(POINTER_LIST);
  const names = list ? [...list[0].matchAll(/`([a-z][a-z0-9-]*)`/gi)].map((n) => n[1]) : [];
  if (!names.length || !names.every((n) => targets.skills.has(n))) return null;
  const listEnd = at + marker.length + list[0].length;
  const tail = text.slice(listEnd);
  const close = tail.search(/[;)]|\.(?=\s|$)|$/);
  if (!/^\s*(skills?)?\s*$/i.test(tail.slice(0, close))) return null;
  const before = text.slice(0, at);
  const start = clauseStart(before);
  const lead = before.slice(start + 1).replace(/[*_]/g, ' ').trim();
  const arrow = marker === '→' || marker === '->';
  if (arrow ? !isSubject(lead, targets.subject) : !isTechniqueTitle(`${lead} technique`.trim(), targets.subject)) return null;
  const after = tail.slice(close);
  const opener = before[start] || '';
  const prefix = start >= scope.offset ? text.slice(scope.offset, start) : '';
  let position = null;
  if (opener === '(') position = /^\)\s*\.?\s*$/.test(after) ? 'aside' : null;
  else if (/^\s*\.?\s*$/.test(after)) position = opener === '.' && start >= scope.offset ? 'footnote' : 'whole';
  if (arrow && opener === ';' && isRoutingMap(scope.own)) position = 'entry';
  if (!position) return null;
  let segments = [];
  if (position === 'footnote') {
    if (arrow || lead) return null;
    const last = prefix.slice(boundaryBefore(prefix, ';') + 1).trim();
    const annotated = new Set(subjectWords(prefix));
    if (subjectWords(last).length <= 3) segments = [last];
    else if (REFERRING.test(last) || NORMATIVE.test(last) || !names.every((n) => [...targets.core.get(n)].some((w) => annotated.has(w)))) return null;
  } else {
    if (position !== 'entry' && (/[;.]/.test(opener) || /;|\.\s/.test(prefix))) return null;
    if (position !== 'entry') segments = prefix.split(/[:(]/);
  }
  if (![...scope.labels, ...segments].every((l) => isLabel(l, targets.subject))) return null;
  if ((position === 'whole' || position === 'footnote') && !scope.governed.every(pointerContent)) return null;
  if (NORMATIVE.test(scope.governors) || NORMATIVE.test(segments.join(' ')) || NORMATIVE.test(before.slice(governingStart(before) + 1)) || NORMATIVE.test(after)) return null;
  return [at + marker.length, listEnd];
}
function stripRoutingPointers(text, targets) {
  const lines = text.split('\n');
  const masks = lines.map(() => new Map());
  for (const s of logicalStatements(lines)) {
    const own = statementText(s);
    if (!own.includes('`')) continue;
    const chain = governingChain(s);
    // Walking up from the statement, a governor labels the pointer when the statement it governs on that path is
    // pointer content or a title. The walk stops at a governor of any other statement (a rule that embeds a
    // routing-map entry or footnote): that governor and everything above it are section titles, checked only for
    // normative wording. The walk never looks at a governor's other children, so siblings cannot turn a label
    // into a section title. Siblings under the direct governor or under a label (with their continuation and
    // nested items), and content the statement governs, are its bounded block: an obligation there that
    // explicitly refers to an indicated technique binds every pointer it may refer to (one: bound; several:
    // ambiguous), and nothing in the statement is masked.
    const labels = [];
    const block = governedContent(s);
    let below = s;
    for (const g of [...chain].reverse()) {
      const labelling = isTitle(below) || POINTER_CONTENT.test(ownText(below));
      if (below === s || labelling) block.push(...g.governs.filter((c) => c !== below).flatMap((c) => [c, ...governedContent(c)]));
      if (!labelling) break;
      labels.unshift(g);
      below = g;
    }
    if (block.some((c) => TECHNIQUE_REFERENCE.test(statementText(c)) && NORMATIVE.test(statementText(c)))) continue;
    const labelTexts = labels.map((g) => statementText(g).trim().replace(/[\s.:;,]+$/, '')).filter(Boolean);
    const combined = labelTexts.length ? `${labelTexts.join(': ')}: ${own}` : own;
    const offset = combined.length - own.length;
    const scope = { own, offset, labels: labelTexts, governors: chain.map(statementText).join(' '), governed: governedContent(s) };
    for (const m of combined.matchAll(/\btechniques?:|→|->/gi)) {
      const range = routingClause(combined, m.index, m[0], targets, scope);
      if (!range) continue;
      for (const span of combined.slice(range[0], range[1]).matchAll(/`[a-z][a-z0-9-]*`/gi)) {
        const at = locate(s, range[0] + span.index - offset);
        if (range[0] + span.index >= offset && at) masks[at.line].set(at.col, span[0].length);
      }
    }
  }
  return lines.map((line, i) => [...masks[i]].sort((a, b) => b[0] - a[0]).reduce((out, [col, n]) => out.slice(0, col) + ' ' + out.slice(col + n), line)).join('\n');
}

// Implementation identity (leak tokens and the implementation name) matches case-insensitively, with space
// and hyphen spellings equivalent: "Two Words", "two words", and "two-words" are the same name.
function namesIdentity(text, token) {
  if (!/^[\w.# -]+$/.test(token) || !/\w$/.test(token)) return text.toLowerCase().includes(token.toLowerCase());
  const pattern = token.split(/[\s-]+/).map(escapeRe).join('[\\s-]+');
  return new RegExp(`(?<![A-Za-z0-9_-])${pattern}(?![A-Za-z0-9_-])`, 'i').test(text);
}

// Lexicon terms match whole words, singular or plural; terms harvested from binding prose match case-insensitively.
function hasTerm(text, { term, ci }) {
  if (!/^[\w.# &-]+$/.test(term) || !/\w$/.test(term)) return text.includes(term);
  const base = /[a-z]s$/.test(term) && term.length > 3 ? term.slice(0, -1) : term;
  const plural = /[A-Za-z]$/.test(base) ? '(?:e?s)?' : '';
  return new RegExp(`(?<![A-Za-z0-9_-])${escapeRe(base)}${plural}(?![A-Za-z0-9_-])`, ci ? 'i' : '').test(text);
}

// Sentence-like segments of prose: sentence-initial words are ordinary capitalization, not names.
function segmentsOf(prose) {
  const out = [];
  for (const line of prose.split('\n')) {
    if (/^\s*(#|>)/.test(line) || /^\s*\|?\s*:?-{3,}/.test(line)) continue;
    // Section references ("§ Failures", "see Sensitive data and logs") start a new segment.
    for (const seg of line.split(/\||(?<=[.!?:;])\s+|\s[—–→]\s|[(§"]|\bsee\s+(?=[A-Z])|^\s*[-*]\s+|^\s*\d+\.\s+/)) {
      const words = seg.replace(/[*_]/g, ' ').split(/[\s,/]+/).map((w) => w.replace(/'s$/, '').replace(/[^A-Za-z0-9#&'-]/g, '')).filter(Boolean);
      if (words.length) out.push(words);
    }
  }
  return out;
}

// Concrete framework nouns stated in Level 2 binding prose: "ASP.NET Core <feature>" heads and
// mid-sentence capitalized runs ("Minimal API").
function bindingProseTerms(section, exclude) {
  const out = [];
  const prose = section.replace(/`[^`\n]*`/g, ' ');
  const values = [];
  for (const line of prose.split('\n')) {
    if (/^\|/.test(line)) {
      const cells = line.split('|').map((c) => c.trim()).filter(Boolean);
      if (cells.length >= 2 && !/^:?-+$/.test(cells[0]) && !/^Neutral term/i.test(cells[0])) values.push(cells[cells.length - 1]);
    } else if (/^\s*-\s+/.test(line) && line.includes(': ')) values.push(line.slice(line.indexOf(': ') + 2));
  }
  for (const value of values) {
    for (const m of value.matchAll(/ASP\.NET Core\s+([A-Za-z][\w-]*)(?:\s+([A-Za-z][\w-]*))?(?:\s+([A-Za-z][\w-]*))?/g)) {
      const [w1, w2, w3] = [m[1], m[2], m[3]];
      if (GENERIC_NOUNS.has(w1.toLowerCase())) continue;
      if (/^[A-Z]/.test(w1)) out.push({ term: [w1, w2, w3].filter((w, i) => w && (i === 0 || (/^[A-Z]/.test(w) && (i === 1 || /^[A-Z]/.test(w2))))).join(' '), ci: false });
      else out.push({ term: w2 && /^[a-z]+$/.test(w2) && !PLATFORM_FOLLOWERS.has(w2) ? `${w1} ${w2}` : w1, ci: true });
    }
    const rest = value.replace(/ASP\.NET Core\s+[A-Za-z][\w-]*/g, ' ').replace(/\.NET|C#/g, ' ');
    for (const words of segmentsOf(rest)) {
      for (let i = 1; i < words.length; i++) {
        if (!/^[A-Z][a-z]/.test(words[i]) || exclude.has(words[i])) continue;
        let start = i;
        while (start > 0 && /^[A-Z][A-Z0-9]+$/.test(words[start - 1])) start--; // acronym-led product names
        let j = i + 1;
        while (j < words.length && /^[A-Z]/.test(words[j])) j++;
        out.push({ term: words.slice(start, j).join(' '), ci: false });
        i = j;
      }
    }
  }
  return out;
}

// Mid-sentence capitalized words and implementation acronyms that are not allowed vocabulary.
function unexpectedCapitals(prose, allowedPhrases, allowedWords) {
  let text = prose;
  for (const p of [...PLATFORM_NAMES, ...allowedPhrases].sort((a, b) => b.length - a.length)) text = text.split(p).join(' x ');
  const out = new Set();
  for (const words of segmentsOf(text)) {
    words.forEach((w, i) => {
      if (TECHNOLOGY_ACRONYMS.has(w.replace(/s$/, ''))) out.add(w);
      else if (i > 0 && /^[A-Z][a-z]/.test(w) && !allowedWords.has(w) && !allowedWords.has(w.replace(/-.*$/, ''))) out.add(w);
    });
  }
  return [...out];
}

function main() {
  const ctx = resolveContext(process.cwd());
  const root = requireConfigRoot(ctx);
  const rel = (abs) => toPosix(path.relative(root, abs));
  const exists = (p) => existsSync(path.join(root, p));
  const claude = path.join(root, '.claude');
  const levelDir = (p) => p.split('/')[2];

  const artifactPaths = [
    'CLAUDE.md',
    '.claude/INSTRUCTION_MAP.md',
    ...['rules', 'skills', 'agents', 'capabilities'].flatMap((d) => listFiles(path.join(claude, d), (f) => f.endsWith('.md')).map(rel)),
  ].filter((p) => exists(p));
  const docs = new Map();
  for (const p of artifactPaths) {
    const text = readText(path.join(root, p));
    const { fm, body } = splitFrontmatter(text);
    const description = (fm.match(/^description:\s*(.+)$/m) || [])[1] || '';
    docs.set(p, { text, fm, body, description, header: parseHeader(body) });
  }

  // Headers.
  for (const [p, d] of docs) {
    if (!d.header) { fail(p, 'missing one-line header starting with "> Level: "'); continue; }
    if (!LEVELS.includes(d.header.Level)) fail(p, `unknown Level '${d.header.Level}'`);
    if (!d.header.Owns) fail(p, 'header lacks "Owns:"');
    if (!d.header.Loading) fail(p, 'header lacks "Loading:"');
    if ('Kind' in d.header || /^Kind:/m.test(d.body)) fail(p, 'uses a "Kind:" classification; classify by Level and Capability only');
  }

  // Slots: exactly the four agreed slots, static composition, frame vs leaves.
  const capDir = path.join(claude, 'capabilities');
  const slotDirs = existsSync(capDir) ? readdirSync(capDir).filter((e) => statSync(path.join(capDir, e)).isDirectory()) : [];
  for (const dir of slotDirs) if (!(dir in SLOTS)) fail(`.claude/capabilities/${dir}`, 'extra slot: only architecture, persistence, backend-testing, and frontend exist');
  const selection = parseSelection(root);
  const selected = {};
  for (const [slot, def] of Object.entries(SLOTS)) {
    const rows = selection.filter((r) => r.slot === slot);
    if (rows.length !== 1) { fail('.claude/rules/3-project/decisions.md', `selection record must have exactly one row for slot '${slot}' (found ${rows.length})`); continue; }
    const row = rows[0];
    if (row.requirement !== def.selection) fail('.claude/rules/3-project/decisions.md', `slot '${slot}' must be '${def.selection}' (found '${row.requirement}')`);
    if (def.requirement === 'required' && !row.selected) fail('.claude/rules/3-project/decisions.md', `required slot '${slot}' has no selected implementation`);
    selected[slot] = row.selected;
    const slotDir = path.join(capDir, slot);
    const contract = docs.get(`.claude/capabilities/${slot}/CONTRACT.md`);
    if (!contract) fail(`.claude/capabilities/${slot}`, 'missing CONTRACT.md');
    else {
      const kind = def.role === 'frame' ? 'required frame' : `${def.requirement} leaf`;
      if (!new RegExp(`^# Slot Contract: ${escapeRe(slot)} \\(${kind}\\)`, 'm').test(contract.body)) fail(`.claude/capabilities/${slot}/CONTRACT.md`, `title must declare "${slot} (${kind})"`);
    }
    const impls = existsSync(slotDir) ? readdirSync(slotDir).filter((e) => statSync(path.join(slotDir, e)).isDirectory()) : [];
    const expected = row.selected ? [row.selected] : [];
    if (impls.sort().join(',') !== expected.join(',')) {
      fail(`.claude/capabilities/${slot}`, `implementations present [${impls.join(', ')}] differ from selection [${expected.join(', ')}] (static composition: only selected modules ship)`);
    }
  }
  for (const row of selection) if (!(row.slot in SLOTS)) fail('.claude/rules/3-project/decisions.md', `unknown slot '${row.slot}' (only the four agreed slots exist)`);

  // Module manifests and facets.
  const modules = [];
  for (const [slot, impl] of Object.entries(selected)) {
    if (!impl) continue;
    const dir = `.claude/capabilities/${slot}/${impl}/`;
    const manifestPath = `${dir}MODULE.md`;
    const doc = docs.get(manifestPath);
    if (!doc) { fail(manifestPath, 'missing module manifest'); continue; }
    const capability = `${slot}/${impl}`;
    const listLine = (name) => { const m = doc.body.match(new RegExp(`^- ${name}:\\s*(.+)$`, 'm')); return m ? m[1].trim() : null; };
    const tokensLine = listLine('leak-tokens');
    const bindsLine = listLine('binds');
    const termsLine = listLine('frame-terms');
    const facets = [...doc.body.matchAll(/^\|\s*`([a-z-]+\.[a-z-]+)`\s*\|\s*`([^`]+)`\s*\|\s*([a-z0-9-]+)\s*\|/gm)]
      .map((m) => ({ facet: m[1], file: m[2], level: m[3] }));
    if (!tokensLine) fail(manifestPath, 'missing "- leak-tokens:" line');
    if (bindsLine === null) fail(manifestPath, 'missing "- binds:" line (use "none" when the module needs no frame binding)');
    if (SLOTS[slot].role === 'frame' && !termsLine) fail(manifestPath, 'frame manifest must list "- frame-terms:"');
    if (facets.length === 0) fail(manifestPath, 'facet table is empty or malformed');
    if (doc.header && doc.header.Capability !== capability) fail(manifestPath, `header Capability must be '${capability}'`);
    const tokens = tokensLine ? tokensLine.split(',').map((t) => t.trim()).filter(Boolean) : [];
    const lead = (doc.body.split('\n').filter((l) => l.trim() && !l.startsWith('>') && !l.startsWith('#'))[0] || '').trim();
    if (tokens.length && !tokens.some((t) => lead.startsWith(t))) fail(manifestPath, `the module description must start with its implementation name, and that name must be a leak token (found "${lead.slice(0, 40)}")`);
    for (const f of facets) {
      if (!f.facet.startsWith(`${slot}.`)) fail(manifestPath, `facet '${f.facet}' does not belong to slot '${slot}'`);
      if (!LEVELS.includes(f.level)) fail(manifestPath, `facet '${f.facet}' has unknown level '${f.level}'`);
      if (SLOTS[slot].role === 'leaf' && RANK[f.level] < 2) fail(manifestPath, `leaf facet '${f.facet}' must be Level 2 or 3 (placement belongs to the frame; technique belongs to the leaf)`);
      if (SLOTS[slot].role === 'frame' && f.file.endsWith('.md') && f.level !== '1-architecture') fail(manifestPath, `frame facet '${f.facet}' must be Level 1 (placement belongs to the frame)`);
      if (!exists(f.file)) { fail(manifestPath, `facet file missing: ${f.file}`); continue; }
      if (f.file.endsWith('.md')) {
        const fd = docs.get(f.file);
        if (fd && fd.header) {
          if (fd.header.Capability !== capability) fail(f.file, `must declare "Capability: ${capability}" (listed in ${manifestPath})`);
          if (fd.header.Facet !== f.facet) fail(f.file, `must declare "Facet: ${f.facet}"`);
          if (fd.header.Level !== f.level) fail(f.file, `Level '${fd.header.Level}' differs from manifest level '${f.level}'`);
        }
      } else if (f.file.endsWith('.json')) {
        try {
          const data = JSON.parse(readText(path.join(root, f.file)));
          const comment = String(data.$comment || '');
          if (!comment.startsWith(`Facet ${f.facet} (Level ${RANK[f.level]}`)) fail(f.file, `"$comment" must start with "Facet ${f.facet} (Level ${RANK[f.level]}" to match ${manifestPath}`);
        } catch { fail(f.file, 'invalid JSON'); }
      }
    }
    // Every file in the module directory is the manifest or a listed facet.
    for (const file of listFiles(path.join(root, dir)).map(rel)) {
      if (file !== manifestPath && !facets.some((f) => f.file === file)) fail(file, `file in module directory is not a facet listed in ${manifestPath}`);
    }
    // The slot contract's required facets are provided at the contracted level.
    const contract = docs.get(`.claude/capabilities/${slot}/CONTRACT.md`);
    if (contract) {
      const required = [...contract.body.matchAll(/^\|\s*(`([a-z-]+\.[a-z-]+)`|knowledge skill)\s*\|[^|]*\|\s*([0-3])\s*\|/gm)]
        .map((m) => ({ facet: m[2] || `${slot}.knowledge`, level: Number(m[3]) }));
      if (required.length === 0) fail(`.claude/capabilities/${slot}/CONTRACT.md`, 'required-facets table is empty or malformed');
      for (const r of required) {
        const provided = facets.find((f) => f.facet === r.facet);
        if (!provided) fail(manifestPath, `does not provide facet '${r.facet}' required by the ${slot} contract`);
        else if (RANK[provided.level] !== r.level) fail(manifestPath, `facet '${r.facet}' is Level ${RANK[provided.level]}; the contract requires Level ${r.level}`);
      }
    }
    const examplesLine = listLine('placement-examples');
    const examples = examplesLine ? examplesLine.split(',').map((t) => t.trim().replace(/\/$/, '')).filter(Boolean) : [];
    modules.push({ slot, impl, capability, manifestPath, facets, tokens, binds: bindsLine, frameTerms: termsLine ? termsLine.split(',').map((t) => t.trim()).filter(Boolean) : [], examples, dir, role: SLOTS[slot].role });
  }
  const ownerOf = (p) => modules.find((m) => p.startsWith(m.dir) || m.facets.some((f) => f.file === p || (f.file.endsWith('/SKILL.md') && p.startsWith(f.file.replace(/SKILL\.md$/, '')))));
  const frame = modules.find((m) => m.role === 'frame');
  const facetLevel = (ref) => { for (const m of modules) { const f = m.facets.find((x) => x.facet === ref); if (f) return f.level; } return null; };

  // Capability declarations must match manifests.
  for (const [p, d] of docs) {
    if (!d.header || !d.header.Capability) continue;
    const m = modules.find((x) => x.capability === d.header.Capability);
    if (!m) { fail(p, `declares Capability '${d.header.Capability}', which is not a selected module`); continue; }
    if (!(p.startsWith(m.dir) || m.facets.some((f) => f.file === p))) fail(p, `declares Capability '${m.capability}' but is not listed in ${m.manifestPath}`);
  }

  // Frame terms used by a leaf module require an explicit binds: declaration.
  if (frame) {
    for (const m of modules.filter((x) => x.role === 'leaf')) {
      const files = [...new Set([...m.facets.map((f) => f.file), ...listFiles(path.join(root, m.dir)).map(rel)])].filter((f) => f !== m.manifestPath && exists(f));
      const used = [];
      for (const f of files) {
        const text = readText(path.join(root, f));
        for (const term of frame.frameTerms) if (contains(text, term)) used.push(`${f} uses '${term}'`);
      }
      const declared = m.binds && m.binds !== 'none' ? m.binds.split(/[\s,]+/)[0] : null;
      if (declared && declared !== frame.capability) fail(m.manifestPath, `binds '${declared}', which is not the selected frame '${frame.capability}'`);
      if (used.length && !declared) fail(m.manifestPath, `module artifacts use frame-specific terms but the manifest declares no "binds: ${frame.capability}" (${used.slice(0, 3).join('; ')})`);
      if (!used.length && declared) warn(m.manifestPath, `declares binds: ${declared} but no artifact uses a frame term; express the binding through roles or drop it`);
    }
  }

  // Rules: level directories, paths, minimum scope.
  for (const [p, d] of docs) {
    if (!p.startsWith('.claude/rules/')) continue;
    const parts = p.split('/');
    if (!LEVELS.includes(levelDir(p))) fail(p, `rule outside a level directory (${LEVELS.join(', ')})`);
    if (d.header && d.header.Level !== levelDir(p)) fail(p, `header Level '${d.header.Level}' does not match directory '${levelDir(p)}'`);
    const pathsBlock = d.fm.match(/^paths:\s*\n((?:\s+-\s+.+\n?)+)/m);
    const globs = pathsBlock ? [...pathsBlock[1].matchAll(/-\s+"?([^"\n]+?)"?\s*$/gm)].map((m) => m[1]) : [];
    if (globs.length === 0) fail(p, 'rule must declare non-empty "paths:" frontmatter');
    if (parts.length > 4 && d.header && !d.header.Capability) fail(p, 'rule in a capability subdirectory must declare "Capability:"');
    const scopes = ((d.header && d.header.Scope) || '').split('(')[0].split(',').map((s) => s.trim()).filter((s) => s in SCOPE_GLOBS);
    for (const scope of scopes) {
      const need = SCOPE_GLOBS[scope];
      const covered = globs.includes('**/*') || globs.includes(need) || (scope === 'backend-tests' && globs.includes('backend/**/*'));
      if (!covered) fail(p, `Scope '${scope}' requires paths covering "${need}"`);
    }
  }

  // Always-loaded surface: CLAUDE.md imports.
  const claudeMd = docs.get('CLAUDE.md');
  if (!claudeMd) fail('CLAUDE.md', 'missing entry point');
  const imports = claudeMd ? [...claudeMd.body.matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]) : [];
  for (const imp of imports) {
    if (!exists(imp)) { fail('CLAUDE.md', `import does not resolve: @${imp}`); continue; }
    const d = docs.get(imp);
    if (d && d.header && !/^always/.test(d.header.Loading)) fail(imp, 'imported by CLAUDE.md but header Loading is not "always"');
  }
  for (const [p, d] of docs) {
    if (p !== 'CLAUDE.md' && d.header && /^always/.test(d.header.Loading) && !imports.includes(p)) fail(p, 'declares "Loading: always" but is not imported by CLAUDE.md');
  }

  // Decisions stay stratified: "Decided:" content only in the frame style facet (Level 1) and Level 3 rules.
  for (const [p, d] of docs) {
    if (!/^\s*-?\s*Decided:/m.test(d.body)) continue;
    const ok = (d.header && d.header.Level === '3-project' && p.startsWith('.claude/rules/')) || (d.header && d.header.Facet === 'architecture.style');
    if (!ok) fail(p, 'holds "Decided:" decision content; decisions live in the frame style rule (Level 1) and Level 3 decision rules only');
  }
  if (existsSync(path.join(claude, 'decisions'))) fail('.claude/decisions', 'a cross-level decision register is not part of this system; keep decisions stratified by level');

  // Implementation-name leakage (bodies and skill descriptions, which are always loaded). A module's
  // identity is its leak tokens plus its implementation name; a leaf manifest's binds: declaration is the
  // one sanctioned place to name the frame capability.
  const identityOf = (m) => [...new Set([...m.tokens, m.impl])];
  for (const [p, d] of docs) {
    if (LEAK_ALLOWED.has(p)) continue;
    const owner = ownerOf(p);
    const text = `${d.description}\n${d.body}`.replace(/^(- binds:\s*)[a-z-]+\/[a-z0-9-]+/m, (all, label) => (modules.some((m) => m.manifestPath === p) ? label : all));
    for (const m of modules) {
      if (owner === m) continue;
      for (const token of identityOf(m)) {
        if (namesIdentity(text, token)) fail(p, `names '${token}' from module ${m.capability}; use slot/facet/role vocabulary or move the content into the module`);
      }
      if (text.includes(m.dir) && !(m.role === 'frame' && p.startsWith('.claude/capabilities/architecture/'))) fail(p, `references the module directory ${m.dir}; refer to its facets by role (<slot>.<facet>)`);
    }
  }
  // Hook and script code carries no implementation names: module-specific behavior comes from facet data.
  for (const file of [...listFiles(path.join(claude, 'hooks'), (f) => f.endsWith('.mjs')), ...listFiles(path.join(claude, 'scripts'), (f) => f.endsWith('.mjs'))]) {
    const text = readText(file);
    for (const m of modules) for (const token of identityOf(m)) if (namesIdentity(text, token)) fail(rel(file), `tooling hardcodes '${token}' from module ${m.capability}; read it from the module's facet data`);
  }

  // Technology lexicon harvested from the template itself.
  const lexicon = new Set(TECHNOLOGY_NAMES);
  const codeIdentifiers = new Set();
  const proseTerms = [];
  const harvestExclude = new Set([...STABLE_WORDS, ...BASE_VOCABULARY, ...(frame ? frame.frameTerms : []), 'ASP', 'NET', 'Core', 'Git', 'NuGet', 'HTTP']);
  for (const m of modules) for (const t of m.tokens) lexicon.add(t);
  for (const [p, d] of docs) {
    if (!d.header || RANK[d.header.Level] < 2) continue;
    for (const section of d.body.split(/^## /m).filter((s) => /^(Platform bindings|Bindings)\b/.test(s))) {
      for (const span of codeSpans(section)) for (const id of apiIdentifiers(span)) { lexicon.add(id); codeIdentifiers.add(id); }
      proseTerms.push(...bindingProseTerms(section, harvestExclude));
    }
    for (const span of codeSpans(d.body)) if (/^[A-Z][A-Za-z0-9]+(\.[A-Z][A-Za-z0-9]+)+$/.test(span.trim()) && !span.startsWith('ASP.NET')) lexicon.add(span.trim());
  }
  const harvestJson = (value) => {
    if (typeof value === 'string') { if (/^[A-Za-z@][\w.@/-]*$/.test(value) && /[A-Z]/.test(value[0]) && value.length > 3 && !value.startsWith('.claude')) lexicon.add(value.replace(/\/$/, '')); }
    else if (Array.isArray(value)) value.forEach(harvestJson);
    else if (value && typeof value === 'object') for (const [k, v] of Object.entries(value)) if (['id', 'prefix'].includes(k) || /Packages|Prefixes|Frameworks/.test(k)) harvestJson(v); else if (typeof v === 'object') harvestJson(v);
  };
  for (const m of modules) for (const f of m.facets) if (f.file.endsWith('.json') && exists(f.file)) { try { harvestJson(JSON.parse(readText(path.join(root, f.file)))); } catch { /* reported above */ } }
  if (exists('.claude/hooks/manifest-policy.json')) harvestJson(JSON.parse(readText(path.join(root, '.claude/hooks/manifest-policy.json'))));
  for (const t of [...lexicon]) {
    const head = t.split('.')[0];
    if (BASE_VOCABULARY.has(t) || PLATFORM_NAMES.includes(t) || (t.includes('.') && (BASE_VOCABULARY.has(head) || head === 'System' || (frame && frame.frameTerms.includes(head))))) lexicon.delete(t);
  }

  for (const m of modules) lexicon.add(m.impl);
  const caseSensitive = (term) => COMMON_WORD_NAMES.has(term) || (codeIdentifiers.has(term) && /^[A-Z][a-z]+$/.test(term));
  const terms = [...lexicon, ...proseTerms.map((t) => t.term)]
    .filter((term, i, all) => term && all.findIndex((x) => x.toLowerCase() === term.toLowerCase()) === i)
    .map((term) => ({ term, ci: !caseSensitive(term) }));
  const isTechnology = (word) => terms.some((t) => hasTerm(word, t));

  // No legalizing by allow-listing: allow-lists and frame-terms hold no technology vocabulary, and a
  // case-sensitive common-word name is never a selected implementation's identity.
  const checker = '.claude/scripts/check-instructions.mjs';
  for (const w of [...BASE_VOCABULARY, ...STABLE_WORDS, ...STABLE_PHRASES]) if (isTechnology(w)) fail(checker, `allow-listed vocabulary '${w}' is technology vocabulary`);
  for (const w of COMMON_WORD_NAMES) for (const m of modules) if (identityOf(m).some((t) => namesIdentity(w, t))) fail(checker, `common-word name '${w}' is the identity of module ${m.capability}; implementation names always match case-insensitively`);
  if (frame) for (const w of frame.frameTerms) if (isTechnology(w)) fail(frame.manifestPath, `frame-terms lists technology vocabulary '${w}'; frame terms name architecture concepts only`);
  if (frame) for (const w of frame.examples) if (isTechnology(w)) fail(frame.manifestPath, `placement-examples lists technology vocabulary '${w}'; examples name project-owned code only`);

  // Frame vocabulary classes. Metadata alone never legalizes a code identifier; each class is honored only
  // on positive evidence in the frame's own facets (the manifest is not evidence):
  //  1. plain frame-terms (words and phrases) serve prose and binds: detection;
  //  2. API-shaped frame-terms are frame code names, honored only when anchored: Add<Layer> for a layer the
  //     style facet maps to a project, or the code spelling of a multi-word phrase the frame's facets state
  //     in plain words ("Unit of Work" -> IUnitOfWork);
  //  3. placement-examples are honored only where the placement facet places them: inside its directory
  //     trees, as folder paths, or as naming variants that extend a placed example with the facet's own words.
  const wordsOf = (id) => id.replace(/^I(?=[A-Z])/, '').match(/[A-Z][a-z0-9]*|[a-z0-9]+/g) || [];
  const isCodeName = (t) => apiIdentifiers(t).length > 0;
  const frameFacet = (name) => frame && frame.facets.find((f) => f.facet === `${frame.slot}.${name}` && docs.has(f.file));
  const frameProse = frame ? ` ${frame.facets.filter((f) => docs.has(f.file)).map((f) => proseOf(docs.get(f.file).body)).join(' ').toLowerCase().replace(/[^a-z0-9]+/g, ' ')} ` : ' ';
  const layers = new Set(frameFacet('style') ? [...docs.get(frameFacet('style').file).body.matchAll(/`[a-z-]+\/<Name>\.([A-Z][A-Za-z]+)`/g)].map((m) => m[1]) : []);
  const anchored = (id) => {
    const add = id.match(/^Add([A-Z][A-Za-z0-9]*)$/);
    if (add) return layers.has(add[1]);
    const w = wordsOf(id);
    return w.length >= 2 && frameProse.includes(` ${w.join(' ').toLowerCase()} `);
  };
  const placement = frameFacet('layout') ? docs.get(frameFacet('layout').file) : null;
  const placementPath = placement ? frameFacet('layout').file : null;
  const examples = new Set(frame ? frame.examples : []);
  const treeText = placement ? [...placement.body.matchAll(/```[^\n]*\n([\s\S]*?)```/g)].map((m) => m[1]).join('\n') : '';
  const PASCAL = /(?<![\w.])([A-Z][A-Za-z0-9]+)(?![A-Za-z0-9])/g;
  const treeNames = new Set([...treeText.matchAll(PASCAL)].map((m) => m[1]));
  const placementSpans = placement ? [...placement.body.replace(/```[^\n]*\n[\s\S]*?```/g, ' ').matchAll(/`([^`\n]+)`/g)].map((m) => m[1]) : [];
  const placementWords = new Set([...(placement ? proseOf(placement.body).toLowerCase().match(/[a-z]+/g) || [] : []),
    ...placementSpans.filter((s) => /^[A-Z][a-z]+$/.test(s)).map((s) => s.toLowerCase())]);
  const stems = new Set([...treeNames].filter((n) => examples.has(n)).map((n) => wordsOf(n)[0]));
  const namingVariant = (id) => { const w = wordsOf(id); return w.length >= 2 && stems.has(w[0]) && w.slice(1).every((x) => placementWords.has(x.toLowerCase())); };
  const placed = (id) => treeNames.has(id) || placementSpans.includes(`${id}/`) || (placementSpans.includes(id) && namingVariant(id));
  const frameCodeNames = new Set(frame ? frame.frameTerms.filter((t) => isCodeName(t) && anchored(t)) : []);
  if (frame) {
    for (const t of frame.frameTerms.filter((x) => isCodeName(x) && !anchored(x))) fail(frame.manifestPath, `frame-terms lists code identifier '${t}', which the frame's own wording does not anchor (Add<Layer> for a mapped layer, or the code spelling of a phrase its facets state in plain words); frame metadata cannot legalize implementation identifiers`);
    for (const t of frame.examples.filter((x) => !placed(x))) fail(frame.manifestPath, `placement-examples lists '${t}', which the placement facet does not place (directory tree, folder path, or naming variant of a placed example); frame metadata cannot legalize implementation identifiers`);
  }
  // Placement examples are masked only at the positions where the placement facet places them.
  const maskPlacement = (body) => body
    .replace(/```[^\n]*\n[\s\S]*?```/g, (block) => block.replace(PASCAL, (id) => (examples.has(id) ? ' ' : id)))
    .replace(/`([A-Z][A-Za-z0-9]+)(\/?)`/g, (span, id, slash) => (examples.has(id) && (slash || namingVariant(id)) ? ' ' : span));
  // The manifest's own vocabulary declarations are validated above, not read as usage.
  const stripDeclarations = (body) => body.replace(/^- (frame-terms|placement-examples):.*$/gm, ' ');

  // Core and Architecture use the fixed platform vocabulary only.
  // Routing targets: the Level 2+ skills and the engineering subjects their names, descriptions, and "Owns:" declare.
  const techniqueDocs = [...docs].filter(([p, d]) => /^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(p) && d.header && RANK[d.header.Level] >= 2);
  const techniqueSkills = {
    skills: new Set(techniqueDocs.map(([p]) => p.split('/')[2])),
    subject: new Set(techniqueDocs.flatMap(([p, d]) => subjectWords(`${p.split('/')[2]} ${d.description} ${d.header.Owns || ''}`))),
    core: new Map(techniqueDocs.map(([p, d]) => [p.split('/')[2], new Set(subjectWords(`${p.split('/')[2]} ${d.header.Owns || ''}`).filter((w) => !JOINERS.has(w)))])),
  };
  for (const [p, d] of docs) {
    if (!d.header || !['0-core', '1-architecture'].includes(d.header.Level)) continue;
    const isFrame = frame && ownerOf(p) === frame;
    let body = d.body;
    if (isFrame && p === frame.manifestPath) body = stripDeclarations(body);
    if (isFrame && p === placementPath) body = maskPlacement(body);
    const text = stripRoutingPointers(stripTooling(`${d.description}\n${body}`), techniqueSkills);
    const allowed = (id) => BASE_VOCABULARY.has(id) || (isFrame && frameCodeNames.has(id));
    const level = `Level ${d.header.Level}`;
    const frameVocabulary = isFrame ? [...frame.frameTerms.filter((t) => !isCodeName(t)), ...frameCodeNames] : [];
    for (const t of terms) {
      if (isFrame && (frameVocabulary.some((f) => f.toLowerCase() === t.term.toLowerCase()) || identityOf(frame).includes(t.term))) continue;
      if (hasTerm(text, t)) fail(p, `${level} names concrete technology '${t.term}'; keep the neutral policy here and bind '${t.term}' at Level 2`);
    }
    for (const m of text.matchAll(/ASP\.NET Core\s+([A-Za-z][\w-]*)/gi)) {
      if (/^[A-Z]/.test(m[1]) || !PLATFORM_FOLLOWERS.has(m[1].toLowerCase())) fail(p, `${level} names framework technique 'ASP.NET Core ${m[1]}'; only the bare platform name is platform vocabulary`);
    }
    const frameWords = isFrame ? [...frameVocabulary, ...frame.tokens].map((w) => w.replace(/\/$/, '')) : [];
    const words = new Set([...STABLE_WORDS, ...BASE_VOCABULARY, ...frameWords.filter((w) => !/\s/.test(w))]);
    for (const w of unexpectedCapitals(proseOf(text), [...STABLE_PHRASES, ...frameWords.filter((x) => /\s/.test(x))], words)) {
      fail(p, `${level} uses '${w}', which is neither fixed-platform, stable architecture/process${isFrame ? ', nor frame' : ''} vocabulary; name the role or bind the technology at Level 2`);
    }
    // Fail closed in frame artifacts too: anchored frame code names are their only extra identifiers.
    const vocabulary = `fixed-platform or stable-role${isFrame ? ' or frame-manifest' : ''} vocabulary`;
    for (const span of codeSpans(text)) for (const id of apiIdentifiers(span)) if (!allowed(id)) fail(p, `${level} code identifier '${id}' is not ${vocabulary}; move it to a Level 2 binding`);
    for (const id of apiIdentifiers(proseOf(text))) if (!allowed(id)) fail(p, `${level} names '${id}', which is not ${vocabulary}; move it to a Level 2 binding`);
  }
  // Level 0/1 enforcement data carries no package identifiers.
  for (const m of modules) {
    for (const f of m.facets.filter((x) => x.file.endsWith('.json') && RANK[x.level] < 2 && exists(x.file))) {
      const data = JSON.parse(readText(path.join(root, f.file)));
      delete data.$comment;
      const flat = JSON.stringify(data);
      for (const t of terms) if (hasTerm(flat, t)) fail(f.file, `Level ${f.level} data names concrete technology '${t.term}'; move it to a Level 2 enforcement facet`);
      for (const mm of flat.matchAll(/"([A-Z][A-Za-z0-9]+(?:\.[A-Z][A-Za-z0-9]+)+)"/g)) fail(f.file, `Level ${f.level} data holds package identifier '${mm[1]}'; move it to a Level 2 enforcement facet`);
    }
  }

  // Conformance dependencies point to the same or a more stable level; references to less stable
  // artifacts from rules and CLAUDE.md must be labeled routing pointers. Imports are loading, not conformance.
  const levelOf = (ref) => {
    if (ref === '.claude/INSTRUCTION_MAP.md') return null; // the human map is never a conformance target
    if (ref.startsWith('.claude/')) { const d = docs.get(ref); return d && d.header ? d.header.Level : null; }
    return facetLevel(ref);
  };
  for (const [p, d] of docs) {
    if (!(p === 'CLAUDE.md' || p.startsWith('.claude/rules/')) || !d.header) continue;
    const from = RANK[d.header.Level];
    for (const line of d.body.split('\n')) {
      if (/^@/.test(line)) continue;
      const refs = [...line.matchAll(/`(\.claude\/[^`\s]+\.md)`/g)].map((m) => m[1])
        .concat([...line.matchAll(/(?<![\w./-])((?:architecture|persistence|backend-testing|frontend)\.[a-z][a-z-]*)(?![\w-])/g)].map((m) => m[1]));
      for (const ref of refs) {
        const to = levelOf(ref);
        if (to === null || RANK[to] <= from) continue;
        if (!ROUTING_LABEL.test(line)) fail(p, `Level ${d.header.Level} depends on less stable ${to} artifact '${ref}'; use a labeled routing pointer (Technique:, Commands:, Framework binding: ...) or move the content`);
      }
    }
  }

  // Facet references.
  for (const [p, d] of docs) {
    for (const m of `${d.description}\n${d.body}`.matchAll(/(?<![\w./-])(architecture|persistence|backend-testing|frontend)\.([a-z][a-z-]*)(?![\w-])/g)) {
      const [ref, slot] = [m[0], m[1]];
      const mod = modules.find((x) => x.slot === slot);
      if (!mod) { if (SLOTS[slot].requirement === 'required') fail(p, `facet reference '${ref}' but slot '${slot}' has no module`); continue; }
      if (!mod.facets.some((f) => f.facet === ref)) fail(p, `facet reference '${ref}' is not declared in ${mod.manifestPath}`);
    }
  }

  // Skills and agents.
  const skillsDir = path.join(claude, 'skills');
  const skills = existsSync(skillsDir) ? readdirSync(skillsDir).filter((e) => existsSync(path.join(skillsDir, e, 'SKILL.md'))) : [];
  const agents = listFiles(path.join(claude, 'agents'), (f) => f.endsWith('.md')).map((f) => path.basename(f, '.md'));
  const moduleKnowledge = modules.flatMap((m) => m.facets.filter((f) => f.facet.endsWith('.knowledge')).map((f) => f.file.split('/')[2]));
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_SHARED_KNOWLEDGE, ...moduleKnowledge]) {
    if (!skills.includes(name)) fail(`.claude/skills/${name}`, 'required skill is missing');
  }
  for (const name of skills) {
    const p = `.claude/skills/${name}/SKILL.md`;
    const d = docs.get(p);
    const fmName = (d.fm.match(/^name:\s*(.+)$/m) || [])[1];
    if (fmName !== name) fail(p, `frontmatter name '${fmName}' must equal directory '${name}'`);
    if (!d.description) fail(p, 'missing description');
    else if (d.description.length > 360) warn(p, `description is ${d.description.length} chars; keep skill listings compact`);
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
    const re = /`([a-z][a-z0-9-]*)`(?=\s+(?:skill|workflow|agent)\b)|(?:\brun|→|Technique:|Procedure:|Procedures:)\s+`([a-z][a-z0-9-]*)`/g;
    for (const m of d.body.matchAll(re)) {
      const name = m[1] || m[2];
      if (!known.has(name)) fail(p, `references unknown skill or agent '${name}'`);
    }
  }

  // Path references.
  for (const [p, d] of docs) {
    for (const m of d.body.matchAll(/`(\.claude\/[^`\s]+|references\/[^`\s]+)`/g)) {
      const target = m[1].replace(/[.,;:]+$/, '');
      if (/[<*>$]/.test(target)) continue;
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

  // Human map coverage: every instruction artifact and enforcement asset is listed.
  const map = docs.get('.claude/INSTRUCTION_MAP.md');
  if (!map) fail('.claude/INSTRUCTION_MAP.md', 'missing instruction map');
  else {
    const assets = [...docs.keys(), ...modules.flatMap((m) => m.facets.map((f) => f.file)),
      ...['hooks', 'scripts'].flatMap((d) => listFiles(path.join(claude, d), (f) => /\.(mjs|json)$/.test(f)).map(rel)), '.claude/settings.json'];
    for (const p of new Set(assets)) if (p !== '.claude/INSTRUCTION_MAP.md' && exists(p) && !map.body.includes(p)) fail('.claude/INSTRUCTION_MAP.md', `does not list ${p}`);
    if (imports.includes('.claude/INSTRUCTION_MAP.md')) fail('CLAUDE.md', 'the instruction map must not be auto-loaded');
  }

  checkHooks(root, exists);

  for (const w of warnings) console.log(`WARNING   ${w}`);
  for (const v of violations) console.log(`VIOLATION ${v}`);
  console.log(`Instruction check of ${toPosix(root)}: ${violations.length === 0 ? 'PASS' : 'FAIL'} (${docs.size} artifacts, ${violations.length} violation(s), ${warnings.length} warning(s)).`);
  process.exit(violations.length === 0 ? 0 : 1);
}

// Hooks: exec form (`command` + `args`), the launcher placeholder used only as argument data, existing
// scripts, the required events and matchers, fail-closed critical PreToolUse, non-blocking post/Stop hooks.
const REQUIRED_HOOKS = [
  { event: 'PreToolUse', tools: ['Bash', 'PowerShell'], script: 'pre-bash-dependency.mjs', critical: true },
  { event: 'PostToolUse', tools: ['Edit', 'Write', 'MultiEdit'], script: 'post-change-checks.mjs' },
  { event: 'PostToolUse', tools: ['Bash', 'PowerShell'], script: 'post-change-checks.mjs' },
  { event: 'PostToolUseFailure', tools: ['Bash', 'PowerShell'], script: 'post-change-checks.mjs' },
  { event: 'Stop', tools: null, script: 'stop-cochange.mjs' },
];
const SCRIPT_ARG = /^\$\{CLAUDE_PROJECT_DIR\}\/(\.claude\/(?:hooks|scripts)\/[A-Za-z0-9._-]+\.mjs)$/;

function checkHooks(root, exists) {
  const file = '.claude/settings.json';
  if (!exists(file)) { fail(file, 'missing'); return; }
  let settings;
  try { settings = JSON.parse(readText(path.join(root, file))); } catch (error) { fail(file, `invalid JSON (${error.message})`); return; }
  const registered = [];
  for (const [event, groups] of Object.entries(settings.hooks || {})) {
    if (!Array.isArray(groups)) { fail(file, `${event} must be an array of matcher groups`); continue; }
    for (const group of groups) {
      const tools = typeof group.matcher === 'string' && group.matcher ? group.matcher.split('|').map((t) => t.trim()) : null;
      for (const hook of group.hooks || []) {
        const where = `${event}${group.matcher ? ` [${group.matcher}]` : ''}`;
        if (hook.type !== 'command') { fail(file, `${where} hook type must be "command"`); continue; }
        if (hook.command !== 'node') fail(file, `${where} hook must use exec form with "command": "node" (found ${JSON.stringify(hook.command)}); shell strings depend on the working directory and shell`);
        if (!Array.isArray(hook.args) || hook.args.length !== 1) { fail(file, `${where} hook must pass exactly the script path in "args"`); continue; }
        const m = String(hook.args[0]).match(SCRIPT_ARG);
        if (!m) { fail(file, `${where} hook arg must be "\${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs" (placeholder as data, no other expansion): ${hook.args[0]}`); continue; }
        if (!exists(m[1])) fail(file, `${where} hook script missing: ${m[1]}`);
        if (!(Number(hook.timeout) > 0)) fail(file, `${where} hook needs a positive timeout`);
        const isCritical = REQUIRED_HOOKS.some((r) => r.critical && r.event === event && path.posix.basename(m[1]) === r.script);
        if (isCritical && hook.onFailure !== 'block') fail(file, `${where} ${path.posix.basename(m[1])} is policy-critical and must set "onFailure": "block" (fail closed)`);
        if (!isCritical && hook.onFailure === 'block') fail(file, `${where} ${path.posix.basename(m[1])} must not block on failure; post and Stop hooks run after the action and stay non-blocking`);
        registered.push({ event, tools, script: path.posix.basename(m[1]), onFailure: hook.onFailure });
      }
    }
  }
  for (const req of REQUIRED_HOOKS) {
    const ok = registered.some((r) => r.event === req.event && r.script === req.script && (req.tools === null || (r.tools && req.tools.every((t) => r.tools.includes(t)))));
    if (!ok) fail(file, `missing ${req.event} registration of ${req.script}${req.tools ? ` for ${req.tools.join('|')}` : ''}`);
  }
}

try {
  main();
} catch (error) {
  console.error(`Instruction check could not run: ${error.message}`);
  process.exit(2);
}
