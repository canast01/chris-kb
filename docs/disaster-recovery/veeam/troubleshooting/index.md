# Veeam — Troubleshooting



<div class="kb-summary">
Veeam — Troubleshooting reference.
</div>

```
┌─────────────────────────────────────── Veeam — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Veeam — Troubleshooting Approach                               │   │
│   │                   1  Identify: which job, component, or resource is failing                   │   │
│   │                  2  Scope: single job vs all jobs; one source vs all sources                  │   │
│   │             3  Collect: logs and run status command; review recent change history             │   │
│   │                 4  Diagnose: match symptoms to known issues; check error codes                │   │
│   │                     5  Fix: apply resolution; verify fix; monitor next run                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │         Application         │  │             Data            │   │
│   │        Network checks       │  │         Log analysis        │  │        Catalog check        │   │
│   │        Storage space        │  │       Job error codes       │  │         Consistency         │   │
│   │        Process health       │  │        Auth failures        │  │       Corruption scan       │   │
│   │    9419 (Veeam REST API)    │  │        Timeout errors       │  │         Restore test        │   │
│   │        Firewall rules       │  │        Version compat       │  │          RPO drift          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
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
```text
┌─────────────────────────────────────── Veeam — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Veeam — Troubleshooting Approach                               │   │
│   │                   1  Identify: which job, component, or resource is failing                   │   │
│   │                  2  Scope: single job vs all jobs; one source vs all sources                  │   │
│   │             3  Collect: logs and run status command; review recent change history             │   │
│   │                 4  Diagnose: match symptoms to known issues; check error codes                │   │
│   │                     5  Fix: apply resolution; verify fix; monitor next run                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │         Application         │  │             Data            │   │
│   │        Network checks       │  │         Log analysis        │  │        Catalog check        │   │
│   │        Storage space        │  │       Job error codes       │  │         Consistency         │   │
│   │        Process health       │  │        Auth failures        │  │       Corruption scan       │   │
│   │    9419 (Veeam REST API)    │  │        Timeout errors       │  │         Restore test        │   │
│   │        Firewall rules       │  │        Version compat       │  │          RPO drift          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
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
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Snapshot failures, proxy timeouts, repository space, and service crashes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and support bundle collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Vendor support portal, case requirements, and support tiers.</span>
</a>

</div>
