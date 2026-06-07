# Ceph — Deploy

<!-- diagram:ceph-deploy -->

<div class="kb-summary">
Ceph deployment with cephadm: bootstrap on first node, add MONs and OSDs, create initial pools, configure network, and validate cluster health before production use.
</div>

```text
┌─────────────────────────────────────────── Ceph Deployment ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Ceph Deployment with cephadm                                 │   │
│   │                   cephadm manages Ceph daemons as containers (Podman/Docker)                  │   │
│   │            Sequence: bootstrap first MON → add hosts → add MONs → add OSDs → pools            │   │
│   │              Bootstrap: cephadm bootstrap --mon-ip <ip> --cluster-network <CIDR>              │   │
│   │                 Validation: HEALTH_OK + all OSDs up+in + PGs all active+clean                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│    cephadm   = Ceph Admin tool; deploys and manages Ceph daemons as containers                        │
│    Bootstrap = First command; creates initial MON + MGR on one node                                   │
│    noout flag= Prevent OSDs from being marked out during maintenance                                  │
│                                                                                                       │
```

## Bootstrap

```bash
# Prerequisites:
# - All nodes: Python 3, Docker or Podman, NTP sync, cluster + public networks configured
# - SSH key-based root access from bootstrap node to all other nodes

# Install cephadm on bootstrap node (Reef/Quincy)
curl --silent --remote-name --location https://download.ceph.com/rpm-reef/el9/noarch/cephadm
chmod +x cephadm
./cephadm install

# Bootstrap first MON + MGR
cephadm bootstrap \
  --mon-ip 10.0.1.10 \
  --cluster-network 10.0.2.0/24 \
  --initial-dashboard-user admin \
  --initial-dashboard-password 'ChangeMe!'

# Access Ceph Dashboard: https://10.0.1.10:8443
```

## Add Hosts

```bash
# Copy SSH public key to each new node
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-node2
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-node3

# Add hosts to cluster
ceph orch host add ceph-node2 10.0.1.11
ceph orch host add ceph-node3 10.0.1.12

# Verify hosts
ceph orch host ls

# Add MONs (3 minimum; 5 for large clusters)
ceph orch apply mon 3  # or: ceph orch apply mon --placement "host1 host2 host3"

# Verify MON quorum
ceph mon stat
```

## Add OSDs

```bash
# Option A: Auto-detect and add all available disks
ceph orch apply osd --all-available-devices

# Option B: Specify devices per host
ceph orch daemon add osd ceph-node1:/dev/sdb
ceph orch daemon add osd ceph-node1:/dev/sdc
ceph orch daemon add osd ceph-node2:/dev/sdb

# Verify OSDs are up+in
ceph osd tree
ceph osd stat  # Expected: X osds, X up, X in

# Check OSD status in detail
ceph osd df
```

## Create Initial Pools

```bash
# RBD pool (block storage)
ceph osd pool create rbd 64
ceph osd pool application enable rbd rbd
rbd pool init rbd

# CephFS pools (if deploying filesystem)
ceph osd pool create cephfs-data 64
ceph osd pool create cephfs-meta 16
ceph fs new myfs cephfs-meta cephfs-data

# RGW pool (if deploying object storage)
# cephadm creates pools automatically when RGW is deployed
ceph orch apply rgw myorg --realm=default --zone=default --placement="2 ceph-node1 ceph-node2"
```

## Post-Deploy Validation

```bash
# Full cluster health check
ceph health detail
ceph status
# Expected: HEALTH_OK, all OSDs up+in, MON quorum established

# Performance test (pre-production baseline)
ceph osd bench 1073741824 4096   # 1 GB test, 4 KB I/O

# RBD test
rbd bench --io-type write --io-size 4K --io-threads 16 --io-total 1G rbd/test-image

# Verify CRUSH is placing data correctly
ceph osd perf
ceph pg dump pools   # check distribution
```
