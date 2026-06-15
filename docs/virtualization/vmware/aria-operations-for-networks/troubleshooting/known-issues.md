---
tags:
  - troubleshooting
  - aria-operations-for-networks
  - vmware
  - known-issues
---
# VMware Aria Operations for Networks — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Aria Operations for Networks (vRNI) bugs, error codes, and workarounds covering collector connectivity, data source configuration, and flow analysis.

*Applies to: Aria Operations for Networks 6.x*
</div>

```text
┌───────────────────────── Virtualization Vmware Aria Operations For Networks ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Vmware: Virtualization Vmware Aria Operations For Networks platform              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │       Management: Virtualization Vmware Aria Operations For Networks management console       │   │
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
│    Physical: Virtualization Vmware Aria Operations For Networks infrastructure · management network   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Aria Operations For Networks platform overview and cor  │
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

- vRNI errors appear in `Settings → Infrastructure and Support → Data Sources`.
- Logs: SSH to Platform node; logs under `/home/ubuntu/log/`.

## Data Sources

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vCenter data source shows `Auth failed` | vRNI 6.x | vCenter credentials changed or service account locked | Update credentials in vRNI data source settings | N/A |
| NSX-T data source `Connection timeout` | vRNI 6.x | Collector cannot reach NSX Manager on 443 | Verify TCP 443 from Collector to NSX Manager IPs | N/A |
| `SNMP collection failed` for physical switch | vRNI 6.x | SNMP v2c community string mismatch or UDP 161 blocked | Update community string; verify UDP 161 from Collector to switch | N/A |

## Flow Analysis

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| IPFIX flows not appearing from NSX | vRNI 6.x | IPFIX not enabled on NSX logical switches | Enable IPFIX on NSX-T via `Fabric → Profiles → IPFIX Collector Profile` | N/A |
| Flow data missing for specific VMs | vRNI 6.x | VM not in inventory scope of connected vCenter | Ensure VM's vCenter is added as data source; resync inventory | N/A |

## Platform

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Platform UI unreachable` after upgrade | vRNI 6.x | Upgrade script left `nginx` service in failed state | SSH to Platform: `service nginx restart` | N/A |
| Collector shows `Offline` after reboot | vRNI 6.x | Collector appliance NTP drift from Platform | Sync Collector NTP source with Platform; restart Collector registration | N/A |

## See also

- [VMware Aria Operations for Networks — Common Issues](common-issues.md)
- [VMware NSX — Known Issues](../../nsx/troubleshooting/known-issues/)
- [VMware Aria Operations — Known Issues](../../aria-operations/troubleshooting/known-issues/)
