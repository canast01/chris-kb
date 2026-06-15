---
tags:
  - troubleshooting
  - recoverpoint
  - dell
  - known-issues
---
# Dell RecoverPoint — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known RecoverPoint bugs, error codes, and workarounds covering RPA clustering, replication groups, and failover.

*Applies to: RecoverPoint for VMs (RP4VM) 5.x / RecoverPoint Classic 5.x*
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


## Before you begin

- RecoverPoint errors appear in Unisphere for RecoverPoint → Alerts.
- `rpcheck` tool on the RPA for connectivity diagnostics.
- Most replication failures are WAN port (11111/7218) or storage splitter issues.

## Replication Groups

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Replication group `Error — link lost` | RecoverPoint 5.x | TCP 11111 or 7218 blocked between RPA clusters | Verify ports 11111/7218 between RPA management IPs cross-site | N/A |
| RPO violation alarm despite recent writes | RecoverPoint 5.x | WAN bandwidth saturated; replication behind | Reduce replication group bandwidth limit; or increase WAN capacity | N/A |
| `Splitter error` on vSphere with RP4VM | RP4VM 5.x | RP4VM vSphere plugin not registered on ESXi host | Re-register RP4VM splitter on affected ESXi hosts | N/A |

## RPA Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| RPA cluster shows `Partial failure` | RecoverPoint 5.x | One RPA offline in HA pair | Check RPA hardware; cluster continues with degraded HA | N/A |
| `RPA cluster communication error` | RecoverPoint 5.x | Port 7225 blocked between RPAs within cluster | Verify TCP 7225 between all RPAs in the same cluster | N/A |

## Failover

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Test failover success but production failover fails | RecoverPoint 5.x | Production failover requires additional steps (enable access on copy) | Follow RecoverPoint failover procedure: `Enable Image Access` → `Failover` | N/A |
| `Cannot failover — consistency group not synchronized` | RecoverPoint 5.x | Group behind RPO; data may be lost | Accept data loss up to last consistent image; or wait for sync | N/A |

## See also

- [Dell RecoverPoint — Common Issues](common-issues.md)
- [Dell VPLEX — Known Issues](../../vplex/troubleshooting/known-issues/)
