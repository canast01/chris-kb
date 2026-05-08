# PowerStore — Components

## Hardware Components

### Storage Nodes

Each PowerStore appliance contains two storage nodes (Node A, Node B). Both nodes are active simultaneously and serve host I/O concurrently via a distributed ownership model over the internal NVMe fabric.

| Specification | PowerStore 500T/X | PowerStore 3000T/X | PowerStore 9000T/X |
|---|---|---|---|
| Node CPUs | Intel Xeon (entry) | Intel Xeon (mid) | Intel Xeon (high-core) |
| Node RAM | 64 GB per node | 128 GB per node | 256 GB per node |
| Cache (NVDIMM) | 16 GB per node | 32 GB per node | 64 GB per node |
| Max raw capacity | ~300 TB | ~2 PB | ~4 PB |
| Max usable NVMe drives | 25 | 80 | 180 |
| Front-end I/O modules | 2 per node | 2 per node | 4 per node |

> Exact specifications vary by software version and drive configuration. Always refer to the current Dell PowerStore spec sheet for the specific model purchased.

### NVMe Drive Enclosures

PowerStore uses NVMe SSDs exclusively — no SATA, SAS, or spinning disk. Drives are housed in hot-swap NVMe enclosures attached to the appliance chassis.

| Drive Type | Use Case | Notes |
|---|---|---|
| NVMe Performance (MLC/TLC) | All primary workloads | Standard SKU shipped with most configurations |
| NVMe Capacity (QLC) | Archive and capacity-optimized workloads | Higher capacity per drive; slightly lower write endurance |
| SCM (Storage Class Memory) | Ultra-low latency workloads (if applicable) | Available on select high-end models; reduces latency to sub-100 microseconds |

### I/O Modules

I/O modules are the front-end host connectivity cards. They are installed per node and are field-replaceable. Both nodes must have the same I/O module configuration for symmetry.

| Module Type | Ports per Module | Protocol |
|---|---|---|
| 32 Gb FC | 2 ports | Fibre Channel (FC-NVMe or SCSI over FC) |
| 16 Gb FC | 4 ports | Fibre Channel (legacy host compatibility) |
| 25 GbE iSCSI/NVMe-oF | 4 ports | iSCSI or NVMe over RoCE |
| 100 GbE iSCSI/NVMe-oF | 2 ports | iSCSI or NVMe over RoCE (high-bandwidth workloads) |

A typical dual-fabric SAN configuration uses one FC module per node, connecting to two separate SAN fabrics (Fabric A and Fabric B) — providing full path redundancy.

### Management Module

Each appliance has a dedicated management module that provides:

- Management IP interface (dedicated 1 GbE port — never use a data port for management)
- BMC (Baseboard Management Controller) access for hardware-level diagnostics
- SupportAssist gateway for Dell call-home telemetry

### NVDIMM (Non-Volatile DIMM)

Each node includes NVDIMM modules that serve as a persistent write buffer. Incoming writes are acknowledged to the host after landing in NVDIMM (battery-backed), then destaged to NVMe SSDs asynchronously. This provides:

- Consistent low write latency independent of flash endurance wear state
- Protection against power loss — NVDIMM contents survive a node power failure
- A destage queue that smooths bursty write workloads

## Software Components

### PowerStoreOS (PSTROS)

PowerStoreOS is the operating system running on both nodes. It is delivered as a single software update package (`.bin` file) applied via PowerStore Manager.

Key software subsystems:

| Subsystem | Role |
|---|---|
| Storage Services | Block volume, NAS server, and vVols management |
| Data Reduction Engine | Inline compression and deduplication |
| RAID Manager | Drive pool management, RAID 5/6, spare management |
| Replication Engine | Async replication and Metro Volume sync replication |
| Protection Engine | Snapshot scheduling, retention policy enforcement |
| Health Monitor | Hardware health polling, fault detection, alerting |
| REST API Server | HTTPS API endpoint for all management operations |
| Upgrade Manager | Non-disruptive firmware and software update orchestration |

### PowerStore Manager

PowerStore Manager is the primary web-based management interface. It is served from the management IP of the appliance cluster and accessed via HTTPS.

Key sections:

| Section | Function |
|---|---|
| Dashboard | Health, capacity, and performance overview |
| Storage | Volume, file system, and vVols provisioning |
| Protection | Snapshot policies, replication sessions, import |
| Hardware | Node, drive, and I/O module health; enclosure view |
| Settings | Network, users, LDAP, SNMP, certificates, NTP |
| Capacity | Pool utilisation and data reduction ratio |

### REST API

The PowerStore REST API is the authoritative interface for all management operations. The web UI uses the same API internally. All resource types (volumes, hosts, snapshots, replication sessions) are accessible via HTTPS REST.

```bash
# Base URL
https://<management-ip>/api/rest/

# Authentication: DELL-EMC-TOKEN header (obtained via login_session)
# Or: HTTP Basic auth on every request

# Example: list all volumes
curl -k -X GET https://<mgmt-ip>/api/rest/volume \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Accept: application/json" | python3 -m json.tool

# Example: get a specific volume by ID
curl -k -X GET https://<mgmt-ip>/api/rest/volume/<volume-id> \
  -H "DELL-EMC-TOKEN: <token>"

# Filter by name (select parameter)
curl -k -X GET "https://<mgmt-ip>/api/rest/volume?select=id,name,size,state" \
  -H "DELL-EMC-TOKEN: <token>"
```

### pstcli

`pstcli` is a thin CLI binary that wraps the REST API. It is installed on a Linux or Windows management host (not on the array itself).

```bash
# Install pstcli (Linux — download from PowerStore Manager)
# PowerStore Manager → Settings → Downloads → pstcli

# Connect (interactive prompt)
pstcli -d 192.168.10.50 -u admin

# Run a single command non-interactively
pstcli -d 192.168.10.50 -u admin -p 'password' "show /volume"

# Use JSON output for scripting
pstcli -d 192.168.10.50 -u admin "show /volume" --output json
```

### vSphere Plugin (vCenter Extension)

The PowerStore vSphere Plugin (delivered as a vCenter Server extension) integrates PowerStore management into the vSphere Client:

- Provision and manage PowerStore datastores (VMFS-on-iSCSI, NFS, vVols) directly from vCenter
- View PowerStore health and capacity inline with VM and datastore views
- Create and manage vVols storage policies aligned to PowerStore protection policies
- Requires VASA Provider registration in vCenter — the VASA Provider is built into PowerStoreOS and does not require a separate VM

### VASA Provider

The VASA (vSphere APIs for Storage Awareness) Provider is embedded in PowerStoreOS and allows vSphere to:

- Discover PowerStore capabilities (RAID level, data reduction, replication)
- Enforce VM Storage Policies that map to PowerStore protection policies
- Provision vVols — individual virtual disks stored as objects on PowerStore rather than in a shared VMFS datastore

```bash
# Register VASA Provider in vCenter
# vCenter → Storage Providers → Add (Storage Providers)
# URL: https://<powerstore-mgmt-ip>/vasa/version.xml
# Credentials: PowerStore admin account

# Verify VASA registration via REST API
curl -k -X GET "https://<mgmt-ip>/api/rest/storage_provider" \
  -H "DELL-EMC-TOKEN: <token>"
```

## Network Components

### Management Network

- Dedicated 1 GbE management port per node (separate from data ports)
- Management IP is a floating virtual IP that follows the active management node
- Both node management ports should be connected for redundancy even though only the active node's management IP is used
- Management network should be on a dedicated management VLAN, isolated from data traffic

### Data Network (iSCSI / NVMe-oF)

- Each node's data ports connect to separate network switches for redundancy
- iSCSI: recommend two separate iSCSI switches (or VLANs) for path A and path B
- NVMe-oF (RoCE): requires RDMA-capable switches (with PFC/ECN enabled for lossless Ethernet); recommend dedicated VLANs separate from general data traffic
- Jumbo frames (MTU 9000) recommended for iSCSI and NVMe-oF interfaces

### SAN Fabric (Fibre Channel)

- Each FC I/O module connects to a separate FC fabric (Fabric A and Fabric B)
- Zone each host initiator to exactly one target port per fabric — do not create mega-zones
- Hard zoning recommended where the FC switch supports it; soft zoning acceptable for lower-security environments
- FC port naming convention on PowerStore: `[appliance-name]:SPA:FC4:1` format (Node A, port 4, lane 1)

## Replication Components

### Replication Session

A replication session is the logical object that tracks an active replication relationship between a source volume (or file system) and a destination volume on a remote PowerStore.

```bash
# List replication sessions
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session" \
  -H "DELL-EMC-TOKEN: <token>"

# Pause a replication session (e.g., before maintenance)
curl -k -X POST "https://<mgmt-ip>/api/rest/replication_session/<id>/pause" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json"

# Resume a replication session
curl -k -X POST "https://<mgmt-ip>/api/rest/replication_session/<id>/resume" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json"
```

### Replication Rule

A replication rule defines the RPO interval (how frequently the source is replicated to the destination). Replication rules are reusable and attached to Protection Policies.

| RPO Setting | Appropriate Use |
|---|---|
| 5 minutes | Tier-1 databases; critical applications |
| 1 hour | Tier-2 applications; file servers |
| 4 hours | Dev/test environments; secondary applications |
| 1 day | Archive workloads; capacity-optimized replication |

### Metro Volume

Metro Volume is a synchronous replication mode (zero RPO) implemented at the PowerStore volume level. It requires a Mediator service for arbitration.

Components:

| Component | Role |
|---|---|
| Primary volume | Source of writes; host connects here normally |
| Secondary volume | Synchronous mirror; read-only to hosts during normal operation |
| Mediator | Lightweight VM at a third site; breaks split-brain on network partition |
| Witness port | TCP port 6666 — Metro Volume nodes communicate with the Mediator on this port |

Mediator can be deployed as:
- A VM at a third physical site (recommended for full resilience)
- A Dell-hosted cloud Mediator (available for supported configurations)
