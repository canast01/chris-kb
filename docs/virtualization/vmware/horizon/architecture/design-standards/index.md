# Horizon — Design Standards


<div class="kb-summary">
Design Standards reference covering Desktop VM Sizing, Storage Sizing, VLAN and Network Design, UAG Sizing, App Volumes Sizing and 3 more sections.
</div>

  Pod Design (up to 7 Connection Servers, 10,000 IC desktops)
```text
┌────────────────────────────────── VMware Horizon — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│  Horizon design standards define Connection Server sizing, UAG placement, desktop                     │
│  pool type selection, storage tier, and display protocol choices.                                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Connection Server Sizing           │  │                 Pool Design                 │   │
│   │           Max 4000 sessions per CS           │  │          Instant clone: non-persist         │   │
│   │               Min 2 CS for HA                │  │         Full clone: persistent desks        │   │
│   │           2 UAGs per site minimum            │  │            RDS farm: server-based           │   │
│   │          Replica CS: read-only pod           │  │           vGPU: graphics-intensive          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Instant clone pools for non-persistent; full clone for persistent with profile.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Storage Standards               │  │              Protocol Standards             │   │
│   │          vSAN: preferred for pools           │  │            Blast Extreme: default           │   │
│   │           Separate OS from profile           │  │             UDP: Blast over 8443            │   │
│   │         vSAN dedupe: instant clones          │  │            PCoIP: legacy use only           │   │
│   │         Profile: CIFS share or vVol          │  │         HTML5: fallback for browsers        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Desktop ESXi hosts need high RAM (512GB+) and fast storage for pool density;                         │
│  Connection Server VMs need 8 vCPU / 32GB RAM per 4000 sessions.                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server= Horizon broker; max 4000 concurrent sessions                                      │
│  Replica CS    = secondary Connection Server; read-only LDAP replica                                  │
│  UAG           = Unified Access Gateway; external session proxy                                       │
│  Instant clone = forked from running parent VM in seconds                                             │
│  Full clone    = independent persistent VM; user-assigned                                             │
│  RDS farm      = RDSH hosts delivering published apps or desktops                                     │
│  Blast Extreme = VMware display protocol; adaptive UDP/TCP                                            │
│  PCoIP         = PC over IP; Teradici protocol; use for legacy clients                                │
│  vSAN dedupe   = space savings on instant clone OS disks                                              │
│  vGPU          = NVIDIA GRID partition; for CAD/graphics VDI                                          │
│  Profile share = Windows file share for DEM/FSLogix user profiles                                     │
│  Pod           = group of Connection Servers in same broadcast domain                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
### App Volumes Storage

| Object | Typical Size |
|---|---|
| AppStack (per app package) | 1–10 GB |
| Writable Volume (per user) | 10–30 GB |
| Total AppStack storage | (# of AppStacks × avg size) — plan for 20% growth |
| Total writable volume storage | (# of users with WV × WV size) |

Store AppStacks on a datastore accessible to all ESXi hosts in the cluster (shared storage, vSAN, or NFS). Writable volumes require read-write access from the host where the desktop VM runs.

### Full Clone Pool Storage

Full Clone VMs are independent — no sharing:

```text
Total = N_VMs × (OS_disk + swap + data_disk)
Example: 50 VMs × (80 GB + 8 GB + 0 GB) = 4,400 GB
```

Add 20% headroom for snapshots during maintenance windows.

---

## VLAN and Network Design

### Recommended VLAN Segmentation

| VLAN | Purpose | Devices |
|---|---|---|
| VLAN-10 Management | Horizon management plane | Connection Servers, App Volumes Manager, DEM file server, vCenter |
| VLAN-20 Desktop | Desktop VM traffic (Blast/PCoIP from internal clients) | Instant Clone VMs |
| VLAN-30 RDS | RDS farm hosts | RDS Windows Server VMs |
| VLAN-40 DMZ | External-facing UAG interfaces | UAG internet-facing NICs |
| VLAN-50 UAG Backend | UAG to Connection Server proxy traffic | UAG backend NICs |

### Firewall Rules (key flows)

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Horizon Client (internal) | Connection Server | 443/TCP | Horizon broker |
| Horizon Client (internal) | Desktop VM | 8443/TCP+UDP | Blast Extreme |
| Horizon Client (internal) | Desktop VM | 4172/TCP+UDP | PCoIP |
| External client | UAG | 443/TCP | HTTPS + tunnel |
| External client | UAG | 8443/TCP+UDP | Blast Extreme |
| UAG | Connection Server | 443/TCP | Broker proxy |
| UAG | Desktop VM | 8443/TCP+UDP | Blast proxy |
| Connection Server | vCenter | 443/TCP | vSphere API |
| Connection Server | AD DCs | 389/TCP+UDP, 636/TCP, 88/TCP+UDP, 3268/TCP | LDAP, Kerberos, GC |
| Desktop VM | App Volumes Mgr | 443/TCP | AppStack mount |
| Desktop VM | DEM Config Share | 445/TCP | SMB policy read |

---

## UAG Sizing

### Appliance Size Options

| Size | vCPU | RAM | Max Concurrent Sessions | Use Case |
|---|---|---|---|---|
| Small (S) | 2 | 4 GB | 1,000 | Development, POC |
| Medium (M) | 4 | 8 GB | 2,000 | Standard production |
| Large (L) | 8 | 16 GB | 10,000 | High-density |

For production, deploy **Medium** UAGs minimum. For > 2,000 external concurrent sessions, use Large or deploy multiple UAGs behind a load balancer.

### UAG Network Interfaces

UAG supports 1-NIC, 2-NIC, or 3-NIC deployments:

| Deployment | Internet NIC | Management NIC | Backend NIC | Recommended |
|---|---|---|---|---|
| 1-NIC | Combined | Combined | Combined | POC only |
| 2-NIC | Separate | Combined with backend | Separate | Common production |
| 3-NIC | Separate | Separate | Separate | Maximum security |

---

## App Volumes Sizing

### App Volumes Manager

| Component | Sizing |
|---|---|
| App Volumes Manager VM | 4 vCPU, 8 GB RAM |
| SQL Server | 4 vCPU, 16 GB RAM (or SQL Express for <500 desktops) |
| AppStack cache on Manager | 4 GB RAM allocated to cache — default |
| Writable volume location | Shared datastore or NFS — must be accessible from all ESXi hosts |

### AppStack Design Rules

- One AppStack per application or related application suite (not monolithic)
- Maximum AppStack size: technically unlimited, practical limit ~40 GB (larger = slower attach)
- Maximum AppStacks assigned per user: 10 (practical limit — more degrades logon time)
- Test AppStack attach time at scale: target < 10 seconds per AppStack

---

## Golden Image Management

### Snapshot Naming Convention

```text
<OS>-<BaseVersion>-<PatchDate>-<Status>
Examples:
  Win11-23H2-20240312-TESTED
  Win11-23H2-20240312-PUBLISHED
  Win10-22H2-20240115-DEPRECATED
```

### Golden Image Update Process

```text
1. Power on golden image VM (do not publish during update)
2. Apply Windows updates, agent updates, application changes
3. Run internal test checklist (logon, app launch, App Volumes attach)
4. Shut down VM cleanly (do not snapshot while powered on)
5. Take snapshot with naming convention above (status: TESTED)
6. Publish snapshot to Instant Clone pool (Horizon Admin > Pool > Maintain > Push Image)
7. Set maintenance window: "Scheduled" (desktops refresh on next logoff) or "Force immediately"
8. Verify first wave of refreshed desktops — check error rate in pool
9. Update snapshot status to PUBLISHED after verification
10. Remove old DEPRECATED snapshots (> 3 months old) to free datastore space
```

### Agent Version in Golden Image

Keep Horizon Agent version within one minor version of Connection Server. Never run an older Connection Server with a newer Agent — unsupported. Check compatibility matrix before any update:

[VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/)

---

## Pod Federation — Cloud Pod Architecture (CPA)

CPA links multiple Horizon pods (at the same or different sites) into a single Global Entitlement. Users see one pool regardless of which site their desktop is provisioned from.

| Metric | Limit |
|---|---|
| Pods per CPA federation | 25 |
| Sites per CPA federation | 25 |
| Desktops per federation | 50,000 |
| Global entitlements per federation | 100 |

**When to use CPA:**
- Multi-site deployments where users need failover between sites
- Environments exceeding single-pod limits
- Providing a unified namespace across geographically distributed VDI

**CPA is not a replication technology** — it does not replicate VMs between sites. Each pod has its own VMs; CPA brokers the user to the appropriate pod.

---

## Naming Conventions

### Pools and Farms

```text
Format: <SITE>-<PERSONA>-<OS>-<TYPE>
Examples:
  LON-KW-W11-IC        London, Knowledge Worker, Win11, Instant Clone
  NYC-TW-W11-IC        New York, Task Worker, Win11, Instant Clone
  LON-RDS-APPS         London, RDS Published Apps Farm
  LON-PW-W11-FC        London, Power User, Win11, Full Clone
```

### Desktop VM Naming Pattern (Instant Clone)

```text
Format: <SITE>-<PERSONA>-{n:fixed=3}
Examples:
  LON-KW-{n:fixed=3}   → LON-KW-001, LON-KW-002, ..., LON-KW-200
  NYC-TW-{n:fixed=3}   → NYC-TW-001, NYC-TW-002
```

### Entitlement Groups (AD Groups)

```text
Format: VDI-<PoolName>-Users
Examples:
  VDI-LON-KW-W11-IC-Users
  VDI-NYC-TW-W11-IC-Users
  VDI-LON-RDS-APPS-Users
```

### UAG Appliance Names

```text
Format: uag-<site>-<index>
Examples:
  uag-lon-01, uag-lon-02
  uag-nyc-01
```
