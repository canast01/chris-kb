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
```text
┌──────────────────────────────────── Linux Operations — Procedures ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Standard Operating Procedures                                 │   │
│   │           User provisioning: adduser → set password → add to groups → configure sudo          │   │
│   │            Disk expansion: pvcreate → vgextend → lvextend → xfs_growfs / resize2fs            │   │
│   │           Service deployment: create unit file → systemctl enable → start → validate          │   │
│   │        Kernel update: dnf update kernel → grub2-set-default → reboot → verify uname -r        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Documented procedures reduce errors and ensure consistent repeatable outcomes                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network & Firewall              │  │              Certificate & SSH              │   │
│   │         ip addr add: add IP address          │  │            ssh-keygen -t ed25519            │   │
│   │         nmcli: NetworkManager config         │  │          ssh-copy-id to target host         │   │
│   │         firewall-cmd --permanent add         │  │          openssl req: generate CSR          │   │
│   │         ss -tlnp: verify open ports          │  │          certbot: ACME cert renewal         │   │
│   │           ip route: add/del routes           │  │           known_hosts maintenance           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · LVM volumes · NIC · iDRAC/iLO BMC · NTP · Power & Cooling                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  pvcreate    = Initialise a block device as an LVM Physical Volume                                    │
│  vgextend    = Add a new Physical Volume to an existing Volume Group                                  │
│  lvextend    = Grow a Logical Volume; must be followed by filesystem resize                           │
│  xfs_growfs  = Online-resize an XFS filesystem to fill available LV space                             │
│  resize2fs   = Online or offline-resize an ext4 filesystem after lvextend                             │
│  grub2-set-default= Select which kernel entry GRUB2 boots by default                                  │
│  nmcli       = NetworkManager CLI; manages connections, devices, and profiles                         │
│  firewall-cmd= CLI for firewalld; adds/removes services, ports, and rich rules                        │
│  ss          = Socket statistics; replaces netstat for viewing open ports/connections                 │
│  ssh-keygen  = Generates RSA/Ed25519 key pairs for SSH public-key authentication                      │
│  openssl req = Generates a Certificate Signing Request from a private key                             │
│  certbot     = ACME client for Let's Encrypt; automates TLS cert issuance and renewal                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
```mermaid
flowchart TD
    hardwareInit["hardware.target\ndevice enumeration"]
    networkOnline["network-online.target\ninterfaces configured"]
    sysInit["sysinit.target\nfsck · mount · sysctl"]
    basic["basic.target\ntimers · sockets · paths"]
    multiUser["multi-user.target\nall services ready"]
    sshd["sshd.service"]
    chronyd["chronyd.service"]
    rsyslog["rsyslog.service"]
    auditd["auditd.service"]

    hardwareInit --> sysInit --> basic --> networkOnline --> multiUser
    basic --> sshd
    basic --> chronyd
    networkOnline --> rsyslog
    basic --> auditd
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
```bash
# Mask a service (prevents any start, even manual)
systemctl mask <service>

# Unmask
systemctl unmask <service>

# Services to disable on production servers (no UI needed)
systemctl disable --now bluetooth cups avahi-daemon
```
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
```mermaid
flowchart TD
    preCheck["Pre-patch checks\nuptime · systemctl --failed · df -h"]
    captureState["Capture state\npackage list · running kernel"]
    checkUpdates["Check available updates\ndnf check-update / apt list --upgradable"]
    apply["Apply patches\ndnf update -y / apt upgrade -y"]
    rebootNeeded{"Reboot\nrequired?"}
    reboot["Reboot\nnew kernel"]
    postValidate["Post-patch validation\nservices · kernel · diff package list"]
    done["Complete\nClose change record"]

    preCheck --> captureState --> checkUpdates --> apply --> rebootNeeded
    rebootNeeded -- Yes --> reboot --> postValidate
    rebootNeeded -- No --> postValidate
    postValidate --> done
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
```bash
# List recent transactions
yum history list | head -20

# View what a transaction did
yum history info <transaction-id>

# Undo a specific transaction (rollback)
yum history undo <transaction-id>
```
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
```bash
# Check if a reboot is required (RHEL)
needs-restarting -r
# Exit code 1 = reboot required

# Check if a reboot is required (Ubuntu)
ls /var/run/reboot-required 2>/dev/null && echo "Reboot required" || echo "No reboot needed"
```
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
