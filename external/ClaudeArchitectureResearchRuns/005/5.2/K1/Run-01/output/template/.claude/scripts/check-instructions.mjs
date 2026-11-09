// Kind: ENF | Scope: repo/meta | Capability: — | Loading: run by template-maintenance or manually: node .claude/scripts/check-instructions.mjs [--root <dir>] | Validates the Kind × Scope × Capability structure of the instruction system
import path from 'node:path';
import { existsSync, readdirSync, statSync } from 'node:fs';
import { EnforcementError, rootFromArgs, listFiles, readText, isMainModule } from './lib/common.mjs';

const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN'];
const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta'];
const RULE_SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];
const SLOTS = { architecture: 'required', persistence: 'required', 'backend-testing': 'required', frontend: 'optional' };
const LEAF_BINDS = { persistence: 'architecture', 'backend-testing': 'architecture' };
const REQUIRED_WORKFLOWS = [
  'development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance',
];
const REQUIRED_NON_SLOT_KNOWLEDGE = [
  'http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration', 'dependency-injection',
  'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication',
];
const REGISTER = 'docs/architecture/decision-register.md';
const MAP = '.claude/MAP.md';
const HEADER = /^Kind: (\w+) \| Scope: ([\w/-]+) \| Capability: (\S+)(?: \([^)]*\))? \| Loading: \S.*$/;
const CODE_HEADER = /^(?:\/\/|#|<!--) Kind: (\w+) \| Scope: ([\w/-]+) \| Capability: (\S+) \| Loading: \S.*$/;
const TEXT_EXTENSIONS = ['.md', '.mjs', '.json', '.cs', '.props', '.editorconfig'];

function splitFrontmatter(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) {
    return { frontmatter: null, body: normalized };
  }
  const end = normalized.indexOf('\n---\n', 4);
  if (end === -1) {
    return { frontmatter: null, body: normalized, broken: true };
  }
  return { frontmatter: normalized.slice(4, end), body: normalized.slice(end + 5) };
}

function frontmatterValue(frontmatter, key) {
  const match = frontmatter?.match(new RegExp(`^${key}:\\s*(.*)$`, 'm'));
  return match ? match[1].trim() : undefined;
}

function frontmatterList(frontmatter, key) {
  const match = frontmatter?.match(new RegExp(`^${key}:\\s*\\n((?:\\s+-\\s+.*\\n?)+)`, 'm'));
  return match ? match[1].split('\n').map((l) => l.replace(/^\s+-\s+/, '').replace(/^"|"$/g, '').trim()).filter(Boolean) : [];
}

function firstLine(body) {
  return body.split('\n').find((line) => line.trim() !== '') ?? '';
}

function headings(text) {
  return [...text.matchAll(/^#{1,6}\s+(.+)$/gm)].map((m) => normalizeHeading(m[1]));
}

function normalizeHeading(text) {
  return text.replace(/`/g, '').replace(/\s+/g, ' ').trim().toLowerCase();
}

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function lineOf(text, index) {
  return text.slice(0, index).split('\n').length;
}

class Checker {
  constructor(root) {
    this.root = root;
    this.defects = [];
    this.info = [];
    this.files = listFiles(root, '.', () => true);
    this.headers = new Map();
  }

  defect(message) {
    this.defects.push(message);
  }

  text(file) {
    return readText(this.root, file).replace(/\r\n/g, '\n');
  }

  isTextFile(file) {
    return TEXT_EXTENSIONS.some((e) => file.endsWith(e)) || file.endsWith('.editorconfig');
  }

  instructionMarkdown() {
    return this.files.filter((f) => f.endsWith('.md') && (
      f === 'CLAUDE.md' || f === 'CUSTOM_SETTINGS.md' || f === REGISTER || f.startsWith('.claude/')));
  }

  checkHeaders() {
    for (const file of this.instructionMarkdown()) {
      const { frontmatter, body, broken } = splitFrontmatter(this.text(file));
      if (broken) {
        this.defect(`${file}: unterminated YAML frontmatter.`);
        continue;
      }
      const line = firstLine(body);
      if (file === MAP) {
        if (!/^Map: .+\| Loading: not loaded/.test(line)) {
          this.defect(`${file}: missing the map header line.`);
        }
        continue;
      }
      const match = line.match(HEADER);
      if (!match) {
        this.defect(`${file}: first line after frontmatter is not a "Kind: | Scope: | Capability: | Loading:" header.`);
        continue;
      }
      for (const fmLine of (frontmatter ?? '').split('\n')) {
        const scalar = fmLine.match(/^[\w-]+:\s+(.+)$/);
        if (scalar && !/^["'>|]/.test(scalar[1]) && (/: |\s#/.test(scalar[1]) || /^[[{&*!%@`]/.test(scalar[1]))) {
          this.defect(`${file}: frontmatter value "${fmLine.slice(0, 60)}..." is not a valid plain YAML scalar (quote it or remove ": " / " #").`);
        }
      }
      const [, kind, scope, capability] = match;
      if (!KINDS.includes(kind)) {
        this.defect(`${file}: unknown Kind "${kind}".`);
      }
      if (!SCOPES.includes(scope)) {
        this.defect(`${file}: unknown Scope "${scope}".`);
      }
      this.headers.set(file, { kind, scope, capability, frontmatter });
    }

    for (const file of this.files) {
      const inClaude = file.startsWith('.claude/');
      if ((inClaude && (file.endsWith('.mjs') || file.endsWith('.cs')))
        || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(file)) {
        const match = firstLine(this.text(file)).match(CODE_HEADER);
        if (!match) {
          this.defect(`${file}: first line is not an ENF classification header comment.`);
        } else {
          this.headers.set(file, { kind: match[1], scope: match[2], capability: match[3] });
        }
      } else if (inClaude && file.endsWith('.json') && file !== '.claude/settings.json') {
        let json;
        try {
          json = JSON.parse(this.text(file));
        } catch (error) {
          this.defect(`${file}: invalid JSON (${error.message}).`);
          continue;
        }
        const match = (json._header ?? '').match(new RegExp(CODE_HEADER.source.replace('^(?:\\/\\/|#|<!--) ', '^')));
        if (!match) {
          this.defect(`${file}: missing "_header" classification field.`);
        } else {
          this.headers.set(file, { kind: match[1], scope: match[2], capability: match[3] });
        }
      }
    }

    for (const file of this.files.filter((f) => this.isTextFile(f))) {
      if (/^Level:/m.test(this.text(file))) {
        this.defect(`${file}: "Level:" headers are not part of this instruction system.`);
      }
    }
  }

  checkLocations() {
    for (const [file, header] of this.headers) {
      const parts = file.split('/');
      const expect = (kinds, why) => {
        if (!kinds.includes(header.kind)) {
          this.defect(`${file}: Kind ${header.kind} does not fit its location (${why}).`);
        }
      };
      if (file === 'CLAUDE.md') expect(['OP'], 'operating policy');
      else if (file === REGISTER) expect(['DEC'], 'decision register');
      else if (file === 'CUSTOM_SETTINGS.md') expect(['IN'], 'product input');
      else if (file.startsWith('.claude/rules/')) {
        expect(['STD'], 'path-scoped standard');
        if (parts.length !== 4 || !RULE_SCOPES.includes(parts[2])) {
          this.defect(`${file}: rules must live in .claude/rules/<scope>/ with scope in ${RULE_SCOPES.join(', ')}.`);
        } else if (header.scope !== parts[2]) {
          this.defect(`${file}: header Scope "${header.scope}" differs from its scope directory "${parts[2]}".`);
        }
        if (frontmatterList(header.frontmatter, 'paths').length === 0) {
          this.defect(`${file}: rule files must declare non-empty "paths:" frontmatter.`);
        }
      } else if (file.startsWith('.claude/skills/')) {
        expect(['WF', 'KNW'], 'skill');
      } else if (file.startsWith('.claude/agents/')) {
        expect(['WF'], 'thin agent delegating to a workflow');
      } else if (file.startsWith('.claude/capabilities/')) {
        if (parts.length === 4 && parts[3] === 'CONTRACT.md') expect(['DEC'], 'slot contract');
        else if (parts[4] === 'MODULE.md') expect(['DEC'], 'module manifest');
        else if (parts[4] === 'workflow-facet.md') expect(['WF'], 'workflow facet');
        else this.defect(`${file}: unexpected file in .claude/capabilities/.`);
      } else if (file.startsWith('.claude/hooks/') || file.startsWith('.claude/scripts/')
        || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(file)) {
        expect(['ENF'], 'enforcement');
      }
    }
  }

  checkSkillsAndAgents() {
    const skillDirs = existsSync(path.join(this.root, '.claude/skills'))
      ? readdirSync(path.join(this.root, '.claude/skills')).filter((d) => statSync(path.join(this.root, '.claude/skills', d)).isDirectory())
      : [];
    this.skills = new Map();
    for (const dir of skillDirs) {
      const file = `.claude/skills/${dir}/SKILL.md`;
      const header = this.headers.get(file);
      if (!header) {
        this.defect(`.claude/skills/${dir}: missing SKILL.md with a header.`);
        continue;
      }
      const name = frontmatterValue(header.frontmatter, 'name');
      const description = frontmatterValue(header.frontmatter, 'description') ?? '';
      if (name !== dir) {
        this.defect(`${file}: frontmatter name "${name}" must equal the directory name "${dir}".`);
      }
      if (description.length < 20 || description.length > 1024) {
        this.defect(`${file}: description must be a concrete trigger description (20-1024 characters).`);
      }
      const userOnly = frontmatterValue(header.frontmatter, 'disable-model-invocation') === 'true';
      this.skills.set(dir, { file, kind: header.kind, description, userOnly, capability: header.capability });
    }
    for (const workflow of REQUIRED_WORKFLOWS) {
      if (this.skills.get(workflow)?.kind !== 'WF') {
        this.defect(`Required workflow skill "${workflow}" is missing or not Kind WF.`);
      }
    }
    for (const knowledge of REQUIRED_NON_SLOT_KNOWLEDGE) {
      const skill = this.skills.get(knowledge);
      if (skill?.kind !== 'KNW' || skill.capability !== '—') {
        this.defect(`Required non-slot knowledge skill "${knowledge}" is missing, not Kind KNW, or not Capability —.`);
      }
    }
    if (!this.skills.get('template-maintenance')?.userOnly) {
      this.defect('template-maintenance must set "disable-model-invocation: true" (user-only).');
    }
    for (const [name, skill] of this.skills) {
      if (name !== 'template-maintenance' && skill.userOnly) {
        this.defect(`${skill.file}: only template-maintenance is user-only.`);
      }
    }

    const agent = this.headers.get('.claude/agents/code-reviewer.md');
    if (!agent) {
      this.defect('Agent .claude/agents/code-reviewer.md is missing.');
    } else {
      const preloads = (frontmatterValue(agent.frontmatter, 'skills') ?? '').split(/[,\s]+/);
      const disallowed = (frontmatterValue(agent.frontmatter, 'disallowedTools') ?? '').split(/[,\s]+/);
      if (!preloads.includes('code-review')) {
        this.defect('code-reviewer agent must preload the code-review workflow (skills: code-review).');
      }
      if (!disallowed.includes('Write') || !disallowed.includes('Edit')) {
        this.defect('code-reviewer agent must disallow Write and Edit (read-only).');
      }
    }

    // Skill-private references are used only by their own skill.
    for (const file of this.files.filter((f) => /^\.claude\/skills\/[^/]+\/references\//.test(f))) {
      const owner = file.split('/')[2];
      const name = file.split('/').slice(3).join('/');
      for (const other of this.files.filter((f) => this.isTextFile(f) && f !== MAP && !f.startsWith(`.claude/skills/${owner}/`))) {
        const text = this.text(other);
        if (text.includes(`skills/${owner}/${name}`) || (text.includes(name) && text.includes(`\`${owner}\``) && new RegExp(`${escapeRegExp(owner)}[^\\n]*${escapeRegExp(name)}`).test(text))) {
          this.defect(`${other}: depends on ${file}, a private reference of "${owner}".`);
        }
      }
    }
  }

  parseRegisterSelection() {
    const text = this.text(REGISTER);
    const start = text.indexOf('## Capability selection');
    if (start === -1) {
      this.defect(`${REGISTER}: missing "## Capability selection" section.`);
      return { section: '', rows: new Map() };
    }
    const nextSection = text.indexOf('\n## ', start + 5);
    const section = text.slice(start, nextSection === -1 ? undefined : nextSection);
    const rows = new Map();
    for (const line of section.split('\n')) {
      const cells = line.split('|').map((c) => c.trim());
      if (cells.length >= 7 && Object.hasOwn(SLOTS, cells[1])) {
        rows.set(cells[1], {
          selected: cells[3].split(/\s+/)[0],
          knowledge: cells[4].replace(/`/g, ''),
          module: cells[5].replace(/`/g, ''),
        });
      }
    }
    this.registerSelection = section;
    return { section, rows };
  }

  parseModule(file) {
    const text = this.text(file);
    const field = (key) => text.match(new RegExp(`^- ${key}:\\s*(.*)$`, 'm'))?.[1].trim();
    const facets = [];
    for (const line of text.split('\n')) {
      const cells = line.split('|').map((c) => c.trim());
      if (cells.length >= 5 && KINDS.includes(cells[1])) {
        const pathMatch = cells[2].match(/`([^`]+)`/);
        facets.push({ kind: cells[1], path: pathMatch ? pathMatch[1] : '', scope: cells[3] });
      }
    }
    return {
      slot: field('slot')?.split(/\s+/)[0],
      implementation: field('implementation'),
      aliases: (field('aliases') ?? '').split(',').map((a) => a.trim()).filter(Boolean),
      binds: field('binds') ?? '',
      facets,
    };
  }

  checkCapabilities() {
    const base = '.claude/capabilities';
    const slotDirs = existsSync(path.join(this.root, base))
      ? readdirSync(path.join(this.root, base)).filter((d) => statSync(path.join(this.root, base, d)).isDirectory())
      : [];
    const expected = Object.keys(SLOTS);
    for (const dir of slotDirs) {
      if (!expected.includes(dir)) {
        this.defect(`${base}/${dir}: only the slots ${expected.join(', ')} exist.`);
      }
    }
    const { rows } = this.parseRegisterSelection();
    this.modules = [];
    for (const [slot, need] of Object.entries(SLOTS)) {
      const slotPath = path.join(this.root, base, slot);
      if (!existsSync(slotPath)) {
        this.defect(`${base}/${slot}: slot directory is missing.`);
        continue;
      }
      if (!existsSync(path.join(slotPath, 'CONTRACT.md'))) {
        this.defect(`${base}/${slot}/CONTRACT.md is missing.`);
      }
      const implementations = readdirSync(slotPath).filter((d) => statSync(path.join(slotPath, d)).isDirectory());
      const row = rows.get(slot);
      if (!row) {
        this.defect(`${REGISTER}: no Capability selection row for slot "${slot}".`);
        continue;
      }
      if (need === 'required' && implementations.length !== 1) {
        this.defect(`${base}/${slot}: a required slot has exactly one implementation (found ${implementations.length}).`);
      }
      if (need === 'optional' && implementations.length > 1) {
        this.defect(`${base}/${slot}: an optional slot has at most one implementation (found ${implementations.length}).`);
      }
      if (row.selected === 'none') {
        if (implementations.length > 0) {
          this.defect(`${base}/${slot}: register selects none, but an implementation is present.`);
        }
        continue;
      }
      if (!implementations.includes(row.selected)) {
        this.defect(`${base}/${slot}: register selects "${row.selected}", which is not present.`);
        continue;
      }
      const moduleDir = `${base}/${slot}/${row.selected}/`;
      if (row.module !== moduleDir) {
        this.defect(`${REGISTER}: module path for ${slot} should be ${moduleDir}.`);
      }
      const manifestFile = `${moduleDir}MODULE.md`;
      if (!existsSync(path.join(this.root, manifestFile))) {
        this.defect(`${manifestFile} is missing.`);
        continue;
      }
      const manifest = this.parseModule(manifestFile);
      const capability = `${slot}/${row.selected}`;
      if (manifest.slot !== slot || manifest.implementation !== row.selected) {
        this.defect(`${manifestFile}: slot/implementation fields do not match ${capability}.`);
      }
      if (manifest.aliases.length === 0) {
        this.defect(`${manifestFile}: declare the implementation's aliases for the leak check.`);
      }
      if (LEAF_BINDS[slot] && !manifest.binds.includes(LEAF_BINDS[slot])) {
        this.defect(`${manifestFile}: must declare binds: ${LEAF_BINDS[slot]}.`);
      }
      const facetKinds = new Set();
      const listed = new Set([manifestFile]);
      for (const facet of manifest.facets) {
        facetKinds.add(facet.kind);
        if (facet.path === REGISTER) {
          if (!new RegExp(`^Capability: ${escapeRegExp(capability)} \\| Kind: DEC$`, 'm').test(this.registerSelection)) {
            this.defect(`${REGISTER}: missing "Capability: ${capability} | Kind: DEC" marker for the DEC facet.`);
          }
          continue;
        }
        listed.add(facet.path);
        if (!existsSync(path.join(this.root, facet.path))) {
          this.defect(`${manifestFile}: facet ${facet.path} does not exist.`);
          continue;
        }
        const header = this.headers.get(facet.path);
        if (!header) {
          this.defect(`${facet.path}: facet has no classification header.`);
        } else {
          if (header.capability !== capability) {
            this.defect(`${facet.path}: header Capability "${header.capability}" should be "${capability}".`);
          }
          if (header.kind !== facet.kind) {
            this.defect(`${facet.path}: header Kind ${header.kind} differs from the manifest (${facet.kind}).`);
          }
        }
        if (facet.kind === 'KNW') {
          const skillName = facet.path.split('/')[2];
          if (row.knowledge !== skillName) {
            this.defect(`${REGISTER}: knowledge facet for ${slot} should be "${skillName}".`);
          }
        } else {
          const base = path.posix.basename(facet.path).toLowerCase();
          if (!facet.path.startsWith(moduleDir) && manifest.aliases.some((a) => base.includes(a.toLowerCase()))) {
            this.defect(`${facet.path}: facet file names are role-based, not implementation-named.`);
          }
        }
      }
      for (const kind of ['DEC', 'STD', 'WF', 'ENF']) {
        if (!facetKinds.has(kind)) {
          this.defect(`${manifestFile}: no ${kind} facet listed.`);
        }
      }
      for (const [file, header] of this.headers) {
        if (header.capability === capability && !listed.has(file)) {
          this.defect(`${file}: declares Capability ${capability} but is not listed in ${manifestFile}.`);
        }
      }
      this.modules.push({ capability, moduleDir, manifestFile, aliases: manifest.aliases, listed });
    }
    for (const [file, header] of this.headers) {
      const known = header.capability === '—' || (file.endsWith('CONTRACT.md') && Object.hasOwn(SLOTS, header.capability))
        || this.modules.some((m) => m.capability === header.capability);
      if (!known) {
        this.defect(`${file}: Capability "${header.capability}" is not a selected module.`);
      }
    }
  }

  checkLeaks() {
    for (const module of this.modules) {
      const patterns = module.aliases.map((a) => new RegExp(`(?<![A-Za-z0-9])${escapeRegExp(a)}(?![A-Za-z0-9])`, 'i'));
      for (const file of this.files.filter((f) => this.isTextFile(f))) {
        if (module.listed.has(file) || file.startsWith(module.moduleDir) || file === MAP) {
          continue;
        }
        let text = this.text(file);
        if (file === REGISTER) {
          text = text.replace(this.registerSelection, '');
        }
        for (const pattern of patterns) {
          const match = pattern.exec(text);
          if (match) {
            this.defect(`${file}:${lineOf(text, match.index)}: names "${match[0]}" of ${module.capability} outside its module (use the slot or facet role).`);
            break;
          }
        }
      }
    }
  }

  resolveReference(fromFile, token) {
    if (token.startsWith('.claude/') || token.startsWith('docs/')
      || ['CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', 'Directory.Build.props', 'Directory.Packages.props', '.editorconfig'].includes(token)) {
      return existsSync(path.join(this.root, token.replace(/\/$/, ''))) ? token.replace(/\/$/, '') : null;
    }
    const local = path.posix.join(path.posix.dirname(fromFile), token);
    if (existsSync(path.join(this.root, local))) {
      return local;
    }
    if (!token.includes('/')) {
      const rules = this.files.filter((f) => f.startsWith('.claude/rules/') && path.posix.basename(f) === token);
      if (rules.length === 1) {
        return rules[0];
      }
      // Role-based facet file names (for example workflow-facet.md) resolve when such a file exists.
      if (rules.length === 0) {
        return this.files.find((f) => path.posix.basename(f) === token) ?? null;
      }
    }
    return null;
  }

  checkReferences() {
    const claude = this.text('CLAUDE.md');
    for (const match of claude.matchAll(/^@(\S+)$/gm)) {
      if (!existsSync(path.join(this.root, match[1]))) {
        this.defect(`CLAUDE.md: import @${match[1]} does not resolve.`);
      }
    }

    const skillNames = new Set([...this.skills.keys(), 'code-reviewer']);
    const pointerTargets = {
      'CLAUDE.md': 'CLAUDE.md',
      'decision register': REGISTER,
    };
    for (const [slot, value] of Object.entries(SLOTS)) {
      const module = this.modules.find((m) => m.capability.startsWith(`${slot}/`));
      if (module && value) {
        pointerTargets[`the ${slot} workflow facet`] = `${module.moduleDir}workflow-facet.md`;
        pointerTargets[`${slot} workflow facet`] = `${module.moduleDir}workflow-facet.md`;
      }
    }

    for (const file of this.files.filter((f) => this.isTextFile(f) && (this.headers.has(f) || f === MAP || f === '.claude/settings.json'))) {
      const text = this.text(file);

      for (const match of text.matchAll(/`([^`\n]+)`/g)) {
        const token = match[1].trim();
        const isPathLike = /^(\.claude\/|docs\/architecture\/)/.test(token)
          || /^(CLAUDE|MAP)\.md$/.test(token)
          || /^references\/[\w.-]+\.md$/.test(token)
          || /^[a-z][a-z-]*\.md$/.test(token);
        if (isPathLike && !/[<>*{}]/.test(token) && !this.resolveReference(file, token)) {
          this.defect(`${file}:${lineOf(text, match.index)}: reference \`${token}\` does not resolve.`);
        }
      }

      for (const match of text.matchAll(/(?:\b[Rr]un (?:the )?|\b[Ff]ollow )`([a-z][a-z0-9-]+)`|`([a-z][a-z0-9-]+)`(?= (?:workflow|skill|knowledge skill|agent)\b)/g)) {
        const name = match[1] ?? match[2];
        if (!skillNames.has(name)) {
          this.defect(`${file}:${lineOf(text, match.index)}: \`${name}\` is not an existing skill or agent.`);
        }
      }

      const pointer = /(?:`([^`\n]+)`|(CLAUDE\.md|decision register|the (?:architecture|persistence|backend-testing|frontend) workflow facet|(?:architecture|persistence|backend-testing|frontend) workflow facet)) → ((?:\d+\. )?[^.;,)\n"|]+?)(?=[.;,)\n"|]| \(| and |$)/gm;
      for (const match of text.matchAll(pointer)) {
        const subject = (match[1] ?? match[2]).trim();
        let target = pointerTargets[subject];
        if (!target && match[1]) {
          if (skillNames.has(subject) && this.skills.has(subject)) {
            target = this.skills.get(subject).file;
          } else {
            target = this.resolveReference(file, subject);
          }
        }
        if (!target || !existsSync(path.join(this.root, target)) || !target.endsWith('.md')) {
          continue;
        }
        const wanted = match[3].split(' / ').map((h) => normalizeHeading(h));
        const available = headings(this.text(target));
        const unnumbered = (h) => h.replace(/^\d+\. /, '');
        for (const heading of wanted) {
          const step = heading.match(/^step (\d+)$/);
          // A pointer may name a heading exactly, by prefix, or continue in prose after the heading text.
          const ok = available.some((h) => [h, unnumbered(h)].some((candidate) => candidate.startsWith(heading)
            || heading.startsWith(`${candidate} `))
            || (step && h.startsWith(`${step[1]}.`)));
          if (!ok) {
            this.defect(`${file}:${lineOf(text, match.index)}: section "${heading}" not found in ${target}.`);
          }
        }
      }
    }
  }

  checkSettings() {
    const file = '.claude/settings.json';
    let settings;
    try {
      settings = JSON.parse(this.text(file));
    } catch (error) {
      this.defect(`${file}: invalid JSON (${error.message}).`);
      return;
    }
    const commands = Object.values(settings.hooks ?? {}).flat().flatMap((entry) => entry.hooks ?? []).map((h) => h.command);
    if (commands.length === 0) {
      this.defect(`${file}: no hooks configured.`);
    }
    for (const command of commands) {
      // Shell-neutral: a plain node invocation with no shell variable expansion or command substitution.
      const direct = /^node (\.claude\/[\w./-]+\.mjs)(?: [\w./-]+)*$/.exec(command ?? '');
      const bootstrap = /^node -e "[^"]*'\.claude','hooks','([\w.-]+\.mjs)'[^"]*"$/.exec(command ?? '');
      const script = direct ? direct[1] : bootstrap ? `.claude/hooks/${bootstrap[1]}` : null;
      if (!script || /[$%`]/.test(command)) {
        this.defect(`${file}: hook command "${command}" must be a shell-neutral node invocation without variable expansion.`);
      } else if (!existsSync(path.join(this.root, script))) {
        this.defect(`${file}: hook script ${script} does not exist.`);
      }
    }
  }

  budget() {
    let characters = this.text('CLAUDE.md').length + this.text(REGISTER).length;
    for (const skill of this.skills.values()) {
      if (!skill.userOnly) {
        characters += skill.description.length + 40;
      }
    }
    const agent = this.headers.get('.claude/agents/code-reviewer.md');
    characters += (frontmatterValue(agent?.frontmatter, 'description') ?? '').length;
    const tokens = Math.round(characters / 4);
    this.info.push(`Always-loaded surface estimate: ~${tokens} tokens (CLAUDE.md, decision register, skill and agent descriptions).`);
    if (tokens > 6000) {
      this.info.push('Warning: the always-loaded surface exceeds ~6000 tokens; keep CLAUDE.md and the register compact.');
    }
  }

  run() {
    this.checkHeaders();
    this.checkLocations();
    this.checkSkillsAndAgents();
    this.checkCapabilities();
    this.checkLeaks();
    this.checkReferences();
    this.checkSettings();
    this.budget();
    return { defects: this.defects, info: this.info };
  }
}

export function checkInstructions(root) {
  return new Checker(root).run();
}

function main() {
  try {
    const root = rootFromArgs(process.argv.slice(2));
    const { defects, info } = checkInstructions(root);
    for (const line of info) {
      console.log(line);
    }
    if (defects.length > 0) {
      console.log(`Instruction-structure defects (${defects.length}):`);
      for (const defect of defects) {
        console.log(`- ${defect}`);
      }
      process.exit(1);
    }
    console.log('Instruction structure: PASS');
  } catch (error) {
    console.error(`Instruction-structure check could not run: ${error instanceof EnforcementError ? error.message : error.stack}`);
    process.exit(3);
  }
}

if (isMainModule(import.meta.url)) {
  main();
}
