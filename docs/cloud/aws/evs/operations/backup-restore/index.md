# Amazon EVS — Backup & Restore

<div class="kb-summary">
EVS backup strategy: SDDC Manager configuration backup to S3, vCenter database backup, VM backups using Veeam or AWS Backup, and restoration procedures.
</div>

```text
┌──────────────────────────────── Amazon EVS — Backup & Restore ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   SDDC Manager config backup: SFTP target (S3 via SFTP bridge or on-prem SFTP); daily        │    │
│   │   vCenter config backup: vCenter UI → Administration → Backup; SFTP or NFS target            │    │
│   │   VM backups: Veeam with vStorage API (VADP); backup datastores on-prem or S3/EBS            │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## SDDC Manager Configuration Backup

```bash
# SDDC Manager backs up its configuration (domains, hosts, VCF topology) to an SFTP server.
# Required for VCF recovery if SDDC Manager is lost.

# Configure via SDDC Manager UI:
# Administration → Backup and Restore → Configure Backup

# SFTP target options for EVS:
# Option A: Transfer Family SFTP (AWS-managed SFTP backed by S3)
#   - Create AWS Transfer Family server with S3 backend
#   - Create IAM user + SSH key for SDDC Manager
#   - SFTP endpoint: <server-id>.server.transfer.us-east-1.amazonaws.com

# Option B: On-premises SFTP server reachable via Direct Connect

# Trigger immediate backup (API)
curl -sk -u "$SDDC_USER:$SDDC_PASSWORD" \
  -X POST "https://sddc-manager.vcf.internal/v1/backups/tasks" \
  -H "Content-Type: application/json" \
  -d '{"type": "BACKUP"}' | python3 -m json.tool

# List backup files
curl -sk -u "$SDDC_USER:$SDDC_PASSWORD" \
  "https://sddc-manager.vcf.internal/v1/backups" | python3 -m json.tool
```

## vCenter Configuration Backup

```bash
# vCenter backup includes vCenter DB and inventory.
# Does NOT include VM data — that requires separate VM backup.

# Via vCenter UI:
# Administration → vCenter Server Settings → Backup → Schedule or Run Now
# Target: SFTP or HTTPS; same SFTP target as SDDC Manager recommended

# Verify backup schedule (via API)
curl -sk -u "administrator@vsphere.local:$VCENTER_PASSWORD" \
  "https://$VCENTER/api/appliance/recovery/backup/schedules" | python3 -m json.tool
```

## VM Backup (Veeam on EVS)

```bash
# Veeam Backup & Replication deployed as a VM on EVS or on-premises.
# Uses VMware vStorage APIs for Data Protection (VADP) for crash-consistent snapshots.

# Veeam backup architecture for EVS:
# Veeam B&R server → vCenter (VADP) → snapshot VM on EVS → read data via proxy
# → write to backup repository (S3, EBS, or on-premises target)

# S3 as Veeam backup repository (recommended for EVS):
# Veeam → Backup Infrastructure → Add Repository → Object Storage → S3
# Use S3 Glacier Instant Retrieval for archival tier (cost optimization)

# For immediate recovery testing:
# Veeam → Instant VM Recovery → mount VM directly from backup and power on
# Useful for testing without restoring to vSAN
```

## Restore Procedures

```bash
# Restore SDDC Manager from backup
# 1. Deploy fresh SDDC Manager OVA (same version as backup)
# 2. SDDC Manager UI → Backup and Restore → Restore
# 3. Provide SFTP credentials and select backup file
# 4. SDDC Manager rebuilds domain inventory from backup

# Restore vCenter from backup
# 1. Deploy fresh vCenter appliance (same version)
# 2. During deployment wizard: select "Restore from backup"
# 3. Provide SFTP backup location

# Restore a VM (Veeam)
# Veeam → Home → Restore → VMware VMs → Restore from backup
# Options: full restore, instant recovery, disk-level restore
```
