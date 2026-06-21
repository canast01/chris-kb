---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Data Domain — Diagnostics

<div class="kb-summary">
Data Domain diagnostic commands: check filesystem state with <code>filesys status</code> and space usage with <code>filesys show space</code>, inspect active alerts with <code>alerts show current</code>, check disk states with <code>disk show state</code> and RAID rebuild with <code>raid show detail</code>, diagnose replication lag with <code>replication status</code> and <code>net ping</code>, investigate DD Boost auth failures with <code>ddboost user list</code>, and collect a support bundle with <code>support bundle generate</code> for Dell escalation.

*Applies to: Data Domain DD OS 7.x*
</div>
![Data Domain — Diagnostics](../../../../assets/storage-dell-data-domain-troubleshooting-diagnostics.svg)




```mermaid
graph TD
    A([Data Domain Issue]) --> B[alerts show current\nfilesys status\nfilesys show space]
    B --> C{Hardware alert active?}
    C -->|Yes| D[disk show state: failed or unknown\nenclosure show hardware: fans PSUs\nOpen Dell support case]
    C -->|No| E{Filesystem not Running?}
    E -->|Yes| F[filesys enable\nMonitor filesys status till Running\nCheck space: filesys show space]
    E -->|No| G{Replication in Error?}
    G -->|Yes| H[replication show errors: detail\nnet ping <dst-dd>: connectivity\nreplication disable then re-enable]
    G -->|No| I{DDBoost auth failure?}
    I -->|Yes| J[ddboost user list: user exists?\nddboost show clients: connected?\nlog view audit | grep ddboost]
    I -->|No| K{Capacity > 80%?}
    K -->|Yes| L[filesys clean start\nreplication show stats: consumers\nExpire old backups via backup app]
    K -->|No| M[support bundle generate\nOpen Dell support case]
    D --> M
    F --> M
    H --> M
    J --> M
    L --> M

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,C,E,G,I,K dark
    class B,D,F,H,J,L action
    class M escalate
```

## Before you begin

- **Access:** SSH to the Data Domain management IP as `sysadmin` or `admin`; serial console access for unresponsive systems; SCP server or USB for bundle transfer
- **Gather first:** the DDOS version (`system show version`), active alerts (`alerts show current`), filesystem state (`filesys status`), and the specific symptom — backup failure error code, replication context name and lag, or DDBoost error message from the backup application
- **Scope:** confirm whether the issue is a filesystem problem (not Running, full), a hardware problem (disk or enclosure alert), a replication problem (specific context in Error state), or a backup integration problem (DDBoost auth failure from a specific backup server)

---

## Step 1 — Filesystem diagnostics

### Check filesystem state

```bash
# State: should show Enabled / Running
filesys status

# Space usage (pre-comp, post-comp, physical)
filesys show space

# Dedup and compression ratios (global and per-stream)
filesys show compression

# Compression trend (shows changes over time)
filesys show compression summary

# Cleaning state
filesys clean status
filesys clean show history

# Filesystem event log (recent filesystem-layer events)
filesys show log
```

### Interpret `filesys show space` output

| Field | Meaning |
|---|---|
| Pre-comp used | Total logical data written by backup software (before dedup/compression) |
| Post-comp used | Physical disk space consumed after dedup and compression |
| Physical capacity | Total raw disk capacity of the array |
| Available | Physical capacity minus post-comp used |
| Compression factor | Pre-comp / post-comp — the effective dedup ratio |

A healthy system shows post-comp used below 80% of physical capacity and a compression factor above 10x.

### Check filesystem integrity

```bash
# Run an online filesystem check
filesys check

# View check results
filesys show log | grep -i check
```

`filesys check` is a non-destructive read-only integrity scan. It may take hours on large arrays. Run it only when integrity is suspected, not as a routine check.

---

## Step 2 — Replication diagnostics

### State triage

```bash
# All contexts and their state
replication show

# Detailed per-context status with lag, throughput, and estimated completion
replication status

# Configuration of each context (source, destination, schedule)
replication show config

# Statistics per context (bytes sent, compression ratio, lag)
replication show stats

# Context-specific errors
replication show errors
```

### Interpreting replication state

| State | Meaning | Urgency |
|---|---|---|
| `Replicating` | Actively syncing data | None |
| `Idle` | Fully synced; waiting for next scheduled sync | None |
| `Initializing` | First-time sync in progress (can take hours/days for large data) | Monitor |
| `Disabled` | Replication paused — intentional or unintentional | Investigate |
| `Error` | Replication failed — immediate investigation required | High |
| `Idle-Error` | Last sync encountered an error but context is idle now | Investigate |

### Lag measurement and analysis

```bash
# Lag in bytes remaining to replicate
replication show stats | grep -i "pre-comp remaining\|lag"

# Throughput in MB/s
replication status | grep -i throughput

# Estimated completion
replication status | grep -i "estimated completion"
```

Convert bytes to time: if pre-comp remaining is 500 GB and throughput is 100 MB/s, estimated catchup is approximately 84 minutes (500 × 1024 / 100 / 60). A growing lag when throughput is non-zero means the source ingest rate exceeds replication drain rate.

### Network path verification

```bash
# Test connectivity to the destination DD
net ping <destination-dd-hostname>

# Trace the network path
net traceroute <destination-dd-hostname>

# Check for interface errors and drops on the replication interface
net show stats | grep -iE "error|drop|collision"

# Check that the correct interface is used for replication
net show all
net route show
```

---

## Step 3 — DD Boost diagnostics

### Service and client status

```bash
# Is the DD Boost service running?
ddboost status

# All connected clients and their state
ddboost show clients

# Verbose client information (connection time, throughput)
ddboost show clients --verbose

# Storage unit list and their mapped MTrees
ddboost storage-unit list
ddboost storage-unit show <name>

# DD Boost throughput statistics
ddboost show stats

# Distributed Segment Processing (DSP) status
ddboost option show | grep -i dist-seg
```

### Diagnosing a DDBoost authentication failure

```bash
# 1. Confirm the expected user exists
ddboost user list

# 2. Confirm the user is assigned to a storage unit
ddboost user list | grep <username>

# 3. Check whether the client appears in the connected list at all
ddboost show clients | grep <backup-server-hostname>

# 4. Review recent authentication events in the audit log
log view audit | grep -i "ddboost\|boost\|auth"
```

---

## Step 4 — Disk and hardware diagnostics

### Disk health

```bash
# All disks with state
disk show state

# Full hardware detail per disk (firmware, model, S/N)
disk show hardware

# Per-disk error statistics
disk show detail | grep -iE "slot|error|sector|reallocated"

# Identify any disk not in 'normal' or 'spare' state
disk show state | grep -ivE "normal|spare"
```

### Disk states reference

| State | Meaning | Action |
|---|---|---|
| `normal` | Healthy and in use | None |
| `spare` | Hot spare, available for automatic rebuild | None |
| `reconstructing` | Rebuilding RAID — do not remove any disk | Monitor rebuild progress |
| `failed` | Hard failure — cannot be read or written | Open Dell support case immediately |
| `unknown` | Not recognised — new disk or seating issue | Check physical seating; do not pull other disks |
| `absent` | Empty bay | Expected if slot is intentionally unused |

### RAID group status

```bash
# RAID group overview
raid show all

# Detailed RAID group status with member disks
raid show detail

# Rebuild progress
raid show detail | grep -iE "rebuild|reconstruct|percent complete"
```

### Enclosure health

```bash
# Full hardware inventory: power, fans, temperature
enclosure show hardware

# All enclosures with state
enclosure show all

# Filter for any faults
enclosure show hardware | grep -iE "fault|fail|warn|critical"
```

---

## Step 5 — Network diagnostics

### Interface state

```bash
# All interfaces — IP, speed, state, MTU
net show all

# Interface configuration (bonding, VLAN, MTU)
net show config

# Network statistics per interface (rx/tx, errors, drops)
net show stats

# Network settings (DNS, gateway, hostname)
net show settings
```

### Connectivity testing

```bash
# Ping from the Data Domain to a target
net ping <ip-or-hostname>
net ping <ip-or-hostname> count 20

# Traceroute
net traceroute <ip-or-hostname>

# Verify DNS resolution
net show settings | grep -i dns
```

### Bonding and LACP

```bash
# Show bonding configuration and active links
net config bond show

# Verify LACP negotiation is successful
net show stats | grep -A5 <bond-interface-name>
```

If a bonded interface is degraded (one link down), throughput is reduced by 50% and the interface will appear as active but with fewer physical links in `net config bond show`.

---

## Step 6 — Log analysis and advanced diagnostics

### Log locations

| Log | Command | Contains |
|---|---|---|
| System log | `log view` | DDOS events, service restarts, hardware events |
| Audit log | `log view audit` | User logins, config changes, all CLI commands |
| Replication log | `log view replication` | Replication events, errors, throughput history |

```bash
# Most recent system log entries (scrollable)
log view

# Follow system log in real time
log watch

# Filter for specific keywords
log view | grep -i "error\|critical\|fail"

# View a specific named log
log view <log-filename>
```

### Common log patterns

| Log Pattern | Meaning |
|---|---|
| `EVT-FILESYS-FULL` | Filesystem at capacity; backup writes will fail |
| `EVT-DISK-FAILED` | Physical disk failure; open support case |
| `EVT-REPL-ERROR` | Replication context entered error state |
| `EVT-DDBOOST-AUTH-FAIL` | DD Boost authentication failure from backup server |
| `EVT-NTP-DRIFT` | Clock drift detected; verify NTP server reachability |
| `EVT-CLEAN-COMPLETE` | Cleaning cycle completed; check `filesys show space` |
| `EVT-CERT-EXPIRE` | TLS certificate approaching expiry; renew |

### Advanced diagnostics with `ddsh`

`ddsh` provides access to Unix-like diagnostic tools not available in the standard DDOS CLI.

```bash
# Enter the diagnostic shell
ddsh

# Inside ddsh:
diagnose all           # full built-in system diagnostic run

iostat -x 1 30         # I/O statistics (30 samples at 1-second intervals)
vmstat 1 10            # Virtual memory, CPU, and I/O stats
netstat -an            # Active network connections
df -h                  # Filesystem usage from OS perspective
top                    # Real-time process list

# Exit ddsh
exit
```

High `%util` on a disk device during backup operations is expected. A concern arises when `await` (average I/O wait time) exceeds 50–100 ms during writes or `%util` is at 100% on multiple devices simultaneously without explanation.

---

## Step 7 — Support bundle collection

```bash
# Generate a support bundle
support bundle generate

# List available bundles
support bundle show

# Transfer bundle to a remote server via SCP
support bundle export scp://user@<jump-host>:/path/bundles/

# Send directly to Dell for an open case
autosupport send <case-number>
```

The support bundle is saved to `/ddr/var/support/` on the DD. For large arrays, the bundle can be several gigabytes. Transfer via SCP from a host with network access to the DD management interface.

### Incident type quick reference

| Incident | Key Commands |
|---|---|
| Backup job failure | `filesys status`, `filesys show space`, `ddboost show clients`, `alerts show current` |
| Replication lag | `replication status`, `replication show stats`, `net show stats`, `net ping <dst>` |
| Disk alert | `disk show state`, `disk show hardware`, `raid show detail`, `enclosure show hardware` |
| Low dedup ratio | `filesys show compression`, `mtree show compression mtree /data/col1/<name>` |
| Slow restore | `filesys clean status`, `ddboost show stats`, `system show stats` |
| Authentication failure | `log view audit`, `ddboost user list`, `auth show` |
| Network connectivity | `net show all`, `net show stats`, `net ping <target>`, `net traceroute <target>` |
| CloudIQ / AutoSupport offline | `autosupport status`, `autosupport test`, `net ping <scg-ip>` |

---

## Log locations

| Log | Command | Contents |
|---|---|---|
| System log | `log view` | DDOS events, service restarts, hardware events |
| Audit log | `log view audit` | User logins, config changes, all CLI commands |
| Replication log | `log view replication` | Replication events, errors, throughput history |
| Debug / support bundle | `support bundle generate` | All logs; required for Dell support cases |

---

## See also

- [Data Domain — Common Issues](common-issues/)
- [Data Domain — Escalation](escalation/)
- [Data Domain — Health Checks](../operations/health-checks/)

## Verify resolution

- `filesys status` returns `Enabled / Running` with no warnings
- `alerts show current` returns no active alerts related to the incident
- `disk show state | grep -ivE "normal|spare|absent"` returns no output (all disks normal or spare)
- For replication issues: `replication status` shows all contexts as `Replicating` or `Idle` with lag at zero or decreasing
- For DD Boost: `ddboost show clients` shows the backup server as `connected` with no authentication errors
- `filesys show space` shows post-comp usage below 80% of physical capacity
