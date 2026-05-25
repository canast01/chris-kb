# Daily VMware Operations Workflow

A repeatable morning workflow to confirm the environment is healthy before the business day begins.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                   Daily Operations Sequence (~20 min)                    │
├───────────────────────────────────────────────────────────────────────── │
│  1. vCenter Alarms (5m)  ──►  Red = fix now  │  Yellow = log + assign    │
│         │                                                                │
│         ▼                                                                │
│  2. Host Health (3m)     ──►  Disconnected?  │  Unexpected maintenance?  │
│         │                                                                │
│         ▼                                                                │
│  3. Cluster HA/DRS (2m)  ──►  HA=On  │  DRS=FullyAutomated               │
│         │                                                                │
│         ▼                                                                │
│  4. Datastore Capacity (3m) ─►  Any > 75%?  →  Action required           │
│         │                                                                │
│         ▼                                                                │
│  5. vSAN Health (2m)     ──►  No red items  │  No unexpected resync      │
│         │                                                                │
│         ▼                                                                │
│  6. Failed Tasks (2m)    ──►  Last 24h  │  Snapshot fails / DRS stuck    │
│         │                                                                │
│         ▼                                                                │
│  7. Backup Status (3m)   ──►  Veeam / CommVault / NBU  │  0 failures     │
│         │                                                                │
│         ▼                                                                │
│  8. Monitoring (2m)      ──►  Aria Ops green  │  Collection state OK     │
│         │                                                                │
│         ▼                                                                │
│  9. Repeat Alerts        ──►  >24h unack → assign owner + task           │
└──────────────────────────────────────────────────────────────────────────┘
```
## Step 1 — vCenter Alarm Triage (5 min)

```powershell
# Connect and get all triggered alarms
Connect-VIServer -Server vcenter.example.local
Get-AlarmDefinition | Where-Object {$_.Enabled} | ForEach-Object {
    Get-Alarm -Entity (Get-Datacenter) | Where-Object {$_.Status -ne "Green"}
} | Select-Object Entity, AlarmDefinition, Status | Format-Table -AutoSize
```

- **Red/critical**: investigate immediately before proceeding
- **Yellow/warning**: log for follow-up; assign owner if persistent

## Step 2 — Host Health (3 min)

```powershell
# Any hosts not fully connected?
Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"} | Select-Object Name, ConnectionState

# Any hosts in maintenance mode unexpectedly?
Get-VMHost -State Maintenance | Select-Object Name, State
```

## Step 3 — Cluster HA and DRS Status (2 min)

```powershell
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, @{
    N="DrsMode"; E={$_.DrsAutomationLevel}
} | Format-Table -AutoSize
```

Confirm: HA Enabled = True, DRS Enabled = True, DrsMode = FullyAutomated (or as per standard).

## Step 4 — Datastore Capacity (3 min)

```powershell
Get-Datastore | Select-Object Name, FreeSpaceGB, CapacityGB, @{
    N="Used%"; E={[math]::Round((1-($_.FreeSpaceGB/$_.CapacityGB))*100,1)}
} | Where-Object {"Used%" -gt 75} | Sort-Object "Used%" -Descending
```

Any datastore > 75% full: investigate and action.

## Step 5 — vSAN Health (2 min, if applicable)

```bash
# SSH to any cluster host, or use vCenter:
# Cluster → Monitor → vSAN → Skyline Health
esxcli vsan health cluster list | grep -v "Green"   # Should return nothing
esxcli vsan debug resync summary                     # Confirm no unexpected resync in progress
```

## Step 6 — Review Failed Tasks (2 min)

vCenter UI → Recent Tasks → filter by Status: Error → review last 24 hours.

Key tasks to watch:
- Snapshot creation failures (backup dependency)
- VM migrate failures (DRS manual recommendations stuck)
- Storage profile compliance failures

## Step 7 — Backup Status (3 min)

Check backup tool dashboard for jobs that ran overnight:
- **Veeam**: Home → Last 24 Hours — any failures → investigate
- **CommVault**: Command Center → Jobs → Failed Jobs
- **NetBackup**: OpsCenter → Monitor → Jobs → Status: Failed

## Step 8 — Monitoring Dashboard (2 min)

Log in to Aria Operations:
- Environment overview: all objects should show green or yellow (not red)
- Confirm collection is running: `Collection State: OK` for all adapters
- Review any new Immediate or Critical alert categories generated overnight

## Step 9 — Follow-Up on Repeat Alerts

Review alerts older than 24 hours that have not been acknowledged:
- Assign each to an owner
- Create a change or task for any alert that has appeared > 3 consecutive days

Total estimated time: **~20 minutes**
