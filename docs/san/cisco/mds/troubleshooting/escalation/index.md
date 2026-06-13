---
tags:
  - san
  - troubleshooting
---
# MDS — Escalation


<div class="kb-summary">
Escalation reference covering Opening a Support Case, Collecting show tech-support (Diagnostic Bundle), Required Information for SR, Support Contract Verification, Severity Levels and 2 more sections.
</div>

```text
┌─────────────────────────────── Cisco MDS — Troubleshooting Escalation ────────────────────────────────┐
│                                                                                                       │
│  Escalation path for MDS issues: internal triage → Cisco TAC → hardware RMA process.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Triage (L1/L2)            │  │          Cisco TAC Escalation (L3)          │   │
│   │       Confirm scope: single or fabric        │  │            Open SR: severity 1-4            │   │
│   │          Collect: show tech-support          │  │          Attach tech-support bundle         │   │
│   │         Check recent changes: config         │  │           TAC remote: Cisco WebEx           │   │
│   │        Check Cisco advisories: PSIRT         │  │         ISSU patch if bug confirmed         │   │
│   │        Isolate: disable suspect port         │  │           Hardware RMA if ASIC/SFP          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Internal triage captures state; TAC escalation requires SR + bundle within 30 min                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Criteria              │  │               Recovery Actions              │   │
│   │        Sev 1: production I/O impacted        │  │         ISSU: non-disruptive upgrade        │   │
│   │          Sev 2: degraded redundancy          │  │           Reload module: line card          │   │
│   │          Sev 3: intermittent errors          │  │          SFP swap: hot-plug capable         │   │
│   │            Sev 4: config question            │  │         Zone rollback: saved config         │   │
│   │         Always log start/end actions         │  │          Post-mortem: RCA document          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS chassis · SFP transceivers · ISL fiber · RMA spare parts · management network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SR             = Service Request; Cisco TAC case identifier                                          │
│  TAC            = Technical Assistance Center; Cisco support organization                             │
│  PSIRT          = Product Security Incident Response Team; Cisco security advisories                  │
│  ISSU           = In-Service Software Upgrade; NX-OS/MDS upgrade without reboot                       │
│  RMA            = Return Merchandise Authorization; defective hardware replacement                    │
│  Severity 1     = Production outage; Cisco commits to 1-hour response SLA                             │
│  tech-support   = All-in-one diagnostic bundle uploaded to Cisco CX Cloud                             │
│  RCA            = Root Cause Analysis; post-incident document identifying root failure                │
│  Zone rollback  = Reverting to a previously saved zoneset configuration                               │
│  Module reload  = Restarting a line card without rebooting the chassis                                │
│  Hot-plug SFP   = Transceiver replaceable while port is active (no chassis power-off)                 │
│  Cisco WebEx    = Collaboration tool used for TAC remote-assist sessions                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Contents of `show tech-support`:
- Running and startup configuration
- NX-OS version info, hardware inventory
- Interface state, port statistics
- VSAN database and zone configuration
- FCNS (Name Server) entries
- Syslog and error logs

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Required Information for SR

| Field | Where to Find |
|---|---|
| NX-OS version | `show version` |
| Serial number | `show inventory` or chassis label |
| VSAN topology | `show vsan` + `show fcdomain vsan <id>` |
| Error log excerpts | `show logging last 500` |
| Affected WWPNs | `show fcns database vsan <id>` |
| Problem description | Exact symptom, timestamps (with timezone), frequency |

## Support Contract Verification

Check SmartNet coverage:
- [cisco.com/go/contractcenter](https://www.cisco.com/c/en/us/support/index.html)
- `show inventory` provides serial numbers for all modules

## Severity Levels

| Severity | Criteria | SLA (SmartNet) |
|---|---|---|
| P1 | Fabric-wide outage; production I/O impacted | 1 hour (24/7) |
| P2 | Significant degradation; redundancy lost | 4 hours |
| P3 | Non-critical; workaround available | Next business day |
| P4 | How-to, enhancement request | Best effort |

## Common Escalation Path

1. Open TAC case online (faster for P3/P4)
2. Call TAC for P1/P2 to get immediate engineer assignment
3. No progress within SLA → request Technical Support Manager involvement in case notes
4. For firmware issues with known bugs: request upgrade to a specific recommended release

## NDFC Support

For issues with Nexus Dashboard Fabric Controller managing MDS switches, open SR against "Cisco Nexus Dashboard Fabric Controller (NDFC)" product and include NDFC support bundle:
- NDFC UI → Operations → Tech Support → Download
