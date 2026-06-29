---
tags:
  - troubleshooting
search:
  boost: 1.5
---
# GPU Workload Troubleshooting

<div class="kb-summary">
This page covers the most common GPU workload failures: out-of-memory errors, CUDA runtime errors, driver mismatches, and multi-GPU communication issues.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
outofmemory_oom_errors: "Out-of-Memory (OOM) Errors" {shape: rectangle}
cuda_runtime_errors: "CUDA Runtime Errors" {shape: rectangle}
driver_and_framework_mismatch: "Driver and Framework Mismatch" {shape: rectangle}
multigpu_issues: "Multi-GPU Issues" {shape: rectangle}
gpu_not_detected: "GPU Not Detected" {shape: rectangle}
temperature_and_throttling: "Temperature and Throttling" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> outofmemory_oom_errors: investigate
symptom -> cuda_runtime_errors: investigate
symptom -> driver_and_framework_mismatch: investigate
symptom -> multigpu_issues: investigate
symptom -> gpu_not_detected: investigate
symptom -> temperature_and_throttling: investigate
outofmemory_oom_errors -> resolution
cuda_runtime_errors -> resolution
driver_and_framework_mismatch -> resolution
multigpu_issues -> resolution
gpu_not_detected -> resolution
temperature_and_throttling -> resolution
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


```text title="Expected output"
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.104.05    Driver Version: 535.104.05    CUDA Version: 12.2   |
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| 0  NVIDIA A100-PCIE-40GB  Off  | 00:1E.0     Off |                  0 |
+-----------------------------------------------------------------------------+

nvcc: CUDA compilation tools, release 12.1, V12.1.105
Build cuda_12.1.r12.1/compiler.33079141_0

2.2.0+cu121
2.15.0
WARNING:tensorflow:From <stdin>: is_gpu_available (from tensorflow.python.framework.config) is deprecated and will be removed in a future version.
True
```

!!! warning "Common errors"
    **`command not found: nvidia-smi`** — Install NVIDIA GPU drivers using your system package manager (e.g., `apt install nvidia-driver-535` on Ubuntu).
    **`ModuleNotFoundError: No module named 'torch'`** — Install PyTorch with CUDA support using `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`.
    **`CUDA version mismatch: CUDA driver version 12.1 is insufficient for CUDA toolkit version 12.2`** — Upgrade your NVIDIA driver to version 550+ or downgrade TensorFlow to 2.14 which supports CUDA 12.1.
If versions conflict:

```bash
# Install a specific PyTorch build matching your CUDA version
pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cu121

# Check available builds
pip index versions torch
```


```text title="Expected output"
Collecting torch==2.2.0
  Downloading https://download.pytorch.org/whl/cu121/torch-2.2.0%2Bcu121-cp311-cp311-linux_x86_64.whl (2547.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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


```text title="Expected output"
nvidia              49152  0
nvidia_uvm          36864  0
lspci: command not found
SecureBoot enabled
```

!!! warning "Common errors"
    **`modprobe: FATAL: Module nvidia not found in directory /lib/modules/5.15.0-86-generic/kernel`** — Install the NVIDIA driver package matching your kernel version with `apt install nvidia-driver-XXX` or use `nvidia-driver-installer`.
    **`lspci: command not found`** — Install the `pciutils` package with `apt install pciutils` or `yum install pciutils`.
    **`ERROR: could not insert 'nvidia': Operation not permitted`** — Disable Secure Boot in BIOS/UEFI or enroll the NVIDIA MOK key with `mokutil --import /var/lib/shim-signed/mok/MOK.der`.
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


```text title="Expected output"
clocks_throttle_reasons.active
0x0000000000000020

Every 2.0s: nvidia-smi --query-gpu=temperature.gpu,clocks.sm,power.draw --format=csv,noheader                                                                                                    Mon Dec 18 10:34:52 2023

73, 1410, 245.00 W
74, 1395, 248.50 W
76, 1380, 251.25 W
78, 1365, 254.75 W
79, 1350, 257.00 W
80, 1335, 259.50 W
81, 1320, 261.00 W
```

!!! warning "Common errors"
    **`NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`** — Verify the NVIDIA driver is installed with `nvidia-smi` (without arguments) and reinstall if needed with `sudo apt install nvidia-driver-XXX` (replacing XXX with your driver version).
    **`command not found: watch`** — Install the procps-ng package with `sudo apt install procps-ng` or use `nvidia-smi --loop=2` as an alternative.
If throttling occurs, check airflow, verify TDP power limits are set correctly, and confirm the cooling solution is adequate for sustained workloads.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Drivers](../drivers/)
- [Monitoring](../monitoring/)
- [Performance](../performance/)
- [Sizing](../sizing/)
- [GPU — Overview](../)
