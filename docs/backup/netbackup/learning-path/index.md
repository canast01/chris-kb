# Veritas NetBackup — Learning Path

<div class="kb-summary">
Recommended reading order for Veritas NetBackup. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture

**Goal**: Understand the NetBackup domain model — master server, media servers, clients, policies, volumes, and the data path from client to storage unit.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — NetBackup domain architecture: primary server (formerly master server) as control plane and catalog host, media servers as data movers, clients as backup sources; storage units pointing to disk or tape libraries; backup policies defining schedule, client list, and backup selections; MSDP dedup pool for inline deduplication
- [Design Standards](../architecture/design-standards/) — Media server sizing (streams, LAN bandwidth, SAN attachment), storage unit group design for load balancing, MSDP pool sizing (capacity and performance), volume pool organisation, Auto Image Replication (AIR) topology for DR site replication, policy type selection (Standard, MS-Windows, VMware, Oracle, NDMP)
- [Integrations](../architecture/integrations/) — VMware vCenter integration for snapshot-based VM backup, Oracle RMAN via NetBackup for Oracle agent, SAP HANA and MSSQL agents, OpenStorage (OST) for third-party dedup appliances (ExaGrid, DataDomain), NetApp NDMP for NAS backup, Veritas Alta for cloud-managed primary server

**Why first**: NetBackup's policy-volume-storage unit model has more moving parts than most backup products — understanding the terminology and data path before deployment prevents the most common configuration errors (wrong storage unit, policy not matching client, volume pool conflict).

---

## Stage 2 — Deployment

**Goal**: Install the primary server, configure media servers and storage units, create volume pools, and run the first policy backup.

**Read**:

- [Deploy](../deploy/) — Primary server installation, media server deployment and registration, disk storage unit creation (BasicDisk, AdvancedDisk, MSDP), volume pool and tape library configuration, VMware or NDMP policy creation and test run
- [Install & Upgrade](../operations/install-upgrade/) — NetBackup upgrade sequence (primary server first, then media servers, then clients), EEB (emergency engineering binary) application, catalog backup before upgrade, version compatibility matrix

---

## Stage 3 — Operations

**Goal**: Manage backup policies, monitor job activity, run catalog backups, manage AIR replication, and execute restores.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check Activity Monitor for failed and queued jobs, verify catalog backup completed, review MSDP pool usage, check AIR replication queue lag
- [CLI Reference](../operations/cli-reference/) — Essential NetBackup CLI: `bpbackup`, `bprestore`, `bplist`, `bpdbjobs`, `nbpemreq`, `bpmedialist`, `nbstl` (storage lifecycle policy), `nbdevquery`; REST API for job monitoring
- [Procedures](../operations/procedures/) — Policy create/modify/delete, manual backup initiation, catalog backup and recovery, image expiration and cleanup, MSDP garbage collection, AIR import at DR site, volume freeze and unfreeze
- [Backup & Restore](../operations/backup-restore/) — File-level restore (GUI and CLI), full VM restore from VMware snapshot policy, Oracle database restore via RMAN, bare-metal recovery (BMR), AIR-replicated image restore at DR site
- [Scripts](../operations/scripts/) — Automated job failure alerting, MSDP usage trending, policy compliance reports, AIR replication lag monitoring

---

## Stage 4 — Security

**Goal**: Secure the NetBackup domain, enforce certificate-based host authentication, and protect the catalog.

**Read**:

- [Access Control](../security/access-control/) — NetBackup RBAC (introduced in 9.x): Security Administrator, Backup Administrator, Restore Operator, Operator; host access control list (bp.conf allowlist); audit log for policy and restore changes
- [Authentication](../security/authentication/) — NetBackup certificate-based host identity (NBU CA), external CA integration, web UI and API authentication via JWT, LDAP/AD for web console login, MFA for administrative access
- [Encryption](../security/encryption/) — Client-side encryption for data in flight, MSDP encryption at rest, storage unit key-based encryption for tape, catalog encryption, KMS (Key Management Service) integration
- [Hardening](../security/hardening/): — NetBackup Security and Encryption Guide controls: restrict `bpcd` access, enforce certificate revocation checks, isolate primary server network, enable Malware Scanning on MSDP

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose failed backup jobs, media server connectivity issues, dedup errors, and restore failures.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Job failing with status code 196 (client connect error), status 83 (media mount error), MSDP space reclamation stuck, AIR replication not completing, catalog recovery after primary server loss
- [Diagnostics](../troubleshooting/diagnostics/) — `bpdbjobs -report`, Activity Monitor detail log, `nbemmcmd` for EMM database, unified logging (`vxlogview`), media server connectivity test (`bptestnetconn`), MSDP health check (`msdpcld`)
- [Escalation](../troubleshooting/escalation/) — Veritas support case process, `nbsu` (NetBackup Support Utility) data collection, OS-level log collection from primary and media servers, catalog consistency check before escalation

**Why last**: NetBackup error status codes only make sense in the context of the policy-volume-storage unit data path — understanding that flow in earlier stages makes troubleshooting systematic rather than random.
