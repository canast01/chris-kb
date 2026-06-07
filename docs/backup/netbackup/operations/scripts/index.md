# NetBackup — Scripts


<div class="kb-summary">
NetBackup Scripts reference.
</div>

```text
┌───────────────────────────────────────── NetBackup — Scripts ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 NetBackup — Automation Scripts                                │   │
│   │             Scripts automate routine NetBackup operations — run via cron or CI/CD             │   │
│   │               Always store credentials in vault (not in script); log all output               │   │
│   │                 Test scripts in non-production before scheduling in production                │   │
│   │                        Scope scripts to least-privilege service account                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Status / Reporting Scripts          │  │              Automation Scripts             │   │
│   │           Job success rate report            │  │            Auto-expire old points           │   │
│   │              Capacity trending               │  │          Auto-add new VMs to policy         │   │
│   │            SLA compliance report             │  │          Nightly DR test validation         │   │
│   │             RPO / RTO dashboard              │  │             Alert on job failure            │   │
│   │               nbpemreq / bpps                │  │             tpconfig / nbstlutil            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection             │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Server = central controller: scheduler, catalog, job manager, policy engine                   │
│  Media Server  = data mover between client and storage; can be co-located with master                 │
│  MSDP          = Media Server Deduplication Pool; inline variable-length block dedup                  │
│  Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot                    │
│  Policy        = defines what, when, and where to back up; contains schedules and clients             │
│  Schedule      = full / differential-incremental / cumulative-incremental timing within policy        │
│  Retention     = how long an image is kept; set per schedule, enforced by catalog expiry              │
│  Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config             │
│  NBU CA        = auto-issued certificate authority; signs host IDs for secure comms                   │
│  vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556           │
│  bpdbjobs      = CLI to query job history: status, duration, exit code, errors                        │
│  bplist        = CLI to list available backup images for a client, policy, or date range              │
│  KMS           = Key Management Service for encryption keys used in backup data encryption            │
│  NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Automation scripts for NetBackup use the `admincmd` CLI tools and are typically scheduled via cron on the Master Server. All scripts should write output to a dated log under `/opt/netbackup/scripts/logs/` and send alerts via email or a syslog forwarder when thresholds are breached. Scripts should be owned by `root` and executable only by the backup service account.

| Script | Language | Purpose |
|---|---|---|
| `nb_daily_job_summary.sh` | Bash | Runs `bpdbjobs -report` and emails a formatted summary of pass/fail counts |
| `nb_failed_job_alert.sh` | Bash | Queries failed jobs and posts to a ticketing system or email alias |
| `nb_stu_capacity.sh` | Bash | Iterates `bpstulist` output and alerts when any STU exceeds 80% capacity |
| `nb_client_connectivity.sh` | Bash | Runs `bptestbpcd` against a client list and reports unreachable clients |
| `nb_catalog_verify.sh` | Bash | Confirms the catalog backup job completed in the last 24 hours; pages on-call if absent |

**Script conventions**

- Use `set -euo pipefail` at the top of every script.
- Log rotation: keep 30 days of logs; use `logrotate` or a cron-based cleanup.
- Credentials: service account API keys or passwords must be stored in the vault (CyberArk) and retrieved at runtime — never hard-coded.
