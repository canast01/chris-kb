---
tags:
  - security
  - veeam
---
# Veeam — Access Control


<div class="kb-summary">
Access Control reference covering Role-Based Access Control, Audit Log.
</div>

```text
┌─────────────────────────────────────── Veeam — Access Control ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Veeam — RBAC and Access Control                                │   │
│   │ Auth: Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
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

Forward to SIEM using a log forwarder (Filebeat, Splunk UF) on the VBR server. Alert on:
- Failed login attempts
- Job deletion or modification outside maintenance windows
- Encryption key management operations
