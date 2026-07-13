---
tags:
  - gpu
  - ai
  - local-ai
description: "Getting the most out of GPU hardware requires profiling to identify bottlenecks, then applying targeted optimisations such as mixed precision, larger..."
---
# GPU Performance Tuning

<div class="kb-summary">
Getting the most out of GPU hardware requires profiling to identify bottlenecks, then applying targeted optimisations such as mixed precision, larger batch sizes, and multi-GPU communication tuning.
</div>

```d2
direction: down

profiling_with_nsight_and_pytorch_pr: "Profiling with Nsight and PyTorch Profiler" {shape: rectangle}
mixed_precision_training: "Mixed Precision Training" {shape: rectangle}
batch_size_and_throughput: "Batch Size and Throughput" {shape: rectangle}
nccl_and_multigpu_communication: "NCCL and Multi-GPU Communication" {shape: rectangle}
performance_benchmarking: "Performance Benchmarking" {shape: rectangle}
common_bottlenecks: "Common Bottlenecks" {shape: rectangle}

profiling_with_nsight_and_pytorch_pr -> mixed_precision_training: uses
mixed_precision_training -> batch_size_and_throughput: uses
batch_size_and_throughput -> nccl_and_multigpu_communication: uses
nccl_and_multigpu_communication -> performance_benchmarking: uses
performance_benchmarking -> common_bottlenecks: uses
```

## Profiling with Nsight and PyTorch Profiler

Start by measuring before optimising. Guessing at bottlenecks wastes time.

```python
import torch
from torch.profiler import profile, record_function, ProfilerActivity

model = MyModel().cuda()
inputs = torch.randn(32, 3, 224, 224).cuda()

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    profile_memory=True,
    with_stack=True
) as prof:
    with record_function("forward_pass"):
        outputs = model(inputs)

# Print top operations by CUDA time
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=20))

# Export for TensorBoard
prof.export_chrome_trace("/tmp/trace.json")
```

For kernel-level profiling, use Nsight Systems:

```bash
nsys profile --trace=cuda,nvtx,osrt \
  --output /tmp/profile_output \
  python train.py --epochs 1 --steps 100
```


```text title="Expected output"
Collecting CUDA/NVTX/OSRT trace data...
Processing events...
Generating CUDA API Summary...
  Total GPU time: 2847.3 ms
  Total CPU time: 3124.5 ms
  GPU Utilization: 91.2%
  Memory Bandwidth: 487.6 GB/s
Generating NVTX Summary...
  Total NVTX ranges: 1247
  Deepest nesting level: 8
Generating OS Runtime Summary...
  Total context switches: 342
  Total page faults: 18
Report generated: /tmp/profile_output.nsys-rep
SQLite database: /tmp/profile_output.sqlite
Elapsed time: 45.2 seconds
```

!!! warning "Common errors"
    **`Error: NVIDIA Nsight Systems is not installed or not in PATH`** — Install nsys via `apt install nvidia-nsight-systems` or add its installation directory to your PATH.
    **`Error: CUDA capability not found. Make sure CUDA is installed and accessible`** — Verify CUDA installation with `nvidia-smi` and ensure `CUDA_HOME` environment variable is set correctly.
    **`Error: Permission denied writing to /tmp/profile_output`** — Run the command with appropriate permissions or specify an output directory where the user has write access.
## Mixed Precision Training

AMP (Automatic Mixed Precision) reduces memory usage by ~50% and accelerates throughput on Tensor Cores by using FP16 for most operations while keeping FP32 for numerically sensitive parts.

```python
import torch
from torch.cuda.amp import GradScaler, autocast

model    = MyModel().cuda()
optimiser = torch.optim.AdamW(model.parameters(), lr=1e-4)
scaler   = GradScaler()

for batch in dataloader:
    inputs, labels = batch[0].cuda(), batch[1].cuda()
    optimiser.zero_grad()

    with autocast():
        outputs = model(inputs)
        loss    = criterion(outputs, labels)

    scaler.scale(loss).backward()
    scaler.step(optimiser)
    scaler.update()
```

## Batch Size and Throughput

Larger batch sizes improve GPU utilisation but increase memory pressure. Find the largest batch size that fits in VRAM:

```python
def find_max_batch_size(model, input_shape, start=8, max_bs=2048):
    bs = start
    while bs <= max_bs:
        try:
            x = torch.randn(bs, *input_shape).cuda()
            _ = model(x)
            torch.cuda.empty_cache()
            print(f"Batch size {bs}: OK")
            bs *= 2
        except RuntimeError as e:
            if "out of memory" in str(e):
                print(f"Batch size {bs}: OOM — use {bs // 2}")
                torch.cuda.empty_cache()
                return bs // 2
            raise
    return bs
```

## NCCL and Multi-GPU Communication

For distributed training, NCCL handles GPU-to-GPU communication. Tuning NCCL can significantly improve multi-GPU scaling efficiency.

```bash
# Enable NCCL debug logging
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=ALL

# Force NVLink (preferred over PCIe)
export NCCL_P2P_LEVEL=NVL

# For InfiniBand / RDMA clusters
export NCCL_IB_DISABLE=0
export NCCL_IB_HCA=mlx5_0

# Launch distributed training (4 GPUs on 1 node)
torchrun --nproc_per_node=4 train.py --distributed
```


```text title="Expected output"
Setting up process group with backend: nccl
[W] NCCL operation timed out after 30s
[I] rank 0: initialized cuda device 0
[I] rank 1: initialized cuda device 1
[I] rank 2: initialized cuda device 2
[I] rank 3: initialized cuda device 3
[I] NCCL version 2.18.3
[I] Ring: 0 1 2 3
[I] Tree: 0->1, 0->2, 0->3
[I] P2P: NVLink enabled for ranks 0-1, 0-2, 0-3
[I] IB: mlx5_0 detected, RDMA enabled
Epoch 1/100 | Loss: 2.341 | GPU0: 89% | GPU1: 87% | GPU2: 91% | GPU3: 88%
Epoch 2/100 | Loss: 1.892 | GPU0: 92% | GPU1: 90% | GPU2: 93% | GPU3: 91%
Saving checkpoint: model_epoch_2.pt
```

!!! warning "Common errors"
    **`NCCL operation timed out after 30s`** — Increase timeout with `export NCCL_SOCKET_TIMEOUT=600` and verify all GPUs are accessible via `nvidia-smi`.
    **`RuntimeError: CUDA out of memory`** — Reduce batch size in train.py or enable gradient checkpointing with `--gradient_checkpointing` flag.
    **`FileNotFoundError: [Errno 2] No such file or directory: 'train.py'`** — Ensure train.py exists in the current working directory and is executable.
## Performance Benchmarking

| Metric | Command | Target |
|---|---|---|
| Memory bandwidth | `bandwidthTest` (CUDA samples) | >900 GB/s (A100 SXM) |
| Compute throughput | `deviceQuery` | Check vs spec sheet |
| Model throughput | Samples/sec logged during training | Increase with AMP + larger batch |
| NVLink bandwidth | `nvidia-smi nvlink --status` | 600 GB/s (A100 NVLink 3.0) |

## Common Bottlenecks

| Bottleneck | Symptom | Fix |
|---|---|---|
| CPU data loading | GPU at <50% util, CPU at 100% | Increase DataLoader workers, use pin_memory |
| Small batch size | Low FLOP/s efficiency | Gradient accumulation to simulate larger batch |
| FP32 where FP16 works | Slow throughput on Tensor Core hardware | Enable AMP |
| PCIe bottleneck | High PCIe tx/rx, NVLink idle | Use NVLink topology, reduce host-device copies |
| Memory copies | High cudaMemcpy in profiler | Pre-allocate tensors, use async transfers |
