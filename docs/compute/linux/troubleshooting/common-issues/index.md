# Linux — Common Issues


<div class="kb-summary">
Quick reference for common problems and resolutions. Structured approach to diagnosing common Linux server issues.
</div>

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
│  Quick-reference for the most frequently encountered Linux operational problems.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Boot & Startup Issues             │  │              Performance Issues             │   │
│   │            grub rescue: grub.cfg             │  │            CPU spike: top -o %CPU           │   │
│   │          initramfs: dracut --force           │  │               RAM low: free -h              │   │
│   │           fstab error: nofail opt            │  │             Disk wait: iostat -x            │   │
│   │            SELinux relabel needed            │  │             Network slow: iperf3            │   │
│   │             Kernel panic: dmesg              │  │             Zombie procs: pstree            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Auth & Access Issues             │  │               Disk & FS Issues              │   │
│   │              SSH deny: auth.log              │  │            ENOSPC: df -h / df -i            │   │
│   │            sudo fail: sudoers -l             │  │              FS ro: remount rw              │   │
│   │            SSSD down: sssd status            │  │             fsck -y: auto repair            │   │
│   │            Lock: faillock --reset            │  │             LVM snap for backup             │   │
│   │           PAM deny: /var/log/auth            │  │             xfs_repair: XFS fix             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · BIOS/UEFI · RAID controller · NIC · IPMI for OOB console                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  initramfs   = Temporary root FS loaded by kernel at boot before real root                            │
│  dracut      = Tool to build initramfs images on RHEL/Fedora systems                                  │
│  GRUB        = GRand Unified Bootloader; chainloads kernel at system start                            │
│  nofail      = fstab option; system boots even if that mount point is unavailable                     │
│  kernel panic= Unrecoverable kernel error; system halts/reboots automatically                         │
│  ENOSPC      = Error No Space; filesystem has no free blocks or inodes                                │
│  zombie proc = Process that has exited but parent has not yet waited on it                            │
│  iostat      = Reports CPU and I/O stats; -x for extended disk utilisation                            │
│  iperf3      = Network throughput test tool; client/server model                                      │
│  faillock    = PAM tool to show and reset account lockout records                                     │
│  xfs_repair  = Offline XFS filesystem repair utility                                                  │
│  fsck        = Filesystem check and repair; must be run on unmounted filesystem                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

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
