from __future__ import annotations

import json
from typing import List, Dict, Any, Optional

from sqlalchemy import select

from .db import get_session
from .models import PolicyRecord, ToolPolicyRecord


async def load_policies_from_db() -> List[Dict[str, Any]]:
    session = await get_session()
    if session is None:
        return []
    async with session as s:
        rows = (await s.execute(select(PolicyRecord).where(PolicyRecord.enabled == True))).scalars().all()
    policies = []
    for row in rows:
        policies.append({
            "id": row.name,
            "stage": row.stage,
            "action": row.action,
            "match": json.loads(row.match_json),
            "risk": float(row.risk) if row.risk else 0.0,
        })
    return policies


async def load_tool_policies_from_db() -> Dict[str, Dict[str, Any]]:
    session = await get_session()
    if session is None:
        return {}
    async with session as s:
        rows = (await s.execute(select(ToolPolicyRecord))).scalars().all()
    tools: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        tools[row.name] = {
            "allowed_envs": json.loads(row.allowed_envs) if row.allowed_envs else [],
            "allowlist": json.loads(row.allowlist) if row.allowlist else [],
            "timeout_seconds": int(row.timeout_seconds),
            "max_bytes": int(row.max_bytes) if row.max_bytes else None,
        }
    return tools
