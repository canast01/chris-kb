---
tags:
  - aria-operations
  - operations
  - vmware
---
# Performance — Resource Optimisation

*Applies to: VMware Aria 8.x*

```bash
# List processes consuming > 1% CPU
ps aux --sort=-%cpu | awk 'NR>1 && $3>1 {print $1, $3"%", $4"%", $11}'

# Average CPU per server (last 30 days via sar)
sar -u -f /var/log/sa/sa$(date +%d) | awk '/Average/ {print $3}'

# Memory available
free -h | awk '/Mem/ {print "Available:", $7}'
```


```text title="Expected output"
root 45.2% 12.8% /usr/lib/vmware-vsan/bin/vsanmgmtd
vmware 38.7% 8.3% /usr/lib/vmware-vix-disklib/bin/vmtoolsd
root 28.1% 5.2% /opt/vmware/aria/bin/java
postgres 15.3% 22.1% /usr/lib/postgresql/bin/postgres
root 8.9% 3.4% /usr/sbin/sshd
Available: 124G
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sar: Cannot open /var/log/sa/sa31: No such file or directory` | Ensure sar data collection is enabled via `systemctl enable sysstat && systemctl start sysstat`, or use an existing sa file date. |
    | `awk: syntax error in pattern near line 1` | Verify the awk field separators match your ps/sar output format; add `-F' '` if whitespace parsing fails. |
```bash
# Unattached managed disks
az disk list \
  --query '[?diskState==`Unattached`].{Name:name,RG:resourceGroup,Size:diskSizeGb,SKU:sku.name}' -o table

# Azure Advisor cost recommendations
az advisor recommendation list \
  --category Cost \
  --query '[*].{Impact:impact,Resource:resourceMetadata.resourceId,Recommendation:shortDescription.solution}' -o table
```

```text title="Expected output"
Name                                    RG              Size    SKU
--------------------------------------  --------------  ------  ----------------
disk-backup-20240115-prod               prod-rg         256     Premium_LRS
disk-old-database-archive               legacy-rg       512     Standard_LRS
disk-temp-migration-test                dev-rg          128     Premium_LRS
disk-unused-snapshot-cache              monitoring-rg   1024    StandardSSD_LRS

Impact    Resource                                                                    Recommendation
--------  -------------------------------------------------------------------------  -----------------------------------------------
High      /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/...    Delete unattached managed disks to reduce costs
Medium    /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/...    Right-size underutilized virtual machines
High      /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/...    Remove unused ExpressRoute circuits
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: The following arguments are required: --subscription` | Add `--subscription <subscription-id>` or set the default subscription with `az account set --subscription <id>`. |
    | `ERROR: No registered resource provider found for location 'eastus'` | Ensure the subscription has the required resource providers registered using `az provider register --namespace Microsoft.Compute`. |
```bash
# ONTAP — volumes with > 50% free space
volume show -percent-used <50 -fields volume,size,used,percent-used

# Large files older than 90 days
find /data -type f -size +1G -mtime +90 -ls | sort -k7 -rn | head -20
```

```d2
direction: right

verify: "Verify" {shape: rectangle}

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
- [Aria Operations — Architecture](../../architecture/)
- [Aria Operations — Deploy](../../deploy/)
- [Aria Operations — Security](../../security/)
- [Aria Operations — Troubleshooting](../../troubleshooting/)
