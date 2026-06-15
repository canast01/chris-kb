---
tags:
  - troubleshooting
  - san
  - certifications
  - known-issues
---
# SAN Certifications — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known issues related to SAN certification exam preparation — covering common exam topic misunderstandings, lab environment issues, and practice test discrepancies.

*Applies to: Brocade BCFP, Cisco CCNP Data Center (SAN track), CompTIA Storage+*
</div>

```text
┌───────────────────────────────── Certifications San Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        San: Certifications San Troubleshooting platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │               Management: Certifications San Troubleshooting management console               │   │
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
│    Physical: Certifications San Troubleshooting infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    San                = Certifications San Troubleshooting platform overview and core concepts        │
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

- SAN certification labs require access to physical or virtual FC switch environments — GNS3 / EVE-NG do not emulate FC.
- Practice exams vary widely in quality — cross-reference with official study guides for discrepancies.

## Lab Environment Issues

| Issue | Cause | Workaround |
|---|---|---|
| Brocade Virtual Fabric OS trial expired | 30-day trial license | Use Brocade vFOS OVA; register for free trial reset; or use GNS3 community images |
| Cannot access Cisco DCNM in lab | DCNM licensing required for full features | Use Cisco dCloud for free lab access to DCNM |
| Zoning changes not persisting in practice lab | Lab environment resetting between sessions | Save configuration: `cfgsave` (Brocade) or `copy running-config startup-config` (Cisco MDS) |

## Exam Preparation

| Issue | Cause | Workaround |
|---|---|---|
| Practice exam question contradicts official guide | Third-party practice exam outdated or incorrect | Trust official Brocade/Cisco documentation; verify via official study guides |
| FC protocol questions mixing FC-SW and FCoE | FCoE is a separate protocol — exam questions distinguish them | Review FC-SW (native FC) vs FCoE (FC over Ethernet) as separate topics |

## See also

- [SAN — Common Issues](index.md)
- [Brocade Fabric OS — Known Issues](../../../san/brocade/fabric-os/troubleshooting/known-issues/)
- [Cisco MDS — Known Issues](../../../san/cisco/mds/troubleshooting/known-issues/)
