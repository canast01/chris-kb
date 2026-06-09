# OpenShift — Backup & Restore

<div class="kb-summary">
etcd backup and restore procedure, OADP (OpenShift API for Data Protection) for application workloads, and recovery from common failure scenarios.
</div>

```text
┌───────────────────────────────────── OpenShift Backup & Restore ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   etcd backup = cluster state snapshot; restore recovers from catastrophic control plane loss  │  │
│   │   OADP = application-level backup (PVCs, resources, namespace); uses Velero under the hood    │   │
│   │   Run etcd backup: before every upgrade, weekly minimum, after large config changes            │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       etcd Backup           │  │       OADP / Velero          │  │     Restore Scenarios       │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  Script on master node      │  │  Operator from OperatorHub   │  │  Single member lost: replace│  │
│   │  Saves snapshot + static PK │  │  BackupStorageLocation (S3)  │  │  Quorum lost: full restore  │  │
│   │  Copy off-cluster (S3/NFS)  │  │  Schedule: CronJob-style     │  │  OADP: restore namespace   │   │
│   │  Verify: check file size    │  │  Include/exclude namespaces  │  │  Partial: selective restore │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    etcd snapshot= Point-in-time copy of all cluster state (secrets, configs, deployments, etc.)       │
│    OADP         = OpenShift API for Data Protection; Velero-based operator for app-level backup       │
│    BackupStorageLocation= S3-compatible endpoint for storing OADP backup tarballs                     │
│    Static pods  = Control plane pods managed by kubelet directly (not via API); backed up with etcd   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## etcd Backup

```bash
# Run on a master node (SSH or oc debug)
oc debug node/<master-node>
chroot /host

# Run the backup script (ships with OCP)
/usr/local/bin/cluster-backup.sh /home/core/assets/backup

# Output:
# /home/core/assets/backup/snapshot_<timestamp>.db
# /home/core/assets/backup/static_kuberesources_<timestamp>.tar.gz

# Verify backup size (should be several hundred MB)
ls -lh /home/core/assets/backup/

# Copy off-node to secure storage
# From your workstation:
oc rsync <master-node>:/home/core/assets/backup/ ./etcd-backup-$(date +%F)/
# Or: scp core@<master-ip>:/home/core/assets/backup/* /backup/etcd/
```

## etcd Restore (Quorum Lost)

```bash
# ONLY USE when etcd quorum is lost and cluster is unrecoverable
# This procedure deletes all nodes and rebuilds from snapshot

# 1. Stop all master nodes except the one you'll restore from

# 2. SSH to the recovery master
ssh core@<master-ip>

# 3. Run restore script with backup files
sudo /usr/local/bin/cluster-restore.sh /home/core/assets/backup

# 4. Verify etcd members
sudo crictl ps | grep etcd

# 5. Restart remaining masters one by one
# Power on master-2, master-3 — they will rejoin the restored etcd

# 6. Delete stale etcd members and approve CSRs
oc get csr | grep Pending
oc adm certificate approve <csr>

# 7. Verify cluster health
oc get nodes
oc get co
```

## Replace Single etcd Member

```bash
# For: one master node failed, other two are healthy (quorum maintained)

# 1. Remove failed member from etcd
oc rsh -n openshift-etcd etcd-<healthy-master> \
  etcdctl member list
oc rsh -n openshift-etcd etcd-<healthy-master> \
  etcdctl member remove <member-id>

# 2. Delete the failed Machine object
oc get machine -n openshift-machine-api | grep <failed-node>
oc delete machine <machine-name> -n openshift-machine-api

# 3. Scale MachineSet or add new machine — new master joins via ignition
# 4. Approve CSR for new master
oc get csr | grep Pending
oc adm certificate approve <csr>

# 5. Verify etcd member joined
oc rsh -n openshift-etcd etcd-<master> etcdctl member list
```

## OADP Application Backup

```bash
# 1. Install OADP operator from OperatorHub

# 2. Create BackupStorageLocation
cat <<EOF | oc apply -f -
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: s3-backup
  namespace: openshift-adp
spec:
  provider: aws
  objectStorage:
    bucket: ocp-backups
    prefix: velero
  config:
    region: us-east-1
    s3ForcePathStyle: "false"
  credential:
    name: cloud-credentials
    key: cloud
EOF

# 3. Create backup
oc create -f - <<EOF
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: my-app-backup
  namespace: openshift-adp
spec:
  includedNamespaces:
  - my-app
  storageLocation: s3-backup
  ttl: 720h
EOF

# 4. Schedule automatic backups
cat <<EOF | oc apply -f -
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: openshift-adp
spec:
  schedule: "0 2 * * *"
  template:
    includedNamespaces: ["*"]
    excludedNamespaces: ["openshift-*","kube-*"]
    storageLocation: s3-backup
EOF

# 5. Restore from backup
oc create -f - <<EOF
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: my-app-restore
  namespace: openshift-adp
spec:
  backupName: my-app-backup
  includedNamespaces:
  - my-app
EOF

# Monitor
oc get backup -n openshift-adp
oc get restore -n openshift-adp
velero backup logs my-app-backup -n openshift-adp
```
