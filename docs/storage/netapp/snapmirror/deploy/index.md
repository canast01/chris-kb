---
tags:
  - deployment
  - netapp
search:
  boost: 1.5
---

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# SnapMirror — Initial Configuration

```text
┌───────────────────────────── NetApp SnapMirror — Configuration Sequence ──────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Source and destination ONTAP clusters on compatible versions (destination must be same or newer)     │
│  Intercluster LIFs: dedicated NICs per node, routable to each other; MTU 9000 recommended             │
│  IPs planned: one intercluster LIF per node on each cluster; dedicated replication VLAN or WAN        │
│  Licences: SnapMirror licence active on both clusters; check: license show -package SnapMirror        │
│  Destination volume: must be DP (data protection) type, equal or larger capacity than source          │
│                                                                                                       │
│                                        │  peer clusters                                               │
│                                        ▼                                                              │
│  Step 2 · Cluster and SVM Peering                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Create intercluster LIFs on each node: network interface create -role intercluster ...               │
│  Peer clusters: cluster peer create -peer-addrs <dest-intercluster-LIF-IPs> on source cluster         │
│  Accept on destination: cluster peer create -peer-addrs <source-intercluster-LIF-IPs>                 │
│  Peer SVMs: vserver peer create -vserver <src-svm> -peer-vserver <dst-svm> -applications snapmirror   │
│  Accept SVM peer on destination: vserver peer accept -vserver <dest-svm> -peer-vserver <source-svm>   │
│                                                                                                       │
│                                        │  create destination volume                                   │
│                                        ▼                                                              │
│  Step 3 · Create Destination DP Volume                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  On destination SVM: volume create -vserver <dest-svm> -volume <vol> -type DP -size <n>g -aggregate   │
│  DP volumes are read-only on destination — no data can be written directly; only via SnapMirror       │
│  Confirm volume exists: volume show -vserver <dest-svm> -volume <vol>                                 │
│                                                                                                       │
│                                        │  create relationship and initialise                          │
│                                        ▼                                                              │
│  Step 4 · Create SnapMirror Relationship and Initialise                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  snapmirror create -source-path <src-svm>:<vol> -destination-path <dst-svm>:<vol> -type DP            │
│  Set schedule: -schedule <cron-name> (e.g. hourly); set policy: -policy MirrorAllSnapshots            │
│  Initialise: snapmirror initialize -destination-path <dst-svm>:<vol> — triggers full baseline copy    │
│  Monitor: snapmirror show -destination-path <dst-svm>:<vol> — wait for Snapmirrored state             │
│                                                                                                       │
│                                        │  validate and monitor                                        │
│                                        ▼                                                              │
│  Step 5 · Validate and Baseline                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Confirm snapmirror show: Relationship Status = Idle, Mirror State = Snapmirrored                     │
│  Verify lag time: SnapMirror Lag Time should be ≤ scheduled RPO interval                              │
│  Test break/resync on a non-production relationship: snapmirror break / snapmirror resync             │
│  Record: relationship paths, policy name, schedule name, RPO target, initial baseline timestamp       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This guide covers configuring NetApp SnapMirror replication from initial cluster prerequisites through a validated first relationship with a scheduled RPO. Applies to ONTAP 9.10 and later.

---

## Prerequisites

**Two ONTAP clusters:**

- Source cluster: production data (AFF/FAS/ASA on ONTAP 9.10+)
- Destination cluster: DR or backup target (may be the same ONTAP version or newer — SnapMirror does not support replicating to older ONTAP versions)
- Both clusters running the same or compatible ONTAP major version

**Intercluster LIFs (required — not optional):**

- Dedicated network interfaces on each cluster for intercluster traffic
- Intercluster LIFs must be routable to each other — typically a dedicated replication VLAN or a WAN link
- Minimum one intercluster LIF per node on each cluster (best practice: one per node per fabric or bonded pair)
- MTU should match on both ends (9000 recommended for high-throughput replication over LAN)

**IP address plan:**

| Cluster      | Node   | Intercluster LIF IP |
|--------------|--------|---------------------|
| source-cls   | node1  | 10.0.20.11          |
| source-cls   | node2  | 10.0.20.12          |
| dest-cls     | node1  | 10.0.20.21          |
| dest-cls     | node2  | 10.0.20.22          |

**Licenses:**

- SnapMirror license active on both clusters:

```bash
system license show -package SnapMirror
# Status should be "licensed"
```

**Destination volume space:**

- The destination volume must be at least as large as the source volume. Create it before initializing SnapMirror (or let SnapMirror create it automatically with `snapmirror create -type DP` — ONTAP will auto-create if the destination volume does not exist and you specify the correct SVM and volume name).

---

## Configure Cluster Peering

Cluster peering establishes an authenticated, encrypted channel between the two ONTAP clusters. All SnapMirror and SnapVault relationships depend on this.

**Step 1 — Create intercluster LIFs on the source cluster:**

```bash
# Run on source cluster
network interface create -vserver source-cls -lif ic_lif_n1 -role intercluster \
  -home-node source-node1 -home-port e0f -address 10.0.20.11 -netmask 255.255.255.0

network interface create -vserver source-cls -lif ic_lif_n2 -role intercluster \
  -home-node source-node2 -home-port e0f -address 10.0.20.12 -netmask 255.255.255.0
```

**Step 2 — Create intercluster LIFs on the destination cluster:**

```bash
# Run on destination cluster
network interface create -vserver dest-cls -lif ic_lif_n1 -role intercluster \
  -home-node dest-node1 -home-port e0f -address 10.0.20.21 -netmask 255.255.255.0

network interface create -vserver dest-cls -lif ic_lif_n2 -role intercluster \
  -home-node dest-node2 -home-port e0f -address 10.0.20.22 -netmask 255.255.255.0
```

**Step 3 — Initiate peering from the source cluster:**

```bash
# On the source cluster:
cluster peer create -peer-addrs 10.0.20.21,10.0.20.22 -ipspace Default

# ONTAP prompts for a passphrase — enter one and record it
# Then, on the destination cluster, accept the peer:
cluster peer create -peer-addrs 10.0.20.11,10.0.20.12 -ipspace Default
# Enter the same passphrase when prompted
```

**Verify peering:**

```bash
# On either cluster:
cluster peer show
# Both clusters should show Availability: Available, Authentication: ok
```

---

## Configure SVM Peering

SVM peering authorizes SnapMirror replication between specific SVMs. This is a separate step from cluster peering.

```bash
# On the source cluster:
vserver peer create -vserver svm_prod -peer-vserver svm_dr -peer-cluster dest-cls -applications snapmirror

# On the destination cluster, accept:
vserver peer accept -vserver svm_dr -peer-vserver svm_prod
```

**Verify SVM peering:**

```bash
vserver peer show
# State should show "peered" for both SVMs
```

If replicating across multiple SVM pairs, repeat this step for each pair.

---

## Create First SnapMirror Relationship

SnapMirror relationships can be type **DP** (Data Protection — asynchronous) or **XDP** (Extended Data Protection — newer, with policy-based schedules). ONTAP 9.12+ defaults to XDP.

**Create a destination volume (if not already created):**

```bash
# On the destination cluster:
volume create -vserver svm_dr -volume vol_nfs_dr01 -aggregate aggr1_dest_node1 \
  -size 1TB -type DP
```

Note: `-type DP` marks the volume as a replication destination (read-only until failover).

**Create the SnapMirror relationship from the destination cluster:**

```bash
# Always create SnapMirror relationships from the DESTINATION cluster
snapmirror create \
  -source-path svm_prod:vol_nfs_data01 \
  -destination-path svm_dr:vol_nfs_dr01 \
  -type XDP \
  -policy MirrorAllSnapshots
```

The `MirrorAllSnapshots` policy is a built-in ONTAP policy that replicates all snapshots. For a tighter RPO with fewer snapshots replicated, use `MirrorLatest`.

**Verify the relationship was created:**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01
# Status: Idle, Health: true (before initialization)
```

---

## Initialize and Verify

Initialization transfers the full baseline data from source to destination. This is the longest step and time depends on source volume size and network bandwidth.

**Initiate initialization:**

```bash
# Run from the destination cluster:
snapmirror initialize -destination-path svm_dr:vol_nfs_dr01
```

**Monitor transfer progress:**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01
# Progress field shows bytes transferred
# Status: Transferring → Finalizing → Idle (when done)
```

For large volumes (multi-TB), the baseline transfer may take hours. Run this during a maintenance window or off-peak hours.

**Verify initialization completed:**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01 -fields mirror-state,lag-time,last-transfer-size
# mirror-state: Snapmirrored
# lag-time: should be minutes after initialization completes
```

Check that the destination volume contains data:

```bash
# On destination cluster:
volume show -vserver svm_dr -volume vol_nfs_dr01 -fields used
```

---

## Configure Schedule

After initialization, SnapMirror updates run on a schedule defined by a job schedule or the policy's schedule rules.

**Check existing schedules:**

```bash
job schedule cron show
# Built-in schedules: hourly, daily, weekly
```

**Create a custom schedule (every 15 minutes):**

```bash
job schedule cron create -name every_15min -minute 0,15,30,45
```

**Modify the SnapMirror relationship to use the schedule:**

```bash
snapmirror modify \
  -destination-path svm_dr:vol_nfs_dr01 \
  -schedule every_15min
```

**Trigger a manual update to confirm scheduled updates work:**

```bash
snapmirror update -destination-path svm_dr:vol_nfs_dr01
snapmirror show -destination-path svm_dr:vol_nfs_dr01
# Lag-time should decrease after the update completes
```

**View transfer history:**

```bash
snapmirror history show -destination-path svm_dr:vol_nfs_dr01
```

---

## Validate RPO

**Check lag time (RPO indicator):**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01 -fields lag-time
# Lag time should be less than the schedule interval (e.g., <15 minutes)
```

**Verify snapshots exist on the destination:**

```bash
snapshot show -vserver svm_dr -volume vol_nfs_dr01
# Snapshots named "sm_created" with SnapMirror timestamps should be present
```

**Test failover (planned failover test only — interrupts production):**

```bash
# Quiesce the relationship (stops replication):
snapmirror quiesce -destination-path svm_dr:vol_nfs_dr01

# Break the relationship to make the destination read-write:
snapmirror break -destination-path svm_dr:vol_nfs_dr01

# Mount and verify the destination volume data
# Mount it on a test host and confirm data is accessible and consistent

# After validation, resync back to normal replication (source→destination):
snapmirror resync -destination-path svm_dr:vol_nfs_dr01
```

Confirm the relationship is back to `Snapmirrored` and lag time is under the RPO target:

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01
```

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Snapmirror — Procedures](../operations/procedures/)
- [Snapmirror — Common Issues](../troubleshooting/common-issues/)
- [Snapmirror — How It Works](../architecture/how-it-works/)
