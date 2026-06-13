---
tags:
  - netbackup
  - troubleshooting
---
# NetBackup — Diagnostics

```bash
# VxUL logs are stored under:
/usr/openv/logs/

# Query with vxlogview for a specific OID and time window
vxlogview -o 117 -d 24h -t "DEBUG|WARNING|ERROR" | less

# Common OIDs:
# 117 — nbpem (policy execution manager)
# 118 — nbjm (job manager)
# 119 — nbstserv (storage service)
# 143 — nbwebsvc (NetBackup web service)
```
```text
┌─────────────────────────────────────── NetBackup — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                NetBackup — Diagnostic Commands                                │   │
│   │                       Collect these before opening a vendor support case                      │   │
│   │                                         nbpemreq / bpps                                       │   │
│   │                                       tpconfig / nbstlutil                                    │   │
│   │                       Check system logs: /var/log/ or Windows Event Viewer                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │               Live Diagnostics              │   │
│   │            Application log bundle            │  │             Network connectivity            │   │
│   │            OS syslog (journalctl)            │  │              Storage path check             │   │
│   │             Core dump if crashed             │  │              Process list check             │   │
│   │             Config export/backup             │  │              Port reachability              │   │
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
```bash
# List all storage units and capacity
bpstulist -U

# Check disk pool utilization (AdvancedDisk / MSDP)
nbdevquery -listdp -stype PureDisk -U

# List media by volume pool
vmquery -b -pn <pool-name>

# Check tape drive status in robot
tpconfig -d

# Inventory robot and reconcile with EMM
vmupdate -rt TLD -rn 0 -rh <robot-host> -rt TLD -rn 0

# MSDP pool health
cacontrol --dsstat -d /msdp/data/dp1

# Check MSDP fingerprint database
cacontrol --dbstat
```
```bash
# List all policies with full detail
bppllist -allpolicies -L

# Check backup windows and schedule for a policy
bpplschedrep <policyname>

# List catalog images for a client
bplist -C <client-hostname> -t 0 -l

# Check catalog database consistency
bpdbm -consistency -verbose

# Show catalog disk usage
du -sh /usr/openv/netbackup/db/

# Expire a specific backup image (frees catalog and media)
bpexpdate -backupid <backup-id> -d 0
```
```bash
# List all registered hosts in EMM
nbemmcmd -listhosts

# Check media server status
nbemmcmd -listhosts -machinetype mediaserver

# Re-register a media server (if it appears missing)
nbemmcmd -updatehost -machinename <media-server> -machinetype mediaserver

# Check network routes between master and media server
traceroute <media-server>
ping -c 10 <media-server>
```
```bash
# Create log directories for key daemons
mkdir -p /usr/openv/netbackup/logs/bpcd
mkdir -p /usr/openv/netbackup/logs/bpbrm
mkdir -p /usr/openv/netbackup/logs/bprd
mkdir -p /usr/openv/netbackup/logs/bptm
mkdir -p /usr/openv/netbackup/logs/bpdbm

# Set global verbose level (0=default, 5=maximum — use briefly)
bpsetconfig -h <master> <<EOF
VERBOSE = 3
EOF

# Revert to default after troubleshooting
bpsetconfig -h <master> <<EOF
VERBOSE = 0
EOF
```
```bash
# Generate nbsupport bundle (run on master server)
/usr/openv/netbackup/bin/support/nbsupport

# Output is written to:
# /tmp/nbsupport_<hostname>_<timestamp>.tar.gz

# Include job IDs and time window when submitting to Veritas
bpdbjobs -jobid <id> -report > /tmp/job_<id>_report.txt
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
