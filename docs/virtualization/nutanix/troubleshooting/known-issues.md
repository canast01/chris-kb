---
tags:
  - troubleshooting
  - nutanix
  - known-issues
---
# Nutanix — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Nutanix AOS / AHV bugs, error codes, and workarounds covering CVM, storage, AHV networking, and Prism issues.

*Applies to: Nutanix AOS 6.x / AHV 20220304.x+*
</div>

```text
┌─────────────────────────────── Virtualization Nutanix Troubleshooting ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    Nutanix: Virtualization Nutanix Troubleshooting platform                   │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │             Management: Virtualization Nutanix Troubleshooting management console             │   │
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
│    Physical: Virtualization Nutanix Troubleshooting infrastructure · management network · monitoring  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Nutanix            = Virtualization Nutanix Troubleshooting platform overview and core concepts    │
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

- Run `cluster status` from any CVM to check all services.
- Nutanix NCC (Node Configuration Checker): `ncc health_checks run_all` from any CVM.
- CVM logs under `/home/nutanix/data/logs/` — key log is `stargate.out` for storage issues.

## CVM and Services

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| CVM service `Stargate` in crash loop | AOS 6.x | Disk I/O error on SSD tier causing Stargate panic | Check `disk_operator.out` for SMART errors; replace failing disk | N/A |
| `Zookeeper not running` on single CVM | AOS 6.x | CVM network partition or CVM OOM | Restart CVM; check CVM memory allocation (min 20 GB reserved) | N/A |
| `Cassandra` ring not converging after node addition | AOS 6.x | New node NTP skew from cluster | Sync NTP on new node; run `nodetool status` from CVM to verify ring | N/A |

## Storage

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VM disk I/O latency spikes during dedup/compression | AOS 6.x | Background data transformation running during peak hours | Schedule data transformation during off-peak via Prism → Data Resiliency | N/A |
| Storage container full but cluster has free capacity | AOS 6.x | Container reservation set too high | Remove or reduce reservation on container; capacity redistributes automatically | N/A |
| vDisk stuck in `Under Replicated` state | AOS 6.x | Node in maintenance mode with insufficient data copies | Exit maintenance mode; or increase replication factor temporarily | N/A |

## AHV Networking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VM loses connectivity after AHV host upgrade | AOS 6.x | OVS bridge reconfigured during upgrade; bond mode changed | Verify OVS bond mode matches upstream switch LACP settings post-upgrade | N/A |
| VLAN traffic not passing for guest VMs | AOS 6.x | VLAN not configured on Prism network; upstream trunk missing | Add VLAN in Prism → VM Network; verify upstream switch trunk includes VLAN ID | N/A |

## Prism

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Prism Central login fails: `SSO metadata error` | Prism Central 2022.x | IdP metadata URL unreachable | Verify Prism Central can reach IdP metadata URL on 443; or re-upload metadata manually | N/A |
| Prism alert `Disk I/O timeout` not clearing | AOS 6.x | Historical alert not auto-resolving | Manually resolve alert in Prism → Alerts after confirming disk is healthy | N/A |

## See also

- [Nutanix — Common Issues](common-issues.md)
- [Nutanix — Diagnostics](diagnostics.md)
