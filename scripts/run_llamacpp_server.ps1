# Start local llama.cpp server from this repository.

param(
    [string]$ProjectRoot = "$PSScriptRoot\..",
    [string]$ServerExe = "$PSScriptRoot\..\llama.cpp\llama-server.exe",
    [string]$ModelPath = "$PSScriptRoot\..\models\qwen2.5-3b-instruct-q4_k_m.gguf",
    [string]$HfRepo = "JackeyLai/Qwen2.5-3B-Instruct-Q4_K_M-GGUF",
    [string]$HfFile = "qwen2.5-3b-instruct-q4_k_m.gguf",
    [int]$Port = 8080,
    [int]$GpuLayers = 35,
    [int]$CtxSize = 2048
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

if (-not (Test-Path $ServerExe)) {
    throw "llama-server.exe not found at '$ServerExe'. Place llama.cpp binaries under Aegis\\llama.cpp."
}

if (Test-Path $ModelPath) {
    & $ServerExe -m $ModelPath --port $Port --n-gpu-layers $GpuLayers --ctx-size $CtxSize
} else {
    & $ServerExe --hf-repo $HfRepo --hf-file $HfFile --port $Port --n-gpu-layers $GpuLayers --ctx-size $CtxSize
}
