import os
from dotenv import load_dotenv

load_dotenv()


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


def _get_list(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name)
    if raw is None:
        return default
    items = [item.strip() for item in raw.split(",")]
    return [item for item in items if item]


class Settings:
    def __init__(self):
        self.aegis_env = _get("AEGIS_ENV", "dev")
        self.database_url = _get("DATABASE_URL", "sqlite:///aegis.db")
        self.aegis_api_key = _get("AEGIS_API_KEY", "changeme")
        self.aegis_fail_closed = _get_bool("AEGIS_FAIL_CLOSED", False)
        self.policy_path = _get("POLICY_PATH", "config/policies.example.yaml")
        self.aegis_semantic_enabled = _get_bool("AEGIS_SEMANTIC_ENABLED", False)
        self.aegis_embed_model = _get("AEGIS_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.aegis_db_enabled = _get_bool("AEGIS_DB_ENABLED", True)
        self.aegis_llm_enabled = _get_bool("AEGIS_LLM_ENABLED", False)
        self.aegis_llm_endpoint = _get("AEGIS_LLM_ENDPOINT", "http://127.0.0.1:8080/v1/chat/completions")
        self.aegis_llm_timeout = _get_int("AEGIS_LLM_TIMEOUT", 12)
        self.aegis_llm_model = _get("AEGIS_LLM_MODEL", "qwen2.5-3b-instruct")
        self.aegis_telemetry_enabled = _get_bool("AEGIS_TELEMETRY_ENABLED", True)
        self.aegis_telemetry_path = _get("AEGIS_TELEMETRY_PATH", "")
        self.jwt_secret = _get("AEGIS_JWT_SECRET", "dev-secret-change")
        self.jwt_issuer = _get("AEGIS_JWT_ISSUER", "aegis")
        self.jwt_exp_minutes = _get_int("AEGIS_JWT_EXP_MINUTES", 120)
        self.otel_enabled = _get_bool("AEGIS_OTEL_ENABLED", False)
        self.aegis_cors_origins = _get_list("AEGIS_CORS_ORIGINS", ["*"])
        self.aegis_rate_limit_backend = _get("AEGIS_RATE_LIMIT_BACKEND", "memory")
        self.aegis_rate_limit_limit = _get_int("AEGIS_RATE_LIMIT_LIMIT", 60)
        self.aegis_rate_limit_window_seconds = _get_int("AEGIS_RATE_LIMIT_WINDOW_SECONDS", 60)
        self.aegis_rate_limit_sqlite_path = _get("AEGIS_RATE_LIMIT_SQLITE_PATH", "aegis_rate_limit.db")


settings = Settings()
