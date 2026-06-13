---
tags:
  - troubleshooting
---
# Ollama Troubleshooting


<div class="kb-summary">
Common Ollama issues include model load failures, slow inference, GPU not being detected, port conflicts, and service startup problems.
</div>
```text
┌──────────────────────── Ai Local Ai Ollama Troubleshooting — Troubleshooting ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Local Ai Ollama troubleshooting: structured diagnostic process for common issues       │   │
│   │         Start with health dashboard, then check recent changes, then review event logs        │   │
│   │        Collect support bundle before contacting vendor support to accelerate resolution       │   │
│   │         Escalation matrix: L1 → L2 → vendor support based on severity and SLA targets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check health → review changes → examine logs → diagnose → resolve                                  │
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
│    Physical: Ai Local Ai Ollama Troubleshooting infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Local Ai Ollama    = Ai Local Ai Ollama Troubleshooting platform overview and core concepts        │
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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
