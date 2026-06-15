---
tags:
  - troubleshooting
  - networking
  - known-issues
---
# Networking — Known Issues Reference

<div class="kb-summary">
Index of protocol-specific known issues and error codes for networking components. This top-level page links to per-protocol known-issues catalogs.

*Applies to: All network protocols in this KB*
</div>

```text
┌───────────────────────────── Networking Troubleshooting Known Issues.Md ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Troubleshooting: Networking Troubleshooting Known Issues.Md platform             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │           Management: Networking Troubleshooting Known Issues.Md management console           │   │
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
│    Physical: Networking Troubleshooting Known Issues.Md infrastructure · management network · monito  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Troubleshooting    = Networking Troubleshooting Known Issues.Md platform overview and core concep  │
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

For network issues, identify the protocol layer first before looking up specific errors:
- **Layer 3** (IP routing, VPN) → check routing tables, MTU, firewall logs
- **Layer 4** (TCP/UDP port) → check firewall rules, port open/close status
- **Layer 7** (application protocol) → check the specific protocol known-issues page below

## Protocol Known-Issues Pages

| Protocol | Known Issues |
|---|---|
| DNS | [DNS — Known Issues](protocols/dns/troubleshooting/known-issues/) |
| NFS | [NFS — Known Issues](protocols/nfs/troubleshooting/known-issues/) |
| SMB / CIFS | [SMB — Known Issues](protocols/smb/troubleshooting/known-issues/) |
| iSCSI | [iSCSI — Known Issues](protocols/iscsi/troubleshooting/known-issues/) |
| Fibre Channel | [FC — Known Issues](protocols/fibre-channel/troubleshooting/known-issues/) |
| TLS / SSL | [TLS — Known Issues](protocols/tls/troubleshooting/known-issues/) |
| LDAP / LDAPS | [LDAP — Known Issues](protocols/ldap/troubleshooting/known-issues/) |

## See also

- [Networking — Common Issues](index.md)
- [Brocade Fabric OS — Known Issues](../san/brocade/fabric-os/troubleshooting/known-issues/)
- [Cisco MDS — Known Issues](../san/cisco/mds/troubleshooting/known-issues/)
