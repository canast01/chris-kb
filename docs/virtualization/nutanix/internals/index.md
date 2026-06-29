---
tags:
  - nutanix
  - internals
  - stargate
  - cassandra
  - curator
  - zeus
---
# Nutanix — Internals

<div class="kb-summary">
Deep dive into AOS distributed architecture — the five core services (Stargate, Curator, Cassandra, Zeus/Zookeeper, Medusa), how they interact, and the data path from VM write to physical disk. Reference for advanced troubleshooting and capacity planning.

*Applies to: AOS 6.x · AHV*
</div>

---

```d2
direction: down

architecture_overview: "Architecture Overview" {shape: rectangle}
stargate_io_controller: "Stargate — I/O Controller" {shape: rectangle}
cassandra_distributed_metadata_store: "Cassandra — Distributed Metadata Store" {shape: rectangle}
zeus_zookeeper_cluster_config: "Zeus / ZooKeeper — Cluster Config" {shape: rectangle}
curator_background_worker: "Curator — Background Worker" {shape: rectangle}
medusa_metadata_access_layer: "Medusa — Metadata Access Layer" {shape: rectangle}

architecture_overview -> stargate_io_controller: uses
stargate_io_controller -> cassandra_distributed_metadata_store: uses
cassandra_distributed_metadata_store -> zeus_zookeeper_cluster_config: uses
zeus_zookeeper_cluster_config -> curator_background_worker: uses
curator_background_worker -> medusa_metadata_access_layer: uses
```

## Architecture Overview

---

## Stargate — I/O Controller

**Role:** Every VM I/O goes through Stargate. It is the I/O dataplane.

**Key behaviours:**
- **Local write first:** Writes land on the local CVM's SSD oplog for fast acknowledgement, then are drained to extent store extents distributed across the cluster
- **Remote reads:** If the data extent lives on another CVM's disk, Stargate routes the read to the appropriate CVM via internal network (1–5ms extra latency)
- **Locality preference:** Stargate prefers to schedule VM disk I/O through the CVM on the same host (data locality). VMs are pinned to the host where their data lives when possible
- **EC-X (Erasure Coding):** After data is written and "cold" (not accessed), Curator triggers EC compression of related extents to reduce space (analogous to RAID-5/6)

```bash
# Check Stargate health
genesis status | grep stargate
curl -s http://localhost:2009/   # Stargate HTTP stats endpoint (on CVM)

# Stargate logs
tail -f /home/nutanix/data/logs/stargate.ERROR
```


```text title="Expected output"
stargate                             RUNNING                 19256
stargate-worker-1                    RUNNING                 19257
stargate-worker-2                    RUNNING                 19258
stargate-worker-3                    RUNNING                 19259

{
  "version": "2.0.5.1",
  "uptime_seconds": 847293,
  "active_connections": 42,
  "total_requests": 5847291,
  "cache_hit_ratio": 0.8734,
  "avg_latency_ms": 3.2
}

==> /home/nutanix/data/logs/stargate.ERROR <==
2024-01-15 14:23:47.123 [stargate-worker-2] ERROR: Failed to replicate extent to replica 10.42.8.45:2009 - Connection timeout after 5000ms
2024-01-15 14:23:52.456 [stargate-worker-1] ERROR: Checksum mismatch detected on vdisk uuid-12345-abcde - CRC32: expected 0xdeadbeef, got 0xcafebabe
2024-01-15 14:24:01.789 [stargate-worker-3] WARN: Slow I/O operation detected - latency 245ms for read on extent group 567
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 2009: Connection refused`** — Verify Stargate is running with `genesis status | grep stargate` and check that the CVM network interface is accessible.
    **`tail: cannot open '/home/nutanix/data/logs/stargate.ERROR' for reading: No such file or directory`** — Confirm you are running this command on a Nutanix CVM (Controller VM) and that Stargate has been initialized with `genesis start stargate`.
---

## Cassandra — Distributed Metadata Store

**Role:** Nutanix-modified Apache Cassandra stores all cluster metadata.

**What it stores:**
- Extent-group to disk mappings (where every data block lives)
- vDisk descriptor maps (which extents make up each VM disk)
- Snapshot finger-print maps
- Protection domain replication state

**Ring topology:**
- Every CVM is a Cassandra node with a token range
- Metadata is replicated RF=3 across CVMs (even for storage RF=2 clusters)
- `nodetool status` shows ring health — all nodes must be `UN` (Up/Normal)

```bash
allssh "nodetool status"   # check ring — all should be UN
allssh "nodetool compactionstats"  # compaction queue (large = recovering)
```


```text title="Expected output"
node-01: Datacenter: dc1
node-01: ===============
node-01: Status=Up/Down
node-01: |/ State=Normal/Leaving/Joining/Moving
node-01: --  Address          Load       Tokens  Owns (effective)  Host ID                               Rack
node-01: UN  192.168.1.101    156.42 GB  256     33.3%             a1b2c3d4-e5f6-7890-abcd-ef1234567890  rack1
node-01: UN  192.168.1.102    148.91 GB  256     33.3%             b2c3d4e5-f6a7-8901-bcde-f12345678901  rack1
node-01: UN  192.168.1.103    151.27 GB  256     33.4%             c3d4e5f6-a7b8-9012-cdef-123456789012  rack1
node-02: Datacenter: dc1
node-02: UN  192.168.1.101    156.42 GB  256     33.3%             a1b2c3d4-e5f6-7890-abcd-ef1234567890  rack1
node-02: UN  192.168.1.102    148.91 GB  256     33.3%             b2c3d4e5-f6a7-8901-bcde-f12345678901  rack1
node-02: UN  192.168.1.103    151.27 GB  256     33.4%             c3d4e5f6-a7b8-9012-cdef-123456789012  rack1
node-01: Compaction from [/var/lib/cassandra/data/system/local/na-1-big-Data.db] complete
node-01: Pending tasks: 0
node-02: Compaction from [/var/lib/cassandra/data/system/peers/na-2-big-Data.db] complete
node-02: Pending tasks: 0
```

!!! warning "Common errors"
    **`nodetool: command not found`** — Ensure Cassandra is installed and `$CASSANDRA_HOME/bin` is in your PATH, or use the full path `/opt/cassandra/bin/nodetool`.
    **`Connection refused`** — Verify Cassandra JMX port (default 7199) is listening with `netstat -tlnp | grep 7199` and restart Cassandra if needed.
    **`DN  192.168.1.102`** (node showing DOWN status) — Restart the down node with `systemctl restart cassandra` and wait 30 seconds for it to rejoin the ring.
---

## Zeus / ZooKeeper — Cluster Config

**Role:** Zeus is Nutanix's configuration store built on ZooKeeper. It is the single source of truth for cluster config and service leadership.

**What it stores:**
- Node membership (which CVMs are in the cluster)
- Service leader elections
- Cluster-wide configuration parameters (DNS, NTP, VIP, RF)

```bash
# Print cluster configuration
zeus_config_printer | head -80

# Inspect ZooKeeper directly
/usr/local/zookeeper/bin/zkCli.sh -server localhost:9876
```


```text title="Expected output"
Cluster UUID: 550e8400-e29b-41d4-a716-446655440000
Cluster Name: prod-cluster-01
Redundancy Factor: 3
Replication Factor: 3
Block Serial: NX-3060-G7-12SFF-001
Hypervisor: AHV 20231015.1234
NOS Version: 6.5.2.1-20231201
Controller VM Count: 3
Data IP Range: 10.42.0.0/16
Prism Central: 10.42.1.50
Storage Pool: default
Disk Count: 36
Memory Total: 2.0 TB
CPU Count: 288 cores
Metadata Replication: enabled
Dedup Status: active
Compression: enabled
Erasure Coding: disabled

Connecting to localhost:9876
[zk: localhost:9876(CONNECTING) 0]
Welcome to ZooKeeper CLI version 3.4.14-4c25d480e66aadd371de8bd2712133f8.3435ecc0a5b5c557357162b5c6614e6c, built on 03/06/2020 22:33 GMT

JLine support is enabled
[zk: localhost:9876(CONNECTED) 0]
```

!!! warning "Common errors"
    **`Connection refused`** — Verify ZooKeeper service is running with `systemctl status zookeeper` and listening on port 9876.
    **`zeus_config_printer: command not found`** — Ensure you are running this command on a Nutanix cluster node with the Acropolis OS installed, not a remote management station.
---

## Curator — Background Worker

**Role:** Curator runs background scans and maintenance jobs across the cluster.

**Scan types:**
- **Partial scan:** Runs every 6 hours; handles urgent tasks (rebuild after failure, tiering of hot data)
- **Full scan:** Runs daily; handles dedup fingerprinting, EC-X encoding, cold-tier migration, rebalancing

**Tasks Curator performs:**
- **Rebuild:** After disk/node failure, re-replicate degraded extents to restore RF
- **Deduplication:** After partial scan builds fingerprints, deduplicate matching extents (Pro/Ultimate)
- **Compression:** Inline (during write) and post-process (via Curator)
- **Erasure Coding:** Convert RF=2 extents to EC-X to save 50% space after data goes cold
- **Tiering:** Move cold data from SSD to HDD tier (hybrid clusters)
- **Rebalancing:** Redistribute extents when cluster imbalance exceeds threshold

```bash
curator_cli get_last_successful_scans     # recent scan history
curator_cli display_curator_tasks          # active tasks now
curator_cli get_scan_info --scan_id=<id>  # detailed scan results
```


```text title="Expected output"
Scan ID: scan_20240115_093847, Cluster: PHX-PROD-01, Status: SUCCESS, Timestamp: 2024-01-15 09:45:22 UTC
Scan ID: scan_20240115_082103, Cluster: PHX-PROD-01, Status: SUCCESS, Timestamp: 2024-01-15 08:23:45 UTC
Scan ID: scan_20240114_195634, Cluster: PHX-PROD-01, Status: SUCCESS, Timestamp: 2024-01-14 19:58:12 UTC
Scan ID: scan_20240114_142201, Cluster: PHX-PROD-01, Status: SUCCESS, Timestamp: 2024-01-14 14:24:33 UTC

Task ID: curator_task_8472, Type: METADATA_SCAN, Status: RUNNING, Progress: 67%, Started: 2024-01-15 10:12:05 UTC
Task ID: curator_task_8471, Type: CONSISTENCY_CHECK, Status: QUEUED, Progress: 0%, Started: 2024-01-15 10:11:22 UTC

Scan Details for scan_20240115_093847:
  Cluster: PHX-PROD-01
  Duration: 2m 34s
  Containers Scanned: 847
  Objects Processed: 2,156,432
  Inconsistencies Found: 0
  Status: PASSED
```

!!! warning "Common errors"
    **`curator_cli: command not found`** — Ensure the Nutanix curator CLI is installed and its path is added to your system PATH variable.
    **`Error: Invalid scan_id format or scan not found`** — Verify the scan ID exists by running `curator_cli get_last_successful_scans` first and use the exact Scan ID from the output.
---

## Medusa — Metadata Access Layer

**Role:** Medusa is the API layer between AOS services (Stargate) and Cassandra. Services never query Cassandra directly — they use Medusa.

Medusa handles:
- Key-value lookups for vDisk → extent mappings
- Caching of hot metadata in CVM memory
- Batching of Cassandra writes for efficiency

Medusa is not a separate visible process — it runs as a library inside each AOS service. Medusa errors surface in Stargate and Acropolis logs.

---

## AHV — KVM Hypervisor

**Role:** AHV is Nutanix's built-in hypervisor based on KVM/QEMU. CVMs run as privileged VMs on AHV (alongside user VMs).

**Key components:**
- **libvirt** — manages KVM VMs (including the CVM itself)
- **QEMU** — VM emulator (one QEMU process per running VM)
- **Open vSwitch (OVS)** — virtual networking fabric; supports VLAN trunking and bonding
- **acropolis** — Nutanix AHV management daemon (bridges acli/Prism to libvirt)

```bash
# On AHV host (root required):
virsh list --all        # all VMs including CVM
virsh nodeinfo          # host CPU/memory
ovs-vsctl show          # OVS switch config
```


```text title="Expected output"
Id   Name                                  State
----------------------------------------------------
 1    NTNX-00051234567890ab-CVM             running
 2    VM-prod-web-01                        running
 3    VM-prod-db-02                         running
 4    VM-dev-test-03                        paused
 -    VM-archive-old-04                     shut off

Host:                 NTNX-00051234567890ab
CPU model:            Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz
CPU(s):               32
CPU frequency:        2400.052 MHz
CPU socket(s):        2
Core(s) per socket:   8
Thread(s) per core:   2
NUMA cell(s):         2
Memory size:          262144 MiB

Manager "br0"
    Bridge "br0"
        fail_mode: secure
        Port "br0"
            Interface "br0"
                type: internal
        Port "bond0"
            Interface "eth0"
            Interface "eth1"
    ovs_version: "2.9.2"
```

!!! warning "Common errors"
    **`error: failed to connect to the hypervisor`** — Ensure you are running as root and the libvirtd service is active with `systemctl status libvirtd`.
    **`ovs-vsctl: unix:/var/run/openvswitch/db.sock: database connection failed`** — Verify Open vSwitch is running with `systemctl status openvswitch` and restart if necessary.
---

## Genesis — Service Manager

**Role:** Genesis is the Nutanix equivalent of systemd for AOS services. It monitors and restarts all AOS services on each CVM.

```bash
genesis status           # list all services and state (UP/DOWN)
genesis restart          # restart all services on this CVM
```


```text title="Expected output"
Service Name                          State      PID
acropolis                             UP         2847
cassandra                             UP         3124
chronos                               UP         2956
curator                               UP         3201
genesis                               UP         1842
prism                                 UP         3456
uhura                                 UP         2734
zookeeper                             UP         2891

Restarting all services on this CVM...
Stopping services...
Starting services...
All services restarted successfully. Elapsed time: 47 seconds
```

!!! warning "Common errors"
    **`genesis: command not found`** — Ensure you are running this command on a Nutanix Controller VM (CVM), not a hypervisor host; SSH to the CVM first.
    **`Permission denied`** — Run the command with sudo or as the root user: `sudo genesis restart`.
Genesis itself is started by the OS init system. If genesis is completely crashed, it must be restarted at the OS level:
```bash
sudo systemctl restart nutanix-genesis
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to restart nutanix-genesis.service: Unit nutanix-genesis.service not found.`** — Verify the Nutanix cluster node is properly initialized and the genesis service is installed with `systemctl list-unit-files | grep nutanix`.
    **`sudo: systemctl: command not found`** — Ensure you are running this command on a Nutanix cluster node (CVM or host) where systemd is available, not on an unsupported OS.
    **`Failed to restart nutanix-genesis.service: Access denied`** — Run the command with proper sudo privileges or as root; verify your user account has passwordless sudo configured for this service.
---

## See also

- [Nutanix — Architecture Overview](../architecture/how-it-works/)
- [Nutanix — Health Checks](../operations/health-checks/)
- [Nutanix — Diagnostics](../troubleshooting/diagnostics/)
