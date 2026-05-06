# Snapshots

> Part of the [NetApp ONTAP CLI Reference](../).

---

## Snapshots

```bash
# List
volume snapshot show
volume snapshot show -vserver <svm> -volume <vol>

# Create / delete / restore
volume snapshot create -vserver <svm> -volume <vol> -snapshot <name>
volume snapshot delete -vserver <svm> -volume <vol> -snapshot <name>
volume snapshot delete -vserver <svm> -volume <vol> -snapshot * -force true
volume snapshot restore -vserver <svm> -volume <vol> -snapshot <name>
volume snapshot rename -vserver <svm> -volume <vol> -snapshot <old> -new-name <new>

# Snapshot policy
volume snapshot policy show
volume snapshot policy create -policy <name> -enabled true
volume snapshot policy add-schedule -policy <name> -schedule <sched> -count <n>
```
