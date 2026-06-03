# Aria Operations — Hardening


<div class="kb-summary">
Hardening reference covering Default Account Hardening, Replace Self-Signed Certificate, SSH Access Restriction, Network Segmentation, Audit Logging and 1 more sections.
</div>

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
