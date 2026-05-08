# Azure — Backup & Restore

> Azure Backup jobs, restore procedures, and Recovery Services vault management.

See also: [Backup & DR](../../backup-dr/) for full Azure Backup and Azure Site Recovery reference.

---

## Quick Reference

```bash
# List Recovery Services vaults
az backup vault list --output table

# List protected items in a vault
az backup item list --vault-name <vault> -g <rg> --output table

# List backup jobs (last 24h)
az backup job list --vault-name <vault> -g <rg> \
  --query '[?properties.startTime >= `2026-01-01`].[properties.jobType,properties.status,properties.startTime]' \
  -o table

# Check failed backup jobs
az backup job list --vault-name <vault> -g <rg> \
  --query '[?properties.status==`Failed`].[properties.jobType,properties.startTime,properties.errorDetails]' \
  -o table

# Trigger ad-hoc backup
az backup protection backup-now --vault-name <vault> -g <rg> \
  --item-name <vm-name> --container-name <container> \
  --backup-management-type AzureIaasVM --retain-until 2026-12-31

# Restore VM disk
az backup restore restore-disks \
  --vault-name <vault> -g <rg> \
  --container-name <container> --item-name <vm-name> \
  --rp-name <recovery-point-name> \
  --storage-account <staging-sa>
```
