import os
import yaml
from ..config import settings
from ..storage.registry import load_policies_from_db


def _resolve_path(path: str) -> str:
    if os.path.isabs(path):
        return path
    # project root = .../Aigis
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    return os.path.join(base, path)


def load_policies():
    if settings.aigis_db_enabled:
        try:
            policies = load_policies_from_db()
            if policies:
                return policies
        except Exception:
            pass
    path = _resolve_path(settings.policy_path)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("policies", [])


def save_policies(policies):
    path = _resolve_path(settings.policy_path)
    payload = {"policies": policies}
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(payload, f, sort_keys=False)
