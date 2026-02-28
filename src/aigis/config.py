import os

def _get(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def _get_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y"}


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


class Settings:
    def __init__(self):
        self.aigis_env = _get("AIGIS_ENV", "dev")
        self.database_url = _get("DATABASE_URL", "")
        self.aigis_api_key = _get("AIGIS_API_KEY", "changeme")
        self.policy_path = _get("POLICY_PATH", "config/policies.example.yaml")
        self.aigis_semantic_enabled = _get_bool("AIGIS_SEMANTIC_ENABLED", False)
        self.aigis_embed_model = _get("AIGIS_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.aigis_db_enabled = _get_bool("AIGIS_DB_ENABLED", False)
        self.aigis_llm_enabled = _get_bool("AIGIS_LLM_ENABLED", False)
        self.aigis_llm_endpoint = _get("AIGIS_LLM_ENDPOINT", "http://127.0.0.1:8080/v1/chat/completions")
        self.aigis_llm_timeout = _get_int("AIGIS_LLM_TIMEOUT", 12)
        self.aigis_llm_model = _get("AIGIS_LLM_MODEL", "qwen2.5-3b-instruct")
        self.aigis_telemetry_enabled = _get_bool("AIGIS_TELEMETRY_ENABLED", True)
        self.aigis_telemetry_path = _get("AIGIS_TELEMETRY_PATH", "")


settings = Settings()
