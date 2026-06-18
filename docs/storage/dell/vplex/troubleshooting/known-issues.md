---
tags:
  - troubleshooting
  - vplex
  - dell
  - known-issues
---
# Dell VPLEX — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known VPLEX bugs, error codes, and workarounds covering Metro clustering, WAN COM, and host connectivity.

*Applies to: VPLEX GeoSynchrony 6.x*
</div>

```text
┌───────────────────────────────────────────── Dell VPLEX ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        VPLEX: federated storage virtualisation and active-active cross-site clustering        │   │
│   │                                     Protocols: FC · iSCSI                                     │   │
│   │                        Management: VPLEX Management Server / vplex CLI                        │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │        Virtualisation       │  │         Backend LUNs        │  │      Abstracted to VVs      │   │
│   │            Metro            │  │         Sync stretch        │  │        <5ms RTT sites       │   │
│   │             Geo             │  │      Async replication      │  │         Any distance        │   │
│   │          Clustering         │  │        Active-active        │  │       Shared namespace      │   │
│   │            Quorum           │  │          Witness VM         │  │      Split-brain guard      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Virtual volume  │ Virtualised LUN  │      FC/iSCSI     │    FC zoning     │   Multi-vendor   │   │
│   │  Metro cluster   │   Sync stretch   │   Inter-cluster   │   Certificate    │    2-site max    │   │
│   │     Witness      │  Quorum arbiter  │       HTTPS       │   Certificate    │     3rd site     │   │
│   │     WAN-COM      │ Geo replication  │   Encrypted WAN   │   Certificate    │     Geo only     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: VPLEX VS2/VS6 appliance · FC fabric · backend arrays · WAN link (Metro/Geo)              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VPLEX              = Dell storage federation; aggregates arrays into virtual volumes across vendo  │
│    Virtual volume     = VPLEX-abstracted LUN presented to hosts; backend is array LUNs                │
│    VPLEX Metro        = synchronous active-active stretch cluster; same VV served from two sites      │
│    VPLEX Geo          = asynchronous active-active replication; higher RPO, no distance constraint    │
│    Distributed VV     = virtual volume spanning two sites for Metro active-active host access         │
│    Witness            = third-site quorum arbiter for Metro; prevents split-brain island scenarios    │
│    WAN-COM            = WAN communication module in VPLEX Geo; manages inter-site replication traffi  │
│    Management Server  = embedded Linux VM in VPLEX engine; serves web UI and vplex CLI                │
│    Consistency group  = set of virtual volumes that failover together maintaining write order         │
│    Backend volume     = LUN from underlying array presented to VPLEX engine for virtualisation        │
│    Local device       = RAID device or extent of backend volumes on a single VPLEX cluster            │
│    Cluster            = single VPLEX installation; Metro topology requires exactly two clusters       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- VPLEX errors appear in the VPLEX Management Console → Alerts.
- `vplexcli` on each engine for CLI diagnostics.
- Metro cluster health: `cluster witness show` — witness must be reachable for Metro split-brain protection.

## Metro Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cluster witness unreachable` alarm | GeoSynchrony 6.x | TCP 443 blocked between witness and both VPLEX engines | Verify witness connectivity; witness is critical for Metro split-brain arbitration | N/A |
| VPLEX Metro splits to single-site after network partition | GeoSynchrony 6.x | WAN COM link lost AND witness unreachable — VPLEX suspends IO on losing site | Restore WAN COM (TCP 443 between engines); restore witness connectivity | N/A |
| I/O suspended on surviving site after split | GeoSynchrony 6.x | Expected protection behavior when arbitration fails | Manually designate winner: `cluster witness force-winner` (requires careful DR process) | N/A |

## WAN COM

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `WAN COM link degraded` | GeoSynchrony 6.x | WAN latency too high (>5ms RTT) or packet loss | Check WAN link quality; VPLEX Metro requires ≤5ms RTT | N/A |

## Host Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Host sees duplicate devices after VPLEX zone change | GeoSynchrony 6.x | Old Fibre Channel zone still active in SAN fabric | Remove old FC zone; rescan host HBA | N/A |

## See also

- [Dell VPLEX — Common Issues](common-issues/)
- [Dell RecoverPoint — Known Issues](../../recoverpoint/troubleshooting/known-issues.md)
