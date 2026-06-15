---
tags:
  - troubleshooting
  - mysql
  - linux
  - known-issues
---
# MySQL — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known MySQL bugs, error codes, and workarounds covering replication, InnoDB, and Group Replication.

*Applies to: MySQL 8.0 / 8.4*
</div>

```text
┌───────────────────────────────────────── Compute Linux Mysql ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Linux: Compute Linux Mysql platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Compute Linux Mysql management console                      │   │
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
│    Physical: Compute Linux Mysql infrastructure · management network · monitoring                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Linux              = Compute Linux Mysql platform overview and core concepts                       │
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

- MySQL errors: `SHOW GLOBAL STATUS LIKE 'Last_Error'`; error log: `/var/log/mysql/error.log`.
- For InnoDB corruption: always stop MySQL cleanly; never force kill during InnoDB write.

## Connectivity

| Error Code | Description | Cause | Fix |
|---|---|---|---|
| Error 1045 | `Access denied for user` | Wrong password or no remote login grant | `GRANT ALL ON db.* TO 'user'@'%'; FLUSH PRIVILEGES;` |
| Error 2003 | `Can't connect to MySQL server` | MySQL not listening or port 3306 blocked | Check: `systemctl status mysql`; verify TCP 3306 |
| Error 1129 | `Host blocked due to many connection errors` | Too many failed logins from host | `FLUSH HOSTS;` or set `max_connect_errors` higher |

## Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Replication stopped: `Error 1062 Duplicate entry` | MySQL 8.x | Row already exists on replica; replayed out of order | Skip: `SET GLOBAL SQL_SLAVE_SKIP_COUNTER=1; START SLAVE;`; or use GTID-based skip | N/A |
| `Slave SQL thread stopped — Error 1032: Row not found` | MySQL 8.x | Row exists on source but not replica (inconsistency) | Re-sync replica from source dump; or use `pt-table-sync` | N/A |

## InnoDB

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `InnoDB: Tablespace corrupt` on startup | MySQL 8.x | Unclean shutdown; disk error | Start with `innodb_force_recovery=1` (increment up to 6 if needed); export data; rebuild | N/A |
| `Table locked` preventing writes | MySQL 8.x | Long-running transaction holding lock | `SHOW PROCESSLIST;` identify long query; `KILL <id>` | N/A |

## Group Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Group Replication member shows `ERROR` state | MySQL 8.x | Network partition or member lagging behind | Check: `SELECT * FROM performance_schema.replication_group_members`; rejoin member | N/A |

## See also

- [MySQL — Common Issues](common-issues.md)
- [Linux — Known Issues](../../troubleshooting/known-issues/)
