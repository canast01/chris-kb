---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
description: "Linux diagnostic commands: query journald for service errors, read dmesg for hardware and kernel events, search auditd for SELinux denials and auth..."
---
# Linux — Diagnostics

<div class="kb-summary">
Linux diagnostic commands: query journald for service errors, read dmesg for hardware and kernel events, search auditd for SELinux denials and auth failures, trace a process with strace and lsof, profile CPU and I/O with vmstat and sar, and collect a full diagnostic bundle for vendor escalation.

*Applies to: RHEL 8/9 · Ubuntu 22.04/24.04 LTS*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "journalctl -u service --since today\nCheck exit code and error message" {shape: rectangle}
D: "dmesg -T | grep -i error\nCheck for OOM or SCSI errors" {shape: rectangle}
E: "ausearch -m avc --start recent\navc: denied = SELinux blocking the action" {shape: rectangle}
F: "journalctl _SYSTEMD_UNIT=sshd.service\nausearch -m USER_AUTH --success no" {shape: rectangle}
G: "vmstat 1 5 / sar -u 1 10\nperf top to find hot function" {shape: rectangle}
H: "dmesg -T | grep -i scsi\niostat -x 1 5 to find saturated device" {shape: rectangle}
I: "strace -p PID\nlsof -p PID | wc -l for fd leak" {shape: rectangle}
J: "J" {shape: rectangle}
K: "lsof -p PID at startup\nCheck paths in unit file" {shape: rectangle}
L: "journalctl -b -1 -p err | grep coreclr\nCheck dmesg for OOM kill" {shape: rectangle}
M: "Check DIMM errors\ndmesg memory\|MCE" {shape: rectangle}
N: "sesearch -A -s process_type -t file_type\nAudit2allow to create policy or relabel" {shape: rectangle}
O: "grep Failed /var/log/secure\nCheck pam_tally lockout" {shape: rectangle}
P: "perf top --sort comm\nCheck WCHAN for blocked threads: ps -eo pid,wchan\n| grep D" {shape: rectangle}
Q: "iostat -x 1 sda: await > 20ms = issue\nCheck dmesg for SCSI timeouts" {shape: rectangle}
R: "Check /proc/PID/fd count vs ulimit -n\nstrace -c -p PID for syscall summary" {shape: rectangle}
S: "Collect sosreport or gather-tech-support bundle" {shape: rectangle}
A: "Linux Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
B -> I
J -> E
J -> K
J -> L
D -> M
E -> N
F -> O
G -> P
H -> Q
I -> R
J -> S
K -> S
L -> S
M -> S
N -> S
O -> S
P -> S
Q -> S
R -> S
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_read_the_service_and_system_l: "Step 1 — Read the service and system log" {shape: rectangle}
step_2_read_dmesg_for_kernel_and_har: "Step 2 — Read dmesg for kernel and hardware events" {shape: rectangle}
step_3_search_audit_log_for_selinux_: "Step 3 — Search audit log for SELinux denials and\nauth event" {shape: rectangle}
step_4_diagnose_authentication_and_s: "Step 4 — Diagnose authentication and SSH events" {shape: rectangle}
step_5_trace_a_failing_process: "Step 5 — Trace a failing process" {shape: rectangle}
step_6_profile_performance: "Step 6 — Profile performance" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_read_the_service_and_system_l: investigate
symptom -> step_2_read_dmesg_for_kernel_and_har: investigate
symptom -> step_3_search_audit_log_for_selinux_: investigate
symptom -> step_4_diagnose_authentication_and_s: investigate
symptom -> step_5_trace_a_failing_process: investigate
symptom -> step_6_profile_performance: investigate
step_1_read_the_service_and_system_l -> resolution
step_2_read_dmesg_for_kernel_and_har -> resolution
step_3_search_audit_log_for_selinux_ -> resolution
step_4_diagnose_authentication_and_s -> resolution
step_5_trace_a_failing_process -> resolution
step_6_profile_performance -> resolution
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


```text title="Expected output"
Jun 01 14:32:15 web-prod-01 nginx[2847]: error connecting to upstream: connection refused
Jun 01 14:32:16 web-prod-01 systemd[1]: nginx.service: Main process exited, code=exited, status=1/FAILURE
Jun 01 14:32:18 web-prod-01 kernel: Out of memory: Kill process 3421 (java) score 892 or sacrifice child
Jun 01 14:32:19 web-prod-01 kernel: Killed process 3421 (java) total-vm:4096000kB, anon-rss:3891200kB
Jun 01 14:32:22 web-prod-01 systemd[1]: systemd-journald.service: Assertion failed: n_inotify_watches < n_inotify_watches_max
Jun 01 14:33:01 web-prod-01 sshd[5612]: error: connect_to 10.42.8.15 port 22: Connection refused
Jun 01 14:33:45 web-prod-01 kernel: audit: type=1130 audit(1748901225.123:456): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=docker-compose comm="systemd" exe="/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'

Jun 01 14:25:00 web-prod-01 nginx[2847]: 2026/06/01 14:25:15 [warn] 2847#2847: *1234 upstream server temporarily disabled while connecting to upstream, client: 192.168.1.50, server: api.internal, request: "GET /health HTTP/1.1"
Jun 01 14:27:33 web-prod-01 systemd[1]: [warn] Watchdog timeout (limit 30s)!
Jun 01 14:29:12 web-prod-01 postgresql[1923]: [warn] connection timeout after 300 seconds

Searching for OOM/SIGKILL/timeout/refused:
Jun 01 14:32:18 web-prod-01 kernel: Out of memory: Kill process 3421 (java) score 892
Jun 01 14:32:19 web-prod-01 kernel: Killed process 3421 (java) total-vm:4096000kB
Jun 01 14:33:01 web-prod-01 sshd[5612]: error: connect_to 10.42.8.15 port 22: Connection refused
Jun 01 14:29:12 web-prod-01 postgresql[1923]: connection timeout after 300 seconds

Disk usage of journal:
Archived and volatile journals take up 1.2G on disk.

(no output — command completes silently)
```

!!! warning "Common errors"
    **`journalctl: command not found`** — Install systemd-journal or verify systemd is running with `systemctl status systemd-journald`.
    **`Failed to get realtime timestamp: Cannot assign requested address`** — Ensure system time is synchronized with `timedatectl set-ntp true` or manually set the date.
    **`Vacuuming journal files... Deleted archived
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


```text title="Expected output"
[Mon Dec 19 14:23:47 2024] usb 1-1: new high-speed USB device number 2 using xhci_hcd
[Mon Dec 19 14:23:48 2024] usb 1-1: New USB device found, idVendor=0951, idProduct=1666, bcdDevice= 1.10
[Mon Dec 19 14:24:12 2024] audit: type=1130 audit(1734614652.891:42): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=systemd-tmpfiles-setup-dev comm="systemd" exe="/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[Mon Dec 19 14:25:33 2024] WARNING: CPU: 3 PID: 8421 at drivers/gpu/drm/amd/amdgpu/../display/dc/core/dc.c:1234 dc_create+0x4a8/0x5c0 [amdgpu]
[Mon Dec 19 14:26:01 2024] Out of memory: Kill process 2847 (java) score 312 or sacrifice child
[Mon Dec 19 14:26:01 2024] Killed process 2847 (java) total-vm:8388608kB, anon-rss:7654321kB, file-rss:0kB, shmem-rss:0kB, UID:1001 pgtables:15234kB oom_score_adj:300
[Mon Dec 19 14:27:15 2024] sd 2:0:0:0: [sda] Assuming drive cache: write through
[Mon Dec 19 14:28:42 2024] ata2.00: exception Emask 0x10 SAct 0x0 SErr 0x0 action 0x6
[Mon Dec 19 14:28:42 2024] ata2.00: failed command: READ DMA
[Mon Dec 19 14:28:42 2024] ata2.00: cmd 25/00:08:00:00:00/00:00:00:00:00/e0 tag 0 dma 4096 in
[Mon Dec 19 14:29:10 2024] bond0: link status definitely down for interface eth0, disabling it
[Mon Dec 19 14:29:11 2024] bond0: making interface eth1 the new active one
[Mon Dec 19 14:30:05 2024] MCE: CPU0: Thermal monitoring enabled (TM1)
[Mon Dec 19 14:30:06 2024] EDAC sbridge MC0: HANDLING MCE MEMORY ERROR
[Mon Dec 19 14:30:06 2024] EDAC sbridge MC0: CPU#0_CHANNEL#0_DIMM#0 Unknown error: ADDR=0x00000000 EDAC agg=FATAL SERRORCNT=1 ERRCOUNT=1
```

!!! warning "Common errors"
    **`dmesg: read kernel buffer failed: Operation not permitted`** — Run the command with `sudo` or as root user
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


```text title="Expected output"
time->Thu Dec 19 10:34:22 2024
type=AVC msg=audit(1734607462.891:2847): avc:  denied  { read } for  pid=3421 comm="httpd" name="shadow" dev="dm-0" ino=1048592 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:shadow_t:s0 tclass=file permissive=0
type=AVC msg=audit(1734607463.102:2848): avc:  denied  { write } for  pid=5847 comm="nginx" name="access.log" dev="dm-0" ino=1048601 scontext=system_u:system_r:nginx_t:s0 tcontext=system_u:object_r:var_log_t:s0 tclass=file permissive=0

AVC Report
# total  type
2         denied
----

USER_AUTH Report
type=USER_AUTH msg=audit(1734607891.445:2849): pid=892 uid=0 auid=1001 ses=15 msg='op=PAM:authentication acct="admin" exe="/usr/sbin/sshd" hostname=192.168.1.50 addr=192.168.1.50 terminal=ssh res=failed'
type=USER_AUTH msg=audit(1734607902.556:2850): pid=893 uid=0 auid=4294967295 ses=4294967295 msg='op=PAM:authentication acct="root" exe="/usr/sbin/sshd" hostname=10.0.0.15 addr=10.0.0.15 terminal=ssh res=failed'

type=EXECVE msg=audit(1734608234.778:2851): argc=3 a0="/usr/bin/cat" a1="/etc/shadow" a2=(null) ppid=1234 pid=5678 auid=0 uid=0 gid=0 euid=0 egid=0 exe="/usr/bin/sudo"

Summary Report
Range of time in logs: 12/19/2024 00:00:00.000 - 12/19/2024 23:59:59.999
Total Events: 847
...

Failed Logins Report
# date             time     acct host
12/19/2024 10:15 admin    192.168.1.50
12/19/2024 10:22 root     10.0.0.15
12/19/2024 14:47 testuser 172.16.0.8
```

!!! warning "Common errors"
    **`No events found in logs.`** — Ensure auditd daemon is running with `systemctl start auditd` and audit rules are loaded with `auditctl -l`.
    **`ausearch: command not found`** — Install audit tools with `yum install audit` or `apt-get install auditd audispd-plugins`.
    **`Error: invalid start time`** — Use valid time formats like `--start today`, `--start recent`, or `--start 12/19/2024` instead of custom formats.
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


```text title="Expected output"
Nov 15 10:23:45 prod-web-01 sshd[2847]: Failed password for invalid user admin from 192.168.1.105 port 54321 ssh2
Nov 15 10:24:12 prod-web-01 sshd[2851]: Failed password for root from 203.0.113.42 port 45678 ssh2
Nov 15 10:25:33 prod-web-01 sshd[2856]: Failed password for invalid user test from 198.51.100.88 port 33221 ssh2
Nov 15 10:26:01 prod-web-01 sshd[2861]: Accepted password for jsmith from 10.0.2.15 port 22456 ssh2
Nov 15 10:26:45 prod-web-01 sshd[2865]: Accepted publickey for automation from 10.0.5.200 port 51234 ssh2
Nov 15 10:27:12 prod-web-01 sshd[2869]: Accepted password for mchen from 10.0.3.88 port 48901 ssh2
Nov 15 10:28:03 prod-web-01 sshd[2873]: Failed password for invalid user oracle from 203.0.113.99 port 39876 ssh2
Nov 15 10:29:15 prod-web-01 sshd[2878]: Accepted publickey for deploy from 10.0.6.45 port 52341 ssh2
Nov 15 10:30:22 prod-web-01 sshd[2882]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=203.0.113.55 user=root
Nov 15 10:31:44 prod-web-01 sshd[2887]: pam_faillock(sshd:auth): Consecutive login failures for user "jdoe" (3)
Nov 15 10:32:10 prod-web-01 sshd[2891]: account locked due to 5 failed logins
When /dev/null 2>&1 is reached:
User:                    jdoe
Failures:                5
Latest failure:          Nov 15 10:32:09 2024
Failure since last success: 5
Time interval:           1200
Attempts left before permanent lockout: 0
Nov 15 10:45:22 prod-web-01 sudo: jsmith : TTY=pts/0 ; PWD=/home/jsmith ; USER=root ; COMMAND=/bin/systemctl restart nginx
Nov 15 10:46:01 prod-web-01 sudo: mchen : TTY=pts/1 ; PWD=/var/log ; USER=root ; COMMAND=/usr/bin/tail -f /var/log/secure
Nov 15 10:47:33 prod-web-01 sudo: automation : TTY=unknown ; PWD=/opt/scripts ; USER=root ; COMMAND=/usr/local/bin/backup.sh
Nov 15 10:48:15 prod-web-01 su[3142]: (to root) jsmith on pts/0
Nov 15 10:
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


```text title="Expected output"
$ strace -p 4521
strace: attach: ptrace(PTRACE_SEIZE, 4521): Operation not permitted
$ strace -c -p 4521
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 45.23    0.156234          12     13045           epoll_wait
 23.18    0.080156           8      9876           read
 18.45    0.063789           7      8934           write
  8.92    0.030845           5      6123           futex
  4.22    0.014589           3      4567      102  recvfrom
------ ----------- ----------- --------- --------- ----------------
100.00    0.345613                 42545      102 total

$ strace -o /tmp/strace-out.txt /usr/bin/curl https://example.com
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1234  100  1234    0     0   5678      0 --:--:-- --:--:-- --:--:--     0

$ lsof -p 8934
COMMAND    PID USER   FD   TYPE             DEVICE SIZE/OFF       NODE NAME
nginx    8934 www-data cwd    DIR                8,1     4096    1048577 /var/www
nginx    8934 www-data rtd    DIR                8,1     4096          2 /
nginx    8934 www-data txt    REG                8,1   987654      65432 /usr/sbin/nginx
nginx    8934 www-data mem    REG                8,1  2097152      78901 /lib/x86_64-linux-gnu/libc.so.6
nginx    8934 www-data    0u   CHR                1,3      0t0       6045 /dev/null
nginx    8934 www-data    3u  IPv4           234567      0t0        TCP *:80 (LISTEN)
nginx    8934 www-data    4u  IPv4           234568      0t0        TCP *:443 (LISTEN)

$ ls /proc/8934/fd | wc -l
42

$ cat /proc/8934/status | grep -E "VmRSS|VmPeak|Threads"
VmPeak:	  456789 kB
VmRSS:	   234567 kB
Threads:	8

$ ps -eo pid,comm,stat,wchan | grep " D "
 2847 kworker/u8:2    D  io_schedule
 5634 java             D  wait_on_page_bit_killable
```

!!! warning "Common errors"
    **`strace: attach: ptrace(PTRACE_SEIZE, <PID>): Operation not permitted`** — Run strace with `sudo` or ensure the user has CAP_SYS_PTRACE capability.
    **`lsof: command not found`** — Install lsof with `apt-get install lsof` (Debian/Ubuntu) or `yum install lsof` (
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


```text title="Expected output"
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0      0 2847104 156832 3921456  0    0    12    45  1204  892 18  4 76  2  0
 1  0      0 2851920 156832 3925680  0    0     8    32  1089  756 16  3 79  2  0
 0  0      0 2856448 156832 3929104  0    0     4    18   987  654 14  2 82  2  0
 1  0      0 2854672 156832 3927328  0    0    14    52  1156  823 19  5 74  2  0
 0  0      0 2859216 156832 3931872  0    0     6    28  1021  712 15  3 80  2  0
 1  0      0 2852544 156832 3925200  0    0    11    41  1098  768 17  4 77  2  0
 0  0      0 2858880 156832 3930816  0    0     7    24   945  621 13  2 83  2  0
 1  0      0 2855104 156832 3927040  0    0    13    48  1167  841 20  5 73  2  0
 0  0      0 2860672 156832 3932528  0    0     5    19   876  589 12  1 85  2  0
 0  0      0 2857936 156832 3929792  0    0     9    35  1032  701 16  3 79  2  0

Linux 5.15.0-84-generic (prod-app-01) 	01/15/2025 	_x86_64_	(8 CPU)

12:34:56 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
12:34:57 PM     all     18.24      0.00      4.18      2.14      0.00     75.44
12:34:58 PM     all     16.87      0.00      3.92      1.98      0.00     77.23
12:34:59 PM     all     19.45      0.00      5.01      2.67      0.00     72.87
12:35:00 PM     all     17.56      0.00      4.34      2.11      0.00     76.00
12:35:01 PM     all     18.92      0.00      4.67      1.89      0.00     74.52

Linux 5.15.0-84-generic (prod-app-01) 	01/15/2025 	_x86_64_	(8 CPU)

Device            r/s     w/s     rMB/s     wMB/s   rrqm/s   wrqm/s  await svctm  %util
sda               8.2    12.4
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


```text title="Expected output"
Please enter your case number (or leave blank): 
Running plugins. This may take a while.

 Setting up archive ...
sosreport (version 4.4)

The following plugins are currently enabled:

 networking, storage, systemd

Running plugins. This may take a while.
[plugin:networking] collecting network interface status
[plugin:storage] collecting disk and filesystem information
[plugin:systemd] collecting systemd journal and unit files
Creating compressed archive...

Your sosreport has been generated and saved in:
  /var/tmp/sosreport-prod-web-01-20240215.tar.xz (287 MB)

tar: /var/log/messages: No such file or directory
tar: /var/log/secure: No such file or directory
/tmp/linux-diag-20240215.tar.gz

              total        used      available use%
Mem:           31Gi       18Gi         12Gi  59%
Swap:          4.0Gi      512Mi        3.5Gi  13%

Filesystem      Size  Used Avail Use%
/dev/sda1       100G   67G   28G  71%
/dev/sda2       500G  412G   75G  83%
```

!!! warning "Common errors"
    **`sosreport: command not found`** — Install sos package with `sudo yum install sos` on RHEL or `sudo apt install sosreport` on Ubuntu.
    **`tar: /var/log/messages: No such file or directory`** — Remove non-existent log paths from the tar command or add `2>/dev/null` to suppress warnings; the archive will still be created with available files.
    **`Permission denied`** — Run the entire diagnostic collection with `sudo` since many log files and /proc entries require root access.
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
