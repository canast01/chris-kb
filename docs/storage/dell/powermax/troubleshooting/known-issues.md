---
tags:
  - troubleshooting
  - powermax
  - dell
  - known-issues
---
# Dell PowerMax — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known PowerMax bugs, error codes, and workarounds covering Unisphere, SRDF, host connectivity, and Solutions Enabler.

*Applies to: PowerMax 2000/8000, Unisphere 10.x, SE 10.x*
</div>

```text
┌──────────────────────────────────────────── Dell PowerMax ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerMax: high-end enterprise NVMe all-flash array for mission-critical workloads       │   │
│   │                      Protocols: FC · iSCSI · NVMe-oF · SRDF (replication)                     │   │
│   │                     Management: Unisphere for PowerMax / Solutions Enabler                    │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │            Cache            │  │          DRAM 2 TB+         │  │        Sub-ms latency       │   │
│   │         FE director         │  │        FC/iSCSI ports       │  │         Host facing         │   │
│   │         BE director         │  │         NVMe drives         │  │        Storage facing       │   │
│   │             SRDF            │  │         RDF director        │  │       Metro/remote DR       │   │
│   │          TimeFinder         │  │         SnapVX/Clone        │  │       Local protection      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    SRDF Sync     │   Zero-RPO DR    │    RDF protocol   │   Certificate    │   Metro <200ms   │   │
│   │    SRDF Async    │  Near-zero RPO   │    RDF protocol   │   Certificate    │   Any distance   │   │
│   │    TimeFinder    │ Local snapshots  │      Internal     │ Solutions Enabl  │   256 snaps/SG   │   │
│   │Solutions Enabler │   CLI/API mgmt   │    HTTPS/symcli   │   Certificate    │     Symm CLI     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerMax 2500/8500 engine · FE/BE/RDF directors · DRAM cache · expansion bays            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerMax           = Dell flagship NVMe all-flash array; millions of IOPS at sub-millisecond late  │
│    SRDF               = Symmetrix Remote Data Facility; sync/async metro and remote site replication  │
│    TimeFinder SnapVX  = space-efficient snapshot technology; up to 256 snapshots per storage group    │
│    Storage group      = logical container for volumes sharing service level and host access policy    │
│    Service level      = performance target for a storage group: Diamond, Platinum, Gold, Silver       │
│    FE director        = front-end director providing FC or iSCSI host-facing ports on the engine      │
│    BE director        = back-end director connecting engine cache to NVMe flash drive bays            │
│    RDF director       = SRDF director providing dedicated bandwidth for replication traffic           │
│    Solutions Enabler  = CLI and API toolkit; symcli commands cover all PowerMax management            │
│    Unisphere          = web GUI and REST API server for PowerMax; unified management interface        │
│    DCM                = Dynamic Cache Management; auto-balances workloads across available cache res  │
│    Service level obj. = workload performance class assigned to storage group; enforced by DPTM        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- PowerMax alerts appear in Unisphere for PowerMax → Alerts Dashboard.
- Use `symcfg list -health` via Solutions Enabler to get array health status.
- ESRS / SRS must be active for Dell proactive support and SRDF remote replication monitoring.

## Host Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Host sees LUN but cannot write — `No access` | PowerMax | Masking view not including host initiator | Add host initiator to correct masking view in Unisphere → Host Groups | N/A |
| iSCSI host loses path after PowerMax iSCSI IP change | PowerMax | Host iSCSI discovery DB not updated | Run `iscsiadm -m discovery -t st -p <new-ip>`; reconnect sessions | N/A |

## SRDF

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| SRDF/S pair shows `Not Ready` | PowerMax | WAN link interruption; SRDF suspended itself | Resume SRDF: `symrdf -g <dev-group> resume`; verify RTT ≤5ms | N/A |
| SRDF/A journal overflow | PowerMax | Delta changes exceed journal capacity during WAN outage | Expand journal LUN; reduce SRDF/A cycle time; ensure WAN recovery before journal fills | N/A |

## Unisphere

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Unisphere UI shows `Array unavailable` | Unisphere 10.x | SYMAPI server not running on Unisphere host | Restart: `symapid stop; symapid start` | N/A |
| Performance dashboard shows `No data` | Unisphere 10.x | Performance data collection not enabled | Enable: Unisphere → System → Manage → Performance Collection | N/A |

## Solutions Enabler

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `stordaemon` not running — all SE commands fail | SE 10.x | `stordaemon` service crashed | Restart: `stordaemon restart all` | N/A |
| `Error 40: No devices discovered` | SE 10.x | SYMAPI server not connected to PowerMax | Check SYMAPI config: `cat /opt/emc/SYMCLI/bin/symapi/config/options` | N/A |

## See also

- [Dell PowerMax — Common Issues](common-issues/)
- [Dell SRDF-A — Known Issues](../../srdf-a/troubleshooting/known-issues.md)
- [Dell SRDF-S — Known Issues](../../srdf-s/troubleshooting/known-issues.md)
