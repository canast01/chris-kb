---
tags:
  - ollama
  - ai
  - local-ai
---
# Ollama Models


<div class="kb-summary">
Ollama's model library includes a wide range of open models. Models are identified by `name:tag` where the tag specifies size and quantisation. Custom models are defined via Modelfiles.

*Applies to: Ollama*
</div>
```text
┌────────────────────────────────────── Ai Local Ai Ollama Models ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Local Ai Ollama: Ai Local Ai Ollama Models platform                      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Ai Local Ai Ollama Models management console                   │   │
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
│    Physical: Ai Local Ai Ollama Models infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Local Ai Ollama    = Ai Local Ai Ollama Models platform overview and core concepts                 │
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


## Pulling Models

```bash
# Pull a model (default tag = latest, usually the smallest recommended quant)
ollama pull llama3.1:8b

# Pull a specific size and quantisation
ollama pull llama3.1:70b-instruct-q4_K_M

# Pull and immediately run
ollama run mistral:7b

# List downloaded models
ollama list

# Show model details (parameters, template, licence)
ollama show llama3.1:8b
ollama show llama3.1:8b --modelfile
```

## Popular Models and Tags

| Model | Tags | Notes |
|---|---|---|
| `llama3.1` | `8b`, `70b`, `405b` | Meta's Llama 3.1, strong general purpose |
| `mistral` | `7b`, `7b-instruct` | Fast and efficient |
| `codellama` | `7b`, `13b`, `34b`, `70b` | Code generation |
| `llava` | `7b`, `13b`, `34b` | Multimodal (vision) |
| `nomic-embed-text` | `latest` | Text embeddings |
| `phi3` | `mini`, `medium` | Microsoft Phi-3, small but capable |
| `gemma2` | `2b`, `9b`, `27b` | Google Gemma 2 |
| `qwen2.5` | `7b`, `14b`, `72b` | Alibaba Qwen 2.5 |
| `deepseek-coder-v2` | `lite`, `236b` | Code focused |

## Quantisation Levels

Quantisation reduces model size at the cost of some accuracy. For most tasks, Q4_K_M is a good default.

| Tag Suffix | Bits | Size vs F16 | Quality |
|---|---|---|---|
| `f16` | 16-bit float | 1× | Reference quality |
| `q8_0` | 8-bit | ~0.5× | Near-lossless |
| `q6_K` | 6-bit | ~0.38× | Very good |
| `q5_K_M` | 5-bit | ~0.31× | Good |
| `q4_K_M` | 4-bit | ~0.25× | Recommended default |
| `q4_0` | 4-bit | ~0.25× | Slightly lower quality than K_M |
| `q3_K_M` | 3-bit | ~0.19× | Noticeable quality loss |
| `q2_K` | 2-bit | ~0.13× | Significant degradation |

## Custom Modelfiles

Modelfiles let you create custom model variants with modified system prompts, parameters, or adapters.

```yaml
# Modelfile for a focused code review assistant
FROM codellama:13b

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
PARAMETER num_gpu 99

SYSTEM """
You are a senior software engineer reviewing code. Focus on:
- Security vulnerabilities
- Performance issues
- Code clarity and maintainability
Provide specific line references and concrete suggestions.
"""

TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
<|assistant|>
{{ end }}"""
```

```bash
# Build the custom model
ollama create code-reviewer -f ./Modelfile

# Use it
ollama run code-reviewer "Review this Python function: ..."
```

## GGUF Models from HuggingFace

```bash
# Import a GGUF file directly
cat > Modelfile << 'EOF'
FROM /path/to/model.gguf
SYSTEM "You are a helpful assistant."
PARAMETER temperature 0.7
EOF

ollama create my-custom-model -f Modelfile
ollama run my-custom-model
```

## Managing the Model Library

```bash
# Copy a model under a new name
ollama cp llama3.1:8b my-base-model

# Remove a model to free space
ollama rm llama2:7b

# Push a custom model to a registry (requires ollama.com account)
ollama push username/my-custom-model

# Check model storage usage
du -sh ~/.ollama/models/manifests/
du -sh ~/.ollama/models/blobs/
```
