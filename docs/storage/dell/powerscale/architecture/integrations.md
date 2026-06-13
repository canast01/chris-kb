---
tags:
  - architecture
  - dell
---
# PowerScale — Integrations


<div class="kb-summary">
Integrations reference covering VMware Integration, Backup Integration, CloudIQ Monitoring, Active Directory / LDAP, REST API.
</div>
```text
┌─────────────────────────────────── Dell PowerScale — Integrations ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    PowerScale integrations: VMware vSphere, Kubernetes CSI, backup software, and monitoring   │   │
│   │                     Protocols: NFS v3/v4.1 · SMB · HDFS · S3 · Swift · FTP                    │   │
│   │    API: OneFS WebUI / isi CLI REST API enables automation and third-party tool integration    │   │
│   │             Plug-ins available for vCenter, OpenShift, Splunk, and SIEM platforms             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    PowerScale → REST API / plug-ins → VMware / K8s / backup / monitoring                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │              OS             │  │            OneFS            │  │        Distributed FS       │   │
│   │           Tiering           │  │          SmartPools         │  │        Auto data move       │   │
│   │         Replication         │  │            SyncIQ           │  │        Async DR copy        │   │
│   │          Snapshots          │  │          SnapshotIQ         │  │       Space-efficient       │   │
│   │         Load balance        │  │         SmartConnect        │  │       DNS client dist.      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      OneFS       │ Distributed file │  NFS/SMB/S3/HDFS  │  Kerberos/NTLM   │ Single namespac  │   │
│   │    SmartPools    │  Tiering policy  │      Internal     │    Admin role    │  Auto data move  │   │
│   │      SyncIQ      │ Async replicatio │   Encrypted TCP   │   Certificate    │   Policy-based   │   │
│   │    SnapshotIQ    │    Snapshots     │      Internal     │    Admin role    │  Per directory   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerScale nodes (All-Flash/Hybrid) · InfiniBand backend · 25/100 GbE frontend           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS              = Dell PowerScale distributed filesystem OS; all nodes share a single namespace │
│    SmartPools         = tiering engine; moves files between All-Flash, Hybrid, and Archive tiers      │
│    SyncIQ             = async replication to DR cluster; RPO-based schedule; failover in minutes      │
│    SnapshotIQ         = space-efficient snapshots; accessed via .snapshot directory in each share     │
│    SmartConnect       = DNS-based load balancing; distributes NFS/SMB client connections across nodes │
│    Access zone        = logical container with separate authentication and export namespace per tenant│
│    Quota              = directory or user quota; hard/soft/advisory limits enforced by OneFS QuotaIQ  │
│    CloudPools         = tiering to cloud object storage (S3/Blob); data remains accessible locally    │
│    isi CLI            = OneFS command-line interface; all management operations available via isi c...│
│    Node pool          = group of same-model nodes sharing protection domain for data distribution     │
│    Protection level   = N+2:1, N+3:1 etc.; defines how many node or drive failures are tolerated      │
│    File pool policy   = rule-based policy assigning files to specific node pools or storage tiers     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## VMware Integration

PowerScale integrates with VMware vSphere in several ways:

- **NFS Datastores**: PowerScale NFS exports are used as NFS datastores for vSphere. Mount via the SmartConnect DNS name (not a node IP) to ensure path failover transparency.
- **VAAI-NAS**: PowerScale supports the VMware VAAI-NAS extension via the Dell VAAI NAS plug-in, enabling hardware-accelerated full-copy and fast-file-clone operations for VM cloning and snapshot workflows.
- **VMDK storage for VMs with large unstructured data**: PowerScale `/ifs` is used as NFS-backed storage for VMs handling large file I/O (media transcoding, genomics analysis).
- **vCenter integration**: CloudIQ can surface PowerScale capacity and performance metrics alongside vSphere metrics for holistic capacity management.

NFS datastore tuning for VMware:
- Set NFS export options: `rw,no_root_squash` for vSphere hosts.
- Use NFSv3 for VAAI-NAS compatibility (NFSv4 does not support VAAI-NAS).
- Assign each ESXi cluster its own SmartConnect IP pool to isolate traffic and simplify ACL management.

## Backup Integration

**Veeam Backup & Replication**:
- Use PowerScale NFS or SMB shares as Veeam backup repositories (hardened or standard).
- Veeam SmartCopy for NAS (Veeam v12+) can use PowerScale SnapshotIQ to create application-consistent NAS backup points.
- Configure the backup repository to connect via SmartConnect DNS name.

**NetBackup / Veritas**:
- PowerScale supports NDMP (Network Data Management Protocol) for backup acceleration. Configure the NDMP service: `isi ndmp settings global modify --enabled true`.
- NDMP three-way backup: backup server connects to DD or tape library; PowerScale streams data directly without traversing the backup server.

**CommVault**:
- CommVault File System Agent on an NFS-mounted client, or IntelliSnap with SnapshotIQ for array-level NAS snapshots.

**Dell Data Domain (DDBoost)**:
- SyncIQ can replicate PowerScale data to another PowerScale cluster used as a long-term retention target; from there, Data Domain replication handles offsite DR.

## CloudIQ Monitoring

- **Setup**: Enable telemetry forwarding in OneFS: `isi cloud accounts create` (for CloudPools) and SupportAssist for CloudIQ health monitoring.
- **Capabilities**: Node health scoring, capacity forecasting, throughput anomaly detection, SyncIQ policy health, and quota headroom trending.
- **Alerts**: CloudIQ sends email and push notifications for node failures, capacity threshold crossings, and protection violations.

## Active Directory / LDAP

PowerScale access zones each have their own authentication providers:

```bash
# Join an Active Directory domain for an access zone
isi auth ads create --name EXAMPLE.COM --user Administrator --password <pw> --zone <zone-name>

# Verify AD join status
isi auth ads list --zone <zone-name>

# Add an LDAP provider for a zone
isi auth ldap create --name ldap-prod --server ldap://ldap.example.com \
  --base-dn "dc=example,dc=com" --zone <zone-name>

# List all auth providers for a zone
isi auth providers list --zone <zone-name>
```

- Use a dedicated service account for AD join; avoid domain admin credentials.
- For multi-protocol (NFS + SMB) environments, configure both AD (for Windows SIDs) and LDAP/NIS (for Unix UIDs/GIDs) on the same zone, and enable identity mapping.

## REST API

PowerScale OneFS exposes a REST API (PAPI):

```bash
# Base URL
https://<cluster-node>:8080/platform/<version>/

# List cluster nodes
curl -k -u admin:password \
  https://<cluster-node>:8080/platform/1/cluster/nodes

# Get quota information for a path
curl -k -u admin:password \
  "https://<cluster-node>:8080/platform/1/quota/quotas?path=/ifs/data/project"

# Create an NFS export
curl -k -u admin:password -X POST \
  -H "Content-Type: application/json" \
  -d '{"paths":["/ifs/data/newproject"],"clients":["10.0.0.0/24"],"map_root":{"user":"nobody"}}' \
  https://<cluster-node>:8080/platform/2/protocols/nfs/exports

# List SyncIQ policies
curl -k -u admin:password \
  https://<cluster-node>:8080/platform/3/sync/policies
```

Use the `isilon_sdk` Python package for scripted automation: `pip install isilon-sdk`.
API documentation is available at `https://<cluster-node>:8080/platform/latest/`.
