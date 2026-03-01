import hashlib
import json
from typing import Dict, Any


def approval_hash(stage: str, content: str, context: Dict[str, Any]) -> str:
    payload = {
        "stage": stage,
        "content": content,
        "tenant_id": context.get("tenant_id"),
        "role": context.get("role"),
        "environment": context.get("environment"),
        "labels": context.get("labels") or [],
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
