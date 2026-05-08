# Dell VPLEX — Components

## Core Components

| Component | Description |
|---|---|
| VPLEX Director | The core processing unit; each director has front-end FC ports (to hosts), back-end FC ports (to storage arrays), and an NVRAM write cache module |
| Director Pair | Two directors in one chassis sharing a mirrored write cache over a high-speed interconnect; a director pair is the minimum HA unit |
| Engine | A VPLEX chassis containing one or two director pairs |
| VPLEX VS2 (Local) | Single-cluster deployment at one site; supports virtualisation, data mobility, and active-active within a single data centre |
| VPLEX Metro | Two-cluster deployment across two sites with synchronous mirroring over the ICL (≤5ms RTT); provides active-active access with zero RPO and transparent failover |
| VPLEX Geo | Two-cluster deployment for distances exceeding Metro RTT limits; uses RecoverPoint for asynchronous replication; DR-mode, not active-active |
| Witness VM | Lightweight VM at a third failure domain; provides quorum arbitration for Metro split-brain scenarios |
| VPLEX Management Server (VMS) | A VM hosting the management console, `vplexcli`, and Unisphere for VPLEX; not in the data path |
| Inter-Cluster Link (ICL) | 10/25GbE WAN or dark fibre link between Metro clusters carrying synchronous write replication traffic |

## Physical Hardware

### Engine and Director Models

VPLEX hardware ships as an engine (chassis) containing director blades. The current generation is the VS2 director.

| Component | Detail |
|---|---|
| Engine chassis | 2U rack unit; houses one or two director pairs |
| Director | Blade-form; two per pair; hot-swappable |
| Write cache (NVRAM) | Per-director NVRAM module; cache is mirrored between pair partners over the internal interconnect |
| Front-end FC ports | 8Gb or 16Gb FC; connect to SAN fabric (host-side); quantity depends on director model |
| Back-end FC ports | 8Gb or 16Gb FC; connect to SAN fabric (array-side); quantity depends on director model |
| Management NIC | Dedicated 1GbE management interface on VMS; no data path |
| ICL ports | 10GbE or 25GbE; present on Metro-configured directors for cluster-to-cluster communication |

### Director Naming Convention

VPLEX names directors systematically within the vplexcli hierarchy:

```
/engines/engine-<site>-<engine_number>/directors/director-<site>-<engine>-<A|B>/
```

Example: `director-1-1-A` = Site 1, Engine 1, Director A (first of the pair).

```bash
# List all engines
vplexcli -q -e "ls /engines"

# List directors in engine-1-1
vplexcli -q -e "ll /engines/engine-1-1/directors/"

# Show hardware detail for a specific director
vplexcli -q -e "ll /engines/engine-1-1/directors/director-1-1-A/hardware/"

# List all ports on a director
vplexcli -q -e "ll /engines/engine-1-1/directors/director-1-1-A/hardware/ports/"
```

## Storage Object Hierarchy

VPLEX builds virtual volumes from back-end arrays through a layered abstraction stack:

```
Back-end Array LUN
    └── Storage Volume    (VPLEX discovers and claims the LUN)
        └── Extent        (VPLEX claim on a storage volume; one-to-one in most cases)
            └── Local Device  (one or more extents, local to a single cluster)
                └── Distributed Device  (RAID-1 across two cluster legs — Metro only)
                    └── Virtual Volume  (presented to hosts via storage views)
```

### Storage Volumes

Storage volumes are unclaimed back-end array LUNs visible to VPLEX back-end ports. VPLEX discovers them when zoning and array masking are correctly configured.

```bash
# List back-end arrays visible to VPLEX
vplexcli -q -e "ls /storage-elements/storage-arrays"

# List storage volumes on a specific array
vplexcli -q -e "ls /storage-elements/storage-arrays/array-A/storage-volumes"

# Claim a storage volume (makes it available for extent creation)
vplexcli -q -e "storage-volume claim \
  --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"

# Unclaim a storage volume (before decommissioning)
vplexcli -q -e "storage-volume unclaim \
  --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"
```

### Extents

An extent is a VPLEX claim on an entire storage volume (or a portion of one). Extents are local to a single cluster.

```bash
# List extents on cluster-1
vplexcli -q -e "ls /clusters/cluster-1/storage-elements/extents"

# Show details of a specific extent
vplexcli -q -e "ll /clusters/cluster-1/storage-elements/extents/ext_app_001/"

# Create an extent from a claimed storage volume
vplexcli -q -e "extent create \
  --name ext_app_001 \
  --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"
```

### Local Devices

A local device aggregates one or more extents into a single addressable storage object within a cluster. Local devices use RAID geometry (typically RAID-0 for a single extent, or RAID-1 for local mirroring).

```bash
# List local devices on cluster-1
vplexcli -q -e "ls /clusters/cluster-1/devices"

# Create a local device (RAID-0, single extent)
vplexcli -q -e "local-device create \
  --name dev_app_001 \
  --geometry raid-0 \
  --extents /clusters/cluster-1/storage-elements/extents/ext_app_001"

# Show local device attributes
vplexcli -q -e "ll /clusters/cluster-1/devices/dev_app_001/"
```

### Distributed Devices (VPLEX Metro)

Distributed devices span two cluster legs (one per site) in a RAID-1 relationship. This is the Metro mirroring mechanism. Both legs receive every write synchronously.

```bash
# List distributed devices
vplexcli -q -e "ls /distributed-storage/distributed-devices"

# Show health and sync state of all distributed devices
vplexcli -q -e "ll /distributed-storage/distributed-devices/*/health-indications/"

# Show detailed state of a single distributed device
vplexcli -q -e "ll /distributed-storage/distributed-devices/dist_app_vol_1/"

# Create a distributed device (prerequisite: local devices on both clusters)
vplexcli -q -e "distributed-device create \
  --name dist_app_vol_1 \
  --geometry raid-1 \
  --components /clusters/cluster-1/devices/dev_app_001,/clusters/cluster-2/devices/dev_app_002"
```

**Distributed device health states:**

| State | Meaning | Action |
|---|---|---|
| `in-sync` | Both legs active and mirrored; full Metro redundancy | Normal |
| `rebuilding` | Resynchronising after an interruption; both legs accessible | Monitor progress; do not interrupt |
| `degraded` | One leg unreachable; single-site I/O only | Investigate the unreachable cluster |
| `detached` | Both legs disconnected; I/O suspended | Restore ICL and Witness; resume manually |
| `paused` | Intentionally paused by administrator | Resume when ready |

### Virtual Volumes

Virtual volumes are the objects presented to hosts. They are created on top of a local device (for VPLEX Local) or a distributed device (for VPLEX Metro).

```bash
# List all virtual volumes
vplexcli -q -e "ls /virtual-volumes"

# Show virtual volume attributes
vplexcli -q -e "ll /virtual-volumes/my_app_vol_1/"

# Create a virtual volume from a local device
vplexcli -q -e "virtual-volume create \
  --name my_app_vol_1 \
  --local-device /clusters/cluster-1/devices/dev_app_001"

# Create a virtual volume from a distributed device (Metro)
vplexcli -q -e "virtual-volume create \
  --name app_vol_metro_1 \
  --distributed-device /distributed-storage/distributed-devices/dist_app_vol_1"

# Expand a virtual volume (after expanding back-end LUN and extent)
vplexcli -q -e "virtual-volume expand \
  --virtual-volume /virtual-volumes/my_app_vol_1"

# Destroy a virtual volume (remove from all storage views first)
vplexcli -q -e "virtual-volume destroy \
  --virtual-volume /virtual-volumes/my_app_vol_1 --force"
```

**Key virtual volume attributes:**

| Attribute | Expected | Description |
|---|---|---|
| `operational-status` | `ok` | Overall volume health |
| `health-state` | `ok` | Health indication |
| `capacity` | (size in bytes) | Volume capacity |
| `supporting-device` | (device path) | Underlying local or distributed device |
| `visibility` | `global` | Determines which clusters can access the volume |

## Storage Views

A storage view is a masking construct that maps a set of virtual volumes to a set of host initiator ports (WWNs) through specific VPLEX front-end ports. This is the primary host access control mechanism.

### Storage View Components

| Component | Description |
|---|---|
| Initiator ports | Host HBA WWNs registered with VPLEX |
| Front-end ports | VPLEX director FC ports through which the volumes are presented |
| Virtual volumes | The volumes made accessible through this view |

### Storage View Operations

```bash
# List storage views on a cluster
vplexcli -q -e "ls /clusters/cluster-1/exports/storage-views"

# Show full detail of a specific storage view
vplexcli -q -e "ll /clusters/cluster-1/exports/storage-views/sv_esxi_host_01/"

# Register a host HBA WWN
vplexcli -q -e "initiator-port register \
  --cluster /clusters/cluster-1 \
  --port-wwn 10:00:00:00:c9:ab:cd:ef \
  --name esxi_host_01_hba0"

# Create a storage view
vplexcli -q -e "storage-view create \
  --name sv_esxi_host_01 \
  --cluster /clusters/cluster-1"

# Add VPLEX front-end ports to the view
vplexcli -q -e "storage-view add-ports \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --ports /clusters/cluster-1/exports/ports/A0-FC00,/clusters/cluster-1/exports/ports/B0-FC00"

# Add host initiator ports to the view
vplexcli -q -e "storage-view add-initiator-ports \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --initiator-ports /clusters/cluster-1/exports/initiator-ports/esxi_host_01_hba0"

# Add virtual volumes to the view
vplexcli -q -e "storage-view add-virtual-volumes \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --virtual-volumes /virtual-volumes/app_vol_metro_1"

# List all registered initiator ports
vplexcli -q -e "ls /clusters/cluster-1/exports/initiator-ports"

# Destroy a storage view (host loses access to all volumes in it)
vplexcli -q -e "storage-view destroy \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 --force"
```

## Consistency Groups

Consistency groups (CGs) ensure a set of distributed virtual volumes is treated as a write-order-consistent unit during failover and recovery. All volumes in a CG fail over together, preventing partial-write scenarios in applications that write to multiple volumes.

```bash
# List all consistency groups
vplexcli -q -e "ls /distributed-storage/consistency-groups"

# Show details and member volumes
vplexcli -q -e "ll /distributed-storage/consistency-groups/cg_app_tier/"

# Create a consistency group
vplexcli -q -e "consistency-group create --name cg_app_tier"

# Add virtual volumes to a consistency group
vplexcli -q -e "consistency-group add-virtual-volumes \
  --consistency-group /distributed-storage/consistency-groups/cg_app_tier \
  --virtual-volumes /virtual-volumes/app_vol_metro_1,/virtual-volumes/app_vol_metro_2"

# Remove a virtual volume from a consistency group
vplexcli -q -e "consistency-group remove-virtual-volumes \
  --consistency-group /distributed-storage/consistency-groups/cg_app_tier \
  --virtual-volumes /virtual-volumes/app_vol_metro_1"
```

**Consistency group design rules:**

- Place all related volumes for a multi-volume application in a single consistency group.
- Single-volume applications should still use a consistency group in Metro deployments to enable coordinated Witness-arbitrated failover.
- One CG per application stack; do not mix unrelated applications in one CG.
- Verify CG membership is documented in the CMDB; changes require a change record.

## VPLEX Management Server (VMS)

The VMS is a virtual machine that hosts:

- The `vplexcli` management shell (accessed via SSH: `ssh service@<VMS_IP>`)
- The Unisphere for VPLEX web GUI (`https://<VMS_IP>/`)
- VPLEX management daemons and log collection

**VMS is not in the data path.** If the VMS fails, hosts continue to access their volumes through the directors. However, no configuration changes can be made until VMS is restored.

VMS operational requirements:

| Item | Guidance |
|---|---|
| Hypervisor | VMware vSphere or compatible; check Dell VPLEX compatibility matrix |
| VM resources | As specified by Dell for the GeoSynchrony version deployed |
| Network | Management VLAN only; no data-path traffic |
| Backup | Snapshot before every change; weekly full backup |
| Redundancy | Deploy a standby VMS or maintain regular snapshots; no built-in HA for VMS |

Access the VMS:

```bash
# SSH to VMS and launch vplexcli interactively
ssh service@<VMS_IP>
vplexcli

# Run a one-shot command without entering interactive mode
vplexcli -q -e "health-check"

# Show GeoSynchrony firmware version
vplexcli -q -e "ll /version/"
```
