# Aria Operations — Hardening

```text
┌─────────────────────────────────────────────────────────────┐
│            Aria Operations Hardening Layers                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Account Hardening                                   │   │
│  │  • admin password changed → vault                    │   │
│  │  • No local admin for day-to-day; named AD accounts  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Certificate                                         │   │
│  │  • Replace self-signed with CA-signed cert           │   │
│  │  • Monitor expiry; alert at 60 days                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  LDAP/SSH                                            │   │
│  │  • LDAPS port 636 only (no plain LDAP)              │    │
│  │  • SSH: restricted to mgmt CIDR via hosts.allow     │    │
│  │  • Root: key-based only (PermitRootLogin prohibit)  │    │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Syslog + Compliance                                 │   │
│  │  • Syslog → Aria Ops for Logs / SIEM  :514          │    │
│  │  • VM disk encryption (vSAN or SAN layer)           │    │
│  │  • NTP delta < 1 second (chronyc tracking)          │    │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Default Account Hardening

Change the `admin` password immediately after deployment:

1. **Administration → Access Control → User Accounts → admin → Reset Password**
2. Use a minimum 16-character password with mixed case, numbers, and symbols
3. Store in an enterprise vault (CyberArk, HashiCorp Vault)
4. Do not use the `admin` local account for day-to-day operations — create named AD-backed accounts for all users

---

## Replace Self-Signed Certificate

Aria Operations ships with a self-signed certificate. Replace it before exposing the UI or API to any users.

```bash
# Verify current certificate subject and expiry
echo | openssl s_client -connect vrops-prod-01.example.local:443 2>/dev/null | \
  openssl x509 -noout -subject -dates -issuer

# Confirm it is self-signed (Issuer == Subject)
```

Replace via: **Administration → Certificates → Replace Certificate** (or via LCM Locker for LCM-managed deployments).

---

## LDAPS (Encrypted LDAP)

Never configure Active Directory over plain LDAP (port 389) in production. Use LDAPS (port 636) with a valid domain CA certificate.

Import the AD CA certificate before configuring the authentication source:

```text
Administration → Certificates → Import Certificate → paste the root CA PEM
```

Then configure the AD source with port 636 and SSL enabled.

```bash
# Verify LDAPS connectivity from the Aria Operations appliance
openssl s_client -connect dc01.example.local:636 -CAfile /tmp/corp-ca.pem 2>&1 | \
  grep -E "Verify return code|subject="
# Expected: Verify return code: 0 (ok)
```

---

## SSH Access Restriction

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

---

## Network Segmentation

Deploy Aria Operations nodes on a dedicated management network segment with strict firewall rules:

| Source | Destination | Port | Justification |
|---|---|---|---|
| Admin workstations / PAW | Aria Ops UI | 443 | UI access |
| Aria Ops | vCenter | 443 | vSphere adapter |
| Aria Ops | NSX Manager | 443 | NSX adapter |
| Aria Ops | ESXi hosts | 443 | Host metrics |
| Aria Ops | SMTP relay | 25/587 | Alert notifications |
| Aria Ops | LDAP/AD | 636 | Authentication |
| Aria Ops | NTP server | 123/UDP | Time sync |
| Remote Collectors | Aria Ops Primary | 4505, 4506 | Collector registration |
| Aria Ops cluster nodes | Each other | 9543, 10010 | Cluster replication |

Block all direct internet access from Aria Operations nodes — use a proxy for any outbound update checks.

---

## Audit Logging

Enable syslog forwarding to Aria Operations for Logs (or SIEM) for all audit events:

```bash
# Configure syslog forwarding from Aria Operations appliance
cat >> /etc/rsyslog.d/vrops-remote.conf << 'EOF'
*.* @@vrli-prod-01.example.local:514
EOF
systemctl restart rsyslog
```

Aria Operations also logs user actions to its internal audit log:

```bash
# View authentication and admin action logs on the appliance
tail -f /data/vcops/log/casa.log | grep -i "login\|logout\|admin\|role"
```

---

## Hardening Checklist

- [ ] Admin local password changed and stored in vault
- [ ] Self-signed certificate replaced with CA-signed certificate
- [ ] LDAP source configured over LDAPS (port 636) — plain LDAP disabled
- [ ] All users access via named AD accounts — local `admin` account not used for routine access
- [ ] AD groups mapped to roles — no individual user role assignments
- [ ] SSH restricted to management network CIDR
- [ ] Root SSH requires key-based authentication
- [ ] Syslog forwarding to Aria Ops for Logs / SIEM active
- [ ] Firewall rules reviewed — only required ports open between Aria Ops and monitored systems
- [ ] Aria Operations software at current patch level
- [ ] VM disk encryption enabled at storage layer (vSAN or SAN)
- [ ] NTP time delta < 1 second: `chronyc tracking` on each node
