---
tags:
  - netbackup
  - troubleshooting
search:
  boost: 1.5
---
# NetBackup — Diagnostics

<div class="kb-summary">
NetBackup diagnostic commands: query failed jobs with bpdbjobs, check storage unit capacity with bpstulist and nbdevquery, verify policy and client config, increase verbose logging with bpsetconfig, check catalog consistency, and generate the nbsupport bundle for Veritas cases.

*Applies to: NetBackup 10.x on Linux master/media servers*
</div>

```text
┌─────────────────────────────────────── NetBackup — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Start here: bpdbjobs (failed jobs) → bpstulist (storage) → bppllist (policy) → VxUL logs  │     │
│   │   Exit code 196: connectivity; exit code 58: media server; exit code 13: client              │    │
│   │   VxUL logs in /usr/openv/logs/ — query with vxlogview -o <OID> -d 24h                      │     │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │               Live Diagnostics              │   │
│   │   vxlogview -o 117 -d 24h (nbpem)           │  │   bpdbjobs -jobid <id> -report              │    │
│   │   vxlogview -o 118 -d 24h (nbjm)            │  │   nbemmcmd -listhosts -machinetype media    │    │
│   │   /usr/openv/netbackup/logs/ (legacy)        │  │   tpconfig -d (tape drives)                 │   │
│   │   nbsupport bundle for Veritas case          │  │   bpstulist -U (storage units)              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Master server (catalog + scheduler) · media server(s) (data movers) · storage units (MSDP / tape)    │
│                                                                                                       │
│  Key terms:                                                                                           │
│  vnetd       = network daemon on port 1556; multiplexes all client-master-media communications        │
│  bpdbjobs    = CLI to query job history: status, duration, exit code, and detailed error text         │
│  nbpem       = policy execution manager (OID 117); generates and dispatches jobs                      │
│  nbjm        = job manager (OID 118); sends jobs to media server, tracks job state                    │
│  MSDP        = Media Server Deduplication Pool; inline variable-length block deduplication            │
│  bplist      = lists available backup images for a client, policy, or date range                      │
│  vxlogview   = VxUL (Unified Logging) viewer; query logs by OID, date range, severity                 │
│  nbsupport   = generates a compressed diagnostic bundle with all logs and configuration               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    A([NetBackup Issue]) --> B{What type of problem?}
    B -->|Backup job failed| C[bpdbjobs -jobid id -report\nRead exit code and error text]
    B -->|No media available| D[bpstulist -U\nnbdevquery -listdp -stype PureDisk]
    B -->|Client not backing up| E[Check policy client list\nbppllist policyname -L]
    B -->|Catalog error| F[bpdbm -consistency -verbose\nCheck PostgreSQL on master]
    B -->|Restore fails| G[bplist -C client -t 0 -l\nVerify image exists and not expired]
    C --> H{Exit code?}
    H -->|196 — network| I[ping media-server\nnetstat -an | grep 1556]
    H -->|58 — media server| J[Check media server status\nnbemmcmd -listhosts -machinetype media]
    H -->|13 — client| K[Check bpcd on client\nTest client-server connectivity]
    H -->|Other| L[vxlogview -o 118 -d 24h\nCheck nbjm log for detail]
    D --> M[Check MSDP health\ncacontrol --dsstat]
    E --> N[bpplschedrep policyname\nVerify schedule and backup window]
    F --> O[Check master disk and PostgreSQL\ndu -sh /usr/openv/netbackup/db]
    G --> P[Adjust retention or rerun\nbpexpdate to extend if needed]
    I --> Q[Collect nbsupport bundle\nfor Veritas SR]
    J --> Q
    K --> Q
    L --> Q
    M --> Q
    N --> Q
    O --> Q
    P --> Q

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,H dark
    class C,D,E,F,G,I,J,K,L,M,N,O,P action
    class Q escalate
```

## Before you begin

- **Access:** NetBackup admin role on the master server; root or sudo on Linux master/media servers
- **Gather first:** the failed job ID (from Admin Console or `bpdbjobs`), the exit code, the policy name, and the affected client hostname
- **Scope:** confirm whether the failure affects one client, one policy, one media server, or all backups
- **Exit codes:** NetBackup exit codes are specific — always look up the exact code in the Veritas documentation or `man bpdbjobs` before drawing conclusions

---

## Step 1 — Check failed jobs

```bash
# List all failed jobs in the last 24 hours
/usr/openv/netbackup/bin/admincmd/bpdbjobs -report -hoursago 24 -state failed
# Output: JobId, Type, State, Status, Policy, Schedule, Client, StartTime, EndTime

# Get detailed report for a specific job
/usr/openv/netbackup/bin/admincmd/bpdbjobs -jobid <job-id> -report
# Shows: every step, exit code, error message text, media server used, storage unit

# Common exit codes:
# 0    = successful
# 1    = partially successful
# 13   = file read failed (client-side permission or agent issue)
# 58   = can't connect to client (network, bpcd service)
# 96   = unable to allocate new media (no media available in pool)
# 196  = network connection broken to media server
# 213  = no storage units available for policy

# View all active jobs
/usr/openv/netbackup/bin/admincmd/bpdbjobs -report -hoursago 1 -state active
```

---

## Step 2 — Check storage unit and pool capacity

```bash
# List all storage units with type, media server, and high watermark
/usr/openv/netbackup/bin/admincmd/bpstulist -U
# Columns: STU Name, Storage Type, Media Server, Free Space, Max MPX, High Watermark
# Problem: Free Space 0% or near High Watermark limit

# Check MSDP / AdvancedDisk pool utilization
/usr/openv/netbackup/bin/admincmd/nbdevquery -listdp -stype PureDisk -U
# Shows: disk pool name, total capacity, used capacity, available

# MSDP pool detailed health check
cacontrol --dsstat -d /msdp/data/dp1
# Expected: Status = Active; shows dedup ratio and throughput

# Check MSDP fingerprint database health
cacontrol --dbstat
# Expected: no errors; shows FP DB size

# List tape media by pool and status
/usr/openv/netbackup/bin/admincmd/vmquery -b -pn <volume-pool-name>
# Status: Active, Full, Frozen (frozen media = error; cannot be written)

# Check tape drives in robot
/usr/openv/netbackup/bin/admincmd/tpconfig -d
# Shows: drive name, serial, status (Up/Down)
```

---

## Step 3 — Check policy and client configuration

```bash
# List all policies with schedule and client detail
/usr/openv/netbackup/bin/admincmd/bppllist -allpolicies -L

# Check a specific policy schedule (backup windows, frequency, type)
/usr/openv/netbackup/bin/admincmd/bpplschedrep <policy-name>

# List catalog images available for a client
/usr/openv/netbackup/bin/admincmd/bplist -C <client-hostname> -t 0 -l
# -t 0 = any backup type; -l = long format with date and size

# Check registered clients and their attributes
/usr/openv/netbackup/bin/admincmd/bpplclients <policy-name> -L

# Verify policy is active and has valid clients
/usr/openv/netbackup/bin/admincmd/bppllist <policy-name> -L | grep -E "ACTIVE|CLIENT|SCHED"
```

---

## Step 4 — Check media server status and catalog

```bash
# List all registered hosts in EMM (Enterprise Media Manager)
/usr/openv/netbackup/bin/admincmd/nbemmcmd -listhosts

# Check media server status specifically
/usr/openv/netbackup/bin/admincmd/nbemmcmd -listhosts -machinetype mediaserver
# Expected: all media servers with Status = UP

# Re-register a media server if missing
/usr/openv/netbackup/bin/admincmd/nbemmcmd -updatehost -machinename <media-server> -machinetype mediaserver

# Check catalog database consistency
/usr/openv/netbackup/bin/admincmd/bpdbm -consistency -verbose
# Expected: no inconsistencies reported

# Check catalog disk usage
du -sh /usr/openv/netbackup/db/
# NetBackup catalog PostgreSQL database; should have > 20% free space on the partition

# Test network connectivity to media server
ping -c 10 <media-server>
traceroute <media-server>

# Verify vnetd port 1556 is listening on master and media
netstat -tulnp | grep 1556
```

---

## Step 5 — Read VxUL logs

```bash
# VxUL logs location (Unified Logging)
ls /usr/openv/logs/

# Query logs by Origin ID (OID) and time range
# OID 117 = nbpem (policy execution manager — job dispatch)
vxlogview -o 117 -d 24h -t "DEBUG|WARNING|ERROR" | less

# OID 118 = nbjm (job manager — data transfer)
vxlogview -o 118 -d 24h -t "WARNING|ERROR" | less

# OID 119 = nbstserv (storage service — STU and media)
vxlogview -o 119 -d 24h -t "ERROR" | less

# OID 143 = nbwebsvc (NetBackup web service — API)
vxlogview -o 143 -d 24h -t "ERROR" | less

# Legacy log directories (pre-VxUL; create directories if debugging)
mkdir -p /usr/openv/netbackup/logs/bpcd     # client daemon
mkdir -p /usr/openv/netbackup/logs/bpbrm    # backup/restore manager
mkdir -p /usr/openv/netbackup/logs/bprd     # request daemon
mkdir -p /usr/openv/netbackup/logs/bpdm     # disk manager
```

---

## Step 6 — Increase verbose logging temporarily

```bash
# Set verbose level to 3 (moderate) on master server
/usr/openv/netbackup/bin/admincmd/bpsetconfig -h <master-server> <<'EOF'
VERBOSE = 3
EOF
# Valid range: 0 (default) to 5 (maximum — very verbose; use briefly)

# After reproducing the issue, revert to default
/usr/openv/netbackup/bin/admincmd/bpsetconfig -h <master-server> <<'EOF'
VERBOSE = 0
EOF

# Set on a specific media server
/usr/openv/netbackup/bin/admincmd/bpsetconfig -h <media-server> <<'EOF'
VERBOSE = 3
EOF
```

---

## Step 7 — Generate nbsupport bundle for Veritas SR

```bash
# Generate diagnostic bundle on the master server
/usr/openv/netbackup/bin/support/nbsupport
# Output: /tmp/nbsupport_<hostname>_<timestamp>.tar.gz
# Includes: VxUL logs, config files, job history, storage unit config

# Include job detail for the failing job in the SR
/usr/openv/netbackup/bin/admincmd/bpdbjobs -jobid <job-id> -report \
  > /tmp/job_${job_id}_report.txt

# Include storage unit status
/usr/openv/netbackup/bin/admincmd/bpstulist -U > /tmp/stu_status.txt
/usr/openv/netbackup/bin/admincmd/nbdevquery -listdp -stype PureDisk -U >> /tmp/stu_status.txt

# Upload to Veritas support portal with:
# - nbsupport .tar.gz file
# - Job ID, exit code, and time window of the issue
# - Policy name, client name, and storage unit name
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| VxUL (nbpem / nbjm) | `vxlogview -o 117 -d 24h` / `vxlogview -o 118 -d 24h` | Job dispatch and data transfer errors |
| Legacy logs | `/usr/openv/netbackup/logs/<daemon>/` | Pre-VxUL daemon logs |
| Catalog | `/usr/openv/netbackup/db/` (PostgreSQL) | Catalog inconsistency and size issues |
| bpdbjobs job report | `bpdbjobs -jobid <id> -report` | Step-by-step job trace with exit code |
| MSDP health | `cacontrol --dsstat` | Dedup pool health and fingerprint DB |
| Windows Event Log | Get-EventLog Application source NetBackup | Windows NBU errors |

---

## See also

- [NetBackup — Common Issues](../common-issues/)
- [NetBackup — Escalation](../escalation/)
- [NetBackup — Health Checks](../../operations/health-checks/)

## Verify resolution

- `bpdbjobs -report -hoursago 24 -state failed` shows no new failures for the affected policy/client
- `bpstulist -U` shows free space above the high watermark threshold on all affected storage units
- Trigger a manual backup of the affected policy: confirm it completes with exit code 0
- `vxlogview -o 118 -d 1h -t "ERROR"` shows no new errors in the last hour
