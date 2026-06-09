# Local AI & GPU Workloads

<div class="kb-summary">
On-premises AI/ML compute — GPU hardware management, driver configuration, and running large language models locally with Ollama. Covers sizing, performance, and operational procedures for GPU-accelerated infrastructure.
</div>

```text
┌────────────────────────────────────── Local AI & GPU Workloads ───────────────────────────────────────┐
│                                                                                                       │
│   On-premises AI/ML compute: GPU hardware management and local large language model serving           │
│   Ollama: self-hosted LLM inference engine; runs models locally with GPU acceleration                 │
│   GPU management: driver configuration, CUDA toolkit, performance tuning, and sizing                  │
│                                                                                                       │
│   Sections in this guide                                                                              │
│   Ollama (Local LLMs): model management, GPU offloading, CLI reference, API integration               │
│   GPU Workloads: instance types, driver install, CUDA toolkit, performance tuning, monitoring         │
│                                                                                                       │
│   Ollama                                                                                              │
│   Serves LLMs via REST API on port 11434; compatible with OpenAI API format                           │
│   GPU offloading via CUDA (NVIDIA) or ROCm (AMD); falls back to CPU if no GPU detected                │
│   Model management: ollama pull / run / list / rm; models stored in ~/.ollama/models                  │
│                                                                                                       │
│   GPU workloads                                                                                       │
│   Driver stack: NVIDIA driver → CUDA toolkit → cuDNN → AI framework (PyTorch / TensorFlow)            │
│   nvidia-smi: GPU utilisation, VRAM usage, temperature, and per-process breakdown                     │
│   Sizing: VRAM is the primary constraint for LLM inference; 7B model requires 4–8 GB VRAM             │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Ollama       = local LLM serving tool; REST API and CLI; supports GGUF model format                 │
│   CUDA         = NVIDIA parallel computing platform; required for GPU-accelerated inference           │
│   nvidia-smi   = NVIDIA system management interface; primary GPU health and utilisation tool          │
│   VRAM         = video RAM on GPU; primary resource constraint for LLM inference workloads            │
│   ROCm         = AMD GPU compute platform; open-source alternative to CUDA for AMD GPUs               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-2">

<a class="kb-card" href="ollama/">
  <strong>Ollama (Local LLMs)</strong>
  <span>Run LLMs locally on-prem using Ollama — model management, GPU acceleration, CLI reference, and API integration.</span>
</a>

<a class="kb-card" href="gpu/">
  <strong>GPU Workloads</strong>
  <span>GPU instance types, driver management, CUDA toolkits, performance tuning, and workload scheduling for AI/ML.</span>
</a>

</div>
