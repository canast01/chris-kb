# Cisco DCNM — Security Hardening

```bash
ssh root@dcnm-dc1.corp.example.com

# Change default admin password via DCNM GUI first:
# Administration > Security > Local User Management > admin > Change Password

# Change OS root password
passwd root
# Store in vault; treat as break-glass only

# Disable the default 'dcnm' local OS account if not needed
usermod -L dcnm   # lock (disable password login)
```text
┌─────────────────────────────────── Cisco DCNM — Security Hardening ───────────────────────────────────┐
│                                                                                                       │
│  DCNM hardening: disable defaults, enforce ISE TACACS+, TLS, RBAC, patch management.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Platform Hardening              │  │               Access Hardening              │   │
│   │        Change default admin password         │  │          ISE TACACS+: no local use          │   │
│   │           Disable HTTP; HTTPS only           │  │           RBAC: operator read-only          │   │
│   │           Firewall: port 443 only            │  │          API IP whitelist: restrict         │   │
│   │         TLS 1.2+ only; disable older         │  │           Session timeout: 30 min           │   │
│   │          Disable unused OS services          │  │               MFA via SAML SSO              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Change defaults day 1; restrict API; enforce ISE TACACS+ before production use.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Monitoring & Alert Hardening         │  │               Patch Management              │   │
│   │        Audit log: all actions logged         │  │            Quarterly DCNM upgrade           │   │
│   │          Failed logins: SIEM alert           │  │          Cisco PSIRT: check monthly         │   │
│   │         Config change: diff + alert          │  │          OS patches: monthly cycle          │   │
│   │             API token expiry: 8h             │  │            Backup before upgrade            │   │
│   │         Cert expiry: 60-day warning          │  │            Test in staging first            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM Linux VM · vSphere host · management-only VLAN · Cisco ISE appliance                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+        = minimum required; disable TLS 1.0/1.1 and SSL 3.0                                  │
│  ISE TACACS+     = Cisco ISE centralised CLI auth; all admin actions audited                          │
│  RBAC            = Role-Based Access Control; operator = read-only; admin = full                      │
│  IP whitelist    = restrict DCNM REST API to known source IP ranges                                   │
│  SAML SSO        = DCNM integrates with IdP; MFA enforced at identity provider                        │
│  Session timeout = idle GUI/API session terminated after 30 minutes                                   │
│  API token expiry= JWT expires after configurable period; 8h default                                  │
│  Cisco PSIRT     = Product Security Incident Response; Cisco security advisories                      │
│  Audit log       = all DCNM GUI and API calls logged with user and timestamp                          │
│  Config diff     = DCNM detects out-of-band zone changes and sends alert                              │
│  Cert expiry     = TLS certificate monitored; 60-day warning before expiry                            │
│  Staging test    = validate DCNM upgrade in non-prod before production rollout                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
