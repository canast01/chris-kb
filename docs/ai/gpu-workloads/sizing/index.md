# GPU Sizing for AI Workloads


<div class="kb-summary">
Selecting the right GPU — and the right number of them — depends on model size, task type (training vs inference), throughput requirements, and budget. This page provides a practical sizing framework.
</div>

## Training vs Inference Requirements

| Aspect | Training | Inference |
|---|---|---|
| VRAM per model | Full weights + gradients + optimiser states (~16-20× param bytes in FP32) | Weights only (~2× param bytes in FP16/INT8) |
| Compute intensity | Very high, sustained | Lower, bursty |
| Latency tolerance | High (batch jobs) | Low (real-time) |
| Multi-GPU benefit | High (data/model parallelism) | Moderate (batching) |
| Preferred GPUs | A100, H100, H200 | A10G, L4, L40S, T4 |

## VRAM Sizing Guide

Rule of thumb for parameter count to VRAM:

| Model Params | FP32 Training VRAM | FP16 Training VRAM | FP16 Inference VRAM |
|---|---|---|---|
| 7B | ~112 GB | ~56 GB | ~14 GB |
| 13B | ~208 GB | ~104 GB | ~26 GB |
| 30B | ~480 GB | ~240 GB | ~60 GB |
| 70B | ~1120 GB | ~560 GB | ~140 GB |

Actual VRAM usage is always higher due to activations, KV cache (inference), and framework overhead. Add 20–30% buffer.

## GPU Specifications Reference

| GPU | VRAM | FP16 TFLOPS | Memory BW | NVLink | Use Case |
|---|---|---|---|---|---|
| NVIDIA T4 | 16 GB | 65 | 300 GB/s | No | Low-cost inference |
| NVIDIA A10G | 24 GB | 125 | 600 GB/s | No | Inference, fine-tuning |
| NVIDIA L4 | 24 GB | 121 | 300 GB/s | No | Inference, cost-optimised |
| NVIDIA L40S | 48 GB | 362 | 864 GB/s | No | Large model inference |
| NVIDIA A100 40GB | 40 GB | 312 | 1555 GB/s | Yes | Training |
| NVIDIA A100 80GB | 80 GB | 312 | 2000 GB/s | Yes | Large model training |
| NVIDIA H100 SXM | 80 GB | 989 | 3350 GB/s | Yes | Large scale training |
| NVIDIA H200 | 141 GB | 989 | 4800 GB/s | Yes | Very large models |

## Estimating Tokens Per Second

For LLM inference, throughput depends on memory bandwidth (memory-bound at low batch sizes) and compute (compute-bound at high batch sizes).

```python
# Rough tokens/sec estimate for memory-bound inference
def estimate_tokens_per_sec(model_params_b, gpu_mem_bw_tb_per_s, precision_bytes=2):
    # Bytes per parameter
    bytes_per_param = precision_bytes
    # Total model bytes
    model_size_gb = model_params_b * 1e9 * bytes_per_param / 1e9
    # Memory bandwidth in GB/s
    bw_gb_s = gpu_mem_bw_tb_per_s * 1000
    # Approximate tokens/sec (each token requires reading all weights once)
    return bw_gb_s / model_size_gb

# Example: 7B model in FP16 on A100 80GB (2000 GB/s)
tps = estimate_tokens_per_sec(7, 2.0, 2)
print(f"~{tps:.0f} tokens/sec")  # ~285 tokens/sec per GPU at batch=1
```

## Cloud Instance Selection

| Provider | Instance | GPUs | VRAM | Best For |
|---|---|---|---|---|
| AWS | p3.2xlarge | 1x V100 16GB | 16 GB | Dev, small models |
| AWS | p4d.24xlarge | 8x A100 40GB | 320 GB | Training |
| AWS | p5.48xlarge | 8x H100 80GB | 640 GB | LLM training |
| AWS | g5.xlarge | 1x A10G | 24 GB | Inference |
| GCP | a2-highgpu-8g | 8x A100 40GB | 320 GB | Training |
| Azure | Standard_NC96ads_A100_v4 | 4x A100 80GB | 320 GB | Training/inference |

## Multi-GPU Strategies

```bash
# Check GPU topology before choosing parallelism strategy
nvidia-smi topo -m
# NV# = NVLink hops, PHB = PCIe host bridge, SYS = cross-socket

# Tensor parallelism splits a single layer across GPUs (requires NVLink)
# Use for models that don't fit on a single GPU

# Pipeline parallelism splits layers across GPUs (works over PCIe)
# Use when NVLink is unavailable

# Data parallelism replicates model across GPUs, splits batch
# Use when model fits on one GPU and you need higher throughput
```
