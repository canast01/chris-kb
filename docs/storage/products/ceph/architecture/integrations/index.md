---
tags:
  - architecture
  - ceph
description: "Ceph integrations: Kubernetes CSI (Rook-Ceph), OpenShift ODF, OpenStack Cinder/Glance/Swift, Prometheus MGR module, and NFS/Ganesha CephFS export."
---
# Ceph — Integrations

<div class="kb-summary">
Ceph integrations: Kubernetes CSI (Rook-Ceph), OpenShift ODF, OpenStack Cinder/Glance/Swift, Prometheus MGR module, and NFS/Ganesha CephFS export.

*Applies to: Red Hat Ceph Storage · Upstream Ceph*
</div>

```d2
direction: right

CEPH: "CEPH" {shape: rectangle}
ODF: "OpenShift ODF\nRBD CSI + CephFS CSI\nopenshift-storage ns" {shape: rectangle}
ROOK: "Kubernetes Rook-Ceph\nCephCluster CR\nRBD + CephFS StorageClass" {shape: rectangle}
OS: "OpenStack\nCinder/RBD\nNova/RBD ephemeral\nSwift/RGW" {shape: rectangle}
PROM: "Prometheus\nMGR prometheus module\nport 9283" {shape: rectangle}
NFS: "NFS Ganesha\nCephFS NFS export\nceph nfs cluster" {shape: rectangle}

CEPH -> ODF
CEPH -> ROOK
CEPH -> OS
CEPH -> PROM
CEPH -> NFS
```

## OpenShift ODF

OpenShift Data Foundation (ODF) is Red Hat's converged storage layer for OpenShift. It deploys Ceph internally via the Rook operator in the `openshift-storage` namespace.

| StorageClass | Access Mode | Backend | Use Case |
|---|---|---|---|
| `ocs-storagecluster-ceph-rbd` | RWO | Ceph RBD | VM disks, database PVCs, stateful apps |
| `ocs-storagecluster-cephfs` | RWX | CephFS | Shared config, CI artifacts, pipelines |
| `ocs-storagecluster-ceph-rgw` | Object (S3) | RGW | Noobaa-backed or direct S3 workloads |

**Install ODF via OperatorHub:**
1. OpenShift console → OperatorHub → search "OpenShift Data Foundation"
2. Install ODF operator into `openshift-storage` namespace
3. Create `StorageSystem` → `StorageCluster` CR to provision Ceph

```bash
# Access Ceph toolbox inside OpenShift ODF
oc rsh -n openshift-storage $(oc get pod -n openshift-storage -l app=rook-ceph-tools -o name)

# Once inside the toolbox
ceph status
ceph osd df
ceph df

# Check ODF StorageCluster health
oc get storagecluster -n openshift-storage
oc describe storagecluster ocs-storagecluster -n openshift-storage

# Check CSI pods
oc get pods -n openshift-storage | grep csi

# List ODF-backed PVCs in all namespaces
oc get pvc -A | grep ocs-storagecluster
```


```text title="Expected output"
Connecting to rook-ceph-tools-abc123def456...
/ # ceph status
  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_OK
    mon: 3 daemons, quorum a,b,c (age 45d)
    mgr: 1 active, 1 standby
    osd: 9 in, 9 up (age 2d)
    pools: 3 pools, 96 pgs
    objects: 2.34M objects, 4.5 TiB
    usage: 6.7 TiB used, 13.3 TiB / 20 TiB avail
    pgs: 96 active+clean

/ # ceph osd df
ID  CLASS WEIGHT  REWEIGHT SIZE    RAW USE %USE  VAR  PGS STATUS
 0   ssd  1.81920  1.00000 2.0 TiB 1.2 TiB 60.0 1.02  32 up
 1   ssd  1.81920  1.00000 2.0 TiB 1.1 TiB 55.0 0.93  32 up
 2   ssd  1.81920  1.00000 2.0 TiB 1.2 TiB 60.0 1.02  32 up
...

/ # ceph df
RAW STORAGE QUOTA     AVAIL     USED RAW USED %RAW USED
    20 TiB  20 TiB 13.3 TiB  6.7 TiB       33.5
POOLS   NAME                 ID QUOTA BYTES QUOTA OBJECTS USED  %USED MAX AVAIL
    3 ocs-storagecluster-cephblockpool  1      N/A        N/A 2.1 TiB 31.3  4.4 TiB
      ocs-storagecluster-cephfilesystem  2      N/A        N/A 1.8 TiB 26.8  4.4 TiB
      ocs-storagecluster-cephobjectstore 3      N/A        N/A 2.8 TiB 41.8  4.4 TiB

NAME                                 READY   STATUS    RESTARTS   AGE
storagecluster.ocs.openshift.io/ocs-storagecluster   True    Active   0          45d

Name:         ocs-storagecluster
Namespace:    openshift-storage
Status:       Ready
Phase:        Ready
External:     false
Created:      2024-01-15T10:23:45Z
Version:      4.14.0

NAME                                    READY   STATUS    RESTARTS   AGE
csi-cephfsplugin-provisioner-abc1d2e3f  2/2     Running   0          45d
csi-cephfsplugin-provisioner-xyz9w8v7u  2/2     Running   0          45d
csi-rbdplugin-provisioner-qwe1r2t
```
## Kubernetes / Rook-Ceph

Rook is the Kubernetes operator that manages the full Ceph lifecycle: deployment, configuration, upgrades, and failure handling.

```yaml
# CephCluster custom resource — defines the cluster layout
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  dataDirHostPath: /var/lib/rook
  mon:
    count: 3
    allowMultiplePerNode: false
  mgr:
    count: 2
  storage:
    useAllNodes: true
    useAllDevices: false
    deviceFilter: "^sd[b-z]"   # use all sdX disks except sda (OS)
```

```yaml
# CephBlockPool — defines the RBD pool
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata:
  name: rbd-pool
  namespace: rook-ceph
spec:
  failureDomain: host
  replicated:
    size: 3
```

```yaml
# StorageClass for RBD (RWO block storage)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-ceph-block
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: rbd-pool
  imageFormat: "2"
  imageFeatures: layering
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
reclaimPolicy: Delete
allowVolumeExpansion: true
```

```yaml
# CephFilesystem — defines MDS-backed CephFS
apiVersion: ceph.rook.io/v1
kind: CephFilesystem
metadata:
  name: myfs
  namespace: rook-ceph
spec:
  metadataPool:
    replicated:
      size: 3
  dataPools:
    - replicated:
        size: 3
  metadataServer:
    activeCount: 1
    activeStandby: true
```

```yaml
# StorageClass for CephFS (RWX shared filesystem)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-cephfs
provisioner: rook-ceph.cephfs.csi.ceph.com
parameters:
  clusterID: rook-ceph
  fsName: myfs
  pool: myfs-data0
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
reclaimPolicy: Delete
allowVolumeExpansion: true
```

PVC provisioning creates an RBD image (for block) or CephFS subvolume (for filesystem) automatically. No manual `ceph` commands required.

## OpenStack Integration

Ceph provides block, image, and object backends for OpenStack.

```bash
# --- Cinder block storage (VM disks) ---
# /etc/cinder/cinder.conf
# [DEFAULT]
# enabled_backends = ceph
# [ceph]
# volume_driver = cinder.volume.drivers.rbd.RBDDriver
# rbd_pool = volumes
# rbd_ceph_conf = /etc/ceph/ceph.conf
# rbd_user = cinder
# rbd_secret_uuid = <libvirt secret UUID>

# Create Ceph user for Cinder
ceph auth get-or-create client.cinder \
  mon 'profile rbd' \
  osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images'

# --- Glance image store ---
# /etc/glance/glance-api.conf
# [glance_store]
# stores = rbd
# default_store = rbd
# rbd_store_pool = images
# rbd_store_user = glance
# rbd_store_ceph_conf = /etc/ceph/ceph.conf

ceph auth get-or-create client.glance \
  mon 'profile rbd' \
  osd 'profile rbd pool=images'
```


```text title="Expected output"
[client.cinder]
	key = AQC7vZdnK3J+ExAAZ8vK9Z4m8K3vZ9K8K3vZ9A==
	caps mon = "profile rbd"
	caps osd = "profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images"

[client.glance]
	key = AQD8wZdnL4K+FxBBa9wL0a5n9L4wA0L9L4wA0B==
	caps mon = "profile rbd"
	caps osd = "profile rbd pool=images"
```

!!! warning "Common errors"
    **`Error EINVAL: invalid command`** — Verify the Ceph cluster is running with `ceph status` and check syntax matches your Ceph version.
    **`Error EACCES: permission denied`** — Run the commands with `sudo` or as a user with Ceph admin keyring access.
    **`Error ENOENT: pool does not exist`** — Create the required pools (`ceph osd pool create volumes`, `ceph osd pool create images`, `ceph osd pool create vms`) before creating the user capabilities.
| Service | Ceph Backend | Pool | Benefit |
|---|---|---|---|
| Cinder | RBD | `volumes` | Thin provisioning, snapshots, live resize |
| Nova (ephemeral) | RBD | `vms` | Live migration without shared NFS; disk stays in Ceph |
| Glance | RBD | `images` | Fast copy-on-write cloning from image to Cinder volume |
| Swift / Object | RGW | N/A | S3/Swift endpoint; no separate Swift cluster needed |

**Live migration with Ceph RBD**: when Nova ephemeral disks are stored in Ceph (`rbd_ephemeral_storage=True`), live migration copies no disk data — only VM memory is transferred. This makes migration instant regardless of disk size.

## Prometheus Integration

The Ceph MGR includes a built-in Prometheus exporter module.

```bash
# Enable the Prometheus MGR module
ceph mgr module enable prometheus

# Verify it's listening
ceph mgr module ls | grep prometheus
curl http://<mgr-host>:9283/metrics | head -40
```


```text title="Expected output"
ok
prometheus                           on (ceph-mgr-1, ceph-mgr-2)
  {
    "always_on": false,
    "can_run": true,
    "error_string": "",
    "name": "prometheus",
    "run_on": [
      "ceph-mgr-1",
      "ceph-mgr-2"
    ]
  }
# HELP ceph_cluster_total_used_bytes Ceph cluster used bytes
# TYPE ceph_cluster_total_used_bytes gauge
ceph_cluster_total_used_bytes 2.748779008e+11
# HELP ceph_cluster_total_avail_bytes Ceph cluster available bytes
# TYPE ceph_cluster_total_avail_bytes gauge
ceph_cluster_total_avail_bytes 7.251220992e+11
# HELP ceph_osd_up OSD up status
# TYPE ceph_osd_up gauge
ceph_osd_up{ceph_daemon="osd.0"} 1
ceph_osd_up{ceph_daemon="osd.1"} 1
ceph_osd_up{ceph_daemon="osd.2"} 1
# HELP ceph_osd_in OSD in status
# TYPE ceph_osd_in gauge
ceph_osd_in{ceph_daemon="osd.0"} 1
ceph_osd_in{ceph_daemon="osd.1"} 1
ceph_osd_in{ceph_daemon="osd.2"} 1
# HELP ceph_pg_active PG active status
# TYPE ceph_pg_active gauge
ceph_pg_active 256
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to <mgr-host> port 9283: Connection refused`** — Verify the MGR host is correct and the prometheus module is actually running with `ceph mgr services`.
    **`Error ENOENT: mgr module 'prometheus' not found`** — Ensure you're running a Ceph version that includes the prometheus module (Luminous or later) and check `ceph versions`.
**Prometheus scrape config:**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: ceph
    static_configs:
      - targets:
          - mgr-host1:9283
          - mgr-host2:9283   # standby MGR (will return empty if not active)
    scrape_interval: 30s
    scrape_timeout: 10s
```

**Key metrics:**

| Metric | Description | Alert threshold |
|---|---|---|
| `ceph_health_status` | 0=OK, 1=WARN, 2=ERR | Alert on ≥ 1 for > 5 min |
| `ceph_osd_up` | 1 if OSD is up | Alert on any OSD down > 5 min |
| `ceph_osd_in` | 1 if OSD is in the cluster | Alert if in=0 unexpectedly |
| `ceph_pg_active` | Count of active PGs | Alert if drops below total expected |
| `ceph_cluster_total_bytes` | Raw total cluster capacity | Capacity planning |
| `ceph_cluster_total_used_bytes` | Raw used bytes | Alert at 80% utilization |
| `ceph_pool_rd` / `ceph_pool_wr` | Read/write IOPS per pool | Workload characterization |
| `ceph_osd_op_r_latency_sum` | OSD read latency | Alert if p99 > 10 ms |
| `ceph_mon_quorum_status` | 1 = MON in quorum | Alert if any MON leaves quorum |

## RGW (S3-Compatible Object Storage)

```bash
# Deploy RGW with cephadm
ceph orch apply rgw myorg --realm=default --zone=default --placement="2 host1 host2"

# Create S3 user
radosgw-admin user create --uid=s3user --display-name="S3 User" --access-key=AKID --secret=SECRET

# List buckets for a user
radosgw-admin bucket list --uid=s3user

# S3 endpoint: http://rgw.ceph.local:7480 (HTTP) or HTTPS with TLS

# Test with AWS CLI
aws s3 ls --endpoint-url http://rgw.ceph.local:7480 \
  --aws-access-key-id AKID --aws-secret-access-key SECRET

# Set bucket quota
radosgw-admin quota set --uid=s3user --quota-scope=bucket --max-size=10G
radosgw-admin quota enable --uid=s3user --quota-scope=bucket
```


```text title="Expected output"
Scheduled rgw update for service rgw.myorg
{
  "user_id": "s3user",
  "display_name": "S3 User",
  "email": "",
  "suspended": 0,
  "max_buckets": 1000,
  "auid": 0,
  "subusers": [],
  "keys": [
    {
      "user": "s3user",
      "access_key": "AKID",
      "secret_key": "SECRET"
    }
  ],
  "swift_keys": [],
  "caps": [],
  "op_mask": "read, write, delete",
  "default_placement": "",
  "default_storage_class": "",
  "placement_tags": [],
  "bucket_quota": {
    "enabled": false,
    "check_on_raw": false,
    "max_size": -1,
    "max_size_kb": 0,
    "max_objects": -1
  },
  "user_quota": {
    "enabled": false,
    "check_on_raw": false,
    "max_size": -1,
    "max_size_kb": 0,
    "max_objects": -1
  },
  "temp_url_keys": [],
  "type": "rgw",
  "mfa_ids": []
}
[]
2024-01-15T09:42:33.521Z 7f8c2a1b9e4d INFO: Bucket quota set for user s3user
2024-01-15T09:42:34.102Z 7f8c2a1b9e4d INFO: Bucket quota enabled for user s3user
```

!!! warning "Common errors"
    **`error: unable to connect to http://rgw.ceph.local:7480`** — Verify RGW service is running with `ceph orch ps | grep rgw` and check DNS resolution for rgw.ceph.local.
    **`error: invalid access key format`** — Use a valid AWS access key ID (typically 20 alphanumeric characters) instead of the placeholder AKID.
    **`error: user 's3user' does not exist`** — Create the user first with `radosgw-admin user create` before attempting quota operations.
## CephFS (Shared Filesystem)

```bash
# Create CephFS filesystem
ceph fs new myfs cephfs-meta cephfs-data

# Mount via kernel driver (Linux clients)
mount -t ceph ceph-mon1,ceph-mon2,ceph-mon3:/ /mnt/cephfs \
  -o name=admin,secretfile=/etc/ceph/admin.secret

# Mount via FUSE (userspace; slower but more portable)
ceph-fuse -m ceph-mon1:6789 /mnt/cephfs
```


```text title="Expected output"
new fs myfs
mount.ceph: trying to mount ABCDEF123456789@.ceph-mon1,ceph-mon2,ceph-mon3:/ at /mnt/cephfs
mount.ceph: mount failed: (1) Operation not permitted
2024-10-15T14:32:18.123456+0000 7f8a9c2d1e4f -1 init, newargc=7 newargv=[ceph-fuse,-m,ceph-mon1:6789,/mnt/cephfs]
ceph-fuse[12847]: starting ceph client
ceph-fuse[12847]: starting fuse
```

!!! warning "Common errors"
    **`mount.ceph: mount failed: (1) Operation not permitted`** — Verify the admin keyring exists at `/etc/ceph/admin.secret` with correct permissions (mode 0400) and the Ceph cluster is healthy with `ceph status`.
    **`ceph-fuse[PID]: error connecting to cluster`** — Ensure the monitor address is resolvable and port 6789 is accessible; check `/etc/ceph/ceph.conf` has correct `mon_host` entries.
    **`ceph fs new: Error EINVAL: filesystem name already exists`** — Drop the existing filesystem with `ceph fs rm myfs --yes-i-really-mean-it` before recreating it.
## NFS / Ganesha

NFS-Ganesha provides an NFS v4.1 export layer over CephFS, enabling non-Linux clients (ESXi, Windows via NFS client) to access Ceph storage.

```bash
# Enable NFS MGR module
ceph mgr module enable nfs

# Create NFS cluster (deploys Ganesha containers via cephadm)
ceph nfs cluster create my-nfs "2 nfs-host1 nfs-host2"

# List NFS clusters
ceph nfs cluster ls

# Create export: expose root of CephFS filesystem over NFS
ceph nfs export create cephfs my-nfs /export myfs

# Create export for a sub-path
ceph nfs export create cephfs my-nfs /export/apps myfs --path=/apps

# List active exports
ceph nfs export ls my-nfs

# Mount from a Linux client
mount -t nfs4 -o proto=tcp nfs-host1:/export /mnt/nfs-cephfs

# Check Ganesha service status
ceph orch ps | grep nfs
```


```text title="Expected output"
enabling module 'nfs'
NFS cluster 'my-nfs' created successfully
my-nfs
/export	myfs	[client_addr=0.0.0.0/0]
/export/apps	myfs	[client_addr=0.0.0.0/0,path=/apps]
/export	myfs	[client_addr=0.0.0.0/0]
/export/apps	myfs	[client_addr=0.0.0.0/0,path=/apps]
NAME                          HOST        PORTS   STATUS      REFRESHED   AGE  MEM_USE  MEM_LIM  CPU_USE
nfs.my-nfs.nfs-host1.abcdef   nfs-host1           running (2h)  2m ago    2h   512.0M   1.0G    0.12
nfs.my-nfs.nfs-host2.ghijkl   nfs-host2           running (2h)  2m ago    2h   498.0M   1.0G    0.08
```

!!! warning "Common errors"
    **`Error: NFS cluster 'my-nfs' already exists`** — Delete the existing cluster with `ceph nfs cluster rm my-nfs` before recreating it.
    **`mount.nfs4: No such file or directory`** — Verify the NFS export path exists on the CephFS filesystem and the Ganesha service is running with `ceph orch ps | grep nfs`.
    **`Error: NFS module not enabled`** — Run `ceph mgr module enable nfs` before attempting to create NFS clusters.
| Parameter | Value | Notes |
|---|---|---|
| NFS version | v4.1 | v4.0 and v3 also supported with extra config |
| Placement | 2+ Ganesha nodes | Active/active; client mounts either node |
| Export path | `/export/<name>` | Maps to CephFS path; sub-path exports supported |
| Auth | `sys` (default) or Kerberos | Kerberos requires `sec=krb5` mount option |
| HA | RAFT quorum (built-in) | Ganesha grace period handles failover transparently |

## See also

- [Ceph — How It Works](../how-it-works/)
- [Ceph — Deploy](../../deploy/)
