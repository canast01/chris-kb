# PowerMax — Standards

```text
┌───────────────────────────── Dell PowerMax Architecture Design Standards ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Design standards define SLO selection, SRDF topology, FC zoning, and SRP sizing rules     │   │
│   │    SLO tier matched to workload IOPS profile: Diamond = latency-critical, Bronze = archive    │   │
│   │      SRDF topology: Metro for zero-RPO HA, Async for DR; Adaptive Copy for data movement      │   │
│   │      FC zoning: single-initiator / single-target per zone; no zone sprawl across fabrics      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Profile workload → select SLO → size SRP → define masking view → configure SRDF topology           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        SLO Standards        │  │        SRDF Standards       │  │       Zoning Standards      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Diamond: <1ms DB      │  │       Metro: zero RPO       │  │        SI/ST per zone       │   │
│   │        Platinum: <2ms       │  │       Sync: near-zero       │  │        2 fabrics min        │   │
│   │       Gold: <5ms mixed      │  │       Async: RPO mins       │  │         VSAN tagging        │   │
│   │        Silver: <10ms        │  │        Adaptive: bulk       │  │        NPIV per host        │   │
│   │       Bronze: archive       │  │       RDF group per SG      │  │        No zone sprawl       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SRP sizing → SRDF consistency group → masking view → host-side multipath (PowerPath/MPIO)          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Standard     │       Rule       │     Rationale     │   Anti-pattern   │      Impact      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       SLO        │ Match IOPS tier  │  Predictable perf │   All Diamond    │   Cost overrun   │   │
│   │       SRP        │Per-workload pool │  Avoid contention │   One SRP all    │  Noisy neighbor  │   │
│   │       SRDF       │  Metro + Async   │   HA + DR layers  │    Sync only     │  No DR fallback  │   │
│   │      Zoning      │  SI/ST per zone  │  Fault isolation  │ Multi-init zone  │   Masking gaps   │   │
│                                                                                                       │
│    Physical: dual-fabric SAN; RDF directors on dedicated SRDF links; separate mgmt network            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SI/ST          = Single-Initiator/Single-Target; one HBA port and one array port per zone          │
│    SRDF Metro     = Active-active stretch cluster; both R1 and R2 volumes serve production I/O        │
│    SRDF Async     = Asynchronous replication; RPO in seconds to minutes; DR site standby              │
│    Adaptive Copy  = Non-disruptive bulk migration or data movement; no consistency guarantee          │
│    RDF group      = Logical SRDF pairing; each group maps one set of volumes to a remote array        │
│    NPIV           = N-Port ID Virtualization; virtual WWN per VM for per-VM zoning                    │
│    Consistency grp= SRDF consistency group; ensures write-order fidelity across volumes               │
│    PowerPath      = Dell multipath driver; load balancing and failover for PowerMax hosts             │
│    MPIO           = Native OS multipath (Windows/Linux) as alternative to PowerPath                   │
│    Noisy neighbor = SRP contention when unrelated workloads share a pool; mitigated by SLO            │
│    VSAN tagging   = Brocade/Cisco zoning attribute to restrict zone scope to a VSAN                   │
│    Zone sprawl    = Excessive zone membership causing management overhead and masking risk            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Symmetrix ID (SID) | 3–12 digit serial, used as-is | `000123456789` |
| Storage Group | `<site>-<app>-<tier>-SG` | `LON-ORACLE-P1-SG` |
| Device Group | `<site>-<app>-DG` | `LON-ORACLE-DG` |
| Port Group | `<site>-<fabric>-PG` | `LON-FAB-A-PG` |
| Initiator Group | `<hostname>-IG` | `db01-LON-IG` |
| Masking View | `<hostname>-<sg>-MV` | `db01-LON-LON-ORACLE-P1-MV` |
| SRDF Group | `RDFg<number>-<site-pair>` | `RDFg10-LON-AMS` |
| SnapVX Snapshot | `<app>-snap-<YYYYMMDD>` | `ORACLE-snap-20260501` |
| RDF Port Group | `<site>-RDF-PG` | `LON-RDF-PG` |

## Build Baseline

Every new PowerMax deployment should meet the following baseline before handover to operations:

- **Solutions Enabler** installed on at least two management hosts (primary and secondary) and pointing to the production SID.
- **Unisphere for PowerMax** deployed as a vApp or physical appliance; connected to the array and secondary SE host.
- **Embedded Management** enabled on the array for break-glass SYMCLI access without external SE.
- **PowerPath/VE** (VMware) or **PowerPath** (Linux/Windows) installed on all production hosts; multipath policy set to `Optimized`.
- **SRDF groups** defined with the remote array and tested for both SRDF/S (synchronous) and SRDF/A (asynchronous) pairs where required.
- **FAST VP** policies configured; at minimum one SLO assigned to production storage groups.
- **SnapVX** expiry policies configured on all storage groups to enforce maximum snapshot retention.
- **Alert thresholds** configured in Unisphere: response time >2 ms, port utilisation >70%, thin pool >75%.
- **Service Level Objectives (SLOs)** assigned to all production storage groups (`Diamond`, `Platinum`, `Gold`, `Silver`, `Bronze`, or `Optimized`).
- **Solutions Enabler symapi.db** backed up after initial configuration.

## Configuration Checklist

- [ ] Array registered in CMDB with SID, model, location, and owning team
- [ ] Solutions Enabler `netcnfg` file updated to include the array SID and IP
- [ ] Unisphere for PowerMax configured with LDAP/AD authentication and local admin account disabled
- [ ] All front-end director ports zoned correctly; zoning validated with `symcfg -sid <SID> show`
- [ ] Storage groups created per application with correct SLO assigned
- [ ] Masking views created and verified — hosts can see LUNs and I/O is confirming on both paths
- [ ] SRDF groups created, pairs established, and pair states confirmed `Synchronized` or `Consistent`
- [ ] SnapVX policy set on all production storage groups; first snapshot tested and linked
- [ ] FAST VP policy active; tier movement verified after 24 hours of production I/O
- [ ] Syslog and SNMP trap forwarding configured to monitoring platform
- [ ] Quarterly review schedule set for capacity, SRDF health, and SnapVX quota usage

## Sizing Guidelines

| Dimension | Guidance |
|---|---|
| Model selection | PowerMax 2000 for up to ~8 PB effective capacity and moderate I/O; PowerMax 8000 for up to ~4 PB raw / 350+ PB effective with data reduction |
| Global memory | 1.5 TB (2000) to 16 TB (8000); more memory improves write-cache hit rate and reduces drive latency |
| Drive count | Scale drives per engine based on workload IOPS and capacity requirements; target <70% of raw capacity used |
| SRDF bandwidth | Size SRDF links at 120% of peak write throughput for SRDF/S; use SRDF/A delta set size to estimate bandwidth for async |
| Thin provisioning | Allow 2:1 to 3:1 oversubscription for general-purpose workloads; monitor subscribed vs. consumed capacity weekly |
| SnapVX impact | Each snapshot session consumes metadata capacity; plan for <128 snapshots per device to maintain headroom |
| Data reduction | Expected effective capacity ratio: 4:1 to 5:1 for mixed workloads with compression and deduplication enabled |
