# Pre-Change Checks


<div class="kb-summary">
Pre-change checks confirm the platform is healthy before maintenance begins. Run these before any host maintenance, upgrade, or configuration change.
</div>

```text
Pre-Change Baseline Sequence
═══════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────┐
  │  Input: Approved change record + maintenance window  │
  └────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────────┐
         ▼                 ▼                     ▼
  ┌─────────────┐  ┌──────────────┐   ┌──────────────────┐
  │  vCenter    │  │  vSAN status │   │  Snapshot count  │
  │  health     │  │  No resync   │   │  Zero stale snaps│
  │  All hosts  │  │  Green health│   │  < 24h or 10 GB  │
  │  connected  │  └──────┬───────┘   └────────┬─────────┘
  └──────┬──────┘         │                    │
         └────────────────┼────────────────────┘
                          ▼
         ┌────────────────┴────────────────┐
         ▼                                 ▼
  ┌─────────────────┐             ┌─────────────────┐
  │  Storage paths  │             │  Backup status  │
  │  No dead paths  │             │  Last job OK    │
  │  Count matches  │             │  Before change  │
  └────────┬────────┘             └────────┬────────┘
           └──────────────┬───────────────┘
                          ▼
                 ┌─────────────────┐
                 │  Rollback plan  │
                 │  documented     │
                 │  All checks PASS│
                 └────────┬────────┘
                          │
                          ▼
                 PROCEED WITH CHANGE
```
┌─────────────────────────────── Pre-Change Checks — Before Maintenance ────────────────────────────────┐
│                                                                                                       │
│    Verify platform is healthy before any host maintenance, upgrade, or config change                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        vCenter Health       │  │        vSAN + Storage       │  │      Snapshots + Backup     │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     All hosts connected     │  │      vSAN health green      │  │      No stale snapshots     │   │
│   │       No active alarms      │  │      No resync in prog.     │  │      Snaps < 24h/10 GB      │   │
│   │        HA/DRS enabled       │  │       All paths active      │  │       Backup ran < 24h      │   │
│   │      Admission ctrl OK      │  │       Datastore < 80%       │  │     Change rec. approv.     │   │
│   │      Tasks/events clear     │  │       No stale extents      │  │      MW window confirm.     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                                            │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             All PASS → proceed with change    ·    Any FAIL → hold until resolved             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Admission ctrl = HA policy reserving cluster capacity to restart all protected VMs                 │
│    Resync         = vSAN rebuilding data after a failure; change causes resync cascade                │
│    Stale extent   = vSAN object component with no active mirror; signals degraded health              │
│    Active paths   = Storage paths from ESXi to array; all should be active/optimised                  │
│    MW window      = Maintenance window; agreed time with app owner and change manager                 │
│    Change rec.    = ITSM change record; must be approved before any maintenance begins                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 3. Active Alarms

```powershell
# Triggered alarms on any host or VM
Get-VMHost | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}
```

Resolve or acknowledge all critical alarms before proceeding. Warning alarms: document and assess risk.

## 4. Datastore Free Space

```powershell
# Datastores below 20% free
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 } |
    Select-Object Name, @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="UsedPct";E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}}
```

## 5. Snapshot Audit

```powershell
# Any snapshots older than 24h or larger than 10 GB
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddHours(-24) -or $_.SizeGB -gt 10 } |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB,2)}}
```

## 6. vSAN Health

```bash
# Run on each ESXi host in vSAN cluster
esxcli vsan health summary get
esxcli vsan debug resync list   # should be empty before maintenance
esxcli vsan debug object list | grep -v healthy   # should return nothing
```

## 7. Storage Paths

```bash
# Any dead paths?
esxcli storage core path list | grep "State: dead"

# Count of active paths (should match expected multipath config)
esxcli storage core path list | grep -c "State: active"
```

## 8. NTP and DNS

```bash
# ESXi host time is synchronised
esxcli system ntp get

# Forward and reverse DNS resolves correctly
nslookup $(hostname)
nslookup vcenter.example.local
```

## 9. Cluster HA and DRS

```powershell
# HA and DRS state
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel

# Any DRS faults or admission control warnings
Get-Cluster | Select-Object Name,
    @{N="HAStatus";E={$_.ExtensionData.Summary.OverallStatus}}
```

## 10. Backup Status

Confirm that the most recent backup completed successfully before making changes. A failed backup combined with a botched change = data at risk.

## 11. Version Capture

```powershell
# Capture current versions before upgrade
Get-VMHost | Select-Object Name, Version, Build | Export-Csv -Path pre_change_versions.csv -NoTypeInformation
$global:DefaultVIServer | Select-Object Name, Version, Build
```

## 12. Rollback Plan Confirmed

Before proceeding, document and confirm:

- [ ] Rollback procedure is documented
- [ ] Maintenance window approval received
- [ ] Change record number noted
- [ ] Escalation contact available during window
- [ ] Time-boxed: if task not complete by X, abort and revert

## Pre-Change Summary Table

| Check | Expected | Status |
|---|---|---|
| vCenter accessible | Connected | |
| All hosts Connected | No Maintenance | |
| Active critical alarms | Zero | |
| Datastore free space | > 20% | |
| Snapshots > 24h | Zero | |
| vSAN health | All GREEN | |
| vSAN resync | Not running | |
| Dead storage paths | Zero | |
| NTP synchronised | Yes | |
| Backup complete | Yes | |
