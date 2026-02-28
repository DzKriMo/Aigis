from __future__ import annotations

from typing import Dict, Any
import json
import httpx

from ..config import settings


SYSTEM_PROMPT = (
    "You are a security classifier for AI guardrails. "
    "Return ONLY valid JSON with keys: "
    "prompt_injection, jailbreak, goal_hijack, exfiltration, data_leakage, "
    "pii, secrets, policy_violation. "
    "Each value must be true or false. No extra text."
)


def _build_user_prompt(text: str) -> str:
    return f"Classify the following content:\\n\\n{text}"


def classify_text(text: str) -> Dict[str, bool]:
    if not settings.aigis_llm_enabled:
        return {}

    payload: Dict[str, Any] = {
        "model": settings.aigis_llm_model,
        "temperature": 0.0,
        "max_tokens": 200,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(text)},
        ],
    }

    try:
        with httpx.Client(timeout=settings.aigis_llm_timeout) as client:
            resp = client.post(settings.aigis_llm_endpoint, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return {k: bool(parsed.get(k, False)) for k in parsed.keys()}
    except Exception:
        return {}
