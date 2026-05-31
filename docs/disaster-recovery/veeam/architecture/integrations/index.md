# Veeam — Integrations

```text
┌────────────────────────────────── Veeam — Architecture Integrations ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Veeam — External Integration Points                              │   │
│   │ Auth: Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials │   │
│   │               Storage: connected via 9419 (Veeam REST API) · 6160 (Veeam Agent)               │   │
│   │            Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems            │   │
│   │     Encryption: AES-256 backup (key in Veeam config DB); TLS on all management; WORM repos    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Identity          │  │           Storage           │  │          Monitoring         │   │
│   │          AD / LDAP          │  │    9419 (Veeam REST API)    │  │        SNMP / syslog        │   │
│   │           SAML SSO          │  │      6160 (Veeam Agent)     │  │         REST webhook        │   │
│   │          RBAC roles         │  │       NFS / iSCSI / FC      │  │         Email alerts        │   │
│   │         MFA optional        │  │       Dedup appliance       │  │          ServiceNow         │   │
│   │          Cert auth          │  │        Object storage       │  │          Prometheus         │   │
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
Veeam integrates with virtualisation, storage, cloud, and monitoring platforms through native plugins and APIs. VMware vSphere is the primary integration: Veeam connects to vCenter (or individual ESXi hosts for standalone), uses VADP for snapshot-based backups, and leverages Changed Block Tracking (CBT) for incremental efficiency. Storage integrations use vendor-specific plugins for hardware snapshot-based backups, reducing backup windows and eliminating I/O impact on production.

| Integration | Method | Notes |
|---|---|---|
| VMware vSphere | VADP, vCenter API | vCenter credentials; CBT for incrementals |
| Microsoft Hyper-V | Hyper-V VSS / RCT | Direct Hyper-V integration |
| Pure FlashArray | Veeam Plugin for Pure | NFS/iSCSI repository or snapshot integration |
| Dell PowerMax | Veeam Plugin for Dell EMC | Hardware snapshot-based backup |
| AWS S3 | Cloud repository / capacity tier | Object Lock for immutable backups |
| Azure Blob | Cloud repository / capacity tier | Azure AD service principal auth |
| GCP Cloud Storage | Cloud repository | Service account key auth |
| Active Directory | Windows auth for VBR console | AD groups mapped to Veeam roles |
| Veeam ONE | VBR API | Monitoring, alerting, and reporting |
| ServiceNow | Custom PowerShell integration | Incident creation on job failure |
