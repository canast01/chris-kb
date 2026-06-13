---
tags:
  - srm
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# SRM — Escalation


<div class="kb-summary">
Escalation reference covering Before Opening a Support Case, Severity Definitions, If SRA Vendor is Involved, Support Portal, Escalation Path and 1 more sections.

*Applies to: SRM 8.x / 9.x*
</div>

```text
┌─────────────────────────────────────── VMware SRM — Escalation ───────────────────────────────────────┐
│                                                                                                       │
│  Escalate SRM issues to VMware GSS when failover fails, site pair cannot reconnect,                   │
│  or replication is permanently broken; attach support bundle and SRA logs.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │             Pre-Escalation Steps            │   │
│   │         Real failover fails mid-run          │  │          Collect SRM support bundle         │   │
│   │           Site pair unrecoverable            │  │          Collect vSR appliance logs         │   │
│   │         Replication broken: all VMs          │  │            Note exact error text            │   │
│   │             Self-help exhausted              │  │             Timeline of changes             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Failed real failover is P1; collect all logs before any further changes.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                GSS Engagement                │  │               Escalation Path               │   │
│   │           Open SR: broadcom portal           │  │             T1: triage + bundle             │   │
│   │           P1: real failover failed           │  │             T2: SRM SE assigned             │   │
│   │           Include SRM version + OS           │  │            T3: engineering review           │   │
│   │           Attach bundle + SRA logs           │  │          Involve storage vendor too         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ABR issues require parallel storage vendor engagement (Dell/NetApp GSS);                             │
│  prepare access to SRM Server via RDP and storage admin credentials.                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM support bundle= generated from SRM UI; includes all SRM logs                                     │
│  vSR logs      = vSphere Replication appliance logs; hbrsrv.log                                       │
│  SRA logs      = storage replication adapter; array-specific errors                                   │
│  P1 SR         = site recovery failure; production impact; urgent                                     │
│  Storage vendor= Dell/NetApp parallel engagement for ABR issues                                       │
│  Timeline      = changes made before failure; critical for GSS                                        │
│  T2 SRM SE     = VMware senior SRM engineer                                                           │
│  SRM version   = check SRM About page in vSphere Client                                               │
│  OS version    = Windows Server version on SRM Server                                                 │
│  RDP access    = GSS may need remote desktop to SRM Server                                            │
│  Do not retry  = failed failover: stop; GSS will guide next steps                                     │
│  Broadcom portal= support.broadcom.com; former my.vmware.com                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Before Opening a Support Case

Collect from both protected and recovery sites:

| Item | How to Collect |
|---|---|
| SRM support bundle (both sites) | Site Recovery → Summary → Download SRM Support Bundle |
| vSphere Replication bundle (both sites) | VRA VAMI → Support → Download Support Bundle |
| SRA logs (both SRM Servers) | Array-vendor specific log path (see Diagnostics page) |
| Recovery Plan execution logs | Site Recovery → Recovery Plans → [plan] → History → export |
| vCenter events for affected VMs | vCenter → Monitor → Events → filter by VM name and DR time |
| SRM version | Settings → About SRM |
| vSphere version | vCenter → About |
| SRA version | Site Recovery → Storage → Adapters |
| Array firmware version | Storage array admin UI / CLI |
| Symptom timeline | When issue started, what action triggered it, what was expected |

---

## Severity Definitions

| Severity | Condition |
|---|---|
| Sev 1 | Active DR failover in progress and SRM is failing — production systems down |
| Sev 2 | DR capability degraded — protection groups in error, replication failing, cannot run recovery |
| Sev 3 | Configuration issue, test recovery failed, one VM not protected |
| Sev 4 | General how-to question, cosmetic issue |

For Sev 1 during an active DR event: open case AND call VMware Support immediately.

---

## If SRA Vendor is Involved

If the failure involves the Storage Replication Adapter or array-side replication:
1. Open a case with VMware for SRM itself
2. **Also open a case with the storage vendor** (Pure, Dell, NetApp) for the SRA
3. Provide SRA logs to both vendors
4. VMware and the storage vendor may need to collaborate — share case numbers cross-vendor

---

## Support Portal

1. **VMware/Broadcom Support Portal:** support.broadcom.com
   - Product: VMware Site Recovery Manager
   - Version: [current version]
   - Attach: SRM support bundles from both sites, SRA logs, symptom description

2. **Call Support directly for Sev 1** — reference case number on call

---

## Escalation Path

| Escalation Level | Trigger |
|---|---|
| Technical Account Manager | Recurring issues, SLA breach |
| Critical Escalation Team | Sev 1 not resolved within 2 hours — request escalation via portal |
| SRM Engineering | Suspected SRM bug — TAM or support can escalate to engineering |
| Storage Vendor Engineering | Suspected SRA bug — escalate via storage vendor support case |

---

## Useful Resources

- SRM Documentation: docs.vmware.com/site-recovery-manager
- SRM Compatibility Matrix: interopmatrix.vmware.com
- SRM KB articles: kb.vmware.com (search "Site Recovery Manager")
- vSphere Replication KB: kb.vmware.com (search "vSphere Replication")
- Pure Storage SRA documentation: support.purestorage.com

---

## See also

- [SRM — Diagnostics](diagnostics/)
- [VMware SRM — Common Issues](common-issues/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
