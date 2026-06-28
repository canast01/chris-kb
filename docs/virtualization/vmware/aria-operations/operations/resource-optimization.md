---
tags:
  - aria-operations
  - operations
  - vmware
---
# Performance — Resource Optimisation

```bash
# List processes consuming > 1% CPU
ps aux --sort=-%cpu | awk 'NR>1 && $3>1 {print $1, $3"%", $4"%", $11}'

# Average CPU per server (last 30 days via sar)
sar -u -f /var/log/sa/sa$(date +%d) | awk '/Average/ {print $3}'

# Memory available
free -h | awk '/Mem/ {print "Available:", $7}'
```

```bash
# Unattached managed disks
az disk list \
  --query '[?diskState==`Unattached`].{Name:name,RG:resourceGroup,Size:diskSizeGb,SKU:sku.name}' -o table

# Azure Advisor cost recommendations
az advisor recommendation list \
  --category Cost \
  --query '[*].{Impact:impact,Resource:resourceMetadata.resourceId,Recommendation:shortDescription.solution}' -o table
```
```bash
# ONTAP — volumes with > 50% free space
volume show -percent-used <50 -fields volume,size,used,percent-used

# Large files older than 90 days
find /data -type f -size +1G -mtime +90 -ls | sort -k7 -rn | head -20
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier

## See also

- [Alert Management](alert-management.md)
- [Aria Operations: Alert Definitions and Policies](alerts.md)
- [Aria Operations Backup & Restore](backup-restore.md)
- [Aria Operations — Operations](index.md)
- [Aria Operations — Architecture](../architecture/)
- [Aria Operations — Deploy](../deploy/)
- [Aria Operations — Security](../security/)
- [Aria Operations — Troubleshooting](../troubleshooting/)
