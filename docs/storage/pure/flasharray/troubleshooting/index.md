---
tags:
  - pure
  - troubleshooting
---
# FlashArray — Troubleshooting


<div class="kb-summary">
FlashArray — Troubleshooting navigation for Common Issues, Diagnostics, Escalation.
</div>
```text
┌────────────────────────────────── Pure FlashArray — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          FlashArray troubleshooting: structured diagnostic process for common issues          │   │
│   │         Start with health dashboard, then check recent changes, then review event logs        │   │
│   │        Collect support bundle before contacting vendor support to accelerate resolution       │   │
│   │         Escalation matrix: L1 → L2 → vendor support based on severity and SLA targets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check health → review changes → examine logs → diagnose → resolve                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         Controllers         │  │        Active-active        │  │           No SPOF           │   │
│   │            Drives           │  │         DirectFlash         │  │         NVMe native         │   │
│   │           Volumes           │  │       Thin provisioned      │  │        Instant clone        │   │
│   │        ActiveCluster        │  │       Sync replication      │  │           Zero RPO          │   │
│   │           SafeMode          │  │       Immutable snaps       │  │      Ransomware resist      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  ActiveCluster   │ Stretch cluster  │    Internal RPC   │   Certificate    │  Active-active   │   │
│   │     SafeMode     │ Locked snapshots │      Internal     │   Pure support   │ Eradicator lock  │   │
│   │ Protection group │ Snap/replication │      Internal     │    Admin role    │   Policy-based   │   │
│   │     ActiveDR     │     Async DR     │    Internal RPC   │   Certificate    │   RPO seconds    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FlashArray//X or //C controllers · DirectFlash NVMe modules · 25/100 GbE / 32Gb FC       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashArray         = Pure all-NVMe block/file array; inline dedup and compression always enabled   │
│    DirectFlash        = Pure proprietary NVMe modules; direct flash access without SAS translation    │
│    ActiveCluster      = synchronous active-active stretch cluster; hosts see a single namespace       │
│    ActiveDR           = asynchronous replication to DR site; recovery point objective in seconds      │
│    SafeMode           = admin-locked immutable snapshots; cannot be deleted even by array administr...│
│    Protection group   = set of volumes and hosts sharing a snapshot and replication schedule          │
│    purefa CLI         = REST CLI tool for FlashArray; purefa CLI connects via REST API key            │
│    purearray          = purectl CLI command: purearray list and purearray show monitoring             │
│    Volume tag         = user-defined key-value label on volumes for policy and reporting purposes     │
│    Host group         = logical collection of hosts sharing volume access via a host group object     │
│    Inline dedup       = content-based deduplication performed inline before data is written to flash  │
│    Evergreen          = Pure architecture; controllers upgrade non-disruptively, shelves remain in ...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
FlashArray Triage Entry Points
  Alert type ──► purealert list
       │
       ├── Hardware ──► puredrive list / purehw list
       │                └── Open Pure support case if drive failed
       │
       ├── Connectivity ──► purehost list + pureport list
       │                    └── Check FC zoning / iSCSI network
       │
       ├── Replication ──► purepod list + purepod list --replicating
       │                   └── Check inter-array replication link
       │
       ├── Performance ──► purearray monitor / purevol monitor
       │                   └── Check QoS limits, check queue depth
       │
       └── Escalate ──► Pure1 diagnostics ──► Open support case
                        └── purediag --send (upload bundle to case)
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
