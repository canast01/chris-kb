# Windows Server Security

## CIS Benchmark Hardening

Windows Server builds are hardened to CIS Microsoft Windows Server Level 1 benchmark, applied via Group Policy Objects linked at the server OU level.

Key GPO-enforced controls:

| Control | Policy Setting |
|---|---|
| Account lockout | 10 failed attempts; 30-minute lockout |
| Password policy | Minimum 14 chars, complexity required, 90-day rotation |
| Audit policy | Success+Failure for: logon, privilege use, object access, policy change |
| SMB signing | RequireSecuritySignature = 1 on servers |
| RDP NLA | Require Network Level Authentication |
| UAC | Prompt for elevated operations |
| Windows Defender | Real-time protection enabled; cloud-delivered protection enabled |
| TLS | TLS 1.2 minimum; TLS 1.0/1.1 disabled via GPO |

Apply GPO immediately (without waiting for next policy refresh cycle):
```powershell
gpupdate /force
rsop.msc   # View resulting set of policy
```

## Windows Defender Configuration

```powershell
# Verify Defender status
Get-MpComputerStatus | Select-Object AMRunningMode, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated

# Trigger signature update
Update-MpSignature

# Check for active threats
Get-MpThreatDetection | Select-Object ActionSuccess, CategoryID, Resources, InitialDetectionTime

# Add exclusion (document every exclusion in CMDB)
Add-MpPreference -ExclusionPath "D:\App\Data\"
```

## CyberArk PAM (Privileged Access Management)

Local administrator accounts are managed via CyberArk:

1. Onboard built-in Administrator account to CyberArk safe
2. Set CyberArk to rotate the password on every checkout (or on a schedule)
3. Require dual approval for admin access to Tier 1 systems

For systems not yet onboarded to CyberArk, use LAPS:

```powershell
# Verify LAPS is installed
Get-AdmPwdPassword -ComputerName $env:COMPUTERNAME

# Check LAPS policy is applied
Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft Services\AdmPwd" |
    Select-Object AdmPwdEnabled, PasswordLength, PasswordAgeDays
```

## Audit Policy

```powershell
# Review current audit policy
auditpol /get /category:*

# Force CIS audit policy (run as Administrator)
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Account Lockout" /success:enable /failure:enable
auditpol /set /subcategory:"Privilege Use" /success:enable /failure:enable
```

## Windows Firewall

```powershell
# Check firewall state per profile
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction

# View active rules
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True" -and $_.Direction -eq "Inbound"} |
    Select-Object DisplayName, Action, Profile

# Add rule (example: allow monitoring on port 9182)
New-NetFirewallRule -DisplayName "Allow WMI Exporter" -Direction Inbound -Protocol TCP -LocalPort 9182 -Action Allow
```

## Event Log Forwarding

Forward security events to SIEM:

```powershell
# Check Windows Event Forwarding (WEF) subscriptions
wecutil es   # List subscriptions

# Or via Splunk/Elastic agent — verify agent service
Get-Service SplunkForwarder | Select-Object Status
Get-Service ElasticAgent | Select-Object Status
```

Events to forward to SIEM:
- Security log: Event IDs 4624 (logon), 4625 (failed logon), 4648 (explicit logon), 4719 (policy change), 4728/4732/4756 (group membership changes)

## Security Hardening Checklist

- [ ] CIS Level 1 GPO applied: `gpresult /h C:\temp\gpreport.html`
- [ ] Windows Defender active with latest signatures
- [ ] CyberArk: Administrator account onboarded (or LAPS configured)
- [ ] Audit policy: logon success+failure enabled
- [ ] SMB signing required via GPO
- [ ] RDP NLA required
- [ ] TLS 1.0/1.1 disabled
- [ ] Windows Firewall enabled on all profiles
- [ ] Security event logs forwarded to SIEM
- [ ] WSUS/SCCM patching active; no updates pending > 30 days
