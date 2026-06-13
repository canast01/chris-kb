---
tags:
  - architecture
  - commvault
---
# Commvault — Integrations


<div class="kb-summary">
Commvault integration with VMware vSphere, storage arrays, LDAP, SMTP, and third-party monitoring platforms.

*Applies to: Commvault 11.x*
</div>

```text
┌──────────────────────── Commvault Integrations — Platforms, Arrays, and Cloud ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Integration Scope                                       │   │
│   │     Commvault integrates with hypervisors, databases, storage arrays, and cloud providers     │   │
│   │         IntelliSnap: native array API (REST/SMI-S) for hardware-accelerated snapshots         │   │
│   │          Application iDAs provide quiesce and consistent backup for DBs and messaging         │   │
│   │           Cloud: S3-compatible, Azure Blob, GCS as secondary copy or primary target           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Each integration has a dedicated iDA or connector; licensing is per data source type               │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Hypervisors      │       Databases       │     Storage Arrays    │      Cloud & SaaS     │   │
│   │   VMware vSphere 7/8  │    Oracle DB (RMAN)   │    Dell PowerStore    │    AWS S3 / Glacier   │   │
│   │   Hyper-V 2019/2022   │    SQL Server (VDI)   │     Dell PowerMax     │   Azure Blob / ADLS   │   │
│   │      Nutanix AHV      │  SAP HANA / BR*Tools  │      NetApp ONTAP     │    Google Cloud GCS   │   │
│   │     KVM (libvirt)     │    Exchange / M365    │      Pure Storage     │    Commvault Cloud    │   │
│   │   AWS EC2 / Azure VM  │   PostgreSQL / MySQL  │    HPE Primera/3PAR   │   Salesforce backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    IntelliSnap offloads snapshot to array; backup job copies snapshot to MA with minimal host I/O     │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               IntelliSnap Flow               │  │              Cloud Integration              │   │
│   │      1. CS triggers snap via array API       │  │       Cloud library: object container       │   │
│   │    2. Array creates crash-consistent snap    │  │     MA authenticates with IAM/SAS token     │   │
│   │       3. MA mounts snap for data read        │  │      Multipart upload for large chunks      │   │
│   │       4. Data streamed to disk library       │  │    Lifecycle: move old copies to Glacier    │   │
│   │    5. Snap unmounted; retained per policy    │  │           WORM via S3 Object Lock           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  IntelliSnap: MA needs FC/iSCSI access to array snap LUNs for mount; HBA/iSCSI initiator              │
│  Array API: dedicated management NIC or VLAN for REST/SMI-S calls from CommServe                      │
│  Cloud: outbound HTTPS 443 from MA to cloud endpoints; proxy support available                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IntelliSnap    = Commvault snap management using native storage array APIs                           │
│  SMI-S          = Storage Management Initiative Specification; standard array management API          │
│  VDI            = SQL Server Virtual Device Interface for hot online backup                           │
│  RMAN           = Oracle Recovery Manager; Commvault Oracle iDA wraps RMAN commands                   │
│  BR*Tools       = SAP backup tools; Commvault integrates as backint backend                           │
│  ADLS           = Azure Data Lake Storage Gen2; supported as cloud library target                     │
│  Object Lock    = S3 immutability feature used for WORM compliance copies                             │
│  IAM Role       = AWS identity for MA EC2 instance; used instead of static credentials                │
│  SAS Token      = Azure shared access signature; time-limited credential for Blob access              │
│  Cloud Library  = Commvault logical library pointing to object store bucket/container                 │
│  Backint        = SAP backup API standard; Commvault implements as SAP HANA target                    │
│  RCT            = Hyper-V Resilient Change Tracking; incremental VM backup mechanism                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Commvault integrates with virtualisation, storage, cloud, and identity platforms through a combination of native agents and vendor-certified plugins. VMware integration uses the Virtual Server Agent (VSA) deployed on a proxy with vCenter credentials, leveraging VADP for snapshot-based VM backups. IntelliSnap integrates with certified storage arrays to orchestrate hardware snapshots as backup sources, dramatically reducing backup windows and production impact.

| Integration | Method | Notes |
|---|---|---|
| VMware vSphere | VSA proxy, VADP, vCenter API | CBT for incrementals; vCenter credentials in CommVault |
| Dell PowerMax | IntelliSnap plugin | Hardware snapshot-based backup; SRDF-aware |
| Dell Data Domain | DD Boost MediaAgent plugin | Inline dedup; AIR replication to secondary DD |
| Dell Unity | IntelliSnap plugin | NAS and block snapshot integration |
| Pure FlashArray | IntelliSnap plugin | REST API-driven snapshot orchestration |
| AWS S3 | Cloud library (MediaAgent) | Long-term retention; lifecycle rules for tiering |
| Azure Blob | Cloud library (MediaAgent) | Azure AD service principal auth |
| LDAP / Active Directory | CommServe auth config | AD groups mapped to CommVault user groups |
| SIEM (Splunk, etc.) | Audit log export / syslog | CommServe audit trail forwarded via syslog |

---

## See also

- [Commvault — Design Standards](../design-standards/)
