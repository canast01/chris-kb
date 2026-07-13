---
tags:
  - troubleshooting
search:
  boost: 1.5
description: "Common Ollama issues include model load failures, slow inference, GPU not being detected, port conflicts, and service startup problems."
---
# Ollama Troubleshooting

<div class="kb-summary">
Common Ollama issues include model load failures, slow inference, GPU not being detected, port conflicts, and service startup problems.

*Applies to: Ollama*
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
checking_ollama_logs: "Checking Ollama Logs" {shape: rectangle}
gpu_not_detected: "GPU Not Detected" {shape: rectangle}
model_load_failures: "Model Load Failures" {shape: rectangle}
slow_inference: "Slow Inference" {shape: rectangle}
port_conflicts: "Port Conflicts" {shape: rectangle}
service_wont_start: "Service Won't Start" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> checking_ollama_logs: investigate
symptom -> gpu_not_detected: investigate
symptom -> model_load_failures: investigate
symptom -> slow_inference: investigate
symptom -> port_conflicts: investigate
symptom -> service_wont_start: investigate
checking_ollama_logs -> resolution
gpu_not_detected -> resolution
model_load_failures -> resolution
slow_inference -> resolution
port_conflicts -> resolution
service_wont_start -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Checking Ollama Logs

```bash
# systemd service logs (most useful first stop)
journalctl -u ollama -n 100 --no-pager

# Follow logs in real time
journalctl -u ollama -f

# Run Ollama in foreground with debug output
systemctl stop ollama
OLLAMA_DEBUG=1 ollama serve
```


```text title="Expected output"
-- Logs begin at Mon 2024-01-15 09:23:14 UTC, end at Mon 2024-01-15 14:47:22 UTC. --
Jan 15 14:47:18 ai-server-01 ollama[2847]: time=2024-01-15T14:47:18.923Z level=INFO msg="Listening on 127.0.0.1:11434"
Jan 15 14:47:15 ai-server-01 ollama[2847]: time=2024-01-15T14:47:15.456Z level=INFO msg="Loaded model mistral:latest (4.1GB)"
Jan 15 14:47:12 ai-server-01 ollama[2847]: time=2024-01-15T14:47:12.234Z level=INFO msg="GPU acceleration enabled: CUDA 12.2"
Jan 15 14:47:08 ai-server-01 ollama[2847]: time=2024-01-15T14:47:08.891Z level=INFO msg="Starting Ollama server"
Jan 15 14:46:55 ai-server-01 systemd[1]: Started Ollama.
Jan 15 14:46:54 ai-server-01 systemd[1]: Starting Ollama...
Jan 15 14:45:22 ai-server-01 ollama[2847]: time=2024-01-15T14:45:22.567Z level=WARN msg="Model cache directory not writable, using /tmp/ollama"
Jan 15 14:45:18 ai-server-01 ollama[2847]: time=2024-01-15T14:45:18.123Z level=INFO msg="Ollama v0.1.28 starting"
Jan 15 14:43:01 ai-server-01 kernel: nvidia-smi: nvidia 550.54.15 loaded
Jan 15 14:42:58 ai-server-01 systemd[1]: Stopped Ollama.
-- following logs --
Jan 15 14:47:22 ai-server-01 ollama[2847]: time=2024-01-15T14:47:22.891Z level=DEBUG msg="Request received" model=mistral tokens=42
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit ollama.service not found.` | Verify the service is installed with `systemctl list-unit-files | grep ollama` and reinstall if missing. |
    | `Failed to start ollama.service: Unit ollama.service is masked.` | Unmask the service with `systemctl unmask ollama` before attempting to stop it. |
    | `error: listen tcp 127.0.0.1:11434: bind: address already in use` | Kill the existing Ollama process with `pkill -f "ollama serve"` or change the port with `OLLAMA_HOST=127.0.0.1:11435 ollama serve`. |
## GPU Not Detected

```bash
# Confirm driver is installed
nvidia-smi

# Check if Ollama detects GPU
OLLAMA_DEBUG=1 ollama run llama3.1:8b "test" 2>&1 | grep -iE "gpu|cuda|device"

# Expected output contains something like:
# msg="detected NVIDIA GPU" id=GPU-xxxx name="NVIDIA GeForce RTX 3080"

# If GPU is missing, check CUDA visibility
echo $CUDA_VISIBLE_DEVICES    # Should be unset or set to valid GPU indices
unset CUDA_VISIBLE_DEVICES
```


```text title="Expected output"
Fri Jan 17 10:45:32 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.90.07              Driver Version: 550.90.07         CUDA Version: 12.4 |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|===========================================================================================|
|   0  NVIDIA GeForce RTX 3080        Off | 00:1F.0        Off   |                  N/A |
| 30%   42C    P2             145W / 320W |   8192MiB / 10240MiB |     65%      Default |
+-----------------------------------------------------------------------------------------+

msg="detected NVIDIA GPU" id=GPU-a1b2c3d4 name="NVIDIA GeForce RTX 3080" vram=10240
msg="CUDA compute capability" major=8 minor=6

(no output — CUDA_VISIBLE_DEVICES is unset)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver` | Reinstall the NVIDIA driver with `sudo apt install --reinstall nvidia-driver-550` and reboot. |
    | `msg="no NVIDIA GPUs detected"` | Verify the GPU is visible with `lspci | grep NVIDIA` and check that CUDA_VISIBLE_DEVICES is not restricting access with `echo $CUDA_VISIBLE_DEVICES`. |
For Docker deployments, ensure `--gpus all` is passed and the NVIDIA Container Toolkit is installed:

```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
apt-get update && apt-get install -y nvidia-container-toolkit
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker
```


```text title="Expected output"
ubuntu2204
gpg: directory '/root/.gnupg' created
gpg: keybox '/root/.gnupg/pubring.kdb' created
deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/ubuntu22.04 / 
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 https://nvidia.github.io/libnvidia-container/ubuntu22.04 InRelease [1247 B]
Get:3 https://nvidia.github.io/libnvidia-container/ubuntu22.04 Packages [3821 B]
Reading package lists... Done
Reading state information... Done
Setting up nvidia-container-toolkit (1.14.3-1) ...
INFO: Wrote updated config to /etc/docker/daemon.json
INFO: Docker runtime configured successfully
docker.service is not active, activating it
docker.service started successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to nvidia.github.io port 443: Connection timed out` | Verify network connectivity and check if the NVIDIA repository is accessible; try again after confirming DNS resolution with `nslookup nvidia.github.io`. |
    | `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)` | Run the entire script with `sudo` or as the root user. |
    | `Error response from daemon: could not select device driver "" with capabilities: [[gpu]]` | Verify NVIDIA GPU is present with `lspci | grep -i nvidia` and ensure the NVIDIA driver is installed with `nvidia-smi`. |
## Model Load Failures

```bash
# Symptom: "error loading model" or model hangs at 0%
# Check available VRAM
nvidia-smi --query-gpu=memory.free --format=csv,noheader

# Try a smaller quantisation
ollama pull llama3.1:8b-instruct-q4_0   # smaller than q4_K_M

# Force CPU-only to rule out GPU issue
OLLAMA_NUM_GPU=0 ollama run llama3.1:8b "test"

# Check model file integrity
ls -lh ~/.ollama/models/blobs/
# Re-pull if a blob is unexpectedly small
ollama pull llama3.1:8b
```


```text title="Expected output"
free                                                 
15360 MiB
pulling manifest
pulling 6a0746a1ec1a... 100% ▕████████████████▏ 4.7 GB
pulling 8f178fafcf1d... 100% ▕████████████████▏ 8.6 MB
pulling 56bb8bd7c55c... 100% ▕████████████████▏ 59 B
pulling 3f8eb801554c... 100% ▕████████████████▏ 483 B
verifying sha256 digest
writing manifest
removing any unused layers
success
>>> test
Loading model...
(no output — model loads and waits for input)
total 18G
-rw-r--r-- 1 user user 4.7G Jan 15 10:23 6a0746a1ec1a2b3c4d5e6f7g8h9i0j1k
-rw-r--r-- 1 user user 8.6M Jan 15 10:24 8f178fafcf1d9e8f7g6h5i4j3k2l1m0n
-rw-r--r-- 1 user user  483B Jan 15 10:24 3f8eb801554c2a1b0c9d8e7f6g5h4i3j
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pull model manifest: not found` | Verify the model name is correct (e.g., `ollama list` to see available models) and check your internet connection. |
    | `CUDA out of memory: tried to allocate X.XXGiB` | Reduce model size further with a lower quantization (e.g., `q3_K_S`) or increase available VRAM by closing other GPU applications. |
    | `connection refused` | Ensure the Ollama daemon is running with `ollama serve` in another terminal before executing `ollama run` commands. |
Common load error causes:

| Error Message | Cause | Fix |
|---|---|---|
| `out of memory` | VRAM insufficient | Use smaller quant, reduce context |
| `model not found` | Tag typo or not pulled | `ollama pull <model>` |
| `unexpected EOF` | Corrupt download | `ollama rm` then re-pull |
| `failed to load model` (no GPU) | Missing CUDA libs | Check driver, restart service |

## Slow Inference

```bash
# Check if model is actually on GPU
curl -s http://localhost:11434/api/ps | jq '.models[].size_vram'
# If size_vram is 0 or very low, model is running on CPU

# Check for CPU throttling (thermal)
cat /proc/cpuinfo | grep "cpu MHz" | head -4

# Check context length — very long contexts slow inference significantly
# Reduce OLLAMA_CONTEXT if not needed
OLLAMA_CONTEXT=2048 ollama run llama3.1:8b "short prompt"
```


```text title="Expected output"
0
0
0
0
cpu MHz		: 2400.000
cpu MHz		: 2400.000
cpu MHz		: 2400.000
cpu MHz		: 2400.000
pulling manifest
pulling 7c4a3c51a89c
pulling 36298d858f47
pulling e0d308ca4a27
pulling 2e0493f5393b
pulling 5f0343b0d42c
verifying sha256 digest
writing manifest
removing any unused layers
success
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to port 11434: Connection refused` | Ensure Ollama service is running with `systemctl start ollama` or `ollama serve` in another terminal. |
    | `jq: parse error: Cannot index number with string "models"` | The API endpoint returned an empty response; verify the model is loaded with `ollama list` and restart with `ollama run <model-name>`. |
    | `Error: model not found` | Pull the model first using `ollama pull llama3.1:8b` before attempting to run it. |
## Port Conflicts

```bash
# Check if port 11434 is already in use
ss -tlnp | grep 11434
lsof -i :11434

# Change Ollama's port
systemctl edit ollama   # or edit the override file directly
# Add: Environment="OLLAMA_HOST=0.0.0.0:11435"
systemctl daemon-reload && systemctl restart ollama
```


```text title="Expected output"
LISTEN    0      4096       127.0.0.1:11434      0.0.0.0:*    users:(("ollama",pid=3847,fd=3))
COMMAND     PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
ollama    3847 root    3u  IPv4  45821      0t0  TCP 127.0.0.1:11434 (LISTEN)

(no output — command completes silently)
(no output — command completes silently)
● ollama.service - Ollama
   Loaded: loaded (/etc/systemd/system/ollama.service; enabled; vendor preset: enabled)
  Drop-in: /etc/systemd/system/ollama.service.d/override.conf
   Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2s ago
     Docs: https://github.com/ollama/ollama
  Process: 3901 ExecStart=/usr/bin/ollama serve (code=exited, status=0/SUCCESS)
 Main PID: 3902 (ollama)
    Tasks: 12 (limit: 4915)
   Memory: 284.3M
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ss: command not found` | Install iproute2 with `apt install iproute2` or `yum install iproute2`. |
    | `Failed to open /etc/systemd/system/ollama.service.d/override.conf: Permission denied` | Run `systemctl edit ollama` with sudo or as root user. |
    | `Job for ollama.service failed because the control process exited with error code` | Verify the OLLAMA_HOST syntax is correct (e.g., `0.0.0.0:11435` without quotes in the Environment line) and check logs with `journalctl -u ollama -n 20`. |
## Service Won't Start

```bash
# Check for permission issues on model directory
ls -la /usr/share/ollama/.ollama/
chown -R ollama:ollama /usr/share/ollama/.ollama/

# Check SELinux/AppArmor
getenforce   # SELinux — if Enforcing, may need policy update
aa-status    # AppArmor

# Verify binary is executable
ls -la /usr/local/bin/ollama
chmod +x /usr/local/bin/ollama

# Check for conflicting processes
ps aux | grep ollama
kill -9 <PID>   # Kill stale process, then restart service
```


```text title="Expected output"
total 48
drwxr-xr-x  5 ollama ollama 4096 Jan 15 10:23 .
drwxr-xr-x  3 root   root   4096 Jan 10 08:45 ..
drwxr-xr-x  2 ollama ollama 4096 Jan 15 10:23 models
-rw-r--r--  1 ollama ollama 2048 Jan 15 10:20 config.json
-rw-r--r--  1 ollama ollama 1024 Jan 15 10:19 cache.db

Enforcing

apparmor module is loaded.
 0 profiles loaded.
 0 profiles in enforce mode.
 0 profiles in complain mode.
 0 processes are unconfined but have a profile defined.

-rwxr-xr-x 1 root root 156284928 Jan 10 08:12 /usr/local/bin/ollama

ollama     1247  0.8  2.3 2847392 189456 ?  Ssl  10:15   0:42 /usr/local/bin/ollama serve
root       3421  0.0  0.0   6408   2304 pts/0 S+   10:31   0:00 grep --color=auto ollama
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `chown: changing ownership of '/usr/share/ollama/.ollama/': No such file or directory` | Create the directory first with `mkdir -p /usr/share/ollama/.ollama/` before running chown. |
    | `getenforce: command not found` | Install SELinux tools with `apt install selinux-utils` on Debian/Ubuntu or `yum install policycoreutils` on RHEL/CentOS. |
    **`Permission denied`** when starting ollama service after chmod — Ensure the ollama user exists with `useradd -r -s /bin/false ollama` and owns the binary's parent directory.
## Connectivity from Remote Hosts

```bash
# Test from a remote host
curl http://<ollama-host-ip>:11434/api/tags

# If unreachable, check firewall
ufw allow 11434/tcp   # Ubuntu
firewall-cmd --add-port=11434/tcp --permanent && firewall-cmd --reload  # RHEL

# Confirm Ollama is listening on 0.0.0.0
ss -tlnp | grep 11434
# Should show 0.0.0.0:11434, not 127.0.0.1:11434
```


```text title="Expected output"
{
  "models": [
    {
      "name": "llama2:latest",
      "modified_at": "2024-01-15T09:32:44.123456789Z",
      "size": 3826087936,
      "digest": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    },
    {
      "name": "mistral:latest",
      "modified_at": "2024-01-14T16:18:22.987654321Z",
      "size": 4109639680,
      "digest": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f"
    }
  ]
}
LISTEN     0      4096      0.0.0.0:11434            0.0.0.0:*        users:(("ollama",pid=2847,fd=3))
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to 192.168.1.50 port 11434: Connection refused` | Verify Ollama is running with `systemctl status ollama` and restart if needed. |
    | `Error: INVALID_ARGUMENT: 'ufw' not found` | Check your firewall tool with `sudo firewall-cmd --version` or `sudo ufw version` and use the appropriate command for your distribution. |
    | `LISTEN     0      4096      127.0.0.1:11434            0.0.0.0:*` | Set `OLLAMA_HOST=0.0.0.0:11434` in `/etc/systemd/system/ollama.service` environment and run `systemctl daemon-reload && systemctl restart ollama`. |
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Cli Reference](../cli-reference/)
- [Gpu Usage](../gpu-usage/)
- [Install Notes](../install-notes/)
- [Models](../models/)
- [Testing](../testing/)
- [Ollama — Overview](../)
