# Aria Suite Lifecycle — Hardening

```
  LCM Hardening Controls
┌──────────────────────────────────────────────────────────────┐
│  Credentials                 SSH                             │
│  ┌──────────────────────┐    ┌──────────────────────────┐    │
│  │ admin@local: change  │    │ PermitRootLogin:         │    │
│  │  immediately, vault  │    │  prohibit-password       │    │
│  │ Locker Master PW:    │    │ Restrict to mgmt CIDR:   │    │
│  │  offline vault only  │    │  /etc/hosts.allow        │    │
│  └──────────────────────┘    └──────────────────────────┘    │
│                                                              │
│  Certificates               Network / Firewall               │
│  ┌──────────────────────┐    ┌──────────────────────────┐    │
│  │ All via Locker only  │    │ Inbound: 443 (UI/API)    │    │
│  │ RSA 4096-bit min     │    │          22 (SSH only    │    │
│  │ Full chain import    │    │           from PAW/jump) │    │
│  │ TLS 1.0/1.1 disabled │    │ Outbound: vCenter 443    │    │
│  └──────────────────────┘    │  VIDM 443 / NFS 2049     │    │
│                              └──────────────────────────┘    │
│  VIDM for all interactive users; no shared local accounts    │
└──────────────────────────────────────────────────────────────┘
```

## Default Password Change

Change the default `admin@local` password immediately after deployment:

1. LCM → Settings → Local Users → admin → **Change Password**
2. Use a minimum 16-character password with mixed case, numbers, and symbols
3. Store the new password in CyberArk or an enterprise vault — never in a shared document

**Locker Master Password**: set during initial LCM configuration wizard. If lost, all certificates and passwords stored in the Locker become inaccessible and require full re-import from source. Store this password in an offline vault (paper or HSM), not in the same digital system as other passwords.

---

## Certificate Management via Locker

All product certificates must be managed through the LCM Locker — not by direct file replacement on appliances. Direct file replacement bypasses LCM's tracking and breaks upgrade workflows.

```
LCM → Locker → Certificates → Import Certificate
```

- Import the full chain: leaf certificate + intermediate CA(s) + root CA
- Private key must be unencrypted (no passphrase) in PEM format
- Minimum key size: RSA 4096-bit for new certificates; RSA 2048-bit is the floor for existing
- Certificate must include SAN for all node FQDNs and the load balancer VIP

---

## SSH Hardening on the LCM Appliance

```bash
# Disable password authentication for root (prefer key-based)
# Edit /etc/ssh/sshd_config
PermitRootLogin prohibit-password
PasswordAuthentication no   # Only if SSH keys are pre-configured

# Restrict SSH to the management network
AllowUsers admin root
# OR use /etc/hosts.allow:
sshd: 10.0.1.0/24  # management network CIDR only

# Restart SSH after changes
systemctl restart sshd
```

---

## TLS Configuration

Ensure LCM does not expose weak TLS versions or cipher suites:

```bash
# Verify TLS version from an external client
openssl s_client -connect lcm-prod-01.corp.local:443 -tls1_2 2>/dev/null | grep "Protocol"
openssl s_client -connect lcm-prod-01.corp.local:443 -tls1   2>/dev/null | grep "alert"
# TLS 1.0 and 1.1 should return an alert — not supported in hardened deployments

# Check the cipher suite negotiated
openssl s_client -connect lcm-prod-01.corp.local:443 -tls1_3 2>/dev/null | grep "Cipher"
```

LCM 8.x ships with TLS 1.2+ enabled by default. Verify no legacy cipher suites are active using an external scanner such as `testssl.sh` or Qualys SSL Labs.

---

## Firewall Rules for LCM

Only necessary ports should be open to the LCM appliance:

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| Admin workstations | LCM appliance | 443 | TCP | Web UI and API |
| Admin workstations | LCM appliance | 22 | TCP | SSH (restrict to PAW/jump host) |
| LCM appliance | vCenter | 443 | TCP | vCenter API for VM deployment |
| LCM appliance | VIDM | 443 | TCP | SSO and group sync |
| LCM appliance | ESXi hosts | 443 | TCP | OVA deployment |
| LCM appliance | NFS server | 2049 | TCP/UDP | Binary repository |
| LCM appliance | DNS server | 53 | UDP | Name resolution |
| LCM appliance | NTP server | 123 | UDP | Time synchronisation |
| LCM appliance | SMTP relay | 25/587 | TCP | Email notifications |
| Product appliances | LCM appliance | 443 | TCP | Upgrade agent callback |

Close all other inbound ports at the network firewall. LCM does not require inbound access from the internet.

---

## Hardening Checklist

Run this checklist after initial deployment and after each major upgrade:

- [ ] `admin@local` password changed from default and stored in vault
- [ ] Locker Master Password stored in offline vault
- [ ] Root SSH login requires key-based authentication (no password SSH for root)
- [ ] SSH access restricted to management network CIDR only
- [ ] TLS 1.0 and 1.1 confirmed disabled (test with `openssl s_client -tls1`)
- [ ] Self-signed certificate replaced with CA-signed certificate in Locker
- [ ] VIDM integration configured — all interactive users authenticate via VIDM, not local accounts
- [ ] AD groups mapped to LCM roles (not individual user accounts)
- [ ] NFS binary repository mounted read-write only from LCM appliance IP (NFS export permission)
- [ ] Syslog forwarding to Aria Ops for Logs or SIEM configured and verified
- [ ] Firewall rules reviewed — only required ports open
- [ ] LCM software at current patch level (check: **LCM → Settings → System Details**)
