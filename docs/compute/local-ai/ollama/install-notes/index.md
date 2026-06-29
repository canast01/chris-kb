---
tags:
  - ollama
  - ai
  - local-ai
---
# Ollama Installation Notes

<div class="kb-summary">
Ollama supports Linux, macOS, and Windows. On Linux, the recommended setup is the official install script or a manually configured systemd service. Docker is also well-supported.

*Applies to: Ollama*
</div>

```d2
direction: down

linux_installation: "Linux Installation" {shape: rectangle}
macos_installation: "macOS Installation" {shape: rectangle}
windows_installation: "Windows Installation" {shape: rectangle}
systemd_service_configuration: "Systemd Service Configuration" {shape: rectangle}
docker_setup: "Docker Setup" {shape: rectangle}
key_environment_variables: "Key Environment Variables" {shape: rectangle}

linux_installation -> macos_installation: uses
macos_installation -> windows_installation: uses
windows_installation -> systemd_service_configuration: uses
systemd_service_configuration -> docker_setup: uses
docker_setup -> key_environment_variables: uses
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


```text title="Expected output"
###################################################################
#                   Ollama Installer                              #
###################################################################

Downloading ollama...
  % Total    % Received % Xferd  Average Speed   Time    Left
100  45.2M  100  45.2M    0     0  8.3M      0  0:00:05  0:00:05 --:--:--
Installing ollama to /usr/local/bin...
Creating ollama user...
Creating systemd service...
Installation complete! Run 'ollama serve' to start the server.

ollama version is 0.1.32

● ollama.service - Ollama
     Loaded: loaded (/etc/systemd/system/ollama.service; enabled; vendor preset: enabled)
     Active: inactive (dead)
     Docs: https://github.com/ollama/ollama
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Update your CA certificates with `update-ca-certificates` or disable SSL verification temporarily with `curl -k`.
    **`sudo: systemctl: command not found`** — Ensure you're running the commands with `sudo` (e.g., `sudo systemctl status ollama`) or as root, since systemd operations require elevated privileges.
    **`useradd: user 'ollama' already exists`** — The ollama user already exists from a previous installation; proceed with the rest of the installation or remove it first with `userdel ollama`.
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


```text title="Expected output"
==> Downloading https://ghcr.io/v2/homebrew/core/ollama/manifests/latest
==> Downloading https://ghcr.io/v2/homebrew/core/ollama/manifests/0.1.32
==> Downloading ollama-0.1.32.arm64_sonoma.bottle.tar.gz
==> Pouring ollama-0.1.32.arm64_sonoma.bottle.tar.gz
🍺  /opt/homebrew/Cellar/ollama/0.1.32: 47 files, 245.3MB
==> Running `brew cleanup ollama`...
==> `brew services start ollama` is running under PID 2847.
Successfully started `ollama` (label: homebrew.mxcl.ollama).
```

!!! warning "Common errors"
    **`Error: ollama: No such file or directory`** — Run `brew install ollama` first before attempting to start the service.
    **`Error: homebrew.mxcl.ollama: already loaded`** — Run `brew services stop ollama` before restarting, or use `brew services restart ollama` instead.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to restart ollama.service: Unit ollama.service not found.`** — Install ollama first with the package manager or ensure the ollama systemd unit exists before creating overrides.
    **`Permission denied`** — Run the entire block with `sudo` since `/etc/systemd/system/` requires root access.
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


```text title="Expected output"
a1f2b3c4d5e6f7g8h9i0j1k2l3m4n5o6
a1f2b3c4d5e6f7g8h9i0j1k2l3m4n5o6
a1f2b3c4d5e6f7g8h9i0j1k2l3m4n5o6
{
  "models": []
}
```

!!! warning "Common errors"
    **`Error response from daemon: driver failed programming external connectivity on endpoint ollama: Bind for 0.0.0.0:11434 failed: port is already allocated`** — Stop the existing container with `docker stop ollama && docker rm ollama`, or use a different port with `-p 11435:11434`.
    **`docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]]`** — Install NVIDIA Docker runtime with `distribution=$(. /etc/os-release;echo $ID$VERSION_ID)` and follow nvidia-docker setup, or remove `--gpus all` for CPU-only mode.
    **`curl: (7) Failed to connect to localhost port 11434: Connection refused`** — Wait 2-3 seconds for the container to fully start, then retry `curl http://localhost:11434/api/tags`.
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


```text title="Expected output"
% curl -fsSL https://ollama.com/install.sh | sh
######################################################################## 100.0%
Installing ollama to /usr/local/bin/ollama
Created symlink /usr/local/bin/ollama → /opt/ollama/bin/ollama
Installation complete!

% brew upgrade ollama
==> Upgrading ollama
  0.1.32 -> 0.1.45
==> Downloading https://ghcr.io/v2/homebrew/core/ollama
==> Pouring ollama--0.1.45.monterey.bottle.tar.gz
🍺  /usr/local/Cellar/ollama/0.1.45 (142 files, 892MB)

% brew services restart ollama
Stopping `ollama`... (might take a few seconds)
==> Successfully stopped `ollama` (label: homebrew.mxcl.ollama)
==> Successfully started `ollama` (label: homebrew.mxcl.ollama)

% docker pull ollama/ollama
Using default tag: latest
latest: Pulling from ollama/ollama
8b16ab74ffd0: Pull complete
a475ecdd6c3f: Pull complete
Digest: sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Status: Downloaded newer image for ollama/ollama:latest

% docker stop ollama && docker rm ollama
ollama
ollama
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to ollama.com port 443: Connection refused`** — Verify network connectivity and check if ollama.com is accessible; try again after confirming DNS resolution with `nslookup ollama.com`.
    **`Error: Homebrew must be run under Ruby 2.3.0! You're running 2.0.0.`** — Update Homebrew with `brew update` or reinstall it following the official Homebrew installation guide.
    **`Error response from daemon: No such container: ollama`** — The container doesn't exist or has already been removed; skip the `docker stop` command and proceed directly with `docker run` to create a fresh container.
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


```text title="Expected output"
4.2G	/home/ubuntu/.ollama/models/

NAME                    ID              SIZE      MODIFIED
mistral:latest          2ae4a534d206    4.1GB     2 minutes ago
neural-chat:7b          b586909a7e21    3.9GB     1 hour ago
llama2:7b               9ff71d577b6f    3.8GB     3 days ago
llama2:13b              91abfb1d3456    7.4GB     5 days ago

Deleted model 'llama2:7b'
```

!!! warning "Common errors"
    **`Error: model 'llama2:7b' not found`** — Verify the exact model name and tag with `ollama list` before attempting removal.
    **`Error: permission denied`** — Ensure the user running the command has read/write permissions to `~/.ollama/models/` directory.