# Aria Suite Lifecycle — Hardening


<div class="kb-summary">
Hardening reference covering SSH Hardening on the LCM Appliance, TLS Configuration, Firewall Rules for LCM, Hardening Checklist.
</div>

  LCM Hardening Controls
```
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
┌────────────────────────────────── Aria Suite LCM Security Hardening ──────────────────────────────────┐
│                                                                                                       │
│  Firewall rules, MFA via vIDM, minimal SSH access, and audit hardening for LCM.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Hardening               │  │              Account Hardening              │   │
│   │         Firewall: allow TCP 443 only         │  │          vIDM SSO: no local logins          │   │
│   │           Port 5480: mgmt net only           │  │         admin@local: vault + rotate         │   │
│   │           SSH: jump host CIDR only           │  │            MFA enforced via vIDM            │   │
│   │          Block direct internet LCM           │  │          Locker: strong encryption          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Restrict LCM network access; enforce vIDM MFA; audit all LCM admin actions.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Audit Logging                 │  │               Depot Hardening               │   │
│   │             Enable LCM audit log             │  │          Offline depot: no internet         │   │
│   │            Forward to SIEM syslog            │  │             Verify PAK checksums            │   │
│   │          Log: all deploy + cert ops          │  │          NFS depot: restrict mount          │   │
│   │             Retain logs 90+ days             │  │           No direct depot internet          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; NSX/physical firewall; vIDM for MFA; SIEM for audit logs                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Firewall Allow-list  = TCP 443 and 5480 only; deny all other inbound to LCM                          │
│  MFA                  = Multi-Factor Auth at vIDM; all LCM logins go through vIDM                     │
│  Minimal SSH          = SSH only from jump host CIDR; disable for all others                          │
│  LCM Locker           = Encrypted credential store; restrict Locker admin access                      │
│  admin@local          = Local break-glass account; rotate every 90 days                               │
│  Audit Log            = LCM records all deployments, upgrades, cert operations                        │
│  SIEM Forward         = Export LCM audit syslog to centralised security tool                          │
│  Offline Depot        = Local NFS depot; no LCM internet access needed                                │
│  PAK Checksum         = Verify SHA hash of PAK file before upload to depot                            │
│  NFS Restrict         = Mount depot NFS read-only; restrict to LCM IP only                            │
│  Port 5480 Restrict   = Allow VAMI only from management network CIDR                                  │
│  Log Retention        = 90 days minimum; match compliance policy                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## TLS Configuration

Ensure LCM does not expose weak TLS versions or cipher suites:

```bash
# Verify TLS version from an external client
openssl s_client -connect lcm-prod-01.example.local:443 -tls1_2 2>/dev/null | grep "Protocol"
openssl s_client -connect lcm-prod-01.example.local:443 -tls1   2>/dev/null | grep "alert"
# TLS 1.0 and 1.1 should return an alert — not supported in hardened deployments

# Check the cipher suite negotiated
openssl s_client -connect lcm-prod-01.example.local:443 -tls1_3 2>/dev/null | grep "Cipher"
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
