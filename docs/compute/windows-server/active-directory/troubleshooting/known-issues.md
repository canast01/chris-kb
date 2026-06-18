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
┌────────────────────────────────────────── Active Directory ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Windows directory service — domain controllers, replication, Kerberos auth          │   │
│   │                Protocols: Kerberos (88) · LDAP (389/636) · SMB (445) · DNS (53)               │   │
│   │                       Management: ADUC / PowerShell (Get-AD*) / dsa.msc                       │   │
│   │                Client auth -> DC (Kerberos) -> Ticket issued -> Resource access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Identity          │  │      Domain Controller      │  │      Holds NTDS.dit DB      │   │
│   │         Replication         │  │         Multi-master        │  │     USN-based, KCC topo     │   │
│   │             Auth            │  │           Kerberos          │  │    5-min clock skew tol.    │   │
│   │             DNS             │  │     AD-integrated zones     │  │    SRV recs for DC disc.    │   │
│   │             FSMO            │  │       5 special roles       │  │      Single-master ops      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │        DC        │ Directory + auth │   Kerb/LDAP/SMB   │       N/A        │NTDS.dit database │   │
│   │     repadmin     │ Replication tool │        N/A        │   Domain admin   │showrepl, syncall │   │
│   │      dcdiag      │ DC health check  │        N/A        │   Domain admin   │ test:all common  │   │
│   │    FSMO roles    │Single-master ops │        N/A        │ Enterprise admin │  PDC, RID, etc.  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: domain controller server(s) - replicated across sites via WAN                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NTDS.dit       = the Active Directory database file on each DC                                       │
│  FSMO           = Flexible Single Master Operations; 5 roles, one DC each                             │
│  PDC Emulator   = FSMO role handling password changes and time sync                                   │
│  KCC            = Knowledge Consistency Checker; auto-builds repl. topology                           │
│  USN            = Update Sequence Number; tracks object changes for repl.                             │
│  Lingering obj. = stale object from a DC offline beyond tombstone life                                │
│  Kerberos skew  = >5 min client/DC time diff breaks authentication                                    │
│  SRV record     = DNS record type letting clients locate DCs/services                                 │
│  RODC           = Read-Only Domain Controller; no writable DB copy                                    │
│  Tombstone life = how long deleted objects are retained (default 180d)                                │
│  ntdsutil       = low-level AD database maintenance and FSMO seize tool                               │
│  nltest         = CLI tool for trust and DC connectivity diagnostics                                  │
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

- [Active Directory — Common Issues](common-issues/)
- [Windows Server — Known Issues](../../troubleshooting/known-issues.md)
- [CyberArk — Known Issues](../../../../security/cyberark/troubleshooting/known-issues.md)
