# vSAN Architecture — Integrations

## vCenter (Required)

vSAN is exclusively managed through vCenter Server. There is no standalone vSAN management interface — all cluster configuration, storage policy management, health monitoring, and capacity reporting is done through the vSphere Client connected to vCenter.

Key vCenter-managed vSAN functions:

- Cluster creation and disk group claim
- Storage policy creation and assignment
- vSAN health service (Skyline Health)
- Stretched cluster configuration
- File Services configuration
- vSAN upgrade via vLCM

If vCenter is unavailable, existing VMs continue running (vSAN data plane is independent of vCenter), but no configuration changes can be made and health monitoring is unavailable.

## NSX Integration

vSAN and NSX coexist on the same ESXi hosts and share the vSphere Distributed Switch (vDS). Careful NIC planning is required to avoid contention.

**NIC allocation considerations:**

| Traffic Type | Recommended NIC Allocation |
|---|---|
| vSAN vmkernel | Dedicated NIC pair (25 GbE or higher) |
| NSX TEP vmkernel | Separate NIC pair or shared with vMotion on lower-bandwidth environments |
| Management vmkernel | Shared with a management NIC pair |

If NICs are shared between vSAN and NSX TEP traffic, use NIOC (Network I/O Control) on the vDS to set bandwidth reservations:

- vSAN: minimum 50% reservation.
- NSX TEP: minimum 25% reservation.
- vMotion: minimum 25% reservation.

Verify that NSX TEP and vSAN vmkernel adapters are on separate VLANs and separate port groups, even if they share the same physical NICs.

## Stretched Cluster Witness

The vSAN Stretched Cluster requires a witness host at a third site to provide split-brain arbitration.

**Witness options:**

| Option | Description |
|---|---|
| vSAN Witness Appliance | Lightweight OVA deployed on an existing vSphere host at the witness site |
| Physical ESXi host | Full ESXi host with minimal resources; holds only metadata |

The witness host does not run production VMs and requires only minimal resources (the Witness Appliance is a small VM).

**Licensing:** The witness host requires a separate vCenter instance or a free vSphere Hypervisor licence. It cannot be managed by the same vCenter as the production cluster without an additional licence.

**Configuration:** The stretched cluster and witness are configured from vCenter via Cluster > Configure > vSAN > Fault Domains. vCenter creates the fault domains (Site A, Site B, Witness) and manages witness communication automatically.

## File Services

vSAN File Services extends the vSAN datastore to provide NFS and SMB file shares, enabling file-level access for containerised workloads, legacy applications, and multi-writer scenarios.

**Supported protocols:** NFS v3, NFS v4.1, SMB 2.x/3.x

**Requirements:**

- Minimum 3-node vSAN cluster.
- File Service Agent VMs are automatically deployed by vCenter (one per host hosting a file share).
- A dedicated IP pool for File Service Agent VMs.
- DNS entry for the file service VDI endpoint.

**Enabling File Services:**

vSphere Client > Cluster > Configure > vSAN > File Service > Enable

Specify the IP pool, subnet, gateway, and DNS. vCenter deploys the File Service Agent VMs automatically.

File Services is suited for:

- Kubernetes persistent volumes (ReadWriteMany) using NFS.
- Legacy applications requiring SMB file shares without a separate NAS.
- Multi-VM shared storage scenarios.

## Aria Operations

The vSAN management pack in Aria Operations (vROps) provides detailed visibility into vSAN performance, capacity, and health.

**Metrics available:**

| Category | Metrics |
|---|---|
| Cluster | Read/write IOPS, throughput, latency, resync throughput |
| Host | Per-host IOPS, latency, disk group utilisation |
| Disk Group | Cache hit ratio, write buffer utilisation, capacity per disk group |
| Capacity | Used/free/reserved capacity with forecast |
| Health | Health score from Skyline Health, degraded object count |

**Alerting:** Configure alerts in Aria Operations for:

- Resync throughput above threshold (indicates recovery in progress).
- Health score below 80%.
- Object non-compliance count > 0 for more than 1 hour.
- Capacity utilisation above 70%.

The vSAN management pack connects through the vCenter adapter; no separate vSAN credentials are required.
