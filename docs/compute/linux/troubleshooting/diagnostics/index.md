---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# Linux — Diagnostics

<div class="kb-summary">
Linux diagnostic commands: query journald for service errors, read dmesg for hardware and kernel events, search auditd for SELinux denials and auth failures, trace a process with strace and lsof, profile CPU and I/O with vmstat and sar, and collect a full diagnostic bundle for vendor escalation.

*Applies to: RHEL 8/9 · Ubuntu 22.04/24.04 LTS*
</div>

```text
┌───────────────────────────────────────── Linux — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Start here: journalctl -b -p err → dmesg -T → ausearch for SELinux or auth events         │     │
│   │   Process crashing: strace -p PID to trace syscalls; lsof -p PID for open file leaks        │     │
│   │   Performance: vmstat 1 for memory and I/O; sar -u 1 10 for CPU; perf top for hotspots      │     │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Log Analysis                 │  │               Process Tracing               │   │
│   │   journalctl -b -p err: boot errors          │  │   strace -p PID: syscall trace             │    │
│   │   dmesg -T: timestamped kernel events        │  │   lsof -p PID: open files and sockets      │    │
│   │   ausearch -m avc: SELinux denials           │  │   /proc/PID/: maps, fd, status, cmdline    │    │
│   │   journalctl -u unit: per-service log        │  │   gdb -p PID: interactive debugger         │    │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  x86-64 server · NIC · storage (local SSD or SAN/NAS) · out-of-band IPMI · monitoring agent           │
│                                                                                                       │
│  Key terms:                                                                                           │
│  journalctl   = systemd log query tool; reads from the binary journal; filter by unit/priority/time   │
│  dmesg        = kernel ring buffer; hardware events, OOM kills, NIC errors, storage SCSI errors       │
│  auditd       = kernel audit daemon; logs syscalls, file access, auth events by policy                │
│  ausearch     = searches auditd log by type, user, file, syscall, or time                             │
│  strace       = system call tracer; attaches to a running process and shows all kernel calls          │
│  lsof         = list open files; shows files, sockets, pipes, and shared memory held by each process  │
│  perf         = Linux performance counter profiler; CPU sampling, flamegraph generation               │
│  vmstat       = virtual memory statistics; shows procs, memory, swap, I/O, CPU per interval           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    A([Linux Issue]) --> B{What type of problem?}
    B -->|Service crashed or won't start| C[journalctl -u service --since today\nCheck exit code and error message]
    B -->|Kernel panic or hardware error| D[dmesg -T | grep -i error\nCheck for OOM or SCSI errors]
    B -->|Permission denied or SELinux| E[ausearch -m avc --start recent\navc: denied = SELinux blocking the action]
    B -->|Login failure or auth issue| F[journalctl _SYSTEMD_UNIT=sshd.service\nausearch -m USER_AUTH --success no]
    B -->|High CPU or memory usage| G[vmstat 1 5 / sar -u 1 10\nperf top to find hot function]
    B -->|High I/O or storage error| H[dmesg -T | grep -i scsi\niostat -x 1 5 to find saturated device]
    B -->|Process leak or crash loop| I[strace -p PID\nlsof -p PID | wc -l for fd leak]
    C --> J{Exit code?}
    J -->|Permission error| E
    J -->|File not found| K[lsof -p PID at startup\nCheck paths in unit file]
    J -->|Signal / crash| L[journalctl -b -1 -p err | grep coreclr\nCheck dmesg for OOM kill]
    D --> M[Check DIMM errors\ndmesg | grep -i ECC\|memory\|MCE]
    E --> N[sesearch -A -s process_type -t file_type\nAudit2allow to create policy or relabel]
    F --> O[grep Failed /var/log/secure\nCheck pam_tally lockout]
    G --> P[perf top --sort comm\nCheck WCHAN for blocked threads: ps -eo pid,wchan | grep D]
    H --> Q[iostat -x 1 sda: await > 20ms = issue\nCheck dmesg for SCSI timeouts]
    I --> R[Check /proc/PID/fd count vs ulimit -n\nstrace -c -p PID for syscall summary]
    J --> S[Collect sosreport or gather-tech-support bundle]
    K --> S
    L --> S
    M --> S
    N --> S
    O --> S
    P --> S
    Q --> S
    R --> S

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,J dark
    class C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R action
    class S escalate
```

## Before you begin

- **Access:** root or sudo-capable account on the target host
- **Gather first:** the service name or process that is failing, the exact error message, and the time the issue started
- **Scope:** confirm whether the issue affects one process, one service, one host, or multiple hosts

---

## Step 1 — Read the service and system log

```bash
# All errors from the current boot
journalctl -b -p err --no-pager | tail -50

# All errors from a specific service since midnight
journalctl -u nginx.service --since today -p err

# Follow a service log in real time
journalctl -u nginx.service -f

# All logs 5 minutes around a known failure time
journalctl --since "2026-06-01 14:25:00" --until "2026-06-01 14:35:00" -p warning

# Check previous boot (for crash or reboot cause)
journalctl -b -1 -p err | tail -100

# Search all units for a specific string
journalctl --since today | grep -i "out of memory\|SIGKILL\|timeout\|refused"

# Disk usage of the journal
journalctl --disk-usage
# If > 2GB: vacuum to 7 days
journalctl --vacuum-time=7d
```

---

## Step 2 — Read dmesg for kernel and hardware events

```bash
# Timestamped kernel ring buffer (most recent last)
dmesg -T | tail -100

# Filter for hardware errors
dmesg -T | grep -i "error\|fail\|warn\|ECC\|MCE\|SCSI\|NVMe\|OOM"

# OOM kills (memory pressure killing processes)
dmesg -T | grep -i "Out of memory\|Killed process"
# Shows: killed process name, PID, and rss (resident memory in KB at time of kill)

# Storage SCSI/NVMe errors
dmesg -T | grep -i "SCSI\|timeout\|reset\|exception\|I/O error"
# Shows: device name (sda/sdb), error type, and LBA address

# NIC errors
dmesg -T | grep -i "eth\|em\|bond\|link\|carrier\|reset"

# MCE (Machine Check Exceptions — hardware faults)
dmesg -T | grep -i "MCE\|DIMM\|memory controller"
```

---

## Step 3 — Search audit log for SELinux denials and auth events

```bash
# SELinux denials (most common reason for unexpected permission denied)
ausearch -m avc --start recent
# Shows: type=AVC avc: denied { action } for pid=X scontext=source tcontext=target

# Summarize SELinux denials by type
aureport --avc --start today

# Failed login events today
ausearch -m USER_AUTH --success no --start today
# Shows: who tried to log in, from which terminal, and the auth result

# Changes to sensitive files
ausearch -f /etc/passwd --start today
ausearch -f /etc/sudoers --start today

# Commands run via sudo today
ausearch -ua root --start today | grep EXECVE

# Summary report of all audit events today
aureport --summary --start today
aureport --login --failed --start today
```

---

## Step 4 — Diagnose authentication and SSH events

```bash
# Failed SSH password attempts
journalctl _SYSTEMD_UNIT=sshd.service | grep "Failed password" | tail -30

# Successful SSH logins
journalctl _SYSTEMD_UNIT=sshd.service | grep "Accepted" | tail -20

# Account lockouts (pam_tally or pam_faillock)
journalctl | grep "pam_tally\|account locked\|pam_unix.*authentication failure" | tail -20

# Check current pam_faillock lockout state (RHEL 8/9)
faillock --user <username>
# Reset a locked account
faillock --user <username> --reset

# Check sudo usage today
journalctl --since today | grep sudo | tail -30

# Recent su or su-l events (privilege escalation)
journalctl --since today | grep -E "su\[|su-l"
```

---

## Step 5 — Trace a failing process

```bash
# Attach strace to a running process (shows all system calls)
strace -p <PID>
# Press Ctrl-C to stop

# Summarize syscall count and time (less verbose)
strace -c -p <PID>
# Shows table: calls, errors, total time, avg time, syscall name

# Trace a new command from start with output
strace -o /tmp/strace-out.txt <command>

# List all open files and sockets for a process
lsof -p <PID>

# Count open file descriptors (check for fd leak)
ls /proc/<PID>/fd | wc -l
# Compare against ulimit -n (typically 1024 or 65536 soft limit)

# Check per-process memory maps
cat /proc/<PID>/status | grep -E "VmRSS|VmPeak|Threads"

# Check what a process is waiting for (D = uninterruptible I/O wait)
ps -eo pid,comm,stat,wchan | grep " D "
# D state processes = waiting for I/O (storage or network filesystem)
```

---

## Step 6 — Profile performance

```bash
# Memory, swap, and I/O per second (run for 10 iterations)
vmstat 1 10
# Columns: r=run queue, b=blocked, swpd=swap, bi/bo=block I/O, wa=wait%

# CPU utilization per second (10 samples)
sar -u 1 10
# %user, %system, %iowait — iowait > 20% = storage bottleneck

# Disk I/O per device (1-second intervals)
iostat -x 1 5
# Key: await (avg wait ms); util% (device saturation); > 20ms await or > 80% util = issue

# Top processes by CPU
perf top --sort comm
# Press Ctrl-C to stop

# Flamegraph via perf (captures 30 seconds of CPU samples)
perf record -ag -F 99 -- sleep 30
perf report --stdio | head -50

# Network I/O per interface
sar -n DEV 1 5
# rxkB/s and txkB/s per interface

# Find large files or directories consuming disk
du -sh /var/log/* 2>/dev/null | sort -h | tail -20
df -h
```

---

## Step 7 — Collect diagnostic bundle for escalation

```bash
# RHEL — generate sosreport (full diagnostic bundle)
sosreport
# Output: /var/tmp/sosreport-<hostname>-<date>.tar.xz
# Prompts for a case number to embed in the filename

# Include specific plugins for targeted analysis
sosreport --only-plugins=networking,storage,systemd

# Ubuntu — generate support bundle
ubuntu-advantage collect-logs 2>/dev/null || \
  tar czf /tmp/linux-diag-$(date +%Y%m%d).tar.gz \
    /var/log/syslog /var/log/auth.log \
    /var/log/kern.log /var/log/messages 2>/dev/null

# Manual log collection for any distro
tar czf /tmp/linux-diag-$(date +%Y%m%d).tar.gz \
  /var/log/messages /var/log/secure \
  /etc/os-release /proc/cpuinfo

# Always include:
journalctl -b --no-pager > /tmp/journal-boot.txt
dmesg -T > /tmp/dmesg.txt
ps auxf > /tmp/ps-tree.txt
free -h > /tmp/memory.txt
df -h > /tmp/disk.txt
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| systemd journal | `journalctl -b -p err` | Service failures, crash events |
| Kernel ring buffer | `dmesg -T` | Hardware errors, OOM kills, SCSI/storage |
| Audit daemon | `ausearch -m avc` / `/var/log/audit/audit.log` | SELinux denials, auth failures |
| Authentication | `journalctl _SYSTEMD_UNIT=sshd.service` | SSH login failures and successes |
| Application logs | `/var/log/` (varies by app) | App-specific errors |
| Core dumps | `/var/lib/systemd/coredump/` or `/tmp/core.*` | Process crash dumps |

---

## See also

- [Linux — Common Issues](../common-issues/)
- [Linux — Escalation](../escalation/)

## Verify resolution

- `journalctl -b -p err -u <service>` shows no new errors after the fix
- `dmesg -T | grep -i error` shows no new hardware errors
- `ausearch -m avc --start recent` shows no new SELinux denials
- The service or process that was failing starts successfully and remains running for at least 10 minutes
- Application-level health check (HTTP 200, successful test query) passes
