# Post-Change Validation (Virtualization)


<div class="kb-summary">
Run these checks after any infrastructure change — maintenance, upgrade, patch, or configuration modification. Document evidence in the change record before closing.
</div>

```text
Post-Change Validation Flow
═══════════════════════════════════════════════════════════

  CHANGE COMPLETE
        │
        ▼
  ┌─────────────────────────────────┐  (within 5 min)
  │  Immediate checks               │
  │  ├─ Hosts connected to vCenter  │
  │  ├─ Cluster HA/DRS active       │
  │  └─ No VMs in unexpected state  │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  Storage checks                 │
  │  ├─ Datastores accessible       │
  │  └─ vSAN health green           │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  Services checks                │
  │  ├─ NSX cluster stable          │
  │  ├─ Backup jobs healthy         │
  │  └─ Aria collecting data        │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  Application validation         │
  │  └─ App owner confirms OK       │
  └─────────────┬───────────────────┘
                │
                ▼
  ┌─────────────────────────────────┐
  │  Evidence captured              │
  │  └─ Screenshots in change record│
  └─────────────┬───────────────────┘
                │
                ▼
         CLOSE CHANGE RECORD
```
```text
┌─────────────────────────────────────── Post-Change Validation ────────────────────────────────────────┐
│                                                                                                       │
│    Run after any change — maintenance, upgrade, patch, or config modification                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Immediate — within 5 min           │  │           Extended — within 1 hour          │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │          Hosts connected to vCenter          │  │           Monitoring alerts clear           │   │
│   │           Cluster HA / DRS active            │  │            App owner confirms OK            │   │
│   │          No VMs in unexpected state          │  │             Backup job succeeds             │   │
│   │          Datastore paths accessible          │  │            Snapshot count stable            │   │
│   │            No new critical alarms            │  │          Performance metrics normal         │   │
│   │              vSAN health green               │  │             Change record closed            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Unexpected state = VM powered off, suspended, or orphaned unexpectedly after change                │
│    Datastore paths  = Storage I/O paths from ESXi; check via esxcli storage core path list            │
│    Snapshot stable  = No new snapshots created by backup; no stale snapshots accumulating             │
│    App owner        = Business stakeholder; must confirm application is healthy post-change           │
│    Change record    = Close only after all checks pass and app owner sign-off is documented           │
│    Monitoring alert = Any new alert fired after change = likely caused by the change; triage          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## NSX (if change was NSX-related)

```bash
# Verify NSX Manager cluster stability
get cluster status   # All nodes: STABLE

# Verify edge nodes are healthy
get service router
get logical-routers
```

## Backup Validation

```powershell
# Confirm backup jobs are not in failed state after change
# (Veeam)
Get-VBRJob | Where-Object {$_.GetLastState() -eq "Failed"} | Select-Object Name, LastRun

# (CommVault — check via Command Center UI for jobs since change window start)
```

## Monitoring Validation

1. Log in to Aria Operations → confirm no new critical or immediate alerts generated by the change
2. Verify collection is still running: Environment → `<cluster name>` → Collection State: OK
3. Check that baseline alerts that existed before the change are not masked by new false positives

## Application Validation

If the change affected production workloads:
- Contact the application owner to confirm the application is functioning correctly
- Run a basic functional test (login to the app, execute a representative transaction)
- Record the application owner's confirmation in the change record

## Change Record Closure

Before closing the change:

- [ ] All hosts connected: confirmed
- [ ] HA/DRS status: verified green
- [ ] vSAN health: no new alarms
- [ ] No unexpected VM state changes
- [ ] Datastores accessible
- [ ] Backup jobs not broken
- [ ] Monitoring collecting data
- [ ] Application owner sign-off (for production changes)
- [ ] Final component versions captured:
  ```powershell
  Get-VMHost | Select-Object Name, Version, Build | Sort-Object Name
  (Get-View ServiceInstance).Content.About.Version   # vCenter version
  ```
- [ ] Change record updated with evidence screenshots or command output
