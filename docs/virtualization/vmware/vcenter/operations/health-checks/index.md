# vCenter — Health Checks


<div class="kb-summary">
Health Checks reference covering Disk Partition Usage, SSO and Lookup Service Health, DNS and NTP Validation, PowerCLI Health Checks, Daily Checks and 2 more sections.
</div>

```text
Health Check Coverage Map
════════════════════════════════════════════════════════

  VAMI (:5480)                   Shell (SSH)
  ┌────────────────────────┐     ┌───────────────────────┐
  │ Summary tab            │     │ service-control        │
  │  ├── CPU / RAM / Disk  │     │  --status --all        │
  │  └── Service overview  │     │                        │
  │                        │     │ df -h                  │
  │ Services tab           │     │  ├── /storage/log      │
  │  └── started/stopped   │     │  ├── /storage/db       │
  │                        │     │  └── /storage/core     │
  │ Certificate Mgmt tab   │     │                        │
  │  └── expiry dates      │     │ timedatectl (NTP)      │
  └────────────────────────┘     │ nslookup (DNS)         │
                                 └───────────────────────┘

  PowerCLI Checks (daily)
  ┌────────────────────────────────────────────────────┐
  │  Get-VMHost      → ConnectionState = Connected?    │
  │  Get-Cluster     → DrsEnabled + HAEnabled?         │
  │  Get-Snapshot    → age > 3 days? (flag stale)      │
  │  Get-Datastore   → FreeSpacePct > 20%?             │
  │  Get-VIEvent     → errors in last 24h?             │
  │  REST /health    → system health = GREEN?          │
  └────────────────────────────────────────────────────┘

  Check Cadence
  Daily ──▶ services, hosts connected, snapshots, alarms
  Weekly ──▶ datastore capacity, certificate expiry
  Pre-change ──▶ backup current, HA capacity, no migrations
```
```text
┌─────────────────────────────────── vCenter Server — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  Regular vCenter health checks verify service state, certificate validity, database                   │
│  health, and host connectivity to prevent silent failures.                                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Service Health                │  │              Certificate Health             │   │
│   │          VAMI: Summary panel green           │  │             Cert expiry >30 days            │   │
│   │           vmon-cli -l: all RUNNING           │  │            STS cert: renew yearly           │   │
│   │          SSO: login works normally           │  │           Machine cert: auto-renew          │   │
│   │          Events: no critical alarms          │  │            certmgr: check via CLI           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Check services first; certificate expiry is the most common silent failure mode.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Database & Disk                │  │              Host Connectivity              │   │
│   │          Postgres: no vacuums stuck          │  │             All hosts: Connected            │   │
│   │         Disk usage <80% on /storage          │  │           vpxa heartbeat: <60s ago          │   │
│   │            Stats DB: no overflow             │  │             DRS: no red clusters            │   │
│   │          Backup: last run <24h ago           │  │          HA: no admission failures          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VCSA health depends on underlying ESXi host resource availability and shared                         │
│  storage connectivity; network latency to hosts must be <10ms.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VAMI         = vCenter Appliance Management Interface; port 5480                                     │
│  vmon-cli     = service monitor; RUNNING state = healthy                                              │
│  STS cert     = Security Token Service cert; 2-year expiry; breaks SSO if expired                     │
│  Machine cert = VCSA machine SSL cert; auto-renewed by default                                        │
│  certmgr      = certificate manager utility on VCSA appliance shell                                   │
│  vpxa         = host agent; heartbeat to vCenter; disconnect = host error                             │
│  Postgres     = VCSA embedded DB; vacuum stuck = performance degradation                              │
│  /storage     = VCSA data partition; events, stats, logs stored here                                  │
│  HA admission = cluster reserves capacity for one host failure; red if short                          │
│  DRS red      = DRS migration imbalance or constraint violation                                       │
│  Stats DB     = performance metrics; rollup jobs run on schedule                                      │
│  certmgr      = /usr/lib/vmware-vmca/bin/certool for cert inspection                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Key partitions to monitor:
- `/storage/log` — fills quickly during issues
- `/storage/db` — vCenter database
- `/storage/core` — core appliance data

## SSO and Lookup Service Health

```bash
service-control --status vmware-sts
service-control --status vmware-lookupsvc
service-control --status vmware-eam
```

## DNS and NTP Validation

```bash
# Check DNS from vCenter appliance shell
nslookup <vcenter-fqdn>
dig <vcenter-fqdn>

# Check NTP status
timedatectl
```

## PowerCLI Health Checks

```powershell
# Host connectivity
Get-VMHost | Select-Object Name, ConnectionState, PowerState

# Cluster DRS/HA state
Get-Cluster | Select-Object Name, DrsEnabled, HAEnabled

# Recent error events
Get-VIEvent -MaxSamples 100 -Type Error | Select-Object CreatedTime, FullFormattedMessage

# Stale snapshots
Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-3)} | Select-Object VM, Name, Created

# vCenter REST API health
curl -sk -u 'administrator@vsphere.local' https://<vcenter>/api/vcenter/health/system
```

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| vCenter GUI accessible | Browser to `https://<vcenter>/ui` | All VCSA services should be healthy |
| DRS and HA enabled | `Get-Cluster \| Select Name,DrsEnabled,HAEnabled` | Should be enabled on all production clusters |
| Hosts connected | `Get-VMHost \| Where-Object {$_.ConnectionState -ne "Connected"}` | Result should be empty |
| Unexpected powered-off VMs | `Get-VM \| Where-Object {$_.PowerState -eq "PoweredOff"}` | Flag unexpected powered-off VMs |
| Snapshots older than 3 days | `Get-VM \| Get-Snapshot \| Where-Object {$_.Created -lt (Get-Date).AddDays(-3)}` | Flag old snapshots |
| Certificate expiry | VAMI → Certificate Management | Flag any expiring within 60 days |
| Recent task failures | vCenter Monitor → Tasks | Review error-level tasks |

## Change Readiness Checklist

- [ ] vCenter backup is current — file-based backup or VAMI snapshot completed and verified
- [ ] No active DRS migrations in progress — confirm vCenter Tasks pane is idle
- [ ] HA admission control capacity checked
- [ ] Certificates valid for more than 30 days
- [ ] SSO and PSC health confirmed before any appliance-level change
- [ ] Rollback plan documented: VCSA restore procedure confirmed and tested
- [ ] Change window approved and communicated to all dependent teams

## When to Restore from Backup

Troubleshoot first if:
- Services can be restarted and recovered
- Disk space can be freed to restore normal function
- A single certificate or SSO issue can be repaired in place

Restore from backup if:
- Database is corrupt
- STS certificate cannot be repaired
- Services fail to start after all troubleshooting steps
- The appliance is unrecoverable after a hardware or VM failure
