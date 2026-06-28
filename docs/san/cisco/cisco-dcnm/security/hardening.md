---
tags:
  - san
  - security
---
# Cisco DCNM — Security Hardening
![Cisco DCNM — Security Hardening](../../../../assets/san-cisco-cisco-dcnm-security-hardening.svg)

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

```bash
cat > /etc/issue.net << 'EOF'
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited.
EOF
```
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
```bash
# On DCNM appliance, configure SNMPv3 for inbound NMS polling
# (DCNM acts as an SNMP agent for its own health)
# Navigate to Administration > SNMP Credentials
# Set: Auth protocol SHA, Priv protocol AES-128
# Remove any v1/v2c community strings
```
```bash
# Verify no plaintext content is served on port 80
curl -sk -o /dev/null -w "%{redirect_url}" http://dcnm-dc1.corp.example.com/
# Expected: redirect to https://...
```
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
```bash
# Forward DCNM OS syslog to SIEM
cat > /etc/rsyslog.d/dcnm-siem.conf << 'EOF'
*.* @@10.10.3.50:514    # TCP syslog to SIEM
EOF

systemctl restart rsyslog

# Test
logger -t dcnm-test "Syslog forwarding test message"
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Cisco Dcnm — Authentication](../authentication/)
- [Cisco Dcnm — Access Control](../access-control/)
- [Cisco Dcnm — Encryption](../encryption/)
