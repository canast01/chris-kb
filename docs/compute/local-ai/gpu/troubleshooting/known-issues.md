---
tags:
  - troubleshooting
  - gpu
  - local-ai
  - known-issues
---
# GPU / Local AI Inference — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known GPU and local AI inference bugs, error codes, and workarounds covering CUDA, driver issues, and out-of-memory errors.

*Applies to: NVIDIA GPU (CUDA 12.x), PyTorch 2.x, local inference stacks*
</div>

## Before you begin

- `nvidia-smi` for GPU health and VRAM usage.
- CUDA errors appear in Python stack traces — `torch.cuda.is_available()` confirms CUDA visibility.
- OOM (out of memory) is the most common failure for large model inference.

## CUDA and Driver

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `CUDA error: no kernel image is available` | PyTorch 2.x | PyTorch CUDA version not matching installed CUDA | Install PyTorch matching CUDA version: `pip install torch --index-url https://download.pytorch.org/whl/cu121` | N/A |
| `Failed to initialize NVML: Driver/library version mismatch` | All | NVIDIA driver and CUDA library version mismatch after kernel update | Reboot; if persistent: reinstall NVIDIA driver matching CUDA | N/A |
| GPU not visible after reboot | Linux | NVIDIA kernel module not loaded | Run: `modprobe nvidia`; check `dmesg | grep nvidia` for errors | N/A |

## Out of Memory

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `RuntimeError: CUDA out of memory` | All | Model too large for GPU VRAM | Use quantized model (4-bit/8-bit); reduce batch size; use CPU offload | N/A |
| VRAM not freed after model unload | PyTorch 2.x | Python reference still held; CUDA caching allocator retaining memory | Run `torch.cuda.empty_cache()`; delete model object; run GC | N/A |

## See also

- [GPU — Common Issues](common-issues.md)
- [Ollama — Known Issues](../../ollama/troubleshooting/known-issues/)
