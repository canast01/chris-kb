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
┌──────────────────────────────────────── Compute Local Ai Gpu ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Local Ai: Compute Local Ai Gpu platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Compute Local Ai Gpu management console                      │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Compute Local Ai Gpu infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Local Ai           = Compute Local Ai Gpu platform overview and core concepts                      │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
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

- [GPU — Common Issues](common-issues.md)
- [Ollama — Known Issues](../../ollama/troubleshooting/known-issues/)
