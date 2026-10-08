#!/usr/bin/env python3
"""E0 hook logger.

Configured by the harness as a Claude Code command hook for every observed
event. It appends the raw hook payload (stdin JSON) plus a harness-side UTC
timestamp to the JSONL file given as argv[1].

It must stay silent: stdout of SessionStart / UserPromptSubmit hooks is added
to Claude's context, so printing anything would contaminate the probe.
"""
import datetime
import json
import sys

MAX_STR = 20000


def _trim(value):
    if isinstance(value, str) and len(value) > MAX_STR:
        return value[:MAX_STR] + f"...<truncated {len(value) - MAX_STR} chars>"
    if isinstance(value, dict):
        return {k: _trim(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_trim(v) for v in value]
    return value


def main() -> int:
    log_path = sys.argv[1]
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    try:
        payload = json.loads(raw)
    except ValueError:
        payload = {"_unparsed": raw[:MAX_STR]}
    record = {
        "logged_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event": payload.get("hook_event_name") if isinstance(payload, dict) else None,
        "payload": _trim(payload),
    }
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # never block or alter the session because of logging
        sys.exit(0)
