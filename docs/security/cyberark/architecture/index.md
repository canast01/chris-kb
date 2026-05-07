# CyberArk Architecture

CyberArk Privileged Access Manager (PAM) is built around the Digital Vault, an encrypted hardened credential store that is the sole authoritative source for managed passwords and SSH keys. The Central Policy Manager (CPM) rotates credentials automatically, the Privileged Session Manager (PSM) proxies and records sessions, and the Password Vault Web Access (PVWA) provides the web UI and REST API gateway.

---
## Component Overview

| Component | Role | Typical Count |
|---|---|---|
| Digital Vault | Encrypted credential store, core engine | 2 (primary + DR) |
| CPM (Central Policy Manager) | Automated password rotation | 1–2 per site |
| PSM (Privileged Session Manager) | Session proxy, recording, isolation | 2+ (load-balanced) |
| PVWA (Password Vault Web Access) | Web UI and REST API | 2+ (load-balanced) |
| PSMP | SSH proxy for Linux privileged access | 1–2 per site |
| DR Vault | Asynchronous replication replica of Vault | 1 per DR site |

---

## Network Topology

```
[Admin workstation / PAW]
         |
         | HTTPS (443)
         v
[PVWA (load-balanced pair)]  <-- AD LDAP/LDAPS (389/636)
         |
         | Vault SDK (1858)
         v
[Digital Vault (primary)]  <--> [DR Vault]
         |                      (replication: 1858)
         |
    +---------+----------+
    |                    |
[CPM]                 [PSM (load-balanced)]
    |                    |
    | (target protocols) | RDP/SSH (through session)
    v                    v
[Target systems]     [Target systems]
```

Key ports:
- PVWA → Vault: TCP 1858
- CPM → Vault: TCP 1858
- PSM → Vault: TCP 1858
- Admin → PVWA: TCP 443
- PSM → Targets: TCP 22 (SSH), TCP 3389 (RDP), TCP 1521 (Oracle), TCP 1433 (MSSQL)
- PSMP → Targets: TCP 22

---

## Digital Vault

The Vault runs on a hardened Windows Server — only the CyberArk Vault service and required OS components are present. No other roles are installed.

- All credentials stored encrypted with AES-256
- Vault OS hardened per CyberArk Vault Hardening Guide (firewall restricts all traffic except port 1858 from CPM/PSM/PVWA and replication to DR Vault)
- Vault event logs forwarded to SIEM via syslog

```powershell
# Check Vault service health (run locally on Vault server)
Get-Service -Name "CyberArk Vault"

# View Vault operational logs
Get-Content "C:\Program Files (x86)\PrivateArk\Server\Logs\vault.log" -Tail 100

# Check replication status to DR Vault
Get-Content "C:\Program Files (x86)\PrivateArk\Server\Logs\dbsync.log" -Tail 50
```

---

## Central Policy Manager (CPM)

CPM connects to target systems on schedule or on-demand to rotate passwords. Each CPM instance handles a partition of accounts determined by safe assignment.

```powershell
# Check CPM service health
Get-Service -Name "CyberArk Central Policy Manager Scanner"

# View CPM operational logs
Get-Content "C:\Program Files (x86)\CyberArk\Password Manager\Logs\pm.log" -Tail 100

# Find accounts with failed rotation (via PVWA REST API — see scripts page)
# Or: In PVWA -> Reports -> CPM Status Report
```

Common CPM failure reasons:
- Target host unreachable (firewall / network change)
- Credentials already changed manually (out-of-sync)
- Account locked by CPM rotation attempt
- Platform plugin misconfiguration

---

## Privileged Session Manager (PSM)

PSM proxies privileged sessions — the user connects to the PSM, which then connects to the target using the managed credential. The user never sees the password.

- Sessions are recorded as video files and stored in the Vault.
- Session isolation: PSM uses a Windows Server with AppLocker and restricted user profile.
- PSM nodes are load-balanced; session stickiness is not required (each session is independent).

```powershell
# Check PSM service health
Get-Service -Name "Cyber-Ark Privileged Session Manager"

# View PSM connection logs
Get-Content "C:\Program Files (x86)\CyberArk\PSM\Logs\PSMConsole.log" -Tail 100

# List active sessions (via PVWA REST API)
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://pvwa.corp.example.com/PasswordVault/API/LiveSessions" `
  -Headers $headers -Method Get
```

---

## PVWA (Password Vault Web Access)

PVWA is the primary interface for users and administrators. It provides:
- Account credential retrieval and check-out
- PSM session launch
- Safe and account management
- REST API gateway for automation

PVWA is deployed as an IIS application on Windows Server, behind a load balancer.

```powershell
# Check PVWA IIS application pool health
Get-WebConfiguration -Filter "system.applicationHost/applicationPools/add[@name='DefaultAppPool']"
Get-WebApplication -Site "Default Web Site" -Name "PasswordVault"

# Verify PVWA can reach the Vault (from PVWA server)
Test-NetConnection -ComputerName vault01.corp.example.com -Port 1858
```

---

## High Availability and DR

| Scenario | Recovery Method |
|---|---|
| Primary Vault hardware failure | Activate DR Vault; reconfigure CPM/PSM/PVWA to point to DR Vault |
| PVWA node failure | Load balancer removes failed node; remaining node serves traffic |
| CPM failure | Accounts queue for rotation; failover CPM picks up queue on restart |
| PSM node failure | Active sessions on failed node terminate; load balancer routes new sessions to healthy node |

DR Vault activation procedure:
1. Stop replication on the DR Vault: `C:\Program Files (x86)\PrivateArk\Server\dbsync.exe` — stop the sync service.
2. Change DR Vault to standalone mode via PrivateArk Client.
3. Update CPM, PSM, and PVWA `vault.ini` to point to the DR Vault IP.
4. Restart CyberArk services on CPM, PSM, PVWA.
5. Validate connectivity and test a credential retrieval.
