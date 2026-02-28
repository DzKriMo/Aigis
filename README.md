# Aigis — Agent Guardrail MVP

Aigis is a guarded agent runtime with policy enforcement across user input, tool calls, tool results, and model output.

## Quickstart (Local)

```powershell
$env:PYTHONPATH="C:\Users\krimo\OneDrive\Desktop\Aigis\src"
C:\Users\krimo\AppData\Local\Python\pythoncore-3.14-64\python.exe -m uvicorn aigis.api.main:app --port 8000
```

## Docker (Production-like)
```powershell
docker compose up --build
```

## Health
```powershell
http://127.0.0.1:8000/v1/health
```

## Endpoints (MVP)
- `POST /v1/sessions` create session
- `GET /v1/sessions` list sessions
- `POST /v1/sessions/{session_id}/messages` send user message
- `POST /v1/sessions/{session_id}/approvals` approve a pending action
- `POST /v1/sessions/{session_id}/tools/execute` execute tool with guardrails
- `GET /v1/sessions/{session_id}` view session log
- `GET /v1/policies` list active policies
- `PUT /v1/policies` replace policies (YAML-backed)
- `GET /v1/dashboard` web UI
- `GET /v1/tool-policies` list tool policies
- `PUT /v1/tool-policies` replace tool policies (DB-only)

## Dashboard Access
Open in browser:
```
http://127.0.0.1:8000/v1/dashboard
```
Enter the API key in the UI and click **Save Key**.

## Demo CLI
```powershell
python scripts/demo_cli.py
```

## One-Click Demo
```powershell
scripts\start_demo.ps1 -ServerExe "C:\path\to\server.exe" -ModelPath "models\qwen2.5-3b-instruct-q4_k_m.gguf"
```
