# Aria Operations Security Hardening

```bash
# Verify current certificate subject and expiry
echo | openssl s_client -connect vrops-prod-01.example.local:443 2>/dev/null | \
  openssl x509 -noout -subject -dates -issuer

# Confirm it is self-signed (Issuer == Subject)
```text
┌───────────────────────────────── Aria Operations Security Hardening ──────────────────────────────────┐
│                                                                                                       │
│  Network restrictions, MFA via vIDM, audit logging, and STIG hardening for vROps.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Hardening               │  │              Account Hardening              │   │
│   │         Firewall: allow TCP 443 only         │  │         Use vIDM/LDAP for all users         │   │
│   │           SSH: jump host CIDR only           │  │        admin@local: break-glass only        │   │
│   │         Port 5480: mgmt network only         │  │           Rotate local pw 90 days           │   │
│   │           Disable unused services            │  │            MFA enforced via vIDM            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Network and account hardening are foundational; audit and STIG are compliance layers.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Audit Logging                 │  │                STIG Hardening               │   │
│   │            Enable vROps audit log            │  │         Apply VMware STIG for vROps         │   │
│   │          Forward to SIEM via syslog          │  │         Disable unneeded OS services        │   │
│   │         Log: login + config changes          │  │          OS: CentOS hardening guide         │   │
│   │             Retain logs 90+ days             │  │          Validate with STIG viewer          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps VMs on vSphere; NSX/physical firewall; SIEM for log collection; vIDM for MFA                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Firewall Allow-list  = Restrict vROps to TCP 443, 5480; block all other inbound                      │
│  MFA                  = Multi-Factor Auth; enforced at vIDM layer for all logins                      │
│  Audit Log            = vROps internal log of user login and configuration changes                    │
│  SIEM Syslog          = Forward audit events to Splunk/Sentinel for correlation                       │
│  STIG                 = Security Technical Implementation Guide from DISA/VMware                      │
│  STIG Viewer          = Tool to assess and document STIG compliance findings                          │
│  Break-glass Account  = admin@local kept secure in vault; used only in emergency                      │
│  Password Rotation    = 90-day cycle for local and service accounts                                   │
│  SSH Restriction      = Allow SSH only from jump host CIDR; deny all other sources                    │
│  Port 5480            = VAMI; restrict to management network CIDR only                                │
│  Log Retention        = Minimum 90 days; match organisational compliance policy                       │
│  Unused Services      = Disable OS services not needed; reduce attack surface                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Limit SSH access to the management network
# Edit /etc/hosts.allow on the Aria Operations appliance
echo "sshd: 10.0.1.0/24" >> /etc/hosts.allow
echo "ALL: ALL" >> /etc/hosts.deny

# Disable root password login (prefer key-based)
# Edit /etc/ssh/sshd_config
PermitRootLogin prohibit-password
systemctl restart sshd
```
```bash
# Configure syslog forwarding from Aria Operations appliance
cat >> /etc/rsyslog.d/vrops-remote.conf << 'EOF'
*.* @@vrli-prod-01.example.local:514
EOF
systemctl restart rsyslog
```
```bash
# View authentication and admin action logs on the appliance
tail -f /data/vcops/log/casa.log | grep -i "login\|logout\|admin\|role"
```
