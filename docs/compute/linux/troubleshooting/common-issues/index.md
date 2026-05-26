# Linux — Common Issues

Quick reference for common problems and resolutions.

Structured approach to diagnosing common Linux server issues.

## Network Connectivity Triage

```mermaid
flowchart TD
    start["Connectivity issue reported"]
    linkUp{"ip link: interface\nstate UP?"}
    hasIP{"ip addr: IP address\npresent?"}
    gwReach{"ping gateway\nsucceeds?"}
    dnsOk{"dig resolves\ncorrectly?"}
    portOpen{"ss -tulnp:\nport listening?"}
    fwBlock{"firewalld / iptables\nblocking?"}
    resolved["Issue identified\nand resolved"]

    start --> linkUp
    linkUp -- No --> resolved
    linkUp -- Yes --> hasIP
    hasIP -- No --> resolved
    hasIP -- Yes --> gwReach
    gwReach -- No --> resolved
    gwReach -- Yes --> dnsOk
    dnsOk -- No --> resolved
    dnsOk -- Yes --> portOpen
    portOpen -- No --> resolved
    portOpen -- Yes --> fwBlock
    fwBlock --> resolved
```
┌──────────────────────────────── Linux — Troubleshooting Common Issues ────────────────────────────────┐
│                                                                                                       │
│  Common Linux issues: SSH failures, boot problems, OOM kills, and permission errors.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SSH Issues                  │  │                Boot Problems                │   │
│   │        Connection refused: sshd down?        │  │         Hang: systemd-analyze blame         │   │
│   │         Permission denied: check key         │  │         grub rescue: boot partition         │   │
│   │        Host key changed: known_hosts         │  │          Emergency mode: root fs ro         │   │
│   │         MaxSessions: too many logins         │  │          Kernel panic: dmesg serial         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH issues: check daemon, then key, then host; boot: single-user or rescue                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Permission Errors               │  │                 Memory / OOM                │   │
│   │    Operation not permitted: capabilities     │  │          OOM kill: dmesg | grep oom         │   │
│   │        Access denied: SELinux context        │  │        Adjust /proc/sys/vm/overcommit       │   │
│   │        Cannot write: check owner/mode        │  │            Add swap: dd + mkswap            │   │
│   │        sudo: not in sudoers: add user        │  │           Tune vm.swappiness value          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · serial console (for boot) · SSH client                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection refused= port closed or sshd not running; check systemctl status sshd                     │
│  known_hosts  = remove stale entry: ssh-keygen -R hostname                                            │
│  Emergency mode= systemd fallback; root filesystem mounted read-only for repair                       │
│  GRUB rescue  = minimal grub shell; set root/prefix then insmod + boot                                │
│  SELinux      = context mismatch causes silent denial; check audit.log                                │
│  OOM killer   = selects victim by oom_score; protect with oom_score_adj                               │
│  overcommit   = 0=heuristic, 1=always, 2=never; 2 prevents OOM but limits malloc                      │
│  swappiness   = 0-100; lower = prefer RAM; 60 default; 10 for database hosts                          │
│  Capabilities = sudo not required; use CAP_NET_ADMIN etc. for specific ops                            │
│  MaxSessions  = sshd_config; default 10 mux sessions per connection                                   │
│  single-user  = boot target for recovery; append single to kernel cmdline                             │
│  serial console= kernel console on COM1; needed when SSH/VGA unavailable                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## High Memory / OOM

```bash
# Current memory state
free -h
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Cached|SwapUsed"

# Processes using most memory
ps aux --sort=-%mem | head -15

# OOM killer activity
dmesg | grep -i "oom\|killed process" | tail -20
journalctl -k --since "1 hour ago" | grep -i oom

# Memory leak — watch a process over time
watch -n5 "ps -o pid,vsz,rss,comm -p <PID>"

# Huge pages usage
cat /proc/meminfo | grep -i huge
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

## SELinux / AppArmor MAC Flow

```mermaid
flowchart LR
    subject["Subject\nProcess (e.g. httpd)"]
    policyCheck["Policy Check\nauditd · SELinux policy DB"]
    object["Object\nFile · Socket · Port"]
    allow["Allow\nAccess granted"]
    deny["Deny\nAVC denial logged\n/var/log/audit/audit.log"]

    subject -->|"access request"| policyCheck
    policyCheck -->|"rule matches"| allow --> object
    policyCheck -->|"no matching rule"| deny
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
