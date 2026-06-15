---
tags:
  - recoverpoint
  - dell
  - networking
  - firewall
  - ports
  - replication
  - dr
---
# Dell RecoverPoint — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell RecoverPoint (RP). Covers Unisphere for RecoverPoint management, RPA (RecoverPoint Appliance) cluster communication, and WAN replication between sites.

*Applies to: RecoverPoint 5.x / 6.x*
</div>

```text
┌────────────────────────────────────── Storage Dell Recoverpoint ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Dell: Storage Dell Recoverpoint platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Storage Dell Recoverpoint management console                   │   │
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
│    Physical: Storage Dell Recoverpoint infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell               = Storage Dell Recoverpoint platform overview and core concepts                 │
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


## Inbound — Management

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin workstations | Unisphere for RecoverPoint web UI and REST API |
| 22 | TCP | Jump hosts | SSH — RPA CLI (admin/root access) |
| 7225 | TCP | RecoverPoint Management Application (boxmgmt) | RecoverPoint internal management (legacy CLI) |

## RPA Cluster Communication (Within Site)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 7218 | TCP | RPA nodes (within site) | RPA internal cluster communication |
| 7225 | TCP | RPA nodes (within site) | RPA management channel |

## WAN Replication (Between Sites — Cross Firewall)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 11111 | TCP | RPA (Site A) ↔ RPA (Site B) | RecoverPoint WAN replication data |
| 7218 | TCP | RPA (Site A) ↔ RPA (Site B) | RecoverPoint cross-site control channel |

## RecoverPoint to Storage (SAN)

RecoverPoint splitters intercept I/O at the storage or host level via FC or iSCSI — the storage side is typically FC fabric (no IP rules). For IP-based (Software Splitter on host):

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | RPA → vCenter | vSphere integration (vRPA software splitter management) |

## Outbound — RPA to External

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 162 | UDP | SNMP receiver | SNMP traps |
| 514 | UDP | Syslog server | RPA syslog |
| 123 | UDP | NTP | Time sync |
| 25 | TCP | SMTP relay | Alert email |
| 443 | TCP | esrs.dell.com | ESRS support |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin clients | RecoverPoint mgmt IP | 443, 22 | Unisphere and CLI |
| RPA nodes (site) | RPA nodes (site) | 7218, 7225 | Local cluster — same VLAN preferred |
| RPA (Site A) | RPA (Site B) | 11111, 7218 | WAN replication — must cross inter-site firewall |

## Verify

```bash
# From admin workstation — test Unisphere for RP
curl -sk -o /dev/null -w "%{http_code}" https://<rp-mgmt-ip>/rest/v2/clusters

# From Site A RPA — test WAN replication port to Site B
nc -zv <site-b-rpa-ip> 11111

# From Site A RPA — test control channel to Site B
nc -zv <site-b-rpa-ip> 7218
```

## See also

- [Dell RecoverPoint — Architecture](how-it-works/)
- [Dell RecoverPoint — Operations](../operations/)
- [Dell SRDF-A — Ports](../../srdf-a/architecture/ports/)
