---
tags:
  - operations
  - srm
  - vmware
---
# SRM — Scripts


<div class="kb-summary">
SRM operational scripts — PowerCLI and REST API automation for replication lag reporting, RPO compliance checking, recovery plan test scheduling, 90-day compliance alerting, placeholder VM verification, and plan history export to CSV for DR governance reporting.

*Applies to: SRM 8.x / 9.x*
</div>

  SRM Automation via PowerCLI + REST API
```text
┌────────────────────────────────── VMware SRM — Operational Scripts ───────────────────────────────────┐
│                                                                                                       │
│  SRM operational scripts use PowerCLI, srm-util, and the REST API to automate                         │
│  DR test scheduling, plan reporting, replication status, and compliance tracking.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Replication Status Scripts          │  │              Compliance Scripts             │   │
│   │           Get-SrmReplicationGroup            │  │            Get plan last-run date           │   │
│   │               Check lag per VM               │  │              Alert if >90 days              │   │
│   │            Report: RPO compliance            │  │            Export plan status CSV           │   │
│   │             srm-util showvms lag             │  │            RTO achieved vs target           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Replication lag and test compliance are the two key SRM health metrics to track.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Plan Management Scripts            │  │             REST API Automation             │   │
│   │             Get-SrmRecoveryPlan              │  │             GET /api/rest/plans             │   │
│   │         Start-SrmRecoveryPlan -Test          │  │         GET /api/rest/plans/{}/runs         │   │
│   │          Get plan history: all runs          │  │         GET /api/rest/vms (prot VMs)        │   │
│   │          Export to HTML/CSV report           │  │         POST /api/rest/plans/{}/test        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerCLI connects from jump host to SRM Server; REST API on port 443;                                │
│  scripts need SRM administrator role to trigger plan tests.                                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Get-SrmReplicationGroup= PowerCLI; list replication groups and status                                │
│  Get-SrmRecoveryPlan  = PowerCLI; list recovery plans                                                 │
│  Start-SrmRecoveryPlan= PowerCLI; trigger test or failover                                            │
│  -Test flag    = run in test mode; no production impact                                               │
│  srm-util showvms= show protected VM list and replication lag                                         │
│  GET /api/rest/plans/{}/runs= list all plan run history                                               │
│  POST /api/rest/plans/{}/test= trigger test via REST                                                  │
│  RPO compliance= lag < RPO target for each protected VM                                               │
│  90-day alert  = compliance: test within 90 days of last run                                          │
│  CSV report    = export plan status for DR governance reporting                                       │
│  RTO vs target = compare achieved vs agreed RTO                                                       │
│  Plan run date = stored in SRM DB; queryable via REST API                                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

