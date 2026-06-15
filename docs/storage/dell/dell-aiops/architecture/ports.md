---
tags:
  - dell-aiops
  - dell
  - networking
  - firewall
  - ports
  - monitoring
---
# Dell AIOps — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell AIOps (AI-driven operations platform for Dell infrastructure). Dell AIOps aggregates telemetry from storage, compute, and networking components and provides predictive analytics.

*Applies to: Dell AIOps / CloudIQ AIOps*
</div>

```text
┌─────────────────────────────────────── Storage Dell Dell Aiops ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Dell: Storage Dell Dell Aiops platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Storage Dell Dell Aiops management console                    │   │
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
│    Physical: Storage Dell Dell Aiops infrastructure · management network · monitoring                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell               = Storage Dell Dell Aiops platform overview and core concepts                   │
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


## How It Works

Dell AIOps is a cloud-delivered (SaaS) analytics layer built on top of CloudIQ and ESRS telemetry. On-premise components send data outbound to Dell's cloud — no on-premise AIOps server is deployed.

## Outbound — Infrastructure to Dell Cloud (Required)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | All monitored array management IPs | cloudiq.dell.com, aiops.dell.com, esrs.dell.com | Telemetry upload for AIOps analytics |

## Admin Access (SaaS)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | cloudiq.dell.com | Admin browser — AIOps dashboards and recommendations |

## Firewall Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Array mgmt IPs | cloudiq.dell.com | 443 | Telemetry for AIOps — same as CloudIQ |
| Admin browsers | cloudiq.dell.com | 443 | SaaS access |

## See also

- [Dell AIOps — Architecture](how-it-works/)
- [Dell CloudIQ — Ports](../../cloudiq/architecture/ports/)
