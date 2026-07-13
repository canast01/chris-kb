---
tags:
  - ollama
  - ai
  - local-ai
description: "Ollama is a tool for running large language models locally. You download models to your machine and talk to them through the ollama command or its..."
---
# Ollama CLI Reference

<div class="kb-summary">
Ollama is a tool for running large language models locally. You download models to your machine and talk to them through the `ollama` command or its built-in API server — no cloud account or API key required.

*Applies to: Ollama*
</div>

 Models are stored as layers (similar to Docker images) and run on your GPU if one is available, or fall back to CPU.

> Install on macOS with `brew install ollama` or download from ollama.com. On Linux, use the install script: `curl -fsSL https://ollama.com/install.sh | sh`. Start the server with `ollama serve` (runs automatically as a service on macOS after install).
---

```d2
direction: down

model_management: "Model Management" {shape: rectangle}
running_models: "Running Models" {shape: rectangle}
server: "Server" {shape: rectangle}
custom_models_modelfiles: "Custom Models (Modelfiles)" {shape: rectangle}
environment_configuration: "Environment & Configuration" {shape: rectangle}
common_patterns: "Common Patterns" {shape: rectangle}

model_management -> running_models: uses
running_models -> server: uses
server -> custom_models_modelfiles: uses
custom_models_modelfiles -> environment_configuration: uses
environment_configuration -> common_patterns: uses
```

## Model Management

Download, list, remove, and copy models. Models are pulled from the Ollama registry by name — use `name:tag` to pin a specific version or quantization level. If you omit the tag, you get the default (usually `latest`).

```bash
# Download a model
ollama pull llama3.2
ollama pull llama3.2:3b               # specific size variant
ollama pull llama3.2:3b-instruct-q4_K_M  # specific quantization
ollama pull mistral
ollama pull gemma3:27b
ollama pull nomic-embed-text          # embedding model (not chat)
ollama pull qwen2.5-coder:7b          # code-focused model

# List downloaded models
ollama list
ollama ls                             # alias for list

# Show model details (architecture, parameters, quantization)
ollama show llama3.2
ollama show llama3.2 --modelfile      # show the Modelfile used to create it
ollama show llama3.2 --parameters     # show sampling parameters
ollama show llama3.2 --template       # show the prompt template

# Remove a model (frees disk space)
ollama rm llama3.2
ollama rm llama3.2:3b

# Copy a model under a new name (useful before customizing)
ollama cp llama3.2 my-custom-llama

# Push a model to the Ollama registry (requires account)
ollama push my-namespace/my-model
```


```text title="Expected output"
pulling manifest
pulling 6a0746a1ec1a
pulling 4e4f826dd538
pulling 2e0493f7e0ba
pulling 92661c9fdf0e
pulling 8ab4d8b6b4c9
verifying sha256 digest
writing manifest
removing any unused layers
success
NAME                           	ID          	SIZE  	MODIFIED
llama3.2:latest                	45e6d7bb5c92	8.0 GB	2 minutes ago
llama3.2:3b                    	a1b2c3d4e5f6	2.0 GB	5 minutes ago
mistral:latest                 	f7e8d9c0b1a2	4.1 GB	1 hour ago
gemma3:27b                     	c3d4e5f6a7b8	16 GB	3 hours ago
nomic-embed-text:latest        	d5e6f7a8b9c0	274 MB	2 hours ago
qwen2.5-coder:7b               	e7f8a9b0c1d2	4.5 GB	45 minutes ago

Model details for llama3.2:
architecture: llama
parameters: 8.0B
quantization: Q4_K_M
context window: 8192
embedding dimension: 4096

Modelfile:
FROM /usr/share/ollama/models/llama3.2-8b-instruct-q4_K_M.gguf
TEMPLATE [INST] {{ .Prompt }} [/INST]

Sampling parameters:
temperature: 0.7
top_k: 40
top_p: 0.9
repeat_penalty: 1.1

Prompt template:
[INST] {{ .Prompt }} [/INST]

deleted 'llama3.2'
deleted 'llama3.2:3b'
copied 'llama3.2' to 'my-custom-llama'
pushing manifest
pushing 6a0746a1ec1a
pushing 4e4f826dd538
pushing 2e0493f7e0ba
pushing 4f5g9h0i1j2k
verifying sha256 digest
success
```

!!! warning "Common errors"
    **`Error: model 'llama3.2' not found`** — Run `ollama pull llama3.2` first to download the model before attempting to use it.
    **`Error: push failed: unauthorized`** — Authenticate with `ollama login` and ensure your namespace matches your Ollama Hub username.
    **`Error: insufficient disk space: need 8.0 GB, have 2.5 GB available`** — Free up disk space or pull a smaller model variant (e.g., `ollama pull llama3.2:3b` instead of the full 8B version).
---

## Running Models

Start an interactive chat session or send a one-shot prompt from the command line. The model server is started automatically when you run `ollama run` if it isn't already running.

```bash
# Start an interactive chat session
ollama run llama3.2
ollama run mistral
ollama run llama3.2:70b              # run the 70B parameter version

# Send a single prompt (non-interactive — useful in scripts)
ollama run llama3.2 "Explain what a VLAN is in one sentence"
echo "What is iSCSI?" | ollama run llama3.2

# Multiline input in interactive mode
# Use triple-quote to start a multiline block:
# >>> """
# ... line 1
# ... line 2
# ... """

# Pass an image (multimodal models only)
ollama run llava "Describe this image" /path/to/image.png

# Useful interactive session commands
# /show info        — show current model details
# /show modelfile   — show the Modelfile
# /set parameter num_ctx 4096  — change context window mid-session
# /set verbose      — show token counts and generation speed
# /bye or Ctrl-D    — exit

# Check which models are currently loaded (running in memory)
ollama ps
```


```text title="Expected output"
>>> Send a single prompt (non-interactive — useful in scripts)
>>> ollama run llama3.2 "Explain what a VLAN is in one sentence"
A VLAN (Virtual Local Area Network) is a logical grouping of network devices that allows you to segment a physical network into multiple isolated broadcast domains for improved security and traffic management.

>>> echo "What is iSCSI?" | ollama run llama3.2
iSCSI (Internet Small Computer Systems Interface) is a protocol that enables block-level data storage access over IP networks by encapsulating SCSI commands in TCP/IP packets, allowing remote storage devices to appear as local disks.

>>> ollama run llava "Describe this image" /path/to/image.png
The image shows a network topology diagram with three switches connected in a triangle formation, each labeled with IP addresses 192.168.1.1, 192.168.2.1, and 192.168.3.1, with colored links indicating active connections.

>>> ollama ps
NAME            ID              SIZE      PROCESSOR       UNTIL
llama3.2        a1b2c3d4e5f6    4.7GB     GPU             4 minutes from now
mistral         f6e5d4c3b2a1    13GB      GPU             2 minutes from now
```

!!! warning "Common errors"
    **`Error: model 'llama3.2' not found, try pulling it first`** — Run `ollama pull llama3.2` to download the model before attempting to run it.
    **`Error: CUDA out of memory. Tried to allocate 2.50 GiB`** — Reduce the model size (e.g., use `llama3.2:7b` instead of `70b`), or stop other running models with `ollama stop <model_name>`.
    **`Error: image file not found: /path/to/image.png`** — Verify the image path exists and use an absolute path or relative path from your current working directory.
---

## Server

The Ollama server exposes a local REST API on port 11434. It manages model loading, keeps recently used models in GPU memory, and handles concurrent requests. You typically don't need to start it manually — it runs as a background service.

```bash
# Start the server manually (foreground)
ollama serve

# Start with a custom host/port
OLLAMA_HOST=0.0.0.0:11434 ollama serve   # listen on all interfaces

# Check server health (returns {"status":"ok"} if running)
curl http://localhost:11434/

# List running models via API
curl http://localhost:11434/api/ps

# Send a chat request via API
curl http://localhost:11434/api/chat \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Hello"}]}'

# Generate (single-turn, no history) via API
curl http://localhost:11434/api/generate \
  -d '{"model":"llama3.2","prompt":"What is Terraform?","stream":false}'

# Pull a model via API
curl http://localhost:11434/api/pull \
  -d '{"name":"mistral"}'

# Generate an embedding vector
curl http://localhost:11434/api/embed \
  -d '{"model":"nomic-embed-text","input":"Some text to embed"}'
```


```text title="Expected output"
time=2025-01-15T09:42:33.847Z level=INFO msg="Starting Ollama server"
time=2025-01-15T09:42:33.912Z level=INFO msg="Listening on 127.0.0.1:11434"
time=2025-01-15T09:42:33.920Z level=INFO msg="Ollama is running"

{"status":"ok"}

[{"name":"llama3.2","model":"llama3.2:latest","size":4687671680,"digest":"sha256:a1b2c3d4e5f6","expires_at":"2025-01-22T09:42:33.847Z","size_vram":4687671680}]

{"message":"Hello! How can I help you today?","model":"llama3.2","created_at":"2025-01-15T09:42:45.123Z","done":true}

{"response":"Terraform is an Infrastructure as Code (IaC) tool developed by HashiCorp that allows you to define, provision, and manage cloud infrastructure using declarative configuration files...","model":"llama3.2","created_at":"2025-01-15T09:42:52.456Z","done":true,"total_duration":8234567890}

{"status":"pulling manifest"}
{"status":"downloading 5b70705...","digest":"sha256:5b70705...","total":4687671680,"completed":2343835840}
{"status":"verifying sha256 digest"}
{"status":"writing manifest"}
{"status":"success"}

{"embedding":[0.0234,-0.0891,0.1234,-0.0456,0.0789,...]}
```

!!! warning "Common errors"
    **`Error: listen tcp 127.0.0.1:11434: bind: address already in use`** — Kill the existing Ollama process with `pkill ollama` or use a different port with `OLLAMA_HOST=127.0.0.1:11435 ollama serve`.
    **`curl: (7) Failed to connect to localhost port 11434: Connection refused`** — Start the Ollama server first with `ollama serve` in another terminal or background process.
    **`{"error":"model 'llama3.2' not found"}`** — Pull the model first with `ollama pull llama3.2` before sending requests.
---

## Custom Models (Modelfiles)

A Modelfile is a plain-text recipe that defines a custom model — you can base it on any downloaded model and change the system prompt, sampling parameters, and prompt template. Think of it like a Dockerfile but for LLMs.

```bash
# Create a Modelfile
cat > Modelfile <<'EOF'
FROM llama3.2

# System prompt — sets the model's persona and constraints
SYSTEM """
You are a senior infrastructure engineer. Answer questions concisely
with a focus on production-readiness and operational impact.
"""

# Sampling parameters (optional overrides)
PARAMETER temperature 0.5       # lower = more deterministic
PARAMETER top_p 0.9
PARAMETER num_ctx 8192          # context window in tokens
PARAMETER num_predict 1024      # max tokens to generate
EOF

# Build the model from the Modelfile
ollama create infra-assistant -f Modelfile

# Test it
ollama run infra-assistant "What happens when a Fibre Channel link goes down?"

# Update a model (edit Modelfile, then recreate with same name)
ollama create infra-assistant -f Modelfile

# Modelfile FROM variants
# FROM llama3.2                  — use a registry model
# FROM ./model.gguf              — use a local GGUF file
# FROM my-namespace/my-model    — use a registry model you pushed
```


```text title="Expected output"
# Modelfile created successfully
(no output — command completes silently)

successfully created model 'infra-assistant'

When a Fibre Channel link goes down, the storage array detects the loss of signal (LOS) 
and triggers failover to redundant paths if configured. Applications experience I/O delays 
or timeouts depending on multipath driver settings. Monitor with `fcstat` and verify 
redundancy is active via `multipathd show topology`. Recovery time depends on your 
fabric's failover timeout (typically 30-90 seconds). Ensure your SAN fabric has 
redundant switches and HBAs to minimize impact.

successfully created model 'infra-assistant'
```

!!! warning "Common errors"
    **`error: model not found`** — Run `ollama pull llama3.2` first to download the base model from the registry.
    **`error: open Modelfile: no such file or directory`** — Verify the Modelfile path is correct and you're in the directory where you created it with `cat >`.
    **`error: failed to create model: context length exceeds maximum`** — Reduce `num_ctx` value (e.g., to 4096) if your system lacks sufficient VRAM to support the requested context window.
---

## Environment & Configuration

Ollama's behavior is controlled through environment variables. On macOS, set these in the service's launchd plist or export them in your shell before running `ollama serve`. On Linux (systemd), add them to `/etc/systemd/system/ollama.service.d/override.conf`.

```bash
# Common environment variables
OLLAMA_HOST=0.0.0.0:11434       # bind address for the API server (default: 127.0.0.1:11434)
OLLAMA_MODELS=/data/ollama      # custom model storage path (default: ~/.ollama/models)
OLLAMA_NUM_PARALLEL=2           # max concurrent model requests
OLLAMA_MAX_LOADED_MODELS=2      # how many models to keep in GPU memory simultaneously
OLLAMA_KEEP_ALIVE=5m            # how long to keep a model loaded after last request (default: 5m)
OLLAMA_FLASH_ATTENTION=1        # enable flash attention (better GPU memory use)
OLLAMA_GPU_OVERHEAD=0           # reserve GPU VRAM (bytes) for other processes
CUDA_VISIBLE_DEVICES=0,1        # limit to specific GPUs (NVIDIA)
ROCR_VISIBLE_DEVICES=0          # limit to specific GPUs (AMD)

# macOS: edit launchd environment to persist settings
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"

# Linux (systemd): create an override to add env vars
sudo systemctl edit ollama
# Add:
# [Service]
# Environment="OLLAMA_HOST=0.0.0.0:11434"
# Environment="OLLAMA_MODELS=/data/ollama/models"
sudo systemctl daemon-reload && sudo systemctl restart ollama

# Check disk usage of model storage
du -sh ~/.ollama/models/
du -sh ~/.ollama/models/manifests/registry.ollama.ai/library/*/

# Log location
# macOS: journalctl or Console.app (system log) — Ollama logs to stderr
# Linux: journalctl -u ollama -f
journalctl -u ollama -f
journalctl -u ollama --since "1 hour ago"
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
12G	/home/ollama/.ollama/models/
2.1G	/home/ollama/.ollama/models/manifests/registry.ollama.ai/library/llama2/
1.8G	/home/ollama/.ollama/models/manifests/registry.ollama.ai/library/mistral/
3.4G	/home/ollama/.ollama/models/manifests/registry.ollama.ai/library/neural-chat/
...
-- Logs begin at Wed 2024-01-10 14:22:33 UTC, end at Wed 2024-01-10 15:47:12 UTC --
Jan 10 15:47:08 ai-server ollama[2847]: time=2024-01-10T15:47:08.234Z level=INFO msg="Listening on 0.0.0.0:11434"
Jan 10 15:47:09 ai-server ollama[2847]: time=2024-01-10T15:47:09.567Z level=INFO msg="loaded model llama2:latest"
Jan 10 15:47:12 ai-server ollama[2847]: time=2024-01-10T15:47:12.891Z level=INFO msg="request completed" model=llama2 duration=3.2s
```

!!! warning "Common errors"
    **`Error: mkdir /data/ollama: permission denied`** — Run the command with `sudo` or ensure the user running ollama has write permissions to the parent directory.
    **`journalctl: No such file or directory`** — Use `sudo journalctl -u ollama -f` or check that systemd is installed; on non-systemd systems use `tail -f /var/log/ollama.log` instead.
    **`[Service] section not found in /etc/systemd/system/ollama.service.d/override.conf`** — Ensure `sudo systemctl edit ollama` opens the editor correctly and the syntax includes `[Service]` header before environment variables.
---

## Common Patterns

```bash
# Quick model comparison — same prompt, different models
for model in llama3.2 mistral gemma3:4b; do
  echo "=== $model ===" && ollama run "$model" "What is a storage aggregate?" && echo
done

# Pipe output into another tool
ollama run llama3.2 "List 5 Linux commands for disk troubleshooting" | grep -E '^\d\.'

# Use in a shell script (non-interactive)
RESPONSE=$(ollama run llama3.2 "Summarize in one line: $INPUT")

# Keep a model warm (prevent it from being unloaded)
curl http://localhost:11434/api/generate \
  -d '{"model":"llama3.2","keep_alive":-1,"prompt":""}'

# Unload a model immediately (free GPU memory)
curl http://localhost:11434/api/generate \
  -d '{"model":"llama3.2","keep_alive":0,"prompt":""}'

# Find all GGUF files on disk (useful when importing local models)
find ~ -name "*.gguf" 2>/dev/null

# Import a local GGUF and run it
echo "FROM /path/to/model.gguf" | ollama create my-local-model -f -
ollama run my-local-model
```


```text title="Expected output"
=== llama3.2 ===
A storage aggregate is a logical grouping of physical storage devices in NetApp systems that combines multiple disks into a single management unit for RAID protection and capacity provisioning.

=== mistral ===
A storage aggregate in NetApp terminology refers to a collection of physical disks organized into RAID groups, providing redundancy and shared storage capacity for multiple volumes.

=== gemma3:4b ===
Storage aggregates are pools of disk drives managed as a single unit, commonly used in enterprise storage systems to distribute data and ensure fault tolerance.

1. df — displays disk space usage
2. du — estimates file and directory sizes
3. iostat — monitors disk I/O performance
4. lsblk — lists block devices and partitions
5. smartctl — checks disk health and SMART status

{"model":"llama3.2","status":"success","response":"","done":true}
{"model":"llama3.2","status":"success","response":"","done":true}

/home/user/.ollama/models/llama3.2.gguf
/mnt/storage/models/mistral-7b.gguf
/opt/local-models/gemma-2b.gguf

transferring model data
pulling manifest
pulling 3d6ba21f45c4
pulling 5c40651648fa
pulling 8f498d36fed3
pulling 5f7cbf9b5d7e
pulling e963a1d3c3da
verifying sha256 digest
writing manifest
removing any unused layers
success
```
Running model my-local-model...
What would you like to know?
!!! warning "Common errors"
    **`Error: model "llama3.2" not found, try pulling it first`** — Run `ollama pull llama3.2` before attempting to run the model.
    **`Error: connection refused — connect to localhost:11434`** — Ensure the Ollama service is running with `ollama serve` or verify it's listening on port 11434.
    **`Error: failed to create model: file not found "/path/to/model.gguf"`** — Verify the GGUF file path exists and use the absolute path in the Modelfile `FROM` directive.
## See also

- [Ollama — Overview](../../)
