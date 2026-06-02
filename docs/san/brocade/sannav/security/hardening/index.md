# SANnav — Hardening


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

---

## Overview

Hardening the SANnav appliance reduces the attack surface of the management plane. Apply this baseline during initial deployment and validate quarterly. The SANnav appliance is a Linux VM — hardening applies both to SANnav application configuration and to the underlying OS.

---

## 1. Replace Default Credentials

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

---

## 4. SSH Hardening

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

---

## 5. OS Patching

The SANnav appliance OS (CentOS/RHEL based) requires security patching independently of SANnav application upgrades:

```bash
# Check for available security updates
sudo yum updateinfo list security

# Apply security patches only (does not touch SANnav application packages)
sudo yum update --security -y

# Verify SANnav services still running after OS update
sannav status
```

Patch the OS quarterly at minimum. Critical OS CVEs (CVSS 9.0+) should be patched within 30 days of publication.

---

## 6. NTP Synchronization

Correct time is essential for log correlation, event timestamps, and certificate validity:

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

---

## 7. SANnav Application Hardening

### Disable Unused Authentication Methods

If LDAP is configured and working, disable local account login for all accounts except break-glass:

1. Navigate to **Administration > Security Settings > Authentication**.
2. Set primary authentication method to **LDAP**.
3. Set fallback to **Local** (required for break-glass when LDAP is unavailable).

### Session Hardening

Navigate to **Administration > Security Settings > Session**:
- Idle timeout: 15 minutes
- Absolute timeout: 8 hours
- Concurrent sessions per user: 2

### API Token Controls

REST API tokens inherit the session idle timeout. For automation accounts:
- Use dedicated service accounts (`svc-monitor`, `svc-automation`)
- Ensure scripts always call `/rest/logout` — uncleaned sessions count against the concurrent session limit
- Monitor for long-lived sessions in **Administration > Audit Log** (filter: LOGIN events without corresponding LOGOUT)

---

## 8. Login Banner

Configure a legal warning banner for the SANnav web UI:

1. Navigate to **Administration > Security Settings > Login Banner**.
2. Enter the banner text:

```text
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited and may be subject to legal action.
```

3. Click **Save**. The banner appears on the SANnav login page.

For SSH access, configure the OS banner:

```bash
sudo vi /etc/issue.net
# Add:
# WARNING: Authorized access only. All activities are monitored and logged.

sudo vi /etc/ssh/sshd_config
# Banner /etc/issue.net
sudo systemctl restart sshd
```

---

## Hardening Checklist

### Appliance Access

- [ ] Default admin password changed; stored in vault
- [ ] SSH restricted to management subnet via firewalld rich rule
- [ ] PermitRootLogin no in sshd_config
- [ ] SSH banner configured
- [ ] Unused OS services disabled

### Application Security

- [ ] LDAP configured; LDAP role mappings applied
- [ ] Local accounts limited to break-glass only
- [ ] Password policy enforced (12+ chars, complexity, 90-day rotation)
- [ ] Account lockout configured (5 attempts, 30-minute lockout)
- [ ] Session idle timeout: 15 minutes
- [ ] Login banner visible on SANnav login page

### Encryption

- [ ] TLS certificate from corporate CA (not self-signed)
- [ ] TLS 1.0 and 1.1 disabled; TLS 1.2/1.3 only
- [ ] LDAPS (port 636) used; not plain LDAP
- [ ] Backup encryption enabled; passphrase in vault

### Patching

- [ ] SANnav application at latest minor/patch release
- [ ] OS security patches applied within last 90 days
- [ ] NTP synchronized; clock offset < 100ms

### Monitoring

- [ ] Syslog forwarding configured to SIEM
- [ ] SANnav audit log reviewed quarterly
- [ ] Failed login alerting configured in SIEM

---

## Periodic Review Schedule

| Review | Frequency |
|---|---|
| Hardening checklist | Quarterly |
| Break-glass password rotation | Quarterly |
| OS security patching | Monthly (critical CVEs within 30 days) |
| TLS certificate expiry check | Monthly |
| User access review | Quarterly |
| SANnav application upgrade | Align with Broadcom release cycle |
