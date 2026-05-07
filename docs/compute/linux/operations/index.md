# Linux Operations

> Part of the [Linux](../) reference.

---
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

---

## Service Management

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

---

## Disk and Filesystem

```bash
# Check disk usage with inode count (inode exhaustion causes "no space left" even with free space)
df -h && df -i

# Find top disk consumers
du -sh /* 2>/dev/null | sort -rh | head -20
du -sh /var/log/* | sort -rh | head -10

# Check for large log files
find /var/log -name "*.log" -size +500M -ls

# Check block devices and mount points
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE

# Check LVM volume group and logical volume space
vgs
lvs
pvs

# Extend an LVM logical volume (online — no unmount required for ext4/xfs)
lvextend -l +100%FREE /dev/vg0/data
resize2fs /dev/vg0/data       # ext4
xfs_growfs /mount/point       # xfs
```

---

## Process and CPU Troubleshooting

```bash
# Check top CPU consumers
ps aux --sort=-%cpu | head -20

# Check top memory consumers
ps aux --sort=-%mem | head -20

# Check system-wide CPU breakdown (interactive)
top
# Press 1 to expand per-CPU view; 'c' to show full command

# Check load by process and thread
pidstat -u 1 5  # CPU usage per process, 5 samples 1 second apart

# Find zombie processes
ps aux | awk '$8 == "Z"'

# Check process open files (useful for "too many open files" errors)
lsof -p <pid> | wc -l
ulimit -n  # current open file limit
```

---

## Memory Troubleshooting

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

---

## Network Operations

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

---

## Log Investigation

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

---

## User and Access Management

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
