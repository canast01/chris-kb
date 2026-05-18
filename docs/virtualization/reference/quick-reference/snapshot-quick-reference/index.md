# VMware Snapshot Quick Reference

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Snapshot Chain — Impact on VM I/O                                       │
│                                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────────────┐ │
│  │ Base VMDK│──►│ Delta 1  │──►│ Delta 2  │──►│ Delta 3 (active I/O) │ │
│  │(read-only│   │(read-only│   │(read-only│   │ Writes here; reads   │ │
│  │ after    │   │ after    │   │ after    │   │ chain through all    │ │
│  │ snapshot)│   │ next snap│   │ next snap│   │ previous deltas      │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────────────────┘ │
│                                                                          │
│  Max age: 7 days  │  Max depth: 3  │  Delta > 10 GB = investigate       │
│  Cleanup: Right-click VM → Snapshots → Delete (or Consolidate)          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Find All Snapshots

In vCenter: **Menu** → **Global Views** → **VMs and Templates** → Filter by snapshot state

Or use Aria Operations: **Environment** → **VMs** → filter by snapshot count > 0

## Check Snapshot Age and Size

In vSphere Client: Right-click VM → **Snapshots** → **Manage Snapshots**

- Review snapshot creation date
- Review snapshot size on disk

## Identify Snapshot Owner

- Check if the snapshot was created by a backup product (name will include backup job name)
- Check if it was a manual change-related snapshot

## Remove a Snapshot Safely

1. Confirm the VM is healthy and the snapshot is no longer needed
2. Right-click VM → **Snapshots** → **Manage Snapshots**
3. Select the snapshot → **Delete**
4. Monitor the consolidation task — it may take several minutes

## Consolidation Warning

If vCenter shows a consolidation needed warning:
- Right-click VM → **Snapshots** → **Consolidate**
- Monitor the task and confirm completion

## Check Datastore Free Space After Cleanup

- Confirm datastore free space has recovered after snapshot removal

## Escalate Locked or Stuck Snapshots

- Do not force-delete stuck snapshots without VMware support guidance
- Collect the snapshot delta file list and vCenter events before escalating
