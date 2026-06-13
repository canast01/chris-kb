---
tags:
  - reference
---
# Daily VMware Operations Workflow


<div class="kb-summary">
A repeatable morning workflow to confirm the environment is healthy before the business day begins.

*Applies to: vSphere 7.x / 8.x*
</div>
```text
┌────────────────────────────── Virtualization Reference Quick Reference ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Reference: Virtualization Reference Quick Reference platform                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Virtualization Reference Quick Reference management console            │   │
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
│    Physical: Virtualization Reference Quick Reference infrastructure · management network · monitoring│
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Reference          = Virtualization Reference Quick Reference platform overview and core concepts  │
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
