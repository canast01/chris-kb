---
tags:
  - troubleshooting
  - aria-operations-for-logs
  - vmware
  - known-issues
---
# VMware Aria Operations for Logs — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Aria Operations for Logs (vRLI) bugs, error codes, and workarounds covering syslog ingestion, agent issues, and cluster problems.

*Applies to: Aria Operations for Logs 8.x*
</div>

```text
┌─────────────────────────── Virtualization Vmware Aria Operations For Logs ────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Vmware: Virtualization Vmware Aria Operations For Logs platform                │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │         Management: Virtualization Vmware Aria Operations For Logs management console         │   │
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
│    Physical: Virtualization Vmware Aria Operations For Logs infrastructure · management network · mo  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Aria Operations For Logs platform overview and core co  │
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

- Aria Ops for Logs errors appear in `Administration → Cluster Management`.
- Logs: `/var/log/loginsight/` on each cluster node.
- Most ingestion issues are syslog format mismatch or port/firewall problems.

## Syslog Ingestion

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Syslog events not appearing from ESXi hosts | Aria Logs 8.x | ESXi syslog target configured for UDP 514 but vRLI only listening on TCP | Change ESXi syslog to TCP 514, or enable UDP listener in vRLI | N/A |
| `Events dropped — queue full` under burst load | Aria Logs 8.x | Insufficient worker threads for ingestion spike | Scale out Aria Logs cluster; add worker node | N/A |
| Windows agent events not appearing | Aria Logs 8.x | CFAPI port 9543 blocked from Windows host to vRLI | Verify TCP 9543 from Windows hosts to vRLI cluster VIP | N/A |

## Agents

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Linux agent stops collecting after OS upgrade | Aria Logs 8.x | Agent service not started after kernel update (systemd unit disabled) | Enable agent: `systemctl enable --now liagent` | N/A |
| Agent shows `Disconnected` in vRLI even though service running | Aria Logs 8.x | Agent config pointing to old vRLI IP/FQDN | Update `/var/lib/loginsight-agent/liagent.ini` with current vRLI VIP | N/A |

## Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Master node fails election — cluster degraded | Aria Logs 8.x | Cluster internal port 9000 blocked between nodes | Verify TCP 9000 between all vRLI nodes | N/A |
| Disk usage alarm — events not being archived | Aria Logs 8.x | NFS archive target unreachable | Check NFS mount on vRLI nodes; verify NFS 2049 connectivity to archive server | N/A |

## See also

- [VMware Aria Operations for Logs — Common Issues](common-issues.md)
- [VMware Aria Operations — Known Issues](../../aria-operations/troubleshooting/known-issues/)
