---
tags:
  - ollama
  - ai
  - local-ai
description: "Ollama's model library includes a wide range of open models. Models are identified by name:tag where the tag specifies size and quantisation. Custom..."
---
# Ollama Models

<div class="kb-summary">
Ollama's model library includes a wide range of open models. Models are identified by `name:tag` where the tag specifies size and quantisation. Custom models are defined via Modelfiles.

*Applies to: Ollama*
</div>

```d2
direction: down

pulling_models: "Pulling Models" {shape: rectangle}
popular_models_and_tags: "Popular Models and Tags" {shape: rectangle}
quantisation_levels: "Quantisation Levels" {shape: rectangle}
custom_modelfiles: "Custom Modelfiles" {shape: rectangle}
gguf_models_from_huggingface: "GGUF Models from HuggingFace" {shape: rectangle}
managing_the_model_library: "Managing the Model Library" {shape: rectangle}

pulling_models -> popular_models_and_tags: uses
popular_models_and_tags -> quantisation_levels: uses
quantisation_levels -> custom_modelfiles: uses
custom_modelfiles -> gguf_models_from_huggingface: uses
gguf_models_from_huggingface -> managing_the_model_library: uses
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


```text title="Expected output"
pulling manifest
pulling 4f0e4312f8e1
pulling 8de71801ce48
pulling 2e0493f59d13
pulling 5236e8387e1f
pulling 6a0746a1ec1a
verifying sha256 digest
writing manifest
success

pulling manifest
pulling 7b4e8c2f9d1a
pulling 3c5f1a8e2b9d
pulling 9e2d4c7f1b3a
pulling 1a8f5c3e9b2d
pulling 4d7e2f9c1a5b
verifying sha256 digest
writing manifest
success

>>> Send a message (/? for help)
>>> Hello

The Mistral model is now running. Type your message or /bye to exit.

NAME                    ID              SIZE    MODIFIED
llama3.1:8b             a1b2c3d4e5f6    4.7GB   2 minutes ago
llama3.1:70b-instruct   f6e5d4c3b2a1    43GB    5 minutes ago
mistral:7b              9z8y7x6w5v4u    4.1GB   1 minute ago

# Model info for llama3.1:8b
Model
	arch                    llama
	parameters              8.0B
	quantization            Q4_K_M
	context length          8192
	embedding length        4096

Parameters
	stop                    "<|start_header_id|>"
	stop                    "<|end_header_id|>"
	stop                    "<|eot_id|>"

License
	LLAMA 2 COMMUNITY LICENSE AGREEMENT

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: model not found` | Verify the model name and tag exist on ollama.com, then retry the pull command. |
    | `Error: insufficient disk space` | Check available disk space with `df -h` and ensure at least 50GB free for large models like 70b variants. |
    | `Error: connection refused` | Start the Ollama daemon with `ollama serve` in another terminal or ensure the service is running. |
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


```text title="Expected output"
pulling manifest
pulling 3c2fbf5da27e
pulling 5c40d17bd924
pulling e994b72fc1f3
pulling 2e0773155812
pulling 8f025a1e9c4a
digest: sha256:8c156b8f9e2a3d4c5b6a7f8e9d0c1b2a3f4e5d6c7b8a9f0e1d2c3b4a5f6e7d
status: success

code-reviewer: created successfully

Review this Python function: ...

The function appears to be a utility for data validation. Consider adding type hints for better IDE support and documentation. The error handling could be more specific—currently catching all exceptions broadly.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: could not find Modelfile` | Ensure the Modelfile exists in the current directory and the path `./Modelfile` is correct. |
    | `Error: model not found` | Run `ollama create code-reviewer -f ./Modelfile` successfully before attempting to run the model. |
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


```text title="Expected output"
# Modelfile created successfully
(no output — command completes silently)

pulling manifest
pulling 3c20f7190570
pulling 5046e3b89b12
pulling e290ff4c5c22
pulling 2e0513e4a477
pulling 2bea3b022b21
verifying sha256 digest
writing manifest
removing any unused layers
success

>>> Hello! How can I help you today?
>>> What's the weather like?
I don't have access to real-time weather data, but I'd be happy to help you find weather information if you tell me your location.
>>> /bye
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: model not found` | Verify the path to model.gguf is absolute and the file exists with `ls -lh /path/to/model.gguf`. |
    | `Error: failed to create model: invalid modelfile` | Check that the Modelfile syntax is correct and the FROM path points to a valid GGUF file, not a directory. |
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


```text title="Expected output"
copying llama3.1:8b to my-base-model... 100% ▕████████████████████▏
deleted llama2:7b
pushing username/my-custom-model... 100% ▕████████████████████▏
pushing manifest... 100% ▕████████████████████▏
pushing config... 100% ▕████████████████████▏
4.2G	/home/user/.ollama/models/manifests/
18G	/home/user/.ollama/models/blobs/
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: model 'llama3.1:8b' not found` | Verify the model exists locally with `ollama list` before copying. |
    | `Error: push failed: unauthorized: authentication required` | Log in with `ollama login` or ensure your ollama.com credentials are valid. |
    | `Error: model 'llama2:7b' is in use` | Stop any running Ollama processes using the model with `ollama stop` before removing it. |