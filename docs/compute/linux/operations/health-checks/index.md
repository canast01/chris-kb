# Linux — Health Checks

Routine checks, service validation, and status verification.

## Daily Health Check

Run these checks before business hours or after any overnight maintenance window.

```bash
# Check for failed systemd units — any output means investigation required
systemctl --failed

# Disk usage — flag anything above 80%
df -h

# Memory and swap
free -h
# If swap is in use, check what's consuming memory
cat /proc/meminfo | grep -E "MemAvailable|SwapFree|Committed"

# Load average — compare to number of CPU cores
uptime
nproc  # total logical CPUs; load average should stay below this value

# Failed login attempts
lastb | head -20

# Recent error-level log entries
journalctl -p err -n 50 --no-pager
# On older RHEL without journald
grep -i "error\|failed\|critical" /var/log/messages | tail -50
```

## System Overview

```bash
# Uptime, load average, logged-in users
uptime
w

# OS version and kernel
cat /etc/os-release
uname -r

# Last reboot
last reboot | head -5
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

## System Logs — Quick Errors

```bash
# All errors from the last hour
journalctl -p err --since "1 hour ago"

# Kernel warnings and errors
dmesg --level=err,warn | tail -30

# Auth failures
journalctl _SYSTEMD_UNIT=sshd.service | grep "Failed\|Invalid" | tail -20
```

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
