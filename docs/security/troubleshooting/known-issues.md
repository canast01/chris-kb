---
tags:
  - troubleshooting
  - security
  - known-issues
---
# Security — Known Issues Reference

<div class="kb-summary">
Index of security product known issues and error codes. This top-level page links to per-product known-issues catalogs.

*Applies to: CyberArk PAM, Venafi TPP, PKI / Certificates*
</div>

```text
┌────────────────────────────── Security Troubleshooting Known Issues.Md ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Troubleshooting: Security Troubleshooting Known Issues.Md platform              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Security Troubleshooting Known Issues.Md management console            │   │
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
│    Physical: Security Troubleshooting Known Issues.Md infrastructure · management network · monitori  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Troubleshooting    = Security Troubleshooting Known Issues.Md platform overview and core concepts  │
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

Security product issues often cascade — a CyberArk CPM failure may stem from an AD authentication issue, which may stem from a certificate expiry. Follow the dependency chain.

## Security Product Known-Issues Pages

| Product | Known Issues |
|---|---|
| CyberArk PAM | [CyberArk — Known Issues](cyberark/troubleshooting/known-issues/) |
| Venafi TPP | [Venafi — Known Issues](venafi/troubleshooting/known-issues/) |
| Certificates / PKI | [Certificates — Known Issues](certificates/troubleshooting/known-issues/) |

## See also

- [Security — Common Issues](index.md)
- [Active Directory — Known Issues](../compute/windows-server/active-directory/troubleshooting/known-issues/)
- [TLS — Known Issues](../networking/protocols/tls/troubleshooting/known-issues/)
