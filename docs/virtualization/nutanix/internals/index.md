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

---

## Genesis — Service Manager

**Role:** Genesis is the Nutanix equivalent of systemd for AOS services. It monitors and restarts all AOS services on each CVM.

```bash
genesis status           # list all services and state (UP/DOWN)
genesis restart          # restart all services on this CVM
```

Genesis itself is started by the OS init system. If genesis is completely crashed, it must be restarted at the OS level:
```bash
sudo systemctl restart nutanix-genesis
```

---

## See also

- [Nutanix — Architecture Overview](../architecture/how-it-works/)
- [Nutanix — Health Checks](../operations/health-checks/)
- [Nutanix — Diagnostics](../troubleshooting/diagnostics/)
