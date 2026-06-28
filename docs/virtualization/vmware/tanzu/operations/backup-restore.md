---
tags:
  - operations
  - tanzu
  - vmware
---
# Tanzu — Backup and Restore


<div class="kb-summary">
Backup and Restore reference covering What to Back Up, Back Up vCenter VCSA (Supervisor), Install and Configure Velero, Schedule Cluster Backups with Velero, Restore from Velero Backup and 3 more sections.

*Applies to: Tanzu 3.x*
</div>
![Tanzu — Backup and Restore](../../../../assets/virtualization-vmware-tanzu-operations-backup-restore.svg)




---

```d2
direction: right

hub: "Tanzu\nOperations" {shape: hexagon}
what_to_back_up: "What to Back Up" {shape: rectangle}
back_up_vcenter_vcsa_supervisor: "Back Up vCenter VCSA (Supervisor)" {shape: rectangle}
install_and_configure_velero: "Install and Configure Velero" {shape: rectangle}
schedule_cluster_backups_with_velero: "Schedule Cluster Backups with Velero" {shape: rectangle}
restore_from_velero_backup: "Restore from Velero Backup" {shape: rectangle}
pvc_backup_with_csi_snapshots: "PVC Backup with CSI Snapshots" {shape: rectangle}

hub -> what_to_back_up
hub -> back_up_vcenter_vcsa_supervisor
hub -> install_and_configure_velero
hub -> schedule_cluster_backups_with_velero
hub -> restore_from_velero_backup
hub -> pvc_backup_with_csi_snapshots
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## What to Back Up

| Component | Backup Method | Notes |
|---|---|---|
| Supervisor cluster (vSphere with Tanzu) | Back up vCenter VCSA | Supervisor state lives in vCenter — VCSA backup covers it |
| TKG management cluster | Velero + etcd backup | etcd holds all K8s object state |
| TKG workload clusters | Velero | Per-cluster backup of K8s resources + PVCs |
| Harbor registry | External DB backup + blob storage backup | Images stored in S3/MinIO or NFS |
| Persistent volumes | Velero CSI snapshots | Requires VolumeSnapshotClass on storage provisioner |

---

## Back Up vCenter VCSA (Supervisor)

```bash
# VCSA file-based backup via VAMI API
curl -sk -X POST \
  "https://vcenter.example.local/api/appliance/recovery/backup/job" \
  -u "administrator@vsphere.local:<password>" \
  -H "Content-Type: application/json" \
  -d '{
    "parts": ["seat", "common"],
    "backup_password": "<backup-password>",
    "location_type": "SFTP",
    "location": "sftp://backup.example.local/vcsa-backups/",
    "location_user": "backupuser",
    "location_password": "<sftp-password>",
    "comment": "Scheduled backup"
  }'
```

---

## Install and Configure Velero

```bash
# Install Velero in TKG cluster (requires S3-compatible storage)
# Example: using MinIO as backup storage location

velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero-backups \
  --backup-location-config \
    region=minio,s3ForcePathStyle=true,s3Url=http://minio.example.local:9000 \
  --secret-file ./credentials-velero \
  --use-volume-snapshots=true \
  --use-node-agent

# credentials-velero file format:
# [default]
# aws_access_key_id = <minio-access-key>
# aws_secret_access_key = <minio-secret-key>
```

---

## Schedule Cluster Backups with Velero

```bash
# Daily backup of all namespaces
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --ttl 720h \
  --include-namespaces '*'

# Backup specific namespace
velero backup create ns-prod-backup \
  --include-namespaces production \
  --wait

# List backups
velero backup get

# Describe a backup
velero backup describe daily-backup-20240101020000
```

---

## Restore from Velero Backup

```bash
# List available backups
velero backup get

# Restore entire backup to a new namespace
velero restore create --from-backup daily-backup-20240101020000 \
  --namespace-mappings production:production-restore

# Restore specific resources only
velero restore create --from-backup daily-backup-20240101020000 \
  --include-resources deployments,services,configmaps \
  --include-namespaces production

# Monitor restore progress
velero restore describe <restore-name>
velero restore logs <restore-name>
```

---

## PVC Backup with CSI Snapshots

```yaml
# Create VolumeSnapshotClass for the storage provisioner
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-vsphere-snapshot-class
  labels:
    velero.io/csi-volumesnapshot-class: "true"
driver: csi.vsphere.volume
deletionPolicy: Delete
```

```bash
# Verify CSI snapshots are being created with Velero backups
kubectl get volumesnapshots -A
```

---

## Harbor Backup

Harbor uses an external PostgreSQL database and blob storage for image layers.

```bash
# Backup Harbor PostgreSQL (if using embedded DB)
kubectl exec -n harbor \
  $(kubectl get pods -n harbor -l component=database -o jsonpath='{.items[0].metadata.name}') \
  -- pg_dumpall -U postgres > harbor-db-$(date +%Y%m%d).sql

# Backup Harbor storage (NFS or S3 mount)
# If using NFS: mount NFS volume and tar the registry data:
tar czf harbor-registry-$(date +%Y%m%d).tar.gz /mnt/harbor-data/registry/

# If using S3: sync to backup bucket:
aws s3 sync s3://harbor-storage s3://harbor-storage-backup
```

---

## Restore Harbor

```bash
# Restore PostgreSQL database
kubectl exec -i -n harbor \
  $(kubectl get pods -n harbor -l component=database -o jsonpath='{.items[0].metadata.name}') \
  -- psql -U postgres < harbor-db-20240101.sql

# Restore image storage (NFS):
tar xzf harbor-registry-20240101.tar.gz -C /mnt/harbor-data/

# Restart Harbor pods to pick up restored data
kubectl rollout restart deployment -n harbor
```

---

## See also

- [Tanzu — Procedures](procedures/)
- [Virtualization Vmware Tanzu — Common Issues](../troubleshooting/common-issues/)
- [Tanzu — Health Checks](health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
