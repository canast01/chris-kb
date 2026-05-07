# Linux Lifecycle

> Part of the [Linux](../) reference.

---
## OS Support Timelines

| OS | Version | End of Maintenance | Extended (ESM/ELS) |
|---|---|---|---|
| RHEL | 8 | May 2029 | May 2031 (ELS) |
| RHEL | 9 | May 2032 | May 2034 (ELS) |
| Ubuntu LTS | 22.04 | Apr 2027 | Apr 2032 (Ubuntu Pro) |
| Ubuntu LTS | 24.04 | Apr 2029 | Apr 2034 (Ubuntu Pro) |

EOL tracking is maintained in the CMDB. Alerts are raised 12 months before support expiry to allow planned migration.

---

## Patching Procedure

**RHEL / Rocky Linux:**

```bash
# Check available updates
dnf check-update

# Apply all security updates only
dnf update --security -y

# Apply all updates
dnf update -y

# Check if a reboot is required
needs-restarting -r    # exits 1 if reboot required, 0 if not
dnf needs-restarting   # also lists which services need restart (no reboot)

# Verify installed kernel versions
rpm -q kernel | sort -V
uname -r   # currently running kernel
```

**Ubuntu:**

```bash
# Check available updates
apt list --upgradable

# Apply all updates
apt update && apt upgrade -y

# Security updates only (via unattended-upgrades)
unattended-upgrade --dry-run
unattended-upgrade -v

# Check if reboot is required
cat /var/run/reboot-required
```

---

## Kernel Management

```bash
# List installed kernels (RHEL)
rpm -q kernel | sort -V

# Set default kernel (RHEL/GRUB2)
grub2-set-default 0    # 0 = latest; run grubby --info=ALL to list entries
grub2-mkconfig -o /boot/grub2/grub.cfg

# List installed kernels (Ubuntu)
dpkg --list | grep linux-image

# Remove old kernels (Ubuntu — keeps current + 1 previous)
apt autoremove --purge
```

---

## Server Provisioning Checklist

After a new RHEL/Ubuntu server is deployed from template:

- [ ] Set hostname: `hostnamectl set-hostname <fqdn>`
- [ ] Verify DNS forward and reverse resolution: `dig <fqdn>` and `dig -x <ip>`
- [ ] Configure NTP: `chronyc sources -v` — confirm active sync
- [ ] Join Active Directory: `realm join <domain>` (see [Integration](../integration/))
- [ ] Apply all available patches before production use
- [ ] Install backup agent and register to backup server
- [ ] Install monitoring agent (node_exporter, Aria agent)
- [ ] Configure `/etc/sudoers.d/` entries for admin AD groups
- [ ] Confirm firewalld rules allow required traffic only
- [ ] Update CMDB with hardware, OS version, owner, and backup policy

---

## Decommission Checklist

Before removing a server:

- [ ] Confirm with the service owner that the server is no longer in use
- [ ] Remove from load balancer pool / DNS entries
- [ ] Remove from monitoring (Prometheus, Aria)
- [ ] Remove backup jobs from Veeam or NetBackup and delete restore points after retention
- [ ] Unjoin from Active Directory: `realm leave`
- [ ] Remove from Ansible inventory
- [ ] Update CMDB state to Retired
- [ ] If VM: remove from vCenter and delete VMDK files
- [ ] If physical: initiate hardware decommission process

---

## RHEL Subscription Management

```bash
# Check subscription status
subscription-manager status
subscription-manager list --consumed

# Register a new system
subscription-manager register --username <rhn-user> --password <rhn-pass>
subscription-manager attach --auto

# Check available repos
subscription-manager repos --list-enabled

# Enable a specific repo
subscription-manager repos --enable=rhel-9-for-x86_64-appstream-rpms
```

---

## In-Place Upgrade (RHEL 8 → 9)

In-place RHEL upgrades use the `leapp` tool and require a maintenance window. Not all workloads support in-place upgrade — validate application vendor support first.

```bash
# Install leapp
dnf install leapp-upgrade

# Pre-upgrade assessment (does not make changes)
leapp preupgrade

# Review inhibitors in /var/log/leapp/leapp-report.txt
cat /var/log/leapp/leapp-report.txt | grep -A5 "inhibitor"

# Perform the upgrade (server will reboot multiple times)
leapp upgrade
```

Take a VM snapshot or backup before starting the upgrade. A rollback after the upgrade completes requires restoring from the snapshot.
