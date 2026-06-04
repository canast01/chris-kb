# vRNI Security Hardening

```bash
ssh ubuntu@vrni.example.local

sudo vim /etc/ssh/sshd_config
# Apply:
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers ubuntu

sudo systemctl restart sshd
```text
┌─────────────────────────────────────── vRNI Security Hardening ───────────────────────────────────────┐
│                                                                                                       │
│  Firewall rules, LDAPS enforcement, minimal accounts, and audit hardening for vRNI.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Hardening               │  │              Account Hardening              │   │
│   │           Allow only needed ports            │  │            Use LDAP/vIDM for auth           │   │
│   │            TCP 443: UI + API only            │  │          Disable unused local accts         │   │
│   │           UDP 2055: collector only           │  │          Rotate admin password 90d          │   │
│   │          Block SSH from prod CIDRs           │  │          Admin role: ops team only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Restrict network access and minimize accounts; enforce LDAPS and audit logging.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            LDAPS & MFA Hardening             │  │              Audit & Compliance             │   │
│   │            Enforce LDAPS port 636            │  │             Enable audit logging            │   │
│   │           MFA via vIDM integration           │  │          Log: login + config change         │   │
│   │          Validate CA cert for LDAPS          │  │             Forward logs to SIEM            │   │
│   │           No plain LDAP (port 389)           │  │           Review access quarterly           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; NSX or physical firewall; AD with LDAPS; SIEM for log ingestion                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LDAPS               = LDAP over TLS (port 636); prevents credential sniffing                         │
│  MFA                 = Multi-Factor Auth enforced at vIDM for all UI logins                           │
│  Firewall Rule       = Allow-list for vRNI: TCP 443, UDP 2055, TCP 5480 mgmt only                     │
│  Minimal Accounts    = Only required service accounts; no shared or personal creds                    │
│  Password Rotation   = 90-day cycle for admin@local and service accounts                              │
│  Audit Log           = Records all login events and configuration changes                             │
│  SIEM Forward        = Syslog export of audit events to centralized security tool                     │
│  Port 389 Disable    = Block plain LDAP; force all auth over LDAPS port 636                           │
│  Break-glass Account = Local admin kept secure and documented; rarely used                            │
│  Quarterly Review    = Periodic check of user list, roles, and token validity                         │
│  CA Cert Validation  = Verify LDAP server cert against trusted CA in vRNI settings                    │
│  SSH Restriction     = Limit SSH to jump host CIDR only; disable for non-admins                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# On Platform VM, if no external firewall:
sudo iptables -A INPUT -p tcp --dport 443 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j DROP
sudo iptables-save > /etc/iptables/rules.v4
```
```bash
sudo vim /etc/nginx/nginx.conf
# Set:
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;

sudo nginx -t && sudo systemctl reload nginx
```
```yaml
Settings → Notifications → Syslog
  Protocol: TCP
  Host: siem.example.local
  Port: 514
  Format: RFC 5424
Enable: Audit events, Alert notifications
```
```bash
# Check current expiry
echo | openssl s_client -connect vrni.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate

# Renew 30 days before expiry via Settings → SSL Certificate → Upload
```
