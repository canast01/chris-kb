---
tags:
  - troubleshooting
  - aria-operations
  - vmware
  - known-issues
---
# VMware Aria Operations — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Aria Operations (vROps) bugs, error codes, and workarounds covering collector issues, adapter failures, and alerting.

*Applies to: Aria Operations 8.x*
</div>

```text
┌──────────────────────────────── Virtualization Vmware Aria Operations ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Vmware: Virtualization Vmware Aria Operations platform                    │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │              Management: Virtualization Vmware Aria Operations management console             │   │
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
│    Physical: Virtualization Vmware Aria Operations infrastructure · management network · monitoring   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Aria Operations platform overview and core concepts     │
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

- Aria Operations errors appear in `Administration → Management → Collector Groups` and `Administration → Management → Solutions`.
- Logs: `/data/vcops/log/` on the Analytics cluster node; key log is `vcops-analytics.log`.

## Adapters and Collectors

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vCenter adapter shows `No data collecting` | Aria Ops 8.x | Adapter credentials expired or vCenter certificate changed | Re-validate vCenter credentials in adapter instance; accept new cert fingerprint | N/A |
| Remote Collector shows `Offline` after IP change | Aria Ops 8.x | Collector registered with old IP; cluster can't reach it | Re-register Collector with new IP; update Collector IP in cluster settings | N/A |
| `SNMP adapter timeout` for network device | Aria Ops 8.x | SNMP community string incorrect or UDP 161 blocked | Verify community string; verify UDP 161 from Collector to device | N/A |
| CIM adapter fails: `SSL handshake failure` | Aria Ops 8.x | ESXi CIM SSL certificate not trusted by Aria Ops | Add ESXi CIM certificate to Aria Ops trust store | N/A |

## Alerting and Dashboards

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Alert `High CPU` never clears despite low CPU | Aria Ops 8.x | Cancel threshold not configured (only trigger threshold set) | Set `Cancel Trigger` in alert definition to auto-cancel when metric normalizes | N/A |
| Dashboard widget shows `No Data` for custom metric | Aria Ops 8.x | Metric path typo in widget configuration | Verify metric path via `Administration → Metric Configuration`; use metric picker | N/A |

## Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Data node stuck in `Initializing` after cluster expand | Aria Ops 8.x | Time skew >60s between cluster nodes | Sync NTP on all nodes; verify same NTP source | N/A |
| Analytics node OOM — containers restarting | Aria Ops 8.x | Insufficient RAM for inventory size | Upgrade VM to minimum 48 GB RAM for large environments (>5000 objects) | N/A |

## See also

- [VMware Aria Operations — Common Issues](common-issues.md)
- [VMware Aria Operations for Logs — Known Issues](../../aria-operations-for-logs/troubleshooting/known-issues/)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues/)
