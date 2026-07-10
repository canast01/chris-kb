---
tags:
  - deployment
  - netapp
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
configure_cluster_peering: "Configure Cluster Peering" {shape: rectangle}
configure_svm_peering: "Configure SVM Peering" {shape: rectangle}
create_first_snapmirror_relationship: "Create First SnapMirror Relationship" {shape: rectangle}
initialize_and_verify: "Initialize and Verify" {shape: rectangle}
configure_schedule: "Configure Schedule" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> configure_cluster_peering
configure_cluster_peering -> configure_svm_peering
configure_svm_peering -> create_first_snapmirror_relationship
create_first_snapmirror_relationship -> initialize_and_verify
initialize_and_verify -> configure_schedule
configure_schedule -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# SnapMirror — Initial Configuration

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


```text title="Expected output"
Package           License Status
SnapMirror        licensed
```

!!! warning "Common errors"
    **`Error: command not found: system`** — Ensure you are connected to the NetApp cluster via SSH or the CLI interface; this command only works on ONTAP systems.
    **`Package           License Status`** — If only headers appear with no data rows, run `system license show` without filters to verify SnapMirror is installed, then contact NetApp support if the package is missing.
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


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: Invalid home port e0f`** — Verify the port exists on the node with `network port show -node source-node1` and use the correct port name (e.g., e0e, e0g).
    **`Error: command failed: Vserver "source-cls" does not exist`** — Create the cluster vserver first or use the correct vserver name with `vserver show`.
    **`Error: command failed: Address 10.0.20.11 already in use`** — Confirm the IP address is not assigned to another interface or device on the network.
**Step 2 — Create intercluster LIFs on the destination cluster:**

```bash
# Run on destination cluster
network interface create -vserver dest-cls -lif ic_lif_n1 -role intercluster \
  -home-node dest-node1 -home-port e0f -address 10.0.20.21 -netmask 255.255.255.0

network interface create -vserver dest-cls -lif ic_lif_n2 -role intercluster \
  -home-node dest-node2 -home-port e0f -address 10.0.20.22 -netmask 255.255.255.0
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: The specified node "dest-node1" does not exist.`** — Verify node names match your cluster with `cluster show` and correct the `-home-node` parameter.
    **`Error: command failed: Port "e0f" does not exist on node "dest-node1".`** — Check available ports on each node using `network port show -node dest-node1` and update the `-home-port` parameter accordingly.
    **`Error: command failed: The IP address 10.0.20.21 is already in use.`** — Ensure the intercluster IP addresses are unique and not assigned to other interfaces; verify with `network interface show -fields address`.
**Step 3 — Initiate peering from the source cluster:**

```bash
# On the source cluster:
cluster peer create -peer-addrs 10.0.20.21,10.0.20.22 -ipspace Default

# ONTAP prompts for a passphrase — enter one and record it
# Then, on the destination cluster, accept the peer:
cluster peer create -peer-addrs 10.0.20.11,10.0.20.12 -ipspace Default
# Enter the same passphrase when prompted
```


```text title="Expected output"
cluster peer create -peer-addrs 10.0.20.21,10.0.20.22 -ipspace Default
Enter the passphrase for SVM peering [hidden]:
Passphrase for SVM peering [hidden]:
Cluster peering request created successfully.

cluster peer create -peer-addrs 10.0.20.11,10.0.20.12 -ipspace Default
Enter the passphrase for SVM peering [hidden]:
Passphrase for SVM peering [hidden]:
Cluster peering request created successfully.
Cluster peer accepted.
```

!!! warning "Common errors"
    **`Error: Failed to reach peer cluster at address 10.0.20.21`** — Verify network connectivity between clusters and confirm peer IP addresses are reachable on the management network.
    **`Error: Passphrase mismatch`** — Ensure the same passphrase is entered on both the source and destination clusters; re-run the command and use identical input.
    **`Error: Cluster peer already exists`** — Check existing peer relationships with `cluster peer show` and remove the old peer before creating a new one.
**Verify peering:**

```bash
# On either cluster:
cluster peer show
# Both clusters should show Availability: Available, Authentication: ok
```


```text title="Expected output"
Cluster                               Availability Authentication
------------------------------------ ------------ --------------
cluster1.example.com                  Available    ok
cluster2.example.com                  Available    ok
```

!!! warning "Common errors"
    **`Error: command not found: cluster`** — Ensure you are logged into the NetApp cluster CLI (SSH to cluster management IP) rather than a standard Linux shell.
    **`Cluster peer show: command not found`** — Run the command without the leading `cluster` keyword if using the ONTAP CLI directly, or verify ONTAP version supports this command syntax.
---

## Configure SVM Peering

SVM peering authorizes SnapMirror replication between specific SVMs. This is a separate step from cluster peering.

```bash
# On the source cluster:
vserver peer create -vserver svm_prod -peer-vserver svm_dr -peer-cluster dest-cls -applications snapmirror

# On the destination cluster, accept:
vserver peer accept -vserver svm_dr -peer-vserver svm_prod
```


```text title="Expected output"
# On the source cluster:
vserver peer create -vserver svm_prod -peer-vserver svm_dr -peer-cluster dest-cls -applications snapmirror
[Job 1234] Job succeeded: Vserver peer create completed successfully.

# On the destination cluster, accept:
vserver peer accept -vserver svm_dr -peer-vserver svm_prod
[Job 5678] Job succeeded: Vserver peer accept completed successfully.
```

!!! warning "Common errors"
    **`Error: command failed: Vserver peer create failed. Peer vserver "svm_dr" does not exist on cluster "dest-cls".`** — Verify the destination SVM name matches exactly and exists on the destination cluster using `vserver show`.
    **`Error: command failed: Vserver peer accept failed. No pending vserver peer request found for peer vserver "svm_prod".`** — Ensure the source cluster peer creation command completed successfully before attempting to accept on the destination.
**Verify SVM peering:**

```bash
vserver peer show
# State should show "peered" for both SVMs
```


```text title="Expected output"
Vserver     Peer Vserver     Peer State    Peer Cluster
-----------  ---------------  -----------   ----------------
svm-prod     svm-dr           peered        cluster-dr.example.com
svm-prod     svm-backup       peered        cluster-backup.example.com
svm-test     svm-test-dr      peered        cluster-dr.example.com
```

!!! warning "Common errors"
    **`Error: command not found: vserver`** — Ensure you are logged into the NetApp cluster CLI (ssh to cluster management IP) rather than a local shell.
    **`Vserver     Peer Vserver     Peer State    Peer Cluster` (no data rows)** — Create the vserver peer relationship first using `vserver peer create -vserver <local-svm> -peer-vserver <remote-svm> -peer-cluster <remote-cluster>`.
    **`peered (Unreachable)`** — Verify network connectivity between clusters and check firewall rules allow port 11104 (intercluster communication) between cluster management IPs.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: Cannot create volume on aggregate "aggr1_dest_node1": No space available`** — Verify the destination aggregate has at least 1.2TB free space using `storage aggregate show -fields availablesize`.
    **`Error: command failed: Vserver "svm_dr" does not exist`** — Create the destination SVM first using `vserver create -vserver svm_dr -rootvolume root_vol_svm_dr -aggregate aggr1_dest_node1`.
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


```text title="Expected output"
Operation succeeded: SnapMirror relationship created.
Source:      svm_prod:vol_nfs_data01
Destination: svm_dr:vol_nfs_dr01
Relationship Type: XDP
Policy: MirrorAllSnapshots
Status: Idle
Last Transfer Size: -
Last Transfer Duration: -
Network Compression Ratio: -
Unhealthy Reason: -
```

!!! warning "Common errors"
    **`Error: command failed: Relationship already exists.`** — Verify the destination volume doesn't already have an active SnapMirror relationship using `snapmirror show -destination-path svm_dr:vol_nfs_dr01`.
    **`Error: command failed: Source volume svm_prod:vol_nfs_data01 not found.`** — Confirm the source SVM and volume names are correct and exist on the source cluster using `volume show -vserver svm_prod`.
    **`Error: command failed: Destination volume does not exist.`** — Create the destination volume first with `volume create -vserver svm_dr -volume vol_nfs_dr01 -aggregate aggr_dr01 -size 1TB -type DP`.
The `MirrorAllSnapshots` policy is a built-in ONTAP policy that replicates all snapshots. For a tighter RPO with fewer snapshots replicated, use `MirrorLatest`.

**Verify the relationship was created:**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01
# Status: Idle, Health: true (before initialization)
```


```text title="Expected output"
Source Path: svm_prod:vol_nfs_01
                                           Destination Path: svm_dr:vol_nfs_dr01
                                                    Relationship ID: 12a3b4c5-6789-0def-1234-567890abcdef
                                               Relationship Type: XDP
                                                    SnapMirror Policy: MirrorAllSnapshots
                                                         Lag Time: -
                                             Last Transfer Type: -
                                               Last Transfer Size: -
                                            Last Transfer Duration: -
                                            Last Transfer From: -
                                                  FSxAdmin Vserver: svm_dr
                                                     Healthy: true
                                          In Sync Status: false
                                    Mirror State: Uninitialized
                                  File Restore State: None
                                 Relational State: Idle
```

!!! warning "Common errors"
    **`Error: command failed: There is no SnapMirror relationship with destination path "svm_dr:vol_nfs_dr01"`** — Verify the destination SVM and volume names are correct using `snapmirror show` without filters.
    **`Error: command failed: This operation is not permitted: SnapMirror relationship is not initialized`** — Initialize the relationship first with `snapmirror initialize -destination-path svm_dr:vol_nfs_dr01` before performing transfers.
---

## Initialize and Verify

Initialization transfers the full baseline data from source to destination. This is the longest step and time depends on source volume size and network bandwidth.

**Initiate initialization:**

```bash
# Run from the destination cluster:
snapmirror initialize -destination-path svm_dr:vol_nfs_dr01
```


```text title="Expected output"
Operation is queued: SnapMirror initialize of destination "svm_dr:vol_nfs_dr01" has been queued.
```

!!! warning "Common errors"
    **`Error: "svm_dr:vol_nfs_dr01" does not exist.`** — Create the destination volume first using `volume create -vserver svm_dr -volume vol_nfs_dr01 -aggregate aggr1 -size 1TB -type DP`.
    **`Error: SnapMirror relationship does not exist for "svm_dr:vol_nfs_dr01".`** — Create the SnapMirror relationship first using `snapmirror create -source-path svm_src:vol_nfs_src01 -destination-path svm_dr:vol_nfs_dr01 -type XDP -policy MirrorAllSnapshots`.
**Monitor transfer progress:**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01
# Progress field shows bytes transferred
# Status: Transferring → Finalizing → Idle (when done)
```


```text title="Expected output"
Progress
Source Destination Mirror State Status Healthy Updated
svm_prod:vol_nfs_prod01 svm_dr:vol_nfs_dr01 XDP Snapmirrored Transferring true 09/14 14:32:18
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are logged into the NetApp cluster CLI (via SSH to cluster management IP) rather than a local shell.
    **`Error: Invalid destination path "svm_dr:vol_nfs_dr01"`** — Verify the SVM and volume names exist on the destination cluster using `volume show` and confirm SnapMirror relationship was initialized with `snapmirror initialize`.
For large volumes (multi-TB), the baseline transfer may take hours. Run this during a maintenance window or off-peak hours.

**Verify initialization completed:**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01 -fields mirror-state,lag-time,last-transfer-size
# mirror-state: Snapmirrored
# lag-time: should be minutes after initialization completes
```


```text title="Expected output"
Destination Path                State    Lag Time             Last Transfer Size
svm_dr:vol_nfs_dr01             Snapmirrored  00:12:34             2.5GB
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are connected to the NetApp cluster via SSH or the ONTAP CLI, not a Linux shell.
    **`Error: Invalid destination path "svm_dr:vol_nfs_dr01"`** — Verify the SVM and volume names exist on the destination cluster using `snapmirror show` without filters.
Check that the destination volume contains data:

```bash
# On destination cluster:
volume show -vserver svm_dr -volume vol_nfs_dr01 -fields used
```


```text title="Expected output"
Vserver   Volume         Used
--------- -------------- --------
svm_dr    vol_nfs_dr01   2.1GB
```

!!! warning "Common errors"
    **`Error: command not found`** — Ensure you are logged into the NetApp cluster CLI (SSH to cluster management IP) rather than a standard Linux shell.
    **`Error: Invalid vserver name "svm_dr"`** — Verify the SVM name exists on the destination cluster using `vserver show` and confirm it matches your SnapMirror destination configuration.
---

## Configure Schedule

After initialization, SnapMirror updates run on a schedule defined by a job schedule or the policy's schedule rules.

**Check existing schedules:**

```bash
job schedule cron show
# Built-in schedules: hourly, daily, weekly
```


```text title="Expected output"
Job Schedule Cron Show
Name                Minute Hour   Day    Month  Day of Week Command
hourly              0      *      -      -      -            -
daily               0      0      -      -      -            -
weekly              0      0      -      -      1            -
custom-backup       30     2      -      -      *            -
snapmirror-sync     */15   *      -      -      -            -
```

!!! warning "Common errors"
    **`Error: command not found: job`** — Ensure you are connected to the NetApp cluster via SSH or the ONTAP CLI; this command only works in ONTAP system shell, not local bash.
    **`Error: This command is not available in the current privilege level`** — Elevate to admin or diag privilege level using `set -privilege admin` before running the command.
**Create a custom schedule (every 15 minutes):**

```bash
job schedule cron create -name every_15min -minute 0,15,30,45
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: "every_15min" already exists.`** — Choose a unique schedule name or delete the existing schedule with `job schedule cron delete -name every_15min` first.
    **`Error: Invalid minute specification "0,15,30,45". Valid range is 0-59.`** — Verify the minute values are comma-separated integers between 0 and 59 without spaces.
**Modify the SnapMirror relationship to use the schedule:**

```bash
snapmirror modify \
  -destination-path svm_dr:vol_nfs_dr01 \
  -schedule every_15min
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: "svm_dr:vol_nfs_dr01" is not a valid destination path`** — Verify the destination SVM and volume names exist with `snapmirror show` and use the correct format `svm_name:volume_name`.
    **`Error: "every_15min" is not a valid schedule`** — Confirm the schedule exists by running `job schedule cron show` and use an existing schedule name or create one with `job schedule cron create`.
    **`Error: SnapMirror relationship does not exist for destination "svm_dr:vol_nfs_dr01"`** — Initialize the SnapMirror relationship first with `snapmirror create -destination-path svm_dr:vol_nfs_dr01 -source-path svm_src:vol_nfs_src01` before modifying it.
**Trigger a manual update to confirm scheduled updates work:**

```bash
snapmirror update -destination-path svm_dr:vol_nfs_dr01
snapmirror show -destination-path svm_dr:vol_nfs_dr01
# Lag-time should decrease after the update completes
```


```text title="Expected output"
Operation succeeded: snapmirror update started.
                                                 Progress
Source Destination Mirror State Status Healthy Updated
------- ------------------- ------ --------- -------- -------
svm_src:vol_nfs_01 svm_dr:vol_nfs_dr01 SnapMirror Snapmirrored Idle true 09/14 14:32:18

Lag-time: 45 seconds
Last Transfer Size: 2.3GB
Last Transfer Duration: 00:03:22
Network Compression Ratio: 1.2:1
```

!!! warning "Common errors"
    **`Error: command failed: There is no SnapMirror relationship with destination svm_dr:vol_nfs_dr01`** — Verify the destination path is correct and the SnapMirror relationship exists using `snapmirror show`.
    **`Error: SnapMirror relationship is broken. Resynchronization is required`** — Run `snapmirror resync -destination-path svm_dr:vol_nfs_dr01` to restore the relationship before updating.
    **`Error: Transfer is already in progress for destination svm_dr:vol_nfs_dr01`** — Wait for the current transfer to complete or check status with `snapmirror show -fields transfer-progress`.
**View transfer history:**

```bash
snapmirror history show -destination-path svm_dr:vol_nfs_dr01
```


```text title="Expected output"
Source Destination Group Relationship ID Transfer Type Last Transfer Size Last Transfer Duration
-------- ----------- ----- --------------- ----------- ------------------- -------------------- ----------------------
svm_prod:vol_nfs_dr01 svm_dr:vol_nfs_dr01 - 12345678-abcd-ef01-2345-6789abcdef01 XDP 2.5GB 00:12:34
svm_prod:vol_nfs_dr01 svm_dr:vol_nfs_dr01 - 12345678-abcd-ef01-2345-6789abcdef01 XDP 2.3GB 00:11:22
svm_prod:vol_nfs_dr01 svm_dr:vol_nfs_dr01 - 12345678-abcd-ef01-2345-6789abcdef01 XDP 2.1GB 00:10:45
svm_prod:vol_nfs_dr01 svm_dr:vol_nfs_dr01 - 12345678-abcd-ef01-2345-6789abcdef01 XDP 1.9GB 00:09:33
svm_prod:vol_nfs_dr01 svm_dr:vol_nfs_dr01 - 12345678-abcd-ef01-2345-6789abcdef01 XDP 2.0GB 00:10:12
```

!!! warning "Common errors"
    **`Error: no entry matched the given criteria`** — Verify the destination path syntax is correct (svm_name:volume_name) and the SnapMirror relationship exists.
    **`Error: command not found: snapmirror`** — Ensure you are connected to the NetApp cluster via SSH or the ONTAP CLI, not a local shell.
---

## Validate RPO

**Check lag time (RPO indicator):**

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01 -fields lag-time
# Lag time should be less than the schedule interval (e.g., <15 minutes)
```


```text title="Expected output"
Source Destination Lag Time
svm_prod:vol_nfs_01 svm_dr:vol_nfs_dr01 00:08:32
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are logged into the NetApp cluster CLI (ssh to cluster management IP) rather than a Linux host, as snapmirror is a Data ONTAP command.
    **`Error: invalid destination-path "svm_dr:vol_nfs_dr01"`** — Verify the destination SVM and volume names exist on the DR cluster using `snapmirror list-destinations` and correct any typos in the path.
**Verify snapshots exist on the destination:**

```bash
snapshot show -vserver svm_dr -volume vol_nfs_dr01
# Snapshots named "sm_created" with SnapMirror timestamps should be present
```


```text title="Expected output"
Vserver     Volume            Snapshot                                State    Size  Total%
----------- ----------------- ----------------------------------- -------- ------ ------
svm_dr      vol_nfs_dr01      sm_created.1735689600.2024-01-01_00-00-00
                                                                   valid    2.1GB   15%
svm_dr      vol_nfs_dr01      sm_created.1735776000.2024-01-02_00-00-00
                                                                   valid    1.8GB   12%
svm_dr      vol_nfs_dr01      sm_created.1735862400.2024-01-03_00-00-00
                                                                   valid    2.3GB   18%
svm_dr      vol_nfs_dr01      sm_created.1735948800.2024-01-04_00-00-00
                                                                   valid    2.0GB   14%
svm_dr      vol_nfs_dr01      sm_created.1736035200.2024-01-05_00-00-00
                                                                   valid    1.9GB   13%
```

!!! warning "Common errors"
    **`Error: command failed: no snapshots found`** — Verify the SnapMirror relationship is initialized and has completed at least one transfer with `snapmirror show -instance`.
    **`Error: Invalid vserver name "svm_dr"`** — Confirm the SVM name is correct by running `vserver show` and check for typos in the vserver parameter.
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


```text title="Expected output"
Operation succeeded: SnapMirror relationship quiesced.
Operation succeeded: SnapMirror relationship broken.
svm_dr:vol_nfs_dr01 is now read-write.
Destination volume mounted at /mnt/nfs_dr01
Data validation: 2,847 files verified, checksums match source
Last common snapshot: 2024-01-15_0200.0
Resync operation initiated for svm_dr:vol_nfs_dr01
Transfer type: incremental
Estimated completion: 12 minutes
```

!!! warning "Common errors"
    **`Error: command failed: relationship does not exist for destination svm_dr:vol_nfs_dr01`** — Verify the destination path is correct and the SnapMirror relationship exists using `snapmirror show -destination-path svm_dr:vol_nfs_dr01`.
    **`Error: operation failed: destination volume is still in use by 1 client(s)`** — Unmount the destination volume on all test hosts before breaking the relationship with `umount /mnt/nfs_dr01`.
    **`Error: resync failed: common snapshot does not exist`** — Re-initialize the relationship using `snapmirror initialize -destination-path svm_dr:vol_nfs_dr01` instead of resync.
Confirm the relationship is back to `Snapmirrored` and lag time is under the RPO target:

```bash
snapmirror show -destination-path svm_dr:vol_nfs_dr01
```


```text title="Expected output"
Source Destination Mirror State Relationship Status Last Transfer
svm_prod:vol_nfs_01 svm_dr:vol_nfs_dr01 Snapmirrored Idle Success 2024-01-15 14:32:15
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are logged into the NetApp cluster CLI (ssh to cluster IP) rather than a local shell, or load the NetApp CLI module if using an SDK.
    **`Error: Invalid destination path format`** — Use the correct SVM:volume format (e.g., `svm_dr:vol_nfs_dr01`) and verify both the SVM and volume names exist with `svm show` and `volume show`.
    **`Error: Access denied for snapmirror command`** — Confirm your cluster user role has the "snapmirror" capability; check with `security login show -user-or-group-name <username>`.
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
