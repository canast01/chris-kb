# SnapMirror

> Part of the [NetApp ONTAP CLI Reference](../).

---

## SnapMirror

```bash
# Show relationships
snapmirror show
snapmirror show -destination-path <svm>:<vol>
snapmirror show -fields source-path,destination-path,state,lag-time,healthy

# Create / delete
snapmirror create -source-path <svm>:<vol> -destination-path <svm>:<vol> -type DP -policy MirrorAllSnapshots
snapmirror delete -destination-path <svm>:<vol>
snapmirror release -source-path <svm>:<vol> -destination-path <svm>:<vol>

# Operations
snapmirror initialize -destination-path <svm>:<vol>
snapmirror update -destination-path <svm>:<vol>
snapmirror quiesce -destination-path <svm>:<vol>
snapmirror break -destination-path <svm>:<vol>
snapmirror resync -destination-path <svm>:<vol>
snapmirror abort -destination-path <svm>:<vol>

# History and lag
snapmirror history show -destination-path <svm>:<vol>
snapmirror lag show
```
