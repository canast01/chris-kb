# GPU Monitoring


<div class="kb-summary">
Monitoring GPU workloads requires tracking utilisation, memory, temperature, power draw, and errors. nvidia-smi provides instant snapshots; DCGM provides time-series and health checks for production clusters.
</div>
```text
┌───────────────────────────────────── Ai Gpu Workloads Monitoring ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Gpu Workloads: Ai Gpu Workloads Monitoring platform                      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Ai Gpu Workloads Monitoring management console                  │   │
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
│    Physical: Ai Gpu Workloads Monitoring infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Gpu Workloads      = Ai Gpu Workloads Monitoring platform overview and core concepts               │
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


## nvidia-smi Basics

```bash
# Snapshot of all GPUs
nvidia-smi

# Watch mode (refresh every 2 seconds)
nvidia-smi dmon -s pucvmet -d 2

# Key fields: sm% (CUDA core util), mem% (memory util), fb (framebuffer used MB),
# temp (°C), pwr (watts), rxpci/txpci (PCIe bandwidth)

# Per-process GPU memory
nvidia-smi pmon -s m

# Detailed info for GPU 0
nvidia-smi -i 0 -q

# Output as CSV for logging
nvidia-smi --query-gpu=timestamp,name,utilization.gpu,utilization.memory,\
memory.used,memory.free,temperature.gpu,power.draw \
--format=csv,noheader,nounits -l 5 >> /var/log/gpu_stats.csv
```

## Key Metrics to Track

| Metric | `nvidia-smi` Query | Healthy Range | Alert Threshold |
|---|---|---|---|
| GPU utilisation | `utilization.gpu` | 70–100% during work | <20% sustained (idle leak) |
| Memory utilisation | `utilization.memory` | 50–95% | >98% (OOM risk) |
| Temperature | `temperature.gpu` | <80°C | >85°C |
| Power draw | `power.draw` | <TDP | At TDP limit sustained |
| ECC errors | `ecc.errors.corrected.total` | 0 | Any uncorrected |
| PCIe throughput | `pcie.link.gen.current` | Gen 4 x16 | Downgraded link width |

## DCGM for Production Clusters

DCGM (Data Center GPU Manager) provides persistent monitoring, health checks, and Prometheus metrics.

```bash
# Install DCGM (Ubuntu)
apt-get install -y datacenter-gpu-manager

# Start DCGM service
systemctl enable --now nvidia-dcgm

# Run a health check
dcgmi health -g 0 -c

# Diag level 1 (quick): ~30 seconds
dcgmi diag -g 0 -r 1

# List all field IDs available for monitoring
dcgmi dmon --list

# Export Prometheus metrics via dcgm-exporter
docker run -d --gpus all \
  -p 9400:9400 \
  --cap-add SYS_ADMIN \
  nvcr.io/nvidia/k8s/dcgm-exporter:3.3.0-3.2.0-ubuntu22.04
```

## Prometheus + Grafana Stack

```yaml
# prometheus.yml scrape config for dcgm-exporter
scrape_configs:
  - job_name: 'dcgm'
    static_configs:
      - targets: ['gpu-node-1:9400', 'gpu-node-2:9400']
    scrape_interval: 15s
```

Key DCGM Prometheus metrics:

```text
DCGM_FI_DEV_GPU_UTIL           # GPU utilisation %
DCGM_FI_DEV_MEM_COPY_UTIL      # Memory bandwidth utilisation %
DCGM_FI_DEV_FB_USED            # Framebuffer memory used (MiB)
DCGM_FI_DEV_GPU_TEMP           # Temperature (°C)
DCGM_FI_DEV_POWER_USAGE        # Power draw (W)
DCGM_FI_DEV_ECC_DBE_VOL_TOTAL  # Double-bit ECC errors (fatal)
DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL  # NVLink bandwidth
```

## Alerts for GPU Workloads

```bash
# Prometheus alert rules (alerts.yml)
groups:
  - name: gpu_alerts
    rules:
      - alert: GPUHighTemperature
        expr: DCGM_FI_DEV_GPU_TEMP > 85
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "GPU temperature above 85°C on {{ $labels.instance }}"

      - alert: GPUMemoryNearFull
        expr: DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_FREE > 0.95
        for: 1m
        labels:
          severity: critical
```
