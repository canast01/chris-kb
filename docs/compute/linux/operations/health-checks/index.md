---
tags:
  - linux
  - operations
---
# Linux — Health Checks

<div class="kb-summary">
Routine checks, service validation, and status verification.

*Applies to: RHEL / Ubuntu LTS*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
cpu_and_load: "CPU and Load" {shape: rectangle}
memory: "Memory" {shape: rectangle}
disk: "Disk" {shape: rectangle}
network: "Network" {shape: rectangle}
services_and_systemd: "Services and Systemd" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> cpu_and_load
cpu_and_load -> memory
memory -> disk
disk -> network
network -> services_and_systemd
services_and_systemd -> generate_report
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these commands in sequence at the start of any health check or before making changes to a Linux server.

```bash
# 1. OS version and uptime
cat /etc/os-release && uptime

# 2. CPU and load average
top -bn1 | head -5
# Or use vmstat for a 3-sample view:
vmstat 1 3

# 3. Memory usage
free -h

# 4. Disk usage (exclude tmpfs mounts)
df -h --output=source,size,used,avail,pcent | grep -v tmpfs

# 5. Filesystem errors in kernel ring buffer
dmesg | grep -i "error\|fail\|fault" | tail -20

# 6. Failed systemd services
systemctl --failed

# 7. Network interface status and routing
ip addr show && ip route show

# 8. Recent login failures
grep "Failed password" /var/log/secure | tail -10
# Ubuntu/Debian:
# grep "Failed password" /var/log/auth.log | tail -10

# 9. Open listening ports
ss -tlnp

# 10. Pending security updates
yum check-update --security 2>/dev/null | wc -l
# Ubuntu/Debian:
# apt list --upgradable 2>/dev/null | wc -l
```


```text title="Expected output"
NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
 10:42:15 up 127 days, 3:15, 2 users, load average: 0.87, 0.92, 0.88

top - 10:42:15 up 127 days,  3:15,  2 users,  load average: 0.87, 0.92, 0.88
Tasks: 156 total,   1 running, 155 sleeping,   0 stopped,   0 zombie
%Cpu(s):  8.3 us,  2.1 sy,  0.0 ni, 89.2 id,  0.4 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 16384512 total,  2847296 free,  9156224 used,  4380992 buff/cache

procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0 102400 2847296 512000 4380992  0    0    12    45  287  521  8  2 89  1  0
 0  0 102400 2851200 512000 4380992  0    0     8    32  281  518  7  2 90  1  0
 0  0 102400 2855104 512000 4380992  0    0     6    28  275  512  6  2 91  1  0

              total        used        free      shared  buff/cache   available
Mem:            15Gi       8.7Gi       2.7Gi       512Mi       3.6Gi       5.2Gi
Swap:          2.0Gi       100Mi       1.9Gi

SOURCE                SIZE  USED AVAIL PCENT
/dev/mapper/cl-root    50G   38G   12G   76%
/dev/sda1            1014M  287M  727M   29%
/dev/mapper/cl-home   100G   67G   33G   67%

[    0.234521] EXT4-fs (dm-0): mounted filesystem with ordered data mode
[  127.456789] audit: type=1130 audit(1642345200.123:4567): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=systemd-tmpfiles-setup-dev comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'

Unit httpd.service entered failed state.
Unit mariadb.service entered failed state.

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```
## CPU and Load

```bash
# Current CPU usage snapshot
top -b -n1 | head -20

# Load average vs. CPU count — load > nCPUs = saturated
nproc
uptime   # 1m 5m 15m averages

# Per-CPU breakdown
mpstat -P ALL 1 3

# Top CPU-consuming processes
ps aux --sort=-%cpu | head -15
```


```text title="Expected output"
top - 14:32:18 up 8 days,  3:21,  2 users,  load average: 2.14, 1.87, 1.62
Tasks: 247 total,   3 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s):  18.2 us,  4.1 sy,  0.0 ni, 77.1 id,  0.4 wa,  0.1 hi,  0.1 si,  0.0 st
MiB Mem :  15987.4 total,  3421.2 free,  8156.8 used,  4409.4 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   7245.6 avail Mem

    PID USER      PR  NI    VIRT    RES  SHR S  %CPU  %MEM     TIME+ COMMAND
  4821 appuser   20   0 2847316 1.2g  45m S  42.3  7.8   1247:33 java
  8934 postgres  20   0  892456 521m  18m S  12.1  3.2    456:12 postgres
  1247 root      20   0  445123 234m  12m S   8.7  1.5    123:45 kubelet
  5612 nginx     20   0  234567  89m   8m S   3.2  0.6     67:23 nginx
  2891 syslog    20   0  156789  45m   3m S   1.1  0.3     34:12 rsyslogd

8
 14:32:18 up 8 days,  3:21,  2 users,  load average: 2.14, 1.87, 1.62
Linux 5.15.0-84-generic (prod-app-01) 	01/17/2025 	_x86_64_	(8 CPU)

Average:     CPU    %usr    %nice    %sys %iowait    %irq   %soft  %steal    %idle
Average:       0   19.34    0.00    4.12    0.23    0.11    0.08    0.00   76.12
Average:       1   21.45    0.00    5.23    0.18    0.09    0.06    0.00   73.00
Average:       2   15.67    0.00    3.89    0.31    0.12    0.10    0.00   80.01
Average:       3   18.92    0.00    4.45    0.19    0.10    0.07    0.00   76.27
Average:       4   17.23    0.00    3.67    0.25    0.08    0.09    0.00   78.68
Average:       5   20.11    0.00    4.78    0.22    0.11    0.08    0.00   74.70
Average:       6   16.89    0.00    3.92    0.28    0.09    0.06    0
```
## Memory

```bash
# Summary
free -h

# Detailed breakdown
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree|Cached|Buffers"

# Top memory-consuming processes
ps aux --sort=-%mem | head -15

# OOM kill events
journalctl -k --since "1 hour ago" | grep -i "oom\|killed process"
dmesg | grep -i "out of memory" | tail -10
```


```text title="Expected output"
total        used        free      shared  buff/cache   available
Mem:           31Gi       18Gi       8.2Gi       512Mi        4.8Gi       12Gi
Swap:          8.0Gi      2.1Gi       5.9Gi

MemTotal:       32768000 kB
MemFree:        8589934 kB
MemAvailable:   12884901 kB
SwapTotal:      8388608 kB
SwapFree:       6291456 kB
Cached:         3145728 kB
Buffers:        1048576 kB

USER       PID %CPU %MEM    VSZ      RSS COMMAND
root      2847  8.3 12.4 2847392 4096000 /usr/bin/java -Xmx8g -jar app.jar
postgres  1523  2.1  8.7 1953284 2867456 postgres: writer
www-data  3421  1.9  6.2 1524288 2048576 /usr/bin/python3 worker.py
root      1245  0.4  3.1  892384  1024000 /opt/monitoring/agent
mysql     1089  0.2  2.8  756288  921600 mysqld
root      4012  0.1  1.5  512000  491520 sshd: root@pts/0
...

Dec 15 14:32:18 prod-app-01 kernel: [12847.293847] Out of memory: Kill process 2847 (java) score 523 or sacrifice child
Dec 15 14:32:19 prod-app-01 kernel: [12848.102938] Killed process 2847 (java) total-vm:2847392kB, anon-rss:4096000kB, file-rss:0kB, shmem-rss:0kB, UID:0 pgtid:2847 OOM killer terminated process
Dec 15 13:45:02 prod-app-01 kernel: [8934.582104] Out of memory: Kill process 1523 (postgres) score 412 or sacrifice child
```

!!! warning "Common errors"
    **`grep: (standard input): No such file or directory`** — Ensure `/proc/meminfo` exists and is readable; this error typically indicates a permission issue or non-Linux system.
    **`journalctl: command not found`** — Install systemd or use `dmesg` alone if the system doesn't use journalctl for kernel logging.
    **`ps: command not found`** — Verify `procps` or `procps-ng` package is installed on the system.
## Disk

```bash
# Filesystem usage — flag anything above 80%
df -h | awk 'NR==1 || $5+0 > 80'

# Inode usage (can fill independently of space)
df -i | awk 'NR==1 || $5+0 > 80'

# I/O stats per device
iostat -xz 1 3

# Disk errors in kernel ring buffer
dmesg | grep -iE "error|failed|reset|timeout" | grep -iE "sd[a-z]|nvme|dm-" | tail -20

# Large files consuming unexpected space
du -sh /var/log/* 2>/dev/null | sort -h | tail -10
du -sh /tmp/* 2>/dev/null | sort -h | tail -10
```


```text title="Expected output"
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   42G  5.2G  85% /
/dev/sdb1      200G  165G   28G  83% /data

Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/sda1     3276800 2891456 385344   88% /
/dev/sdb1    13107200 9437184 3670016  72% /data

Linux 5.15.0-91-generic (prod-web-04) 	01/17/2025 	_x86_64_	(16 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           18.42    0.00   12.56   8.34    0.12   60.56

Device            r/s     w/s     rMB/s     wMB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz %util
sda             142.33  287.91     4.21     11.47    12.4    45.2   8.0   13.5   3.2    18.7   2.1   42.1
sdb              89.12  156.44     2.89      8.12     5.1    22.3   5.4   12.5   2.8    22.1   1.8   31.5

[Tue Jan 17 10:42:18 2025] sd 2:0:0:0: [sda] Assuming drive cache: write through
[Tue Jan 17 11:03:45 2025] sd 3:0:1:0: [sdb] FAILED: Result: hostbyte=DID_ERROR driverbyte=DRIVER_OK
[Tue Jan 17 11:15:22 2025] nvme0n1: I/O error, dev nvme0n1, sector 2048576 op 0x1:(WRITE) flags 0x0 phys_seg 1 prio class 0

1.2G	/var/log/syslog
856M	/var/log/audit/audit.log
412M	/var/log/apache2/access.log
287M	/var/log/apache2/error.log
156M	/var/log/mysql/slow.log

512M	/tmp/backup_20250117.tar.gz
284M	/tmp/cache_dump.bin
```

!!! warning "Common errors"
    **`awk: syntax error at source line 1`** — Ensure awk is installed and the script uses proper syntax; try `awk 'NR==1 || ($5+0) > 80'` with explicit parentheses.
    **`iostat: command not found`** — Install sysstat package with `apt-get install sysstat` or `yum install sysstat`.
    **`du: Permission denied`** — Run with `sudo du -sh /var/log/* 2>/dev/null` or adjust directory permissions for the executing user.
## Network

```bash
# Interface status and IPs
ip -br addr

# Active listening ports
ss -tulnp

# Interface errors and drops
ip -s link show | grep -A 5 "errors\|dropped"

# Connection counts
ss -s

# Recent network-related kernel events
dmesg | grep -iE "link is down|link is up|reset adapter|carrier" | tail -10
```


```text title="Expected output"
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             192.168.1.45/24 fe80::a00:27ff:fe4e:66a1/64
eth1             UP             10.0.0.12/24 fe80::a00:27ff:fe4e:66a2/64
docker0          UP             172.17.0.1/16

Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
tcp   LISTEN 0      128    0.0.0.0:22          0.0.0.0:*        users:(("sshd",pid=1247,fd=3))
tcp   LISTEN 0      100    127.0.0.1:25        0.0.0.0:*        users:(("master",pid=2156,fd=13))
tcp   LISTEN 0      128    [::]:22             [::]:*           users:(("sshd",pid=1247,fd=4))
udp   UNCONN 0      0      0.0.0.0:68          0.0.0.0:*        users:(("dhclient",pid=891,fd=6))

RX: bytes packets errors dropped overrun mcast
    4521847 12456  0      2      0      0
TX: bytes packets errors dropped overrun mcast
    3891234 10234  0      0      0      0

Total: TCP sockets: 47 (estab 12, closed 0, orphaned 0, synrecv 0, timewait 2, tw 2)
       UDP sockets: 8
       INET: inuse 55 orphan 0 tw 2 alloc 57
       FRAG: inuse 0 memory 0

[  156.234521] e1000: eth0 NIC Link is Up 1000 Mbps Full Duplex
[  234.891234] systemd-udevd[445]: renamed network interface eth1 to eth1
[  512.456789] e1000: eth0 NIC Link is Down
[  513.123456] e1000: eth0 NIC Link is Up 1000 Mbps Full Duplex
```

!!! warning "Common errors"
    **`Cannot open netlink socket: Permission denied`** — Run the commands with `sudo` or as root user.
    **`ss: No such file or service`** — Install the iproute2 package with `apt install iproute2` (Debian/Ubuntu) or `yum install iproute2` (RHEL/CentOS).
## Services and Systemd

```bash
# Failed units — should return 0
systemctl --failed

# Check a specific service
systemctl status <service-name>

# Service restart history
journalctl -u <service-name> | grep -i "start\|stop\|fail" | tail -20

# Services that have restarted unexpectedly
journalctl --since "24 hours ago" | grep "Start request repeated" | tail -10
```


```text title="Expected output"
0 loaded units listed.
● nginx.service - The NGINX HTTP and Web Server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
     Active: active (running) since Wed 2024-01-10 14:32:18 UTC; 2 days ago
       Docs: http://nginx.org/en/docs/
    Process: 8472 ExecStart=/usr/sbin/nginx -g daemon off; (code=exited, status=0/SUCCESS)
   Main PID: 8473 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 12.4M
        CPU: 2min 34.821s
     CGroup: /system.slice/nginx.service
             ├─8473 nginx: master process /usr/sbin/nginx -g daemon off;
             └─8474 nginx: worker process
Jan 10 14:32:18 prod-web-01 systemd[1]: Started The NGINX HTTP and Web Server.
Jan 10 14:32:19 prod-web-01 nginx[8472]: 2024/01/10 14:32:19 [notice] 8472#8472: signal process started
Jan 10 14:35:42 prod-web-01 systemd[1]: Stopped The NGINX HTTP and Web Server.
Jan 10 14:35:43 prod-web-01 systemd[1]: Started The NGINX HTTP and Web Server.
Jan 09 08:12:05 prod-web-01 systemd[1]: nginx.service: Start request repeated too quickly (2 times in 10s).
Jan 08 22:18:33 prod-web-01 systemd[1]: nginx.service: Start request repeated too quickly (3 times in 10s).
```

!!! warning "Common errors"
    **`Unit <service-name> could not be found.`** — Verify the service name with `systemctl list-units --type=service` and use the correct name without the `.service` suffix.
    **`Failed to get properties: Connection refused`** — Ensure systemd is running with `systemctl status` and check that you have sufficient permissions (use `sudo` if needed).
    **`journalctl: No entries found in specified time range.`** — Adjust the time range with `--since "48 hours ago"` or remove the filter to check all available logs.
## System Logs — Quick Errors

```bash
# All errors from the last hour
journalctl -p err --since "1 hour ago"

# Kernel warnings and errors
dmesg --level=err,warn | tail -30

# Auth failures
journalctl _SYSTEMD_UNIT=sshd.service | grep "Failed\|Invalid" | tail -20
```


```text title="Expected output"
-- Logs begin at Mon 2024-01-15 09:23:44 UTC, end at Mon 2024-01-15 14:47:12 UTC. --
Jan 15 14:32:18 prod-web-03 kernel: audit: type=1130 audit(1705334538.921:4521): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=systemd-tmpfiles-clean comm="systemd" exe="/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Jan 15 14:15:44 prod-web-03 systemd[1]: Failed to start Daily apt download activities.
Jan 15 14:02:33 prod-web-03 kernel: Out of memory: Kill process 2847 (java) score 512 or sacrifice child
Jan 15 13:58:12 prod-web-03 sudo: pam_unix(sudo:auth): authentication failure; logname=ubuntu uid=1001 euid=0 tty=pts/0 ruser=ubuntu rhost=10.42.18.5 user=root
Jan 15 13:45:09 prod-web-03 systemd[1]: systemd-journald.service: Main process exited, code=exited, status=1/FAILURE

[kernel output]
[14254.332891] audit: type=1130 audit(1705334538.921:4521): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=systemd-tmpfiles-clean'
[14287.445123] WARNING: CPU0: Package temperature/speed normal
[14301.667834] EXT4-fs warning (device sda1): ext4_dx_add_entry:2147: Directory index full!
[14512.891234] systemd[1]: Failed to start Daily apt download activities.
[14623.445678] kernel: Out of memory: Kill process 2847 (java) score 512 or sacrifice child
[14701.223445] audit: type=1400 audit(1705335661.445:4589): apparmor="DENIED" operation="capable" profile="unconfined" pid=3421 comm="curl" capability=36 capname="block_suspend"

Jan 15 14:32:18 prod-web-03 sshd[4521]: Failed password for invalid user admin from 203.0.113.42 port 54321 ssh2
Jan 15 14:28:55 prod-web-03 sshd[4412]: Invalid user testuser from 198.51.100.88 port 49876 ssh2
Jan 15 14:15:33 prod-web-03 sshd[4298]: Failed password for root from 192.0.2.15 port 38945 ssh2
Jan 15 14:01:22 prod-web-03 sshd[4187]: Invalid user oracle from 203.0.113.99 port 44321 ssh2
Jan 15 13:47:09 prod-web-03 sshd[4076]: Failed password for ubuntu from 198.51.100.44 port 39234 ssh2
```

!!! warning "Common errors"
    **
## NTP / Time Sync

```bash
# Check sync status
timedatectl status

# chrony detail (RHEL)
chronyc tracking
chronyc sources -v

# Flag offset > 1 second
chronyc tracking | grep "System time"
```


```text title="Expected output"
Local time: Wed 2024-01-17 14:32:45 UTC
           Universal time: Wed 2024-01-17 14:32:45 UTC
                 RTC time: Wed 2024-01-17 14:32:45
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
           RTC in local TZ: no

Reference ID    : 91F20D01 (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Wed Jan 17 14:32:40 2024
System time     : 0.000234567 seconds fast of NTP time
Frequency       : 2.341 ppm fast
Residual freq   : +0.002 ppm
Residual skew   : 0.123 ppm
Root delay      : 0.031250 seconds
Root dispersion : 0.046387 seconds
Max error       : 0.054621 seconds
Min error       : 0.000234 seconds
Leap status     : Normal

MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================
^* ntp1.example.com              1  64  377   32   -234us[ -234us] +/-   15ms
^+ ntp2.example.com              1  64  377   45   +156us[ +156us] +/-   18ms
^- ntp3.example.com              2  64  377   61   +892us[ +892us] +/-   22ms
^? ntp4.example.com              0  64   0     -     +0ns[   +0ns] +/-    0ns

System time     : 0.000234567 seconds fast of NTP time
```

!!! warning "Common errors"
    **`chronyc: command not found`** — Install chrony with `sudo yum install chrony` (RHEL) or `sudo apt install chrony` (Debian), then start the service with `sudo systemctl start chronyd`.
    **`System time     : 1.234567 seconds fast of NTP time`** — Offset exceeds 1 second; run `sudo chronyc makestep` to force immediate clock correction, then verify with `timedatectl status`.
    **`Leap status     : Leap second pending`** — A leap second adjustment is scheduled; this is normal and will resolve automatically at the designated UTC time.
## Security Posture

```bash
# SELinux status (RHEL)
getenforce
sestatus | grep -E "mode|status"

# AppArmor status (Ubuntu)
aa-status 2>/dev/null | head -5

# Locked or expired accounts
passwd -S -a 2>/dev/null | grep -E " L | P " | head -20

# Sudo configuration
visudo -c   # Syntax check, no changes
```


```text title="Expected output"
Enforcing
SELinux status:   enabled
Current mode:                 enforcing
Mode from config file:        enforcing
apparmor module is loaded.
 13 profiles are loaded.
root           P 01/15/2025 0 99999 7 -1
daemon         L 01/10/2025 0 99999 7 -1
sync           L 01/10/2025 0 99999 7 -1
grammar check successful
```

!!! warning "Common errors"
    **`getenforce: command not found`** — Install SELinux utilities with `yum install policycoreutils-python-utils` on RHEL systems.
    **`aa-status: command not found`** — Install AppArmor tools with `apt-get install apparmor-utils` on Ubuntu systems.
    **`>>> /etc/sudoers: syntax error near line 42`** — Fix the syntax error in `/etc/sudoers` using `visudo` editor directly and review the flagged line.
## Health Check Summary Table

| Check | Command | Healthy |
|---|---|---|
| Load vs CPU count | `uptime` + `nproc` | load ≤ nCPU |
| Memory available | `free -h` | Available > 20% |
| No FS > 85% | `df -h` | All < 85% |
| No inode FS > 85% | `df -i` | All < 85% |
| No failed services | `systemctl --failed` | 0 failed |
| NTP synchronised | `timedatectl` | Synchronised: yes |
| No interface errors | `ip -s link` | TX/RX errors = 0 |
| No kernel errors | `dmesg --level=err` | None recent |
| SELinux enforcing | `getenforce` | Enforcing |

## Log Pipeline

## Log Locations

| Log | Path / Command | Content |
|---|---|---|
| System journal | `journalctl` | All systemd units, kernel, boot |
| Kernel messages | `dmesg` / `journalctl -k` | Hardware, driver events |
| Auth / SSH | `journalctl _SYSTEMD_UNIT=sshd.service` | Login, sudo, SSH |
| Audit | `/var/log/audit/audit.log` | SELinux denials, syscall auditing |
| Application | `/var/log/<app>/` or `journalctl -u <svc>` | Per-service |
| cron | `/var/log/cron` (RHEL) / `journalctl -u cron` | Scheduled job output |
| Boot log | `journalctl -b` | Full boot sequence |
| DNF/YUM history | `/var/log/dnf.log` + `dnf history` | Package installs/removals (RHEL) |
| APT history | `/var/log/apt/history.log` | Package changes (Ubuntu) |

## journalctl — Common Queries

```bash
# Errors and above — last hour
journalctl -p err --since "1 hour ago"

# Follow a service in real time
journalctl -u nginx.service -f

# Messages since last boot
journalctl -b

# Previous boot (for crashed systems)
journalctl -b -1

# Between timestamps
journalctl --since "2026-05-01 08:00:00" --until "2026-05-01 09:00:00"

# By PID
journalctl _PID=1234

# Kernel messages only
journalctl -k

# Output as JSON (for parsing)
journalctl -u myservice -o json | jq '.MESSAGE'

# Export for TAC/vendor
journalctl --since "yesterday" > /tmp/journal-export.txt
```


```text title="Expected output"
-- Logs begin at Wed 2026-04-29 14:22:17 UTC, end at Wed 2026-04-29 15:18:43 UTC. --
Apr 29 15:12:34 prod-web-01 kernel: Out of memory: Kill process 2847 (java) score 512 or sacrifice child
Apr 29 15:13:02 prod-web-01 systemd: nginx.service: Main process exited, code=exited, status=1/FAILURE
Apr 29 15:14:18 prod-web-01 sudo: pam_unix(sudo:auth): authentication failure; logname=admin uid=1002 euid=0
Apr 29 15:16:55 prod-web-01 kernel: audit: type=1130 audit(1714425415.892:847): pid=1 uid=0 auid=4294967295 ses=4294967295
Apr 29 15:17:41 prod-web-01 systemd: Failed to start PostgreSQL Database Server.

-- Logs begin at Wed 2026-04-29 14:22:17 UTC, end at Wed 2026-04-29 15:18:43 UTC. --
Apr 29 15:18:12 prod-web-01 nginx[8934]: 192.168.1.45 - - [29/Apr/2026:15:18:12 +0000] "GET /health HTTP/1.1" 200 145 "-" "curl/7.68.0"
Apr 29 15:18:18 prod-web-01 nginx[8934]: 10.0.2.18 - - [29/Apr/2026:15:18:18 +0000] "POST /api/v1/users HTTP/1.1" 201 892 "-" "python-requests/2.28.1"
Apr 29 15:18:23 prod-web-01 nginx[8934]: 192.168.1.50 - - [29/Apr/2026:15:18:23 +0000] "GET /static/app.js HTTP/1.1" 304 0 "-" "Mozilla/5.0"
Apr 29 15:18:29 prod-web-01 nginx[8934]: 10.0.2.22 - - [29/Apr/2026:15:18:29 +0000] "DELETE /api/v1/sessions/abc123 HTTP/1.1" 204 0 "-" "curl/7.68.0"

-- Logs begin at Wed 2026-04-29 14:22:17 UTC, end at Wed 2026-04-29 15:18:43 UTC. --
Apr 29 14:22:18 prod-web-01 systemd: Started Session c1 of user root.
Apr 29 14:22:19 prod-web-01 kernel: Linux version 5.15.0-94-generic (buildd@lgw02-amd64-060) (gcc-11 (Ubuntu 11.4.0-1ubuntu1~22.04.1) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38)
Apr 29 14:22:20
```
## dmesg — Kernel Ring Buffer

```bash
# Errors and warnings
dmesg --level=err,warn

# Watch in real time
dmesg -w

# Hardware errors (memory, disk, network)
dmesg | grep -iE "error|fail|reset|timeout|uncorrect" | tail -30

# Disk I/O errors
dmesg | grep -iE "sd[a-z]|nvme|blk_update_request|I/O error"

# OOM events
dmesg | grep -i "oom\|killed process\|out of memory"
```


```text title="Expected output"
[    0.000000] Linux version 5.15.0-86-generic (buildd@lgw02-amd64-060) (gcc-11 (Ubuntu 11.4.0-1ubuntu1~22.04.1) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #93-Ubuntu SMP Fri Oct 20 15:10:22 UTC 2023 (Ubuntu 5.15.0-86.96-generic 5.15.131)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-86-generic root=UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890 ro quiet splash
[    1.234567] WARNING: CPU0: Core temperature/speed normal
[    2.456789] EXT4-fs warning (device sda1): ext4_validate_block_bitmap:383: bg 0: block bitmap does not match checksum
[    3.567890] audit: type=1400 audit(1698765432.123:45): apparmor="STATUS" operation="profile_load" name="man_filter" name2="default" pid=1234 comm="apparmor_parser"
[    4.678901] systemd[1]: Started User Manager for UID 1000.
[    5.789012] WARNING: CPU1: Package temperature/speed normal
[    6.890123] audit: type=1130 audit(1698765433.456:46): pid=5678 uid=0 auid=4294967295 ses=4294967295 msg='unit=systemd-tmpfiles-clean comm="systemd" exe="/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'

dmesg: read 1048576 bytes of kernel log buffer
```

!!! warning "Common errors"
    **`dmesg: read buffer failed: Operation not permitted`** — Run the command with `sudo` or as root user.
    **`dmesg: invalid log level 'err,warn'`** — Use `dmesg --level=err --level=warn` or upgrade to a newer kernel version that supports comma-separated levels.
## Audit Log (auditd)

```bash
# SELinux denials
ausearch -m avc --start recent

# Failed logins
ausearch -m USER_AUTH --success no --start today

# Changes to sensitive files
ausearch -f /etc/passwd
ausearch -f /etc/sudoers

# Commands run via sudo
ausearch -ua root --start today | grep EXECVE

# Summary report
aureport --summary
aureport --login --failed
```


```text title="Expected output"
time->Wed Dec 13 10:45:22 2024
type=AVC msg=audit(1702475122.445:8934): avc:  denied  { read } for  pid=2847 comm="httpd" name="shadow" dev="dm-0" ino=1048592 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:shadow_t:s0 tclass=file permissive=0

time->Wed Dec 13 10:32:15 2024
type=USER_AUTH msg=audit(1702474335.221:8901): pid=1456 uid=1000 auid=1000 ses=42 msg='op=PAM:authentication acct="testuser" exe="/usr/sbin/sshd" hostname=client.example.com addr=192.168.1.105 terminal=ssh res=failed'

time->Wed Dec 13 09:18:44 2024
type=EXECVE msg=audit(1702470324.556:8876): argc=3 a0="/usr/bin/passwd" a1="jsmith" a2="--stdin"

time->Wed Dec 13 08:55:12 2024
type=EXECVE msg=audit(1702468512.889:8845): argc=2 a0="/usr/sbin/usermod" a1="-G"

Summary Report
======================
Total Events Audited: 14,287
Range of Events: 12/13/2024 - 12/13/2024
Events processed: 14,287
Requests realtime data: no

Failed Login Summary
=====================
Total Failed Logins: 3
Failed Login Sources
root                 0
testuser             2
admin                1
```

!!! warning "Common errors"
    **`ausearch: no matches found`** — Verify the audit daemon is running with `systemctl status auditd` and that audit rules are loaded with `auditctl -l`.
    **`Error opening config file (/etc/audit/audit.rules): Permission denied`** — Run ausearch and aureport commands with `sudo` or as root user.
    **`audit: type=1130 audit(1702475122.445:8934): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='audit: rate limit exceeded'`** — Increase the audit buffer size in `/etc/audit/audit.rules` with `buffer_size = 8192` and reload with `service auditd restart`.
## Remote Log Forwarding (rsyslog)

```bash
# /etc/rsyslog.d/90-remote.conf — forward all logs via TCP to centralised syslog
*.* action(type="omfwd"
    target="syslog.example.local"
    port="514"
    protocol="tcp")

# Restart rsyslog
systemctl restart rsyslog

# Verify TCP connection to syslog server
ss -tnp | grep :514
```


```text title="Expected output"
tcp    ESTABLISHED 0      0      192.168.10.45:52847      203.0.113.22:514    users:(("rsyslogd",pid=2847,fd=3))
tcp    LISTEN      0      128    0.0.0.0:514              0.0.0.0:*
```

!!! warning "Common errors"
    **`Job for rsyslog.service failed because the control process exited with error code.`** — Check `/var/log/rsyslog.log` for syntax errors in the config file (missing quotes, brackets, or invalid action parameters).
    **`Name or service not known`** — Verify the hostname `syslog.example.local` resolves correctly with `nslookup syslog.example.local` or update `/etc/hosts` with the correct IP address.
    **`Connection refused`** — Confirm the remote syslog server is listening on port 514 with `ss -tnlp` on the syslog server and check firewall rules allow outbound TCP 514.
## Journal Size Management

```bash
# Check journal disk usage
journalctl --disk-usage

# Vacuum to keep last 7 days
journalctl --vacuum-time=7d

# Vacuum to size limit
journalctl --vacuum-size=500M

# Persistent journal size cap in /etc/systemd/journald.conf:
# SystemMaxUse=2G
systemctl restart systemd-journald
```


```text title="Expected output"
Journals take up 1.2G on disk.
Vacuumed journals to 7 days old (removed 450M).
Vacuumed journals to 500M.
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to vacuum journal: Permission denied`** — Run the journalctl and systemctl commands with `sudo`.
    **`Failed to parse config file '/etc/systemd/journald.conf': Invalid argument`** — Check the SystemMaxUse syntax in journald.conf; ensure it uses valid units like `2G`, `1024M`, or `512K`.
---

## CPU Health

Commands to assess CPU utilisation and identify processes causing high load.

```bash
# Load average vs. CPU count — load > nCPUs indicates saturation
nproc
uptime

# Snapshot of CPU usage by process
top -bn1 | head -20

# Per-CPU utilisation over 3 samples
mpstat -P ALL 1 3

# Top CPU-consuming processes
ps aux --sort=-%cpu | head -15

# Processor interrupt and context-switch rates
vmstat 1 5
```


```text title="Expected output"
8
 10:47:23 up 14 days, 3:22,  2 users,  load average: 2.14, 1.89, 1.76
top - 10:47:23 up 14 days,  3:22,  2 users,  load average: 2.14, 1.89, 1.76
Tasks: 247 total,   3 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s):  18.2 us,  4.1 sy,  0.0 ni, 77.1 id,  0.4 wa,  0.1 hi,  0.1 si,  0.0 st
MiB Mem :  32014.5 total,  8421.3 free,  14562.1 used,  9031.1 buff/cache
MiB Swap:   4096.0 total,   4096.0 free,      0.0 used.  16891.2 avail Mem
    PID USER      PR  NI    VIRT    RES  SHR S  %CPU %MEM     TIME+ COMMAND
  14782 appuser   20   0 2847364 1.2g 142m S  24.5 3.9   45:12.88 java
  18934 postgres  20   0  892456 521m  48m S  12.3 1.6   28:44.21 postgres
   2156 root      20   0  156248  18m   8m S   8.7 0.1    3:21.15 sshd
   1847 root      20   0  245632  42m  12m S   4.2 0.1    1:09.44 systemd-journal
Linux 5.15.0-91-generic (prod-app-01) 	10/18/2024 	_x86_64_	(8 CPU)
Average:     CPU    %usr   %nice    %sys %iowait   %irq  %soft  %steal  %guest  %gnice
Average:       0   19.34    0.00    4.12    0.89   0.01   0.23    0.00    0.00    0.00
Average:       1   21.45    0.00    3.87    1.02   0.02   0.19    0.00    0.00    0.00
Average:       2   17.89    0.00    4.34    0.76   0.00   0.31    0.00    0.00    0.00
Average:       3   18.12    0.00    4.01    0.95   0.01   0.25    0.00    0.00    0.00
Average:     CPU    %usr   %nice    %sys %iowait   %irq  %soft  %steal  %guest  %gnice
Average:   all   19.20    0.00    4.09    0.91   0.01   0.25    0.00    0.00    0.00
USER       PID %CPU %MEM    VSZ   RSS CMD
appuser  14782 24.5  3.9 2847364 1265408
```
What to look for:
- Load average 1-minute value consistently above `nproc` output indicates CPU saturation.
- `%iowait` above 20% in `mpstat` output suggests disk I/O is blocking CPU.
- Single-core pinned at 100% may indicate a runaway process or missing multi-threading.
- `%steal` above 5% on VMs indicates the hypervisor is overcommitting CPU resources.

---

## Memory Health

Commands to assess memory availability and detect Out-of-Memory (OOM) events.

```bash
# Summary: total / used / free / available
free -h

# Detailed breakdown from kernel
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree|Cached|Buffers"

# Top memory-consuming processes
ps aux --sort=-%mem | head -15

# OOM kill events
journalctl -k --since "24 hours ago" | grep -i "oom\|killed process\|out of memory"
dmesg | grep -i "out of memory" | tail -10

# Swap usage — high swap usage with low available RAM = memory pressure
swapon --show
```


```text title="Expected output"
total        used        free      shared  buff/cache   available
Mem:           31Gi       18Gi       2.1Gi       512Mi        10Gi       12Gi
Swap:          8.0Gi      1.2Gi       6.8Gi

MemTotal:       32768000 kB
MemFree:         2211840 kB
MemAvailable:   12582912 kB
SwapTotal:       8388608 kB
SwapFree:        7127040 kB
Cached:          8912384 kB
Buffers:         1048576 kB

USER       PID %CPU %MEM    VSZ   RSS COMMAND
root      2847 12.3 22.1 4521280 7340156 java -Xmx8g -jar application.jar
postgres  1523  8.7 18.9 2891456 6291456 postgres: writer
www-data  3102  3.2  9.4 1024512 3145728 python3 /opt/app/server.py
root      1024  2.1  5.3  512000 1757184 /usr/sbin/mysqld
root       892  1.8  3.2  256000 1048576 /usr/bin/redis-server
root      4521  0.9  2.1  128000  696320 node /srv/api/index.js
...

Nov 18 14:32:15 prod-db-01 kernel: [2847.123456] Out of memory: Kill process 2847 (java) score 892 or sacrifice child
Nov 18 14:32:16 prod-db-01 kernel: [2847.234567] Killed process 2847 (java) total-vm:4521280kB, anon-rss:7340156kB, file-rss:0kB, shmem-rss:0kB, UID:0 pgtables:18432kB oom_score_adj:0

NAME      TYPE SIZE USED PRIO
/dev/sda3 partition 8.0G 1.2G   -2
```

!!! warning "Common errors"
    **`journalctl: command not found`** — Install systemd-journal or use `dmesg` alone on systems without journalctl.
    **`cat: /proc/meminfo: No such file or directory`** — This file is only available on Linux; confirm the system is Linux-based.
    **`swapon: command not found`** — Install the util-linux package or use `cat /proc/swaps` as an alternative.
What to look for:
- `MemAvailable` below 10% of `MemTotal` indicates memory pressure.
- Any OOM kill events in `dmesg` require immediate investigation — a process was terminated by the kernel.
- Swap usage above 20% of swap total on a system with low available RAM indicates the system is swapping heavily.
- Large `Cached` value is normal and healthy — Linux uses free memory as page cache.

---

## Disk and Filesystem Health

Commands to assess filesystem usage, I/O performance, and detect disk errors.

```bash
# Filesystem usage — flag anything above 85%
df -h | awk 'NR==1 || $5+0 > 80'

# Inode usage — can fill independently of block usage
df -i | awk 'NR==1 || $5+0 > 80'

# I/O statistics — await (ms) and utilisation per device
iostat -xz 1 3

# Disk errors in kernel ring buffer
dmesg | grep -iE "error|failed|reset|timeout|I/O error" | grep -iE "sd[a-z]|nvme|dm-" | tail -20

# Large files or directories consuming unexpected space
du -sh /var/log/* 2>/dev/null | sort -h | tail -10
du -sh /tmp/* 2>/dev/null | sort -h | tail -10
```


```text title="Expected output"
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   43G  4.2G  87% /
/dev/sda2      200G  156G   35G  82% /home
/dev/sdb1      500G  425G   62G  86% /data

Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/sda1     3276800 2891456 385344   88% /
/dev/sda2     13107200 9437184 3670016  72% /home

Linux 5.15.0-91-generic (prod-db-01) 	01/22/2025 	_x86_64_	(16 CPU)

Device            r/s     w/s     rMB/s     wMB/s   rrqm/s   wrqm/s  await svctm  %util
sda             142.3   87.6      8.2      12.4     12.1     34.2   18.4   2.1  47.3
sdb              89.1   156.2     5.1      24.7      8.3     28.9   22.7   1.8  43.9
nvme0n1         312.4   203.1     18.6     31.2     0.0      0.0   12.1   0.9  51.6

[12847.234521] sd 2:0:0:0: [sda] Assuming drive cache: write through
[15234.891234] EXT4-fs error (device sda1): ext4_mb_generate_buddy:805: group 1234 block bitmap corrupted
[18392.456789] I/O error, dev sda, sector 2048576 op 0x0:(READ) flags 0x0 phys_seg 1 prio class 0

1.2G	/var/log/syslog
856M	/var/log/auth.log
234M	/var/log/kern.log
128M	/var/log/apache2/access.log
89M	/var/log/apache2/error.log
...

45M	/tmp/backup_20250122.tar.gz
12M	/tmp/cache_build_artifacts
8.4M	/tmp/session_data
```

!!! warning "Common errors"
    **`awk: syntax error in file - line 1: unexpected character '+'`** — Use `$5 > 80` instead of `$5+0 > 80` if awk version doesn't support coercion, or ensure field 5 contains only numeric values.
    **`dmesg: read error: Operation not permitted`** — Run the dmesg command with `sudo` to access the full kernel ring buffer.
    **`du: cannot access '/var/log/*': Permission denied`** — Add `sudo` before the du commands or check read permissions on the target directories.
What to look for:
- Any filesystem above 85% used requires action — logs and application data will fail to write at 100%.
- `await` above 20ms in `iostat` output indicates disk latency; above 100ms is critical.
- `%util` above 80% in `iostat` means the device is saturated.
- Hardware errors in `dmesg` (`I/O error`, `blk_update_request`, `reset`) may indicate a failing disk — escalate immediately.
- Inode exhaustion (`df -i` shows 100%) prevents file creation even when block space is available.

---

## Network Health

Commands to verify interface state, connectivity, and detect errors or unexpected connections.

```bash
# Interface status and IP addresses
ip -br addr
ip link show

# Routing table
ip route show

# Active listening ports
ss -tlnp

# Interface error and drop counters
ip -s link show

# Connection counts by state
ss -s

# Recent network-related kernel events
dmesg | grep -iE "link is down|link is up|reset adapter|carrier" | tail -10

# DNS resolution test
dig corp.local
```


```text title="Expected output"
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             192.168.1.45/24 fe80::a00:27ff:fe4e:66a1/64
eth1             UP             10.0.0.12/25 fe80::a00:27ff:fe4e:66a2/64
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:4e:66:a1 brd ff:ff:ff:ff:ff:ff
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:4e:66:a2 brd ff:ff:ff:ff:ff:ff
default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45 metric 100
10.0.0.0/25 dev eth1 proto kernel scope link src 10.0.0.12 metric 256
LISTEN    0      128                0.0.0.0:22              0.0.0.0:*    users:(("sshd",pid=847,fd=3))
LISTEN    0      128           [::]:22                 [::]:*    users:(("sshd",pid=847,fd=4))
LISTEN    0      100            127.0.0.1:25             0.0.0.0:*    users:(("master",pid=1204,fd=13))
RX: bytes  packets  errors  dropped overrun mcast
lo:        1234567  12456   0       0       0       0
eth0:      987654321 456789  2       0       0       1245
eth1:      123456789 234567  0       1       0       567
TX: bytes  packets  errors  dropped carrier colls
lo:        1234567  12456   0       0       0       0
eth0:      654321098 345678  0       0       0       0
eth1:      98765432  123456  0       0       0       0
TCP:   ESTAB 12 TIME-WAIT 3 CLOSE-WAIT 1 SYN-RECV 0
UDPLITE:   0
IPv6-ICMP: InType3 2 OutType3 1
[  145.234] e1000: eth0 NIC Link is Up 1000 Mbps Full Duplex
[  156.891] systemd-udevd[512]: renamed network interface eth1 from 'enp0s8' to 'eth1'
[  234.567]
```
What to look for:
- Any interface showing `DOWN` state that should be `UP` requires immediate investigation.
- Non-zero `RX errors` or `TX errors` in `ip -s link` output indicate NIC or cabling issues.
- Unexpected listening ports in `ss -tlnp` may indicate an unauthorized service.
- High `CLOSE-WAIT` or `TIME-WAIT` connection counts in `ss -s` may indicate application connection handling issues.
- `link is down` messages in `dmesg` that are not expected (scheduled maintenance) indicate network instability.

---

## Service Health

Commands to check the state of systemd services and review recent service failures.

```bash
# Failed services — should return 0 in a healthy state
systemctl --failed

# Check a specific service
systemctl status <service-name>

# Services that auto-started unexpectedly (restart loops)
journalctl --since "24 hours ago" | grep "Start request repeated" | tail -10

# Recent service stop/start events
journalctl --since "1 hour ago" | grep -iE "started|stopped|failed|killed" | grep -v "^--" | tail -20

# Services enabled at boot
systemctl list-unit-files --type=service --state=enabled
```


```text title="Expected output"
(no output — command completes silently)

● nginx.service - The NGINX HTTP and web server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2 days ago
       Docs: man:nginx(8)
    Process: 4521 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
   Main PID: 4522 (nginx)
      Tasks: 3 (limit: 2048)
     Memory: 12.4M
        CPU: 2min 34s
     CGroup: /system.slice/nginx.service
             ├─4522 nginx: master process /usr/sbin/nginx
             ├─4523 nginx: worker process
             └─4524 nginx: worker process

Jan 15 11:42:18 prod-web-01 systemd[1]: Start request repeated too quickly for mysql.service
Jan 15 11:42:19 prod-web-01 systemd[1]: Start request repeated too quickly for mysql.service
Jan 15 11:42:21 prod-web-01 systemd[1]: Start request repeated too quickly for mysql.service

Jan 15 14:15:33 prod-web-01 systemd[1]: Started PostgreSQL Database Server.
Jan 15 14:16:02 prod-web-01 systemd[1]: Stopped The NGINX HTTP and web server.
Jan 15 14:16:05 prod-web-01 systemd[1]: Started The NGINX HTTP and web server.
Jan 15 14:17:44 prod-web-01 systemd[1]: Failed to start Redis In-Memory Data Store.
Jan 15 14:18:12 prod-web-01 systemd[1]: Killed Docker Application Container Engine.
...

UNIT FILE                                  STATE    VENDOR PRESET
auditd.service                             enabled  enabled
chrony.service                             enabled  enabled
docker.service                             enabled  enabled
getty@tty1.service                         enabled  enabled
nginx.service                              enabled  enabled
postgresql.service                         enabled  enabled
rsyslog.service                            enabled  enabled
ssh.service                                enabled  enabled
```

!!! warning "Common errors"
    **`Unit <service-name> could not be found.`** — Verify the exact service name with `systemctl list-units --type=service` and use the correct unit file name.
    **`Failed to get properties: Connection refused`** — Restart systemd with `systemctl daemon-reexec` or reboot the system to restore the systemd connection.
    **`Start request repeated too quickly for <service>.service`** — Check service logs with `journalctl -u <service> -n 50` to identify the root cause (missing config, port conflict, or dependency failure) and fix it before re-enabling.
What to look for:
- Any unit in `systemctl --failed` output requires immediate investigation and resolution.
- Services entering a restart loop (`Start request repeated too quickly`) indicate a configuration or dependency problem.
- `Killed` entries in the journal often indicate OOM kills — correlate with memory health checks.
- Services that were `Active: active (running)` and are now `inactive (dead)` without a scheduled stop.

---

## Security Health

Commands to verify security controls, access policy, and detect suspicious activity.

```bash
# SELinux enforcement status (RHEL/AlmaLinux)
getenforce
sestatus | grep -E "mode|status"

# AppArmor status (Ubuntu/Debian)
aa-status 2>/dev/null | head -5

# Recent SELinux denials
ausearch -m avc --start recent 2>/dev/null | tail -20

# Failed SSH login attempts
grep "Failed password" /var/log/secure | tail -20
# Ubuntu: grep "Failed password" /var/log/auth.log | tail -20

# Currently logged-in users
who
w

# Recent sudo usage
journalctl -u sudo --since "24 hours ago" | tail -20

# Open ports — verify all are expected
ss -tlnp

# Check for accounts with empty passwords
awk -F: '($2 == "") {print $1}' /etc/shadow 2>/dev/null
```


```text title="Expected output"
Enforcing
   Loaded policy name:             targeted
   Current mode:                   enforcing
   Mode from config file:          enforcing
   Policy MLS status:              enabled
   Policy deny_unknown status:     allowed
   Memory protection checking:     enabled
   Max kernel policy version:      31

apparmor module is loaded.
16 profiles are loaded.
16 profiles are in enforce mode.
   /sbin/dhclient
   /usr/lib/snapd/snap-confine

type=AVC msg=audit(1704067200.123:4567): avc: denied { read } for pid=2847 comm="sshd" name="shadow" dev="dm-0" ino=8912345 scontext=system_u:system_r:sshd_t:s0-s0:c0.c1023 tcontext=system_u:object_r:shadow_t:s0 tclass=file permissive=0

Failed password for invalid user admin from 192.168.1.105 port 54321 ssh2
Failed password for root from 203.0.113.42 port 38291 ssh2
Failed password for ubuntu from 198.51.100.8 port 41922 ssh2

root     pts/0        2024-01-01 14:23 (10.0.0.50)
ubuntu   pts/1        2024-01-01 15:45 (10.0.0.51)

Jan 01 14:32:15 prod-web-01 sudo: ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; COMMAND=/bin/systemctl restart nginx
Jan 01 15:18:42 prod-web-01 sudo: admin : TTY=pts/1 ; PWD=/var/log ; USER=root ; COMMAND=/usr/bin/tail -f syslog

LISTEN    0         128                0.0.0.0:22              0.0.0.0:*        users:(("sshd",pid=1247,fd=3))
LISTEN    0         128                0.0.0.0:80              0.0.0.0:*        users:(("nginx",pid=5432,fd=6))
LISTEN    0         128                0.0.0.0:443             0.0.0.0:*        users:(("nginx",pid=5432,fd=7))
LISTEN    0         128             127.0.0.1:3306            0.0.0.0:*        users:(("mysqld",pid=2891,fd=21))
LISTEN    0         128                [::]:22                 [::]:*           users:(("sshd",pid=1247,fd=4))

(no output — no accounts with empty passwords found)
```

!!! warning "Common errors"
    **`ausearch: command not found`** — Install audit tools with `yum install audit` or `apt install auditd` and ensure the auditd service is running.
    **`grep: /var/log/secure: No such file or directory`** — On Ubuntu/Debian systems, check `/var/log/auth.log` instead of `/var/log/secure` (which is RHEL/AlmaLinux only).
    **`ss: command not found`** — Install iproute2 package with `y
What to look for:
- SELinux should be `Enforcing` on production RHEL systems — `Permissive` means policy is not being enforced.
- Repeated failed SSH logins from the same IP indicate a brute-force attack — consider `fail2ban` or firewall block.
- Unexpected users in `who` output or logins at unusual hours warrant investigation.
- Any account with an empty password in `/etc/shadow` is a critical security misconfiguration.
- Unexpected listening ports may indicate a backdoor or misconfigured service.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Linux — Procedures](../procedures/)
- [Linux — CLI Reference](../cli-reference/)
- [Linux — Common Issues](../../troubleshooting/common-issues/)
