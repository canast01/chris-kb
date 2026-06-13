---
tags:
  - troubleshooting
  - veeam
---
# Veeam — Escalation


<div class="kb-summary">
Veeam case creation, log export, and Veeam support escalation procedures for unresolved backup and restore failures.

*Applies to: Veeam 12.x*
</div>

```text
┌───────────────────────────────────────── Veeam — Escalation ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    Veeam — Escalation Path                                    │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │                Product version: Veeam version string from About / version command             │   │
│   │                           Full log bundle: Start-VBRInstantVMRecovery                         │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Backup Server = central Veeam component: scheduler, job engine, catalog, REST API                    │
│  Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H       │
│  CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors          │
│  VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup                 │
│  SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage        │
│  Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds                   │
│  SureBackup    = automated backup verification; test-restores VM in isolated virtual lab              │
│  Replication   = creates VM replica at DR site; enables failover without full restore time            │
│  GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points      │
│  Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec       │
│  Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery           │
│  VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required                    │
│  Health Check  = periodic backup integrity scan; verifies restore points are readable                 │
│  Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Veeam support is accessed via the Veeam Customer Support Portal at my.veeam.com. Cases are raised by selecting the product (Veeam Backup & Replication), specifying the version, and classifying severity. ProSupport tiers provide enhanced SLAs and a designated technical account manager for enterprise customers. Before opening a case, export the Veeam log bundle from the console to provide the full diagnostic context immediately.

**Collecting log export**

1. In the VBR console: Main Menu > Help > Support Information
2. Click "Export Logs" — select the job or time range relevant to the issue
3. The wizard packages logs from the Backup Server and relevant proxies into a single ZIP archive

**Required information for a support case**

- VBR version (Help > About)
- Infrastructure type (VMware / Hyper-V / Agent)
- Job name and session ID of the failing job
- Error message from the job statistics view (copy the full text)
- Log export ZIP from the console

**Support tiers**

| Tier | Sev 1 SLA | Availability | Notes |
|---|---|---|---|
| Production | 2 hours | 24x7 | Standard enterprise |
| ProSupport | 1 hour | 24x7 | Designated engineer |
| ProSupport Plus | 30 minutes | 24x7 | TAM + proactive monitoring |

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

