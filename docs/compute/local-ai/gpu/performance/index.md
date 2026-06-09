# GPU Performance Tuning


<div class="kb-summary">
Getting the most out of GPU hardware requires profiling to identify bottlenecks, then applying targeted optimisations such as mixed precision, larger batch sizes, and multi-GPU communication tuning.
</div>
```text
┌──────────────────────────────────── Ai Gpu Workloads Performance ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Gpu Workloads: Ai Gpu Workloads Performance platform                     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Ai Gpu Workloads Performance management console                  │   │
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
│    Physical: Ai Gpu Workloads Performance infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Gpu Workloads      = Ai Gpu Workloads Performance platform overview and core concepts              │
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
