param(
    [string]$ProjectRoot = "$PSScriptRoot\..",
    [string]$VenvPath = "$PSScriptRoot\..\.venv",
    [string]$ServerExe = "$PSScriptRoot\..\llama.cpp\llama-server.exe",
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

if (-not (Test-Path $ServerExe)) {
    throw "llama-server.exe not found at '$ServerExe'."
}

# Start llama.cpp server in a new window
if (Test-Path $ModelPath) {
    $llamaCmd = "& `"$ServerExe`" -m `"$ModelPath`" --port $LlmPort --n-gpu-layers 35 --ctx-size 2048"
} else {
    $llamaCmd = "& `"$ServerExe`" --hf-repo `"$HfRepo`" --hf-file `"$HfFile`" --port $LlmPort --n-gpu-layers 35 --ctx-size 2048"
}

Start-Process powershell -WorkingDirectory $ProjectRoot -ArgumentList @(
    "-NoExit",
    "-Command",
    $llamaCmd
)

# Start Aegis API (includes dashboard endpoint) in a new window
Start-Process powershell -WorkingDirectory $ProjectRoot -ArgumentList @(
    "-NoExit",
    "-Command",
    "`$env:PYTHONPATH='src'; `$env:AEGIS_LLM_ENABLED='true'; `$env:AEGIS_LLM_ENDPOINT='http://127.0.0.1:$LlmPort/v1/chat/completions'; `$env:AEGIS_LLM_MODEL='qwen2.5-3b-instruct'; & `"$PythonExe`" -m uvicorn aegis.api.main:app --port $ApiPort --reload"
)

Write-Host "Started LLM server: http://127.0.0.1:$LlmPort" -ForegroundColor Green
Write-Host "Dashboard URL: http://127.0.0.1:$ApiPort/v1/dashboard" -ForegroundColor Green
