---
tags:
  - troubleshooting
  - confluence
  - itsm
  - known-issues
---
# Confluence — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Confluence Data Center bugs, error codes, and workarounds covering Synchrony (collaborative editing), clustering, and database issues.

*Applies to: Confluence Data Center 8.x*
</div>

```text
┌─────────────────────────────────── Itsm Confluence Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Confluence: Itsm Confluence Troubleshooting platform                     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                 Management: Itsm Confluence Troubleshooting management console                │   │
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
│    Physical: Itsm Confluence Troubleshooting infrastructure · management network · monitoring         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Confluence         = Itsm Confluence Troubleshooting platform overview and core concepts           │
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

- Confluence logs: `<confluence-home>/logs/atlassian-confluence.log`.
- Synchrony (collaborative editing) logs: `<confluence-home>/logs/atlassian-synchrony.log`.
- Most collaborative editing failures are Synchrony (port 8091) connectivity issues.

## Synchrony (Collaborative Editing)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot collaborate — Synchrony not available` | Confluence DC 8.x | Synchrony process not running or port 8091 blocked | Restart Synchrony; verify TCP 8091 between browser and Confluence server | N/A |
| Collaborative editing not syncing between users | Confluence DC 8.x | Synchrony cluster split — nodes not communicating | Check `<confluence-home>/synchrony-args.properties` cluster config; verify TCP 25500 between nodes | N/A |

## Clustering

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Node joining cluster failed` | Confluence DC 8.x | Hazelcast port 5701 blocked | Verify TCP 5701 between all Confluence DC nodes | N/A |
| Cache inconsistency after node restart | Confluence DC 8.x | Node rejoined cluster with stale cache | Full node restart; cache refreshes automatically on join | N/A |

## Database

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Confluence startup fails: `Cannot connect to database` | Confluence DC 8.x | Database server unreachable or wrong credentials in `confluence.cfg.xml` | Verify DB connectivity; update credentials in `<confluence-home>/confluence.cfg.xml` | N/A |

## See also

- [Confluence — Common Issues](common-issues.md)
- [Jira — Known Issues](../../jira/troubleshooting/known-issues/)
- [PostgreSQL — Known Issues](../../../compute/linux/postgresql/troubleshooting/known-issues/)
