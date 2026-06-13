# Ollama Installation Notes


<div class="kb-summary">
Ollama supports Linux, macOS, and Windows. On Linux, the recommended setup is the official install script or a manually configured systemd service. Docker is also well-supported.

*Applies to: Ollama*
</div>
```text
┌────────────────────────────────── Ai Local Ai Ollama Install Notes ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   Local Ai Ollama: Ai Local Ai Ollama Install Notes platform                  │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Ai Local Ai Ollama Install Notes management console                │   │
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
│    Physical: Ai Local Ai Ollama Install Notes infrastructure · management network · monitoring        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Local Ai Ollama    = Ai Local Ai Ollama Install Notes platform overview and core concepts          │
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


## Linux Installation

```bash
# Official one-liner (installs to /usr/local/bin, creates systemd service)
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
systemctl status ollama

# The installer creates:
# - /usr/local/bin/ollama (binary)
# - /etc/systemd/system/ollama.service (service file)
# - ollama user and group
# - /usr/share/ollama/.ollama (model storage)
```

## macOS Installation

```bash
# Download the macOS app from ollama.com, or use Homebrew
brew install ollama

# Start as a background service
brew services start ollama

# Or run interactively
ollama serve

# Models are stored in ~/.ollama/models
```

## Windows Installation

Download the installer from [ollama.com](https://ollama.com). Ollama installs as a Windows service. Models are stored in `C:\Users\<user>\.ollama\models`.

For WSL2 users, install the Linux version inside WSL2. GPU passthrough requires WSL2 with CUDA support (Windows 11 or Windows 10 21H2+).

## Systemd Service Configuration

The default service binds to `127.0.0.1:11434`. To expose on all interfaces or a different port:

```bash
# Edit the service override
mkdir -p /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/override.conf << 'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MODELS=/data/ollama/models"
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_MAX_LOADED_MODELS=2"
EOF

systemctl daemon-reload
systemctl restart ollama
```

## Docker Setup

```bash
# CPU only
docker run -d \
  -v ollama-models:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama

# NVIDIA GPU
docker run -d \
  --gpus all \
  -v ollama-models:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama

# AMD GPU (ROCm)
docker run -d \
  --device /dev/kfd --device /dev/dri \
  -v ollama-models:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama:rocm

# Verify it's running
curl http://localhost:11434/api/tags
```

## Key Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `127.0.0.1:11434` | Listen address and port |
| `OLLAMA_MODELS` | `~/.ollama/models` | Model storage directory |
| `OLLAMA_NUM_PARALLEL` | `1` | Concurrent request handling |
| `OLLAMA_MAX_LOADED_MODELS` | `1` | Max models in memory |
| `OLLAMA_KEEP_ALIVE` | `5m` | How long to keep model loaded |
| `OLLAMA_DEBUG` | `0` | Enable verbose debug logging |
| `OLLAMA_FLASH_ATTENTION` | `0` | Enable flash attention |
| `CUDA_VISIBLE_DEVICES` | (all) | Which GPUs to use |

## Updating Ollama

```bash
# Linux: re-run the install script
curl -fsSL https://ollama.com/install.sh | sh

# macOS with Homebrew
brew upgrade ollama
brew services restart ollama

# Docker: pull the new image
docker pull ollama/ollama
docker stop ollama && docker rm ollama
# Re-run the docker run command with the same volume
```

## Storage Planning

Models can be large. Ensure the model storage directory has sufficient space:

```bash
# Check space used by current models
du -sh ~/.ollama/models/

# List models and their sizes
ollama list

# Remove unused models
ollama rm llama2:7b
```
