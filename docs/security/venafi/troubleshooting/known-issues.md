---
tags:
  - troubleshooting
  - venafi
  - certificates
  - known-issues
---
# Venafi Trust Protection Platform — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Venafi TPP bugs, error codes, and workarounds covering certificate discovery, ADCS integration, and policy engine issues.

*Applies to: Venafi TPP 22.x / 23.x*
</div>

```text
┌─────────────────────────────────── Security Venafi Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Venafi: Security Venafi Troubleshooting platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                 Management: Security Venafi Troubleshooting management console                │   │
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
│    Physical: Security Venafi Troubleshooting infrastructure · management network · monitoring         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Troubleshooting platform overview and core concepts           │
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

- Venafi errors appear in TPP UI → Monitor → Log.
- Venafi support logs: collected via `VenafiLog.ps1` or TPP Diagnostic → Log Collection.
- DCOM issues (port 135 + dynamic) are the most common ADCS CA integration problem.

## Certificate Issuance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Certificate request fails: `CA unavailable` | TPP 22.x | TPP cannot reach ADCS CA on port 135 | Verify TCP 135 + dynamic RPC (49152-65535) from TPP to CA server | N/A |
| `Policy violation — key length too short` | TPP 22.x | Certificate template requesting 1024-bit RSA vs policy minimum | Update certificate request to use 2048/4096 RSA or P-256 ECC | N/A |
| `Certificate already exists in CA` | TPP 22.x | Duplicate CN in CA; TPP trying to re-issue without revoke | Revoke existing certificate in CA before re-issuing; or use `Force Reissue` option | N/A |

## Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Network discovery not finding certificates on hosts | TPP 22.x | Discovery engine cannot connect to target on 443 | Ensure discovery engine has network access to target hosts on 443 | N/A |
| `SSH key scan failed` for Linux hosts | TPP 22.x | TPP discovery account lacks SSH access | Verify TPP discovery account has SSH key configured; test SSH from TPP server | N/A |

## Satellite and Agents

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Venafi Satellite `Offline` in TPP | TPP 22.x | TCP 443 from Satellite to TPP Management UI blocked | Verify TCP 443 from Satellite host to TPP server | N/A |
| `Venafi agent not responding` on Windows host | TPP 22.x | VenafiAgent Windows service stopped | Restart: `Get-Service VenafiAgent | Start-Service` | N/A |

## See also

- [Venafi TPP — Common Issues](common-issues.md)
- [Certificates — Known Issues](../../certificates/troubleshooting/known-issues/)
- [Active Directory — Known Issues](../../../compute/windows-server/active-directory/troubleshooting/known-issues/)
