---
tags:
  - troubleshooting
  - cyberark
  - pam
  - known-issues
---
# CyberArk — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known CyberArk PAM bugs, error codes, and workarounds covering Vault, PVWA, CPM, and PSM components.

*Applies to: CyberArk PAS / Privilege Cloud 13.x+*
</div>

```text
┌──────────────────────────────────────────── CyberArk PAM ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Privileged Access Management — vault, password rotation, session recording          │   │
│   │              Protocols: HTTPS (PVWA) · CyberArk vault protocol (1858) · RDP · SSH             │   │
│   │               Management: PVWA web UI · REST API · PACLI CLI · PrivateArk client              │   │
│   │          User auth -> PVWA -> vault credential lookup -> CPM rotation -> PSM session          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Storage           │  │        Digital Vault        │  │  Encrypted credential store │   │
│   │            Access           │  │             PVWA            │  │      Web UI + REST API      │   │
│   │           Rotation          │  │             CPM             │  │     Auto password change    │   │
│   │           Session           │  │             PSM             │  │      Proxy + recording      │   │
│   │             Sync            │  │      Distributed Vault      │  │     DR / HA replication     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Digital Vault   │ Credential store │      TCP 1858     │ Vault user cert  │AES-256 encrypted │   │
│   │       PVWA       │ User web access  │     HTTPS 443     │   LDAP / SAML    │Session recording │   │
│   │       CPM        │Password rotation │  Target protocol  │  Vault svc acct  │Dual control aware│   │
│   │       PSM        │  Session proxy   │     RDP / SSH     │  Vault account   │Records + isolates│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: PVWA/CPM/PSM servers -> Digital Vault -> managed target systems (AD, Linux, DB)            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Digital Vault = CyberArk encrypted credential repository; core PAM component                         │
│  PVWA         = Password Vault Web Access; web UI and REST API gateway                                │
│  CPM          = Central Policy Manager; automates password rotation on targets                        │
│  PSM          = Privileged Session Manager; proxy for RDP/SSH with recording                          │
│  Safe         = CyberArk logical container grouping accounts with access policy                       │
│  Platform     = policy template defining rotation frequency and auth method                           │
│  Dual control = requires two approvers before releasing a credential                                  │
│  OPM          = On-Demand Privileges Manager; sudo elevation management                               │
│  EPM          = Endpoint Privilege Manager; workstation least-privilege agent                         │
│  Conjur       = CyberArk secrets management for DevOps/CI pipelines                                   │
│  DR Vault     = hot-standby vault replica; failover target on production vault loss                   │
│  PACLI        = Privileged Access CLI; scriptable interface to vault API                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- CyberArk errors appear in the PVWA → Monitoring → Session Management, or in Vault audit logs.
- Vault logs: `C:\Program Files (x86)\PrivateArk\Server\Logs\italog.log`.
- PSM logs: `C:\Program Files (x86)\CyberArk\PSM\Logs\PSMConsole.log`.

## Vault Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| PVWA `Cannot connect to Vault` | CyberArk 13.x | TCP 1858 blocked between PVWA and Vault | Verify TCP 1858 from all PVWA servers to Vault; test: `telnet <vault-ip> 1858` | N/A |
| CPM `Account reconciliation failed — cannot connect to target` | CyberArk 13.x | CPM cannot reach target system (SSH 22 / RDP 3389) | Verify CPM has network access to target; check CPM firewall rules | N/A |
| DR Vault not promoting after primary failure | CyberArk 13.x | DR Vault replication port 1858 blocked from primary site | Verify TCP 1858 between primary Vault and DR Vault subnets | N/A |

## Password Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Account locked out` after CPM rotation | CyberArk 13.x | CPM rotated password but target system not updated; old password cached | Check CPM platform settings for reconcile account; use `Immediate Change` with reconcile | N/A |
| `CPM cannot change password — AD account` | CyberArk 13.x | CPM domain account lacks password change permission in AD | Grant CPM service account `Reset Password` right on target OU | N/A |
| Password rotation failing for Windows local account | CyberArk 13.x | Windows UAC or local security policy blocking remote password change | Configure CPM platform to use `Pass This Object` or reconcile via domain admin | N/A |

## PSM (Privileged Session Manager)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| PSM RDP session disconnecting after 10 minutes | CyberArk 13.x | Windows RDP idle session timeout on PSM server | Increase `Idle Session Limit` via Group Policy on PSM Windows host | N/A |
| `Cannot initiate connection` for PSM SSH target | CyberArk 13.x | Target SSH host key changed since last PSM connection | Remove cached host key from PSM known_hosts; allow PSM to accept new key | N/A |

## See also

- [CyberArk — Common Issues](common-issues/)
