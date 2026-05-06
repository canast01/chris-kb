# Disk Groups

> Part of the [vSAN CLI Reference](../).

---

## Disk Groups

```bash
# List disk groups
esxcli vsan storage list

# Per-disk stats
esxcli vsan storage stats get

# Evacuate disk group (before removal)
esxcli vsan storage evacuate -d <device_naa>

# Add disk to disk group
esxcli vsan storage add -s <ssd_naa> -d <capacity_naa>

# Remove disk group
esxcli vsan storage remove -s <ssd_naa>
```
