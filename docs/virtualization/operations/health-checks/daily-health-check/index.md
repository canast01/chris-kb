# Daily Health Check


<div class="kb-summary">
Morning checks covering all components that can silently degrade overnight. Target: complete in under 15 minutes.
</div>

```text
Morning Check Sequence
═══════════════════════════════════════════════════════════

  START (07:00 – 07:15)
        │
        ▼
  ┌─────────────────┐     FAIL → Investigate before
  │ 1. vCenter      │            proceeding further
  │    Alarms       ├─── OK ──►  continue
  └─────────────────┘
        │
        ▼
  ┌─────────────────┐     FAIL → Restart vpxa/hostd
  │ 2. Host status  │            or escalate
  │    Connected?   ├─── OK ──►  continue
  └─────────────────┘
        │
        ▼
  ┌─────────────────┐     FAIL → Check HA logs
  │ 3. Cluster HA   │            and admission ctrl
  │    DRS enabled? ├─── OK ──►  continue
  └─────────────────┘
        │
        ▼
  ┌─────────────────┐     WARN → Plan capacity action
  │ 4. Datastore    │     FAIL → Immediate remediation
  │    free space   ├─── OK ──►  continue
  └─────────────────┘
        │
        ▼
  ┌─────────────────┐     FAIL → Check disk groups
  │ 5. vSAN health  │            and resync queue
  │    Skyline grn? ├─── OK ──►  continue
  └─────────────────┘
        │
        ▼
  ┌─────────────────┐     FAIL → Investigate and
  │ 6. Backup jobs  │            retry or escalate
  │    All success? ├─── OK ──►  DONE — record results
  └─────────────────┘
```
┌──────────────────────────────── Daily Health Check — Morning Sequence ────────────────────────────────┐
│                                                                                                       │
│    Run every morning; target completion under 15 minutes; document failures in the change log         │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Step       │    Component     │   Pass Condition  │     On FAIL      │       Tool       │   │
│   │  ──────────────  │  ──────────────  │  ───────────────  │  ──────────────  │  ──────────────  │   │
│   │    1  vCenter    │  No red alarms   │  All green/clear  │ Investigate 1st  │  vSphere Client  │   │
│   │  2  Host status  │  All connected   │   No disconnects  │   Restart vpxa   │  vSphere Client  │   │
│   │  3  Cluster HA   │    HA enabled    │    Admission OK   │  Check HA logs   │   esxcli / UI    │   │
│   │  4  vSAN health  │   Green status   │     No resync     │  vSAN Health UI  │  vSAN Health UI  │   │
│   │  5  Datastores   │    < 80% used    │    No overprov.   │  Free up space   │   Storage view   │   │
│   │   6  VM state    │  All powered on  │   No stuck tasks  │  Force-end task  │  vSphere Client  │   │
│   │  7  Backup jobs  │  All succeeded   │   No failed jobs  │ → backup runbook │  Backup console  │   │
│   │   8  Snapshots   │    None stale    │   < 24h or 10 GB  │ Consolidate VMs  │   Snapshot mgr   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vpxa       = VMware vCenter Agent on each ESXi host; restart restores host connection              │
│    hostd      = ESXi host management daemon; restart if vpxa restart fails                            │
│    HA admission = Policy ensuring enough cluster capacity to restart all protected VMs                │
│    Resync     = vSAN rebuilding data to meet the storage policy; do not patch during                  │
│    Consolidate = Merging stale snapshots into the VM base disk; run via vSphere Client                │
│    Stuck task  = vCenter task in running state > 30 min; cancel via task manager panel                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

## 3. Cluster HA / DRS

```powershell
# Check HA and DRS are enabled
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel

# Check active HA errors
Get-VIEvent -Types Error -MaxSamples 200 |
    Where-Object { $_.FullFormattedMessage -match "HA|DRS" } |
    Select-Object CreatedTime, FullFormattedMessage | Select-Object -First 10
```

## 4. Datastore Free Space

```powershell
# Flag datastores below 20% free
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.20 } |
    Select-Object Name,
        @{N="FreeGB"; E={ [math]::Round($_.FreeSpaceGB,1) }},
        @{N="CapGB";  E={ [math]::Round($_.CapacityGB,1) }},
        @{N="Free%";  E={ [math]::Round($_.FreeSpaceGB/$_.CapacityGB*100,1) }}
```

## 5. vSAN Health

```bash
# Run on any ESXi host in the vSAN cluster
esxcli vsan health cluster list | grep -v "Green\|healthy"

# Check for resyncing objects
esxcli vsan debug object list | grep -i "Resyncing\|Degraded\|Absent" | wc -l
```

## 6. Critical VM Status

```powershell
# Check VMs with PoweredOff state (expected list should be known)
Get-VM | Where-Object { $_.PowerState -ne "PoweredOn" } |
    Select-Object Name, PowerState, Guest

# Check snapshots older than 3 days
Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-3) } |
    Select-Object VM, Name, Created, SizeGB
```

## 7. Active Alarms

```powershell
# All triggered alarms at cluster and higher scope
Get-Folder "Datacenters" | Get-View |
    Select-Object -ExpandProperty TriggeredAlarmState |
    ForEach-Object {
        [PSCustomObject]@{
            Entity = (Get-View $_.Entity).Name
            Alarm  = (Get-View $_.Alarm).Info.Name
            Status = $_.OverallStatus
            Time   = $_.Time
        }
    } | Where-Object { $_.Status -ne "green" }
```

## 8. Backup Job Status

```powershell
# Veeam — check last 24h job results
Get-VBRJob | ForEach-Object {
    $last = Get-VBRRestorePoint -Job $_ | Sort-Object CreationTime -Descending | Select-Object -First 1
    [PSCustomObject]@{ Job = $_.Name; LastResult = $_.GetLastResult(); LastRun = $_.ScheduleOptions.LatestRunLocal }
} | Where-Object { $_.LastResult -ne "Success" }
```

## 9. Identity Source / SSO

```powershell
# Verify LDAP/AD identity source is reachable
Get-SsoAuthenticationSource | Select-Object Name, Type, Enabled
# Check for recent SSO errors in vCenter events
Get-VIEvent -MaxSamples 100 | Where-Object { $_.FullFormattedMessage -match "SSO\|identity\|LDAP" } |
    Select-Object -First 5 CreatedTime, FullFormattedMessage
```

## Daily Check Summary Template

| Area | Status | Notes |
|---|---|---|
| vCenter reachable | | |
| All hosts connected | | |
| HA/DRS enabled | | |
| No datastores < 20% free | | |
| vSAN health all green | | |
| No critical VM alarms | | |
| No stale snapshots | | |
| All backup jobs succeeded | | |
| Identity source healthy | | |
