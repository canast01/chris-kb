# Commvault — Escalation


<div class="kb-summary">
Commvault — Escalation reference.
</div>

```
┌────────────────────────── Commvault Escalation — Support and Case Handling ───────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Tier 1 — L1 Ops           │  │       Internal Tier 2 — L2 Backup Eng       │   │
│   │       Check Job Activity for failures        │  │         Deep log analysis (CV_DIAG)         │   │
│   │         Restart CV services (GxCVD)          │  │         DDB repair and library fixes        │   │
│   │        Check disk library free space         │  │         CommServe DB troubleshooting        │   │
│   │            Run CV_DIAG collection            │  │       Config change and policy review       │   │
│   │        Escalate if not resolved in 2h        │  │        Escalate to Commvault Support        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Escalation path: L1 Ops → L2 Backup Engineering → Commvault Vendor Support                         │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Commvault Vendor Support (Tier 3)                               │   │
│   │              Portal: ma.commvault.com → Create Case; login with entitled account              │   │
│   │          Severity 1 (production down): 24x7 response SLA 1h; call hotline immediately         │   │
│   │             Severity 2 (degraded): business hours response SLA 4h; email + portal             │   │
│   │           Required info: CS version, SP level, CV_DIAG bundle, error codes, job IDs           │   │
│   │           Remote assist: Commvault engineer joins via WebEx/remote session if needed          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Commvault Support may request firewall exception for remote session (WebEx/Teams)                    │
│  Ensure CV_DIAG bundle uploadable to Commvault FTP or case attachment (< 2 GB)                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ma.commvault.com = Commvault support portal for case management and KB articles                      │
│  Severity 1     = Complete production outage; CommServe down or all backups failing                   │
│  Severity 2     = Significant impact; some backups failing or restore degraded                        │
│  CV_DIAG Bundle = Compressed log and config archive required for all support cases                    │
│  SP Level       = Service Pack version installed; check Help → About in CommCell Console              │
│  Entitled Acct  = Commvault support portal account tied to licensed CommCell ID                       │
│  Remote Session = Commvault engineer connects to CommServe for live troubleshooting                   │
│  CommCell ID    = Unique identifier for the CommCell installation; required for support               │
│  Case Number    = Reference ID from Commvault portal; track via ma.commvault.com                      │
│  L2 Backup Eng  = Internal SME for CommVault; owns platform config and deep diagnosis                 │
│  Hotline        = Commvault 24x7 phone support for Sev1; number on support portal                     │
│  Entitlement    = Active support contract tied to CommCell serial number                              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────── Commvault Escalation — Support and Case Handling ───────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Tier 1 — L1 Ops           │  │       Internal Tier 2 — L2 Backup Eng       │   │
│   │       Check Job Activity for failures        │  │         Deep log analysis (CV_DIAG)         │   │
│   │         Restart CV services (GxCVD)          │  │         DDB repair and library fixes        │   │
│   │        Check disk library free space         │  │         CommServe DB troubleshooting        │   │
│   │            Run CV_DIAG collection            │  │       Config change and policy review       │   │
│   │        Escalate if not resolved in 2h        │  │        Escalate to Commvault Support        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Escalation path: L1 Ops → L2 Backup Engineering → Commvault Vendor Support                         │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Commvault Vendor Support (Tier 3)                               │   │
│   │              Portal: ma.commvault.com → Create Case; login with entitled account              │   │
│   │          Severity 1 (production down): 24x7 response SLA 1h; call hotline immediately         │   │
│   │             Severity 2 (degraded): business hours response SLA 4h; email + portal             │   │
│   │           Required info: CS version, SP level, CV_DIAG bundle, error codes, job IDs           │   │
│   │           Remote assist: Commvault engineer joins via WebEx/remote session if needed          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Commvault Support may request firewall exception for remote session (WebEx/Teams)                    │
│  Ensure CV_DIAG bundle uploadable to Commvault FTP or case attachment (< 2 GB)                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ma.commvault.com = Commvault support portal for case management and KB articles                      │
│  Severity 1     = Complete production outage; CommServe down or all backups failing                   │
│  Severity 2     = Significant impact; some backups failing or restore degraded                        │
│  CV_DIAG Bundle = Compressed log and config archive required for all support cases                    │
│  SP Level       = Service Pack version installed; check Help → About in CommCell Console              │
│  Entitled Acct  = Commvault support portal account tied to licensed CommCell ID                       │
│  Remote Session = Commvault engineer connects to CommServe for live troubleshooting                   │
│  CommCell ID    = Unique identifier for the CommCell installation; required for support               │
│  Case Number    = Reference ID from Commvault portal; track via ma.commvault.com                      │
│  L2 Backup Eng  = Internal SME for CommVault; owns platform config and deep diagnosis                 │
│  Hotline        = Commvault 24x7 phone support for Sev1; number on support portal                     │
│  Entitlement    = Active support contract tied to CommCell serial number                              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
