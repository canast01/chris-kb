# Ceph — Integrations

<div class="kb-summary">
Ceph integrations: Kubernetes CSI (Rook-Ceph), OpenStack Cinder/Glance/Swift, RBD for VM block storage, CephFS for shared filesystems, and S3-compatible RGW for object storage.
</div>

```text
┌──────────────────────────────── Ceph — Integrations ──────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Kubernetes: Rook operator manages Ceph inside K8s; CSI driver for PVC provisioning          │   │
│   │   OpenStack: Cinder (block), Glance (images), Manila (file), Swift (object) via RGW           │   │
│   │   RBD: thin-provisioned block devices; snapshots, clones, live resize without downtime        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Kubernetes (Rook-Ceph)

```yaml
# Rook deploys and manages Ceph inside Kubernetes
# Install via Helm:
# helm repo add rook-release https://charts.rook.io/release
# helm install --create-namespace rook-ceph rook-release/rook-ceph -n rook-ceph

# CephCluster custom resource
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
# StorageClass for RBD (block storage)
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

## OpenStack Integration

```bash
# Ceph as Cinder backend (block storage for VMs)
# /etc/cinder/cinder.conf
# [DEFAULT]
# enabled_backends = ceph
# [ceph]
# volume_driver = cinder.volume.drivers.rbd.RBDDriver
# rbd_pool = volumes
# rbd_ceph_conf = /etc/ceph/ceph.conf
# rbd_user = cinder

# Create Ceph user for Cinder
ceph auth get-or-create client.cinder \
  mon 'profile rbd' \
  osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images'

# Ceph as Glance backend (VM images)
# /etc/glance/glance-api.conf
# [glance_store]
# stores = rbd
# default_store = rbd
# rbd_store_pool = images
# rbd_store_user = glance
# rbd_store_ceph_conf = /etc/ceph/ceph.conf
```

## RGW (Object Storage / S3-Compatible)

```bash
# Deploy RGW with cephadm
ceph orch apply rgw myorg --realm=default --zone=default --placement="2 host1 host2"

# Create S3 user
radosgw-admin user create --uid=s3user --display-name="S3 User" --access-key=AKID --secret=SECRET

# List buckets
radosgw-admin bucket list --uid=s3user

# S3 endpoint (HAProxy or DNS round-robin over RGW nodes)
# http://rgw.ceph.local:7480  (HTTP) or HTTPS if TLS configured

# Test with AWS CLI
aws s3 ls --endpoint-url http://rgw.ceph.local:7480 \
  --aws-access-key-id AKID --aws-secret-access-key SECRET
```

## CephFS (Shared Filesystem)

```bash
# Create CephFS
ceph fs new myfs cephfs-meta cephfs-data

# Mount CephFS on a Linux client (kernel driver)
mount -t ceph ceph-mon1,ceph-mon2,ceph-mon3:/ /mnt/cephfs \
  -o name=admin,secretfile=/etc/ceph/admin.secret

# Mount CephFS via FUSE (userspace)
ceph-fuse -m ceph-mon1:6789 /mnt/cephfs

# NFS export of CephFS via NFS-Ganesha (for VMware or non-Linux clients)
ceph orch apply nfs myorg --placement="2 host1 host2"
ceph nfs export create cephfs myorg /export /    # export root of CephFS
```
