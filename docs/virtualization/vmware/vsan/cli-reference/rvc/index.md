# RVC Commands (Legacy)

> Part of the [vSAN CLI Reference](../).

---

## RVC Commands (Ruby vSphere Console — legacy)

```bash
# Connect to vSAN cluster via RVC
rvc <user>@<vcenter>

# vSAN summary
vsan.health.health_check <cluster_path>
vsan.disks_stats <cluster_path>
vsan.resync_dashboard <cluster_path>
vsan.obj_status_report <cluster_path>
vsan.object_info <cluster_path> <object_uuid>
vsan.proactive_rebalance_info <cluster_path>
vsan.cluster_info <cluster_path>
```
