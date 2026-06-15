---
tags:
  - troubleshooting
  - dr-operations
  - backup
  - known-issues
---
# DR Operations — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known issues in DR runbook operations covering failover testing, network re-IP, DNS cutover, and application restart sequencing.

*Applies to: DR operations across all platforms*
</div>

```text
┌──────────────────────────────── Backup Dr Operations Troubleshooting ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Dr Operations: Backup Dr Operations Troubleshooting platform                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │              Management: Backup Dr Operations Troubleshooting management console              │   │
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
│    Physical: Backup Dr Operations Troubleshooting infrastructure · management network · monitoring    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dr Operations      = Backup Dr Operations Troubleshooting platform overview and core concepts      │
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

- DR test failures are almost always sequencing or network issues, not storage failures.
- Always verify: DNS cutover, network re-IP, application dependency order, and authentication (AD/LDAP) at DR site before declaring DR success.

## Failover Testing

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Application accessible but returning stale data | Test failover using isolated network; production data not replicated to test environment | Use production replicas for tests; or create a dedicated DR test environment with data clone |
| DNS not resolving DR site FQDNs | DNS delegation to DR site DNS not configured | Pre-configure DR DNS servers with all application FQDNs before DR test |
| AD authentication failing at DR site | AD DCs at DR site not reachable or not promoted | Ensure at least one writable DC is at DR site; test AD replication health before failover |
| Applications start in wrong order (dependency failures) | Runbook sequence incorrect | Document and test startup sequence: DB → middleware → app → load balancer |

## Network Re-IP

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Servers have same IP at DR as production (IP conflict) | DR network is a copy of production; L2 extension used | Use L3 re-IP at DR site; or L2 extension with appropriate isolation |
| Load balancer VIPs not responding at DR | VIP not migrated or physical LB not configured at DR | Configure DR load balancer VIPs in advance; test via DR network before production failover |

## Storage

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| DR VM starts but filesystem read-only | Replication-based copy has filesystem journal in unclean state | Mount with recovery: `mount -o remount,rw /dev/<device>` (Linux) or run `chkdsk` (Windows) |

## See also

- [DR Operations — Common Issues](common-issues.md)
- [Veeam — Known Issues](../../veeam/troubleshooting/known-issues/)
- [VMware SRM — Known Issues](../../../virtualization/vmware/srm/troubleshooting/known-issues/)
