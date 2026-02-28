from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aigis_env: str = "dev"
    database_url: str
    aigis_api_key: str = "changeme"
    policy_path: str = "config/policies.example.yaml"
    aigis_semantic_enabled: bool = False
    aigis_embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    aigis_db_enabled: bool = False

    class Config:
        env_prefix = ""
        env_file = ".env"

settings = Settings()
