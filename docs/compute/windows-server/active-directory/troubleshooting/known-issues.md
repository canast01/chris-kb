---
tags:
  - troubleshooting
  - active-directory
  - windows-server
  - known-issues
---
# Active Directory — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Active Directory bugs, error codes, and workarounds covering replication, DNS, authentication, and FSMO role issues.

*Applies to: Windows Server 2019 / 2022 Active Directory Domain Services*
</div>

```text
┌─────────────────────────────── Compute Windows Server Active Directory ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Windows Server: Compute Windows Server Active Directory platform               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │             Management: Compute Windows Server Active Directory management console            │   │
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
│    Physical: Compute Windows Server Active Directory infrastructure · management network · monitorin  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Windows Server     = Compute Windows Server Active Directory platform overview and core concepts   │
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

- `dcdiag /test:all` runs all DC health checks — address all failures before further troubleshooting.
- `repadmin /showrepl` shows replication status between DCs.
- Kerberos authentication failures almost always trace to clock skew (>5 minutes) or DNS.

## Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Replication error 1722: The RPC server is unavailable` | All | TCP 135 + dynamic RPC range blocked between DCs | Open TCP 135 + 49152-65535 between all DCs; verify `netlogon` service running | N/A |
| `USN rollback detected` — DC isolated from replication | All | VM snapshot restored to old state; USN regressed | Demote and re-promote affected DC; do not restore AD DCs from VM snapshots | N/A |
| Replication `lingering objects` warning | All | DC offline for >TSL period (default 180 days) | Remove lingering objects: `repadmin /removelingeringobjects` | N/A |

## Authentication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Kerberos error: clock skew too great` | All | Client clock differs from DC clock by >5 minutes | Sync NTP on client; configure all hosts to same NTP source as DCs | N/A |
| LDAP `49 — Invalid credentials` | All | Account locked out or wrong password | Check: `Get-ADUser -Identity <name> -Properties LockedOut` | N/A |
| `No logon servers available` for domain users | All | All DCs unreachable (network/firewall) | Verify TCP 88 (Kerberos), 389 (LDAP), 445 (SMB) from client to DC | N/A |

## DNS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `_msdcs` SRV records missing | All | AD-integrated DNS zone not replicating | Force DNS replication: `repadmin /syncall /AdeP`; check `dnscmd /zoneinfo` | N/A |
| DC IP change not reflected in DNS | All | DC DNS A record not updated automatically | Manually update DC's DNS record; verify `netlogon` DNS registration: `nltest /dsregdns` | N/A |

## FSMO Roles

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot change password — PDC emulator unreachable` | All | PDC FSMO role holder offline | Seize PDC role to another DC: `ntdsutil "roles" "connections" "connect to server <dc>" "quit" "seize pdc" "quit" "quit"` | N/A |
| `Schema modification failed` | All | Schema Master FSMO offline | Transfer or seize Schema Master to reachable DC | N/A |

## See also

- [Active Directory — Common Issues](common-issues.md)
- [Windows Server — Known Issues](../../troubleshooting/known-issues/)
- [CyberArk — Known Issues](../../../../security/cyberark/troubleshooting/known-issues/)
