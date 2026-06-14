---
tags:
  - active-directory
  - windows-server
  - networking
  - firewall
  - ports
  - identity
---
# Active Directory — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Microsoft Active Directory Domain Services. Covers client-to-DC authentication, DC-to-DC replication, DNS, LDAP, and Kerberos. Required for any firewall between clients and domain controllers, or between AD sites.

*Applies to: Windows Server 2019 / 2022 Active Directory*
</div>

```text
┌─────────────────────────── Active Directory — Network Traffic Zones ──────────────────────────────────┐
│                                                                                                       │
│  Client Zone                 Domain Controller Zone              AD Site B (Replication)              │
│  ─────────────               ────────────────────               ─────────────────────────             │
│  Windows clients ──88/389──► DC (Site A) ──135+dynamic──► DC (Site B, SYSVOL/AD replication)          │
│  Linux clients   ──88/389──► DC           ──53 UDP/TCP──► DC (DNS zone transfer)                      │
│  Applications    ──636 ────► DC                                                                       │
│  Admin           ──3389/5985► DC                                                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- Active Directory uses a large dynamic RPC port range (49152–65535) for replication and some admin operations — this is difficult to firewall without restricting the range via GPO
- Restrict the dynamic RPC range using the registry key `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters\TCP/IP Port` (or Group Policy) to narrow the range for inter-site replication firewalls
- All domain-joined systems need at minimum: 53 (DNS), 88 (Kerberos), 389 (LDAP), 445 (SMB) to reach a DC in their site
- LDAPS (636) is strongly preferred over LDAP (389) for any non-Windows client or application integration — enable and enforce via Group Policy or CA-signed DC certificates

---

## Client Authentication — All Domain-Joined Systems

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 53 | TCP/UDP | All domain-joined clients | DC (DNS server) | DNS — domain name resolution (required first) |
| 88 | TCP/UDP | All domain-joined clients | DC (KDC) | Kerberos authentication |
| 389 | TCP/UDP | All domain-joined clients | DC | LDAP — user and computer object queries |
| 445 | TCP | All domain-joined clients | DC | SMB — Group Policy application, SYSVOL access, NETLOGON |
| 135 | TCP | All domain-joined clients | DC | RPC endpoint mapper (Netlogon, trust operations) |
| 49152–65535 | TCP | All domain-joined clients | DC | Dynamic RPC (Netlogon, RPC-based admin) |
| 464 | TCP/UDP | All domain-joined clients | DC | Kerberos password change (kpasswd) |
| 123 | UDP | All clients | DC or NTP server | NTP — Kerberos requires ≤5 min clock skew |

---

## Application Integration (LDAP/LDAPS)

Non-Windows applications (Linux, vCenter, Nutanix, etc.) that integrate with AD for authentication:

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 636 | TCP | Application servers | DC | LDAPS — encrypted LDAP (preferred for all non-Windows integrations) |
| 389 | TCP | Application servers | DC | LDAP (plain-text — only if LDAPS not supported; add firewall encryption) |
| 3268 | TCP | Application servers | DC | Global Catalog LDAP (multi-domain environments) |
| 3269 | TCP | Application servers | DC | Global Catalog LDAPS (preferred) |
| 88 | TCP/UDP | Application servers | DC (KDC) | Kerberos (Linux Kerberos, NFS Kerberos, SMB Kerberos) |

---

## DNS (Domain Controller as DNS Server)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 53 | UDP | All DNS clients | DNS queries (standard — all queries under 512 bytes) |
| 53 | TCP | DNS resolvers, DCs | DNS queries over 512 bytes, zone transfers |

---

## DC-to-DC Replication (Intra-Site)

Intra-site replication is initiated by KCC using RPC over IP.

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 135 | TCP | DC ↔ DC | RPC endpoint mapper (replication setup) |
| 49152–65535 | TCP | DC ↔ DC | Dynamic RPC — AD replication data |
| 389 | TCP/UDP | DC ↔ DC | LDAP replication |
| 445 | TCP | DC ↔ DC | SMB — SYSVOL/NETLOGON DFS replication (DFSR) |

---

## DC-to-DC Replication (Inter-Site — Across Firewall)

For inter-site replication through a perimeter or WAN firewall. Restrict the dynamic RPC range to a known set of ports on the DC for manageability.

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 135 | TCP | DC (Site A) ↔ DC (Site B) | RPC endpoint mapper |
| 49152–65535 | TCP | DC (Site A) ↔ DC (Site B) | Dynamic RPC for replication — restrict range via registry or GPO |
| 389 | TCP/UDP | DC (Site A) ↔ DC (Site B) | LDAP replication |
| 445 | TCP | DC (Site A) ↔ DC (Site B) | DFSR (SYSVOL) — DFS replication uses SMB |
| 53 | TCP/UDP | DC (Site A) ↔ DC (Site B) | DNS zone transfer (if DCs are DNS servers for both sites) |

---

## Remote Administration

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 3389 | TCP | Admin workstations | DC | RDP — remote desktop for DC management |
| 5985 | TCP | Admin workstations | DC | WinRM — PowerShell remoting (HTTP) |
| 5986 | TCP | Admin workstations | DC | WinRM — PowerShell remoting (HTTPS) |
| 445 | TCP | Admin workstations | DC | SMB — administrative file share access (SYSVOL, admin$) |
| 135 | TCP | Admin workstations | DC | DCOM/RPC (Windows admin tools: ADUC, DNS Manager, etc.) |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| All domain clients | DC | 53, 88, 389, 445, 135, 464 | Core auth — all domain-joined systems |
| All domain clients | DC | 49152-65535 TCP | Dynamic RPC — restrict range in GPO if firewalled |
| App servers (non-Windows) | DC | 636, 3268/3269 | LDAPS preferred over LDAP |
| DC ↔ DC (intra-site) | DC ↔ DC | 135, 445, 49152-65535 | Replication — typically same L2 |
| DC ↔ DC (inter-site) | DC ↔ DC | 135, 445, 389, 49152-65535 | Inter-site firewall; restrict dynamic range |
| Admin workstations | DC | 3389, 5985, 5986 | Management — restrict to jump hosts |

---

## Verify

```powershell
# From a domain-joined client — test core AD ports
Test-NetConnection -ComputerName dc01.corp.local -Port 389
Test-NetConnection -ComputerName dc01.corp.local -Port 636
Test-NetConnection -ComputerName dc01.corp.local -Port 88
Test-NetConnection -ComputerName dc01.corp.local -Port 445

# From a Linux client — test Kerberos and LDAP
nc -zv dc01.corp.local 88
nc -zv dc01.corp.local 636

# Test DNS resolution of the domain
nslookup corp.local <dc-ip>
nslookup -type=SRV _kerberos._tcp.corp.local <dc-ip>

# From a DC — check replication health
repadmin /replsummary
repadmin /showrepl

# From a DC — check DNS zone transfer
dnscmd dc01 /zoneprint corp.local | head -30
```

---

## See also

- [Active Directory — Architecture](how-it-works/)
- [Active Directory — Deploy](../deploy/)
- [Active Directory — Operations](../operations/)
- [Active Directory — Security](../security/)
