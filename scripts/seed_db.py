import json
import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aigis.storage.models import Base, PolicyRecord, ToolPolicyRecord
from aigis.runtime.tool_registry import _TOOLS


def main():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL not set")

    engine = create_engine(url.replace("+asyncpg", ""), echo=False)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    with open("config/policies.example.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    policies = data.get("policies", [])

    session = Session()

    # Seed policies
    for p in policies:
        record = PolicyRecord(
            name=p.get("id", "unnamed"),
            stage=p.get("stage", ""),
            action=p.get("action", ""),
            match_json=json.dumps(p.get("match", {})),
            risk=str(p.get("risk", "")) if p.get("risk") is not None else None,
            enabled=True,
        )
        session.add(record)

    # Seed tool policies from in-code registry
    for name, t in _TOOLS.items():
        record = ToolPolicyRecord(
            name=name,
            allowed_envs=json.dumps(t.allowed_envs),
            allowlist=json.dumps(t.allowlist),
            timeout_seconds=t.timeout_seconds,
            max_bytes=t.max_bytes,
        )
        session.add(record)

    session.commit()
    session.close()
    print("Seed complete.")


if __name__ == "__main__":
    main()
