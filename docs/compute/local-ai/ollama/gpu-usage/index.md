---
tags:
  - ollama
  - ai
  - local-ai
---
# Ollama GPU Acceleration

<div class="kb-summary">
Ollama automatically uses the GPU when drivers and CUDA/ROCm are installed. This page covers confirming GPU usage, configuring which GPU(s) to use, VRAM requirements per model, and ROCm support.

*Applies to: Ollama*
</div>

```d2
direction: down

confirming_gpu_usage: "Confirming GPU Usage" {shape: rectangle}
cuda_setup: "CUDA Setup" {shape: rectangle}
rocm_amd_gpu_setup: "ROCm (AMD GPU) Setup" {shape: rectangle}
vram_requirements_by_model_size: "VRAM Requirements by Model Size" {shape: rectangle}
controlling_gpu_layer_count: "Controlling GPU Layer Count" {shape: rectangle}
multigpu_configuration: "Multi-GPU Configuration" {shape: rectangle}

confirming_gpu_usage -> cuda_setup: uses
cuda_setup -> rocm_amd_gpu_setup: uses
rocm_amd_gpu_setup -> vram_requirements_by_model_size: uses
vram_requirements_by_model_size -> controlling_gpu_layer_count: uses
controlling_gpu_layer_count -> multigpu_configuration: uses
```

## Confirming GPU Usage

```bash
# When running a model, check if GPU layers are loaded
ollama run llama3.1:8b "Hello"

# In a separate terminal, watch GPU utilisation
watch -n 1 nvidia-smi

# Or query Ollama's running model info
curl http://localhost:11434/api/show \
  -d '{"name":"llama3.1:8b"}' | jq '.details'

# Check Ollama logs for GPU detection
journalctl -u ollama -n 50
# Look for: "detected GPU" or "loaded model ... on GPU"
```


```text title="Expected output"
Hello

NVIDIA-SMI 535.104.05    Driver Version: 535.104.05    CUDA Version: 12.2     |
GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
  0  NVIDIA RTX 4090      Off  | 00:1E.0     Off |                  0 |
  0%   45C    P2    89W / 575W |   7842MiB / 24576MiB |     68%      Default |
  1  NVIDIA RTX 4090      Off  | 00:1F.0     Off |                  0 |
  0%   38C    P8     5W / 575W |      0MiB / 24576MiB |      0%      Default |

{
  "parameter_size": "8.0B",
  "quantization_level": "Q4_K_M",
  "family": "llama",
  "families": ["llama"],
  "object_type": "model"
}

Nov 15 14:32:18 gpu-server ollama[2847]: time=2024-11-15T14:32:18.234Z level=INFO msg="detected GPU" id=0 name="NVIDIA RTX 4090" vram=24576000000
Nov 15 14:32:19 gpu-server ollama[2847]: time=2024-11-15T14:32:19.567Z level=INFO msg="loaded model llama3.1:8b on GPU 0" layers=33/33
Nov 15 14:32:20 gpu-server ollama[2847]: time=2024-11-15T14:32:20.891Z level=INFO msg="inference complete" duration=2.3s tokens_per_sec=45.2
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 11434: Connection refused`** — Ensure Ollama service is running with `systemctl start ollama` and listening on port 11434.
    **`jq: parse error: Cannot index object with string "details"`** — The API response structure differs; use `curl http://localhost:11434/api/show -d '{"name":"llama3.1:8b"}' | jq '.'` to inspect the full response first.
    **`Unit ollama.service could not be found`** — Install and enable the Ollama systemd service, or check logs directly with `ollama serve` in foreground mode instead of journalctl.
Ollama outputs the number of GPU layers loaded at model start. If `num_gpu: 0` appears, Ollama is running on CPU only.

## CUDA Setup

Ollama bundles its own CUDA libraries and only requires the NVIDIA driver — the CUDA toolkit does not need to be installed separately.

```bash
# Verify driver is present
nvidia-smi

# Check Ollama detects the GPU
OLLAMA_DEBUG=1 ollama run llama3.1:8b "test" 2>&1 | grep -i gpu

# Set specific GPU(s) (CUDA device index)
CUDA_VISIBLE_DEVICES=0 ollama serve   # Use GPU 0 only
CUDA_VISIBLE_DEVICES=0,1 ollama serve # Use GPUs 0 and 1
```


```text title="Expected output"
Fri Jan 10 14:32:15 2025
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.104.05    Driver Version: 535.104.05    CUDA Version: 12.2             |
|---------------------------------------------------------------------------------------|
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA RTX 4090      Off  | 00:1F.0     Off |                  Off |
| 30%   42C    P0    89W / 575W |   8192MiB / 24576MiB |     45%      Default |
|   1  NVIDIA RTX 4090      Off  | 00:20.0     Off |                  Off |
| 25%   38C    P0    72W / 575W |   6144MiB / 24576MiB |     32%      Default |
+---------------------------------------------------------------------------------------+

time=2025-01-10T14:32:47.123Z level=INFO msg="GPU detected" device_id=0 device_name="NVIDIA RTX 4090" compute_capability="8.9"
time=2025-01-10T14:32:47.124Z level=INFO msg="GPU detected" device_id=1 device_name="NVIDIA RTX 4090" compute_capability="8.9"
```

!!! warning "Common errors"
    **`NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`** — Reinstall the NVIDIA driver with `sudo apt install nvidia-driver-535` (or appropriate version) and reboot.
    **`time=2025-01-10T14:32:47.123Z level=ERROR msg="no CUDA-capable device is detected"`** — Verify GPU visibility with `nvidia-smi` and ensure `CUDA_VISIBLE_DEVICES` is not restricting access to all devices.
## ROCm (AMD GPU) Setup

```bash
# Install ROCm 6.x (Ubuntu 22.04)
wget https://repo.radeon.com/amdgpu-install/6.1.2/ubuntu/jammy/amdgpu-install_6.1.60102-1_all.deb
dpkg -i amdgpu-install_6.1.60102-1_all.deb
apt-get update
amdgpu-install --usecase=rocm

# Add user to render and video groups
usermod -aG render,video $USER

# Verify ROCm
rocm-smi
rocminfo | grep gfx

# Ollama uses ROCm automatically when detected
HSA_OVERRIDE_GFX_VERSION=11.0.0 ollama serve  # Override for unsupported gfx version
```


```text title="Expected output"
Get:1 https://repo.radeon.com/amdgpu-install/6.1.2/ubuntu/jammy InRelease [1,247 B]
Get:2 https://repo.radeon.com/amdgpu-install/6.1.2/ubuntu/jammy/amdgpu-install all [45.2 MB]
Fetched 45.2 MB in 8s (5.6 MB/s)
Reading package lists... Done
Setting up amdgpu-install (6.1.60102-1) ...
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  rocm-core rocm-device-libs rocm-runtime hip-runtime-amd rocm-smi
Processing triggers for libc-bin (2.35-0ubuntu3.4) ...
Processing triggers for man-db (2.10.2-1) ...

ROCm version: 6.1.60102
GPU 0: AMD Radeon RX 7900 XTX
  GPU Memory: 24576 MB
  Temperature: 45 C
  GPU Load: 0 %

gfx1100
gfx1101

Ollama running on 127.0.0.1:11434
```

!!! warning "Common errors"
    **`dpkg: error processing archive (--unpack): cannot open file '/root/amdgpu-install_6.1.60102-1_all.deb': No such file or directory`** — Run `wget` first to download the .deb file, or verify the file exists with `ls -la amdgpu-install*.deb`.
    **`usermod: user 'root' is already a member of 'render' group`** — This is informational when running as root; the command succeeds and the user is already in the required groups.
    **`rocm-smi: command not found`** — Ensure ROCm installation completed successfully by running `apt-get install rocm-smi` explicitly, or verify `/opt/rocm/bin` is in your PATH with `echo $PATH`.
## VRAM Requirements by Model Size

| Model | Quantisation | VRAM Required | Minimum GPU |
|---|---|---|---|
| llama3.1:8b | Q4_K_M (default) | ~5 GB | RTX 3060 12GB |
| llama3.1:8b | F16 | ~16 GB | RTX 3080 / A10G |
| llama3.1:70b | Q4_K_M | ~40 GB | A100 40GB |
| llama3.1:70b | Q8_0 | ~74 GB | A100 80GB |
| mistral:7b | Q4_K_M | ~4.5 GB | RTX 3060 |
| llava:13b (vision) | Q4_K_M | ~8 GB | RTX 3080 |
| codestral:22b | Q4_K_M | ~13 GB | RTX 3090 |

## Controlling GPU Layer Count

Ollama automatically calculates how many layers fit in VRAM. Override with `OLLAMA_NUM_GPU`:

```bash
# Force specific number of layers to GPU (0 = CPU only, 99 = all layers)
OLLAMA_NUM_GPU=32 ollama run llama3.1:8b

# Or in Modelfile
FROM llama3.1:8b
PARAMETER num_gpu 32
```


```text title="Expected output"
pulling manifest
pulling 6a0746a1ec1a
pulling 4fa551d4061c
pulling c41d6999ee2d
pulling 2e0d4e6c4f21
pulling 8b6f3522f969
verifying sha256 digest
writing manifest
removing any unused layers
success
>>> What is machine learning?
Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms and statistical models to identify patterns in data and make predictions or decisions based on those patterns.

>>> /bye
```

!!! warning "Common errors"
    **`Error: model not found`** — Run `ollama pull llama3.1:8b` first to download the model.
    **`Error: CUDA out of memory`** — Reduce `OLLAMA_NUM_GPU` value (e.g., set to 16 or 24) to offload fewer layers to GPU.
## Multi-GPU Configuration

```bash
# Ollama distributes layers across multiple GPUs automatically
# Check layer distribution in debug output
OLLAMA_DEBUG=1 ollama run llama3.1:70b 2>&1 | grep "layer"

# Restrict to specific GPUs
CUDA_VISIBLE_DEVICES=0,1,2,3 ollama serve

# Monitor all GPUs during inference
nvidia-smi dmon -s u -d 2
```


```text title="Expected output"
[1] "llm_load_tensors: ggml_cuda_host_alloc: allocated 0 bytes on CPU"
[1] "llm_load_tensors: offloading 48 layers to GPU 0"
[1] "llm_load_tensors: offloading 22 layers to GPU 1"
[1] "llm_load_tensors: layer 0 -> GPU 0 (2048 MB)"
[1] "llm_load_tensors: layer 24 -> GPU 1 (1856 MB)"
[1] "llm_load_tensors: layer 48 -> GPU 0 (2104 MB)"
Listening on 127.0.0.1:11434
#gpu   pid  sm   mem   enc   dec
   0 12847  42  8532     0     0
   1 12847  38  7104     0     0
   2 12847  15  2240     0     0
   3 12847   8   512     0     0
```

!!! warning "Common errors"
    **`CUDA_VISIBLE_DEVICES: command not found`** — Set the environment variable before the command: `CUDA_VISIBLE_DEVICES=0,1,2,3 ollama serve` (not as a separate line).
    **`nvidia-smi: command not found`** — Install NVIDIA GPU drivers and CUDA toolkit; verify with `nvidia-smi` alone first.
    **`Error: could not connect to ollama server`** — Ensure `ollama serve` is running in another terminal before executing inference commands.
## Flash Attention

Enable flash attention for lower VRAM usage and faster inference on supported models:

```bash
OLLAMA_FLASH_ATTENTION=1 ollama serve
```


```text title="Expected output"
time=2024-01-15T09:42:33.847Z level=INFO msg="Starting Ollama server"
time=2024-01-15T09:42:33.912Z level=INFO msg="Listening on 127.0.0.1:11434"
time=2024-01-15T09:42:34.156Z level=INFO msg="Loaded dynamic library /usr/lib/libcuda.so.1"
time=2024-01-15T09:42:34.203Z level=INFO msg="GPU detected: NVIDIA A100 (compute capability 8.0)"
time=2024-01-15T09:42:34.245Z level=INFO msg="Flash Attention enabled for GPU acceleration"
time=2024-01-15T09:42:34.312Z level=INFO msg="VRAM available: 40960 MB"
time=2024-01-15T09:42:34.401Z level=INFO msg="Ollama server ready"
```

!!! warning "Common errors"
    **`error loading CUDA library: libnvml.so.1: cannot open shared object file`** — Install NVIDIA GPU drivers with `sudo apt install nvidia-driver-550` or equivalent for your distribution.
    **`OLLAMA_FLASH_ATTENTION=1: command not found`** — Use `export OLLAMA_FLASH_ATTENTION=1` before running ollama serve, or run as `OLLAMA_FLASH_ATTENTION=1 ollama serve` with proper shell quoting.
    **`listen tcp 127.0.0.1:11434: bind: address already in use`** — Kill the existing ollama process with `pkill ollama` or change the port with `OLLAMA_HOST=127.0.0.1:11435 ollama serve`.
Flash attention reduces the KV cache memory footprint significantly, allowing longer context windows with less VRAM.
