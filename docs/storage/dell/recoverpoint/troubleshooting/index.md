---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# RecoverPoint — Troubleshooting



<div class="kb-summary">
Diagnosing RecoverPoint replication failures, consistency group errors, splitter connectivity, and RPO violations.

*Applies to: RecoverPoint 5.x*
</div>

```text
┌─────────────────────────────────── RecoverPoint — Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            RecoverPoint — Troubleshooting Approach                            │   │
│   │                   1  Identify: which job, component, or resource is failing                   │   │
│   │                  2  Scope: single job vs all jobs; one source vs all sources                  │   │
│   │             3  Collect: logs and run status command; review recent change history             │   │
│   │                 4  Diagnose: match symptoms to known issues; check error codes                │   │
│   │                     5  Fix: apply resolution; verify fix; monitor next run                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │         Application         │  │             Data            │   │
│   │        Network checks       │  │         Log analysis        │  │        Catalog check        │   │
│   │        Storage space        │  │       Job error codes       │  │         Consistency         │   │
│   │        Process health       │  │        Auth failures        │  │       Corruption scan       │   │
│   │       443 (mgmt HTTPS)      │  │        Timeout errors       │  │         Restore test        │   │
│   │        Firewall rules       │  │        Version compat       │  │          RPO drift          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>CG errors, journal overflow, splitter failures, and RPO violations.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, support bundle collection, and diagnostic commands.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Dell support engagement, SR creation, and log collection.</span>
</a>

</div>

