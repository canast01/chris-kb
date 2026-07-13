---
tags:
  - security
description: "Patch Compliance Monitoring reference covering Patch Classification, Windows Patch Compliance, Linux Patch Compliance, SCCM / Endpoint Manager (Windows..."
---
# Patch Compliance Monitoring

<div class="kb-summary">
Patch Compliance Monitoring reference covering Patch Classification, Windows Patch Compliance, Linux Patch Compliance, SCCM / Endpoint Manager (Windows fleet), Patch Reporting and 2 more sections.
</div>

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Patch scanning, SLA tracking, WSUS/SCCM management, exception handling</div>
  </a>
</div>

## Patch Classification

| Severity | Definition | Deployment SLA |
|---|---|---|
| Critical | Remote code execution, active exploitation | 15 days |
| Important | Privilege escalation, data exposure | 30 days |
| Moderate | Requires unusual conditions or local access | 90 days |
| Low | Minimal impact | Next scheduled window |

## Windows Patch Compliance

```powershell
# List installed hotfixes sorted by date
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20

# List missing updates (requires Windows Update module)
$session = New-Object -ComObject Microsoft.Update.Session
$searcher = $session.CreateUpdateSearcher()
$missing = $searcher.Search("IsInstalled=0 and Type='Software'")
$missing.Updates | Select-Object Title, MsrcSeverity | Sort-Object MsrcSeverity

# WSUS — get patch compliance per computer
# Run on WSUS server (requires UpdateServices module)
$wsus = Get-WsusServer -Name wsus01 -PortNumber 8530
$computers = Get-WsusComputer -UpdateServer $wsus -All
$computers | Select-Object FullDomainName, LastSyncTime, @{N='NotInstalled';E={$_.GetUpdateInstallationSummary().NotInstalled}} |
  Sort-Object NotInstalled -Descending | Select-Object -First 20
```

## Linux Patch Compliance

```bash
# RHEL/CentOS — list available security updates
yum updateinfo list security available 2>/dev/null

# Count critical updates
yum updateinfo summary security 2>/dev/null | grep "Critical"

# Ubuntu/Debian — list upgradable security packages
apt list --upgradable 2>/dev/null | grep -i security

# Confirm last update date
rpm -qa --last | head -10          # RHEL
grep "install" /var/log/dpkg.log | tail -10  # Debian

# Check kernel version vs latest available
uname -r
rpm -q kernel | sort -V | tail    # RHEL — latest installed kernel
```


```text title="Expected output"
RHEL-SA-2024-1847  security  kernel-5.10.0-28.el7                    available
RHEL-SA-2024-1923  security  openssl-1.1.1k-12.el7_9                 available
RHEL-SA-2024-2156  security  glibc-2.17-326.el7_9.5                  available
RHEL-SA-2024-2401  security  systemd-219-78.el7_9.11                 available
RHEL-SA-2024-2847  security  curl-7.29.0-59.el7_9.3                  available

    3 Security notice(s)
        3 Critical notice(s)

ii  curl-security-patch                    7.68.0-1ubuntu2.18+security1    amd64
ii  openssl-security-update                1.1.1f-1ubuntu2.21+security2    amd64

kernel-5.10.0-28.el7_9.x86_64              Mon 18 Mar 2024 02:15:22 PM UTC
kernel-5.10.0-27.el7_9.x86_64              Fri 15 Mar 2024 09:42:10 AM UTC
kernel-5.10.0-26.el7_9.x86_64              Wed 13 Mar 2024 11:28:45 AM UTC
kernel-5.10.0-25.el7_9.x86_64              Mon 11 Mar 2024 08:33:17 AM UTC
kernel-5.10.0-24.el7_9.x86_64              Sat 09 Mar 2024 04:19:33 PM UTC

2024-03-18 14:22:08 install openssl:amd64 1.1.1f-1ubuntu2.21+security2
2024-03-17 09:15:42 install curl:amd64 7.68.0-1ubuntu2.18+security1
2024-03-16 11:47:19 install linux-image-generic 5.15.0-105-generic

5.10.0-28.el7_9.x86_64
kernel-5.10.0-28.el7_9.x86_64
kernel-5.10.0-27.el7_9.x86_64
kernel-5.10.0-26.el7_9.x86_64
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `yum: command not found` | Verify the system is RHEL/CentOS by checking `/etc/os-release`, or use `dnf` on RHEL 8+. |
    | `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)` | Run the apt command with `sudo` or as root. |
    | `grep: /var/log/dpkg.log: No such file or directory` | Check `/var/log/apt/history.log` instead on some Debian/Ubuntu versions. |
## SCCM / Endpoint Manager (Windows fleet)

```powershell
# Query SCCM database for patch compliance (run on SCCM server)
$query = "SELECT SMS_R_System.Name, SMS_UpdateComplianceStatus.Status FROM SMS_R_System
          INNER JOIN SMS_UpdateComplianceStatus ON SMS_R_System.ResourceID = SMS_UpdateComplianceStatus.MachineID
          WHERE SMS_UpdateComplianceStatus.ArticleID = '<KB-number>'"
```

## Patch Reporting

| Metric | Target |
|---|---|
| Critical patches applied within 15 days | >95% of hosts |
| High patches applied within 30 days | >90% of hosts |
| Systems with no patches >90 days | 0 |
| Unapproved exceptions | Must have documented business justification + compensating control |

## Compliance Checks by Tool

**Qualys / Tenable patch compliance:**
```bash
# Query Tenable.io for patch compliance data
curl -s -H "X-ApiKey: accessKey=<ak>;secretKey=<sk>" \
  "https://cloud.tenable.com/workbenches/assets/vulnerabilities" \
  | jq '.vulnerabilities[] | select(.plugin_family=="Windows : Microsoft Bulletins") | {name,severity,count}'
```


```text title="Expected output"
{
  "name": "MS19-001: Security Updates for Microsoft Windows",
  "severity": "high",
  "count": 23
}
{
  "name": "MS19-002: Security Updates for Microsoft Office",
  "severity": "critical",
  "count": 8
}
{
  "name": "MS18-012: Security Updates for Windows Kernel",
  "severity": "high",
  "count": 15
}
{
  "name": "MS20-045: Security Updates for Windows SMB",
  "severity": "critical",
  "count": 5
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: cloud.tenable.com` | Verify network connectivity and DNS resolution, or check if your firewall blocks access to Tenable.io endpoints. |
    | `{"error":"Invalid Credentials","status":401}` | Ensure your API key and secret key are correctly formatted and have not expired in the Tenable.io console. |
    | `jq: parse error: Invalid JSON` | Confirm the API response is valid JSON by testing the curl command without the jq filter first. |
**Azure Update Manager:**
```bash
# List VMs with missing critical updates
az maintenance configuration list -o table

# Check update status for a VM
az maintenance update list -g <rg> --resource-name <vm-name> --resource-type VirtualMachines \
  --provider-name Microsoft.Compute \
  --query '[?properties.maintenanceScope==`InGuestPatch`]'
```


```text title="Expected output"
Name                          ResourceGroup      Location    MaintenanceScope
-----------------------------  -----------------  ----------  ------------------
prod-patch-config-01          prod-rg            eastus      InGuestPatch
prod-patch-config-02          prod-rg            eastus      InGuestPatch
staging-patch-weekly          staging-rg         westus2     InGuestPatch
dev-emergency-patches         dev-rg             eastus      InGuestPatch

[
  {
    "id": "/subscriptions/a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-server-01/providers/Microsoft.Maintenance/updates/2024-01-15-critical-kb5034765",
    "name": "2024-01-15-critical-kb5034765",
    "properties": {
      "maintenanceScope": "InGuestPatch",
      "impactType": "Freeze",
      "duration": "PT30M",
      "status": "Pending"
    }
  }
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound` | Verify the resource group name with `az group list` and ensure you're using the correct subscription with `az account show`. |
    | `ResourceNotFound` | Confirm the VM exists in the specified resource group using `az vm list -g <rg> -o table` and check the exact VM name spelling. |
## Exception Handling

When a patch cannot be applied within the SLA:
1. Document the exception with system name, patch, and reason
2. Identify compensating controls (WAF rule, network segmentation, IDS signature)
3. Set review date (maximum 30-day extension for non-critical systems)
4. Obtain security team and management sign-off
5. Track in vulnerability management system
