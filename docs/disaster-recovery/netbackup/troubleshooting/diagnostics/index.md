# NetBackup — Diagnostics

> Part of the [NetBackup Troubleshooting](../index.md) reference.

---

## Log Locations

NetBackup uses a unified log framework (VxUL) for most modern components, supplemented by legacy per-daemon flat logs.

### Legacy (flat) logs — primary troubleshooting source

| Log path | Component | When to check |
|---|---|---|
| `/usr/openv/netbackup/logs/bprd/log.<yyyymmdd>` | Backup/restore request daemon | Job submission errors, policy lookup failures |
| `/usr/openv/netbackup/logs/bpbrm/log.<yyyymmdd>` | Backup/restore manager | Client connection failures, status 23/59 |
| `/usr/openv/netbackup/logs/bpcd/log.<yyyymmdd>` | Client daemon | Client-side job errors |
| `/usr/openv/netbackup/logs/bptm/log.<yyyymmdd>` | Tape/media manager | Drive errors, media allocation, status 83 |
| `/usr/openv/netbackup/logs/bpdbm/log.<yyyymmdd>` | Catalog database manager | Catalog corruption, backup failures |
| `/usr/openv/netbackup/logs/nbemm/log.<yyyymmdd>` | Enterprise media manager | Media server registration, EMM comms |
| `/usr/openv/netbackup/logs/spoold/log.<yyyymmdd>` | MSDP storage daemon | Deduplication errors, pool health |
| `/usr/openv/netbackup/logs/nbjm/log.<yyyymmdd>` | Job manager | Job scheduling and queue issues |
| `C:\Program Files\Veritas\NetBackup\logs\bpcd\log.<yyyymmdd>` | Client daemon (Windows) | Windows client job errors |

### VxUL unified logs

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

---

## Daemon Status Diagnostics

```bash
# Show all running NetBackup processes (master/media server)
bpps -a

# Confirm all expected daemons are UP
/usr/openv/netbackup/bin/bpgetconfig -g localhost -L | grep -i daemon

# Restart all NetBackup services (use with caution — kills active jobs)
/usr/openv/netbackup/bin/bp.kill_all
/usr/openv/netbackup/bin/bp.start_all
```

---

## Job Diagnostics

```bash
# Summary of all jobs in the last 24 hours
bpdbjobs -report -all_columns -hoursago 24

# Detail for a specific failed job
bpdbjobs -jobid <job-id> -report

# Show failed jobs in last 24 hours with status code
bpdbjobs -report -failed -hoursago 24 | grep -E "jobid|status"

# Get the status code explanation
bperror -S <status-code> -L

# Trace a job end-to-end (requires debug logging enabled)
grep "<job-id>" /usr/openv/netbackup/logs/bpbrm/log.<yyyymmdd>
grep "<job-id>" /usr/openv/netbackup/logs/bprd/log.<yyyymmdd>
```

---

## Client Connectivity Diagnostics

```bash
# Test NetBackup client from master server
bptestbpcd -client <client-hostname>

# Manually test port reachability (bpcd port)
nc -zv <client-hostname> 13782
telnet <client-hostname> 13782

# Check client's server list (what masters the client trusts)
bpgetconfig -g <client-hostname> -L | grep -E "SERVER|CLIENT"

# Validate name resolution matches between master and client
nslookup <client-hostname>           # Run on master
nslookup <master-hostname>           # Run on client
```

---

## Storage and Media Diagnostics

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

---

## Policy and Catalog Diagnostics

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

---

## Media Server Diagnostics

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

---

## Enabling Debug Logging

NetBackup logs are only written if the log directories exist. Create missing directories to enable logging:

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

---

## Diagnostic Bundle for Veritas Support

```bash
# Generate nbsupport bundle (run on master server)
/usr/openv/netbackup/bin/support/nbsupport

# Output is written to:
# /tmp/nbsupport_<hostname>_<timestamp>.tar.gz

# Include job IDs and time window when submitting to Veritas
bpdbjobs -jobid <id> -report > /tmp/job_<id>_report.txt
```
