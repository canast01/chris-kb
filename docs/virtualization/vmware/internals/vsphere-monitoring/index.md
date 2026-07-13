---
title: vSphere Monitoring
tags:
  - internals
  - vmware
description: "Reference for vSphere observability. Covers performance chart metrics (CPU Ready, memory balloon, disk latency), log file locations on ESXi and vCenter..."
---

# vSphere Monitoring — Performance, Logs, and Skyline

<div class="kb-summary">
Reference for vSphere observability. Covers performance chart metrics (CPU Ready, memory balloon, disk latency), log file locations on ESXi and vCenter, support bundle collection, vSphere Cluster Services retreat mode, VMware Skyline proactive monitoring, and hands-on tools including ESXTOP, RESXTOP, and PowerCLI Get-Stat.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Performance, Logs, and Skyline \u2014 Thresholds",
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
        "metric": "CPU Usage (%)",
        "zone": "Safe",
        "val": 20
      },
      {
        "metric": "CPU Usage (%)",
        "zone": "Alert",
        "val": 80
      },
      {
        "metric": "CPU Latency (%)",
        "zone": "Safe",
        "val": 95
      },
      {
        "metric": "CPU Latency (%)",
        "zone": "Alert",
        "val": 5
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

## Performance Charts

vCenter performance charts provide metric data for hosts, VMs, clusters, datastores, and networks. Data is available at different time resolutions:

| Chart Type | Interval | Retention | Use Case |
|---|---|---|---|
| **Real-time** | 20 seconds | 1 hour | Active troubleshooting — spot current spikes |
| **Past day** | 5 minutes | 1 day | Review today's trend |
| **Past week** | 30 minutes | 1 week | Identify patterns over days |
| **Past month** | 2 hours | 1 month | Capacity trend analysis |
| **Past year** | 1 day | 1 year | Long-term capacity planning |

**Metric groups available:** CPU, Memory, Disk, Network, Storage I/O (SIOC), Cluster services.

Real-time data is collected in memory on ESXi hosts. When rolled up to vCenter, averages are stored in the vCenter database (vPostgres). If vCenter is unavailable, real-time data is temporarily lost.

---

## CPU Metrics

| Metric | Description | Healthy Threshold | Concern |
|---|---|---|---|
| **CPU Usage (%)** | Percentage of physical CPU capacity consumed | < 80% average | > 90% sustained |
| **CPU Ready (ms)** | Time a vCPU spent ready to run but waiting for a physical core | < 5 ms per 20s interval | > 10 ms = contention |
| **CPU Co-Stop (ms)** | Time an SMP VM's vCPU was paused waiting for co-scheduling (Fault Tolerance) | ~0 for non-FT VMs | Any value in FT VMs = investigate |
| **CPU Swap-Wait (ms)** | Time vCPUs waited for memory being swapped | ~0 | Any value = memory pressure causing CPU stall |
| **CPU Latency (%)** | Percentage of time waiting for scheduling | < 5% | > 10% sustained |

### Understanding CPU Ready

CPU Ready is the most important CPU contention metric. It measures how long a vCPU was in the "ready" state — meaning it was runnable but no physical CPU was available to schedule it.

```bash
# ESXTOP — view CPU Ready (field: %RDY)
esxtop
# Press 'c' for CPU view
# Look at %RDY column per VM world

# In batch mode — collect 10 samples at 5-second intervals
esxtop -b -d 5 -n 10 > /tmp/cpu_stats.csv

# PowerCLI — get CPU Ready metric for a VM
Get-Stat -Entity (Get-VM "web-server-01") \
  -Stat cpu.ready.summation \
  -Start (Get-Date).AddHours(-1) \
  -Interval 20 | Select Timestamp, Value
```


```text title="Expected output"
# esxtop interactive mode (press 'c' for CPU view)
ESXTOP for VMware ESXi 7.0.3 build-19482429 — 14:32:15
GID  NAME                NWLD %USED  %RDY %SYS %WAIT %IDLE
  1  web-server-01        4   18.5   2.3  0.8  1.2  77.2
  2  db-primary-03        8   42.1   5.7  1.1  3.2  48.0
  3  app-cache-02         2    8.9   0.4  0.3  0.1  90.3
  4  monitoring-vm        1   12.4   1.1  0.5  0.8  85.2
  5  backup-staging       6   31.2   4.2  0.9  2.1  61.6

# esxtop batch mode output (first 5 lines of /tmp/cpu_stats.csv)
"GID","NAME","NWLD","%USED","%RDY","%SYS","%WAIT","%IDLE"
1,"web-server-01",4,18.5,2.3,0.8,1.2,77.2
1,"web-server-01",4,19.1,2.8,0.9,1.3,75.9
1,"web-server-01",4,17.8,1.9,0.7,1.1,78.5
1,"web-server-01",4,20.3,3.1,1.0,1.4,74.2
...

# PowerCLI output
Timestamp           Value
---------           -----
2024-01-15 14:32:10 1847
2024-01-15 14:52:10 2156
2024-01-15 15:12:10 1923
2024-01-15 15:32:10 2341
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `esxtop: command not found` | Run esxtop directly on an ESXi host via SSH or vSphere Client console, not from a Windows/Linux management station. |
    | `Get-Stat : The term 'Get-Stat' is not recognized` | Install VMware PowerCLI module with `Install-Module -Name VMware.PowerCLI -Force` and import it via `Import-Module VMware.PowerCLI`. |
    | `Exception calling "AddHours" with "1" argument(s): Object reference not set to an instance of an object.` | Ensure you are connected to vCenter with `Connect-VIServer -Server vcenter.example.com` before running Get-Stat. |
> **VCP-DCV Exam Note:** **CPU Ready threshold is typically > 10 ms per 20-second interval** (or expressed as > 5% in some older references). CPU Ready is caused by too many vCPUs competing for too few physical cores — common with over-provisioned VMs. The fix is to reduce the number of vCPUs on VMs that don't need them, not to add more hosts. **CPU Co-Stop** is specific to Fault Tolerance VMs — it measures synchronization pauses between primary and secondary VMs.

---

## Memory Metrics

| Metric | Description | What It Indicates |
|---|---|---|
| **Active** | Memory the guest OS is actively reading/writing | True working set size |
| **Consumed** | Physical memory allocated and backed by RAM (includes shared) | Actual host RAM in use |
| **Balloon** | Memory reclaimed by the balloon driver (vmmemctl) | Host is memory-pressured; guest is being asked to give back pages |
| **Swap (In/Out)** | Memory swapped to the .vswp file on disk | Severe memory pressure — expect significant performance degradation |
| **Compressed** | Memory compressed into the memory compression cache | Moderate pressure; less severe than swapping |
| **Overhead** | VMkernel overhead per VM | Fixed cost per VM for VMX process and virtualization structures |

### Balloon Driver Operation

When a host runs low on physical memory, the VMkernel inflates the **balloon driver** (vmmemctl) inside the guest OS. The balloon driver allocates guest OS memory pages and holds them — forcing the guest OS to use its own memory management (paging) to reclaim pages. The VMkernel then reclaims those physical pages for other VMs.

Balloon is preferred over swapping because guest-side paging is more intelligent (the guest knows which pages are truly idle) than VMkernel-level swapping.

Memory reclamation priority order (from least to most disruptive):
1. **TPS (Transparent Page Sharing)** — deduplicate identical memory pages across VMs
2. **Balloon** — ask the guest to free memory via balloon driver
3. **Compression** — compress pages into memory compression cache
4. **Swap** — write pages to .vswp disk file (most disruptive)

```bash
# ESXTOP — view memory metrics (press 'm')
esxtop
# Key columns: MCTLSZ (balloon size MB), SWPWRT/SWPRD (swap activity)

# PowerCLI — get balloon metric
Get-Stat -Entity (Get-VMHost "esxi01.corp.local") \
  -Stat mem.vmmemctl.average \
  -Start (Get-Date).AddHours(-2) \
  -Interval 300
```


```text title="Expected output"
Loaded plugin 'vsanObserver'
ESXTOP started — press 'm' for memory view
GID  NAME             MCTLSZ  SWPWRT  SWPRD  TCHD   NCHD   PSHP   SHPS
  1  VM-web-01        512.0   0.0     0.0    4096   2048   1024   512
  2  VM-db-prod       2048.5  128.3   64.1   8192   6144   2560   1280
  3  VM-app-cache     256.2   0.0     0.0    2048   1024   512    256
  4  VM-backup        1024.1  256.7   192.4  4096   3072   1536   768

Timestamp                     Entity         Metric                 Value
---------                     ------         ------                 -----
2024-01-15 14:32:00 -05:00    esxi01.corp... mem.vmmemctl.average   384.50
2024-01-15 14:37:00 -05:00    esxi01.corp... mem.vmmemctl.average   412.25
2024-01-15 14:42:00 -05:00    esxi01.corp... mem.vmmemctl.average   398.75
2024-01-15 14:47:00 -05:00    esxi01.corp... mem.vmmemctl.average   425.10
2024-01-15 14:52:00 -05:00    esxi01.corp... mem.vmmemctl.average   441.80
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connect-VIServer : The underlying connection was closed: Could not establish trust relationship for the SSL/TLS secure channel.` | Add `-SkipCertificateCheck` parameter or import the vCenter certificate into PowerCLI's certificate store. |
    | `Get-Stat : Cannot bind argument to parameter 'Entity' because it is null.` | Verify the ESXi hostname matches exactly and the vCenter account has permissions to query that host. |
> **VCP-DCV Exam Note:** Know what each memory metric means and the reclamation order. **Balloon** means the VMkernel is asking guests to return memory. **Swap** means memory is being written to disk — this indicates severe pressure and will cause noticeable VM performance degradation. **Active memory** is the most accurate measure of a VM's true memory need — a VM with 8 GB allocated but only 500 MB active is a candidate for reclamation.

---

## Disk and Network Metrics

### Disk Latency Metrics

| Metric | Description | Healthy | Concern |
|---|---|---|---|
| **DAVG (Device Average Latency)** | Latency in the storage device (array or disk) — time from HBA to device acknowledgment | < 10 ms | > 20 ms |
| **KAVG (Kernel Average Latency)** | Latency in the VMkernel storage stack (queueing in the kernel) | < 2 ms | > 4 ms |
| **GAVG (Guest Average Latency)** | Total latency seen by the guest OS (DAVG + KAVG) | < 15 ms | > 25 ms |

**Interpretation:**
- High DAVG, low KAVG → problem is in the storage array or fabric
- High KAVG, low DAVG → problem is VMkernel queuing (queue depth, too many concurrent I/Os)
- High GAVG with both DAVG and KAVG normal → investigate in-guest I/O patterns

```bash
# ESXTOP — view disk metrics (press 'u' for storage adapter, 'd' for disk)
esxtop
# DAVG, KAVG, GAVG visible in disk device view

# esxcli — check storage path latency
esxcli storage core device stats get --device naa.xxxxxx
```


```text title="Expected output"
# ESXTOP — view disk metrics (press 'u' for storage adapter, 'd' for disk)
esxtop
(esxtop interactive terminal interface launches — real-time monitoring display with columns: DAVG, KAVG, GAVG, CMDS/s, MB/s)

# esxcli — check storage path latency
esxcli storage core device stats get --device naa.6001405abcdef1234567890123456789
Device naa.6001405abcdef1234567890123456789 Statistics:
  Read Commands: 45821
  Write Commands: 12340
  Read Bytes: 2147483648
  Write Bytes: 536870912
  Read Latency (us): 1240
  Write Latency (us): 890
  IOPS: 1523
  Throughput (MB/s): 287.4
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown device naa.xxxxxx` | Replace `naa.xxxxxx` with the actual NAA identifier from `esxcli storage core device list`. |
    | `Error: esxtop: command not found` | Ensure you are connected directly to an ESXi host via SSH or console; esxtop only runs on ESXi, not vCenter. |
### Network Metrics

| Metric | Description | Concern |
|---|---|---|
| **Received/Transmitted (KBps)** | Network throughput per VM or vmk adapter | Near NIC saturation |
| **Dropped Rx/Tx (packets)** | Packets dropped due to buffer overflow | Any sustained drop rate |
| **Packets Received/Transmitted** | Packet rate — useful for PPS-sensitive workloads | Context-dependent |

Dropped packets on receive (Rx) indicate the VM or host cannot consume packets fast enough. Dropped packets on transmit (Tx) indicate the uplink is saturated.

---

## Log Files

### ESXi Key Logs

| Log File | Location | Contents |
|---|---|---|
| **vmkernel.log** | `/var/log/vmkernel.log` | Core VMkernel messages — storage, networking, hardware events |
| **vmkwarning.log** | `/var/log/vmkwarning.log` | Warning-level VMkernel messages only |
| **vobd.log** | `/var/log/vobd.log` | VMkernel observation daemon — hardware observation events (CIM) |
| **hostd.log** | `/var/log/hostd.log` | Host daemon — all host management operations via vCenter or direct API |
| **vpxa.log** | `/var/log/vpxa.log` | vCenter agent on ESXi — communication with vCenter |
| **fdm.log** | `/var/log/fdm.log` | Fault Domain Manager — vSphere HA agent events |
| **storageRM.log** | `/var/log/storageRM.log` | Storage Resource Manager — SIOC events |
| **shell.log** | `/var/log/shell.log` | ESXi Shell (SSH) command history |
| **auth.log** | `/var/log/auth.log` | Authentication events — login/logout, sudo |
| **syslog.log** | `/var/log/syslog.log` | General syslog output |

### vCenter Key Logs

| Log File | Location | Contents |
|---|---|---|
| **vpxd.log** | `/var/log/vmware/vpxd/vpxd.log` | Main vCenter service log — all vCenter operations |
| **vcsservicemanager.log** | `/var/log/vmware/vcsservicemanager.log` | vCenter service manager — service start/stop, dependency management |
| **sso/vmware-sts-idmd.log** | `/var/log/vmware/sso/` | SSO identity management — login, token, federation events |
| **eam/eam.log** | `/var/log/vmware/eam/eam.log` | ESX Agent Manager — vCLS agent VM management |
| **content-library/cls.log** | `/var/log/vmware/content-library/` | Content Library service events |

> **VCP-DCV Exam Note:** Key log file associations to memorize: **fdm.log → vSphere HA**. **vpxa.log → ESXi-to-vCenter agent communication**. **vpxd.log → vCenter main service**. **vobd.log → hardware events via CIM**. These are common exam targets. On ESXi, most logs are in `/var/log/`. On VCSA, most vCenter-specific logs are in `/var/log/vmware/`.

```bash
# View recent HA events on an ESXi host
tail -f /var/log/fdm.log

# Filter for storage errors in vmkernel log
grep -i "error\|fail" /var/log/vmkernel.log | tail -50

# View hostd log for specific VM operations
grep "web-server-01" /var/log/hostd.log | tail -30

# List services and their status on ESXi
esxcli system process list | grep -i log
```


```text title="Expected output"
2024-01-15T14:32:18.045Z [7F4A2C1B] HA: Received heartbeat from host-02.lab.local (10.20.30.45)
2024-01-15T14:32:22.112Z [7F4A2C1C] HA: Master election in progress, candidate host-01.lab.local
2024-01-15T14:32:25.891Z [7F4A2C1D] HA: Cluster reconfiguration completed, 4 hosts active
2024-01-15T14:32:31.456Z [7F4A2C1E] HA: Heartbeat timeout from host-03.lab.local, isolation detected
2024-01-15T14:32:35.223Z [7F4A2C1F] HA: VM restart initiated for prod-db-01 on host-01.lab.local
^C

2024-01-15T10:15:42.123Z cpu0:2048)WARNING: NFS: NFS server 10.50.60.10 not responding
2024-01-15T10:16:01.456Z cpu1:2049)ERROR: ScsiDeviceIO: Command 0x28 failed: H:0x0 D:0x2 P:0x0
2024-01-15T10:16:15.789Z cpu2:2050)WARNING: VMFS: Heartbeat failed on volume datastore-03
2024-01-15T10:16:28.234Z cpu0:2051)ERROR: PSA: Path failover initiated for device naa.60000000000000001
2024-01-15T10:16:42.567Z cpu3:2052)FAIL: iSCSI session timeout to target iqn.2020-01.local:storage-01
...

2024-01-15T09:45:12.234Z [hostd.pl] web-server-01: VM power on initiated by admin@vsphere.local
2024-01-15T09:45:15.567Z [hostd.pl] web-server-01: CPU reservation 4000 MHz allocated
2024-01-15T09:45:18.891Z [hostd.pl] web-server-01: Memory reservation 8192 MB allocated
2024-01-15T09:45:22.123Z [hostd.pl] web-server-01: vNIC 0 connected to vSwitch0
2024-01-15T09:45:25.456Z [hostd.pl] web-server-01: VM power on completed successfully
...

   PID    Name                                   World ID Busy CPU Sys CPU
  2048    vmkernel                                    1    0.0%   0.0%
  2156    hostd                                    2048    1.2%   0.8%
  2234    vpxa                                     2049    0.5%   0.3%
  2312    syslog                                   2050    0.1%   0.0%
  2401    vobd                                     2051    0.3%   0.2%
  2489    wsman                                    2052    0.2%   0.1%
```

!!! warning "Common errors"
    **`tail
---

## Log Bundle Generation

### ESXi Support Bundle

```bash
# Generate support bundle from ESXi CLI (creates .tgz in /var/tmp)
vm-support

# Generate and specify output location
vm-support -w /vmfs/volumes/datastore1/

# From vCenter UI: Host → Monitor → Support → Export System Logs
# This calls vm-support remotely and downloads the bundle

# Using vim-cmd
vim-cmd hostsvc/advopt/view | grep diagnostic

# Alternative — use the ESXi DCUI or direct SSH
ssh root@esxi01.corp.local "vm-support" && \
  scp root@esxi01.corp.local:/var/tmp/esx-*.tgz .
```


```text title="Expected output"
Generating support bundle, this may take a few minutes...
Collecting system logs...
Collecting system state information...
Collecting sar data...
Collecting disk information...
Collecting network information...
Support bundle completed successfully.
Bundle location: /var/tmp/esx-esxi01-2024-01-15-14-32-45.tgz
Bundle size: 287 MB

diagnostic.coreMaxSize = "110"
diagnostic.coreMaxFiles = "100"
diagnostic.enableFencingClockHosts = "true"
diagnostic.heapMaxSize = "512"

esx-esxi01-2024-01-15-14-32-45.tgz                    100%  287MB   4.2MB/s   01:08
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vm-support: error: insufficient space on /var/tmp` | Specify an alternate writable datastore path with `-w /vmfs/volumes/datastore_name/` or free space on the host. |
    | `Permission denied (publickey,password).` | Ensure SSH is enabled on the ESXi host and root credentials are correct; verify firewall rules allow port 22 inbound. |
    | `vim-cmd: Unknown command` | Run the command from the ESXi shell directly (not from vCenter); if using vCenter, use `esxcli system syslog config get` instead. |
### VCSA Support Bundle

```bash
# From VAMI (port 5480): Administration → Support → Create Support Bundle
# Download from the VAMI browser interface after generation

# From VCSA API
curl -X POST \
  "https://vcenter.corp.local/api/appliance/support-bundle" \
  -H "vmware-api-session-id: <session-token>"

# From VCSA shell
vc-support.sh
# Output: /var/tmp/vc-support-*.tgz
```


```text title="Expected output"
% curl -X POST \
  "https://vcenter.corp.local/api/vcenter/support-bundle" \
  -H "vmware-api-session-id: 52b20672-3dcc-4a00-8000-000000000001"
{
  "value": "support-bundle-vcenter.corp.local-2024.01.15-14.32.45.tgz",
  "status": "RUNNING"
}

% vc-support.sh
Generating support bundle for vCenter Server 8.0.1.00000...
Collecting system logs...
Collecting vCenter services status...
Collecting database information...
Collecting network configuration...
Support bundle created: /var/tmp/vc-support-2024.01.15-14.32.45.tgz
Bundle size: 487 MB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification, or use the FQDN that matches the certificate CN. |
    | `HTTP/1.1 401 Unauthorized` | Ensure the session token is valid and not expired; obtain a fresh token via `/api/session` endpoint with valid vCenter credentials. |
    | `vc-support.sh: command not found` | Run the command from the vCenter shell (SSH to VCSA) or use the full path `/usr/lib/vmware-vmafd/bin/vc-support.sh`. |
---

## vSphere Cluster Services (vCLS) Retreat Mode

**vSphere Cluster Services (vCLS)** are agent VMs that vCenter automatically deploys into clusters to maintain DRS and HA functionality. Even if vCenter becomes unavailable, vCLS agent VMs keep cluster services running.

Under normal operation, vCenter deploys 3 vCLS agent VMs per cluster (1 for small clusters). These VMs are managed by vCenter and cannot be manually deleted — vCenter recreates them automatically.

### Retreat Mode

**Retreat mode** temporarily disables vCLS and removes the agent VMs from a cluster. This is used exclusively for troubleshooting scenarios where vCLS VMs are causing problems (e.g., interfering with maintenance, consuming resources in a resource-constrained environment during troubleshooting).

**Enabling retreat mode (per cluster):**
```bash
# Find the cluster's MoRef ID
# From PowerCLI:
$cluster = Get-Cluster "Production-Cluster"
$cluster.ExtensionData.MoRef.Value
# Example output: domain-c123

# Enable retreat mode by modifying cluster advanced setting
# vCenter UI: Cluster → Configure → vSphere Cluster Service → Retreat Mode
# Or via API — set config.retreatMode = true on the cluster

# PowerCLI approach
$clusterView = Get-View $cluster
$spec = New-Object VMware.Vim.ClusterConfigSpecEx
# retreatMode is set via cluster configuration API
```


```text title="Expected output"
domain-c123
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Get-Cluster : The term 'Get-Cluster' is not recognized as the name of a cmdlet, function, script file, or operable program.` | Load the VMware PowerCLI module first with `Import-Module VMware.PowerCLI`. |
    | `You do not have permission to perform this operation.` | Ensure your vCenter user account has Administrator or Cluster Administrator role on the target cluster. |
**Impact of retreat mode:**
- vCLS agent VMs are powered off and removed
- **DRS enters manual mode** — automated load balancing stops
- **HA Optimal Placement is disabled** — HA can still restart VMs but without optimized placement
- vCenter-level cluster health checks are affected

> **VCP-DCV Exam Note:** The most common exam question about vCLS retreat mode asks about its **impact on HA**. The correct answer is that **HA Optimal Placement is disabled** when retreat mode is active — HA can still function and restart VMs, but optimal placement decisions require vCLS. Retreat mode is not a permanent setting and should only be used temporarily for troubleshooting.

---

## VMware Skyline

**VMware Skyline** is VMware's proactive support and monitoring platform. It collects telemetry data from vSphere environments and analyzes it against known issue signatures, security advisories, and best practices.

### What Skyline Does

| Capability | Description |
|---|---|
| **Proactive monitoring** | Continuous collection of vSphere telemetry — configurations, logs, performance data |
| **Health checks** | Validates environment against VMware-defined health rules |
| **Advisory recommendations** | Surfaces known issues before they become outages |
| **Security advisories** | Alerts when installed versions have known CVEs |
| **Support acceleration** | Pre-populates support tickets with environment context when you open a case |

### Skyline Advisor Pro

Skyline Advisor Pro is the enhanced tier offering:
- Custom health checks per environment
- Integration with your support contract
- API access for automation
- Trending analysis and executive-level reporting

### Configuring Skyline Data Collection

```bash
# Skyline Collector is a virtual appliance deployed in your environment
# Configuration is done via the Skyline Collector VAMI (port 5480)

# Verify Skyline Collector connectivity to VMware cloud endpoints
curl -sk https://sc-collector.vmware.com/ping

# PowerCLI — check if Skyline health is enabled
(Get-View ServiceInstance).Content.Health
```


```text title="Expected output"
{"status":"pong","timestamp":"2024-01-15T09:42:33Z","collector_id":"sc-collector-prod-us-west-2","version":"8.7.2"}

HealthSystemManager
Key                 Value
---                 -----
systemHealthManager HealthSystemManager
numericSensorInfo   {NumericSensorInfo, NumericSensorInfo, NumericSensorInfo...}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag (already present) or import the collector's CA certificate into your system trust store. |
    | `The term 'Get-View' is not recognized as the name of a cmdlet, function, script file, or operable program.` | Load the VMware.VimAutomation.Core PowerCLI module with `Import-Module VMware.VimAutomation.Core` before running Get-View commands. |
    | `Unable to connect to the remote server` | Verify the Skyline Collector appliance is running and accessible on the network; check firewall rules and DNS resolution for sc-collector.vmware.com. |
### Relationship to Aria Operations

VMware Aria Operations (formerly vRealize Operations) and Skyline serve different purposes:
- **Skyline** — vendor-managed proactive support; VMware analyzes your telemetry against their global knowledge base
- **Aria Operations** — customer-managed performance and capacity management; you define policies and thresholds; runs in your environment or as SaaS

---

## Performance Monitoring Tools

### ESXTOP

ESXTOP is the primary real-time performance tool for ESXi hosts. It runs interactively via SSH or in batch mode for data collection.

| ESXTOP View | Key | Important Columns |
|---|---|---|
| CPU | c | %USED, %RDY, %CSTP, %MLMTD |
| Memory | m | MEMSZ, MCTLSZ (balloon), SWPWRT, SWPRD |
| Network | n | MbRX/s, MbTX/s, DRPRX/s, DRPTX/s |
| Disk/Storage Adapter | u | CMDS/s, DAVG, KAVG |
| Disk Device | d | DAVG/cmd, KAVG/cmd, GAVG/cmd |
| Virtual Disk | v | RDLATENCY, WRLATENCY |
| Power | p | PCPU power states |

```bash
# Interactive ESXTOP
esxtop

# Batch mode — 30 samples at 2-second intervals, write to CSV
esxtop -b -d 2 -n 30 > /tmp/perf_data.csv

# Replay mode — analyze a previously captured batch file
esxtop -R /tmp/perf_data.csv

# Filter to specific VM (useful in busy environments)
esxtop   # then press 'e' to expand, search by VM name
```


```text title="Expected output"
Batch mode output (esxtop -b -d 2 -n 30 > /tmp/perf_data.csv):
(no output — command completes silently)

Replay mode output (esxtop -R /tmp/perf_data.csv):
ESXTOP REPLAY MODE
Replaying from: /tmp/perf_data.csv
Sample 1 of 30 (timestamp: 2024-01-15T14:32:45Z)
  CPU%USED: 18.5  MEM%USED: 62.3  DISK RD: 1245 MB/s  DISK WR: 342 MB/s
  VM: prod-web-01  CPU: 12.3%  MEM: 4096 MB  READY: 2.1%
  VM: prod-db-02   CPU: 5.2%   MEM: 8192 MB  READY: 0.8%
  VM: test-app-03  CPU: 0.9%   MEM: 2048 MB  READY: 0.1%
Sample 2 of 30 (timestamp: 2024-01-15T14:32:47Z)
  CPU%USED: 19.1  MEM%USED: 62.5  DISK RD: 1267 MB/s  DISK WR: 358 MB/s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Cannot open batch file /tmp/perf_data.csv` | Verify the batch file exists and was created successfully with `ls -la /tmp/perf_data.csv`. |
    | `Error: esxtop: command not found` | Run esxtop directly on an ESXi host via SSH or vSphere console, not from a remote management station. |
    | `Error: Permission denied writing to /tmp/perf_data.csv` | Ensure the user running esxtop has write permissions to /tmp or specify an alternative writable directory. |
### RESXTOP

RESXTOP is ESXTOP accessed remotely without SSH, using the vSphere CLI. It connects to a host via the vSphere API and presents the same interface as ESXTOP.

```bash
# RESXTOP from a remote system with vSphere CLI installed
resxtop --server esxi01.corp.local --username root

# Batch mode collection remotely
resxtop --server esxi01.corp.local --batch output.csv --samples 30 --interval 5
```


```text title="Expected output"
Connected to esxi01.corp.local
Authenticating as root...
Authentication successful.

RESXTOP 7.0.3 build-19482429
Press 'q' to quit, 'h' for help

   PCPU USED(%): 12.45  PCPU RUN QUEUE: 2.3
   MEMORY USAGE(%): 68.92  SWAP USED(MB): 0
   DISK READ(MB/s): 45.23  DISK WRITE(MB/s): 12.67
   NET RECV(Mbps): 234.5  NET XMIT(Mbps): 89.3

Sample 1/30 collected at 2024-01-15 14:32:18
Sample 2/30 collected at 2024-01-15 14:32:23
Sample 3/30 collected at 2024-01-15 14:32:28
...
Sample 30/30 collected at 2024-01-15 14:34:13
Data written to output.csv
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unable to connect to host esxi01.corp.local on port 443` | Verify the ESXi hostname is resolvable and accessible, and check firewall rules for port 443. |
    | `Error: Authentication failed for user root` | Confirm the root password is correct and the account is not locked; use `--password` flag or enter interactively when prompted. |
    | `Error: resxtop: command not found` | Install the vSphere CLI package (e.g., `apt-get install vmware-vsphere-cli` on Linux or download from VMware) and ensure it is in your PATH. |
### PowerCLI Get-Stat

```bash
# Get CPU Ready for a VM over the last hour (20s intervals)
Get-Stat -Entity (Get-VM "db-server-01") \
  -Stat cpu.ready.summation \
  -Start (Get-Date).AddHours(-1) \
  -Interval 20 | Measure-Object Value -Average -Maximum

# Get memory balloon for all hosts in a cluster
Get-VMHost -Location (Get-Cluster "Production-Cluster") | ForEach-Object {
  Get-Stat -Entity $_ -Stat mem.vmmemctl.average \
    -Start (Get-Date).AddHours(-1) -Interval 300
} | Select EntityId, Timestamp, Value | Sort-Object Value -Descending

# Get disk DAVG for a datastore
Get-Stat -Entity (Get-Datastore "vSAN-Datastore") \
  -Stat datastore.totalReadLatency.average \
  -Start (Get-Date).AddHours(-4) -Interval 300
```


```text title="Expected output"
Count             : 180
Average           : 1247.33
Maximum           : 8934

EntityId                             Timestamp            Value
--------                             ---------            -----
HostSystem-host-42                   2024-01-15 14:32:00  2847.5
HostSystem-host-38                   2024-01-15 14:27:00  1923.2
HostSystem-host-41                   2024-01-15 14:22:00  1456.8
HostSystem-host-39                   2024-01-15 14:17:00   892.3
HostSystem-host-40                   2024-01-15 14:12:00   445.1

Timestamp            Value
---------            -----
2024-01-15 14:45:30  3.847
2024-01-15 14:40:30  3.621
2024-01-15 14:35:30  2.934
2024-01-15 14:30:30  2.156
2024-01-15 14:25:30  1.823
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Get-VM : The term 'Get-VM' is not recognized` | Load the VMware PowerCLI module with `Import-Module VMware.VimAutomation.Core` before running these commands. |
    | `You are not currently connected to any vCenter servers` | Connect to vCenter first using `Connect-VIServer -Server <vcenter-fqdn>` with appropriate credentials. |
    | `Get-Stat : A parameter cannot be found that matches parameter name 'Interval'` | Use `-IntervalSecs` instead of `-Interval` for the time period in seconds. |
### Key Metrics Summary Table

| Metric | Tool | Threshold | Action If Exceeded |
|---|---|---|---|
| CPU Ready | ESXTOP %RDY, vCenter charts | > 10 ms / 20s interval | Reduce vCPU count, add hosts |
| CPU Co-Stop | ESXTOP %CSTP | > 0 on FT VMs | Review FT secondary placement |
| Memory Balloon | ESXTOP MCTLSZ, mem.vmmemctl | Any sustained value | Add RAM to host, reduce VM allocation |
| Memory Swap Write | ESXTOP SWPWRT | > 0 | Immediate attention — add RAM |
| Disk DAVG | ESXTOP disk view | > 20 ms | Array performance investigation |
| Disk KAVG | ESXTOP disk view | > 4 ms | Reduce VMkernel queue depth |
| Network Dropped Rx | ESXTOP DRPRX/s | > 0 sustained | Increase VM network buffer, check NIC saturation |

---

## Related Pages

- [vSphere Networking Concepts](../vsphere-networking/)
- [Cluster Services — DRS, HA, and vSAN](../cluster-services/)
- [vSphere Lifecycle Management](../vsphere-lifecycle/)
- [ESXi Troubleshooting](../../products/esxi/)
- [Aria Operations](../../products/aria-operations/)
