# Linux Patching

Patch management procedures for RHEL 8/9 and Ubuntu 22.04 LTS servers.
## Pre-Patch Checklist

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

## RHEL — dnf Patching

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

## RHEL — yum history (Rollback)

```bash
# List recent transactions
yum history list | head -20

# View what a transaction did
yum history info <transaction-id>

# Undo a specific transaction (rollback)
yum history undo <transaction-id>
```

## Ubuntu — apt Patching

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

## Kernel Updates and Reboot

```bash
# Check if a reboot is required (RHEL)
needs-restarting -r
# Exit code 1 = reboot required

# Check if a reboot is required (Ubuntu)
ls /var/run/reboot-required 2>/dev/null && echo "Reboot required" || echo "No reboot needed"

# Check which processes need restart (Ubuntu)
needs-restarting 2>/dev/null || checkrestart   # Debian: apt install debian-goodies

# Verify new kernel is default after update
grub2-editenv list | grep saved_entry   # RHEL
grep GRUB_DEFAULT /etc/default/grub     # Ubuntu
```

## Red Hat Subscription and Repositories

```bash
# Check subscription status
subscription-manager status
subscription-manager list --consumed

# List enabled repos
dnf repolist enabled

# Enable a specific repo
subscription-manager repos --enable=rhel-9-for-x86_64-appstream-rpms

# Check RHEL version
cat /etc/redhat-release
```

## Ansible Patching at Scale

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

## Post-Patch Validation

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

## Patch Schedule Standards

| Server Tier | Patch Frequency | Reboot Window |
|---|---|---|
| Non-production | Weekly (automated) | Immediate on completion |
| Production — non-critical | Monthly (change-controlled) | Weekend 02:00–06:00 |
| Production — critical | Quarterly OR emergency (CVE ≥ 9.0) | Agreed maintenance window |
| Emergency (CVSS ≥ 9.0) | Within 72 hours | Emergency change process |
