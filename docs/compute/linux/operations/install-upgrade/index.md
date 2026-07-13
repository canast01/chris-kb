---
tags:
  - linux
  - operations
description: "Linux install and upgrade: kickstart/preseed PXE setup, OS patching with yum update or apt upgrade, kernel module management, and decommission steps."
---
# Linux — Install & Upgrade

<div class="kb-summary">
Linux install and upgrade: kickstart/preseed PXE setup, OS patching with `yum update` or `apt upgrade`, kernel module management, and decommission steps.

*Applies to: RHEL / Ubuntu LTS*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
linux_boot_sequence: "Linux Boot Sequence" {shape: rectangle}
inplace_upgrade_rhel_8_9: "In-Place Upgrade (RHEL 8 → 9)" {shape: rectangle}
server_lifecycle: "Server Lifecycle" {shape: rectangle}
decommission_checklist: "Decommission Checklist" {shape: rectangle}
patching: "Patching" {shape: rectangle}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> linux_boot_sequence
linux_boot_sequence -> inplace_upgrade_rhel_8_9
inplace_upgrade_rhel_8_9 -> server_lifecycle
server_lifecycle -> decommission_checklist
decommission_checklist -> patching
patching -> verify
verify -> validate
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Linux Boot Sequence

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


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Wed Nov 15 14:22:18 2024.
Dependencies resolved.
================================================================================
 Package                Arch              Version              Repository
================================================================================
Installing:
 leapp-upgrade          x86_64            0.18.0-1.el8         rhel-8-appstream
 leapp                  x86_64            0.18.0-1.el8         rhel-8-appstream
 leapp-data-rhel       x86_64            8.10-1.el8           rhel-8-appstream

Transaction Summary
================================================================================
Install  3 Packages

Total download size: 45 M
Installed size: 156 M
Is this ok? [y/N]: y
Downloading Packages:
[============================] 100%
Running transaction
Installing : leapp-0.18.0-1.el8.x86_64                                    1/3
Installing : leapp-upgrade-0.18.0-1.el8.x86_64                            2/3
Installing : leapp-data-rhel-8.10-1.el8.x86_64                            3/3
Complete!

Leapp preupgrade started at Wed Nov 15 14:25:42 2024
Checking system compatibility with target OS rhel:9.2...
Scanning system...
[###############################################] 100%
Preupgrade assessment complete.

Report saved to /var/log/leapp/leapp-report.txt
Summary: 2 inhibitors, 8 warnings found.

=== INHIBITOR: Incompatible kernel module ===
Kernel module 'floppy' is no longer supported in RHEL 9.
Remove or blacklist the module before upgrade.

=== INHIBITOR: Custom GRUB configuration ===
Custom GRUB parameters detected that may not be compatible.
Review /etc/default/grub before proceeding.

Leapp upgrade started at Wed Nov 15 14:28:15 2024
Preparing system for upgrade...
Downloading RHEL 9 packages...
[###############################################] 100%
Executing upgrade transaction...
System will reboot now.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: Leapp preupgrade found inhibitors. Please review /var/log/leapp/leapp-report.txt` | Address all inhibitors listed in the report before running `leapp upgrade`. |
    | `ERROR: insufficient disk space for upgrade (required: 2.5G, available: 1.8G)` | Free up disk space on the root filesystem or expand the partition before retrying the upgrade. |
    | `ERROR: leapp command not found` | Install the leapp package with `dnf install leapp-upgrade` and ensure the RHEL subscription is active. |
Take a VM snapshot or backup before starting the upgrade. A rollback after the upgrade completes requires restoring from the snapshot.

## Server Lifecycle

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

## Patching

Patch management procedures for RHEL 8/9 and Ubuntu 22.04 LTS servers.

### Pre-Patch Checklist

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
10:34:22 up 127 days, 3:45,  2 users,  load average: 0.42, 0.38, 0.35
(no output — no failed units)
/dev/mapper/vg0-lv_var     50G   44G  3.2G  94% /var
/dev/sda1                 500M  487M   13M  98% /boot

(no output — command completes silently)

5.10.0-28-generic #29-Ubuntu SMP Thu Apr 2 12:26:46 UTC 2024

Listing...
audit-libs/x86_64                                    3.0.7-14.el9                    rhel-9-appstream
bash/x86_64                                          5.1.16-2.el9                    rhel-9-baseos
bind-libs/x86_64                                     9.16.48-2.el9_4.1               rhel-9-appstream
curl/x86_64                                          7.76.1-29.el9_4.5               rhel-9-appstream
kernel/x86_64                                        5.10.209-2.el9                  rhel-9-baseos
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Filesystem /var is 94% full` | Run `df -h` to identify large files and archive or delete non-critical logs before patching. |
    | `error: rpmdb open failed: Permission denied` | Execute the rpm/dnf commands with `sudo` or as root user. |
    | `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)` | Run apt commands with `sudo` to acquire the package manager lock. |
### RHEL — dnf Patching

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
Last metadata expiration check: 0:12:34 ago on Wed 19 Feb 2025 14:22:18 UTC.
kernel.x86_64                                5.14.0-427.13.1.el9_4          rhel-9-baseos-rpms
glibc.x86_64                                 2.34-104.el9_4                  rhel-9-baseos-rpms
openssl.x86_64                               3.0.7-27.el9_4                  rhel-9-baseos-rpms
systemd.x86_64                               252-18.el9_4.5                  rhel-9-baseos-rpms
curl.x86_64                                  7.76.1-29.el9_4                 rhel-9-appstream-rpms
...

Updating Subscription Management repositories.
Last metadata expiration check: 0:12:34 ago on Wed 19 Feb 2025 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package                    Arch       Version              Repository    Size
================================================================================
Upgrading:
 kernel                     x86_64     5.14.0-427.13.1.el9_4 rhel-9-baseos-rpms 65 M
 glibc                      x86_64     2.34-104.el9_4       rhel-9-baseos-rpms 2.2 M
 openssl                    x86_64     3.0.7-27.el9_4       rhel-9-appstream-rpms 1.5 M

Transaction Summary
================================================================================
Upgrade  3 packages

Total download size: 68.7 M
Downloading Packages:
[1/3] kernel-5.14.0-427.13.1.el9_4.x86_64.rpm    45% | 29 MB     00:08 ETA
[3/3] Complete!
Running transaction
Preparing        :                                                        1/1
Upgrading        : glibc-2.34-104.el9_4.x86_64                           1/6
Upgrading        : openssl-3.0.7-27.el9_4.x86_64                         2/6
Upgrading        : kernel-5.14.0-427.13.1.el9_4.x86_64                   3/6
Complete!

RHSA-2026:1234 | Critical Patch Advisory | kernel-5.14.0-427.13.1.el9_4
RHSA-2026:1235 | Important Patch Advisory | glibc-2.34-104.el9_4
RHSA-2026:1236 | Moderate Patch Advisory | curl-7.76.1-29.el9_4
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Failed to synchronize cache for repo 'rhel-9-baseos-rpms'` | Verify network connectivity and subscription status with `subscription-manager status`, then retry the update. |
    | `Error: Package kernel conflicts with kernel-5.14.0-427.12.1.el9_4.x86_64` | Remove the conflicting kernel version with `dnf remove kernel-5.14.0-427. |
### RHEL — yum history (Rollback)

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
    99 | root       | 2024-01-15 14:32 | Install        |    1
    98 | root       | 2024-01-15 14:28 | Update         |    3
    97 | root       | 2024-01-15 13:45 | Erase          |    1
    96 | root       | 2024-01-14 09:22 | Install        |    2
    95 | root       | 2024-01-14 08:15 | Update         |    5
    94 | root       | 2024-01-13 16:50 | Install        |    1
    93 | root       | 2024-01-13 15:33 | Update         |    4
    92 | root       | 2024-01-12 11:20 | Install        |    2
    91 | root       | 2024-01-12 10:05 | Erase          |    1
    90 | root       | 2024-01-11 17:42 | Update         |    6

Loaded plugins: fastestmirror, security
ID     : 98
Timestamp : 2024-01-15 14:28:30
Begin rpmdb : 247:5d8e9c2f1a4b6e7f9c3d2e1f5a8b9c0d
End rpmdb   : 250:7f2e1d9c8b7a6f5e4d3c2b1a9f8e7d6c
User       : <root>
Return-Code: Success
Command Line: update kernel
Packages Altered:
    Install kernel-3.10.0-1160.92.1.el7.x86_64 @updates
    Erase   kernel-3.10.0-1160.el7.x86_64 @anaconda
    Install kernel-firmware-3.10.0-1160.92.1.el7.noarch @updates

Loaded plugins: fastestmirror, security
Undoing transaction 98, from Mon Jan 15 14:28:30 2024
    Erase kernel-3.10.0-1160.92.1.el7.x86_64
    Install kernel-3.10.0-1160.el7.x86_64
    Erase kernel-firmware-3.10.0-1160.92.1.el7.noarch
Is this ok [y/N]: y
Running transaction
Complete!
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Transaction ID "98" doesn't exist` | Verify the transaction ID exists by running `yum history list` and use a valid ID from the output. |
    | `Error: Could not open rpmdb` | Ensure yum is not already running in another terminal and check disk space with `df -h /var`. |
### Ubuntu — apt Patching

```bash
# Refresh package index
apt update

# List upgradable packages
apt list --upgradable 2>/dev/null

# Apply all upgrades
apt upgrade -y

# Apply security updates only (using unattended-upgrades filter)
apt-get install --only-upgrade $(apt-get --just-print upgrade 2>/dev/null | \
  grep "^Inst" | grep -i security | awk '{print $2}') -y

# Full upgrade (handles dependency changes)
apt full-upgrade -y

# Remove unused packages after upgrade
apt autoremove -y
```


```text title="Expected output"
Hit:1 http://archive.ubuntu.com/ubuntu focal InRelease
Hit:2 http://security.ubuntu.com/ubuntu focal-security InRelease
Hit:3 http://archive.ubuntu.com/ubuntu focal-updates InRelease
Reading package lists... Done
Building dependency tree... Done

Listing... Done
curl/7.68.0-1ubuntu1.14 -> 7.68.0-1ubuntu1.16
openssl/1.1.1f-1ubuntu2.19 -> 1.1.1f-1ubuntu2.21
linux-image-generic/5.4.0.150.146 -> 5.4.0.156.152
openssh-server/1:8.2p1-4ubuntu0.7 -> 1:8.2p1-4ubuntu0.9
...

Reading package lists... Done
Building dependency tree... Done
Calculating the upgrade set... Done
Processing triggers for man-db (2.9.1-1)...
Setting up curl (7.68.0-1ubuntu1.16) [100%]
Done. 23 upgraded, 0 newly installed, 0 to remove.

Reading package lists... Done
Building dependency tree... Done
Calculating the upgrade set... Done
0 upgraded, 0 newly installed, 0 to remove.

Reading package lists... Done
Building dependency tree... Done
Calculating the upgrade set... Done
0 upgraded, 0 newly installed, 0 to remove.

Reading package lists... Done
Building dependency tree... Done
Calculating the upgrade set... Done
0 upgraded, 0 newly installed, 2 to remove.
Removing libssl1.0.0:amd64 (1.0.2-1ubuntu4.20) ...
Removing libcurl3:amd64 (7.58.0-2ubuntu3.24) ...
Processing triggers for libc6:amd64 (2.31-0ubuntu9.9) ...
Done.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)` | Run the script with `sudo` or as the root user. |
    | `E: Unable to locate package` (during security-only upgrade)` | The grep filter may match no packages; wrap the apt-get install command with `[ -n "$(apt-get --just-print upgrade 2>/dev/null | grep "^Inst" | grep -i security)" ] &&` to skip if empty. |
### Kernel Updates and Reboot

```bash
# Check if a reboot is required (RHEL)
needs-restarting -r
# Exit code 1 = reboot required

# Check if a reboot is required (Ubuntu)
ls /var/run/reboot-required 2>/dev/null && echo "Reboot required" || echo "No reboot needed"

# Verify new kernel is default after update
grub2-editenv list | grep saved_entry   # RHEL
grep GRUB_DEFAULT /etc/default/grub     # Ubuntu
```


```text title="Expected output"
# Check if a reboot is required (RHEL)
$ needs-restarting -r
Core libraries or services have been updated.
Reboot is required to ensure that your system benefits from these updates.

# Check if a reboot is required (Ubuntu)
$ ls /var/run/reboot-required 2>/dev/null && echo "Reboot required" || echo "No reboot needed"
Reboot required

# Verify new kernel is default after update
$ grub2-editenv list | grep saved_entry
saved_entry=0

$ grep GRUB_DEFAULT /etc/default/grub
GRUB_DEFAULT=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `needs-restarting: command not found` | Install the yum-utils package with `sudo yum install yum-utils` on RHEL/CentOS. |
    | `grep: /etc/default/grub: No such file or directory` | Verify the system is Ubuntu/Debian-based; RHEL systems use `/etc/default/grub2` instead. |
### Ansible Patching at Scale

```yaml
# patch-rhel.yml — apply security patches to a group of RHEL servers
- hosts: rhel_servers
  become: true
  tasks:
    - name: Apply all security updates
      ansible.builtin.dnf:
        name: "*"
        state: latest
        security: true
      register: dnf_result

    - name: Check if reboot is required
      ansible.builtin.command: needs-restarting -r
      register: reboot_check
      failed_when: false
      changed_when: false

    - name: Reboot if required
      ansible.builtin.reboot:
        reboot_timeout: 300
      when: reboot_check.rc == 1
```

### Post-Patch Validation

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

# Verify no unexpected changes in /etc
find /etc -newer /tmp/pre-patch-packages.txt -type f 2>/dev/null | head -20
```


```text title="Expected output"
5.10.0-28.el7.x86_64
active
active
active
(no units in failed state)
< kernel-2.6.32-754.el7.x86_64
> kernel-5.10.0-28.el7.x86_64
< openssl-libs-1.0.2k-19.el7.x86_64
> openssl-libs-1.0.2k-26.el7.x86_64
< systemd-219-78.el7.x86_64
> systemd-219-88.el7.x86_64
/etc/ssh/sshd_config.rpmnew
/etc/chrony.conf.rpmnew
/etc/audit/rules.d/audit.rules
/etc/default/grub
/etc/fstab
/etc/hostname
/etc/resolv.conf
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `diff: /tmp/pre-patch-packages.txt: No such file or directory` | Run the pre-patch snapshot command (`rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n" | sort > /tmp/pre-patch-packages.txt`) before patching to create the baseline file. |
    | `find: '/etc': Permission denied` | Run the find command with `sudo` or as root to access all files in /etc without permission errors. |
    | `systemctl is-active: command not found` | Ensure you are on a systemd-based system (RHEL 7+, CentOS 7+); on older systems use `service sshd status` instead. |
### Patch Schedule Standards

| Server Tier | Patch Frequency | Reboot Window |
|---|---|---|
| Non-production | Weekly (automated) | Immediate on completion |
| Production — non-critical | Monthly (change-controlled) | Weekend 02:00–06:00 |
| Production — critical | Quarterly OR emergency (CVE ≥ 9.0) | Agreed maintenance window |
| Emergency (CVSS ≥ 9.0) | Within 72 hours | Emergency change process |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Linux — Deploy](../../deploy/)
