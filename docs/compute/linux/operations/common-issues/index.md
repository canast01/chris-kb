---
tags:
  - linux
  - operations
description: "Quick reference for common problems and resolutions. Structured approach to diagnosing common Linux server issues."
---
# Linux — Known Issues

<div class="kb-summary">
Quick reference for common problems and resolutions. Structured approach to diagnosing common Linux server issues.

*Applies to: RHEL / Ubuntu LTS*
</div>

Quick reference for common problems and resolutions.

Structured approach to diagnosing common Linux server issues.

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
triage_order: "Triage Order" {shape: rectangle}
high_disk_io_or_latency: "High Disk I/O or Latency" {shape: rectangle}
network_connectivity_issues: "Network Connectivity Issues" {shape: rectangle}
service_not_starting: "Service Not Starting" {shape: rectangle}
ssh_access_denied: "SSH Access Denied" {shape: rectangle}
disk_full_emergency: "Disk Full — Emergency" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> triage_order: investigate
symptom -> high_disk_io_or_latency: investigate
symptom -> network_connectivity_issues: investigate
symptom -> service_not_starting: investigate
symptom -> ssh_access_denied: investigate
symptom -> disk_full_emergency: investigate
triage_order -> resolution
high_disk_io_or_latency -> resolution
network_connectivity_issues -> resolution
service_not_starting -> resolution
ssh_access_denied -> resolution
disk_full_emergency -> resolution
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Triage Order

1. **Is the host reachable?** — ping, SSH, IPMI/iDRAC console
2. **Is it a hardware or OS issue?** — dmesg errors, IPMI SEL
3. **What changed recently?** — yum/dnf history, git log, cron, deployments
4. **What is the resource state?** — CPU, memory, disk, network
5. **Which services/processes are involved?** — systemctl, ps, journalctl

```d2
direction: right

alert: "Alert / Issue Reported" {shape: rectangle}
reachable: "reachable" {shape: rectangle}
changed: "changed" {shape: rectangle}
resources: "resources" {shape: rectangle}
services: "services" {shape: rectangle}
resolve: "Identify root cause\nand resolve" {shape: rectangle}
escalate: "Escalate to\nvendor / L3" {shape: rectangle}
hardware: "hardware" {shape: rectangle}

alert -> reachable
changed -> resources
resources -> services
services -> resolve
```

## High Disk I/O or Latency

```bash
# Which device is busy?
iostat -xz 1 5
# %util > 80% = saturated; await > 20ms = high latency

# Which process is doing the I/O?
iotop -o -P

# Filesystem fill causing ENOSPC errors
df -h | awk '$5+0 > 85'
dmesg | grep -i "ENOSPC\|no space left\|filesystem full"

# Large temp files
find /tmp /var/tmp -size +100M 2>/dev/null

# Growing log files
du -sh /var/log/* | sort -h | tail -10
```


```text title="Expected output"
Linux 5.15.0-1234-aws (ip-10-2-45-67)	01/15/2025	_x86_64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           12.45    0.00   8.32   34.21    0.00   45.02

Device            r/s     w/s     rMB/s     wMB/s   %util  await
sda             145.2   892.1     2.34     18.67   87.3   24.5
sdb              12.1    34.5     0.12      0.89   18.2    3.2

PID  DISK READ  DISK WRITE  SWAPIN  IO>    COMMAND
2847   8.45 M    156.23 M    0.00 % 98.2 % java -Xmx4g
1923   1.23 M     45.67 M    0.00 % 45.1 % mysqld
3012   0.00 B      2.34 M    0.00 %  8.3 % rsyslog

/dev/xvda1      100G   89G   11G   89% /
/dev/xvdb       500G  487G   13G   97% /data

dmesg: [2847.234521] EXT4-fs warning (device dm-0): ext4_mb_generate_buddy:805: EXT4-fs (dm-0): ENOSPC: Can't allocate blocks for [inode 4521234]

/tmp/backup_20250115.tar.gz    245M
/var/tmp/cache_dump.bin        156M

/var/log/syslog                 2.3G
/var/log/auth.log               1.8G
/var/log/apache2/access.log     892M
/var/log/mysql/error.log        456M
/var/log/nginx/access.log       234M
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `df: cannot access '/var/log/*': Permission denied` | Run the command with `sudo` or as root to access all log directories. |
    | `iotop: command not found` | Install iotop with `sudo apt-get install iotop` (Debian/Ubuntu) or `sudo yum install iotop` (RHEL/CentOS). |
    | `find: '/tmp': Permission denied` | Run find with `sudo` or check that the /tmp directory is readable by your user account. |
## Network Connectivity Issues

```bash
# Step 1 — Is the interface up?
ip link show | grep -E "state UP|state DOWN"

# Step 2 — Does the IP and route exist?
ip addr show
ip route show

# Step 3 — Can we reach the gateway?
ping -c 4 $(ip route show default | awk '{print $3}')

# Step 4 — Can we reach DNS?
dig +short google.com @8.8.8.8

# Step 5 — Is the local port open?
ss -tulnp | grep <port>

# Step 6 — Is firewall blocking?
firewall-cmd --list-all          # RHEL
ufw status verbose               # Ubuntu
iptables -L -n -v | grep DROP    # Direct iptables

# Step 7 — Packet capture to confirm traffic flow
tcpdump -i eth0 host <remote-ip> and port <port> -c 50
```


```text title="Expected output"
eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
eth1: <BROADCAST,MULTICAST> mtu 1500

inet 192.168.1.45/24 brd 192.168.1.255 scope global eth0
inet 127.0.0.1/8 scope host lo

default via 192.168.1.1 dev eth0 proto kernel scope link src 192.168.1.45
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45

PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=2.11 ms
64 bytes from 192.168.1.1: icmp_seq=4 ttl=64 time=1.97 ms

142.250.185.46

LISTEN   0   128   0.0.0.0:22   0.0.0.0:*   users:(("sshd",pid=1024,fd=3))

public (active)
  ports: 22/tcp 80/tcp 443/tcp
  masquerading: no

tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:32:45.123456 IP 192.168.1.45.54321 > 10.0.0.50.8080: Flags [S], seq 0, win 65535, length 0
14:32:45.124891 IP 10.0.0.50.8080 > 192.168.1.45.54321: Flags [S.], seq 1234567, ack 1, win 32768, length 0
14:32:45.125234 IP 192.168.1.45.54321 > 10.0.0.50.8080: Flags [.], ack 1234568, win 65535, length 0
50 packets captured
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ping: unknown host 192.168.1.1` | Verify the default route exists with `ip route show default` and check DNS resolution is working. |
    | `ss: No such file or directory` | Install `ss` via `apt install iproute2` (Ubuntu) or `yum install iproute` (RHEL), or use `netstat -tulnp` as fallback. |
    | `tcpdump: Permission denied` | Run tcpdump with `sudo` or add your user to the `tcpdump` group with `sudo usermod -a -G tcpdump $USER`. |
## Service Not Starting

```bash
# Check the exact error
systemctl status <service> -l
journalctl -u <service> -n 50 --no-pager

# Check dependencies
systemctl list-dependencies <service> | grep failed

# Validate unit file
systemd-analyze verify /etc/systemd/system/<service>.service

# Check if port is already in use
ss -tulnp | grep <port>

# Test the command manually
sudo -u <service-user> <ExecStart-command> --dry-run
```


```text title="Expected output"
● nginx.service - The NGINX HTTP and reverse proxy server
     Loaded: loaded (/etc/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: failed (Result: exit-code) since Thu 2024-01-18 14:32:15 UTC; 2min 43s ago
       Docs: man:nginx(1)
    Process: 8421 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=1)
   Main PID: 8421 (code=exited, status=1)
        CPU: 12ms

Jan 18 14:32:15 web-prod-01 systemd[1]: nginx.service: Main process exited, code=exited, status=1/FAILURE
Jan 18 14:32:15 web-prod-01 systemd[1]: nginx.service: Failed with result 'exit-code'.
Jan 18 14:32:15 web-prod-01 nginx[8421]: nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
Jan 18 14:32:15 web-prod-01 nginx[8421]: nginx: [emerg] bind() to [::]:80 failed (98: Address already in use)

UNIT                                      LOAD   ACTIVE SUB    DESCRIPTION
nginx.service                              loaded active running The NGINX HTTP and reverse proxy server
├─ system-getty.slice                      loaded active active Getty units
└─ system-modprobe.slice                   loaded active active Kernel module units

/etc/systemd/system/nginx.service: OK

LISTEN    PROTO LOCAL ADDRESS           FOREIGN ADDRESS         STATE       PID/PROGRAM NAME
tcp       INADDR_ANY:80                 INADDR_ANY:*            LISTEN      7834/apache2
tcp6      [::]:80                       [::]:*                  LISTEN      7834/apache2

nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
nginx: [emerg] bind() to [::]:80 failed (98: Address already in use)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)` | Stop the conflicting service (e.g., `sudo systemctl stop apache2`) or change nginx's listening port in `/etc/nginx/nginx.conf`. |
    | `systemd[1]: <service>: Main process exited, code=exited, status=1/FAILURE` | Review the full journal output with `journalctl -u <service> -n 100` to identify the actual startup error in the logs. |
    | `Failed to parse command line argument` | Verify the `ExecStart` command syntax in the unit file matches the actual binary's argument format using `man <binary>`. |
## SSH Access Denied

```bash
# Check sshd is running
systemctl status sshd

# Check sshd config for auth method restrictions
grep -E "PasswordAuth|PubkeyAuth|AllowUsers|DenyUsers|MaxAuthTries" /etc/ssh/sshd_config

# Check PAM for account restrictions
journalctl _SYSTEMD_UNIT=sshd.service | grep "Failed\|error\|pam" | tail -20

# Check if account is locked
passwd -S <username>   # L = locked
faillock --user <username>    # Check failed login counter
faillock --user <username> --reset    # Reset counter

# Check /etc/hosts.allow and hosts.deny (tcpwrappers)
cat /etc/hosts.deny
cat /etc/hosts.allow

# SELinux blocking SSH (non-standard port)
ausearch -m avc -c sshd --start recent | tail -10
```


```text title="Expected output"
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2 days ago
       Docs: man:sshd(8) man:sshd_config(5)
   Main PID: 1247 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 5.2M
        CPU: 142ms
     CGroup: /system.slice/sshd.service
             └─1247 /usr/sbin/sshd -D

PasswordAuthentication yes
PubkeyAuthentication yes
AllowUsers admin@10.0.0.* testuser
MaxAuthTries 6

Jan 15 11:42:33 prod-web-01 sshd[8934]: Failed password for invalid user appuser from 192.168.1.105 port 54321 ssh2
Jan 15 11:43:01 prod-web-01 sshd[8945]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=192.168.1.105 user=appuser
Jan 15 11:45:22 prod-web-01 sshd[8956]: error: maximum authentication attempts exceeded for invalid user appuser from 192.168.1.105 port 54322 ssh2 [preauth]

appuser L     01/15/2024 11:47     0        0        0

appuser:
	Failures before successful login: 5
	Latest failure: Mon 01/15/2024 11:45:22 UTC
	Root login failures: 0

sshd: ALL
sshd: 10.0.0.0/24

type=AVC msg=audit(1705318800.123:4567): avc:  denied  { name_bind } for  pid=1247 comm="sshd" name="2222" dev="sockfs" ino=12345 scontext=system_u:system_r:sshd_t:s0-s0:c0.c1023 tcontext=system_u:object_r:unreserved_port_t:s0 tclass=tcp_socket permissive=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /etc/ssh/sshd_config: No such file or directory` | Verify the SSH config path is correct; on some systems it may be `/etc/ssh/sshd_config.d/` or check if OpenSSH is installed with `rpm -q openssh-server`. |
    | `journalctl: command not found` | Install systemd-devel or use `tail -f /var/log/auth.log` on systems without journalctl support. |
    | `ausearch: command not found` | Install audit tools with `yum install audit` or `apt install auditd`, then ensure the audit daemon is running with `systemctl start auditd`. |
## Disk Full — Emergency

```bash
# Find the full filesystem
df -h | awk '$5+0 > 90'

# Largest directories
du -sh /* 2>/dev/null | sort -h | tail -10
du -sh /var/* 2>/dev/null | sort -h | tail -10

# Large log files
find /var/log -size +100M -type f 2>/dev/null
# Truncate (don't delete — running process may hold FD open)
> /var/log/large-logfile.log

# Open but deleted files still consuming space
lsof | grep deleted | sort -k7 -rn | head -10
# Restart the holding process to release inodes

# Force journal vacuum
journalctl --vacuum-size=500M
```


```text title="Expected output"
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   47G  1.2G  95% /
/dev/sda2      200G  156G   34G  83% /home

    12G	/var
    8.5G	/usr
    4.2G	/home
    2.1G	/opt
    1.8G	/tmp
    ...

    6.3G	/var/log
    2.8G	/var/cache
    1.4G	/var/lib
    890M	/var/spool
    ...

/var/log/apache2/access.log
/var/log/syslog
/var/log/audit/audit.log

(no output — command completes silently)

    PID   USER      FD   SIZE      NODE NAME
  2847  syslog     4r  245M    1048592 /var/log/syslog (deleted)
  3102  mysql      5w  189M    1048601 /var/log/mysql/error.log (deleted)
  1956  root       3r  156M    1048589 /var/log/auth.log (deleted)
    ...

Vacuumed journals from /var/log/journal/abc123def456 (size now 498M)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `du: cannot read directory '/root': Permission denied` | Run the du commands with `sudo` to access restricted directories. |
    | `lsof: command not found` | Install lsof with `apt-get install lsof` (Debian/Ubuntu) or `yum install lsof` (RHEL/CentOS). |
    | `journalctl: Refusing to vacuum journal files, as this would result in less than the requested amount of free space` | Lower the vacuum size target (e.g., `--vacuum-size=100M`) or free additional space first. |
## System Crash / Reboot Analysis

```bash
# Recent reboots
last reboot | head -10

# Was it a kernel panic?
journalctl -b -1 | tail -50   # Previous boot
dmesg | grep -i "panic\|bug:\|BUG:\|Oops:"

# kdump crash dump (if configured)
ls /var/crash/

# Hardware errors (memory, CPU, PCIe)
mcelog --client 2>/dev/null
dmesg | grep -iE "mce|machine check|uncorrect|hardware error"

# Check IPMI SEL (system event log)
ipmitool sel list | tail -20
```


```text title="Expected output"
wtmp begins Fri Jan 10 14:32:00 2025
reboot   system boot  5.15.0-1234-aws Fri Jan 10 14:32 - 16:45  (02:13)
reboot   system boot  5.15.0-1234-aws Fri Jan 10 12:18 - 14:31  (02:13)
reboot   system boot  5.15.0-1233-aws Thu Jan  9 23:47 - 12:17  (12:30)
reboot   system boot  5.15.0-1233-aws Thu Jan  9 18:22 - 23:46  (05:24)
reboot   system boot  5.15.0-1232-aws Wed Jan  8 09:15 - 18:21  (09:06)

Jan 10 14:32:15 ip-172-31-42-18 kernel: [    0.000000] Linux version 5.15.0-1234-aws (buildd@lcy02-amd64-030) (gcc-11 (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.37) #1234-Ubuntu SMP Fri Jan 10 13:45:22 UTC 2025
Jan 10 14:32:15 ip-172-31-42-18 kernel: [    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-1234-aws root=UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890 ro console=tty1 console=ttyS0
Jan 10 14:32:16 ip-172-31-42-18 kernel: [    0.156234] Memory: 8012345K/8388608K available (14339K kernel code, 2847K rwdata, 4612K rodata, 2840K init, 8956K pages, 5120K reserved, 0K cma)
Jan 10 14:32:18 ip-172-31-42-18 systemd[1]: Started LSB: Record successful boot for GRUB.

total 0

(no output — command completes silently)

Jan 10 14:32:19 ip-172-31-42-18 kernel: [    0.234567] MCE: CPU0: Thermal monitoring enabled (TM1)

   1 | 01/10/2025 | 14:32:15 | Power Supply #1 | Lower Critical | Asserted
   2 | 01/10/2025 | 14:32:18 | System Board Temp Sensor | Normal | Asserted
   3 | 01/10/2025 | 14:33:02 | CPU0 Temp Sensor | Upper Warning | Asserted
   4 | 01/10/2025 | 14:35:44 | Power Supply #2 | Normal | Asserted
   5 | 01/10/2025 | 14:37:21 | System Board Temp Sensor | Normal | Asserted
```

!!! warning "Common errors"
    **`ipmitool: Error: Unable to
## Useful One-Liners

```bash
# All errors in the last 10 minutes
journalctl -p err --since "10 minutes ago"

# Files recently modified in /etc
find /etc -newer /etc/fstab -type f 2>/dev/null | sort

# Which process has a file open
lsof /path/to/file

# Which process is listening on a port
ss -tlnp | grep :8080

# Strace a process for syscall-level debugging
strace -p <PID> -s 200 -f 2>&1 | head -100

# Check for time skew (NTP offset > 1s = problematic)
chronyc tracking | grep "System time"
```


```text title="Expected output"
-- Logs begin at Mon 2024-01-15 09:22:14 UTC, end at Mon 2024-01-15 14:47:33 UTC. --
Jan 15 14:42:18 prod-web-03 kernel: [45821.234567] Out of memory: Kill process 2847 (java) score 512 or sacrifice child
Jan 15 14:43:05 prod-web-03 systemd[1]: Failed to start PostgreSQL Database Server.
Jan 15 14:45:22 prod-web-03 sudo: pam_unix(sudo:auth): authentication failure; logname=deploy uid=1002 ruser=deploy rhost=? user=root

/etc/nginx/nginx.conf
/etc/nginx/conf.d/default.conf
/etc/systemd/system/app.service
/etc/hosts
/etc/resolv.conf

COMMAND     PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx    45821   www-data    5u   REG  10,2    2048 1234567 /path/to/file
nginx    45822   www-data    5u   REG  10,2    2048 1234567 /path/to/file

LISTEN    0      128          0.0.0.0:8080      0.0.0.0:*    users:(("java",pid=3847,fd=42))

strace: attach: ptrace(PTRACE_SEIZE, 3847): Operation not permitted
strace: Process 3847 attached
[pid  3847] epoll_wait(5, [{EPOLLIN, {u32=0, u64=0}}], 128, 5000) = 1
[pid  3847] read(42, "GET /health HTTP/1.1\r\nHost: loc"..., 4096) = 89
[pid  3847] write(42, "HTTP/1.1 200 OK\r\nContent-Type: "..., 156) = 156
[pid  3847] epoll_wait(5, [], 128, 5000) = 0

Reference time server: ntp.ubuntu.com
System time: 0.000234567 seconds slow of NTP time
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `strace: attach: ptrace(PTRACE_SEIZE, <PID>): Operation not permitted` | Run strace with `sudo` or ensure the process owner matches your user. |
    | `lsof: command not found` | Install lsof with `apt-get install lsof` or `yum install lsof`. |
    | `journalctl: command not found` | Ensure systemd is installed; on non-systemd systems use `tail -f /var/log/syslog` instead. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Linux — Procedures](../procedures/)
- [Linux — Health Checks](../health-checks/)
- [Linux — CLI Reference](../cli-reference/)
- [Linux — Scripts](../scripts/)
- [Linux — Backup and Restore](../backup-restore/)
- [Linux — Install and Upgrade](../install-upgrade/)
- [Linux — Common Issues](../../troubleshooting/common-issues/)
