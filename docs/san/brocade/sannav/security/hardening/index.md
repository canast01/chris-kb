---
tags:
  - san
  - security
---
# Brocade SANnav — Security Hardening

```bash
# SSH to SANnav appliance
ssh admin@sannav-dc1.corp.example.com

# Change default admin password immediately after deployment
passwd admin
# Use a password that meets the corporate complexity policy (20+ characters)
# Store in vault; treat as break-glass

# Change default OS root password (if accessible)
sudo passwd root
```
```text
┌───────────────────────────────── Brocade SANnav — Security Hardening ─────────────────────────────────┐
│                                                                                                       │
│  SANnav hardening: disable defaults, TACACS+ enforce, TLS, RBAC, patch management.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Platform Hardening              │  │               Access Hardening              │   │
│   │        Replace default admin password        │  │         TACACS+: no local admin use         │   │
│   │           Disable HTTP; HTTPS only           │  │           RBAC: read-only for ops           │   │
│   │          Disable unused OS services          │  │         API: IP whitelist source IPs        │   │
│   │          OS firewall: port 443 only          │  │           Session timeout: 30 min           │   │
│   │         TLS 1.2+ only; disable older         │  │               MFA via SAML SSO              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Change defaults on day 1; restrict API access; enforce TACACS+ before production use.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Monitoring & Alerting             │  │          Patch & Update Management          │   │
│   │        Audit log: all actions logged         │  │           Quarterly SANnav upgrade          │   │
│   │         Failed logins: alert to SIEM         │  │           Check BCM PSIRTs monthly          │   │
│   │         Config changes: diff + alert         │  │          OS patches: monthly cycle          │   │
│   │         API token expiry: 8h default         │  │          Backup before any upgrade          │   │
│   │        Cert expiry monitor: 60d warn         │  │            Test in staging first            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav Linux VM · vSphere host · management-only VLAN · TACACS+ server                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+        = minimum required; disable TLS 1.0/1.1 and SSL 3.0                                  │
│  RBAC            = Role-Based Access Control; operator = read-only; admin = full                      │
│  IP whitelist    = restrict SANnav REST API to known source IP ranges                                 │
│  SAML SSO        = SANnav integrates with IdP; MFA enforced at IdP level                              │
│  Session timeout = idle GUI/API session terminated after 30 minutes                                   │
│  API token expiry= JWT expires after configurable period; 8 hours default                             │
│  PSIRT           = Product Security Incident Response; Broadcom security advisories                   │
│  Audit log       = all GUI clicks and API calls logged with user and timestamp                        │
│  Config diff     = SANnav detects out-of-band zone changes and alerts                                 │
│  Cert expiry     = TLS certificate monitored; 60-day warning before expiry                            │
│  OS patches      = SANnav VM runs Linux; apply OS patches on monthly cycle                            │
│  Staging test    = validate SANnav upgrade in non-prod before production rollout                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
sudo vi /etc/ssh/sshd_config

# Recommended settings:
Protocol 2
PermitRootLogin no
PasswordAuthentication yes     # or 'no' if using SSH key auth
PubkeyAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300        # disconnect idle sessions after 5 minutes
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
AllowUsers admin sannav        # restrict SSH to specific local accounts

sudo systemctl restart sshd

# Verify
sudo sshd -T | grep -E "permitrootlogin|passwordauthentication|protocol|maxauthtries"
```
```bash
# Check for available security updates
sudo yum updateinfo list security

# Apply security patches only (does not touch SANnav application packages)
sudo yum update --security -y

# Verify SANnav services still running after OS update
sannav status
```
```bash
# Check NTP synchronization
timedatectl status
# Expected: "synchronized: yes", NTP service active

# If not synchronized, configure NTP
sudo vi /etc/chrony.conf
# Add: server 10.10.0.10 prefer
#       server 10.10.0.11

sudo systemctl enable --now chronyd
chronyc tracking
# Expected: Reference ID should match your NTP server, offset < 1ms
```
```text
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited and may be subject to legal action.
```
```bash
sudo vi /etc/issue.net
# Add:
# WARNING: Authorized access only. All activities are monitored and logged.

sudo vi /etc/ssh/sshd_config
# Banner /etc/issue.net
sudo systemctl restart sshd
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

