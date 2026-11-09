// Kind: ENF | Scope: repo/meta | Capability: — | Loading: shared helpers for .claude/scripts and .claude/hooks
'use strict';

const fs = require('fs');
const path = require('path');

const IGNORED_DIRS = new Set(['.git', 'node_modules', 'bin', 'obj', 'dist', '.vs', 'TestResults', 'coverage']);

function toPosix(p) {
  return p.split(path.sep).join('/');
}

/** Repository root: two levels above .claude/scripts or .claude/hooks. */
function rootFrom(dirname, levels) {
  const root = path.resolve(dirname, ...Array(levels).fill('..'));
  if (!fs.existsSync(path.join(root, '.claude'))) {
    throw new Error(`Cannot locate the project root from ${dirname}: expected a .claude directory at ${root}`);
  }
  return root;
}

/** Resolve a path relative to root; returns null when it escapes the root. */
function relInside(root, filePath) {
  const abs = path.resolve(root, filePath);
  const rel = path.relative(root, abs);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

function exists(root, rel) {
  return fs.existsSync(path.join(root, rel));
}

function readText(root, rel) {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

function walk(root, startRel = '', filter = () => true) {
  const out = [];
  const start = path.join(root, startRel);
  if (!fs.existsSync(start)) return out;
  const stack = [start];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!IGNORED_DIRS.has(entry.name)) stack.push(abs);
      } else {
        const rel = toPosix(path.relative(root, abs));
        if (filter(rel)) out.push(rel);
      }
    }
  }
  return out.sort();
}

/** Minimal attribute/element reader for MSBuild files (no external XML dependency). */
function xmlElements(text, tag) {
  const results = [];
  const re = new RegExp(`<${tag}\\b([^>]*?)(/>|>([\\s\\S]*?)</${tag}>)`, 'g');
  let m;
  while ((m = re.exec(text)) !== null) {
    const attrs = {};
    const attrRe = /([A-Za-z_:][\w:.-]*)\s*=\s*"([^"]*)"/g;
    let a;
    while ((a = attrRe.exec(m[1])) !== null) attrs[a[1]] = a[2];
    const body = m[3] || '';
    const child = {};
    const childRe = /<([A-Za-z_][\w.-]*)>([^<]*)<\/\1>/g;
    let c;
    while ((c = childRe.exec(body)) !== null) child[c[1]] = c[2].trim();
    results.push({ attrs, child });
  }
  return results;
}

function stripXmlComments(text) {
  return text.replace(/<!--[\s\S]*?-->/g, '');
}

function finding(severity, file, message, owner) {
  return { severity, file, message, owner };
}

function formatFindings(findings) {
  return findings
    .map(f => `[${f.severity}] ${f.file}: ${f.message}${f.owner ? ` -> ${f.owner}` : ''}`)
    .join('\n');
}

module.exports = {
  toPosix,
  rootFrom,
  relInside,
  exists,
  readText,
  walk,
  xmlElements,
  stripXmlComments,
  finding,
  formatFindings,
};
