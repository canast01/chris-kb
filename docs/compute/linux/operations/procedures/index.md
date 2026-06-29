---
tags:
  - linux
  - operations
---
# Linux Operations — Procedures

```bash
# Confirm system is healthy before making changes
uptime
systemctl --failed
df -h | awk '$5+0 > 85'

# Capture current state for comparison
rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n" | sort > /tmp/pre-change-packages.txt   # RHEL
dpkg -l | awk 'NR>5' > /tmp/pre-change-packages.txt   # Ubuntu

# Capture running kernel
uname -r
```


```text title="Expected output"
10:42:15 up 47 days, 3:21,  2 users,  load average: 0.84, 0.91, 0.78
(no failed units)
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   44G  3.2G  88% /
/dev/sda2      200G  156G   35G  79% /var
5.10.0-28-generic #1-Ubuntu SMP Thu Jan 30 12:00:00 UTC 2025
```

!!! warning "Common errors"
    **`df: /dev/sda1: Permission denied`** — Run the command with `sudo` to access all filesystem information.
    **`rpm: command not found`** — Comment out the rpm command on Ubuntu systems or the dpkg command on RHEL systems depending on your distribution.
    **`cannot open /tmp/pre-change-packages.txt: Permission denied`** — Ensure `/tmp` is writable or redirect output to a directory with write permissions like `~/pre-change-packages.txt`.
```bash
# Detailed memory breakdown
cat /proc/meminfo

# Check OOM (Out of Memory) killer events
journalctl -k | grep -i "oom\|killed process"
dmesg | grep -i "oom\|killed process"

# Check which process the OOM killer targeted
dmesg | grep -i "out of memory" | tail -10

# Drop caches if available memory is low (safe on production — does not affect file data)
echo 3 > /proc/sys/vm/drop_caches
```

```text title="Expected output"
MemTotal:        16384000 kB
MemFree:         2048576 kB
MemAvailable:    4096128 kB
Buffers:         512000 kB
Cached:          1536000 kB
SwapTotal:       8192000 kB
SwapFree:        7680000 kB
Slab:            256000 kB
SReclaimable:    128000 kB
SUnreclaim:      128000 kB

[12345.678901] Out of memory: Kill process 4521 (java) score 892 or sacrifice child
[12345.679012] Killed process 4521 (java) total-vm:8388608kB, anon-rss:8257024kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:16384kB oom_score_adj:300

[12345.679012] Out of memory: Kill process 4521 (java) score 892 or sacrifice child
[12345.679456] Killed process 4521 (java) total-vm:8388608kB, anon-rss:8257024kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:16384kB oom_score_adj:300

(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: /proc/sys/vm/drop_caches: Permission denied`** — Run the command with `sudo` or as root user.
    **`journalctl: command not found`** — Install systemd utilities with `apt-get install systemd` or use `dmesg` alone on systems without journalctl.
    **`dmesg: read error`** — Increase dmesg buffer size with `sysctl kernel.printk_ratelimit=0` or run with `sudo dmesg`.
```bash
# Check interface state and IP addresses
ip addr show
ip link show

# Check routing table
ip route show
ip route get <destination-ip>  # shows which interface and gateway would be used

# Check listening ports and connections
ss -tlnp   # TCP listeners
ss -unlp   # UDP listeners
ss -tnp    # established TCP connections with PID

# Test connectivity
ping -c 4 <host>
traceroute <host>
curl -v --max-time 5 http://<host>  # test HTTP reachability

# Check DNS resolution
dig <hostname>
dig @<dns-server-ip> <hostname>
nslookup <hostname> <dns-server-ip>

# Check firewalld rules (RHEL)
firewall-cmd --list-all
firewall-cmd --list-services

# Check iptables directly
iptables -L -n -v
```

```text title="Expected output"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 52:54:00:a1:2f:8c brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.45/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::5054:ff:fea1:2f8c/64 scope link
default via 192.168.1.1 dev eth0 proto kernel scope link src 192.168.1.45
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=12.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=119 time=12.3 ms
--- 8.8.8.8 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 11.8/12.1/12.4/0.24 ms
LISTEN    0      128          0.0.0.0:22            0.0.0.0:*    users:(("sshd",pid=1247,fd=3))
LISTEN    0      128             [::]:22               [::]:*    users:(("sshd",pid=1247,fd=4))
LISTEN    0      100        127.0.0.1:25            0.0.0.0:*    users:(("master",pid=2156,fd=13))
; <<>> DiG 9.16.23-RH <<>> google.com
;; Query time: 45 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Mon Jan 15 14:32:18 UTC 2024
;; MSG SIZE  rcvd: 55
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0
  sources:
  services: ssh
  ports:
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich
```
```bash
# Search journal for a specific service over a time range
journalctl -u sshd --since "2024-01-15 08:00" --until "2024-01-15 09:00" --no-pager

# Follow logs in real time
journalctl -f
journalctl -f -u <service>

# Check authentication log (failed/successful logins)
journalctl -u sshd | grep -E "Failed|Accepted"
cat /var/log/secure   # RHEL
cat /var/log/auth.log # Ubuntu/Debian

# Kernel messages (hardware errors, OOM, filesystem errors)
dmesg -T | tail -50
dmesg -T | grep -i "error\|warning\|fail"
```

```text title="Expected output"
-- Logs begin at Mon 2024-01-15 07:45:23 EST, end at Mon 2024-01-15 09:15:47 EST. --
Jan 15 08:12:34 prod-web-01 sshd[2847]: Accepted publickey for ubuntu from 203.0.113.42 port 54321 ssh2: RSA SHA256:aBcD1234efGH5678ijKL9012mnOP3456qrST7890uvW
Jan 15 08:23:15 prod-web-01 sshd[3102]: Failed password for invalid user admin from 198.51.100.89 port 48392 ssh2
Jan 15 08:45:02 prod-web-01 sshd[3456]: Accepted password for root from 192.0.2.15 port 52847 ssh2
Jan 15 08:56:44 prod-web-01 sshd[3789]: Failed password for ubuntu from 203.0.113.42 port 54322 ssh2
Jan 15 09:00:18 prod-web-01 sshd[4012]: Connection closed by authenticating user ubuntu 203.0.113.42 port 54323 [preauth]

Mon Jan 15 08:12:34 2024 prod-web-01 kernel: [12847.234567] Out of memory: Kill process nginx (1234) score 567 or sacrifice child
Mon Jan 15 08:34:22 2024 prod-web-01 kernel: [12934.456789] EXT4-fs warning (device sda1): ext4_validate_extent_entries:5432: invalid extent in block group 128
Mon Jan 15 08:56:11 2024 prod-web-01 kernel: [13056.789012] systemd-journald[847]: Failed to write entry (23 bytes) with sequence number 45678 to /var/log/journal/a1b2c3d4e5f6g7h8/system.journal: No space left on device
```

!!! warning "Common errors"
    **`journalctl: No such file or directory`** — Ensure journalctl is available (systemd-based systems only); use `cat /var/log/secure` or `/var/log/auth.log` on non-systemd systems.
    **`Failed to open /var/log/secure: Permission denied`** — Run the command with `sudo` to read protected log files.
    **`dmesg: read kernel buffer failed: Operation not permitted`** — Execute `dmesg` with `sudo` or add your user to the `adm` group with `sudo usermod -aG adm $USER`.
```bash
# List logged-in users
who
w

# Recent login history
last | head -20
lastb | head -20   # failed logins

# Check sudo access for a user
sudo -l -U <username>

# Lock / unlock a user account
passwd -l <username>   # lock
passwd -u <username>   # unlock

# Check account expiry
chage -l <username>

# Check /etc/sudoers and sudoers.d
visudo -c   # validate sudoers file
ls -la /etc/sudoers.d/
```
```d2
direction: right

hardwareInit: "hardware.target\ndevice enumeration" {shape: rectangle}
sysInit: "sysinit.target\nfsck · mount · sysctl" {shape: rectangle}
basic: "basic.target\ntimers · sockets · paths" {shape: rectangle}
networkOnline: "network-online.target\ninterfaces configured" {shape: rectangle}
multiUser: "multi-user.target\nall services ready" {shape: rectangle}
sshd: "sshd.service" {shape: rectangle}
chronyd: "chronyd.service" {shape: rectangle}
rsyslog: "rsyslog.service" {shape: rectangle}
auditd: "auditd.service" {shape: rectangle}

hardwareInit -> sysInit
sysInit -> basic
basic -> networkOnline
networkOnline -> multiUser
basic -> sshd
basic -> chronyd
networkOnline -> rsyslog
basic -> auditd
```
```bash
# List all running services
systemctl list-units --type=service --state=running

# Start / stop / restart a service
systemctl start <service>
systemctl stop <service>
systemctl restart <service>

# Enable service to start at boot
systemctl enable <service>

# Check service status with recent log tail
systemctl status <service>

# View full service logs
journalctl -u <service> -n 100 --no-pager
journalctl -u <service> --since "1 hour ago"
```

```text title="Expected output"
UNIT                                        LOAD   ACTIVE SUB     DESCRIPTION
accounts-daemon.service                     loaded active running Accounts Service
avahi-daemon.service                        loaded active running Avahi mDNS/DNS-SD Stack
cron.service                                loaded active running Regular background program processing daemon
docker.service                              loaded active running Docker Application Container Engine
nginx.service                               loaded active running A high performance web server and a reverse proxy server
openssh-server.service                      loaded active running OpenSSH server daemon
systemd-journald.service                    loaded active running Journal Service
udev.service                                loaded active running udev Kernel Device Manager
...

● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
   Main PID: 4521 (nginx)
      Tasks: 9 (limit: 2048)
     Memory: 18.4M
        CPU: 2min 34s
     CGroup: /system.slice/nginx.service
             ├─4521 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
             └─4522 nginx: worker process

Jan 15 14:32:18 prod-web-01 systemd[1]: Started A high performance web server and a reverse proxy server.

-- Logs begin at Mon 2024-01-15 10:18:42 UTC, end at Wed 2024-01-17 09:45:33 UTC. --
Jan 17 09:42:15 prod-web-01 nginx[4521]: 192.168.1.105 - - [17/Jan/2024:09:42:15 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0"
Jan 17 09:42:16 prod-web-01 nginx[4521]: 192.168.1.106 - - [17/Jan/2024:09:42:16 +0000] "GET /api/health HTTP/1.1" 200 45 "-" "curl/7.68.0"
Jan 17 09:42:18 prod-web-01 nginx[4521]: 2024/01/17 09:42:18 [notice] 4521#4521: signal process started
Jan 17 09:43:02 prod-web-01 nginx[4521]: 192.168.1.107 - - [17/Jan/2024:09:43:02 +0000] "POST /api/submit HTTP/1.1" 201 89 "-" "curl/7.68.0"
```

!!! warning "Common errors"
    **`Failed to start <service>.service: Unit <service>.service not found.`** — Verify the correct service name with `systemctl list-units --all` and use the exact unit name.
    **`Failed to enable <service>.service: Unit <service>.service is masked.`** — Unmask the service with `systemctl unmask <service>` before enabling it.
    **`Failed to get unit file state for <service>.service: No such file or directory`** — Ensure
```bash
# All active services
systemctl list-units --type=service --state=active

# Failed services
systemctl --failed

# All services (active + inactive)
systemctl list-units --type=service --all

# Services that are enabled but not running
systemctl list-units --type=service --state=inactive | grep enabled
```

```text title="Expected output"
UNIT                                   LOAD   ACTIVE SUB     DESCRIPTION
accounts-daemon.service                loaded active running Accounts Service
avahi-daemon.service                   loaded active running Avahi mDNS/DNS-SD Stack
cron.service                           loaded active running Regular background program processing daemon
docker.service                         loaded active running Docker Application Container Engine
openssh-server.service                 loaded active running OpenSSH server daemon
systemd-journald.service               loaded active running Journal Service
systemd-logind.service                 loaded active running User Login Management
systemd-resolved.service               loaded active running systemd DNS resolver
udev.service                           loaded active running udev Kernel Device Manager

UNIT                   LOAD   ACTIVE SUB    DESCRIPTION
nginx.service          loaded failed failed A high performance web server and a reverse proxy server
postgresql.service     loaded failed failed PostgreSQL database server

UNIT                                   LOAD   ACTIVE   SUB         DESCRIPTION
accounts-daemon.service                loaded active   running     Accounts Service
apparmor.service                       loaded inactive dead        Load AppArmor profiles
avahi-daemon.service                   loaded active   running     Avahi mDNS/DNS-SD Stack
cron.service                           loaded active   running     Regular background program processing daemon
docker.service                         loaded active   running     Docker Application Container Engine
...
(showing 87 of 127 loaded units)

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to get unit file state for <service>: No such file or directory`** — Verify the service name is correct and the unit file exists in `/etc/systemd/system/` or `/usr/lib/systemd/system/`.
    **`System has not been booted with systemd as init system (PID 1). Can't operate.`** — Ensure you are running on a systemd-based distribution; this command is not compatible with init or other init systems.
```bash
# What does a service depend on?
systemctl list-dependencies <service>

# What depends on this service?
systemctl list-dependencies --reverse <service>

# Show service unit file
systemctl cat <service>

# Show all properties
systemctl show <service>
```
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yaml
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```
```bash
# Load and start the new unit
systemctl daemon-reload
systemctl enable --now myapp
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to enable unit: Unit file does not exist.`** — Verify the unit file exists at `/etc/systemd/system/myapp.service` or the correct path before running `systemctl enable`.
    **`Failed to start myapp.service: Unit myapp.service not found.`** — Run `systemctl daemon-reload` first to refresh systemd's view of available units, then retry `systemctl enable --now myapp`.
```bash
# Check current limits on a running service
systemctl show <service> | grep -E "LimitNOFILE|LimitNPROC|MemoryMax|CPUQuota"

# Set memory limit via drop-in
mkdir -p /etc/systemd/system/<service>.service.d/
cat > /etc/systemd/system/<service>.service.d/limits.conf <<EOF
[Service]
MemoryMax=2G
LimitNOFILE=65536
EOF
systemctl daemon-reload
systemctl restart <service>
```

```text title="Expected output"
LimitNOFILE=65536
LimitNPROC=32768
MemoryMax=2147483648
CPUQuota=80%
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to restart <service>.service: Unit <service>.service not found.`** — Replace `<service>` with the actual service name (e.g., `nginx`, `postgresql`) and verify it exists with `systemctl list-units --type=service`.
    **`Permission denied`** — Run the entire block with `sudo` or as root, since `/etc/systemd/system/` requires elevated privileges.
    **`Failed to parse config file '/etc/systemd/system/<service>.service.d/limits.conf': Invalid value for MemoryMax=`** — Ensure memory values use valid suffixes (K, M, G, T) and are properly formatted (e.g., `2G` not `2GB`).
```bash
# Mask a service (prevents any start, even manual)
systemctl mask <service>

# Unmask
systemctl unmask <service>

# Services to disable on production servers (no UI needed)
systemctl disable --now bluetooth cups avahi-daemon
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
Removed /etc/systemd/system/bluetooth.service.
Removed /etc/systemd/system/cups.service.
Removed /etc/systemd/system/avahi-daemon.service.
```

!!! warning "Common errors"
    **`Failed to mask unit: Unit file /etc/systemd/system/<service>.service does not exist.`** — Verify the exact service name with `systemctl list-unit-files | grep <service>` before masking.
    **`Failed to disable unit, unit /etc/systemd/system/<service>.service does not exist.`** — Confirm the service is installed and enabled first with `systemctl is-enabled <service>`.
    **`Access denied`** — Run the commands with `sudo` or as root, as masking/disabling services requires elevated privileges.
```bash
# 1. Check status for the error message
systemctl status <service> -l

# 2. Check journal for the unit
journalctl -u <service> -n 50 --no-pager

# 3. Check dependencies
systemctl list-dependencies <service> | grep failed

# 4. Validate unit file syntax
systemd-analyze verify /etc/systemd/system/<service>.service

# 5. Test ExecStart command manually as the service user
sudo -u <service-user> /path/to/binary --args
```
```d2
direction: right

preCheck: "Pre-patch checks\nuptime · systemctl --failed · df -h" {shape: rectangle}
captureState: "Capture state\npackage list · running kernel" {shape: rectangle}
checkUpdates: "Check available updates\ndnf check-update / apt list --upgradable" {shape: rectangle}
apply: "Apply patches\ndnf update -y / apt upgrade -y" {shape: rectangle}
rebootNeeded: "rebootNeeded" {shape: rectangle}
reboot: "Reboot\nnew kernel" {shape: rectangle}
postValidate: "Post-patch validation\nservices · kernel · diff package list" {shape: rectangle}
done: "Complete\nClose change record" {shape: rectangle}

preCheck -> captureState
captureState -> checkUpdates
checkUpdates -> apply
apply -> rebootNeeded
reboot -> postValidate
postValidate -> done
```
```bash
# 1. Confirm system is healthy before patching
uptime
systemctl --failed
df -h | awk '$5+0 > 85'

# 2. Capture current package versions (rollback reference)
rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n" | sort > /tmp/pre-patch-packages.txt   # RHEL
dpkg -l | awk 'NR>5' > /tmp/pre-patch-packages.txt   # Ubuntu

# 3. Capture running kernel
uname -r

# 4. Check available updates without applying
dnf check-update   # RHEL
apt list --upgradable 2>/dev/null   # Ubuntu
```

```text title="Expected output"
10:47:23 up 45 days, 3:22,  2 users,  load average: 0.84, 0.91, 0.78
(no output — no failed units)
/dev/mapper/vg0-var     50G   44G  6.0G  88% /var
5.10.0-28-generic #29-Ubuntu SMP Thu Oct 5 12:15:22 UTC 2023
Last metadata expiration check: 0:12:34 ago on Thu Jan 11 10:47:15 2024.
kernel.x86_64                                 5.10.0-28-generic           5.10.0-29-generic
openssl-libs.x86_64                           1:3.0.7-6.el9_1              3.0.7-7.el9_1
glibc.x86_64                                  2.34-60.el9                  2.34-61.el9
systemd.x86_64                                252-18.el9_1                 252-20.el9_1
...
```

!!! warning "Common errors"
    **`df: command not found`** — Verify coreutils is installed with `yum install coreutils` or `apt install coreutils`.
    **`rpm: command not found`** — This script targets RHEL/CentOS; use `dpkg -l` instead on Debian/Ubuntu systems.
    **`dnf check-update: command not found`** — Install dnf with `yum install dnf` or use `yum check-update` on older RHEL versions.
```bash
# List available updates
dnf check-update

# Apply all updates (security + bug fix + enhancement)
dnf update -y

# Apply security updates only
dnf update --security -y

# Apply a specific advisory
dnf update --advisory=RHSA-2026:1234 -y

# Apply updates excluding the kernel (maintenance without reboot risk)
dnf update --exclude=kernel* -y

# List installed security advisories
dnf updateinfo list security installed | head -20
```

```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 14 Nov 2024 09:47:22 AM UTC.
kernel.x86_64                                5.14.0-427.13.1.el9_4          rhel-9-baseos-rpms
glibc.x86_64                                 2.34-60.el9_4.2                rhel-9-baseos-rpms
openssl-libs.x86_64                          1:3.0.7-27.el9_4               rhel-9-baseos-rpms
systemd.x86_64                               252-18.el9_4.5                 rhel-9-baseos-rpms
curl.x86_64                                  7.76.1-29.el9_4.1              rhel-9-baseos-rpms
...

Updating Subscription Management repositories.
Dependencies resolved.
================================================================================
 Package                  Arch      Version              Repository      Size
================================================================================
Upgrading:
 kernel                   x86_64    5.14.0-427.13.1.el9_4 rhel-9-baseos-rpms 68 M
 glibc                    x86_64    2.34-60.el9_4.2      rhel-9-baseos-rpms 2.3 M
 openssl-libs             x86_64    1:3.0.7-27.el9_4     rhel-9-baseos-rpms 1.5 M

Transaction Summary
================================================================================
Upgrade  47 packages

Total download size: 892 M
Downloading Packages:
[============================] 100%
Running transaction
Preparing        :                                                        1/1
Upgrading        : kernel-5.14.0-427.13.1.el9_4.x86_64                  1/94
Upgrading        : glibc-2.34-60.el9_4.2.x86_64                         2/94
...
Complete!

RHSA-2026:1234 Important/Sec. kernel-5.14.0-427.13.1.el9_4 x86_64
RHSA-2026:1235 Important/Sec. glibc-2.34-60.el9_4.2 x86_64
RHSA-2026:1236 Moderate/Sec.  openssl-libs-1:3.0.7-27.el9_4 x86_64
RHSA-2026:1237 Low/Sec.       curl-7.76.1-29.el9_4.1 x86_64
```

!!! warning "Common errors"
    **`Error: Failed to synchronize cache for repo 'rhel-9-baseos-rpms'`** — Verify network connectivity and subscription status with `subscription-manager status`, then retry the command.
    **`Error: Package kernel-5.14.0-427.13.1.el9_4.x86_64 not found`** — Run `dnf clean all` to clear the metadata cache, then re-run the update command.
```bash
# List recent transactions
yum history list | head -20

# View what a transaction did
yum history info <transaction-id>

# Undo a specific transaction (rollback)
yum history undo <transaction-id>
```

```text title="Expected output"
ID     | Login user | Date and time    | Action(s)      | Altered
-------------------------------------------------------------------------------
    99 | root       | 2024-01-15 14:32 | Install        |    3
    98 | root       | 2024-01-15 14:28 | Update         |    8
    97 | root       | 2024-01-15 13:45 | Erase          |    1
    96 | root       | 2024-01-14 09:12 | Install        |    5
    95 | root       | 2024-01-14 08:55 | Update         |   12
    94 | root       | 2024-01-13 16:20 | Install        |    2
    93 | root       | 2024-01-13 15:10 | Update         |    6
    92 | root       | 2024-01-12 11:33 | Install        |    4

Transaction ID : 99
Begin rpmdb   : 1234:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
End rpmdb     : 1235:x9y8z7w6v5u4t3s2r1q0p9o8n7m6l5k4
User          : root
Return-Code   : Success
Command Line  : install nginx-1.24.0-1.el7.x86_64
Packages Altered:
    Install nginx-1.24.0-1.el7.x86_64
    Install nginx-filesystem-1.24.0-1.el7.noarch
    Install nginx-all-modules-1.24.0-1.el7.noarch

Undoing transaction 99, which modified 3 packages
Erasing    nginx-1.24.0-1.el7.x86_64
Erasing    nginx-filesystem-1.24.0-1.el7.noarch
Erasing    nginx-all-modules-1.24.0-1.el7.noarch
Complete!
```

!!! warning "Common errors"
    **`Transaction ID "99" doesn't exist`** — Verify the transaction ID exists by running `yum history list` and use a valid ID from the output.
    **`Cannot undo transaction 99, it is not the last transaction`** — Use `yum history undo last` to undo the most recent transaction, or check if dependencies prevent rolling back older transactions.
    **`Error: Could not invoke yum plugins during: as_yum_plugin_hook`** — Ensure yum plugins are properly installed and the system has sufficient disk space to complete the rollback operation.
```bash
# Refresh package index
apt update

# List upgradable packages
apt list --upgradable 2>/dev/null

# Apply all upgrades
apt upgrade -y

# Full upgrade (handles dependency changes)
apt full-upgrade -y

# Remove unused packages after upgrade
apt autoremove -y
```

```text title="Expected output"
Get:1 http://archive.ubuntu.com/ubuntu focal InRelease [265 kB]
Get:2 http://archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:3 http://security.ubuntu.com/ubuntu focal-security InRelease [114 kB]
Fetched 493 kB in 2s (246 kB/s)
Reading package lists... Done
Building dependency tree
Reading state information... Done

Listing... Done
curl/7.68.0-1ubuntu1.14 7.68.0-1ubuntu1.16 upgradable
linux-image-generic/5.4.0.42 5.4.0.150 upgradable
openssh-client/1:7.6p1-4ubuntu0.6 1:7.6p1-4ubuntu0.7 upgradable
openssl/1.1.1-1ubuntu2.1 1.1.1-1ubuntu2.4 upgradable
systemd/245.4-4ubuntu3.2 245.4-4ubuntu3.6 upgradable
... (12 more upgradable packages)

Reading package lists... Done
Building dependency tree... Done
Calculating upgrade... Done
The following packages will be upgraded:
  curl linux-image-generic openssh-client openssl systemd (5 upgraded, 0 newly installed, 0 to remove)
Need to get 156 MB of archives.
After this operation, 45.2 MB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 curl amd64 7.68.0-1ubuntu1.16 [320 kB]
Processing triggers for man-db (2.9.1-1) ... Done
Setting up curl (7.68.0-1ubuntu1.16) ...

Reading package lists... Done
Building dependency tree... Done
Calculating upgrade... Done
0 upgraded, 0 newly installed, 0 to remove
Processing triggers for initramfs-tools (0.136ubuntu6.7) ...

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages will be REMOVED:
  linux-image-5.4.0-42-generic linux-modules-5.4.0-42-generic (2 packages)
0 upgraded, 0 newly installed, 2 to remove
Processing triggers for linux-image-generic (5.4.0.150-generic.202110) ...
```

!!! warning "Common errors"
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the command with `sudo` or as the root user.
    **`E: Unable to locate package <package-name>`** — Run `apt update` first to refresh the package index before attempting upgrades.
    **`E: The following packages have unmet dependencies`** — Review the dependency conflict with `apt install -f` or use `apt full-upgrade -y` instead of `apt upgrade -y` to allow dependency resolution.
```bash
# Check if a reboot is required (RHEL)
needs-restarting -r
# Exit code 1 = reboot required

# Check if a reboot is required (Ubuntu)
ls /var/run/reboot-required 2>/dev/null && echo "Reboot required" || echo "No reboot needed"
```

```text title="Expected output"
Reboot is required
```

!!! warning "Common errors"
    **`command not found: needs-restarting`** — Install the yum-utils package with `sudo yum install yum-utils` on RHEL/CentOS systems.
    **`ls: cannot access '/var/run/reboot-required': No such file or directory`** — This is expected on systems that don't require a reboot; the script correctly handles this with `2>/dev/null` redirection, so verify the system is Ubuntu/Debian-based.
```bash
# Confirm updated kernel is running (after reboot)
uname -r

# Confirm critical services are up
systemctl is-active sshd chronyd auditd

# Check for new failed services
systemctl --failed

# Compare package list to pre-patch snapshot
rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n" | sort > /tmp/post-patch-packages.txt
diff /tmp/pre-patch-packages.txt /tmp/post-patch-packages.txt
```


```text title="Expected output"
5.10.0-28.el7.x86_64
active
active
active
(no output — command completes silently)
(no output — command completes silently)
< kernel-3.10.0-1160.el7.x86_64
> kernel-5.10.0-28.el7.x86_64
< openssl-libs-1.0.2k-26.el7.x86_64
> openssl-libs-1.0.2k-27.el7.x86_64
< systemd-219-78.el7_9.5.x86_64
> systemd-219-78.el7_9.6.x86_64
```

!!! warning "Common errors"
    **`systemctl is-active: command not found`** — Verify systemctl is available on this system (RHEL 6 and older use `service` instead).
    **`diff: /tmp/pre-patch-packages.txt: No such file or directory`** — Run the pre-patch snapshot capture command (`rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n" | sort > /tmp/pre-patch-packages.txt`) before patching.
    **`Unit sshd.service could not be found`** — Check the actual SSH service name with `systemctl list-units --type=service | grep ssh` (may be `ssh` on Debian-based systems).
---

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Add a User Account

Create a new local user account, set a password, assign group membership, and ensure a home directory is created.

```bash
# Create user with home directory
useradd -m -s /bin/bash <username>

# Set password
passwd <username>

# Add user to supplementary groups (e.g., wheel for sudo, docker, adm)
usermod -aG wheel,adm <username>

# Verify account and home directory
id <username>
ls -la /home/<username>

# Confirm group membership
groups <username>
```


```text title="Expected output"
Changing password for user testuser.
New password: 
Retype new password: 
passwd: all authentication tokens updated successfully.
uid=1002(testuser) gid=1002(testuser) groups=1002(testuser),10(wheel),4(adm)
total 24
drwx------  2 testuser testuser 4096 Jan 15 10:42 .
drwxr-xr-x 15 root     root     4096 Jan 15 10:41 ..
-rw-r--r--  1 testuser testuser  220 Jan 15 10:42 .bash_logout
-rw-r--r--  1 testuser testuser 3771 Jan 15 10:42 .bashrc
-rw-r--r--  1 testuser testuser  807 Jan 15 10:42 .profile
testuser : wheel adm
```

!!! warning "Common errors"
    **`useradd: user 'testuser' already exists`** — Use `userdel -r testuser` to remove the existing user first, or choose a different username.
    **`usermod: user 'testuser' does not exist`** — Ensure the `useradd -m` command completed successfully before running `usermod`.
Home directory is created automatically with `-m`; skeleton files from `/etc/skel` are copied in. On RHEL, `wheel` group members get sudo access by default.

---

## Configure Sudo Access

Grant a user or group elevated privileges using the `/etc/sudoers.d/` drop-in approach (preferred over editing `/etc/sudoers` directly).

```bash
# Create a drop-in file for the user (preferred — avoids editing /etc/sudoers directly)
visudo -f /etc/sudoers.d/<username>
```


```text title="Expected output"
(no output — command opens editor for /etc/sudoers.d/<username>)
```

!!! warning "Common errors"
    **`visudo: /etc/sudoers.d/<username>: No such file or directory`** — Create the parent directory first with `mkdir -p /etc/sudoers.d` if it doesn't exist.
    **`visudo: syntax error near line 1`** — Ensure the sudoers syntax is correct (e.g., `username ALL=(ALL) NOPASSWD: ALL`) before saving; visudo will reject invalid syntax.
Drop-in file contents:
```bash
# Validate sudoers syntax before saving
visudo -c

# Validate a specific drop-in file
visudo -c -f /etc/sudoers.d/<username>

# List what a user can sudo
sudo -l -U <username>
```


```text title="Expected output"
/etc/sudoers: parsed OK
/etc/sudoers.d/jsmith: parsed OK
Matching Defaults entries for jsmith on host-prod-01:
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin

User jsmith may run the following commands on host-prod-01:
    (root) NOPASSWD: /usr/bin/systemctl restart nginx
    (root) /usr/bin/apt-get update
    (ALL) /usr/local/bin/deploy.sh
```

!!! warning "Common errors"
    **`/etc/sudoers.d/jsmith: syntax error near line 3`** — Review the specified file for typos in command paths or user/group syntax using `visudo -c -f /etc/sudoers.d/jsmith` to pinpoint the exact line.
    **`sudo: user <username> not found in sudoers`** — Verify the username exists with `getent passwd <username>` and that a sudoers entry has been created for that user or their group.
Drop-in files in `/etc/sudoers.d/` are included automatically. File names must not contain `.` or `~`. Set permissions to `0440`.

---

## Configure Network Interface (nmcli)

Configure a static IP address, DNS, and gateway on a NetworkManager-managed interface.

```bash
# List all connections
nmcli con show

# Show current connection details
nmcli con show "<connection-name>"

# Set static IP address (replace DHCP)
nmcli con mod "<connection-name>" ipv4.method manual \
    ipv4.addresses "192.168.1.100/24" \
    ipv4.gateway "192.168.1.1" \
    ipv4.dns "192.168.1.10,8.8.8.8"

# Disable IPv6 if not required
nmcli con mod "<connection-name>" ipv6.method ignore

# Apply changes by restarting the connection
nmcli con down "<connection-name>" && nmcli con up "<connection-name>"

# Verify the new configuration
ip addr show
ip route show
cat /etc/resolv.conf
```


```text title="Expected output"
NAME                UUID                                  TYPE      DEVICE
Wired connection 1  a7f2c9e1-4b3d-11ed-b878-001a2b3c4d5e  ethernet  eth0
docker0             9k8l7m6n-5c4e-12fe-c989-002b3c4d5e6f  bridge    docker0

NAME                UUID                                  TYPE      DEVICE
Wired connection 1  a7f2c9e1-4b3d-11ed-b878-001a2b3c4d5e  ethernet  eth0
connection.id:                          Wired connection 1
connection.type:                        802-3-ethernet
ipv4.method:                            auto
ipv4.dns:                               
ipv6.method:                            auto

Connection successfully modified.
Connection successfully modified.
Connection successfully modified.
Connection successfully modified.
Connection 'Wired connection 1' successfully deactivated.
Connection 'Wired connection 1' successfully activated with 192.168.1.100/24.

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 08:00:27:a1:b2:c3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0

default via 192.168.1.1 dev eth0 proto static metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100 metric 100

nameserver 192.168.1.10
nameserver 8.8.8.8
```

!!! warning "Common errors"
    **`Error: unknown or ambiguous command 'con show'`** — Verify nmcli version supports this syntax; use `nmcli connection show` on older versions.
    **`Error: Connection '<connection-name>' does not exist`** — Replace `<connection-name>` with the actual connection name from the first `nmcli con show` output (e.g., "Wired connection 1").
    **`Error: Connection 'Wired connection 1' does not exist or is not active`** — Ensure the connection name is correct and the device is physically connected before running `nmcli con up`.
```bash
# Add a secondary DNS search domain
nmcli con mod "<connection-name>" ipv4.dns-search "example.local,corp.local"

# Verify NetworkManager applied the settings
nmcli -p con show "<connection-name>" | grep -E "ipv4|ipv6"
```


```text title="Expected output"
ipv4.addresses:                          192.168.1.100/24
ipv4.gateway:                            192.168.1.1
ipv4.dns:                                8.8.8.8,8.8.4.4
ipv4.dns-search:                         example.local,corp.local
ipv4.ignore-auto-dns:                    no
ipv4.dhcp-duid:                          
ipv4.dhcp-iaid:                          
ipv4.dhcp-timeout:                       0 (auto)
ipv4.dhcp-send-hostname:                 yes
ipv6.addresses:                          
ipv6.gateway:                            
ipv6.dns:                                
ipv6.dns-search:
```

!!! warning "Common errors"
    **`Error: unknown or ambiguous command 'mod'.`** — Use `nmcli connection modify` instead of `nmcli con mod`, or verify your NetworkManager version supports the shorthand.
    **`Error: Connection '<connection-name>' not found.`** — Replace `<connection-name>` with the actual connection name from `nmcli con show` output (e.g., "Wired connection 1" or "eth0").
---

## Mount a Filesystem Permanently

Add a persistent mount entry to `/etc/fstab` so a filesystem mounts automatically at boot.

```bash
# Identify the device UUID (preferred over /dev/sdX — stable across reboots)
blkid /dev/sdb1

# Create the mount point directory
mkdir -p /mnt/data

# Test the fstab entry without rebooting
mount -a

# Verify the mount
df -h /mnt/data
mount | grep /mnt/data
```


```text title="Expected output"
/dev/sdb1: UUID="a7f3c2e1-9b4d-4f8a-b2c6-1d5e8f3a9b7c" TYPE="ext4" PARTUUID="5a8b2c1d-01"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb1       100G  2.1G   92G   3% /mnt/data
/dev/sdb1 on /mnt/data type ext4 (rw,relatime)
```

!!! warning "Common errors"
    **`mount: /mnt/data: special device /dev/sdb1 does not exist.`** — Verify the correct device name with `lsblk` or `fdisk -l` before mounting.
    **`mount: /mnt/data: mount point does not exist.`** — Create the mount point directory first with `mkdir -p /mnt/data`.
    **`mount: /mnt/data: wrong fs type, bad option, bad superblock on /dev/sdb1, missing codepage or helper program, or other error.`** — Check the filesystem type with `blkid` and ensure the device is formatted; if needed, run `mkfs.ext4 /dev/sdb1` to initialize it.
Add entry to `/etc/fstab`:
Common NFS mount options in `/etc/fstab`:
The `_netdev` option tells systemd to wait for the network before mounting. Use `pass` value `0` for network filesystems and non-root local disks; use `2` for additional local disks; `1` is reserved for `/`.

---

## Configure NTP (chrony)

Configure chrony as the NTP client on RHEL/CentOS/AlmaLinux or configure systemd-timesyncd on Debian/Ubuntu.

```bash
# RHEL / AlmaLinux — edit chrony configuration
vi /etc/chrony.conf
```


```text title="Expected output"
(no output — command opens vi editor with /etc/chrony.conf loaded)
```

!!! warning "Common errors"
    **`E212: Can't open file for writing`** — Ensure you have write permissions on /etc/chrony.conf or run with sudo: `sudo vi /etc/chrony.conf`
    **`E325: ATTENTION: Found a swap file`** — A previous vi session crashed; press `D` to delete the swap file or `R` to recover, then retry the edit.
Key directives in `/etc/chrony.conf`:
```bash
# Restart and enable chrony
systemctl enable --now chronyd

# Verify time sources and synchronisation
chronyc sources -v
chronyc tracking

# Check offset — should be < 1 second in normal operation
chronyc tracking | grep "System time"

# Force immediate sync
chronyc makestep

# Confirm system clock is synchronised
timedatectl status
```


```text title="Expected output"
Created symlink /etc/systemd/system/multi-user.target.wants/chronyd.service → /etc/systemd/system/chronyd.service.
210 Number of sources = 8

  .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
 / .- Source state '*' = current synced, '+' = combined , '-' = not combined,
| /   '?' = unreachable, 'x' = time may be wrong, '~' = time too variable.
| |       Name/IP Address         Stratum Poll Reach LastRx Last sample
==============================================================================
^* ntp.ubuntu.com                       2  10   377    12    -45us[ -102us] +/-   21ms
^+ time.google.com                      1  10   377   645   +156us[ +156us] +/-   18ms
^- ntp.cloudflare.com                   2  10   377  1023   +892us[ +892us] +/-   24ms
^? 91.189.89.198                        2  10     0     -     +0ns[   +0ns] +/-    0ms
^? 91.189.89.199                        2  10     0     -     +0ns[   +0ns] +/-    0ms
...

Reference ID    : C0248F97 (ntp.ubuntu.com)
Leap status     : Normal
System time     : 0.000234567 seconds fast of NTP time
Frequency       : 2.341 ppm fast
Residual freq   : +0.012 ppm
Residual skew   : 0.034 ppm
Root delay      : 0.031234 seconds
Root dispersion : 0.015678 seconds
Update interval : 64.8 seconds
Leap second     : None

System time     : 0.000234567 seconds fast of NTP time
200 OK
Step system clock by 0.000234567 seconds

               Local time: Tue 2024-01-16 14:32:18 UTC
           Universal time: Tue 2024-01-16 14:32:18 UTC
                 RTC time: Tue 2024-01-16 14:32:18
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
           RTC in local TZ: no
```

!!! warning "Common errors"
    **`chronyd: command not found`** — Install chrony with `apt-get install chrony` (Debian/Ubuntu) or `yum install chrony` (RHEL/CentOS).
    **`Failed to enable unit: Unit /etc/systemd/system/chronyd.service is masked.`** — Unmask the service with `systemctl unmask chronyd` before enabling.
    **`System time     : 1.234567 seconds fast of NTP time`** — Check network connectivity to NTP servers and verify firewall allows UDP port 123 outbound.
Ubuntu/Debian — systemd-timesyncd alternative:

```ini
# /etc/systemd/timesyncd.conf
[Time]
NTP=ntp1.example.local ntp2.example.local
FallbackNTP=pool.ntp.org
```

```bash
systemctl restart systemd-timesyncd
timedatectl show-timesync --no-pager
```


```text title="Expected output"
timedatectl show-timesync --no-pager
       Server: 91.189.89.198 (ntp.ubuntu.com)
Frequency: +42.993ppm
    Delay: 21.922ms
   Offset: -1.234ms
  Jitter: 892us
 Packet count: 8
    Leap: normal
 Poll interval: 34min 8s
TX time stamp: Wed 2024-01-17 14:32:19.847291 UTC
RX time stamp: Wed 2024-01-17 14:32:19.869213 UTC
Dest timestamp: Wed 2024-01-17 14:32:19.869213 UTC
    Root distance: 45.623ms
       Stratum: 2
    Reference: C0248F97
    Precision: 1us
```

!!! warning "Common errors"
    **`Failed to restart systemd-timesyncd.service: Unit systemd-timesyncd.service not found.`** — Verify the service is installed with `systemctl list-unit-files | grep timesyncd` and install systemd if missing.
    **`Failed to get properties: Unit systemd-timesyncd.service not loaded.`** — Enable and start the service with `systemctl enable --now systemd-timesyncd`.
---

## Extend an LVM Volume

Grow a logical volume online and resize the filesystem to use the additional space.

```bash
# 1. Confirm new disk or partition is visible
lsblk
fdisk -l /dev/sdb

# 2. Initialise the disk as a Physical Volume
pvcreate /dev/sdb

# 3. Extend the Volume Group with the new PV
vgextend <vg-name> /dev/sdb

# 4. Confirm free extents are available
vgdisplay <vg-name> | grep "Free  PE"

# 5. Extend the Logical Volume (use all available space with -l +100%FREE)
lvextend -l +100%FREE /dev/<vg-name>/<lv-name>
# Or extend by a specific size:
lvextend -L +20G /dev/<vg-name>/<lv-name>

# 6. Resize the filesystem (online — no unmount required)
# For XFS:
xfs_growfs /mount/point

# For ext4:
resize2fs /dev/<vg-name>/<lv-name>

# 7. Verify
df -h /mount/point
lvdisplay /dev/<vg-name>/<lv-name>
```


```text title="Expected output"
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0  100G  0 disk
├─sda1   8:1    0    1G  0 part /boot
└─sda2   8:2    0   99G  0 part /
sdb      8:16   0   50G  0 disk

Disk /dev/sdb: 50 GiB, 53687091200 bytes, 104857600 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes

Physical volume "/dev/sdb" successfully created with label size 2.00 MiB.

Volume group "vg0" successfully extended

  Free  PE / Size       50 / 12.50 GiB

Logical volume vg0/lv_data successfully resized to 62.50 GiB.

meta-data=/dev/mapper/vg0-lv_data inode-size=512   agcount=5, agsize=3276800 blks
data blocks changed from 16384000 to 16384000

Filesystem           Size  Used Avail Use% Mounted on
/dev/mapper/vg0-lv_data   63G   28G   35G  45% /data

  LV Path                /dev/vg0/lv_data
  LV Name                lv_data
  VG Name                vg0
  LV Size                62.50 GiB
  Current LE             16000
  Segments                2
```

!!! warning "Common errors"
    **`Device /dev/sdb not found`** — Verify the disk is attached with `lsblk` and use the correct device name (e.g., `/dev/nvme0n1` for NVMe drives).
    **`Physical volume "/dev/sdb" already exists with uuid <uuid>`** — The disk is already initialized as a PV; skip `pvcreate` or use `pvremove /dev/sdb` first if repurposing.
    **`Filesystem has unsupported feature: metadata_csum_seed`** — Use `resize2fs -f` to force resize on ext4, or ensure the kernel supports the filesystem version.
XFS filesystems can only grow, not shrink. `resize2fs` works online for ext4 on kernels 3.8+.

---

## Configure syslog / rsyslog Forwarding

Forward all local syslog events to a central syslog server using rsyslog.

```bash
# Create a drop-in forwarding config
vi /etc/rsyslog.d/90-remote.conf
```


```text title="Expected output"
(no output — command opens vi editor with blank file)
```

!!! warning "Common errors"
    **`E212: Can't open file for writing`** — Ensure you have sudo privileges: `sudo vi /etc/rsyslog.d/90-remote.conf`
    **`/etc/rsyslog.d/: No such file or directory`** — Create the directory first with `sudo mkdir -p /etc/rsyslog.d`
Contents of `/etc/rsyslog.d/90-remote.conf`:
```bash
# Validate rsyslog configuration syntax
rsyslogd -N1

# Apply the new configuration
systemctl restart rsyslog

# Verify the TCP connection to the syslog server
ss -tnp | grep :514

# Send a test message and confirm it appears on the remote server
logger -t TEST "rsyslog forwarding test from $(hostname)"
```


```text title="Expected output"
rsyslogd: version 8.2102.0, config validation run (level 0), master config /etc/rsyslog.conf
rsyslogd: End of config validation run. Bye.
(no output — command completes silently)
LISTEN    0      25           0.0.0.0:514      0.0.0.0:*    users:(("rsyslogd",pid=4782,fd=5))
LISTEN    0      25              [::]:514         [::]:*    users:(("rsyslogd",pid=4782,fd=6))
(no output — command completes silently)
```

!!! warning "Common errors"
    **`rsyslogd: syntax error on line X of /etc/rsyslog.conf`** — Review the specified line for malformed directives, unclosed quotes, or invalid action syntax.
    **`Job for rsyslog.service failed because the control process exited with error code.`** — Run `rsyslogd -N1` again to identify the syntax error, then correct the configuration file before retrying the restart.
    **`ss: No such file or directory`** — Install the `iproute2` package or use `netstat -tnp | grep :514` as an alternative on older systems.
Use TLS encryption (`omfwd` with `StreamDriver="gtls"`) for forwarding across untrusted networks.

---

## Manage systemd Services

Enable, disable, start, stop, and monitor systemd services and their logs.

```bash
# Enable a service to start at boot (and start it immediately)
systemctl enable --now <service>

# Disable a service (and stop it immediately)
systemctl disable --now <service>

# Start / stop / restart
systemctl start <service>
systemctl stop <service>
systemctl restart <service>

# Reload configuration without full restart (if the service supports it)
systemctl reload <service>

# Check status — shows recent log lines
systemctl status <service>
```


```text title="Expected output"
# Enable a service to start at boot (and start it immediately)
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
# Disable a service (and stop it immediately)
Removed /etc/systemd/system/multi-user.target.wants/nginx.service.
# Start / stop / restart
# Check status — shows recent log lines
● nginx.service - The NGINX HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
     Active: active (running) since Tue 2024-01-16 14:32:18 UTC; 2min 45s ago
       Docs: man:nginx(8)
    Process: 8742 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
   Main PID: 8751 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 12.4M
        CPU: 145ms
     CGroup: /system.slice/nginx.service
             ├─8751 nginx: master process /usr/sbin/nginx
             └─8752 nginx: worker process
```

!!! warning "Common errors"
    **`Failed to enable unit: Unit file /etc/systemd/system/<service>.service does not exist.`** — Verify the service name is correct and the package is installed with `systemctl list-unit-files | grep <service>`.
    **`Failed to start <service>.service: Unit <service>.service not found.`** — Install the service package first (e.g., `apt install nginx`) or use the full path to the unit file.
    **`Job for <service>.service failed because the control process exited with error code.`** — Check the service configuration for syntax errors using `systemctl status <service>` and review logs with `journalctl -u <service> -n 20`.
```bash
# Follow service logs in real time
journalctl -u <service> -f

# View last 100 log lines
journalctl -u <service> -n 100 --no-pager

# Logs since a specific time
journalctl -u <service> --since "1 hour ago"

# Reload all unit files after editing a unit
systemctl daemon-reload
```


```text title="Expected output"
-- Logs begin at Mon 2024-01-15 08:23:47 UTC, end at Mon 2024-01-15 14:52:19 UTC. --
Jan 15 14:52:15 prod-app-01 nginx[2847]: 192.168.1.105 - - [15/Jan/2024:14:52:15 +0000] "GET /health HTTP/1.1" 200 145 "-" "curl/7.68.0"
Jan 15 14:52:16 prod-app-01 nginx[2847]: 192.168.1.106 - - [15/Jan/2024:14:52:16 +0000] "POST /api/users HTTP/1.1" 201 892 "-" "python-requests/2.28.1"
Jan 15 14:52:17 prod-app-01 nginx[2847]: 192.168.1.107 - - [15/Jan/2024:14:52:17 +0000] "GET /api/config HTTP/1.1" 200 2341 "-" "curl/7.68.0"
Jan 15 14:52:18 prod-app-01 nginx[2847]: 2024-01-15T14:52:18.234Z [INFO] Request processed in 45ms
Jan 15 14:52:19 prod-app-01 nginx[2847]: 2024-01-15T14:52:19.567Z [INFO] Cache hit ratio: 87.3%
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to get unit file state for <service>: No such file or directory`** — Verify the service name is correct with `systemctl list-units --type=service` and use the exact unit name.
    **`Failed to open journal: Permission denied`** — Run the command with `sudo` or add your user to the `systemd-journal` group with `sudo usermod -aG systemd-journal $USER`.
    **`Unit <service> not found.`** — Confirm the service is installed and enabled with `systemctl status <service>` before attempting to view its logs.
```bash
# Check all failed services
systemctl --failed

# List all services with their start type
systemctl list-units --type=service --all

# Mask a service to prevent it from being started by any means
systemctl mask <service>
```


```text title="Expected output"
● ssh.service                                                    loaded failed failed    OpenSSH Daemon
● docker.service                                                 loaded failed failed    Docker Application Container Engine

UNIT                                          LOAD   ACTIVE   SUB     DESCRIPTION
proc-sys-fs-binfmt_misc.automount             loaded active   running Arbitrary Executable File Formats File System Automount Point
systemd-journald.service                      loaded active   running Journal Service
ssh.service                                   loaded failed   failed  OpenSSH Daemon
docker.service                                loaded failed   failed  Docker Application Container Engine
networking.service                            loaded active   running Raise network interfaces
cron.service                                  loaded active   running Regular background program processing daemon
rsyslog.service                               loaded active   running System Logging Service
...

Added /etc/systemd/system/<service>.service.d/override.conf.
Created symlink /etc/systemd/system/<service>.service → /dev/null.
```

!!! warning "Common errors"
    **`Failed to mask unit, unit <service>.service does not exist.`** — Verify the service name with `systemctl list-units --type=service --all` and use the correct unit name.
    **`Access denied`** — Run the command with `sudo` or as root to modify systemd service states.
---

## Apply Security Updates

Patch a Linux server with security-only updates and determine whether a reboot is required.

```bash
# RHEL / AlmaLinux / Rocky — check available security updates
dnf check-update --security

# Apply security updates only
dnf update --security -y

# Apply a specific advisory
dnf update --advisory=RHSA-2026:1234 -y

# Check if a reboot is required after patching
needs-restarting -r
# Exit code 0 = no reboot needed; 1 = reboot required

# Check which services need restarting without a full reboot
needs-restarting -s
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 22 Jan 2025 14:47:22 UTC.
kernel.x86_64                                    6.10.8-1.el9                   baseos
kernel-core.x86_64                               6.10.8-1.el9                   baseos
openssl.x86_64                                   1:3.0.7-27.el9                 baseos
glibc.x86_64                                     2.34-104.el9_3                 baseos
systemd.x86_64                                   252-32.el9_3                   baseos

Updating Subscription Management repositories.
Rocky Linux 9 - BaseOS                           2.4 MB/s | 3.8 MB     00:01
Rocky Linux 9 - AppStream                        3.1 MB/s | 5.2 MB     00:01
Dependencies resolved.
================================================================================
 Package                  Arch       Version              Repository      Size
================================================================================
Upgrading:
  kernel                  x86_64     6.10.8-1.el9         baseos         65 MB
  openssl                 x86_64     1:3.0.7-27.el9       baseos         2.4 MB
  glibc                   x86_64     2.34-104.el9_3       baseos         1.8 MB

Transaction Summary
================================================================================
Upgrade  3 Packages

Total download size: 69 MB
Downloading Packages:
[1/3]: openssl-3.0.7-27.el9.x86_64.rpm           1.2 MB/s | 2.4 MB     00:02
[2/3]: glibc-2.34-104.el9_3.x86_64.rpm           1.8 MB/s | 1.8 MB     00:01
[3/3]: kernel-6.10.8-1.el9.x86_64.rpm            2.1 MB/s | 65 MB      00:31
Running transaction
Preparing        :                                                        1/1
Upgrading        : glibc-2.34-104.el9_3.x86_64                           1/6
Upgrading        : openssl-1:3.0.7-27.el9.x86_64                         2/6
Upgrading        : kernel-6.10.8-1.el9.x86_64                            3/6
Complete!

RHSA-2026:1234 already installed.

Core libraries or services have been updated since boot:
  systemd (PID 1)
  sshd (PID 4521)
  rsyslog (PID 2847)
```

!!! warning "Common errors"
    **`Error: No security updates available`** — Run `dnf check-update` without the `--security` flag to see all available updates, or verify your subscription/repository configuration is correct.
    **`Error: Failed to download metadata for repo 'baseos': Cannot prepare internal mirrorlist: No URLs in mirrorlist`** — Check network connectivity and verify your repository URLs are accessible with `dnf repolist all` and `ping` to the mirror host.
    **`Error: Advisory RHSA-2026:1234 not found`
```bash
# Ubuntu / Debian — update package index and apply security upgrades
apt update
apt-get upgrade -y

# Check if reboot is required (Ubuntu)
ls /var/run/reboot-required 2>/dev/null && echo "Reboot required" || echo "No reboot needed"
cat /var/run/reboot-required.pkgs 2>/dev/null
```


```text title="Expected output"
Get:1 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
Get:3 http://security.ubuntu.com/ubuntu jammy-security InRelease [110 kB]
Fetched 499 kB in 2s (248 kB/s)
Reading package lists... Done
Reading state information... Done
Calculating the upgrade set... Done
Processing triggers for man-db (2.10.2-1) ...
Processing triggers for libc-bin (2.35-0ubuntu3.4) ...
Reboot required
linux-image-generic
linux-headers-generic
```

!!! warning "Common errors"
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the commands with `sudo` or as the root user.
    **`E: Unable to locate package`** — Run `apt update` first to refresh the package index before attempting upgrades.
```bash
# Post-patch: verify critical services are still running
systemctl is-active sshd chronyd auditd rsyslog

# Confirm running kernel after reboot
uname -r
```


```text title="Expected output"
active
active
active
active
5.10.0-28-generic
```

!!! warning "Common errors"
    **`inactive`** — Run `systemctl start <service-name>` to restart the stopped service and investigate why it failed to auto-start.
    **`Unit <service> could not be found.`** — Verify the service name is correct with `systemctl list-unit-files | grep <service>` and check if the package is installed.
---

## Configure SSH Key Authentication

Generate an SSH key pair, deploy the public key to a remote host, and harden the SSH daemon configuration.

```bash
# 1. Generate an Ed25519 key pair (recommended — smaller and more secure than RSA)
ssh-keygen -t ed25519 -C "$(whoami)@$(hostname)-$(date +%Y%m%d)"
# Default output: ~/.ssh/id_ed25519 (private) and ~/.ssh/id_ed25519.pub (public)

# For RSA (use when Ed25519 is not supported)
ssh-keygen -t rsa -b 4096 -C "$(whoami)@$(hostname)"

# 2. Copy the public key to the remote host
ssh-copy-id -i ~/.ssh/id_ed25519.pub <user>@<remote-host>
# This appends the key to ~/.ssh/authorized_keys on the remote host

# 3. Verify key-based login works before disabling password auth
ssh -i ~/.ssh/id_ed25519 <user>@<remote-host>
```


```text title="Expected output"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/admin/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/admin/.ssh/id_ed25519
Your public key has been saved in /home/admin/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:7kR9mQ2xL8vN5pJ3wK6bH4cD1eF9gT2uY7sA8vB5nC admin@prod-web-01-20240115
The key's randomart image is:
+--[ED25519 256]--+
|        .o.      |
|       o.o .     |
|      . o + o    |
|       o + = .   |
|      . S o o    |
+----[SHA256]-----+

Number of key(s) added: 1

Now try logging in with:
	"ssh -i /home/admin/.ssh/id_ed25519 admin@prod-web-01"

and check to make sure that only the key(s) you wanted were added.

Connection to prod-web-01 closed.
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the public key was copied to `~/.ssh/authorized_keys` on the remote host and that SSH daemon is configured to accept public key authentication.
    **`ssh-copy-id: ERROR: No identities found`** — Ensure the private key exists at the specified path and has correct permissions (600 for the key file, 700 for ~/.ssh directory).
    **`Host key verification failed.`** — Add the remote host's key to `~/.ssh/known_hosts` by running `ssh-keyscan -H <remote-host> >> ~/.ssh/known_hosts` first.
```bash
# Manually add a public key (when ssh-copy-id is not available)
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAA... comment" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the authorized_keys file has 600 permissions and ~/.ssh has 700 permissions using `ls -la ~/.ssh/`.
    **`bash: ~/.ssh/authorized_keys: Permission denied`** — Run `chmod 600 ~/.ssh/authorized_keys` to make the file writable by the current user.
Harden `/etc/ssh/sshd_config`:
```bash
# Validate sshd_config syntax before restarting
sshd -t

# Apply the new configuration
systemctl reload sshd
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sshd: line 42: Bad configuration option: "PermitRootLogin yes"`** — Fix the syntax error in `/etc/ssh/sshd_config` (remove extra spaces, check for typos) and run `sshd -t` again before reloading.
    **`Failed to reload sshd.service: Unit sshd.service not found.`** — Verify the service name with `systemctl list-unit-files | grep ssh` and use the correct name (may be `ssh` instead of `sshd` on some distributions).
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Linux — Health Checks](../health-checks/)
- [Linux — CLI Reference](../cli-reference/)
- [Linux — Common Issues](../../troubleshooting/common-issues/)
