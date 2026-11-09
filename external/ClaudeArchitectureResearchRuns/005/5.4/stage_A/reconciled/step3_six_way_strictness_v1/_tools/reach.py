"""Mechanical delivery (reach) class of a v3 record, from its delivery_context string.

This is a classification of HOW a line reaches the agent, never of what it requires.
Ranks: lower number = reaches the agent more reliably for an arbitrary task.
"""
import re

RANK = {
    "ROOT_ALWAYS": 0, "IMPORT_ALWAYS": 0, "RULE_ALWAYS": 0,
    "RULE_ANY_FILE": 1, "RULE_PATH": 2,
    "HOOK": 2, "BUILD_TOOL": 2, "SETTINGS": 2,
    "SKILL": 3, "CAPABILITY": 3, "SUBAGENT": 3,
    "SKILL_REF": 4, "CHECKER": 4,
    "HUMAN_MAP": 6, "OTHER": 5,
}
ENFORCING = {"HOOK", "CHECKER", "BUILD_TOOL", "SETTINGS"}


def reach_class(dc):
    d = (dc or "").strip()
    low = d.lower()
    if low.startswith("root claude.md"):
        return "ROOT_ALWAYS"
    if "imported by root claude.md" in low:
        return "IMPORT_ALWAYS"
    if low.startswith("hook file") or low.startswith("hook "):
        return "HOOK"
    if low.startswith("checker/helper"):
        return "CHECKER"
    if low.startswith("build/tool"):
        return "BUILD_TOOL"
    if low.startswith("human instruction map") or "not auto-loaded" in low:
        return "HUMAN_MAP"
    if low.startswith("capability file"):
        return "CAPABILITY"
    if low.startswith("subagent"):
        return "SUBAGENT"
    if low.startswith("rule "):
        if "path-scoped" in low:
            m = re.search(r"paths:(.*)\)", d)
            paths = m.group(1) if m else ""
            if re.fullmatch(r'\s*-\s*"\*\*/\*"\s*', paths or ""):
                return "RULE_ANY_FILE"
            return "RULE_PATH"
        return "RULE_ALWAYS"
    if low.startswith("skill ") and ("private file" in low or "read on demand" in low):
        return "SKILL_REF"
    if low.startswith("skill "):
        return "SKILL"
    if ".claude/skills/" in low and "/references/" in low:
        return "SKILL_REF"
    if ".claude/skills/" in low:
        return "SKILL"
    if low.startswith("claude.md") or low == "claude.md":
        return "ROOT_ALWAYS"
    if ".claude/rules/" in low:
        return "RULE_PATH"
    if low.startswith(".claude/hooks/"):
        return "HOOK"
    if low.startswith(".claude/scripts/") or ".claude/tools/" in low:
        return "CHECKER"
    if low.startswith("claude code project settings"):
        return "SETTINGS"
    return "OTHER"


def rule_paths(dc):
    m = re.search(r"paths:(.*)\)", dc or "")
    if not m:
        return None
    return re.findall(r'"([^"]+)"', m.group(1))
