# Example script to start llama.cpp server (Windows)
# Requires llama.cpp built with CUDA. Adjust paths.
# Example:
# .\server.exe -m models\phi-3.5-mini-instruct.Q4_K_M.gguf --port 8080 --n-gpu-layers 28 --ctx-size 2048

param(
    [string]$ServerExe = "server.exe",
    [string]$ModelPath = "models\\phi-3.5-mini-instruct.Q4_K_M.gguf",
    [int]$Port = 8080,
    [int]$GpuLayers = 28,
    [int]$CtxSize = 2048
)

& $ServerExe -m $ModelPath --port $Port --n-gpu-layers $GpuLayers --ctx-size $CtxSize
