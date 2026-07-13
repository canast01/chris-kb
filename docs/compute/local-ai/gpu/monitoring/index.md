---
tags:
  - gpu
  - ai
  - local-ai
description: "Monitoring GPU workloads requires tracking utilisation, memory, temperature, power draw, and errors. nvidia-smi provides instant snapshots; DCGM provides..."
---
# GPU Monitoring

<div class="kb-summary">
Monitoring GPU workloads requires tracking utilisation, memory, temperature, power draw, and errors. nvidia-smi provides instant snapshots; DCGM provides time-series and health checks for production clusters.
</div>

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "GPU Monitoring \u2014 Thresholds",
    "fontSize": 13,
    "fontWeight": "normal"
  },
  "width": 480,
  "height": {
    "step": 26
  },
  "data": {
    "values": [
      {
        "metric": "GPU utilisation",
        "zone": "Safe",
        "val": 80
      },
      {
        "metric": "GPU utilisation",
        "zone": "Alert",
        "val": 20
      },
      {
        "metric": "Memory utilisation",
        "zone": "Safe",
        "val": 98
      },
      {
        "metric": "Memory utilisation",
        "zone": "Alert",
        "val": 2
      }
    ]
  },
  "mark": {
    "type": "bar",
    "cornerRadiusEnd": 3
  },
  "encoding": {
    "y": {
      "field": "metric",
      "type": "nominal",
      "axis": {
        "title": null,
        "labelLimit": 200
      },
      "sort": null
    },
    "x": {
      "field": "val",
      "type": "quantitative",
      "stack": "normalize",
      "axis": {
        "title": "Threshold boundary",
        "format": ".0%"
      }
    },
    "color": {
      "field": "zone",
      "type": "nominal",
      "scale": {
        "domain": [
          "Safe",
          "Alert"
        ],
        "range": [
          "#15803d",
          "#dc2626"
        ]
      },
      "legend": {
        "title": "Zone"
      }
    },
    "order": {
      "field": "zone",
      "sort": [
        "Safe",
        "Alert"
      ]
    },
    "tooltip": [
      {
        "field": "metric",
        "type": "nominal",
        "title": "Metric"
      },
      {
        "field": "zone",
        "type": "nominal",
        "title": "Zone"
      },
      {
        "field": "val",
        "type": "quantitative",
        "title": "Segment %",
        "format": ".0f"
      }
    ]
  }
}
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


```text title="Expected output"
Wed Dec 18 10:45:32 2024       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.104.05             Driver Version: 535.104.05                |
| GPU  Name                 Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|   0  NVIDIA A100-PCIE-40GB          On | 00:1E.0     Off |                  0 |
| N/A   38C    P0    45W / 250W |   8234MiB / 40960MiB |     12%      Default |
|   1  NVIDIA A100-PCIE-40GB          On | 00:1F.0     Off |                  0 |
| N/A   42C    P0    52W / 250W |  15678MiB / 40960MiB |     28%      Default |
+-----------------------------------------------------------------------------+

gpu   pid  sm   mem   enc   dec   fb  pci rxpci txpci
  0 12847  15    22     0     0 8234  100    12    18
  1 13021  28    38     0     0 15678 100    45    67

gpu   pid  type  fb
  0 12847  C    8234
  1 13021  C    15678

2024/12/18 10:45:32.123, NVIDIA A100-PCIE-40GB, 12, 22, 8234, 32726, 38, 45.2
2024/12/18 10:45:37.456, NVIDIA A100-PCIE-40GB, 28, 38, 15678, 25282, 42, 52.1
```

!!! warning "Common errors"
    **`NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`** — Verify the NVIDIA driver is installed with `nvidia-smi` standalone, or reinstall with `sudo apt install nvidia-driver-535` (adjust version as needed).
    **`No such file or directory: /var/log/gpu_stats.csv`** — Create the log file and ensure write permissions with `sudo touch /var/log/gpu_stats.csv && sudo chmod 666 /var/log/gpu_stats.csv`.
    **`Invalid GPU device id: 0`** — Confirm available GPUs with `nvidia-smi --list-gpus` and adjust the `-i` parameter to a valid device ID.
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


```text title="Expected output"
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  datacenter-gpu-manager
Processing triggers for systemd (249.11-0ubuntu3.6) ...
Created symlink /etc/systemd/system/multi-user.target.wants/nvidia-dcgm.service → /etc/systemd/system/nvidia-dcgm.service.
nvidia-dcgm.service is being started.

GPU 0: NVIDIA A100-PCIE-40GB
Health Status: Healthy

Diag Level 1 (Quick) Results:
  GPU 0: PASS
  Diagnostic Duration: 28.3 seconds

Field ID | Field Name                              | Units
---------|----------------------------------------|----------
1        | GPU_TEMP                               | C
2        | GPU_CLOCK                              | MHz
3        | SM_CLOCK                               | MHz
4        | MEMORY_CLOCK                           | MHz
9        | GPU_POWER_USAGE                        | W
...

3.3.0-3.2.0-ubuntu22.04: Pulling from nvidia/k8s/dcgm-exporter
Digest: sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
Status: Downloaded newer image for nvcr.io/nvidia/k8s/dcgm-exporter:3.3.0-3.2.0-ubuntu22.04
8f4a9c2e1d5b7a3f6e9c2b5d8a1f4e7c9b2d5a8f1e4c7a0d3b6e9f2c5a8d1e4
```

!!! warning "Common errors"
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the command with `sudo` or as root user.
    **`nvidia-dcgm.service is not active, it is inactive.`** — Verify NVIDIA drivers are installed with `nvidia-smi` and check systemd logs with `journalctl -u nvidia-dcgm -n 20`.
    **`docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]].`** — Install NVIDIA Container Toolkit with `distribution=$(. /etc/os-release;echo $ID$VERSION_ID)` and `apt-get install -y nvidia-container-toolkit`, then restart Docker.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: field DCGM_FI_DEV_GPU_TEMP not found`** — Verify DCGM exporter is running and exposing metrics with `curl localhost:9400/metrics | grep DCGM_FI_DEV_GPU_TEMP`.
    **`yaml: line 5: mapping values are not allowed in this context`** — Check indentation is consistent (2 spaces per level) and there are no tabs in the YAML file.