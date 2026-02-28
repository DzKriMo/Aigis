from __future__ import annotations

from typing import Dict, Any, Optional, List
import requests


class AigisClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": api_key}

    def create_session(self) -> str:
        r = requests.post(f"{self.base_url}/sessions", headers=self.headers, timeout=10)
        r.raise_for_status()
        return r.json()["session_id"]

    def send_message(self, session_id: str, content: str, **kwargs) -> Dict[str, Any]:
        payload = {"content": content}
        payload.update(kwargs)
        r = requests.post(f"{self.base_url}/sessions/{session_id}/messages", json=payload, headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.json()

    def execute_tool(
        self,
        session_id: str,
        tool_name: str,
        payload: Dict[str, Any],
        environment: Optional[str] = None,
        allowlist: Optional[List[str]] = None,
        denylist: Optional[List[str]] = None,
        filesystem_root: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        body = {
            "tool_name": tool_name,
            "payload": payload,
            "environment": environment,
            "allowlist": allowlist or [],
            "denylist": denylist or [],
            "filesystem_root": filesystem_root,
        }
        body.update(kwargs)
        r = requests.post(f"{self.base_url}/sessions/{session_id}/tools/execute", json=body, headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.json()
