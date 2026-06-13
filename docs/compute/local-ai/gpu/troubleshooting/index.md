---
tags:
  - troubleshooting
---
# GPU Workload Troubleshooting


<div class="kb-summary">
This page covers the most common GPU workload failures: out-of-memory errors, CUDA runtime errors, driver mismatches, and multi-GPU communication issues.
</div>
```text
┌───────────────────────── Ai Gpu Workloads Troubleshooting — Troubleshooting ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Gpu Workloads troubleshooting: structured diagnostic process for common issues        │   │
│   │         Start with health dashboard, then check recent changes, then review event logs        │   │
│   │        Collect support bundle before contacting vendor support to accelerate resolution       │   │
│   │         Escalation matrix: L1 → L2 → vendor support based on severity and SLA targets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check health → review changes → examine logs → diagnose → resolve                                  │
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
│    Physical: Ai Gpu Workloads Troubleshooting infrastructure · management network · monitoring        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Gpu Workloads      = Ai Gpu Workloads Troubleshooting platform overview and core concepts          │
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

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Out-of-Memory (OOM) Errors

OOM is the most frequent GPU failure. It occurs when allocated VRAM exceeds the card's capacity.

```bash
# Check current memory usage
nvidia-smi --query-gpu=memory.used,memory.free,memory.total \
  --format=csv -i 0
```

```python
import torch

# Check PyTorch allocated memory
print(torch.cuda.memory_allocated(0) / 1e9, "GB allocated")
print(torch.cuda.memory_reserved(0) / 1e9, "GB reserved")

# Print full memory snapshot
print(torch.cuda.memory_summary(device=0))

# Clear cache between experiments
torch.cuda.empty_cache()
```

OOM fixes:

| Fix | How |
|---|---|
| Reduce batch size | Halve batch size, use gradient accumulation |
| Use mixed precision | `torch.cuda.amp.autocast()` cuts VRAM ~50% |
| Gradient checkpointing | `model.gradient_checkpointing_enable()` trades compute for memory |
| Offload optimiser to CPU | DeepSpeed ZeRO stage 2/3 |
| Use smaller dtype | Load model in `torch.float16` or `torch.bfloat16` |

## CUDA Runtime Errors

```bash
# Common CUDA errors and what they mean
# CUDA error: device-side assert triggered — usually an index out of bounds
# CUDA error: illegal memory access — pointer arithmetic bug or corrupted tensor
# CUDA error: CUBLAS_STATUS_EXECUTION_FAILED — matrix dimensions mismatch

# Run with CUDA_LAUNCH_BLOCKING to get precise stack traces
CUDA_LAUNCH_BLOCKING=1 python train.py 2>&1 | head -50
```

```python
# Check if CUDA is available and healthy
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))

# Quick sanity check
x = torch.tensor([1.0]).cuda()
print(x + 1)  # Should print tensor([2.], device='cuda:0')
```

## Driver and Framework Mismatch

```bash
# Check all version components
nvidia-smi                  # Driver version + CUDA driver version
nvcc --version              # CUDA toolkit version
python -c "import torch; print(torch.__version__, torch.version.cuda)"
python -c "import tensorflow as tf; print(tf.__version__, tf.test.is_gpu_available())"

# Typical compatibility matrix check
# PyTorch 2.2 requires CUDA 11.8 or 12.1
# TF 2.15 requires CUDA 12.2
```

If versions conflict:

```bash
# Install a specific PyTorch build matching your CUDA version
pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cu121

# Check available builds
pip index versions torch
```

## Multi-GPU Issues

```bash
# Verify all GPUs are visible
nvidia-smi -L

# Check NVLink status
nvidia-smi nvlink --status

# Test NCCL communication (nccl-tests)
git clone https://github.com/NVIDIA/nccl-tests
cd nccl-tests && make
./build/all_reduce_perf -b 8 -e 128M -f 2 -g 4

# Common NCCL errors:
# NCCL error: unhandled system error — network/firewall blocking NCCL ports
# NCCL error: invalid argument — GPU topology mismatch
```

```python
import torch.distributed as dist

# Test basic distributed init
dist.init_process_group(backend="nccl")
print(f"Rank {dist.get_rank()} of {dist.get_world_size()} initialised")
```

## GPU Not Detected

```bash
# Check if kernel module is loaded
lsmod | grep nvidia

# Reload module
modprobe nvidia
modprobe nvidia-uvm

# Check PCIe device is visible
lspci | grep -i nvidia

# Check for Secure Boot blocking unsigned module
mokutil --sb-state  # "SecureBoot enabled" may block NVIDIA modules
# Solution: enroll the NVIDIA MOK key or disable Secure Boot
```

## Temperature and Throttling

```bash
# Check for thermal throttling
nvidia-smi --query-gpu=clocks_throttle_reasons.active \
  --format=csv -i 0

# Key throttle reason codes:
# 0x0000000000000000 — no throttling
# 0x0000000000000008 — GPU idle
# 0x0000000000000020 — SW thermal slowdown (temperature limit)
# 0x0000000000000040 — HW slowdown (temperature or power)

# Monitor temperature in real time
watch -n 2 nvidia-smi --query-gpu=temperature.gpu,clocks.sm,power.draw \
  --format=csv,noheader
```

If throttling occurs, check airflow, verify TDP power limits are set correctly, and confirm the cooling solution is adequate for sustained workloads.
