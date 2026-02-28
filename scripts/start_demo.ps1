param(
    [string]$ProjectRoot = "$PSScriptRoot\..",
    [string]$VenvPath = "$PSScriptRoot\..\.venv",
    [string]$ServerExe = "server.exe",
    [string]$ModelPath = "$PSScriptRoot\..\models\qwen2.5-3b-instruct-q4_k_m.gguf",
    [string]$HfRepo = "JackeyLai/Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
    [string]$HfFile = "qwen2.5-3b-instruct-q4_k_m.gguf",
    [string]$PythonExe = "C:\Users\krimo\AppData\Local\Python\pythoncore-3.14-64\python.exe",
    [int]$ApiPort = 8000,
    [int]$LlmPort = 8080
)

$ErrorActionPreference = "Stop"

Set-Location $ProjectRoot

# Activate venv if present
$activate = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $activate) {
  . $activate
} else {
  Write-Host "Venv not found. Using PythonExe directly." -ForegroundColor Yellow
}

if (-not (Test-Path $PythonExe)) {
  $PythonExe = "python"
}

# Start llama.cpp server in new window
if (Test-Path $ModelPath) {
  $llamaCmd = "& `"$ServerExe`" -m `"$ModelPath`" --port $LlmPort --n-gpu-layers 35 --ctx-size 2048"
} else {
  $llamaCmd = "& `"$ServerExe`" --hf-repo `"$HfRepo`" --hf-file `"$HfFile`" --port $LlmPort --n-gpu-layers 35 --ctx-size 2048"
}

Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-Command",
  $llamaCmd
)

# Start Aigis API in new window
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-Command",
  "`$env:PYTHONPATH='src'; `$env:AIGIS_LLM_ENABLED='true'; `$env:AIGIS_LLM_ENDPOINT='http://127.0.0.1:$LlmPort/v1/chat/completions'; `$env:AIGIS_LLM_MODEL='qwen2.5-3b-instruct'; & `"$PythonExe`" -m uvicorn aigis.api.main:app --port $ApiPort --reload"
)

# Wait for API to be ready
$apiUrl = "http://127.0.0.1:$ApiPort/v1/sessions"
$ready = $false
for ($i = 0; $i -lt 60; $i++) {
  try {
    $resp = Invoke-WebRequest -Method Options -Uri $apiUrl -TimeoutSec 2
    $ready = $true
    break
  } catch {
    Start-Sleep -Seconds 1
  }
}

if (-not $ready) {
  Write-Host "API not ready yet. You can run: $PythonExe scripts/demo_cli.py" -ForegroundColor Yellow
  exit 1
}

# Run demo
& $PythonExe scripts/demo_cli.py

Write-Host "Dashboard: http://127.0.0.1:$ApiPort/v1/dashboard (x-api-key header required)" -ForegroundColor Green
