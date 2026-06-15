---
tags:
  - cisco
  - dcnm
  - san
  - networking
  - firewall
  - ports
---
# Cisco DCNM — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Cisco DCNM (Data Center Network Manager). DCNM manages MDS SAN switches and NX-OS data center fabrics. Note: DCNM is being superseded by Nexus Dashboard Fabric Controller (NDFC).

*Applies to: Cisco DCNM 11.x*
</div>

```text
┌──────────────────────────────────────── San Cisco Cisco Dcnm ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Cisco: San Cisco Cisco Dcnm platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: San Cisco Cisco Dcnm management console                      │   │
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
│    Physical: San Cisco Cisco Dcnm infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cisco              = San Cisco Cisco Dcnm platform overview and core concepts                      │
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


## Inbound — Admin to DCNM Server

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin browsers | DCNM web UI and REST API |
| 22 | TCP | Jump hosts | SSH — DCNM appliance OS access |

## DCNM to Managed Devices

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 22 | TCP | DCNM | MDS switches, NX-OS devices | SSH — device configuration and monitoring |
| 161 | UDP | DCNM | MDS switches, NX-OS devices | SNMP polling |
| 443 | TCP | DCNM | NX-API capable devices | NX-API REST |

## Inbound — SNMP Traps from Devices

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 162 | UDP | MDS switches, NX-OS devices | DCNM | SNMP traps |

## DCNM Database

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 5432 | TCP | PostgreSQL (embedded or external) | DCNM configuration database |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin clients | DCNM | 443 | Web UI |
| DCNM | Managed switches | 22, 161 UDP, 443 | Management |
| Managed switches | DCNM | 162 UDP | SNMP traps |

## Verify

```bash
# From admin workstation — test DCNM API
curl -sk -o /dev/null -w "%{http_code}" https://<dcnm-ip>/api/v1/host

# From DCNM — test switch SSH
ssh admin@<mds-switch-ip> show version | head -3

# From DCNM — test SNMP
snmpget -v2c -c <community> <switch-ip> 1.3.6.1.2.1.1.1.0
```

## See also

- [Cisco DCNM — Architecture](how-it-works/)
- [Cisco Nexus Dashboard — Ports](../../nexus-dashboard/architecture/ports/)
- [Cisco MDS — Ports](../../mds/architecture/ports/)
