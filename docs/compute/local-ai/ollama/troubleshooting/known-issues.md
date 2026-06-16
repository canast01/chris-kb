---
tags:
  - troubleshooting
  - ollama
  - local-ai
  - known-issues
---
# Ollama — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Ollama bugs, error codes, and workarounds covering model loading, GPU offload, and API server issues.

*Applies to: Ollama 0.3.x / 0.4.x*
</div>

```text
┌─────────────────────────────────────────────── Ollama ────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Local LLM runner — model pull/serve, GPU offload, OpenAI-compatible API            │   │
│   │                             Protocols: HTTP (TCP 11434, local API)                            │   │
│   │                           Management: ollama CLI (pull/run/serve/ps)                          │   │
│   │            ollama pull -> Model stored locally -> ollama serve -> API -> Inference            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         Model store         │  │       ~/.ollama/models      │  │       GGUF, quantized       │   │
│   │            Server           │  │         ollama serve        │  │       Listens on 11434      │   │
│   │             API             │  │     REST + OpenAI-compat    │  │   /api/generate, /v1/chat   │   │
│   │         GPU offload         │  │         CUDA layers         │  │    Partial if VRAM short    │   │
│   │          Modelfile          │  │     Custom model config     │  │     num_ctx, sys prompt     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   ollama serve   │ API server proc. │     HTTP 11434    │   None default   │Bind 0.0.0.0 4 rmt│   │
│   │   ollama pull    │  Download model  │       HTTPS       │       N/A        │ From ollama.com  │   │
│   │    ollama ps     │Show loaded models│        N/A        │       N/A        │GPU/CPU mem split │   │
│   │    Modelfile     │Define model parms│        N/A        │       N/A        │num_ctx, template │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: host with optional NVIDIA GPU - local disk for model storage                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GGUF           = quantized model file format used by Ollama/llama.cpp                                │
│  Quant. level   = e.g. Q4_K_M; trades model quality for size/speed                                    │
│  num_ctx        = context window size set via Modelfile or API                                        │
│  OLLAMA_HOST    = env var controlling bind address (default 127.0.0.1)                                │
│  Modelfile      = config defining a custom model (base+params+prompt)                                 │
│  ollama ps      = lists loaded models and their GPU/CPU memory split                                  │
│  Context exceeded = prompt exceeds the model configured num_ctx                                       │
│  GPU layers     = number of model layers offloaded to GPU vs CPU                                      │
│  ollama pull    = downloads a model from the Ollama model registry                                    │
│  API compat.    = Ollama exposes an OpenAI-compatible /v1/chat endpoint                               │
│  Embedding model= specialized model type for vectors, not chat                                        │
│  Model registry = ollama.com hosted catalog of pullable models                                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Ollama logs: `journalctl -u ollama` (systemd) or `ollama serve --verbose` for debug output.
- `ollama ps` shows currently loaded models and GPU/CPU memory allocation.
- GPU support requires CUDA 12.x; verify with `nvidia-smi` before assuming GPU offload.

## Model Loading

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Error: model not found` | Ollama 0.3+ | Model name typo or model not pulled | Run `ollama pull <model>`; list with `ollama list` | N/A |
| Model runs on CPU only despite GPU present | Ollama 0.3+ | CUDA not found by Ollama; missing CUDA libraries | Install CUDA 12.x; verify `ldconfig -p | grep libcuda`; restart Ollama | N/A |
| `Context length exceeded` | Ollama 0.3+ | Prompt exceeds model's configured context window | Use `num_ctx` parameter in Modelfile or via API `options.num_ctx` | N/A |

## API Server

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Ollama API returning `connection refused` on port 11434 | Ollama 0.3+ | Ollama service not running | Start: `ollama serve` or `systemctl start ollama` | N/A |
| `Cannot bind to 0.0.0.0:11434 — port in use` | Ollama 0.3+ | Another process using port 11434 | Kill conflicting process: `lsof -i :11434`; restart Ollama | N/A |
| Remote clients cannot reach Ollama API | Ollama 0.3+ | Ollama bound to 127.0.0.1 only | Set: `OLLAMA_HOST=0.0.0.0` environment variable; restart Ollama | N/A |

## Performance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Very slow inference on GPU | Ollama 0.3+ | Model too large for VRAM; partially offloaded to CPU | Use smaller quantized model (Q4_K_M); check `ollama ps` for GPU layers count | N/A |

## See also

- [Ollama — Common Issues](common-issues.md)
- [GPU — Known Issues](../../gpu/troubleshooting/known-issues/)
