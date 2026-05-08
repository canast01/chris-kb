# Linux — Components

Core components, services, and technical specifications.

## Disk Layout

Standard LVM partition layout — applied at provisioning via Kickstart or cloud-init:

```
/boot          512 MB      xfs     (separate /boot partition — not in LVM)
VG: vg_system
  lv_root     20 GB       xfs     /
  lv_var      20 GB       xfs     /var
  lv_tmp       5 GB       xfs     /tmp (noexec,nosuid mount options)
  lv_home      5 GB       xfs     /home
  lv_swap      8 GB       swap    (= RAM, up to 16 GB max)

VG: vg_data (application data — sized per role)
  lv_app      100+ GB     xfs     /opt/<app>
```

LVM enables future resizing without OS reinstallation:
```bash
# Extend a volume
lvextend -L +20G /dev/vg_system/lv_var
xfs_growfs /var
```

## Init System and Services

systemd manages all services:

```bash
# Common service management
systemctl status <service>
systemctl start <service>
systemctl enable <service>   # Persistent across reboots
journalctl -u <service> -n 100 --no-pager   # Recent logs
```

## Package Management

```bash
# RHEL (dnf)
dnf check-update             # List available updates
dnf upgrade                  # Apply all updates
dnf history                  # Review change log
subscription-manager status  # Verify RH subscription

# Ubuntu (apt)
apt-get update
apt-get upgrade -y
apt list --upgradable
ua status                    # Verify Ubuntu Advantage subscription
```

Repositories locked to approved internal mirrors — no direct internet access from production servers.

---

## Networking

Standard network configuration (nmcli / Netplan):

```bash
# RHEL — configure bonded interface with VLAN
nmcli con add type bond ifname bond0 bond.options "mode=802.3ad,miimon=100"
nmcli con add type ethernet ifname eth0 master bond0
nmcli con add type ethernet ifname eth1 master bond0
nmcli con add type vlan con-name bond0.100 dev bond0 id 100
nmcli con modify bond0.100 ipv4.addresses <ip>/<prefix> ipv4.gateway <gw> ipv4.method manual
```

All production servers require:
- Bonded uplinks (LACP) for redundancy
- Separate management IP (VLAN 10 or equivalent) and data IP (role-specific VLAN)
- DNS configured to internal resolvers

### Interface Status

```bash
# Brief summary of all interfaces and IPs
ip -br addr

# Detailed interface info
ip addr show <interface>

# Interface statistics (errors, drops, bytes)
ip -s link show <interface>

# Link state (up/down)
ip link show | grep -E "state UP|state DOWN"

# Physical link detection
ethtool <interface> | grep -E "Link detected|Speed|Duplex"
```

### IP Routes

```bash
# Routing table
ip route show

# Route for a specific destination
ip route get 10.0.0.1

# Default gateway
ip route show default

# Policy routing tables
ip rule list
```

### DNS

```bash
# Test resolution
dig +short hostname.corp.local
nslookup hostname.corp.local

# Check configured resolvers
cat /etc/resolv.conf
resolvectl status   # systemd-resolved

# Flush DNS cache
resolvectl flush-caches   # systemd-resolved
systemctl restart nscd    # if using nscd

# Reverse lookup
dig -x 10.0.0.5
```

### Active Connections and Ports

```bash
# All listening ports with PID
ss -tulnp

# Established connections
ss -tnp state established

# Connections to a specific port
ss -tnp '( dport = :443 or sport = :443 )'

# UDP listening sockets
ss -ulnp

# Legacy (older systems)
netstat -tulnp
```

### Network Configuration (nmcli — RHEL/Ubuntu)

```bash
# List connections
nmcli connection show

# Show active connection details
nmcli connection show <connection-name>

# Bring up/down a connection
nmcli connection up <name>
nmcli connection down <name>

# Add a static IP
nmcli connection modify <name> \
    ipv4.addresses "10.0.1.50/24" \
    ipv4.gateway "10.0.1.1" \
    ipv4.dns "10.0.1.10" \
    ipv4.method manual
nmcli connection up <name>

# Create a bond
nmcli connection add type bond \
    ifname bond0 bond.options "mode=802.3ad,miimon=100"
nmcli connection add type ethernet \
    ifname eth0 master bond0
nmcli connection add type ethernet \
    ifname eth1 master bond0
```

### VLAN Configuration

```bash
# Add VLAN interface (temporary)
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 10.1.100.5/24 dev eth0.100
ip link set eth0.100 up

# Permanent via nmcli
nmcli connection add type vlan \
    con-name vlan100 dev eth0 id 100 \
    ipv4.addresses "10.1.100.5/24" \
    ipv4.method manual
nmcli connection up vlan100
```

### Firewall (RHEL — firewalld)

```bash
# Check active rules
firewall-cmd --list-all
firewall-cmd --list-all-zones

# Open a port permanently
firewall-cmd --permanent --add-port=8080/tcp
firewall-cmd --reload

# Add a service
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# Check if port is open
firewall-cmd --query-port=443/tcp

# Temporarily disable (testing — not for production)
systemctl stop firewalld
```

### Firewall (Ubuntu — ufw)

```bash
# Status and rules
ufw status verbose

# Allow port
ufw allow 443/tcp

# Allow from specific source
ufw allow from 10.0.0.0/24 to any port 22

# Deny
ufw deny 23/tcp

# Enable/disable
ufw enable
ufw disable
```

### Packet Capture

```bash
# Capture on interface (write to file)
tcpdump -i eth0 -w /tmp/capture.pcap

# Capture with filter
tcpdump -i eth0 host 10.0.0.5 and port 443

# Read capture file
tcpdump -r /tmp/capture.pcap | head -50

# Capture ICMP only
tcpdump -i eth0 icmp
```

### Connectivity Tests

```bash
# Basic reachability
ping -c 4 10.0.0.1

# MTU test — set DF bit and test with 1500-byte payload
ping -M do -s 1472 10.0.0.1   # 1472 + 28 ICMP/IP headers = 1500 MTU

# Path MTU discovery
tracepath 10.0.0.1

# TCP port test
nc -zv 10.0.0.5 443
timeout 3 bash -c ">/dev/tcp/10.0.0.5/443" && echo "open" || echo "closed"

# Trace route
traceroute -n 10.0.0.1
mtr -n 10.0.0.1   # Continuous trace with packet loss stats
```

---

## Storage

Disk, LVM, filesystem, and mount management on RHEL and Ubuntu.

### Disk and Block Device Overview

```bash
# List all block devices with sizes and mount points
lsblk
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,UUID

# Disk details and partition table
fdisk -l /dev/sdb
parted /dev/sdb print

# Identify device by serial number / WWN (useful for SAN)
lsblk -o NAME,SERIAL,WWN,SIZE
udevadm info /dev/sdb | grep -E "ID_SERIAL|ID_WWN"
```

### LVM — Physical Volumes

```bash
# List PVs
pvdisplay
pvs

# Create PV on a new disk
pvcreate /dev/sdb

# Remove PV (after moving data off)
pvremove /dev/sdb
```

### LVM — Volume Groups

```bash
# List VGs
vgdisplay
vgs

# Create VG
vgcreate vg_data /dev/sdb /dev/sdc

# Extend VG with a new disk
vgextend vg_data /dev/sdd

# Check free space in VG
vgs -o name,size,free
```

### LVM — Logical Volumes

```bash
# List LVs
lvdisplay
lvs

# Create LV
lvcreate -L 50G -n lv_app vg_data

# Create LV using percentage of free VG space
lvcreate -l 80%FREE -n lv_app vg_data

# Extend LV and filesystem in one step
lvextend -L +20G /dev/vg_data/lv_app
xfs_growfs /dev/vg_data/lv_app     # XFS — online resize
resize2fs /dev/vg_data/lv_app      # ext4 — online resize

# Remove LV
lvremove /dev/vg_data/lv_app
```

### Filesystem Operations

```bash
# Format
mkfs.xfs /dev/vg_data/lv_app       # XFS (default on RHEL)
mkfs.ext4 /dev/vg_data/lv_app      # ext4

# Mount temporarily
mount /dev/vg_data/lv_app /opt/app

# Persistent mount in /etc/fstab
echo "/dev/vg_data/lv_app  /opt/app  xfs  defaults,nofail  0  2" >> /etc/fstab
mount -a    # Test fstab without reboot

# Check filesystem
xfs_repair /dev/vg_data/lv_app    # XFS (must be unmounted)
e2fsck -f /dev/vg_data/lv_app     # ext4 (must be unmounted)
```

### Disk Usage

```bash
# Filesystem usage summary
df -h

# Directory sizes (find large consumers)
du -sh /var/log/* 2>/dev/null | sort -h | tail -10
du -sh /home/* 2>/dev/null | sort -h | tail -10

# Find files larger than 1 GB
find / -xdev -size +1G -type f 2>/dev/null

# Find files modified in the last 24 hours
find /var/log -newer /tmp -type f 2>/dev/null | head -20
```

### Multipath (SAN LUNs)

```bash
# List multipath devices
multipath -ll

# Check path states
multipath -ll | grep -E "status|running|active|failed"

# Reload multipath config
systemctl reload multipathd

# Add a new LUN (after SAN zoning/mapping)
rescan-scsi-bus.sh       # Install: sg3_utils
echo "- - -" > /sys/class/scsi_host/host*/scan
multipath

# Verify device is visible
lsblk | grep dm-
```

### iSCSI

```bash
# Discover targets
iscsiadm -m discovery -t sendtargets -p <iscsi-target-ip>

# Login to target
iscsiadm -m node --login

# Check session status
iscsiadm -m session

# Persistent login (survive reboot)
iscsiadm -m node -o update -n node.startup -v automatic
```

### NFS Mounts

```bash
# Mount NFS share
mount -t nfs 10.0.0.5:/export/data /mnt/data

# Persistent NFS mount (with timeout options)
echo "10.0.0.5:/export/data  /mnt/data  nfs  defaults,_netdev,timeo=30,retrans=3  0  0" >> /etc/fstab

# Check NFS mount stats
nfsstat -m

# Show NFS exports from server
showmount -e 10.0.0.5
```

### Disk I/O Performance

```bash
# I/O statistics per device — extended
iostat -xz 1 5

# Key columns: %util (saturation), await (ms latency), r/s w/s (IOPS)
# %util > 80% = busy; await > 20ms = latency concern

# Per-process I/O (requires iotop)
iotop -o -P

# Disk read/write speed test (non-destructive — writes to tmpfs)
dd if=/dev/zero of=/tmp/testfile bs=1G count=1 oflag=direct
```

### Swap

```bash
# Check swap usage
free -h
swapon --show

# Add swap space (temporary — file-based)
dd if=/dev/zero of=/swapfile bs=1G count=4
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Persistent — add to /etc/fstab
echo "/swapfile  none  swap  sw  0  0" >> /etc/fstab

# Check swappiness
cat /proc/sys/vm/swappiness
# Set lower value for server workloads (10 recommended)
echo "vm.swappiness=10" >> /etc/sysctl.d/99-sysctl.conf
sysctl -p
```
