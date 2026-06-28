---
tags:
  - servicenow
---
# Inventory — License Management

```bash
# Debian / Ubuntu — list installed packages
dpkg -l | awk '{print $2, $3}' | grep -v "^ii"  # filter to installed only
dpkg-query -W -f='${Package} ${Version}\n'

# RHEL / Rocky — list installed
rpm -qa --qf "%{NAME} %{VERSION}-%{RELEASE}\n" | sort

# Running processes (for unlicensed software audit)
ps aux --sort=-%cpu | awk '{print $11}' | sort -u | head -30
```

```powershell
# Connect to Microsoft Graph (requires MgGraph module)
Connect-MgGraph -Scopes "Directory.Read.All"

# List subscriptions and assigned / total
Get-MgSubscribedSku | Select-Object SkuPartNumber,
  @{N="Purchased";E={$_.PrepaidUnits.Enabled}},
  @{N="Assigned";E={$_.ConsumedUnits}} |
  Where-Object { $_.Purchased -gt 0 }
```
```powershell
# Connect vCenter
Connect-VIServer -Server vcenter.corp.example.com

# License usage
Get-View -ViewType LicenseManager | ForEach-Object {
  $_.Licenses | Select-Object Name, Total, Used, @{N="Available";E={$_.Total - $_.Used}}
}
```
```sql
-- Logical CPU count (for per-core licensing)
SELECT cpu_count, hyperthread_ratio,
       cpu_count / hyperthread_ratio AS physical_cores
FROM sys.dm_os_sys_info;

-- SQL Server edition and version
SELECT @@VERSION;
SELECT SERVERPROPERTY('Edition') AS edition, SERVERPROPERTY('ProductVersion') AS version;
```
```bash
# Script to check license expiry from a CSV inventory
# columns: Product,ExpiryDate,RenewalOwner
awk -F',' 'NR>1 {
  cmd = "date -d \"" $2 "\" +%s"
  cmd | getline expiry; close(cmd)
  now = systime()
  days = int((expiry - now) / 86400)
  if (days < 90) print "WARNING: " $1 " expires in " days " days — owner: " $3
}' license-inventory.csv
```
