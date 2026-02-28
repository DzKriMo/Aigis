# Tool execution guardrails (prellm/postllm integration point)
# NOTE: This is a conservative, default-deny helper. Integrate with your tool router.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import os
import re

DANGEROUS_COMMANDS = {
    "rm",
    "del",
    "rmdir",
    "format",
    "diskpart",
}

@dataclass
class ToolDecision:
    allowed: bool
    message: str | None = None


def _is_outside_root(path: str, root: str) -> bool:
    try:
        abs_path = os.path.abspath(path)
        abs_root = os.path.abspath(root)
        return not abs_path.startswith(abs_root)
    except Exception:
        return True


def guard_tool_call(
    tool_name: str,
    environment: Optional[str],
    allowlist: Optional[List[str]] = None,
    denylist: Optional[List[str]] = None,
) -> ToolDecision:
    allowlist = allowlist or []
    denylist = denylist or []

    if tool_name in denylist:
        return ToolDecision(False, "Tool denylisted")
    if allowlist and tool_name not in allowlist:
        return ToolDecision(False, "Tool not allowlisted")

    if environment == "prod" and tool_name in {"shell", "filesystem"}:
        return ToolDecision(False, "Destructive tools blocked in prod")

    return ToolDecision(True)


def guard_shell_command(command: str) -> ToolDecision:
    lower = command.strip().lower()
    if any(re.search(r"\b" + re.escape(cmd) + r"\b", lower) for cmd in DANGEROUS_COMMANDS):
        return ToolDecision(False, "Dangerous command blocked")
    return ToolDecision(True)


def guard_filesystem_path(path: str, root: str) -> ToolDecision:
    if _is_outside_root(path, root):
        return ToolDecision(False, "Filesystem access outside root blocked")
    return ToolDecision(True)
