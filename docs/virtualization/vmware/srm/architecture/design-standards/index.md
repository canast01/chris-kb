# SRM — Design Standards


<div class="kb-summary">
Design Standards reference covering Test Network Design, IP Customization Strategy, Recovery Plan Structure Best Practices, RPO Targets and SRA Capability, Test Frequency Recommendations and 1 more sections.
</div>

  Replication Topology + Recovery Plan Structure
```text
┌──────────────────────────────────── VMware SRM — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│  SRM design standards define RPO tiers, protection group structure, test frequency,                   │
│  recovery plan priority, and site-pair capacity requirements.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              RPO Tier Standards              │  │           Protection Group Design           │   │
│   │          Tier 1: ≤15min (ABR/sync)           │  │          Group by application tier          │   │
│   │           Tier 2: ≤1h (vSR async)            │  │              One plan per group             │   │
│   │           Tier 3: ≤4h (vSR async)            │  │           Startup order: DB first           │   │
│   │          Tier 4: 24h (non-critical)          │  │          Dependencies: script wait          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  RPO tier drives replication technology choice; group VMs by app dependency.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Recovery Site Standards            │  │                Test Standards               │   │
│   │          Capacity: 100% Tier 1 VMs           │  │           Test: at least quarterly          │   │
│   │          Standby: Tier 2–4 (burst)           │  │            Document RTO achieved            │   │
│   │              N+1 hosts minimum               │  │           Cleanup: auto after test          │   │
│   │             Same vSAN disk count             │  │          Evidence: screenshot plan          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Recovery site needs compute and storage for Tier 1 VMs always on standby;                            │
│  WAN bandwidth must sustain replication traffic for all tiers.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; acceptable data loss window                                │
│  RTO           = Recovery Time Objective; time to restore service                                     │
│  Tier 1        = most critical; <15min RPO; ABR or vSR 5min                                           │
│  Protection group= set of VMs with same replication and recovery plan                                 │
│  Startup order = SRM powers on VMs in sequence; DB before app                                         │
│  Script wait   = custom step; waits for service health before next VM                                 │
│  Burst capacity= recovery site scales up on failover from off state                                   │
│  N+1 hosts     = recovery site has one host spare for HA during DR                                    │
│  Quarterly test= regulatory minimum for most DR frameworks                                            │
│  Evidence      = screenshot + log of test outcome for audit                                           │
│  Cleanup       = SRM removes test VMs and snapshots after test                                        │
│  WAN BW        = replication bandwidth; plan for peak replication rate                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
enabled), 0.5 (no compression)

Example:
VM daily change rate = 50 GB
With compression: (50 × 8192) / (86400 × 0.7) = 6.8 Mbps
```text

---

## Test Frequency Recommendations

| Activity | Recommended Frequency |
|---|---|
| Full Recovery Plan test (all VMs) | Quarterly minimum; semi-annually acceptable for stable environments |
| Partial test (critical VMs only) | Monthly |
| Protection Group health review | Weekly (automated script or SRM dashboard) |
| RPO compliance check | Daily (automated alert) |
| Network mapping validation | Each time infrastructure changes at either site |
| SRA connectivity check | Weekly |
| SRM license validity check | Monthly |

Regular testing is the only way to confirm recovery plans actually work. Document test results and resolve any failures before the next scheduled test.

---

## SRM Design Checklist

### Pre-Implementation

- [ ] vCenter versions at both sites are SRM-compatible (same major version required).
- [ ] SRM version is compatible with vCenter version (check VMware Compatibility Guide).
- [ ] Network connectivity between sites meets port requirements.
- [ ] Recovery site has sufficient compute, memory, and storage for all protected VMs.
- [ ] Storage replication is configured and healthy at array level before SRM installation.
- [ ] VR Appliances sized for VM count and change rate.
- [ ] Recovery site network (VLANs / NSX segments) mirrors protected site topology.
- [ ] IP customization strategy decided (subnet mapping / per-VM / DHCP).
- [ ] DNS strategy for IP re-addressing defined.
- [ ] SRM service account created with minimum required privileges.

### Post-Implementation

- [ ] All Protection Groups show status **OK**.
- [ ] All protected VMs have placeholder VMs at recovery site.
- [ ] Network mappings configured for all port groups used by protected VMs.
- [ ] Folder and resource mappings configured.
- [ ] Test failover completed for all Recovery Plans.
- [ ] Test cleanup completed successfully.
- [ ] Test failover results documented.
- [ ] RPO compliance monitored and all VMs within target RPO.

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Protection Group | `PG-<tier>-<site-pair>` | `PG-DB-DC1DC2` |
| Recovery Plan | `RP-P<priority>-<tier>-<site-pair>` | `RP-P1-DB-DC1DC2` |
| vSphere Replication group | `VR-<app>-<env>` | `VR-ERP-PROD` |
| Test network (bubble) | `vPG-SRM-Test-Bubble` | — |


## Priority Tiers

| Priority | Application Class | RPO | RTO |
|---|---|---|---|
| P1 | Mission-critical (financial, ERP core) | 0 (SRDF/S) | < 15 min |
| P2 | Business-critical (standard apps) | ≤ 30 min | < 1 hour |
| P3 | Non-critical (dev mirror, reporting) | ≤ 4 hours | < 4 hours |

### Protection Group to Recovery Plan Mapping




## Recovery Plan Design

- Power-on sequence is mandatory: infrastructure VMs (DC, DNS) → DB tier → APP tier → WEB tier
- Each step must include a health check (custom script or vSphere Replication quiescing check)
- IP customisation rules must be configured for every VM in a non-same-subnet recovery design
- Boot dependencies: set appropriate per-step delays (e.g., wait 120 seconds after DB server boot before starting APP servers)


## Test Frequency and Documentation

| Test Type | Minimum Frequency | Documentation |
|---|---|---|
| Recovery plan test (non-disruptive) | Quarterly | Change record + test report |
| Live failover drill (maintenance window) | Annually | Post-incident review document |
| Failback validation after drill | After each live drill | Separate change record |

Test reports must include:
1. Date, time, and personnel involved
2. RTO achieved vs. target
3. Any failed steps and root cause
4. Outstanding action items with owners and due dates


## SRA Standards

| Storage Platform | SRA | Minimum Version |
|---|---|---|
| Dell PowerMax | Dell SRA for PowerMax | v5.0+ |
| Pure FlashArray | Pure Storage SRA | v3.0+ |
| NetApp ONTAP | NetApp SRA | v4.0+ |
| VMware vSphere Replication | Built-in (no SRA needed) | VR 8.x |

Install SRA on both SRM servers (protected and recovery site). Re-scan array managers after SRA update.


## Datastore Mapping Standards

- Every source datastore must have a recovery-site counterpart documented in the SRM datastore mapping
- Datastore mappings must be validated as part of quarterly test (verify VMs register on correct datastores post-test)
- Placeholder VMs: SRM creates placeholder VMs on recovery-site datastores; ensure recovery datastores have adequate free space for placeholders plus recovered VMs
