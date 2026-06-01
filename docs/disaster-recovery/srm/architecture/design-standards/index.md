# SRM Architecture — Standards


<div class="kb-summary">
Standards reference covering Naming Conventions, Priority Tiers, Recovery Plan Design, Test Frequency and Documentation, SRA Standards and 1 more sections.
</div>

```text
┌─────────────────────────────────────── SRM — Design Standards ────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Sizing Guidelines               │  │               HA Requirements               │   │
│   │         Deduplicate where supported          │  │           N+1 component redundancy          │   │
│   │          Bandwidth: 10 GbE minimum           │  │          Heartbeat / health monitor         │   │
│   │          Storage: 130% of raw data           │  │          Separate mgmt / data VLANs         │   │
│   │         Latency: < 10 ms to storage          │  │          Out-of-band access (IPMI)          │   │
│   │           CPU: 8+ vCPU for engine            │  │          Anti-affinity VM placement         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ports: 443 (SRM HTTPS) · 9086 (SRM-SRM pairing) · 443 (vCenter)                                    │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Standard SRM Design Rules                                   │   │
│   │            RPO target drives snapshot/cycle frequency — document in service design            │   │
│   │            RTO target drives recovery tier: instant, warm standby, or cold restore            │   │
│   │                  Dedicated backup network VLAN — no shared production traffic                 │   │
│   │      Encryption: SRM management TLS; replication encryption controlled by array/SRA layer     │   │
│   │               Service accounts: minimum privilege; rotate credentials quarterly               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SRM](../../index.md) reference.

---

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
