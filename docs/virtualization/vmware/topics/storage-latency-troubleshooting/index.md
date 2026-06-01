# Storage Latency Troubleshooting (VMware)


<div class="kb-summary">
Storage Latency Troubleshooting (VMware) reference covering Latency Thresholds, Step 1: Identify Affected VMs and Datastores, Step 2: Check Storage Paths, Step 3: Check for vSAN Resync or Rebuild, Step 4: Queue Depth and Congestion and 3 more sections.
</div>
```text
┌──────────────────────────────────── Virtualization Vmware Topics ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Vmware: Virtualization Vmware Topics platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Virtualization Vmware Topics management console                  │   │
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
│    Physical: Virtualization Vmware Topics infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Topics platform overview and core concepts              │
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


## Latency Thresholds

| Latency | State | Action |
|---|---|---|
| < 5 ms | Excellent | No action |
| 5–10 ms | Normal | No action |
| 10–20 ms | Warning | Monitor; identify source |
| 20–50 ms | Problem | Investigate immediately |
| > 50 ms | Severe | Application timeouts expected — escalate |

## Step 1: Identify Affected VMs and Datastores

```powershell
# Datastores with low free space (often correlates with high latency)
Get-Datastore | Select-Object Name,
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="UsedPct";E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}} |
    Sort-Object UsedPct -Descending

# VMs with snapshots (delta VMDKs increase read latency)
Get-VM | Get-Snapshot | Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB,2)}}
```

## Step 2: Check Storage Paths

```bash
# Path states on the ESXi host
esxcli storage core path list | grep -E "State:|Device:|Adapter:"

# Dead paths (need recovery or failover)
esxcli storage core path list | grep "State: dead"

# Confirm active path count per device
esxcli storage nmp path list | grep -E "Active|Device"

# Current PSP (Path Selection Policy)
esxcli storage nmp device list | grep -E "Device:|PSP:"
```

## Step 3: Check for vSAN Resync or Rebuild

vSAN resync heavily consumes storage backend IOPS:

```bash
# Active resync (if running — latency will be elevated)
esxcli vsan debug resync list

# Resync byte count (estimate duration)
esxcli vsan debug resync list | grep -E "Total Bytes|Remaining"

# Check if objects are degraded
esxcli vsan debug object list | grep -v healthy
```

## Step 4: Queue Depth and Congestion

```bash
# Device queue depth
esxcli storage core device list | grep "Queue Full Threshold"

# Check if devices are hitting queue full
grep -i "queue full\|queue depth\|SCSI cmd abort" /var/log/vmkernel.log | tail -20

# Adjust queue depth for a specific device (requires reboot to persist)
esxcli storage core device set --device <naa.xxx> -O MaxQueueDepth=32
```

## Step 5: Datastores on the Same LUN/Volume

Multiple datastores sharing an underlying volume compete for IOPS:

```bash
# LUN to device mapping
esxcli storage core device list | grep -E "naa\.|Device Display"

# Check VAAI support (helps with copy offload and ATS locking)
esxcli storage core device vaai status get -d <naa.xxx>
```

## Step 6: esxtop Storage Analysis

```bash
# Launch esxtop, switch to storage view
esxtop
# Press 'u' for device view
# Key columns: DAVG/cmd (device latency), KAVG/cmd (kernel latency), QAVG/cmd (queue latency)
# DAVG > 10ms = storage backend issue
# KAVG > 2ms  = host-side queuing issue
```

## Common Causes Reference

| Cause | Indicator | Fix |
|---|---|---|
| vSAN resync | `resync list` shows bytes remaining | Wait for completion; avoid additional disk removal |
| Snapshot chain | Delta VMDK in `ls -lah` is large | Remove/consolidate snapshots |
| Dead paths | `path list` shows dead state | Rescan adapters; check physical SAN connectivity |
| Queue depth saturation | vmkernel.log "queue full" | Reduce queue depth per device or balance VMs |
| Storage array overload | DAVG high on all VMs | Redistribute VMs; check array CPU/cache hit rate |
| All-Paths-Down (APD) | APD in vmkernel.log | Recover connectivity; check SAN zoning and HBAs |
| Thin provisioning overcommit | Datastore > 90% used | Add capacity immediately — thin disks can pause on overcommit |
