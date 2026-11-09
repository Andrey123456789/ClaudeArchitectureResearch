// Level: 3 Project · Owns: shared helpers for hook entry points · Enforcement asset (not an instruction source)
import { readFileSync } from 'node:fs';
import path from 'node:path';

export function readHookInput() {
  try {
    const raw = readFileSync(0, 'utf8');
    return raw.trim() ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export function projectDir(input) {
  return path.resolve(process.env.CLAUDE_PROJECT_DIR || input?.cwd || process.cwd());
}

export function toRepoPath(root, filePath) {
  if (!filePath) return '';
  const absolute = path.isAbsolute(filePath) ? filePath : path.resolve(root, filePath);
  return path.relative(root, absolute).split(path.sep).join('/');
}

// Exit code 2 sends stderr to Claude: PreToolUse blocks the call, PostToolUse and Stop return feedback.
export function feedback(lines) {
  if (!lines.length) process.exit(0);
  process.stderr.write(`${lines.join('\n')}\n`);
  process.exit(2);
}
