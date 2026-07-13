---
tags:
  - linux
  - troubleshooting
search:
  boost: 2
description: "Quick reference for common problems and resolutions. Structured approach to diagnosing common Linux server issues."
---
# Linux — Common Issues

<div class="kb-summary">
Quick reference for common problems and resolutions. Structured approach to diagnosing common Linux server issues.

*Applies to: RHEL / Ubuntu LTS*
</div>

Quick reference for common problems and resolutions.

Structured approach to diagnosing common Linux server issues.

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
network_connectivity_triage: "Network Connectivity Triage" {shape: rectangle}
high_disk_io_or_latency: "High Disk I/O or Latency" {shape: rectangle}
network_connectivity_issues: "Network Connectivity Issues" {shape: rectangle}
service_not_starting: "Service Not Starting" {shape: rectangle}
ssh_access_denied: "SSH Access Denied" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> network_connectivity_triage: investigate
symptom -> high_disk_io_or_latency: investigate
symptom -> network_connectivity_issues: investigate
symptom -> service_not_starting: investigate
symptom -> ssh_access_denied: investigate
diagnostic_flow -> resolution
network_connectivity_triage -> resolution
high_disk_io_or_latency -> resolution
network_connectivity_issues -> resolution
service_not_starting -> resolution
ssh_access_denied -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "SSH Access Denied" {shape: rectangle}
D2: "D2" {shape: rectangle}
R2: "Disk Full — Emergency" {shape: rectangle}
D3: "D3" {shape: rectangle}
R3: "Service Not Starting" {shape: rectangle}
D4: "D4" {shape: rectangle}
R4: "High Disk I/O or Latency" {shape: rectangle}
D5: "D5" {shape: rectangle}
R5: "Network Connectivity Issues" {shape: rectangle}
R6: "System Crash / Reboot Analysis" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}

D1 -> R1
D2 -> R2
D3 -> R3
D4 -> R4
D5 -> R5
R1 -> R6
```

---

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Network Connectivity Triage

```d2
direction: right

start: "Connectivity issue reported" {shape: oval}
linkUp: "linkUp" {shape: rectangle}
fwBlock: "fwBlock" {shape: rectangle}
resolved: "Issue identified\nand resolved" {shape: rectangle}
hasIP: "hasIP" {shape: rectangle}
gwReach: "gwReach" {shape: rectangle}
dnsOk: "dnsOk" {shape: rectangle}
portOpen: "portOpen" {shape: rectangle}

start -> linkUp
fwBlock -> resolved
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
Linux 5.15.0-1234-aws (ip-10-42-8-15) 	01/15/2025 	_x86_64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           12.45    0.00   8.32   34.21    0.00   45.02

Device            r/s     w/s     rMB/s     wMB/s   %util  await
sda             156.2   89.4      2.14      1.87   92.15  18.34
sdb              45.1   12.3      0.56      0.09   38.42   6.21

PID  USER     DISK READ  DISK WRITE  SWAPIN  IO>    COMMAND
2847 postgres   1.23 M    4.56 M      0.0 %  98.2 % postgres: writer
1923 root       0.34 M    2.11 M      0.0 % 45.1 % rsync --daemon
3421 mysql      0.12 M    0.89 M      0.0 % 12.3 % mysqld

/dev/mapper/vg0-root  100G   89G   11G   89% /
/dev/sdb1             500G  487G   13G   97% /data

Jan 15 14:23:45 ip-10-42-8-15 kernel: [12847.234521] EXT4-fs warning (device dm-0): ext4_end_bio:4892: I/O error -28
Jan 15 14:24:12 ip-10-42-8-15 kernel: [12874.456123] EXT4-fs error (device dm-0): ext4_journal_check_start:61: Filesystem has errors, running e2fsck is recommended

/tmp/backup_20250115.tar.gz  245M
/var/tmp/cache_dump.bin      156M

/var/log/syslog                 2.3G
/var/log/auth.log               1.8G
/var/log/apache2/access.log     892M
/var/log/mysql/error.log        456M
/var/log/postgresql/postgresql.log  234M
```

!!! warning "Common errors"
    **`iotop: command not found`** — Install iotop with `apt-get install iotop` (Debian/Ubuntu) or `yum install iotop` (RHEL/CentOS).
    **`find: '/tmp': Permission denied`** — Run the find command with `sudo` or check directory permissions with `ls -ld /tmp`.
    **`awk: syntax error at source line 1`** — Use proper quoting: `df -h | awk '$5+0 > 85 {print}'` to ensure the pattern is correctly interpreted.
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
1: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
   lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
2: inet 192.168.1.45/24 brd 192.168.1.255 scope global eth0
   inet 127.0.0.1/8 scope host lo
   default via 192.168.1.1 dev eth0 proto kernel scope link src 192.168.1.45
3: PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
   64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.34 ms
   64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.89 ms
   64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=2.11 ms
   64 bytes from 192.168.1.1: icmp_seq=4 ttl=64 time=1.95 ms
   --- 192.168.1.1 statistics ---
   4 packets transmitted, 4 received, 0% packet loss, time 3004ms
4: 142.250.185.46
5: LISTEN    0      128                 0.0.0.0:22              0.0.0.0:*    users:(("sshd",pid=1247,fd=3))
6: public (active)
     ports: 22/tcp 80/tcp 443/tcp
   Status: active
     Default incoming: deny
     Default outgoing: allow
   Chain INPUT (policy DROP 0 packets, 0 bytes)
     0     0 DROP       all  --  *      *       0.0.0.0/0            0.0.0.0/0
7: tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
   14:32:15.847291 IP 192.168.1.45.54821 > 10.0.2.8.443: Flags [S], seq 1234567890, win 65535, length 0
   14:32:15.849102 IP 10.0.2.8.443 > 192.168.1.45.54821: Flags [S.], seq 987654321, ack 1234567891, win 32768, length 0
   14:32:15.850445 IP 192.168.1.45.54821 > 10.0.2.8.443: Flags [.], ack 987654322, win 65535, length 0
   50 packets captured
```

!!! warning "Common errors"
    **`ping: google.com: Name or service not known`** — DNS resolution failed; verify nameserver in `/etc/resolv.conf` and check connectivity to 8.8.8.8 with `ping 8.8.8.8`.
    **`ss: No such file or directory`** — `ss` command not found; install with `apt install iproute2` (Ubuntu) or `yum install iproute`
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
    Process: 8742 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=1)
   Main PID: 8742 (code=exited, status=1)
      Error: 'address already in use'

Jan 18 14:32:15 web-prod-01 nginx[8742]: nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
Jan 18 14:32:15 web-prod-01 nginx[8742]: nginx: [emerg] bind() to [::]:80 failed (98: Address already in use)
Jan 18 14:32:15 web-prod-01 nginx[8742]: nginx: [emerg] Aborting due to port conflict.

nginx.service
└─ openssl.service (active)

(no output — unit file is valid)

LISTEN    0         128          0.0.0.0:80            0.0.0.0:*    users:(("apache",pid=5821,fd=4))
LISTEN    0         128             [::]:80               [::]:*    users:(("apache",pid=5821,fd=4))

nginx: [alert] master process terminated with code 1
```

!!! warning "Common errors"
    **`nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)`** — Stop the conflicting service (e.g., `systemctl stop apache2`) or change nginx's listen port in `/etc/nginx/nginx.conf`.
    **`Job for nginx.service failed because the control process exited with error code.`** — Run `sudo nginx -t` to validate the configuration syntax and check `/var/log/nginx/error.log` for parsing errors.
    **`Unit nginx.service not found.`** — Verify the service file exists at `/etc/systemd/system/nginx.service` and run `systemctl daemon-reload` after creating or modifying it.
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

# SELinux blocking SSH (non-standard port)
ausearch -m avc -c sshd --start recent | tail -10
```


```text title="Expected output"
● sshd.service - OpenSSH Daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2 days ago
       Docs: man:sshd(8) man:sshd_config(5)
     Process: 2847 ExecStart=/usr/sbin/sshd -D $OPTIONS (code=exited, status=0/SUCCESS)
    Main PID: 2848 (sshd)
       Tasks: 1 (limit: 2048)
      Memory: 5.2M
         CPU: 142ms
      CGroup: /system.slice/sshd.service
              └─2848 /usr/sbin/sshd -D

PasswordAuthentication yes
PubkeyAuthentication yes
AllowUsers admin@10.0.0.0/24 deploy
MaxAuthTries 6

Jan 18 14:45:22 prod-web-01 sshd[5621]: Failed password for invalid user testuser from 192.168.1.105 port 54321 ssh2
Jan 18 14:46:01 prod-web-01 sshd[5634]: error: PAM: Authentication failure for user admin from 192.168.1.110
Jan 18 14:47:15 prod-web-01 sshd[5645]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=192.168.1.115 user=admin
Jan 18 14:48:33 prod-web-01 sshd[5667]: Failed password for user deploy from 192.168.1.120 port 54389 ssh2
Jan 18 14:49:10 prod-web-01 sshd[5678]: pam_faillock(sshd:auth): Consecutive login failures for user "deploy" (3)

admin                PS      2024-01-15 14:22:10 +0000 3 0 0 0 0

deploy               L       2024-01-18 13:45:22 +0000 0 0 0 0 0

User:     deploy
When:     Thu Jan 18 13:45:22 UTC 2024
Type:     RHOST
Source:   192.168.1.125
Valid:    Thu Jan 18 14:45:22 UTC 2024

type=AVC msg=audit(1705594815.234:8921): avc:  denied  { name_connect } for  pid=2848 comm="sshd" name="2222" scontext=system_u:system_r:sshd_t:s0-s0:c0.c1023 tcontext=system_u:object_r:unreserved_port_t:s0 tclass=tcp_socket permissive=0
type=AVC msg=audit(1705594816.445:8922): avc:  denied  { read } for  pid=2848 comm="sshd" name="authorized_keys" dev="dm-0" ino=
```
## SELinux / AppArmor MAC Flow

```d2
direction: right

subject: "Subject\nProcess (e.g. httpd" {shape: rectangle}
policyCheck: "Policy Check\nauditd · SELinux policy DB" {shape: rectangle}
allow: "Allow\nAccess granted" {shape: rectangle}
object: "Object\nFile · Socket · Port" {shape: rectangle}
deny: "Deny\nAVC denial logged\n/var/log/audit/audit.log" {shape: rectangle}

subject -> policyCheck
policyCheck -> allow
allow -> object
policyCheck -> deny
```

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
/dev/sda2      100G   89G   8.2G  91% /var

/var              18G
/usr              12G
/home             8.5G
/opt              4.2G
/srv              2.1G
/lib              1.8G
/boot             512M
/root             256M
...

/var/log           6.2G
/var/cache         4.1G
/var/lib           3.8G
/var/spool         2.3G
/var/tmp           1.9G
/var/backups       892M
...

/var/log/audit/audit.log
/var/log/syslog
/var/log/kern.log

(no output — command completes silently)

COMMAND     PID     USER   FD   TYPE DEVICE  SIZE/OFF NODE NAME
java       2847    root   45u  REG  8,1    2147483648 1048592 /var/log/application.log (deleted)
nginx      1923    www    12u  REG  8,1    536870912  524288 /var/log/access.log (deleted)
mysql      2156   mysql   34u  REG  8,1    268435456  262144 /var/log/mysql.log (deleted)

Vacuumed journals from /var/log/journal/*, freed 487M.
```

!!! warning "Common errors"
    **`du: cannot read directory '/root': Permission denied`** — Run the command with `sudo` or adjust the wildcard to skip restricted directories like `du -sh /var/* /home/* /opt/* 2>/dev/null`.
    **`lsof: command not found`** — Install lsof with `apt install lsof` (Debian/Ubuntu) or `yum install lsof` (RHEL/CentOS).
    **`bash: /var/log/large-logfile.log: Permission denied`** — Use `sudo` to truncate the file: `sudo > /var/log/large-logfile.log`.
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
reboot   system boot  5.15.0-1234-aws  Fri Jan 10 14:32 - 16:45  (02:13)
reboot   system boot  5.15.0-1234-aws  Fri Jan 10 12:01 - 14:31  (02:30)
reboot   system boot  5.15.0-1233-aws  Thu Jan  9 18:22 - 12:00  (17:38)
reboot   system boot  5.15.0-1233-aws  Thu Jan  9 15:45 - 18:21  (02:36)

Jan 10 14:32:15 prod-db-01 kernel: [    0.000000] Linux version 5.15.0-1234-aws (buildd@lgw02-amd64-031) (gcc-11 (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #1234-Ubuntu SMP Fri Jan 10 13:45:22 UTC 2025
Jan 10 14:32:15 prod-db-01 kernel: [    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-1234-aws root=/dev/mapper/ubuntu--vg-root ro quiet splash vt_handoff=7
Jan 10 14:32:16 prod-db-01 kernel: [    0.847291] Memory: 16384000K/16777216K available (14339K kernel code, 2847K rwdata, 4612K rodata, 2560K init, 7891K pages, 5242K reserved, 0K cma)

(no output — command completes silently)

(no output — command completes silently)

Total_mce_registers: 10
MCE events since last login: 0

(no output — command completes silently)

SEL has 128 entries (max 128 entries)
   1 | 01/10/2025 | 14:32:01 | Power Supply #0x20 | Voltage high | Asserted
   2 | 01/10/2025 | 14:32:15 | System Event #0x73 | OEM Event | Asserted
   3 | 01/10/2025 | 14:32:22 | Processor #0x30 | Thermal Threshold | Asserted
   4 | 01/10/2025 | 14:33:01 | Memory Module #0x40 | Correctable ECC | Asserted
   5 | 01/10/2025 | 14:35:44 | System Event #0x73 | Boot completed | Asserted
```

!!! warning "Common errors"
    **`ipmitool: Error: Unable to establish IPMI v1 / IPMI v2 session`** — Verify IPMI is enabled in BIOS and the BMC is accessible; if running in a VM, IPMI may not be available.
    **`journalctl: command not found`** — Install systemd-journal or use `dmesg` and
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
-- Logs begin at Wed 2024-01-10 14:22:33 UTC, end at Wed 2024-01-10 14:32:18 UTC. --
Jan 10 14:28:45 prod-app-01 kernel: [12847.392] Out of memory: Kill process 2156 (java) score 892 or sacrifice child
Jan 10 14:29:12 prod-app-01 systemd[1]: Failed to start PostgreSQL Database Server.
Jan 10 14:31:05 prod-app-01 sudo: pam_unix(sudo:auth): authentication failure; logname=admin uid=1002 ruser=admin rhost=? user=root

/etc/nginx/nginx.conf
/etc/systemd/system/app.service
/etc/resolv.conf
/etc/hosts
/etc/ssh/sshd_config.d/99-custom.conf

COMMAND     PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx    45821    root    5u   REG  10,2   4096    892145 /path/to/file
nginx    45822   www-data 5u   REG  10,2   4096    892145 /path/to/file

LISTEN    0      128          0.0.0.0:8080       0.0.0.0:*    users:(("java",pid=3421,fd=42))

Process 3421 attached
[pid  3421] mmap(NULL, 2097152, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f8c2a400000
[pid  3421] mprotect(0x7f8c2a400000, 2097152, PROT_NONE) = 0
[pid  3421] mmap(0x7f8c2a400000, 1048576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0) = 0x7f8c2a400000
[pid  3421] brk(0x55a8c5e5f000) = 0x55a8c5e5f000
[pid  3421] mmap(NULL, 262144, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f8c29fc0000
...

System time   : -0.000000234 seconds slow of NTP time
```

!!! warning "Common errors"
    **`journalctl: No such file or directory`** — Ensure systemd-journal is installed and the journal directory exists at `/var/log/journal` or `/run/log/journal`.
    **`lsof: command not found`** — Install the lsof package with `apt install lsof` (Debian/Ubuntu) or `yum install lsof` (RHEL/CentOS).
    **`strace: attach: ptrace(PTRACE_SEIZE, <PID>): Operation not permitted`** — Run strace with sudo or ensure the user has CAP_SYS_PTRACE capability.
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Linux — Diagnostics](../diagnostics/)
- [Linux — Escalation](../escalation/)
- [Linux — Health Checks](../../operations/health-checks/)
