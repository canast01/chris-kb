# Windows Server — Hardening


<div class="kb-summary">
CIS benchmark GPO controls, Windows Defender configuration, audit policy, GPO hardening baseline, and Security Compliance Manager (SCM).
</div>

## CIS Benchmark and Security Baselines

Microsoft and the Center for Internet Security publish security baselines for Windows Server that map to GPO settings.

### Tools

- **Microsoft Security Compliance Toolkit (SCT)** — downloadable GPO templates from Microsoft, aligned to CIS/STIG.
- **CIS Benchmarks** — prescriptive guidance at [cisecurity.org](https://www.cisecurity.org).
- **Policy Analyzer** — part of SCT; compares a machine's effective policy against a baseline.

```powershell
# Import Microsoft Security Baseline GPO backup
# 1. Download SCT from Microsoft Download Center
# 2. Extract baseline GPO backups
# 3. Import via GPMC
Import-GPO -BackupGpoName "MSFT Windows Server 2022 - Domain Security" `
  -TargetName "CORP Baseline - Domain Security" `
  -Path "C:\SCT\Windows Server 2022 Security Baseline\GPOs" `
  -CreateIfNeeded

# Run Policy Analyzer (GUI tool) — compare live settings vs. baseline
# PolicyAnalyzer.exe from SCT
```
┌───────────────────────────────────── Windows Server — Hardening ──────────────────────────────────────┐
│                                                                                                       │
│  OS hardening: CIS Benchmark baseline, GPO policies, attack surface reduction, Defender.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            OS & Service Hardening            │  │           Attack Surface Reduction          │   │
│   │           CIS Benchmark L1/L2 GPOs           │  │        Disable unused roles/features        │   │
│   │         STIG SCAP scan and remediate         │  │          Close unused TCP/UDP ports         │   │
│   │       Disable SMBv1, TelnetFTP,WDigest       │  │        ASR rules: Office macro block        │   │
│   │        Enable Secure Boot + UEFI lock        │  │           AppLocker/WDAC whitelist          │   │
│   │          Patch: patch Tuesday + OOB          │  │         RDP: restrict to jump server        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  GPO baseline locks config; ASR rules reduce malware execution paths.                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Defender & EDR                │  │              Account Hardening              │   │
│   │         Defender: real-time + cloud          │  │          Rename built-in Admin acct         │   │
│   │         Defender ATP: EDR telemetry          │  │            Disable Guest account            │   │
│   │            Tamper protection: on             │  │         Fine-grained password policy        │   │
│   │        Credential Guard: LSASS in VBS        │  │         Account lockout: 5 attempts         │   │
│   │          Device Guard: HVCI kernel           │  │          LAPS for all local admins          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical server · TPM 2.0 · UEFI Secure Boot · dedicated management NIC (iDRAC/iLO)                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CIS Benchmark  = Center for Internet Security; numbered controls for OS hardening                    │
│  STIG           = Security Technical Implementation Guide; DoD hardening standard                     │
│  SCAP           = Security Content Automation Protocol; machine-readable STIG scanning                │
│  WDigest        = legacy auth provider; caches cleartext passwords in LSASS memory                    │
│  ASR            = Attack Surface Reduction rules; Defender policies blocking exploit paths            │
│  AppLocker      = Windows policy engine; whitelist which executables/scripts can run                  │
│  WDAC           = Windows Defender Application Control; kernel code integrity policy                  │
│  Credential Guard= VBS-isolated LSASS; prevents pass-the-hash/ticket attacks                          │
│  Device Guard   = HVCI: Hypervisor-Protected Code Integrity; kernel driver validation                 │
│  HVCI           = Hypervisor Protected Code Integrity; kernel runs in VBS environment                 │
│  VBS            = Virtualisation-Based Security; Hyper-V isolates security features                   │
│  LAPS           = Local Admin Password Solution; rotates local admin passwords in AD                  │
│  Defender ATP   = Microsoft Defender for Endpoint; EDR platform with SIEM integration                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## Audit Policy

Configure via GPO: Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy Configuration.

### Recommended Audit Categories

| Category | Subcategory | Setting |
|---|---|---|
| Account Logon | Credential Validation | Success, Failure |
| Account Logon | Kerberos Authentication | Success, Failure |
| Account Management | User Account Management | Success, Failure |
| Account Management | Security Group Management | Success, Failure |
| DS Access | Directory Service Changes | Success |
| Logon/Logoff | Logon | Success, Failure |
| Logon/Logoff | Logoff | Success |
| Logon/Logoff | Account Lockout | Failure |
| Object Access | File System | Failure (Success only for sensitive paths) |
| Privilege Use | Sensitive Privilege Use | Success, Failure |
| Policy Change | Audit Policy Change | Success |
| Policy Change | Authentication Policy Change | Success |
| System | Security System Extension | Success |
| System | System Integrity | Success, Failure |

```powershell
# Apply audit subcategory settings via auditpol
auditpol /set /subcategory:"Credential Validation" /success:enable /failure:enable
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Account Lockout" /failure:enable
auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable
auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable
auditpol /set /subcategory:"Audit Policy Change" /success:enable

# View current audit policy
auditpol /get /category:*

# Export audit policy to CSV
auditpol /backup /file:C:\temp\audit-policy.csv
```

### Security Event Log Size

```powershell
# Set Security log maximum size to 512 MB and retain via circular wrapping
wevtutil sl Security /ms:524288000 /rt:false /ab:false
# Equivalent in GPO: Computer Configuration > Windows Settings > Security Settings >
#                   Event Log > Maximum security log size = 524288 KB
```

## Windows Defender Antivirus

```powershell
# Verify Windows Defender is running and definitions are current
Get-MpComputerStatus | Select-Object AMRunningMode, AMProductVersion,
  AntivirusSignatureLastUpdated, RealTimeProtectionEnabled

# Force a signature update
Update-MpSignature

# Run a quick scan
Start-MpScan -ScanType QuickScan

# Run a full scan
Start-MpScan -ScanType FullScan

# View recent threat detections
Get-MpThreatDetection | Select-Object InitialDetectionTime, DomainUser, ProcessName,
  Resources, ActionSuccess | Sort-Object InitialDetectionTime -Descending | Select-Object -First 20

# Configure exclusions (add only when operationally necessary)
Add-MpPreference -ExclusionPath "C:\App\Databases"
Add-MpPreference -ExclusionExtension ".mdf", ".ldf"

# Verify exclusions (review periodically)
(Get-MpPreference).ExclusionPath
(Get-MpPreference).ExclusionProcess
```

### Attack Surface Reduction Rules

```powershell
# Enable ASR rules in block mode (audit mode = 2, block mode = 1)
# Block Office applications from creating child processes
Add-MpPreference -AttackSurfaceReductionRules_Ids D4F940AB-401B-4EFC-AADC-AD5F3C50688A `
  -AttackSurfaceReductionRules_Actions Enabled

# Block credential stealing from LSASS
Add-MpPreference -AttackSurfaceReductionRules_Ids 9E6C4E1F-7D60-472F-BA1A-A39EF669E4B0 `
  -AttackSurfaceReductionRules_Actions Enabled

# Block execution of potentially obfuscated scripts
Add-MpPreference -AttackSurfaceReductionRules_Ids 5BEB7EFE-FD9A-4556-801D-275E5FFC04CC `
  -AttackSurfaceReductionRules_Actions Enabled

# View current ASR rule states
(Get-MpPreference).AttackSurfaceReductionRules_Ids |
  ForEach-Object { "$_ : $((Get-MpPreference).AttackSurfaceReductionRules_Actions)" }
```

## GPO Hardening Baseline

### Account Policy (Default Domain Policy)

GPO path: Computer Configuration > Windows Settings > Security Settings > Account Policies

| Setting | Value |
|---|---|
| Minimum password length | 14 characters |
| Password complexity | Enabled |
| Maximum password age | 90 days |
| Minimum password age | 1 day |
| Enforce password history | 24 passwords |
| Account lockout threshold | 5 invalid attempts |
| Account lockout duration | 15 minutes |
| Reset account lockout counter | 15 minutes |

### Security Options — Key Settings

GPO path: Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options

| Setting | Value |
|---|---|
| Accounts: Guest account status | Disabled |
| Accounts: Limit local account use of blank passwords to console logon only | Enabled |
| Audit: Shut down system immediately if unable to log security audits | Disabled (review — can cause outage) |
| Interactive logon: Do not display last user name | Enabled |
| Interactive logon: Machine inactivity limit | 900 seconds |
| Interactive logon: Message text for logon | (Set legal banner) |
| Network access: Do not allow anonymous enumeration of SAM accounts | Enabled |
| Network access: Do not allow anonymous enumeration of SAM accounts and shares | Enabled |
| Network access: Restrict anonymous access to Named Pipes and Shares | Enabled |
| Network security: LAN Manager authentication level | Send NTLMv2 response only. Refuse LM & NTLM |
| Network security: Minimum session security for NTLM SSP | Require NTLMv2, Require 128-bit |
| System objects: Require case insensitivity for non-Windows subsystems | Enabled |
| User Account Control: Admin Approval Mode for the built-in Administrator | Enabled |
| User Account Control: Behavior of the elevation prompt for admins | Prompt for credentials |

### Windows Firewall

```powershell
# Enable firewall on all profiles
Set-NetFirewallProfile -Profile Domain,Private,Public -Enabled True

# Set default inbound to block, outbound to allow
Set-NetFirewallProfile -Profile Domain,Private,Public `
  -DefaultInboundAction Block -DefaultOutboundAction Allow

# Allow RDP from management network only
New-NetFirewallRule -DisplayName "RDP - Management Network" `
  -Direction Inbound -Protocol TCP -LocalPort 3389 `
  -RemoteAddress 10.10.10.0/24 -Action Allow -Profile Domain

# Allow SMB from specific subnets only
New-NetFirewallRule -DisplayName "SMB - Internal" `
  -Direction Inbound -Protocol TCP -LocalPort 445 `
  -RemoteAddress 10.0.0.0/8 -Action Allow -Profile Domain

# Block SMB from outside (public profile)
New-NetFirewallRule -DisplayName "Block SMB Public" `
  -Direction Inbound -Protocol TCP -LocalPort 445 `
  -Action Block -Profile Public

# Export current firewall rules
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"} |
  Export-Csv C:\temp\firewall-rules.csv -NoTypeInformation
```

## PowerShell Security

```powershell
# Set PowerShell execution policy — RemoteSigned minimum
Set-ExecutionPolicy RemoteSigned -Scope LocalMachine -Force

# Enable PowerShell script block logging (logs all executed script content)
$logPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
New-Item -Path $logPath -Force
Set-ItemProperty -Path $logPath -Name "EnableScriptBlockLogging" -Value 1

# Enable PowerShell transcription (logs sessions to a central share)
$transcriptPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription"
New-Item -Path $transcriptPath -Force
Set-ItemProperty -Path $transcriptPath -Name "EnableTranscripting" -Value 1
Set-ItemProperty -Path $transcriptPath -Name "OutputDirectory" -Value "\\logserver\pstranscripts\"
Set-ItemProperty -Path $transcriptPath -Name "EnableInvocationHeader" -Value 1

# Constrained Language Mode — restrict PowerShell to safer command set
# Set via GPO or WDAC policy (not registry alone)
# Verify current mode
$ExecutionContext.SessionState.LanguageMode
```

## Remote Desktop Hardening

```powershell
# Require NLA (Network Level Authentication) for RDP
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" `
  -Name "UserAuthentication" -Value 1

# Set RDP encryption level to High
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" `
  -Name "MinEncryptionLevel" -Value 3

# Restrict RDP to specific users
# Add users to "Remote Desktop Users" group only — do not grant Domain Admins direct RDP

# Disable RDP if not needed
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" `
  -Name "fDenyTSConnections" -Value 1
```

## Credential Protection

```powershell
# Disable storing of LAN Manager hash (empty string policy ensures no LM hash stored)
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" `
  -Name "NoLMHash" -Value 1

# Enable Protected Users security group for privileged accounts
# Members cannot use NTLM, cannot delegate credentials, tickets expire in 4 hours
Add-ADGroupMember -Identity "Protected Users" -Members "jsmith","admin.jsmith"

# Enable Credential Guard (see Authentication page for full steps)
# Verify LSA is running as protected process
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "RunAsPPL"
# Value should be 1
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "RunAsPPL" -Value 1
```

## CIS Benchmark Quick Checks

```powershell
# Quick hardening verification script
$checks = @{
    "Guest account disabled"              = { (Get-LocalUser Guest).Enabled -eq $false }
    "SMB signing required"                = { (Get-SmbServerConfiguration).RequireSecuritySignature }
    "Firewall enabled (Domain)"           = { (Get-NetFirewallProfile -Name Domain).Enabled }
    "Defender Real-Time enabled"          = { (Get-MpComputerStatus).RealTimeProtectionEnabled }
    "NLA required for RDP"                = {
        (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp").UserAuthentication -eq 1
    }
    "LM hash storage disabled"            = {
        (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa").NoLMHash -eq 1
    }
    "Script block logging enabled"        = {
        (Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -ErrorAction SilentlyContinue).EnableScriptBlockLogging -eq 1
    }
}

foreach ($check in $checks.GetEnumerator()) {
    $result = try { & $check.Value } catch { $false }
    $status = if ($result) { "PASS" } else { "FAIL" }
    Write-Host "$status : $($check.Key)" -ForegroundColor $(if ($result) { "Green" } else { "Red" })
}
```

## Quick Reference

| Topic | Tool / Location |
|---|---|
| Security baseline import | Security Compliance Toolkit (SCT) + GPMC |
| Audit policy | `auditpol /get /category:*` |
| Defender status | `Get-MpComputerStatus` |
| Defender update | `Update-MpSignature` |
| Firewall policy | `Get-NetFirewallProfile`, `Set-NetFirewallProfile` |
| NLA for RDP | `UserAuthentication = 1` in Terminal Server registry |
| LM hash disabled | `HKLM:\...\Lsa\NoLMHash = 1` |
| PowerShell logging | `HKLM:\...\PowerShell\ScriptBlockLogging\EnableScriptBlockLogging = 1` |
| GPO result | `gpresult /H report.html /F` |
| Policy analysis | Policy Analyzer (SCT tool) |
