# Cisco DCNM — Hardening

> Part of the [Cisco DCNM](../../index.md) reference.

---

## Overview

This page defines the security baseline for Cisco DCNM 11.x. Apply during initial deployment and validate quarterly. Controls apply to both the DCNM application and its underlying Linux OS.

---

## 1. Change Default Credentials

```bash
ssh root@dcnm-dc1.corp.example.com

# Change default admin password via DCNM GUI first:
# Administration > Security > Local User Management > admin > Change Password

# Change OS root password
passwd root
# Store in vault; treat as break-glass only

# Disable the default 'dcnm' local OS account if not needed
usermod -L dcnm   # lock (disable password login)
```

---

## 2. Restrict Management Network Access

```bash
# Configure firewalld to restrict access to management subnet only
systemctl enable --now firewalld

# Allow HTTPS from management subnet only
firewall-cmd --permanent --remove-service=https
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.10.0.0/24" port port="443" protocol="tcp" accept'

# Allow SSH from jump host / management subnet only
firewall-cmd --permanent --remove-service=ssh
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.10.0.0/24" service name="ssh" accept'

# Allow SNMP traps from switch subnets only
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.20.0.0/16" port port="162" protocol="udp" accept'

# Allow syslog from switch subnets
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.20.0.0/16" port port="514" protocol="udp" accept'

# Set default zone to drop all other traffic
firewall-cmd --permanent --set-default-zone=drop
firewall-cmd --reload

# Verify
firewall-cmd --list-all
```

---

## 3. SSH Hardening

```bash
vi /etc/ssh/sshd_config

# Apply:
Protocol 2
PermitRootLogin no        # use sudo from a non-root account
PasswordAuthentication yes
PubkeyAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
Banner /etc/issue.net

systemctl restart sshd
```

Configure SSH login banner:

```bash
cat > /etc/issue.net << 'EOF'
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited.
EOF
```

---

## 4. OS Patching

```bash
# Check available security updates
yum updateinfo list security

# Apply security patches
yum update --security -y

# Reboot if kernel update was applied
needs-restarting -r && echo "No reboot needed" || echo "Reboot required"

# After reboot, verify DCNM services restarted
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status
```

Apply OS security patches monthly. DCNM application upgrades follow Cisco's release schedule independently.

---

## 5. Disable Unused Services

```bash
# List all active services
systemctl list-units --type=service --state=active

# Disable services not required for DCNM
systemctl disable --now avahi-daemon
systemctl disable --now cups
systemctl disable --now bluetooth
systemctl disable --now postfix   # DCNM uses its own SMTP configuration

# Verify DCNM services are unaffected
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status
```

---

## 6. DCNM Application Hardening

### Authentication Settings

1. Navigate to **Administration > Security > Authentication**.
2. Set primary authentication to **LDAP** (or TACACS+).
3. Set fallback to **Local** for break-glass.
4. Enforce password policy (12+ chars, complexity, 90-day expiry).
5. Set session idle timeout to 15 minutes.
6. Enable audit logging.

### Remove Unused Local Accounts

After LDAP is configured and tested:
1. Navigate to **Administration > Security > Local User Management**.
2. Delete all accounts except the break-glass `admin` account.
3. Document the break-glass account password storage location.

### SNMPv3 on DCNM's Own SNMP Engine

If DCNM itself is monitored via SNMP from an NMS:

```bash
# On DCNM appliance, configure SNMPv3 for inbound NMS polling
# (DCNM acts as an SNMP agent for its own health)
# Navigate to Administration > SNMP Credentials
# Set: Auth protocol SHA, Priv protocol AES-128
# Remove any v1/v2c community strings
```

### Disable HTTP Redirect Only

Ensure DCNM does not serve plaintext HTTP. Port 80 should redirect to 443 only:

```bash
# Verify no plaintext content is served on port 80
curl -sk -o /dev/null -w "%{redirect_url}" http://dcnm-dc1.corp.example.com/
# Expected: redirect to https://...
```

---

## 7. NTP Configuration

```bash
# Verify NTP
timedatectl status
# Expected: synchronized: yes

# Configure NTP if not set
vi /etc/chrony.conf
# server 10.10.0.10 prefer
# server 10.10.0.11

systemctl enable --now chronyd
chronyc tracking
# Expect: reference from NTP server, offset < 50ms
```

---

## 8. Syslog and Audit Logging

```bash
# Forward DCNM OS syslog to SIEM
cat > /etc/rsyslog.d/dcnm-siem.conf << 'EOF'
*.* @@10.10.3.50:514    # TCP syslog to SIEM
EOF

systemctl restart rsyslog

# Test
logger -t dcnm-test "Syslog forwarding test message"
```

DCNM application audit log: **Administration > Logs > Audit Logs > Export**. Schedule a monthly audit log export to the SIEM if DCNM does not forward directly.

---

## Hardening Checklist

### OS and Network

- [ ] Default passwords changed; stored in vault
- [ ] SSH root login disabled (`PermitRootLogin no`)
- [ ] firewalld active; management subnet restrictions applied
- [ ] Unused OS services disabled
- [ ] OS security patches current (< 30 days for critical CVEs)
- [ ] NTP synchronized; offset < 100ms
- [ ] SSH login banner configured
- [ ] Syslog forwarding to SIEM active

### Application Security

- [ ] LDAP or TACACS+ configured and tested
- [ ] Local accounts limited to break-glass admin only
- [ ] Password policy enforced (12+ chars, 90-day rotation)
- [ ] Session idle timeout: 15 minutes
- [ ] Audit logging enabled
- [ ] TLS certificate from corporate CA (not self-signed)
- [ ] TLS 1.0 and 1.1 disabled

### Access Control

- [ ] RBAC roles assigned according to least privilege
- [ ] Fabric-level scoping applied for multi-site environments
- [ ] Service accounts documented; passwords in vault
- [ ] Quarterly access review scheduled

### Operational

- [ ] Backup schedule configured and tested (restore tested annually)
- [ ] Backup encryption enabled
- [ ] Pre-upgrade backup procedure documented and followed
- [ ] Certificate expiry monitored (< 30 days = alert)

---

## Periodic Review Schedule

| Review | Frequency |
|---|---|
| Full hardening checklist | Quarterly |
| OS security patching | Monthly |
| Break-glass password rotation | Quarterly |
| TLS certificate expiry | Monthly |
| User access review | Quarterly |
| Audit log review | Monthly |
| DCNM application upgrade | Align with Cisco advisory and EoL notices |
