import yaml
from ..config import settings
from ..storage.db import run_async
from ..storage.registry import load_policies_from_db


def load_policies():
    if settings.aigis_db_enabled:
        try:
            policies = run_async(load_policies_from_db())
            if policies:
                return policies
        except Exception:
            pass
    path = settings.policy_path
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("policies", [])
