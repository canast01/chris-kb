# Linux Security

## CIS Benchmark Hardening

All Linux servers are hardened to CIS Benchmark Level 1 at provisioning using an Ansible hardening role. Level 2 controls are reviewed and applied where operationally feasible.

Key controls applied automatically:

| Control | RHEL 9 | Ubuntu 22.04 |
|---|---|---|
| SSH hardening | Key-only, no root, restricted ciphers | Same |
| sudo policy | AD group-based, no NOPASSWD | Same |
| Audit logging | auditd with CIS ruleset | auditd with CIS ruleset |
| MAC | SELinux enforced | AppArmor profiles |
| Host firewall | firewalld zones | ufw rules |
| File integrity | AIDE daily scan | AIDE daily scan |
| Password policy | PAM pam_pwquality | PAM pwquality |

## SSH Hardening

```bash
# /etc/ssh/sshd_config — enforced via Ansible
PermitRootLogin no
PasswordAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
AllowAgentForwarding no
X11Forwarding no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Approved ciphers and MACs
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,chacha20-poly1305@openssh.com
MACs hmac-sha2-512,hmac-sha2-256
```

## SELinux (RHEL)

```bash
# Verify SELinux is enforcing
getenforce      # Should show: Enforcing
sestatus        # Full status

# Check for denied operations in the last 24 hours
ausearch -m avc,user_avc -ts today | audit2why | head -50

# If a legitimate operation is being blocked, create a policy module:
audit2allow -a -M mypolicy
semodule -i mypolicy.pp
```

Never set SELinux to Permissive on production — investigate denials and create policy modules instead.

## AppArmor (Ubuntu)

```bash
# Check status
apparmor_status

# List profiles
aa-status | grep -E "enforced|complain"

# Check denials
dmesg | grep apparmor | grep DENIED
journalctl -k | grep apparmor | grep DENIED
```

## Audit Logging (auditd)

```bash
# Verify auditd is running
systemctl status auditd

# Search audit log for privilege escalation events
ausearch -m user_auth,user_acct -ts today | aureport -u

# Watch for suspicious commands
auditctl -w /etc/passwd -p wa -k identity_changes
auditctl -w /etc/sudoers -p wa -k sudoers_changes
auditctl -w /bin/su -p x -k priv_escalation
```

CIS auditd ruleset covers: file permission changes, privileged commands, network configuration changes, user and group management.

## Host Firewall

```bash
# RHEL firewalld — check active rules
firewall-cmd --list-all

# Allow a specific service
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-port=9100/tcp   # node_exporter
firewall-cmd --reload

# Ubuntu ufw
ufw status verbose
ufw allow ssh
ufw deny from <suspicious-ip>
ufw enable
```

## AIDE File Integrity

```bash
# Initialize AIDE database after provisioning (baseline)
aide --init && mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz

# Run daily check via cron
aide --check > /var/log/aide/aide_$(date +%Y%m%d).log

# Review changes
grep -v "^$" /var/log/aide/aide_$(date +%Y%m%d).log
```

Any unexpected file changes should be investigated immediately.

## Security Hardening Checklist

- [ ] SSH key-only authentication configured
- [ ] Root login disabled
- [ ] SELinux enforcing (RHEL) / AppArmor enforced (Ubuntu)
- [ ] firewalld/ufw active; only required ports open
- [ ] auditd running with CIS ruleset
- [ ] AIDE initialized and daily scan cron active
- [ ] All local user accounts reviewed (no stale accounts)
- [ ] Syslog forwarding to SIEM confirmed
- [ ] All non-essential services disabled: `systemctl list-unit-files --state=enabled`
- [ ] Kernel parameters hardened: `sysctl -a | grep -E "accept_redirects|rp_filter|syn_cookies"`
