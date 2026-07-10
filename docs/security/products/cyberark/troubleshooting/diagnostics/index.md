---
tags:
  - security
  - troubleshooting
search:
  boost: 1.5
---
# CyberArk — Diagnostics

<div class="kb-summary">
CyberArk PAM diagnostic commands: check Vault, PVWA, CPM, and PSM Windows service status, test Vault port 1858 connectivity, inspect component log files, diagnose LDAP and RADIUS auth issues, and collect the PrivateArk diagnostic bundle for CyberArk support cases.

*Applies to: CyberArk PAM (Privilege Access Manager) — Vault, PVWA, CPM, PSM*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "Check PVWA IIS app pool\nGet-WebApplication PasswordVault" {shape: rectangle}
D: "Check CPM service\nGet-Service CyberArk Central Policy Manager" {shape: rectangle}
E: "Check PSM service\nGet-Service Cyber-Ark Privileged Session Manager" {shape: rectangle}
F: "Test LDAPS port 636\nTest RADIUS port 1812" {shape: rectangle}
G: "Test-NetConnection vault01 -Port 1858\nVault reachable?" {shape: rectangle}
H: "Review pm.log\nFind rotation error code" {shape: rectangle}
I: "Review PSMConsole.log\nFind session launch error" {shape: rectangle}
J: "Check PVWA auth config\nAuth Methods in PVWA Admin" {shape: rectangle}
K: "K" {shape: rectangle}
L: "Check firewall rules\nbetween component and Vault" {shape: rectangle}
M: "Collect component logs\nfor CyberArk support" {shape: rectangle}
N: "Open CyberArk SR\nmy.cyberark.com" {shape: rectangle}
A: "CyberArk issue reported" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
C -> G
D -> H
E -> I
F -> J
K -> L
K -> M
H -> M
I -> M
J -> M
L -> M
M -> N
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_vault_service_status: "Step 1 — Check Vault service status" {shape: rectangle}
step_2_test_vault_connectivity_from_: "Step 2 — Test Vault connectivity from each component" {shape: rectangle}
step_3_check_pvwa_password_vault_web: "Step 3 — Check PVWA (Password Vault Web Access)" {shape: rectangle}
step_4_check_cpm_password_rotation_f: "Step 4 — Check CPM (password rotation failures)" {shape: rectangle}
step_5_check_psm_session_launch_fail: "Step 5 — Check PSM (session launch failures)" {shape: rectangle}
step_6_check_ldap_and_mfa_authentica: "Step 6 — Check LDAP and MFA authentication" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_vault_service_status: investigate
symptom -> step_2_test_vault_connectivity_from_: investigate
symptom -> step_3_check_pvwa_password_vault_web: investigate
symptom -> step_4_check_cpm_password_rotation_f: investigate
symptom -> step_5_check_psm_session_launch_fail: investigate
symptom -> step_6_check_ldap_and_mfa_authentica: investigate
step_1_check_vault_service_status -> resolution
step_2_test_vault_connectivity_from_ -> resolution
step_3_check_pvwa_password_vault_web -> resolution
step_4_check_cpm_password_rotation_f -> resolution
step_5_check_psm_session_launch_fail -> resolution
step_6_check_ldap_and_mfa_authentica -> resolution
```

## Before you begin

- **Access:** Windows admin access on the Vault, PVWA, CPM, and PSM servers; PVWA admin role for audit log review
- **Gather first:** the exact error message the user sees (copy from the PVWA error page or component log), the affected account name, and the Safe it belongs to
- **Scope:** confirm whether the issue affects one account, one Safe, one component (e.g., CPM only), or all users
- **Vault connectivity first:** all CyberArk components depend on TCP 1858 to the Vault — verify this before investigating the individual component

---

## Step 1 — Check Vault service status

```powershell
# On the PrivateArk Vault server (Windows)

# Check Vault service
Get-Service 'PrivilegeVault' | Select-Object Name, Status, StartType
# Expected: Status = Running

# Start if stopped
Start-Service 'PrivilegeVault'

# Check Vault event log
Get-EventLog -LogName Application -Source "PrivateArk" -Newest 50 |
  Select-Object TimeGenerated, EntryType, Message |
  Format-List

# Vault log file location
# C:\Program Files (x86)\PrivateArk\Server\Logs\
Get-Content "C:\Program Files (x86)\PrivateArk\Server\Logs\traces.log" -Tail 100
```

---

## Step 2 — Test Vault connectivity from each component

Run these from the PVWA, CPM, and PSM servers, not from the Vault itself:

```powershell
# Test TCP 1858 to Vault (the critical port for all CyberArk components)
Test-NetConnection -ComputerName <vault-hostname> -Port 1858
# Expected: TcpTestSucceeded: True
# If False: firewall rule missing between this server and the Vault

# Test TCP 443 for REST API (required by PVWA and newer CPM versions)
Test-NetConnection -ComputerName <vault-hostname> -Port 443

# Check from multiple components — port 1858 must be open from:
# - Each PVWA server → Vault
# - Each CPM server → Vault
# - Each PSM server → Vault
# - Each DR Vault → Primary Vault
```

---

## Step 3 — Check PVWA (Password Vault Web Access)

```powershell
# On the PVWA server (Windows + IIS)

# Check the PasswordVault IIS application pool
Import-Module WebAdministration
Get-WebApplication -Name "PasswordVault"
Get-WebConfiguration -PSPath "IIS:\" -Filter "system.applicationHost/applicationPools/add[@name='PasswordVault']" |
  Select-Object name, state
# Expected: state = Started

# Restart PVWA application pool if stopped
Restart-WebAppPool -Name "PasswordVault"

# PVWA application log
$pvwaLog = "C:\inetpub\wwwroot\PasswordVault\Logs\"
Get-ChildItem $pvwaLog | Sort-Object LastWriteTime -Descending | Select-Object -First 5
Get-Content "$pvwaLog\error.log" -Tail 100

# IIS access log (W3C format)
$iisLog = "C:\Windows\System32\LogFiles\W3SVC1\"
Get-ChildItem $iisLog | Sort-Object LastWriteTime -Descending | Select-Object -First 1
# Look for 500 errors: Get-Content <log-file> | Select-String " 500 "
```

---

## Step 4 — Check CPM (password rotation failures)

```powershell
# On the CPM server

# Check CPM service
Get-Service 'CyberArk Central Policy Manager' | Select-Object Name, Status
# Expected: Running

# Start if stopped
Start-Service 'CyberArk Central Policy Manager'

# CPM log location
$cpmLog = "C:\Program Files (x86)\CyberArk\Password Manager\Logs\"
Get-ChildItem $cpmLog | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Show recent rotation errors in pm.log
Get-Content "$cpmLog\pm.log" -Tail 200 |
  Select-String -Pattern "error|fail|ERR|cannot|refused" -CaseSensitive:$false

# Common CPM error codes and meanings:
# PACP035E - Authentication failure on target system (wrong current password)
# PACP069E - Target host not reachable (firewall / network)
# PACP014E - Dual control approval required but no approver available
# ITATS528E - Account locked out on target platform

# Test connectivity from CPM to a target system (e.g., a Windows host for AD account rotation)
Test-NetConnection -ComputerName <target-hostname> -Port 445  # for Windows LDAP/local account
Test-NetConnection -ComputerName <target-hostname> -Port 22   # for Linux SSH account
```

---

## Step 5 — Check PSM (session launch failures)

```powershell
# On the PSM server

# Check PSM service
Get-Service 'Cyber-Ark Privileged Session Manager' | Select-Object Name, Status
# Expected: Running

# PSM console log
$psmLog = "C:\Program Files (x86)\CyberArk\PSM\Logs\"
Get-Content "$psmLog\PSMConsole.log" -Tail 200 |
  Select-String -Pattern "error|fail|ERR|cannot|session" -CaseSensitive:$false

# PSM trace log (verbose — only enable temporarily)
Get-Content "$psmLog\PSMTrace.log" -Tail 100

# Common PSM errors:
# "Failed to connect to Vault" - port 1858 blocked between PSM and Vault
# "PSM Connection Client failed" - target platform plugin not found or misconfigured
# "RDP session initialization failed" - target RDP firewall or NLA issue
# "Shadow user credentials expired" - PSM shadow user in Vault needs password reset

# Check PSM shadow user (the internal account PSM uses to create sessions)
# PVWA → Administration → Component Details → PSM Servers → check Shadow User details
```

---

## Step 6 — Check LDAP and MFA authentication

```powershell
# Test LDAPS connectivity from PVWA server
Test-NetConnection -ComputerName <ldap-server> -Port 636
# Expected: TcpTestSucceeded: True for LDAPS
# If using plain LDAP (not recommended): port 389

# Test RADIUS connectivity (for Duo, RSA, etc.)
Test-NetConnection -ComputerName <radius-proxy-server> -Port 1812
# Note: RADIUS uses UDP — Test-NetConnection tests TCP; use a dedicated UDP test if needed

# Check PVWA auth method configuration
# PVWA → Administration → LDAP Integration
# Verify: LDAP Server address, Base DN, Bind User, SSL/TLS setting

# Simulate an LDAP bind (confirms credentials and SSL)
# From PVWA server PowerShell:
$ldap = New-Object System.DirectoryServices.DirectoryEntry(
  "LDAP://<ldap-server>:636/DC=corp,DC=local",
  "bind-user@corp.local",
  "bind-password"
)
$ldap.name   # Should return the domain root name if bind succeeds

# Check PVWA authentication log
Get-Content "C:\inetpub\wwwroot\PasswordVault\Logs\CyberArk.WebApplication.log" -Tail 200 |
  Select-String -Pattern "LDAP|auth|login|fail" -CaseSensitive:$false
```

---

## Step 7 — Collect logs for CyberArk support

```powershell
# Collect all relevant log files to a single directory
$dest = "C:\Temp\CyberArk-Diag-$(Get-Date -Format yyyyMMdd-HHmm)"
New-Item -ItemType Directory -Path $dest

# Vault logs (run on Vault server)
Copy-Item "C:\Program Files (x86)\PrivateArk\Server\Logs\*" $dest -Recurse -Force

# PVWA logs (run on PVWA server)
Copy-Item "C:\inetpub\wwwroot\PasswordVault\Logs\*" $dest -Force

# CPM logs (run on CPM server)
Copy-Item "C:\Program Files (x86)\CyberArk\Password Manager\Logs\*" $dest -Force

# PSM logs (run on PSM server)
Copy-Item "C:\Program Files (x86)\CyberArk\PSM\Logs\*" $dest -Force

# Compress
Compress-Archive -Path $dest -DestinationPath "$dest.zip"
Write-Host "Diagnostic bundle: $dest.zip"

# Attach to the CyberArk SR at my.cyberark.com
# Include: component versions, exact error message, account name, Safe name, time of failure
```

---

## Log locations

| Component | Log path | What to look for |
|---|---|---|
| Vault | `C:\Program Files (x86)\PrivateArk\Server\Logs\traces.log` | Service errors, Vault startup failures |
| PVWA | `C:\inetpub\wwwroot\PasswordVault\Logs\` | Login errors, auth failures, IIS 500 errors |
| CPM | `C:\Program Files (x86)\CyberArk\Password Manager\Logs\pm.log` | Rotation error codes (PACP, ITATS prefix) |
| PSM | `C:\Program Files (x86)\CyberArk\PSM\Logs\PSMConsole.log` | Session launch failures |
| Windows Event Log | `Get-EventLog -LogName Application -Source "PrivateArk"` | Service crashes, critical errors |

---

## See also

- [CyberArk — Common Issues](../common-issues/)
- [CyberArk — Escalation](../escalation/)
- [CyberArk — Procedures](../../operations/procedures/)

## Verify resolution

- All CyberArk services are running: Vault, PVWA app pool, CPM, PSM
- `Test-NetConnection <vault-hostname> -Port 1858` returns `TcpTestSucceeded: True` from all component servers
- PVWA login succeeds for an affected user; confirm with an audit log entry in PVWA → Audit → Audit Log
- A password rotation test account rotates successfully: PVWA → Accounts → select account → CPM → Verify Now
- PSM session launch succeeds to a test target; the session recording appears in PVWA → Monitoring
