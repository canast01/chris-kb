# Aria Ops for Logs — Hardening


<div class="kb-summary">
Hardening reference covering Default Account Hardening, LDAPS-Only Authentication, SSH Hardening, Firewall Rules, Syslog Output for Audit and 1 more sections.
</div>

## Default Account Hardening

Change the `admin` password immediately after completing the setup wizard:

```text
Administration → Authentication → Local Users → admin → Edit → Change Password
```
```
┌──────────────────────────────── Aria Operations for Logs — Hardening ─────────────────────────────────┐
│                                                                                                       │
│  Harden vRLI with TLS syslog, firewall restrictions, minimal admin accounts, and audit.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Hardening               │  │               Access Hardening              │   │
│   │          Use TLS 6514, not UDP 514           │  │       Minimum accounts: disable unused      │   │
│   │       Firewall: UI (443) mgmt-net only       │  │       Admin password: strong + rotated      │   │
│   │         VAMI (9543): jump host only          │  │       LDAP: use LDAPS (636), not plain      │   │
│   │       SSH: disable after initial setup       │  │        MFA via vIDM if SSO configured       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Audit and monitoring settings ensure log integrity and compliance for vRLI itself.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Configuration Hardening            │  │             Audit and Compliance            │   │
│   │       Disable TLS 1.0/1.1 on all ports       │  │          Syslog vRLI itself to SIEM         │   │
│   │     CA-signed cert; no self-signed prod      │  │       Admin action audit in vRLI logs       │   │
│   │     NTP: synced for log timestamp trust      │  │        VMware STIG: apply vRLI guide        │   │
│   │     No plaintext syslog from prod hosts      │  │      Log retention: meet compliance min     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · management VLAN · firewall · vIDM (SSO+MFA) · AD LDAPS · CA                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  UDP 514 disable   = UDP syslog provides no encryption or auth; replace with TLS 6514                 │
│  VAMI restriction  = Restrict port 9543 to jump hosts only; avoid internet exposure                   │
│  SSH disable       = SSH to vRLI appliance disabled post-setup; use VAMI for maintenance              │
│  LDAPS             = LDAP over TLS; prevents AD credential sniffing                                   │
│  Self-signed cert  = Acceptable in lab; production requires CA-signed cert                            │
│  VMware STIG       = Security hardening guide; follow applicable controls for vRLI                    │
│  Log vRLI to SIEM  = vRLI forwards its own admin audit events to Splunk/SIEM                          │
│  Timestamp trust   = NTP sync ensures log timestamps are accurate; critical for forensics             │
│  Compliance min    = Many regulations require ≥90d hot + 1yr archive log retention                    │
│  TLS 1.0/1.1       = Deprecated protocols; disable in vRLI SSL config                                 │
│  Admin audit       = vRLI logs all login, config change events in runtime.log                         │
│  MFA enforcement   = Handled by vIDM access policy if vRLI uses SSO                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## LDAPS-Only Authentication

Disable plain LDAP (port 389) for AD authentication — always use LDAPS (port 636):

1. Import the domain CA certificate: **Administration → SSL → Import Certificate**
2. Configure AD with port 636 and **Use SSL: Yes**
3. Test the connection before saving
4. Firewall: block outbound TCP 389 from the Aria Ops for Logs appliance to domain controllers

---

## SSH Hardening

```bash
# Restrict SSH to the management network
echo "sshd: 10.0.1.0/24" >> /etc/hosts.allow
echo "ALL: ALL" >> /etc/hosts.deny

# Disable root password login
# Edit /etc/ssh/sshd_config:
PermitRootLogin prohibit-password
PasswordAuthentication no   # Only after SSH keys are configured

systemctl restart sshd
```

---

## Firewall Rules

| Source | Destination Port | Protocol | Purpose |
|---|---|---|---|
| Admin workstations | 443 | TCP | Web UI and API |
| Admin workstations | 22 | TCP | SSH (restrict to PAW/jump host) |
| ESXi hosts | 514 | UDP | Syslog from ESXi |
| vCenter | 514 | UDP | vCenter syslog |
| NSX nodes | 514 | UDP | NSX syslog |
| LI Agent endpoints | 9543 | TCP | cfapi/TLS agent protocol |
| Generic TCP syslog sources | 1514 | TCP | Reliable syslog |
| SNMP trap sources | 162 | UDP | Network device traps |
| Aria Ops for Logs → SMTP relay | 25/587 | TCP | Alert notifications |
| Aria Ops for Logs → LDAP/AD | 636 | TCP | LDAPS authentication |
| Aria Ops for Logs → Aria Ops | 443 | TCP | Bi-directional integration |
| Aria Ops for Logs → NFS archive | 2049 | TCP | Log archiving |

Block all other inbound ports. Aria Ops for Logs does not require any inbound internet access.

---

## Syslog Output for Audit

Forward the Aria Ops for Logs appliance's own system logs to a SIEM or separate log repository — a log analytics platform should not be its own audit log store:

```bash
cat > /etc/rsyslog.d/vrli-audit.conf << 'EOF'
# Forward all syslog to SIEM
*.* @@siem.example.local:514
EOF
systemctl restart rsyslog
```

---

## Hardening Checklist

- [ ] Admin password changed and stored in vault
- [ ] Self-signed certificate replaced with CA-signed certificate
- [ ] LDAPS configured (port 636); domain CA imported
- [ ] AD groups mapped to roles — local accounts used only for break-glass
- [ ] SSH restricted to management network CIDR
- [ ] Firewall rules reviewed — only log ingestion ports open from appropriate sources
- [ ] Syslog output to SIEM configured and verified
- [ ] TLS 1.0 and 1.1 confirmed disabled
- [ ] LI Agent connections use cfapi/TLS (port 9543), not unencrypted port 9000
- [ ] Aria Ops for Logs software at current patch level
- [ ] VM disk encryption enabled at storage layer
- [ ] NTP configured and delta < 1 second: `chronyc tracking`
- [ ] SNMP trap receiver enabled only if network devices are configured to send traps; disabled otherwise
