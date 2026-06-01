# ESXi Diagnostics

```text
ESXi Diagnostic Data Sources
┌──────────────────────────────────────────────────────────┐
│  vSphere Client (GUI)                                    │
│  ├── Host → Monitor → Issues & Alarms                    │
│  ├── Host → Monitor → Tasks (recent task failures)       │
│  └── Host → Monitor → Performance (CPU, mem, storage)    │
├──────────────────────────────────────────────────────────┤
│  ESXi Shell / SSH (CLI)                                  │
│  ├── /var/log/vmkernel.log  storage, network, drivers    │
│  ├── /var/log/hostd.log     API, VM ops, config          │
│  ├── /var/log/vpxa.log      vCenter agent comms          │
│  ├── /var/log/fdm.log       HA / Fault Domain Manager    │
│  ├── /var/log/auth.log      SSH logins, PAM failures     │
│  └── esxtop                 interactive real-time perf   │
│      c=CPU  m=Mem  d=Disk  n=Net                         │
├──────────────────────────────────────────────────────────┤
│  Support Bundle                                          │
│  └── vm-support -w /tmp/                                 │
│      Includes all logs + config + network + storage state│
├──────────────────────────────────────────────────────────┤
│  Key Performance Thresholds                              │
│  ├── CPU Ready    < 5%    │ > 10% → investigate          │
│  ├── Mem Balloon  ~0      │ Growing → monitor            │
│  ├── Mem Swap     = 0     │ > 0 → urgent                 │
│  └── DS Latency   < 10ms  │ > 20ms → investigate         │
└──────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────────── ESXi — Diagnostics ──────────────────────────────────────────┐
│                                                                                                       │
│  Log file locations, esxcli diagnostic commands, and support bundle collection.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Key Log Files                 │  │          esxcli Diagnostic Commands         │   │
│   │            /var/log/vmkernel.log             │  │             esxcli system stats             │   │
│   │              /var/log/hostd.log              │  │           esxcli network stat get           │   │
│   │              /var/log/vpxa.log               │  │           esxcli storage core path          │   │
│   │            /var/log/fdm.log (HA)             │  │            esxcli vm process list           │   │
│   │            /scratch/log (SD/USB)             │  │            esxcli system process            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Logs → esxcli live state → esxtop performance → support bundle for GSS.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              esxtop Performance              │  │                Support Bundle               │   │
│   │            esxtop interactive TUI            │  │          vm-support -w /tmp/bundle          │   │
│   │             c=CPU, m=mem, d=disk             │  │           vCenter: Export Support           │   │
│   │            n=network, i=interrupt            │  │           Includes logs + configs           │   │
│   │             batch mode: -b -n 5              │  │             Upload to VMware SR             │   │
│   │             DAVG > 25ms = issue              │  │             Keep for 30 days min            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 hosts, SAN/NAS storage, management network, syslog server for logs                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vmkernel.log = main ESXi kernel log; storage/network/crash events                                    │
│  hostd.log   = host daemon log; VM operations, config changes                                         │
│  vpxa.log    = vCenter agent log; connection issues to vCenter                                        │
│  fdm.log     = HA agent log; cluster membership and failover events                                   │
│  esxtop      = real-time performance tool; CPU/mem/disk/net metrics                                   │
│  DAVG        = device average latency; > 25ms indicates storage issue                                 │
│  KAVG        = kernel average latency; VMkernel queue delay                                           │
│  vm-support  = CLI tool to create ESXi diagnostic bundle                                              │
│  SR          = Service Request; VMware GSS support ticket                                             │
│  /scratch    = persistent log path; on SD/USB hosts may be volatile                                   │
│  batch mode  = esxtop -b -n N; captures N iterations non-interactively                                │
│  Support bundle = zip of logs, configs, hardware state for GSS analysis                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## Common Issues

- Failed or stuck tasks
- Certificate, DNS, or authentication issues
- Capacity pressure
- Service health warnings
- Version mismatch after maintenance
- Monitoring gaps

## Log Analysis

### Key Log Files

| Log | Path | Content |
|---|---|---|
| vmkernel | `/var/log/vmkernel.log` | Storage, network, driver-level events |
| hostd | `/var/log/hostd.log` | Host management agent (API, VM operations) |
| vpxa | `/var/log/vpxa.log` | vCenter agent communication |
| vobd | `/var/log/vobd.log` | Hardware/system observation (IPMI, sensors) |
| fdm | `/var/log/fdm.log` | HA agent (Fault Domain Manager) |
| auth | `/var/log/auth.log` | SSH logins, sudo |

### Searching Logs

```bash
# Errors and warnings
grep -i "error\|warning\|fail\|fault" /var/log/vmkernel.log | tail -30
grep -i "error" /var/log/hostd.log | tail -20
grep -i "disconnected\|lost connectivity" /var/log/vpxa.log | tail -10

# Storage path errors
grep -i "lost path\|path down\|APD\|PDL" /var/log/vmkernel.log | tail -20

# Network errors
grep -i "link down\|carrier\|vmnic" /var/log/vmkernel.log | tail -20

# HA events
grep -i "isolation\|restart\;fdm" /var/log/fdm.log | tail -20
```

### Collect Support Bundle

```bash
vm-support -n -w /tmp/
# Output: /tmp/esx-<hostname>-<date>.tgz
# Or: vSphere Client → Host → Actions → Export System Logs
```

## Performance Troubleshooting

### Common Symptoms

- High CPU ready time
- High memory ballooning or swapping
- High storage latency
- Slow VM response
- VM time drift
- Host contention alarms

### Key Metrics

| Metric | Normal | Caution | Problem |
|---|---|---|---|
| CPU Ready | < 5% | 5–10% | > 10% |
| Memory Balloon | ~0 | Any | Growing |
| Memory Swap | 0 | Any | Growing |
| Datastore Latency | < 10 ms | 10–20 ms | > 20 ms |

### esxtop

```bash
esxtop
```

Interactive mode keys:
- `c` — CPU view
- `m` — Memory view
- `d` — Disk view
- `n` — Network view

```bash
# Batch capture (60 seconds, 2-second intervals)
esxtop -b -d 2 -n 30 > /tmp/esxtop.csv
```

### First Actions

1. Identify the affected VM or host
2. Check CPU ready
3. Check memory ballooning or swap
4. Check datastore latency
5. Check network packet drops
6. Review recent changes

## Host Disconnect Troubleshooting

### Symptoms

- ESXi host shows disconnected or not responding in vCenter
- vCenter cannot manage the host
- Host tasks fail or timeout
- VMs may still be running but management is degraded

### Likely Causes

- Recent configuration change
- DNS, certificate, or authentication issue
- Resource pressure
- Failed service (`hostd`, `vpxa`)
- Storage or network dependency issue
- Version or compatibility mismatch

### Troubleshooting Workflow

1. Confirm scope — is it one host or multiple?
2. Check recent changes in vCenter Tasks & Events
3. Review alarms and events on the affected host
4. Validate management connectivity (ping, traceroute to management vmk0 IP)
5. Check logs: `hostd.log`, `vpxa.log`, `vmkernel.log`
6. Isolate the failing dependency (DNS, NTP, certificate, storage)
7. Apply fix or escalate with evidence

```bash
# Restart management agents if host is accessible via SSH or console
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
```

## Maintenance Mode Validation

Use before placing a host into maintenance mode and before returning it to service.

### Pre-Checks

- Confirm cluster has sufficient capacity to absorb workload
- Confirm maintenance window if changes are planned
- Confirm current health and check recent alerts and tasks
- Confirm access to management tools
- Confirm rollback path if configuration changes are made

### Post-Maintenance Validation

- Confirm the host is Connected in vCenter
- Confirm no new critical alarms
- Confirm monitoring reflects the expected state
- Confirm related systems still have access
- Document the result

### Rollback

- Revert the changed setting if possible
- Restore prior configuration from documented state
- Escalate if rollback requires vendor support
