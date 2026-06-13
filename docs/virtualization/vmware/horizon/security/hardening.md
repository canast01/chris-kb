---
tags:
  - horizon
  - security
  - vmware
---
# Horizon — Hardening


<div class="kb-summary">
Hardening reference covering Windows Hardening of Connection Server, UAG Hardening, USB Redirection Policy, Clipboard Direction Restriction, Drive Mapping Restriction and 3 more sections.

*Applies to: Horizon 8.x*
</div>

  Hardening Checklist Coverage
```text
┌───────────────────────────────────── VMware Horizon — Hardening ──────────────────────────────────────┐
│                                                                                                       │
│  Horizon hardening follows the VMware Horizon Security Hardening Guide: TLS enforcement,              │
│  MFA, network isolation, session timeout, and audit logging.                                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Hardening               │  │              Session Hardening              │   │
│   │            Desktop VLAN: isolated            │  │           Session timeout: 8h max           │   │
│   │           DMZ: UAG only, port 443            │  │            Disconnect timeout: 1h           │   │
│   │          No direct CS from internet          │  │         Logoff on disconnect: enable        │   │
│   │            Firewall: CS mgmt only            │  │           USB: restrict or disable          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  UAG as the only external entry point is the most important network control.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Auth Hardening                │  │              Audit & Compliance             │   │
│   │            MFA: RADIUS/RSA on UAG            │  │            Events DB: all logins            │   │
│   │           TLS 1.2 minimum: enforce           │  │          Syslog: CS events to SIEM          │   │
│   │         Smart card: enforce for govt         │  │          SIEM: login failure alerts         │   │
│   │           SSO: Workspace ONE + MFA           │  │         Quarterly: entitlement audit        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Desktop VMs run on dedicated ESXi hosts with isolated VLAN; Connection Server VMs                    │
│  on management network; UAG in DMZ; profile shares on NAS.                                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Session timeout= max session age; logoff user after 8h inactivity                                    │
│  Disconnect timeout= auto-logoff disconnected sessions after 1h                                       │
│  Logoff on disconnect= destroy instant clone on disconnect for security                               │
│  USB restrict  = limit USB redirection to approved device classes                                     │
│  DMZ           = demilitarised zone; UAG sits here with dual NIC                                      │
│  Events DB     = Horizon SQL event log; login/session/admin events                                    │
│  SIEM          = Security Info and Event Mgmt; receives CS syslog                                     │
│  TLS 1.2       = minimum; disable TLS 1.0/1.1 in CS config                                            │
│  MFA           = Multi-Factor Auth; configured on UAG                                                 │
│  Entitlement audit= check all pool entitlements; remove stale groups                                  │
│  RADIUS        = MFA backend; OTP from RSA/Duo/Okta                                                   │
│  Isolated VLAN = desktop VMs cannot reach management or other VLANs                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## UAG Hardening

```bash
# UAG Admin UI → Advanced Settings → TLS Settings
  SSL Ciphers: ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256
  TLS Versions: TLSv1.2,TLSv1.3

# UAG Admin UI → Advanced Settings → DoS Mitigation
  Enable DoS protection: Yes
  Max connections per client: 25 (reduce for restrictive environments)

# Restrict UAG admin UI to management IP only
  Admin Interface: bind to management NIC IP only
  Allow access from: management subnet CIDR
```

---

## USB Redirection Policy

```text
Group Policy → Computer Configuration → VMware Horizon Agent
  USB Redirection Enabled: No (disable entirely for highly regulated desktops)
  OR:
  Exclude Device Family: Storage,Bluetooth,SmartCard  (allow only specific devices)
  Include Device: <VID>_<PID>  (explicitly allow CAC reader by VID/PID)
```

---

## Clipboard Direction Restriction

```text
Group Policy → Computer Configuration → VMware Blast → Clipboard
  Clipboard Direction: Client to Agent only
  (Users can paste into the desktop but cannot copy out — prevents data exfiltration)
```

For kiosk or shared-terminal pools: set to Disabled entirely.

---

## Drive Mapping Restriction

```text
Group Policy → Computer Configuration → VMware Horizon Agent
  Client Drive Redirection: Disabled
```

Prevents users from mapping their local drives into the virtual desktop — eliminates a data exfiltration path.

---

## Disable Direct Console Access

Connection Server should not be accessible directly from desktop VMs:

```text
locked.properties:
  checkOrigin=true
  allowedHosts=<management-subnet>
```

Physical server hosting Connection Server should not be on the same VLAN as desktop VMs.

---

## Monitor Admin Events

```bash
Horizon Console → Monitor → Events
  Filter: Role = Administrator, Action = Configuration Change
  Export to CSV for audit trail
```

For automated monitoring, configure Events Database (SQL Server) and query it with scheduled reports.

---

## Security Hardening Checklist

| Control | Status Check |
|---|---|
| TLS 1.0/1.1 disabled on CS | `nmap --script ssl-enum-ciphers -p 443 horizon-cs01.example.local` |
| CA-signed cert on CS | `openssl s_client -connect horizon-cs01:443 \| openssl x509 -issuer` |
| CA-signed cert on UAG | `openssl s_client -connect uag:443 \| openssl x509 -issuer` |
| 2FA enabled for external access | Horizon Console → Settings → CS → Authentication |
| Clipboard restricted | GPO audit — verify policy applied to desktop OUs |
| USB storage blocked | GPO audit — verify Exclude Device Family includes Storage |
| Drive mapping disabled | GPO audit |
| CS admin UI restricted to mgmt VLAN | Test: access `https://horizon-cs01` from desktop VLAN |
| Events DB configured | Monitor → Events: confirm long history available |
