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

```text
┌────────────────────────────────────── GPU / Local AI Inference ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              NVIDIA GPU inference stack — CUDA, drivers, PyTorch, VRAM management             │   │
│   │                   Protocols: N/A — local compute, not network protocol-bound                  │   │
│   │                Management: nvidia-smi / nvidia-ml-py / vendor driver installer                │   │
│   │            Driver load -> CUDA runtime -> Framework (PyTorch) -> Model -> Inference           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Driver           │  │     NVIDIA kernel module    │  │     Must match CUDA ver.    │   │
│   │           Runtime           │  │         CUDA toolkit        │  │     Pinned to framework     │   │
│   │          Framework          │  │      PyTorch/TensorFlow     │  │       Links CUDA libs       │   │
│   │            Memory           │  │             VRAM            │  │      Hard limit per GPU     │   │
│   │         Quantization        │  │      4-bit/8-bit models     │  │       Reduces VRAM use      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    nvidia-smi    │  GPU/VRAM view   │        N/A        │    root/sudo     │ First diag. step │   │
│   │   CUDA toolkit   │ GPU compute API  │        N/A        │       N/A        │Must match driver │   │
│   │     PyTorch      │   ML framework   │        N/A        │       N/A        │ torch.cuda check │   │
│   │       NVML       │GPU monitoring lib│        N/A        │       N/A        │ Backs nvidia-smi │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: server/workstation with discrete NVIDIA GPU(s) - PCIe - cooling                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CUDA           = NVIDIA parallel compute platform/API for GPU acceleration                           │
│  VRAM           = GPU dedicated memory; model size must fit within it                                 │
│  NVML           = NVIDIA Management Library; underlies nvidia-smi                                     │
│  Quantization   = reducing weight precision (4/8-bit) to save VRAM                                    │
│  CUDA OOM       = out-of-memory error when model/batch exceeds VRAM                                   │
│  Caching alloc. = PyTorch VRAM reuse layer; can retain freed memory                                   │
│  Driver mismatch= NVIDIA driver version incompatible with CUDA libs                                   │
│  Kernel module  = nvidia.ko; in-kernel driver loaded via modprobe                                     │
│  CPU offload    = running part of a model on CPU when VRAM is short                                   │
│  Batch size     = inputs processed together; larger uses more VRAM                                    │
│  empty_cache()  = releases cached but unused VRAM back to the OS                                      │
│  Mixed precision= fp16/bf16 to reduce memory and raise throughput                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

- [Ollama — Known Issues](../../ollama/troubleshooting/known-issues.md)
