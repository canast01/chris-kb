# CyberArk — Components

## Safe / Account / Platform Hierarchy

```mermaid
graph TD
    vault["Digital Vault"] --> safe1["Safe: PROD-DB-Accounts"]
    vault --> safe2["Safe: PROD-WIN-Accounts"]
    vault --> safe3["Safe: APP-Service-Accounts"]
    safe1 --> acct1["Account: db01-svc-app\n@ db01.corp.example.com"]
    safe1 --> acct2["Account: db02-sa\n@ db02.corp.example.com"]
    safe2 --> acct3["Account: local-admin\n@ win-srv-01"]
    safe1 -. "governed by" .-> plat["Platform: WinServerLocal\n(CPM rotation policy)"]
    safe1 -. "member" .-> grp["AD Group: GG_CyberArk_SafeOwners"]
```

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

## Safes

Safes are the organisational unit within the Vault. Each safe holds a set of accounts and has its own membership and access policy.

_Add safe-specific notes, checks, and commands here._

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

## Credential Checkout Sequence

```mermaid
sequenceDiagram
    participant user as Privileged User
    participant pvwa as PVWA
    participant vault as Digital Vault
    participant cpm as CPM
    participant target as Target System

    user->>pvwa: Request credential (account ID + reason)
    pvwa->>vault: Validate entitlement + retrieve credential
    vault-->>pvwa: Return credential (encrypted)
    pvwa-->>user: Credential available (check-out)
    note over user,target: User accesses target directly or via PSM
    user->>target: Connect with retrieved credential
    pvwa->>vault: Record audit event (who, what, when)
    pvwa->>cpm: Queue password rotation (after check-in)
    cpm->>target: Rotate credential on target
    cpm->>vault: Store new credential
```

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

## Session Isolation Flow

```mermaid
flowchart TD
    userReq["User requests session\nin PVWA"] --> pvwaLaunch["PVWA launches PSM connection"]
    pvwaLaunch --> psmAuth["PSM authenticates to Vault\n& retrieves credential"]
    psmAuth --> psmConnect["PSM connects to target system\nwith managed credential"]
    psmConnect --> sessionRecord["Session recording begins\n(video stored in Vault)"]
    sessionRecord --> userSession["User interacts via PSM proxy\nCredential never exposed"]
    userSession --> sessionEnd["Session ends — user disconnects"]
    sessionEnd --> recStore["Recording stored & indexed in Vault"]
    recStore --> cpmRotate["CPM rotates credential\nafter session check-in"]
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
