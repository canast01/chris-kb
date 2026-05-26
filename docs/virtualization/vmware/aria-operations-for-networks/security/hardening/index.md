# Aria Operations for Networks — Hardening

---

## Post-Deployment Checklist

| Control | Action | Priority |
|---|---|---|
| Change default admin password | Settings → My Account → Change Password | Critical |
| Replace self-signed TLS certificate | Settings → SSL Certificate | High |
| Enable LDAP/AD authentication | Settings → Authentication → LDAP | High |
| Create read-only service accounts | vCenter and NSX — Read Only / Auditor roles | Critical |
| Restrict SSH to jump hosts only | Firewall or iptables | High |
| Configure syslog forwarding to SIEM | Settings → Notifications → Syslog | Medium |
| Set session timeout to 15 minutes | Settings → Security → Session Timeout | Medium |
| Remove unused data sources | Settings → Data Sources | Medium |
| Apply VM Encryption to Platform VM | vCenter storage policy | Medium |
| Review and revoke stale API tokens | Settings → API Tokens | Medium |

---

## SSH Hardening

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
```

Firewall rule: allow TCP 22 to Platform VM and Collector VMs from jump host subnet only.

---

## Least-Privilege Service Accounts

**vCenter (read-only):**
```text
vCenter → Administration → Global Permissions → Add
  User: svc-vrni-vc@corp.local | Role: Read Only | Propagate: Yes
```

**NSX-T (read-only):**
```text
NSX-T → System → User Management → Add User
  Username: svc-vrni-nsx | Role: Auditor
```

Never use admin-level credentials. vRNI only reads topology — no write access needed for monitoring.

---

## Network Access Restriction

Restrict Platform VM UI/API to management VLAN:

```bash
# On Platform VM, if no external firewall:
sudo iptables -A INPUT -p tcp --dport 443 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j DROP
sudo iptables-save > /etc/iptables/rules.v4
```

---

## TLS Hardening

```bash
sudo vim /etc/nginx/nginx.conf
# Set:
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;

sudo nginx -t && sudo systemctl reload nginx
```

---

## SIEM / Syslog Integration

```yaml
Settings → Notifications → Syslog
  Protocol: TCP
  Host: siem.example.local
  Port: 514
  Format: RFC 5424
Enable: Audit events, Alert notifications
```

Key events to alert on:
- Failed login (>3 attempts in 5 minutes)
- Role mapping changes
- Data source deletion
- API token creation / revocation
- Admin password change

---

## API Token Hygiene

- Assign minimum required role (Auditor for read-only monitoring)
- Set explicit expiry dates (90–365 days)
- Store in secrets manager (Vault, Key Vault) — never in scripts
- Revoke on personnel departure or role change
- Review quarterly: Settings → API Tokens

---

## Certificate Rotation

```bash
# Check current expiry
echo | openssl s_client -connect vrni.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate

# Renew 30 days before expiry via Settings → SSL Certificate → Upload
```

---

## Regular Audit Schedule

| Frequency | Action |
|---|---|
| Weekly | Review open problems and unacknowledged alerts |
| Monthly | Verify all expected data sources healthy; check disk usage |
| Quarterly | Review user list, rotate API tokens, test syslog delivery |
| Annually | Renew TLS certificate; review firewall rules; update service account passwords |
