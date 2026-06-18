---
tags:
  - srdf
  - srdf-a
  - dell
  - powermax
  - networking
  - firewall
  - ports
  - replication
---
# Dell SRDF/A — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell SRDF/A (Symmetrix Remote Data Facility / Asynchronous). SRDF replicates data between PowerMax/VMAX arrays. FC-based SRDF uses the FC fabric (no IP ports). IP-based SRDF/A uses iSCSI or GigE ports on the array.

*Applies to: PowerMax SRDF/A with GigE / iSCSI links*
</div>

```text
┌───────────────────────────────────────── Storage Dell Srdf A ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Dell: Storage Dell Srdf A platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Storage Dell Srdf A management console                      │   │
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
│    Physical: Storage Dell Srdf A infrastructure · management network · monitoring                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell               = Storage Dell Srdf A platform overview and core concepts                       │
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


## SRDF Data Path — FC (No IP Rules Needed)

When SRDF uses Fibre Channel ISL links between arrays (most common), no IP firewall rules are required. FC traffic flows through the FC fabric zoning.

## SRDF Data Path — IP (GigE / iSCSI Links)

For SRDF/A configured over IP links between PowerMax arrays:

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 3260 | TCP | Source PowerMax GigE port ↔ Target PowerMax GigE port | SRDF/A asynchronous replication over iSCSI/IP |

The specific port may vary depending on the GigE director configuration on the array — confirm with `symcfg list -rdfg all` output.

## Unisphere Management

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 8443 | TCP | Admin workstations | Unisphere for PowerMax — SRDF configuration and monitoring |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| PowerMax GigE port (source) | PowerMax GigE port (target) | 3260 | IP-based SRDF only; FC-based needs no IP rules |
| Admin clients | PowerMax mgmt | 8443 | SRDF group management |

## Verify

```bash
# From admin workstation — test Unisphere
curl -sk -o /dev/null -w "%{http_code}" https://<powermax-ip>:8443/univmax/restapi/version

# Check SRDF group replication status via symcli
symrdf -g <rdfg-number> query
```

## See also

- [Dell SRDF/A — Architecture](how-it-works/)
- [Dell SRDF/S — Ports](../../srdf-s/architecture/ports.md)
- [Dell PowerMax — Ports](../../powermax/architecture/ports.md)
