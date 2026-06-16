---
tags:
  - troubleshooting
  - superna-eyeglass
  - netapp
  - known-issues
---
# Superna Eyeglass — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Superna Eyeglass bugs, error codes, and workarounds covering SyncIQ DR orchestration, share replication, and AD integration.

*Applies to: Superna Eyeglass 2.x / 3.x for PowerScale (OneFS)*
</div>

```text
┌────────────────────────────────────────── Superna Eyeglass ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          OneFS DR automation — config sync, SyncIQ policy, and failover orchestration         │   │
│   │                    Protocols: HTTPS (UI/API) · PAPI (OneFS) · SNMP · syslog                   │   │
│   │             Management: Eyeglass web UI · REST API · Alarm Manager · job scheduler            │   │
│   │           Monitor SyncIQ -> detect lag -> trigger failover -> update DNS -> validate          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Monitor           │  │        SyncIQ watcher       │  │     Policy + job health     │   │
│   │         Config sync         │  │       Shares / exports      │  │       Replicated to DR      │   │
│   │           Failover          │  │       DR runbook exec       │  │     Automated or manual     │   │
│   │             DNS             │  │       DNS zone update       │  │   Redirects clients to DR   │   │
│   │            Alarms           │  │        Alarm Manager        │  │     Email / SNMP alerts     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Eyeglass VM    │ DR orchestrator  │     HTTPS 443     │   LDAP / local   │  OVA on vSphere  │   │
│   │   PAPI client    │ OneFS API access │    HTTPS (PAPI)   │   OneFS admin    │Per-cluster creds │   │
│   │   Config repl    │Share/export sync │     PAPI push     │   OneFS admin    │  Near-real-time  │   │
│   │  Failover plan   │    DR runbook    │      Internal     │    Admin user    │ Pre-tested steps │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Eyeglass VM -> source OneFS cluster -> DR OneFS cluster -> DNS servers                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Superna Eyeglass = DR automation platform for NetApp PowerScale (Isilon)                             │
│  SyncIQ       = OneFS native replication engine; Eyeglass monitors its policies                       │
│  Config replication = Eyeglass copies SMB shares, NFS exports, quotas to DR                           │
│  Failover     = Eyeglass orchestrates cutover: unmounts source, mounts DR, updates DNS                │
│  Alarm Manager = Eyeglass alerting subsystem; routes issues to email/SNMP/ITSM                        │
│  PAPI         = Platform API; OneFS REST interface Eyeglass uses for all queries                      │
│  Runbook      = Eyeglass-defined sequence of DR steps executed on failover                            │
│  Lag          = SyncIQ replication lag; Eyeglass alerts when this exceeds threshold                   │
│  Policy       = SyncIQ replication job definition; includes schedule and target path                  │
│  Config drift = source/DR config divergence; Eyeglass auto-corrects periodically                      │
│  DFS          = Distributed File System; optional Eyeglass DFS namespace failover                     │
│  Test failover = Eyeglass DR test without cutting over production traffic                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Eyeglass errors appear in the web UI under `Administration → Activity → Jobs`.
- Logs: `/var/log/superna/` on the Eyeglass appliance.
- Most issues are API connectivity to PowerScale (port 8080) or AD (LDAP 636).

## DR Orchestration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Failover job fails: `SyncIQ policy not in compliance` | Eyeglass 3.x | SyncIQ lag exceeds RPO before failover triggered | Allow SyncIQ to complete sync; retry failover; or override RPO check for emergency failover | N/A |
| `Cannot connect to cluster` during failover | Eyeglass 3.x | DR cluster API (port 8080) unreachable at time of failover | Verify TCP 8080 from Eyeglass to DR cluster SmartConnect | N/A |
| Share replication incomplete: `AD object not found` | Eyeglass 3.x | AD user or group referenced in share ACL does not exist on DR AD domain | Ensure AD is synced / extended to DR site before failover | N/A |

## Share and Quota Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Quota replication not running on schedule | Eyeglass 3.x | Eyeglass scheduler service stopped after appliance update | Restart Eyeglass services: `service eyeglass restart` | N/A |
| Share ACL replication fails: `LDAP authentication failed` | Eyeglass 3.x | AD LDAPS (636) certificate expired or changed | Update LDAP certificate in Eyeglass → Configuration → LDAP | N/A |

## See also

- [Superna Eyeglass — Common Issues](common-issues.md)
- [Dell PowerScale — Known Issues](../../../dell/powerscale/troubleshooting/known-issues/)
- [NetApp ONTAP — Known Issues](../../ontap/troubleshooting/known-issues/)
