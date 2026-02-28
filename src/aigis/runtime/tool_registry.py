from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from ..config import settings
from ..storage.db import run_async
from ..storage.registry import load_tool_policies_from_db


@dataclass
class ToolPolicy:
    name: str
    allowed_envs: List[str]
    allowlist: List[str]
    timeout_seconds: int
    max_bytes: Optional[int] = None


_TOOLS: Dict[str, ToolPolicy] = {
    "shell": ToolPolicy(
        name="shell",
        allowed_envs=["dev"],
        allowlist=["python", "pip", "dir", "ls", "echo"],
        timeout_seconds=5,
    ),
    "filesystem_read": ToolPolicy(
        name="filesystem_read",
        allowed_envs=["dev", "prod"],
        allowlist=[],
        timeout_seconds=2,
        max_bytes=64 * 1024,
    ),
    "http_fetch": ToolPolicy(
        name="http_fetch",
        allowed_envs=["dev"],
        allowlist=[],
        timeout_seconds=5,
        max_bytes=64 * 1024,
    ),
    "json_transform": ToolPolicy(
        name="json_transform",
        allowed_envs=["dev", "prod"],
        allowlist=[],
        timeout_seconds=1,
    ),
}


def get_tool_policy(name: str) -> Optional[ToolPolicy]:
    if settings.aigis_db_enabled:
        try:
            db_tools = run_async(load_tool_policies_from_db())
            if name in db_tools:
                t = db_tools[name]
                return ToolPolicy(
                    name=name,
                    allowed_envs=t.get("allowed_envs", []),
                    allowlist=t.get("allowlist", []),
                    timeout_seconds=int(t.get("timeout_seconds", 5)),
                    max_bytes=t.get("max_bytes"),
                )
        except Exception:
            pass
    return _TOOLS.get(name)
