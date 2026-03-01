from __future__ import annotations

from typing import Dict, Any, Optional, List

from .client import AegisClient


class GuardedTools:
    def __init__(self, client: AegisClient, session_id: str):
        self.client = client
        self.session_id = session_id

    def shell(self, command: str, environment: Optional[str] = "dev") -> Dict[str, Any]:
        return self.client.execute_tool(
            self.session_id,
            tool_name="shell",
            payload={"command": command},
            environment=environment,
        )

    def filesystem_read(self, path: str, root: Optional[str] = None) -> Dict[str, Any]:
        return self.client.execute_tool(
            self.session_id,
            tool_name="filesystem_read",
            payload={"path": path},
            filesystem_root=root,
        )

    def http_fetch(self, url: str, environment: Optional[str] = "dev") -> Dict[str, Any]:
        return self.client.execute_tool(
            self.session_id,
            tool_name="http_fetch",
            payload={"url": url, "method": "GET"},
            environment=environment,
        )
