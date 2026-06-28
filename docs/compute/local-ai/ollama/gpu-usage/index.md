---
tags:
  - ollama
  - ai
  - local-ai
---
# Ollama GPU Acceleration

<div class="kb-summary">
Ollama automatically uses the GPU when drivers and CUDA/ROCm are installed. This page covers confirming GPU usage, configuring which GPU(s) to use, VRAM requirements per model, and ROCm support.

*Applies to: Ollama*
</div>

```d2
direction: down

confirming_gpu_usage: "Confirming GPU Usage" {shape: rectangle}
cuda_setup: "CUDA Setup" {shape: rectangle}
rocm_amd_gpu_setup: "ROCm (AMD GPU) Setup" {shape: rectangle}
vram_requirements_by_model_size: "VRAM Requirements by Model Size" {shape: rectangle}
controlling_gpu_layer_count: "Controlling GPU Layer Count" {shape: rectangle}
multigpu_configuration: "Multi-GPU Configuration" {shape: rectangle}

confirming_gpu_usage -> cuda_setup: uses
cuda_setup -> rocm_amd_gpu_setup: uses
rocm_amd_gpu_setup -> vram_requirements_by_model_size: uses
vram_requirements_by_model_size -> controlling_gpu_layer_count: uses
controlling_gpu_layer_count -> multigpu_configuration: uses
```

## Confirming GPU Usage

```bash
# When running a model, check if GPU layers are loaded
ollama run llama3.1:8b "Hello"

# In a separate terminal, watch GPU utilisation
watch -n 1 nvidia-smi

# Or query Ollama's running model info
curl http://localhost:11434/api/show \
  -d '{"name":"llama3.1:8b"}' | jq '.details'

# Check Ollama logs for GPU detection
journalctl -u ollama -n 50
# Look for: "detected GPU" or "loaded model ... on GPU"
```

Ollama outputs the number of GPU layers loaded at model start. If `num_gpu: 0` appears, Ollama is running on CPU only.

## CUDA Setup

Ollama bundles its own CUDA libraries and only requires the NVIDIA driver — the CUDA toolkit does not need to be installed separately.

```bash
# Verify driver is present
nvidia-smi

# Check Ollama detects the GPU
OLLAMA_DEBUG=1 ollama run llama3.1:8b "test" 2>&1 | grep -i gpu

# Set specific GPU(s) (CUDA device index)
CUDA_VISIBLE_DEVICES=0 ollama serve   # Use GPU 0 only
CUDA_VISIBLE_DEVICES=0,1 ollama serve # Use GPUs 0 and 1
```

## ROCm (AMD GPU) Setup

```bash
# Install ROCm 6.x (Ubuntu 22.04)
wget https://repo.radeon.com/amdgpu-install/6.1.2/ubuntu/jammy/amdgpu-install_6.1.60102-1_all.deb
dpkg -i amdgpu-install_6.1.60102-1_all.deb
apt-get update
amdgpu-install --usecase=rocm

# Add user to render and video groups
usermod -aG render,video $USER

# Verify ROCm
rocm-smi
rocminfo | grep gfx

# Ollama uses ROCm automatically when detected
HSA_OVERRIDE_GFX_VERSION=11.0.0 ollama serve  # Override for unsupported gfx version
```

## VRAM Requirements by Model Size

| Model | Quantisation | VRAM Required | Minimum GPU |
|---|---|---|---|
| llama3.1:8b | Q4_K_M (default) | ~5 GB | RTX 3060 12GB |
| llama3.1:8b | F16 | ~16 GB | RTX 3080 / A10G |
| llama3.1:70b | Q4_K_M | ~40 GB | A100 40GB |
| llama3.1:70b | Q8_0 | ~74 GB | A100 80GB |
| mistral:7b | Q4_K_M | ~4.5 GB | RTX 3060 |
| llava:13b (vision) | Q4_K_M | ~8 GB | RTX 3080 |
| codestral:22b | Q4_K_M | ~13 GB | RTX 3090 |

## Controlling GPU Layer Count

Ollama automatically calculates how many layers fit in VRAM. Override with `OLLAMA_NUM_GPU`:

```bash
# Force specific number of layers to GPU (0 = CPU only, 99 = all layers)
OLLAMA_NUM_GPU=32 ollama run llama3.1:8b

# Or in Modelfile
FROM llama3.1:8b
PARAMETER num_gpu 32
```

## Multi-GPU Configuration

```bash
# Ollama distributes layers across multiple GPUs automatically
# Check layer distribution in debug output
OLLAMA_DEBUG=1 ollama run llama3.1:70b 2>&1 | grep "layer"

# Restrict to specific GPUs
CUDA_VISIBLE_DEVICES=0,1,2,3 ollama serve

# Monitor all GPUs during inference
nvidia-smi dmon -s u -d 2
```

## Flash Attention

Enable flash attention for lower VRAM usage and faster inference on supported models:

```bash
OLLAMA_FLASH_ATTENTION=1 ollama serve
```

Flash attention reduces the KV cache memory footprint significantly, allowing longer context windows with less VRAM.
