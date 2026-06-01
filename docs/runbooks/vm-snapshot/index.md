# VM Snapshot Runbook


<div class="kb-summary">
| Field | Value | |---|---| | Risk | Low (taking) / Medium (removing) | | Approval | No formal change required to take; revert requires change ticket | | Estimated time | 2–5 minutes to create; 10–30 minutes to remove (consolidation) | | Impact | None during creation (brief I/O s
</div>

| Field | Value |
|---|---|
| Risk | Low (taking) / Medium (removing) |
| Approval | No formal change required to take; revert requires change ticket |
| Estimated time | 2–5 minutes to create; 10–30 minutes to remove (consolidation) |
| Impact | None during creation (brief I/O stun < 1s); performance degraded while snapshot exists |

!!! warning
    Snapshots are **not backups**. Delta disks grow continuously and degrade performance. Remove within **24–72 hours** — never leave snapshots over a weekend.

## Process Flow

```text
  Change window starting
           │
           ▼
  Pre-check: existing snapshots? ── Yes ──► Stop. Remove stale snapshots first.
           │ No
           ▼
  Datastore ≥ 20% free? ─────────── No ──► Stop. Free space or use a different DS.
           │ Yes
           ▼
  Create snapshot (quiesced if app-consistent needed)
           │
           ▼
  Perform change
           │
  ┌────────┴─────────────┐
  │ Change outcome?      │
  └────────┬─────────────┘
  Success  │  Failure
           │         └──────────────► Revert to snapshot
           ▼
  Validate application is healthy
           │
           ▼
  Remove snapshot (within change window if possible)
           │
           ▼
  Confirm ConsolidationNeeded = False
```
```
┌──────────────────────────────────────── Runbook — VM Snapshot ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           VM snapshots capture state for short-term rollback; NOT a backup solution           │   │
│   │          Delete snapshots within 24–72 hours; older snapshots degrade VM performance          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Create Snapshot                │  │               Delete Snapshot               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          Confirm VM not in snapshot          │  │           Verify change succeeded           │   │
│   │      Quiesce filesystem (VMware tools)       │  │           Delete via Snapshot Mgr           │   │
│   │          Name: CHG-XXXXX-pre-change          │  │         "Delete All" commits deltas         │   │
│   │              Note creation time              │  │           Monitor datastore space           │   │
│   │           Max 1 snapshot in change           │  │           Confirm space reclaimed           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Action      │   vSphere GUI    │      PowerCLI     │      Limit       │       Risk       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Create      │Actions > Snapshot│    New-Snapshot   │   1 per change   │   Delta growth   │   │
│   │       List       │   Snapshot Mgr   │    Get-Snapshot   │        —         │        —         │   │
│   │      Delete      │  Delete in Mgr   │  Remove-Snapshot  │    Delete all    │  Consolidation   │   │
│   │      Revert      │  Revert to snap  │  Set-VM -Snapshot │   Loss of data   │   Irreversible   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Delta VMDK   = Snapshot child disk capturing writes after snapshot; grows until deleted            │
│    Quiesce      = VMware Tools flushes guest FS buffers; ensures consistent snapshot state            │
│    Consolidation= vCenter merges delta disks back into base on snapshot delete                        │
│    Snapshot stun= Momentary IO pause during snapshot create/delete; worse with large VMs              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

## Step 2 — Create Snapshot

**PowerCLI — crash-consistent:**
```powershell
New-Snapshot -VM <vmname> `
    -Name "pre-change-$(Get-Date -Format yyyyMMdd-HHmm)" `
    -Description "Before <change description>"
```

**PowerCLI — app-consistent (quiesced, requires VMware Tools):**
```powershell
New-Snapshot -VM <vmname> `
    -Name "pre-change-$(Get-Date -Format yyyyMMdd-HHmm)" `
    -Quiesce -Memory:$false
```

**ESXi CLI:**
```bash
# Args: VMID, name, description, memory (0=no), quiesce (0=no)
vim-cmd vmsvc/snapshot.create <VMID> "pre-change" "Before change" 0 0
```

## Step 3 — Revert to Snapshot (if change fails)

```powershell
$snap = Get-VM <vmname> | Get-Snapshot -Name "pre-change*"
Set-VM <vmname> -Snapshot $snap -Confirm:$false
```

Then validate the application has rolled back correctly before proceeding.

## Step 4 — Remove Snapshot (after successful change)

Remove as soon as the change is validated — do not leave it to "clean up later".

```powershell
Get-VM <vmname> | Get-Snapshot | Remove-Snapshot -Confirm:$false

# Confirm no consolidation needed
(Get-VM <vmname>).Extensiondata.Runtime.ConsolidationNeeded
# Must return: False
```

**If consolidation is needed:**
```powershell
(Get-VM <vmname>).Extensiondata.ConsolidateVMDisks_Task()
# Monitor in vSphere Client → Tasks
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Snapshot creation fails | Datastore space | Free space; relocate VM or use different datastore |
| Quiesce fails | VMware Tools not running | Use crash-consistent snapshot; fix Tools after |
| Old snapshot found | Previous cleanup missed | Remove immediately; check for consolidation needed |
| ConsolidationNeeded = True after removal | Consolidation didn't run | Trigger manually via PowerCLI or vSphere Client |
| VM performance degraded | Snapshot chain too deep or too old | Remove snapshot immediately; consolidate |

## Checklist

- [ ] No existing snapshots on VM
- [ ] Datastore ≥ 20% free
- [ ] Snapshot created and ID/name recorded
- [ ] Change performed
- [ ] Application validated (or revert taken)
- [ ] Snapshot removed within change window
- [ ] `ConsolidationNeeded` confirmed False
