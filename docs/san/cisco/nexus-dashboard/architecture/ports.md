---
tags:
  - cisco
  - nexus-dashboard
  - san
  - networking
  - firewall
  - ports
---
# Cisco Nexus Dashboard — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Cisco Nexus Dashboard (ND). Nexus Dashboard is the modern replacement for DCNM, providing multi-fabric management for NX-OS switches and MDS SANs via Nexus Dashboard Fabric Controller (NDFC).

*Applies to: Cisco Nexus Dashboard 3.x / NDFC 12.x*
</div>

```text
┌────────────────────────────────────── San Cisco Nexus Dashboard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Cisco: San Cisco Nexus Dashboard platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: San Cisco Nexus Dashboard management console                   │   │
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
│    Physical: San Cisco Nexus Dashboard infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cisco              = San Cisco Nexus Dashboard platform overview and core concepts                 │
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


## Inbound — Admin to Nexus Dashboard

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin browsers | Nexus Dashboard web UI and REST API |
| 22 | TCP | Jump hosts | SSH — ND appliance OS access (rescue/diagnostic) |

## Nexus Dashboard to Managed Devices

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 22 | TCP | ND | NX-OS switches, MDS | SSH — device configuration and telemetry |
| 161 | UDP | ND | NX-OS switches, MDS | SNMP polling |
| 443 | TCP | ND | NX-API capable switches | NX-API REST |
| 830 | TCP | ND | Devices supporting NETCONF | NETCONF over SSH |

## Inbound — From Managed Devices to ND

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 162 | UDP | NX-OS / MDS switches | ND | SNMP traps |
| 9898 | TCP | Switches (streaming telemetry) | ND | gRPC telemetry ingestion |

## Nexus Dashboard Cluster (Node-to-Node)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 443 | TCP | ND nodes | Inter-node API |
| 2379/2380 | TCP | ND nodes | etcd peer (consensus) |
| 8884 | TCP | ND nodes | Cluster keepalive |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin clients | ND | 443 | UI and REST API |
| ND | Managed devices | 22, 161 UDP, 443 | Management |
| Devices | ND | 162 UDP, 9898 | Traps and streaming telemetry |
| ND nodes | ND nodes | 443, 2379, 2380 | Cluster internal |

## Verify

```bash
# From admin workstation — test ND API
curl -sk -o /dev/null -w "%{http_code}" https://<nd-ip>/login

# From ND — test switch SSH
nc -zv <switch-ip> 22

# From ND — test SNMP
snmpget -v2c -c <community> <switch-ip> 1.3.6.1.2.1.1.1.0
```

## See also

- [Cisco Nexus Dashboard — Architecture](how-it-works/)
- [Cisco DCNM — Ports](../../cisco-dcnm/architecture/ports/)
- [Cisco MDS — Ports](../../mds/architecture/ports/)
