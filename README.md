# Aigis — Agent Guardrail Runtime (Demo-Ready)

![Status](https://img.shields.io/badge/status-demo--ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Aigis is a Python-based agent guardrail runtime that enforces policies across **user input**, **tool calls**, **tool results**, and **model output**. It includes a web dashboard, JWT auth, database-backed event storage, and optional local LLM classification via llama.cpp.

> This repository is a **demo-ready** implementation for coursework and presentations.

---

## Features

- **Pre-LLM firewall**: prompt injection, jailbreak, goal hijack, normalization, network URL firewall
- **Post-LLM firewall**: secrets/PII redaction, exfiltration blocking, approvals
- **Tool guardrails**: allow/deny, environment restrictions, sandboxed execution
- **LLM-based classification** (local): llama.cpp sidecar + Qwen2.5-3B GGUF
- **JWT + API key auth**
- **Database persistence** (SQLite default)
- **Web dashboard** with event timeline and LLM classifications
- **Telemetry hooks** + optional OpenTelemetry

---

## Project Structure

```
Aigis/
  src/aigis/
    api/            # FastAPI endpoints (sessions, auth, dashboard)
    auth/           # API key + JWT, rate limiting
    detectors/      # regex/semantic + LLM classifiers
    runtime/        # policy engine + guarded runtime
    storage/        # DB + in-memory stores
    tools/          # client/wrappers
    telemetry/      # logging + OpenTelemetry
  config/
  scripts/
```

---

## Quickstart (Local, CPU)

```powershell
python.exe -m uvicorn aigis.api.main:app --port 8000
```

Dashboard:
```
http://127.0.0.1:8000/v1/dashboard
```

---

## Enable Local LLM Classification (llama.cpp)

1) Start llama.cpp server (GPU suggested):
```powershell
llama-server.exe \
  -m Aigis\models\qwen2.5-3b-instruct-q4_k_m.gguf \
  --port 8080 --n-gpu-layers 35 --ctx-size 2048
```

2) Start API with LLM enabled:
```powershell
$env:AIGIS_LLM_ENABLED="true"
$env:AIGIS_LLM_ENDPOINT="http://127.0.0.1:8080/v1/chat/completions"
$env:AIGIS_LLM_MODEL="qwen2.5-3b-instruct"
python.exe -m uvicorn aigis.api.main:app --port 8000
```

Check LLM health:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/llm/ping" -Headers @{ "x-api-key"="changeme" } -UseBasicParsing
```

---

## Demo Script

```powershell
python.exe C:\Users\krimo\OneDrive\Desktop\Aigis\scripts\demo_cli.py
```

---

## Auth

- **API Key**: pass `x-api-key: changeme`
- **JWT**: request token and use `Authorization: Bearer <token>`

Token:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/auth/token" -Headers @{ "x-api-key"="changeme" }
```

---

## Config

Edit `.env`:
```
AIGIS_API_KEY=changeme
AIGIS_LLM_ENABLED=true
AIGIS_LLM_ENDPOINT=http://127.0.0.1:8080/v1/chat/completions
AIGIS_LLM_MODEL=qwen2.5-3b-instruct
AIGIS_DB_ENABLED=true
DATABASE_URL=sqlite:///aigis.db
```

---

## Docker

```powershell
docker compose up --build
```

---

## Docs

- `SYSTEM_ARCHITECTURE.md` — full system walkthrough
- `CONTRIBUTING.md` — how to contribute
- `SECURITY.md` — security policy

---

## License

MIT (for coursework / demo use)
