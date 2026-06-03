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

```text
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
```
```powershell
# Set Security log maximum size to 512 MB and retain via circular wrapping
wevtutil sl Security /ms:524288000 /rt:false /ab:false
# Equivalent in GPO: Computer Configuration > Windows Settings > Security Settings >
#                   Event Log > Maximum security log size = 524288 KB
```
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
