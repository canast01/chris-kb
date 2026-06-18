---
tags:
  - troubleshooting
  - srdf
  - dell
  - known-issues
---
# Dell SRDF/S — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SRDF/S (Synchronous) bugs, error codes, and workarounds. SRDF/S is zero-RPO synchronous replication — issues typically manifest as production I/O latency when the WAN link degrades.

*Applies to: PowerMax SRDF/S*
</div>

```text
┌───────────────────────────────────────── Storage Dell Srdf S ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Dell: Storage Dell Srdf S platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Storage Dell Srdf S management console                      │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Storage Dell Srdf S infrastructure · management network · monitoring                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell               = Storage Dell Srdf S platform overview and core concepts                       │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- SRDF/S requires consistent ≤5ms RTT between sites — latency above this directly increases production host I/O response time.
- `symrdf -g <dev-group> query` for pair state; `symrdf -g <dev-group> verify` for integrity check.
- A WAN outage will cause SRDF/S to pause (R-state `Suspended`) — production continues on R1 in Read/Write mode.

## Link and Latency

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Production I/O latency elevated during peak load | PowerMax | WAN latency spike above 5ms RTT causes SRDF/S write to delay production commit | Check WAN RTT: `symrdf -g <dg> query` for estimated link latency; contact WAN provider | N/A |
| SRDF/S pair `Suspended` | PowerMax | WAN link lost; PowerMax suspended replication to protect production | Restore WAN link; resume: `symrdf -g <dg> resume` | N/A |

## Failover

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Planned failover fails: `R1 devices still accessible` | PowerMax | Source site not fenced; both sites trying to own devices | Confirm source site is fenced from SAN fabric before issuing failover | N/A |
| Post-failover applications report read errors | PowerMax | Residual writes in flight at failover moment | Investigate with application team; SRDF/S guarantees consistency — I/O errors are application layer | N/A |

## See also

- [Dell SRDF-S — Common Issues](common-issues/)
- [Dell PowerMax — Known Issues](../../powermax/troubleshooting/known-issues.md)
- [Dell SRDF-A — Known Issues](../../srdf-a/troubleshooting/known-issues.md)
