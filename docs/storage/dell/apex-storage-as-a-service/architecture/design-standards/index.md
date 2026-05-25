# APEX Storage as a Service — Standards

```text
┌─────────────────────────── Dell Apex STaaS — Architecture Design Standards ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Apex design standards: tier selection, network isolation, redundancy, and sizing       │   │
│   │         Tier: Performance (NVMe) for latency-sensitive; Capacity (SAS) for bulk/backup        │   │
│   │          Network: dedicated iSCSI VLAN (jumbo MTU 9000) or FC fabric (dual-fabric HA)         │   │
│   │        Redundancy: dual-controller array; multipath on hosts (PowerPath or native MPIO)       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Workload profile → tier selection → network design → host multipath → committed sizing             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Tier Design         │  │        Network Design       │  │          Redundancy         │   │
│   │        Perf: <1ms lat       │  │        Dedicated VLAN       │  │       Dual controller       │   │
│   │       Cap: bulk/backup      │  │        MTU 9000 iSCSI       │  │        Dual fabric FC       │   │
│   │        File: NFS/SMB        │  │        Dual FC fabric       │  │        PowerPath MPIO       │   │
│   │          Mix tiers          │  │       NFS storage VLAN      │  │        No SPOF design       │   │
│   │        Size committed       │  │        OOB management       │  │       Alert thresholds      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Commit 70–80% of expected peak usage; burst covers spikes without capacity delays                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Area       │     Standard     │        Why        │      Verify      │      Notes       │   │
│   │    iSCSI MTU     │    9000 jumbo    │        Perf       │   ping -s 8972   │    End-to-end    │   │
│   │    Multipath     │  MPIO/PowerPath  │      HA paths     │   Paths active   │     ≥2 paths     │   │
│   │    Committed     │   70–80% peak    │    Cost control   │   Usage report   │   Burst covers   │   │
│   │    Monitoring    │  CloudIQ alert   │     Proactive     │   Alert config   │  80% threshold   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array (dual controller) · 10/25/100 GbE NICs · FC 16/32Gb HBAs                      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Performance tier = NVMe all-flash; sub-millisecond latency; suited to databases/VMs                │
│    Capacity tier    = SAS/NL-SAS; lower cost per TB; suited to backup, archive, file                  │
│    iSCSI VLAN       = Isolated VLAN for storage traffic; prevents broadcast interference              │
│    Jumbo MTU        = 9000-byte frames on iSCSI path; reduces CPU overhead                            │
│    Dual fabric      = Two independent FC fabrics; each HBA port on different fabric                   │
│    PowerPath        = Dell multipath software; active-active path policy for arrays                   │
│    MPIO             = Native OS multipath I/O; Windows/Linux alternative to PowerPath                 │
│    Committed size   = Contracted Apex STaaS capacity; billed monthly regardless of use                │
│    Burst threshold  = Capacity level triggering burst billing; configure alert at 80%                 │
│    OOB management   = Out-of-band management network for array controller access                      │
│    No SPOF          = No Single Point of Failure; dual fabric + dual controller + MPIO                │
│    Tier mix         = Mix Performance and Capacity tiers in same Apex subscription                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [APEX Storage as a Service](../../index.md) reference.

---

## Upgrade Notes

| Step | Action |
|---|---|
| 1 | Hardware firmware and lifecycle upgrades for APEX STaaS are Dell's responsibility — do not initiate firmware changes on APEX-managed infrastructure without coordination |
| 2 | Monitor the APEX Console for Dell-initiated maintenance notifications; Dell will schedule maintenance windows for upgrades and communicate via the Console |
| 3 | Confirm Secure Connect Gateway is at the current recommended version — SCG upgrades can be triggered from the APEX Console or SCG management interface |
| 4 | After any Dell-initiated maintenance, verify all subscriptions show healthy status in APEX Console and confirm on-premises platform availability from the host side |

## Design Standards

- Deploy two SCG appliances for redundancy; register each APEX system to both
- Monitor APEX Console alerts daily — infrastructure issues are Dell's responsibility but customer must confirm SLA compliance
- Request capacity tier increases at least 30 days before projected threshold breach
- Document subscription ID, contract end date, committed tier, and burst thresholds in a runbook
