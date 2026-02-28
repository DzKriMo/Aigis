# Aigis — Agent Guardrail MVP

Aigis is a guarded agent runtime with policy enforcement across user input, tool calls, tool results, and model output.

## Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:PYTHONPATH="src"
uvicorn aigis.api.main:app --reload
```

## Optional ML Detectors (Open Source, Low-Resource)
The hybrid detectors can use a small open-source embedding model for semantic matching. This is optional.

```powershell
pip install -r requirements-ml.txt
$env:AIGIS_SEMANTIC_ENABLED="true"
$env:AIGIS_EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
python scripts/download_semantic_model.py
```

## Endpoints (MVP)
- `POST /v1/sessions` create session
- `POST /v1/sessions/{session_id}/messages` send user message
- `POST /v1/sessions/{session_id}/approvals` approve a pending action
- `POST /v1/sessions/{session_id}/tools/execute` execute tool with guardrails
- `GET /v1/sessions/{session_id}` view session log

## Persistence (Optional)
If `AIGIS_DB_ENABLED=true`, the service will attempt to load policies and tool policies from Postgres.
It falls back to `config/policies.example.yaml` and the in-code tool registry on failure.

### Migrations
```powershell
pip install -r requirements.txt
$env:DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/aigis"
alembic upgrade head
```

## Policies
See `config/policies.example.yaml` for a starter rule set.

## Notes
This is a scaffold only. Replace placeholder detectors with real implementations.
