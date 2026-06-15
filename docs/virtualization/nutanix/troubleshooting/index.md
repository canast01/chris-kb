# Nutanix — Troubleshooting

<div class="kb-summary">
Nutanix troubleshooting guide — common operational problems, diagnostic tools and log locations, NCC health check interpretation, and Nutanix GSS escalation procedures.

*Applies to: AOS 6.x · AHV*
</div>

```text
┌──────────────────────── Nutanix Troubleshooting — Diagnostics and Escalation ─────────────────────────┐
│                                                                                                       │
│  Start with NCC; review Prism alerts; check logs; collect logbay bundle before                        │
│  contacting Nutanix GSS; include NCC output and cluster config details.                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Diagnostic Flow                │  │                Common Issues                │   │
│   │         1. Run NCC health_checks all         │  │          CVM down: cluster degraded         │   │
│   │            2. Review Prism alerts            │  │          Disk failure: auto-rebuild         │   │
│   │         3. Check cluster health tab          │  │         Network: CVM SSH unreachable        │   │
│   │           4. Collect logbay bundle           │  │         Storage: RF2 under threshold        │   │
│   │        5. Open GSS case if unresolved        │  │         Upgrade stuck: LCM task fail        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Never restart all CVMs simultaneously — use rolling restart via Prism or ncli.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Locations                 │  │                GSS Escalation               │   │
│   │           /home/nutanix/data/logs/           │  │           portal.nutanix.com case           │   │
│   │           Stargate: stargate.INFO            │  │          Severity: P1 (down) to P4          │   │
│   │          Cassandra: cassandra.INFO           │  │          Pre-collect: logbay bundle         │   │
│   │             Genesis: genesis.out             │  │        Include: cluster ID + version        │   │
│   │             NCC: ncc_output.log              │  │          AOS + AHV version required         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  CVM SSH for log access; Prism for GUI diagnostics; IPMI/iDRAC for OOB;                               │
│  logbay uploads directly to Nutanix FTP for GSS analysis.                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NCC           = Nutanix Cluster Check; run: ncc health_checks run_all                                │
│  logbay        = support bundle tool; collects all CVM logs into one bundle                           │
│  GSS           = Global Support Services; Nutanix support team                                        │
│  P1 severity   = cluster down or data loss risk; 24/7 Nutanix response                                │
│  Cluster ID    = unique identifier; found in Prism > Cluster Details                                  │
│  CVM restart   = restart storage services on one node; safe if rolling                                │
│  Stargate FATAL= storage I/O path failure; high priority; check logs now                              │
│  RF alert      = replication factor degraded; disk/node failure needs attention                       │
│  Cassandra     = metadata store; failures affect cluster operations broadly                           │
│  Genesis       = service manager on CVM; restart resolves many CVM issues                             │
│  LCM task fail = upgrade failed; check LCM logs; may need manual pre-upgrade                          │
│  Prism alerts  = Prism > Alerts; filter by critical before checking logs                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="common-issues/">
    <strong>Common Issues</strong>
    <span>CVM down, NCC failures, storage degraded, VM stuck power states, cluster full, and replication failures.</span>
  </a>
  <a class="kb-card" href="diagnostics/">
    <strong>Diagnostics</strong>
    <span>Key log locations, NCC check details, Stargate/Cassandra/Curator diagnostics, and support bundle collection.</span>
  </a>
  <a class="kb-card" href="escalation/">
    <strong>Escalation</strong>
    <span>When to call Nutanix GSS, severity classification, case opening procedure, and what to collect beforehand.</span>
  </a>
</div>
