# Horizon — Design Standards

## Connection Server Sizing

### Per-Server Limits

| Metric | Recommended Limit | Hard Limit |
|---|---|---|
| Concurrent sessions per Connection Server | 2,000 | 4,000 (not recommended) |
| Connection Servers per pod | 2 (min HA) – 7 (max) | 7 |
| vCenter instances per pod | 1 (typical) – 10 | 10 |
| Desktops per pod (Instant Clone) | 10,000 | ~15,000 |
| Pools per pod | 200 | 200 |

### Connection Server VM Sizing

| Environment Scale | vCPU | RAM | Disk |
|---|---|---|---|
| Small (<500 concurrent) | 4 | 10 GB | 60 GB |
| Medium (500–2000 concurrent) | 8 | 16 GB | 60 GB |
| Large (2000+ concurrent) | 8–12 | 16–24 GB | 60 GB |

Connection Server is CPU-bound at high session counts. Do not over-commit CPU on the ESXi host running Connection Server VMs. Recommend dedicated management cluster.

### HA Requirements

- **Minimum 2 Connection Servers** per pod for HA — one can go down without service impact
- All Connection Servers replicate configuration via AD LDS (ADAM) — no shared database required
- Place behind a load balancer or DNS round-robin for client distribution
- Do not place all Connection Servers on the same ESXi host — use anti-affinity rules

```powershell
# PowerCLI — create anti-affinity DRS rule for Connection Servers
$cluster = Get-Cluster "Management-Cluster"
$vms = Get-VM "cs01","cs02","cs03"
New-DrsRule -Cluster $cluster -Name "CS-AntiAffinity" -KeepTogether $false -VM $vms -Enabled $true
```

---

## Desktop VM Sizing

### Standard Sizing by Persona

| Persona | Typical Use Case | vCPU | RAM | OS Disk | Notes |
|---|---|---|---|---|---|
| Task Worker | Call center, data entry, browser-only | 2 | 4 GB | 60 GB | High desktop density on ESXi |
| Knowledge Worker | Office apps, email, Teams/Zoom | 2–4 | 6–8 GB | 60 GB | Majority of enterprise VDI |
| Power User | Developer, analyst, multiple monitors | 4–8 | 8–16 GB | 80 GB | May need vGPU |
| GPU User | CAD, 3D, video editing | 4–8 | 16–32 GB | 80 GB | vGPU required (NVIDIA GRID) |
| RDS Session | Shared desktop/published app | N/A (host-level) | 2 GB/session | N/A | Size RDS host, not session |

### RDS Host Sizing

| RDS Host Size | vCPU | RAM | Concurrent Sessions |
|---|---|---|---|
| Small | 8 | 32 GB | 20–30 |
| Medium | 16 | 64 GB | 40–60 |
| Large | 32 | 128 GB | 80–120 |

Actual session density depends heavily on workload. Test with load simulation (LoginVSI or similar) before production sizing.

### ESXi Host Desktop Density

Rule of thumb for Instant Clone pools (no vGPU):

| Desktop Persona | Desktops per ESXi Host (dual-socket, 28–32 physical cores, 384 GB RAM) |
|---|---|
| Task Worker (2 vCPU / 4 GB) | 100–150 |
| Knowledge Worker (4 vCPU / 8 GB) | 50–80 |
| Power User (8 vCPU / 16 GB) | 25–40 |

Apply a CPU over-commit ratio of 4:1 (vCPU:pCPU) for task workers, 3:1 for knowledge workers. Monitor CPU ready (%) — keep below 5% average.

---

## Storage Sizing

### Instant Clone Storage Per Pool

| Object | Size per Desktop | Notes |
|---|---|---|
| Golden image OS disk | 40–80 GB | Shared via replica — one copy per datastore |
| Replica VM disk | = Golden image | Read-only, shared across all children |
| Parent VM disk | Thin delta above replica | Small — typically <1 GB |
| Child VM OS delta disk | 2–10 GB | Grows during session; reset on logoff |
| Child VM swap/memory | = Guest RAM | On same datastore; size accordingly |

**Practical formula:**
```
Total datastore capacity = (Replica size × 1) + (N_desktops × avg_delta × 1.25)
Example: 60 GB replica + (200 desktops × 5 GB delta × 1.25) = 60 + 1250 = 1,310 GB per datastore
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

```
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

```
<OS>-<BaseVersion>-<PatchDate>-<Status>
Examples:
  Win11-23H2-20240312-TESTED
  Win11-23H2-20240312-PUBLISHED
  Win10-22H2-20240115-DEPRECATED
```

### Golden Image Update Process

```
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

```
Format: <SITE>-<PERSONA>-<OS>-<TYPE>
Examples:
  LON-KW-W11-IC        London, Knowledge Worker, Win11, Instant Clone
  NYC-TW-W11-IC        New York, Task Worker, Win11, Instant Clone
  LON-RDS-APPS         London, RDS Published Apps Farm
  LON-PW-W11-FC        London, Power User, Win11, Full Clone
```

### Desktop VM Naming Pattern (Instant Clone)

```
Format: <SITE>-<PERSONA>-{n:fixed=3}
Examples:
  LON-KW-{n:fixed=3}   → LON-KW-001, LON-KW-002, ..., LON-KW-200
  NYC-TW-{n:fixed=3}   → NYC-TW-001, NYC-TW-002
```

### Entitlement Groups (AD Groups)

```
Format: VDI-<PoolName>-Users
Examples:
  VDI-LON-KW-W11-IC-Users
  VDI-NYC-TW-W11-IC-Users
  VDI-LON-RDS-APPS-Users
```

### UAG Appliance Names

```
Format: uag-<site>-<index>
Examples:
  uag-lon-01, uag-lon-02
  uag-nyc-01
```
