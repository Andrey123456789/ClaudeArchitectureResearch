// Level 3 Project · enforcement asset: instruction-structure checker for the stability-level model.
// Usage: node .claude/tools/check-instructions.mjs   (exit 0 = valid, 1 = structural errors)
// Validates level-first rule layout, classification headers, `paths` declarations, technology
// neutrality of Levels 0-1, dependency direction and acyclicity, imports, internal references,
// skill-private references, hook commands, map completeness, and the always-loaded size estimate.
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const LEVEL_DIRS = { '0-core': 0, '1-architecture': 1, '2-technology': 2, '3-project': 3 };
const LEVEL_NAMES = ['Core', 'Architecture', 'Technology', 'Project'];
const PRODUCT_INPUTS = ['SPECIFICATION.md', 'CUSTOM_SETTINGS.md'];
const MAP = '.claude/INSTRUCTION_MAP.md';
const BUDGET_TOKENS = 5500;

const REQUIRED_WORKFLOWS = [
  'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow',
  'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance',
];
const REQUIRED_KNOWLEDGE = [
  'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory',
  'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check',
  'docker', 'ci-cd', 'angular', 'modern-csharp', 'authentication',
];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];

// Concrete technologies that Levels 0 and 1 must not name (fixed platform: .NET, C#, TypeScript; Git).
const TECHNOLOGY_TERMS = [
  /EF Core/i, /Entity Framework/i, /\bDbContext\b/, /\bDbSet\b/, /\bNUnit\b/i, /\bxUnit\b/i, /\bMSTest\b/i,
  /\bAngular\b/i, /\bRxJS\b/i, /\bSerilog\b/i, /\bFluentValidation\b/i, /ASP\.NET/i, /\bSwashbuckle\b/i,
  /\bSwagger\b/i, /\bDocker\b/i, /\bKubernetes\b/i, /\bnpm\b/i, /\bNuGet\b/i, /SQL Server/i, /\bSqlServer\b/i,
  /\bPostgreSQL\b/i, /\bRedis\b/i, /\bMapster\b/i, /\bAutoMapper\b/i, /\bPolly\b/i, /\bPlaywright\b/i,
  /\bVitest\b/i, /\bJest\b/i, /\bTestcontainers\b/i, /\bMediatR\b/i, /\bKommand\b/i, /\bHybridCache\b/,
  /\bIExceptionHandler\b/, /\bProblemDetails\b/, /\bIActionResult\b/, /\bActionResult\b/,
  /\bWebApplicationFactory\b/, /GitHub Actions/i, /\bScrutor\b/i, /\bef-core\b/i, /\baspnet/i,
];

function toPosix(p) {
  return p.split(path.sep).join('/');
}

function listFiles(root, dir) {
  const abs = path.join(root, dir);
  if (!existsSync(abs)) return [];
  const out = [];
  const walk = current => {
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) walk(full);
      else out.push(toPosix(path.relative(root, full)));
    }
  };
  walk(abs);
  return out.sort();
}

function parseFrontmatter(text) {
  if (!text.startsWith('---\n') && !text.startsWith('---\r\n')) return { data: null, body: text };
  const end = text.indexOf('\n---', 4);
  if (end < 0) return { data: null, body: text, error: 'unterminated frontmatter' };
  const raw = text.slice(text.indexOf('\n') + 1, end).replace(/\r/g, '');
  const body = text.slice(text.indexOf('\n', end + 1) + 1);
  const data = {};
  let currentKey = null;
  for (const line of raw.split('\n')) {
    const item = line.match(/^\s+-\s+"?([^"]*)"?\s*$/);
    const pair = line.match(/^([A-Za-z-]+):\s*(.*)$/);
    if (item && currentKey) {
      if (!Array.isArray(data[currentKey])) data[currentKey] = [];
      data[currentKey].push(item[1]);
    } else if (pair) {
      currentKey = pair[1];
      data[currentKey] = pair[2] === '>' || pair[2] === '|' ? '' : pair[2];
    } else if (currentKey && typeof data[currentKey] === 'string' && line.trim()) {
      data[currentKey] = `${data[currentKey]} ${line.trim()}`.trim();
    }
  }
  return { data, body };
}

function parseHeader(body) {
  const first = body.split(/\r?\n/).find(line => line.trim().length > 0) ?? '';
  const match = first.match(/^> Level: (\d) (\w+) · Owns: (.+?) · Scope: (.+?) · Loads: (.+?) · Depends on: (.+)$/);
  if (!match) return null;
  return {
    level: Number(match[1]),
    levelName: match[2],
    owns: match[3],
    scope: match[4],
    loads: match[5],
    dependsOn: match[6].trim() === 'none'
      ? []
      : match[6].split(',').map(item => item.replace(/\(.*?\)/g, '').trim()).filter(Boolean),
  };
}

function stripCodeFences(text) {
  return text.replace(/```[\s\S]*?```/g, '');
}

export function checkInstructions(root) {
  const errors = [];
  const warnings = [];
  const info = [];
  const read = file => {
    const text = readFileSync(path.join(root, file), 'utf8');
    return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  };

  if (!existsSync(path.join(root, 'CLAUDE.md')) || !existsSync(path.join(root, '.claude'))) {
    errors.push(`not a template root: CLAUDE.md or .claude/ missing under ${root}`);
    return { errors, warnings, info };
  }

  // ---- collect instruction artifacts ----
  const ruleFiles = listFiles(root, '.claude/rules').filter(f => f.endsWith('.md'));
  const skillFiles = listFiles(root, '.claude/skills').filter(f => f.endsWith('.md'));
  const agentFiles = listFiles(root, '.claude/agents').filter(f => f.endsWith('.md'));
  const artifacts = ['CLAUDE.md', ...ruleFiles, ...skillFiles, ...agentFiles, MAP];
  const meta = new Map();

  for (const file of artifacts) {
    if (!existsSync(path.join(root, file))) {
      errors.push(`${file}: missing`);
      continue;
    }
    const text = read(file);
    const { data, body, error } = parseFrontmatter(text);
    if (error) errors.push(`${file}: ${error}`);
    const header = parseHeader(body);
    if (!header) {
      errors.push(`${file}: first line must be the classification header '> Level: N Name · Owns: … · Scope: … · Loads: … · Depends on: …'`);
      continue;
    }
    if (LEVEL_NAMES[header.level] !== header.levelName) errors.push(`${file}: Level ${header.level} must be named '${LEVEL_NAMES[header.level]}'`);
    if (/(^|\n)\s*>?\s*Kind:/.test(text)) errors.push(`${file}: 'Kind:' classification is not part of this instruction model`);
    meta.set(file, { header, data, body, text });
  }

  // ---- rules: level-first layout and paths ----
  for (const file of ruleFiles) {
    const parts = file.split('/');
    if (parts.length !== 4 || !(parts[2] in LEVEL_DIRS)) {
      errors.push(`${file}: rules must live in .claude/rules/{0-core,1-architecture,2-technology,3-project}/`);
      continue;
    }
    const entry = meta.get(file);
    if (!entry) continue;
    if (entry.header.level !== LEVEL_DIRS[parts[2]]) errors.push(`${file}: header Level ${entry.header.level} does not match directory ${parts[2]}`);
    const paths = entry.data?.paths;
    if (!Array.isArray(paths) || paths.length === 0 || paths.some(p => !p.trim())) errors.push(`${file}: every rule file must declare a non-empty 'paths' list`);
  }

  // ---- CLAUDE.md imports ----
  const claude = meta.get('CLAUDE.md');
  const imports = [...read('CLAUDE.md').matchAll(/^@(\S+)\s*$/gm)].map(m => m[1]);
  if (claude && claude.header.level !== 0) errors.push('CLAUDE.md: must be Level 0 Core');
  for (const target of imports) {
    if (!existsSync(path.join(root, target))) errors.push(`CLAUDE.md: import ${target} does not resolve`);
  }
  const expectedImports = ['.claude/rules/1-architecture/overview.md', '.claude/rules/3-project/decisions.md'];
  for (const expected of expectedImports) {
    if (!imports.includes(expected)) errors.push(`CLAUDE.md: must import the stratified decision summary ${expected}`);
  }
  for (const target of imports) {
    if (!expectedImports.includes(target)) warnings.push(`CLAUDE.md: additional import ${target} enlarges the always-loaded surface`);
  }

  // ---- skills and agents ----
  const skillDirs = existsSync(path.join(root, '.claude/skills'))
    ? readdirSync(path.join(root, '.claude/skills')).filter(name => statSync(path.join(root, '.claude/skills', name)).isDirectory())
    : [];
  const skillNames = new Set();
  for (const dir of skillDirs) {
    const file = `.claude/skills/${dir}/SKILL.md`;
    const entry = meta.get(file);
    if (!entry) {
      errors.push(`${file}: missing`);
      continue;
    }
    if (entry.data?.name !== dir) errors.push(`${file}: frontmatter name must be '${dir}'`);
    if (!entry.data?.description) errors.push(`${file}: frontmatter description is required`);
    skillNames.add(dir);
  }
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_KNOWLEDGE]) {
    if (!skillNames.has(name)) errors.push(`required skill '${name}' is missing`);
  }
  for (const name of FORBIDDEN_SKILLS) {
    if (skillNames.has(name)) errors.push(`standalone skill '${name}' duplicates a private reference of the knowledge surface`);
  }
  const maintenance = meta.get('.claude/skills/template-maintenance/SKILL.md');
  if (maintenance && maintenance.data?.['disable-model-invocation'] !== 'true') {
    errors.push('template-maintenance: must set disable-model-invocation: true (user-only)');
  }
  const agentNames = new Set();
  for (const file of agentFiles) {
    const entry = meta.get(file);
    if (!entry) continue;
    if (!entry.data?.name || !entry.data?.description) errors.push(`${file}: agent frontmatter needs name and description`);
    agentNames.add(entry.data?.name);
  }
  const reviewer = meta.get('.claude/agents/code-reviewer.md');
  if (!reviewer) errors.push('agent code-reviewer is missing');
  else {
    const disallowed = String(reviewer.data?.disallowedTools ?? '');
    if (!/\bWrite\b/.test(disallowed) || !/\bEdit\b/.test(disallowed)) errors.push('code-reviewer: must disallow Write and Edit (read-only)');
    if (!reviewer.body.includes('.claude/skills/code-review/SKILL.md')) errors.push('code-reviewer: must delegate to .claude/skills/code-review/SKILL.md');
  }

  // ---- technology neutrality of Levels 0 and 1 ----
  for (const [file, entry] of meta) {
    if (entry.header.level > 1 || file === MAP) continue;
    for (const term of TECHNOLOGY_TERMS) {
      const hit = entry.text.match(term);
      if (hit) errors.push(`${file}: Level ${entry.header.level} must not name the concrete technology '${hit[0]}'`);
    }
  }

  // ---- dependency direction and acyclicity ----
  const graph = new Map();
  for (const [file, entry] of meta) {
    const targets = [];
    for (const dep of entry.header.dependsOn) {
      if (PRODUCT_INPUTS.includes(dep)) {
        errors.push(`${file}: engineering policy must not depend on product input ${dep}`);
        continue;
      }
      if (dep.endsWith('/**')) {
        const prefix = dep.slice(0, -2);
        targets.push(...[...meta.keys()].filter(other => other.startsWith(prefix) && other !== file));
        continue;
      }
      if (!meta.has(dep)) {
        errors.push(`${file}: 'Depends on' target ${dep} is not an instruction artifact`);
        continue;
      }
      targets.push(dep);
    }
    for (const target of targets) {
      const targetLevel = meta.get(target).header.level;
      if (targetLevel > entry.header.level) {
        errors.push(`${file}: Level ${entry.header.level} must not depend on more volatile Level ${targetLevel} (${target})`);
      }
    }
    graph.set(file, targets);
  }
  const state = new Map();
  const visit = (node, trail) => {
    if (state.get(node) === 'done') return;
    if (state.get(node) === 'active') {
      errors.push(`dependency cycle: ${[...trail, node].join(' → ')}`);
      return;
    }
    state.set(node, 'active');
    for (const next of graph.get(node) ?? []) visit(next, [...trail, node]);
    state.set(node, 'done');
  };
  for (const node of graph.keys()) visit(node, []);

  // ---- internal references ----
  const ruleByBase = new Map();
  for (const file of ruleFiles) {
    const base = path.posix.basename(file);
    ruleByBase.set(base, ruleByBase.has(base) ? null : file);
  }
  const resolveReference = (from, token) => {
    if (token.startsWith('.claude/') || PRODUCT_INPUTS.includes(token) || token === 'CLAUDE.md') return token;
    if (/^[0-3]-[a-z]+\/[A-Za-z0-9.-]+\.md$/.test(token)) return `.claude/rules/${token}`;
    if (token.startsWith('references/')) {
      const skill = from.match(/^\.claude\/skills\/[^/]+\//);
      return skill ? `${skill[0]}${token}` : null;
    }
    if (!token.includes('/')) {
      const sibling = path.posix.join(path.posix.dirname(from), token);
      if (existsSync(path.join(root, sibling))) return sibling;
      return ruleByBase.get(token) ?? null;
    }
    return token;
  };
  for (const [file, entry] of meta) {
    const text = stripCodeFences(entry.body);
    const tokens = new Set();
    for (const m of text.matchAll(/`([^`\s]+\.(?:md|mjs|json))`/g)) tokens.add(m[1]);
    for (const m of text.matchAll(/(?<![\w/.-])(\.claude\/[A-Za-z0-9_.\/-]+\.(?:md|mjs|json))/g)) tokens.add(m[1]);
    for (const dep of entry.header.dependsOn) if (!dep.endsWith('/**')) tokens.add(dep);
    for (const token of tokens) {
      if (/^(package|angular|launchSettings|global|appsettings[^`]*)\.json$/.test(token) || token === 'package-lock.json') continue;
      if (token === 'SKILL.md' || token === 'README.md' || token.endsWith('settings.local.json')) continue;
      const resolved = resolveReference(file, token);
      if (!resolved || !existsSync(path.join(root, resolved))) errors.push(`${file}: reference '${token}' does not resolve`);
      const privateRef = (resolved ?? '').match(/^\.claude\/skills\/([^/]+)\/references\//);
      if (privateRef && !file.startsWith(`.claude/skills/${privateRef[1]}/`) && file !== MAP) {
        errors.push(`${file}: skill-private reference ${resolved} may be used only by skill '${privateRef[1]}'`);
      }
    }
    for (const m of text.matchAll(/`([a-z][a-z0-9-]+)`\s+(skill|workflow|agent)\b/g)) {
      const known = m[2] === 'agent' ? agentNames.has(m[1]) : skillNames.has(m[1]);
      if (!known) errors.push(`${file}: ${m[2]} '${m[1]}' does not exist`);
    }
    for (const m of text.matchAll(/\b(?:[Rr]un|[Rr]uns|[Ff]ollow|[Ff]ollows)\s+`([a-z][a-z0-9-]+)`/g)) {
      if (!skillNames.has(m[1]) && !agentNames.has(m[1])) errors.push(`${file}: routed workflow '${m[1]}' does not exist`);
    }
  }
  for (const m of read('CLAUDE.md').matchAll(/\|\s*`([a-z][a-z0-9-]+)`/g)) {
    if (!skillNames.has(m[1]) && !agentNames.has(m[1])) errors.push(`CLAUDE.md: routing target '${m[1]}' does not exist`);
  }

  // ---- forbidden constructs of other instruction models ----
  for (const file of listFiles(root, '.claude')) {
    if (/(^|\/)(manifests?|contracts?|slots?|capabilit(y|ies))(\/|\.|$)/i.test(file.replace(/^\.claude\//, ''))) {
      errors.push(`${file}: manifests, capability contracts, and slots are not part of this instruction model`);
    }
  }

  // ---- hooks ----
  const settingsFile = path.join(root, '.claude/settings.json');
  if (!existsSync(settingsFile)) errors.push('.claude/settings.json: missing');
  else {
    let settings = null;
    try {
      settings = JSON.parse(read('.claude/settings.json'));
    } catch (error) {
      errors.push(`.claude/settings.json: invalid JSON (${error.message})`);
    }
    for (const [event, groups] of Object.entries(settings?.hooks ?? {})) {
      for (const group of groups) {
        for (const hook of group.hooks ?? []) {
          const command = String(hook.command ?? '');
          if (/[$%`]/.test(command)) errors.push(`.claude/settings.json ${event}: hook command must not rely on shell variable expansion ('${command}')`);
          const match = command.match(/^node\s+(\S+\.mjs)(\s+[a-z-]+)*$/);
          if (!match) errors.push(`.claude/settings.json ${event}: hook command must be 'node <script>.mjs <event>' ('${command}')`);
          else if (!existsSync(path.join(root, match[1]))) errors.push(`.claude/settings.json ${event}: script ${match[1]} does not exist`);
        }
      }
    }
  }

  // ---- human map completeness ----
  if (existsSync(path.join(root, MAP))) {
    const map = read(MAP);
    const mapped = [
      ...artifacts.filter(file => file !== MAP),
      ...listFiles(root, '.claude/hooks'),
      ...listFiles(root, '.claude/tools'),
      '.claude/settings.json',
    ];
    for (const file of mapped) {
      const short = file.replace(/^\.claude\/rules\//, '');
      if (!map.includes(file) && !map.includes(short)) errors.push(`${MAP}: does not list ${file}`);
    }
  }

  // ---- always-loaded surface estimate ----
  let chars = read('CLAUDE.md').length;
  for (const target of imports) if (existsSync(path.join(root, target))) chars += read(target).length;
  for (const [file, entry] of meta) {
    const listed = (file.endsWith('/SKILL.md') && entry.data?.['disable-model-invocation'] !== 'true') || file.startsWith('.claude/agents/');
    if (listed) chars += String(entry.data?.name ?? '').length + String(entry.data?.description ?? '').length + 8;
  }
  const tokens = Math.round(chars / 4);
  info.push(`always-loaded surface ≈ ${tokens} tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)`);
  if (tokens > BUDGET_TOKENS) warnings.push(`always-loaded surface ≈ ${tokens} tokens exceeds the ${BUDGET_TOKENS}-token guideline`);

  return { errors, warnings, info };
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
  const { errors, warnings, info } = checkInstructions(root);
  for (const line of info) console.log(`info: ${line}`);
  for (const line of warnings) console.log(`warning: ${line}`);
  for (const line of errors) console.log(`error: ${line}`);
  console.log(errors.length === 0 ? 'Instruction structure: PASS' : `Instruction structure: FAIL (${errors.length} error(s))`);
  process.exit(errors.length === 0 ? 0 : 1);
}
