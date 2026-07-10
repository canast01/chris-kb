---
tags:
  - architecture
  - ceph
---
# Ceph — Design Standards

<div class="kb-summary">
Ceph cluster design: node and disk sizing, OSD-to-MON-to-MGR ratios, network separation (public vs cluster), CRUSH hierarchy for fault domains, and capacity planning rules.

*Applies to: Red Hat Ceph Storage · Upstream Ceph*
</div>

```d2
direction: right

TIERS: "Cluster Storage Tiers" {shape: rectangle}
NVMe: "All-NVMe\nLatency-sensitive workloads\nVM boot disks, databases\nHighest cost per TB" {shape: rectangle}
HYB: "Hybrid — NVMe cache + HDD capacity\nMixed workloads\nNVMe BlueStore WAL/DB\nHDD object data" {shape: rectangle}
HDD: "All-HDD\nCold / bulk storage\nArchive, backup targets\nLowest cost per TB" {shape: rectangle}
EC: "Erasure Coded\nCost-efficient bulk\nk=4 m=2 → 1.5x overhead\nNo RBD overwrite support" {shape: rectangle}

TIERS -> NVMe
TIERS -> HYB
TIERS -> HDD
TIERS -> EC
```

```d2
direction: down

cluster_sizing: "Cluster Sizing" {shape: rectangle}
node_hardware_recommendations: "Node Hardware Recommendations" {shape: rectangle}
replication_vs_erasure_coding: "Replication vs Erasure Coding" {shape: rectangle}
crush_map_design: "CRUSH Map Design" {shape: rectangle}
pg_count_formula: "PG Count Formula" {shape: rectangle}
network_design: "Network Design" {shape: rectangle}

cluster_sizing -> node_hardware_recommendations: hardens
node_hardware_recommendations -> replication_vs_erasure_coding: hardens
replication_vs_erasure_coding -> crush_map_design: hardens
crush_map_design -> pg_count_formula: hardens
pg_count_formula -> network_design: hardens
```

## Cluster Sizing

| Scale | OSD Nodes | Total OSDs | MONs | MGRs | Notes |
|---|---|---|---|---|---|
| Small | 3 | 10–30 | 3 | 2 | All daemons may share nodes; separate MON/OSD recommended |
| Medium | 6–10 | 60–120 | 3–5 | 2 | Dedicated MON/MGR nodes; rack-level failure domain |
| Large | 12+ | 200+ | 5 | 2 | Dedicated MON/MGR nodes mandatory; consider multi-site |

**MON/MGR placement rules:**
- Small clusters (≤ 5 nodes): MON and MGR may share OSD nodes.
- Medium+ clusters: dedicate at least 3 nodes for MON + MGR to prevent MON quorum loss during OSD node failure.
- Never place more than 1 MON on the same physical host (violates quorum fault tolerance).
- MGR active/standby must be on different hosts. Both must be running at all times.

## Node Hardware Recommendations

| Role | vCPU | RAM | NIC | Disk |
|---|---|---|---|---|
| MON / MGR node | 4+ | 32 GB | 1× 10 GbE (public) | 100 GB OS + 100 GB MON DB SSD |
| OSD node (HDD) | 2 per OSD | 4–6 GB per OSD + 16 GB base | 2× 25 GbE (public + cluster) | 1× NVMe WAL/DB per 4–6 HDDs; HDDs for data |
| OSD node (NVMe) | 4 per OSD | 4 GB per OSD + 16 GB base | 2× 25 GbE or 1× 100 GbE | 1 NVMe per OSD; no separate WAL/DB device needed |
| MDS node | 8+ | 64 GB+ | 1× 10 GbE | 100 GB OS SSD |
| RGW node | 8+ | 32 GB | 2× 10 GbE | 100 GB OS SSD |

## Replication vs Erasure Coding

| Property | Replicated (size=3) | Erasure Coded (k=4, m=2) |
|---|---|---|
| Raw overhead | 3× | 1.5× |
| Minimum OSDs | 3 | k+m = 6 |
| Write IOPS impact | Low | Higher (encoding CPU cost) |
| Read IOPS | Full random read from any replica | Decode overhead on partial reads |
| RBD support | Full (including overwrites) | Partial (requires BlueStore + EC overwrites enabled) |
| CephFS support | Yes | Data pool only (metadata pool must be replicated) |
| Recovery cost | Copy full objects | Rebuild from k shards — less data transferred |
| Use case | VM disks, databases, latency-sensitive | Cold storage, backups, bulk object store |

## CRUSH Map Design

**Failure domain selection:**

| Cluster size | Recommended failure domain | Rationale |
|---|---|---|
| 3 nodes | `host` | Only 3 failure domains available |
| 6–12 nodes (2–4 per rack) | `rack` | Rack power/switch failure isolated |
| 12+ nodes, multi-AZ | `datacenter` | AZ-level fault tolerance |

```bash
# Create rack-level CRUSH rule
ceph osd crush rule create-replicated rack_replicated default rack firstn

# Assign pool to rack rule
ceph osd pool set rbd-pool crush_rule rack_replicated

# Mixed media — separate CRUSH roots for SSD and HDD pools
# Add SSD OSDs to a separate root
ceph osd crush add-bucket ssd-root root
ceph osd crush set-bucket-item ssd-root ssd-host1
ceph osd crush rule create-replicated ssd_rule ssd-root host firstn

# Assign weight (in TB) to each OSD
ceph osd crush reweight osd.5 3.64      # 4 TB HDD = 3.64 usable TB

# View full CRUSH tree with weights
ceph osd crush tree --show-shadow
ceph osd df tree
```


```text title="Expected output"
created rule rack_replicated at (2)
set pool 0 crush_rule to rack_replicated
added bucket ssd-root of type root to crush tree
set item ssd-root weight to 1 in bucket default
created rule ssd_rule at (3)
reweighted item osd.5 to 3.64 in crush tree
ID  CLASS WEIGHT   TYPE NAME
-13       10.92    root ssd-root
-12        3.64     host ssd-host1
  5   hdd  3.64      osd.5
 -1       36.48    root default
 -2        7.28     rack rack1
  0   hdd  3.64      osd.0
  1   hdd  3.64      osd.1
 -3        7.28     rack rack2
  2   hdd  3.64      osd.2
  3   hdd  3.64      osd.3

HOST WEIGHT REWEIGHT SIZE   USE    AVAIL   %USE PGS STATUS
ssd-host1 3.64  1.00    4.0T  1.2T   2.8T  30.0  128 up
rack1     7.28  1.00    8.0T  2.4T   5.6T  30.0  256 up
rack2     7.28  1.00    8.0T  2.4T   5.6T  30.0  256 up
```

!!! warning "Common errors"
    **`Error ENOENT: crush rule 'rack_replicated' does not exist`** — Ensure the rule was created successfully before assigning it to a pool; check with `ceph osd crush rule ls`.
    **`Error EINVAL: invalid crush rule name 'ssd_rule'`** — Verify the ssd_rule was created with the correct root bucket name using `ceph osd crush rule dump ssd_rule`.
## PG Count Formula

```text
PGs per pool = (Total OSDs × 100) / pool_size
```

Round the result up to the next power of 2. Keep total PGs per OSD ≤ 250 across all pools.

| OSDs | Pool size | Raw result | Rounded (power of 2) |
|---|---|---|---|
| 30 | 3 | 1000 | 1024 |
| 60 | 3 | 2000 | 2048 |
| 120 | 3 | 4000 | 4096 |
| 30 | 2 | 1500 | 2048 |

**PG autoscaler** (default on in Octopus+) handles PG count automatically:

```bash
# Check autoscaler status
ceph osd pool autoscale-status

# Enable autoscaler on a specific pool
ceph osd pool set rbd-pool pg_autoscale_mode on

# Set target ratio (autoscaler calculates PGs based on % of cluster)
ceph osd pool set rbd-pool target_size_ratio 0.4   # 40% of cluster capacity

# Disable autoscaler globally (use manual PG counts)
ceph config set global osd_pool_default_pg_autoscale_mode off
```


```text title="Expected output"
POOL                 SIZE  TARGET SIZE  RATIO  EFFECTIVE RATIO  BIAS  PG_NUM  NEW PG_NUM  AUTOSCALE
rbd-pool            12.4G       50.0G  0.248        0.248        1.0    128       256       on
metadata             2.1G        8.0G  0.263        0.263        4.0     32        32       on
.rgw.root           512M        2.0G  0.256        0.256        1.0      8         8       on

(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error ENOENT: pool 'rbd-pool' does not exist`** — Verify the pool name with `ceph osd pool ls` and use the correct pool identifier.
    **`Error EINVAL: invalid pg_autoscale_mode 'on'`** — Use valid values `off`, `warn`, or `on` (ensure no typos in the mode string).
## Network Design

```text
Two networks required:
  Public network:   10.0.1.0/24   → client-to-OSD traffic (reads, writes)
  Cluster network:  10.0.2.0/24   → OSD-to-OSD replication and recovery

Why separate?
  Without a cluster network, recovery/replication traffic consumes client I/O bandwidth.
  Recovery after a disk failure can generate 100–500 Mbps per OSD.

Bandwidth guidelines:
  Public:  10 GbE minimum per OSD node; 25 GbE for NVMe-heavy clusters
  Cluster: 25 GbE minimum; 100 GbE for dense NVMe nodes (50+ OSDs per node)
```

| Network | Minimum | Recommended | Notes |
|---|---|---|---|
| Public (client I/O) | 10 GbE | 25 GbE | Carries client reads/writes to OSDs |
| Cluster (replication) | 10 GbE | 25 GbE; 100 GbE for NVMe nodes | Carries OSD-to-OSD replication; no client traffic |
| MTU | 1500 | 9000 (jumbo frames) | Enable jumbo frames on cluster network for replication throughput |
| Bonding | Optional | Recommended (LACP) | 2× NICs bonded for redundancy on both networks |

```bash
# Verify Ceph is using separate networks (from ceph.conf or cephadm config)
ceph config get osd public_network
ceph config get osd cluster_network

# Set cluster network (if not already configured)
ceph config set global public_network 10.0.1.0/24
ceph config set global cluster_network 10.0.2.0/24
```


```text title="Expected output"
10.0.1.0/24
10.0.2.0/24
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error EINVAL: invalid value '10.0.1.0/24' for option 'public_network'`** — Ensure the CIDR notation is valid and the network actually exists in your infrastructure.
    **`Error: failed to set config option 'cluster_network': Permission denied`** — Run the command with appropriate ceph admin privileges or use `sudo ceph config set`.
## Capacity Planning

```text
Replicated pool (size=3):
  Raw capacity needed = usable × 3
  Safety threshold: never exceed 85% full (ceph warns at nearfull ratio)
  Full threshold: cluster stops writes at 95% (full ratio)

Erasure-coded pool (k=4, m=2):
  Raw capacity needed = usable × 1.5
  Better efficiency but slightly more complex recovery

OSD count formula:
  OSDs = Usable capacity target (TB) × replication factor / disk size (TB)
  Example: 100 TB usable, replica=3, 8 TB disks: (100 × 3) / 8 = 37.5 → 40 OSDs

PG count formula:
  PGs per pool = (Total OSDs × 100) / pool size (round to power of 2)
  Total PGs across all pools: aim for 100–200 per OSD
```

```bash
# Check cluster capacity and usage
ceph df
ceph df detail

# Check per-OSD usage
ceph osd df

# Adjust nearfull and full thresholds
ceph config set global mon_osd_nearfull_ratio 0.80
ceph config set global mon_osd_full_ratio 0.90
ceph config set global mon_osd_backfillfull_ratio 0.85
```


```text title="Expected output"
RAW STORAGE:
    CLASS     SIZE        AVAIL       USED        RAW USED     %RAW USED
    ssd       1.099 TiB   892.3 GiB   206.7 GiB   206.7 GiB       18.81
    TOTAL     1.099 TiB   892.3 GiB   206.7 GiB   206.7 GiB       18.81

POOLS:
    POOL                     ID     STORED      OBJECTS     USED        %USED     MAX AVAIL
    device_health_metrics     1     1.2 MiB        256      3.6 MiB      0.00      297.4 GiB
    rbd-pool                  2     142.5 GiB   36521      427.5 GiB    47.89      297.4 GiB
    cephfs_data               3     58.3 GiB    14892      174.9 GiB    19.60      297.4 GiB
    cephfs_metadata           4     512 MiB      8124      1.5 GiB      0.17      297.4 GiB

OSD     CLASS  WEIGHT   REWEIGHT   SIZE        RAW USE     %USE     VAR      PGS   STATUS
0       ssd    1.00000  1.00000    366.4 GiB   68.9 GiB    18.81    1.00     256   up
1       ssd    1.00000  1.00000    366.4 GiB   68.9 GiB    18.81    1.00     256   up
2       ssd    1.00000  1.00000    366.4 GiB   68.9 GiB    18.81    1.00     256   up

(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error EACCES: access denied`** — Ensure the user running the command has appropriate Ceph admin capabilities or is part of the ceph group.
    **`Error: unknown command`** — Verify the Ceph version supports the `ceph config set` syntax; older versions may require `ceph tell mon.\* config set` instead.
## CRUSH Hierarchy Design

```bash
# Standard CRUSH hierarchy: datacenter → room → rack → host → OSD
# Minimum failure domain: host (3 hosts = 3 failure domains for replica=3)

# Example CRUSH rule for host-level failure domain
ceph osd crush rule create-replicated replicated_rule default host firstn

# Rack-level failure domain (better fault isolation)
ceph osd crush rule create-replicated rack_rule default rack firstn

# Assign pool to rack-level rule
ceph osd pool set rbd-pool crush_rule rack_rule

# Verify OSD placement
ceph osd crush tree
ceph osd df tree
```


```text title="Expected output"
created rule replicated_rule
created rule rack_rule
set pool 'rbd-pool' crush_rule to rack_rule
ID CLASS WEIGHT  TYPE NAME                                    UP/DOWN REWEIGHT PRIMARY-AFFINITY
-1       270.00 root default
-3       90.00     datacenter dc1
-5       45.00         room room-a
-7       15.00             rack rack-01
 0   ssd  5.00                 host osd-node-01
 1   ssd  5.00                 host osd-node-02
 2   ssd  5.00                 host osd-node-03
-9       30.00             rack rack-02
 3   ssd  5.00                 host osd-node-04
 4   ssd  5.00                 host osd-node-05
 5   ssd  5.00                 host osd-node-06

ID CLASS WEIGHT  REWEIGHT SIZE    RAW USE %USE  VAR  PGS STATUS
 0   ssd  5.00   1.00000 5.0G  2.1G 42.00 0.98  156    up
 1   ssd  5.00   1.00000 5.0G  2.0G 40.00 0.93  154    up
 2   ssd  5.00   1.00000 5.0G  2.2G 44.00 1.02  158    up
...
```

!!! warning "Common errors"
    **`Error EINVAL: invalid crush rule name 'rack_rule'`** — Verify the rule was created successfully with `ceph osd crush rule ls` and check for typos in the pool set command.
    **`Error ENOENT: pool 'rbd-pool' does not exist`** — Create the pool first with `ceph osd pool create rbd-pool <pg_num> <pgp_num>` before assigning a crush rule.
## Upgrade and Maintenance Standards

```bash
# Check cluster compatibility before upgrade
ceph versions                     # lists all daemon versions in cluster
ceph osd require-osd-release quincy  # set minimum OSD release gate

# Drain OSDs on a node before maintenance (graceful)
ceph osd set noout               # prevent OSDs from being marked out during maint
# --- perform maintenance ---
ceph osd unset noout             # re-enable after returning node to service

# Full set of maintenance flags
ceph osd set norecover           # pause all recovery
ceph osd set norebalance         # pause rebalancing
ceph osd set nobackfill          # pause backfill
ceph osd unset norecover
ceph osd unset norebalance
ceph osd unset nobackfill
```


```text title="Expected output"
{
  "mon": {
    "ceph version 17.2.6 (quincy)": 2
  },
  "mgr": {
    "ceph version 17.2.6 (quincy)": 2
  },
  "osd": {
    "ceph version 17.2.6 (quincy)": 24,
    "ceph version 17.2.5 (quincy)": 2
  },
  "mds": {}
}
set require_osd_release = quincy
noout is set
(no output — command completes silently)
norecover is set
norebalance is set
nobackfill is set
norecover is unset
norebalance is unset
nobackfill is unset
```

!!! warning "Common errors"
    **`Error EACCES: access denied`** — Ensure you have admin-level Ceph credentials or run with appropriate `ceph` keyring permissions.
    **`Error EINVAL: invalid value`** — Verify the release name matches a supported Ceph version (e.g., quincy, reef) and check cluster status with `ceph status` first.
| Flag | Effect | When to use |
|---|---|---|
| `noout` | Prevents OSDs from being marked out | Node maintenance, short outages |
| `norecover` | Stops recovery operations | Prevents I/O saturation during maintenance |
| `norebalance` | Stops rebalancing after OSD addition | Adding multiple OSDs in a batch |
| `nobackfill` | Stops backfill to new OSDs | Controlled rollout of new nodes |
| `pause` | Pauses all client I/O | Emergency cluster freeze |

## cephadm Orchestration Commands

```bash
# View all running daemons
ceph orch ps

# Deploy additional MON
ceph orch apply mon --placement="host1,host2,host3"

# Add OSDs from a specific host/device
ceph orch daemon add osd host1:/dev/sdb

# Remove an OSD gracefully (marks out, waits for clean, then removes)
ceph orch osd rm osd.12 --replace

# Check orchestrator status
ceph orch status
ceph orch ls
```


```text title="Expected output"
NAME                 HOST      STATUS        REFRESHED  AGE  VERSION   IMAGE ID      CONTAINER ID
mon.a                host1     running (15h)  2m ago     8d   17.2.5    abc123def456  pod-mon-a-xyz
mon.b                host2     running (15h)  2m ago     8d   17.2.5    abc123def456  pod-mon-b-xyz
mon.c                host3     running (15h)  2m ago     8d   17.2.5    abc123def456  pod-mon-c-xyz
osd.0                host1     running (12h)  1m ago     45d  17.2.5    abc123def456  pod-osd-0-abc
osd.1                host2     running (12h)  1m ago     45d  17.2.5    abc123def456  pod-osd-1-def
osd.2                host3     running (12h)  1m ago     45d  17.2.5    abc123def456  pod-osd-2-ghi
mgr.host1.abcd12     host1     running (8h)   3m ago     8d   17.2.5    abc123def456  pod-mgr-xyz

Scheduled to deploy mon on hosts: host1, host2, host3
(no output — command completes silently)

Created osd.13 on host1 device /dev/sdb
(no output — command completes silently)

Removing osd.12 (marked out, waiting for rebalance to complete)
osd.12 marked out. Waiting for PGs to rebalance...
osd.12 removed successfully

Orchestrator: ceph-rook
Backend: rook
Available: Yes

SERVICE         PORTS   RUNNING  REFRESHED  AGE  PLACEMENT
alertmanager            1        2m ago     8d   count:1
crash                   6        2m ago     8d   *
grafana         3000    1        2m ago     8d   count:1
mds.cephfs      -       2        2m ago     8d   label:mds=true
mon             3300    3        2m ago     8d   host1,host2,host3
mgr             8443    2        2m ago     8d   label:mgr=true
osd             -       3        2m ago     8d   *
prometheus      9095    1        2m ago     8d   count:1
```

!!! warning "Common errors"
    **`Error: osd.12 is still rebalancing, cannot remove yet`** — Wait for the cluster to reach a healthy state (ceph health) before attempting removal.
    **`Error: host1 is not in the orchestrator inventory`** — Verify the host is added to the cluster with `ceph orch host ls` and ensure it has a valid IP and SSH connectivity.
    **`Error: /dev/sdb does not exist or is already in use on host1`** — Confirm the device path with `lsblk` on the target host and ensure it is not already part of another OSD.
## See also

- [Ceph — How It Works](../how-it-works/)
- [Ceph — Deploy](../../deploy/)
