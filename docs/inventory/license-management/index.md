# License Management

Track software entitlements, monitor utilisation against purchased seats, and prevent compliance violations.

## License Inventory — Key Attributes

| Field | Description |
|---|---|
| Product name | Software title and version |
| Vendor | Publisher / licensor |
| License type | Per-seat, per-core, per-server, subscription, open-source |
| Quantity purchased | Total entitlements |
| Quantity deployed | Current installations (from discovery) |
| Expiry date | Maintenance or subscription end date |
| Contract / PO reference | Procurement document |
| Renewal owner | Who is responsible for renewal |

## Discovery — Installed Software

### Linux

```bash
# Debian / Ubuntu — list installed packages
dpkg -l | awk '{print $2, $3}' | grep -v "^ii"  # filter to installed only
dpkg-query -W -f='${Package} ${Version}\n'

# RHEL / Rocky — list installed
rpm -qa --qf "%{NAME} %{VERSION}-%{RELEASE}\n" | sort

# Running processes (for unlicensed software audit)
ps aux --sort=-%cpu | awk '{print $11}' | sort -u | head -30
```

### Windows

```powershell
# All installed software (Programs and Features)
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
  Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
  Where-Object { $_.DisplayName } | Sort-Object DisplayName | Export-Csv installed-software.csv -NoTypeInformation

# 64-bit apps
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
  Select-Object DisplayName, DisplayVersion, Publisher | Where-Object { $_.DisplayName }

# Windows features (server roles)
Get-WindowsFeature | Where-Object Installed
```

### AWS — Software Inventory via SSM

```bash
# View software inventory for an instance
aws ssm list-inventory-entries \
  --instance-id <instance-id> \
  --type-name "AWS:Application" \
  --query 'Entries[*].{Name:Name,Version:Version,Publisher:Publisher}' --output table

# Aggregate across all managed instances
aws ssm list-resource-data-sync
aws ssm get-inventory \
  --filters "Key=AWS:Application.Name,Values=Oracle*,Type=BeginWith" \
  --query 'Entities[*].Data.AWS:Application.Content[*]' --output table
```

## License Utilisation — Common Products

### Microsoft 365

```powershell
# Connect to Microsoft Graph (requires MgGraph module)
Connect-MgGraph -Scopes "Directory.Read.All"

# List subscriptions and assigned / total
Get-MgSubscribedSku | Select-Object SkuPartNumber,
  @{N="Purchased";E={$_.PrepaidUnits.Enabled}},
  @{N="Assigned";E={$_.ConsumedUnits}} |
  Where-Object { $_.Purchased -gt 0 }
```

### VMware vSphere

```powershell
# Connect vCenter
Connect-VIServer -Server vcenter.corp.example.com

# License usage
Get-View -ViewType LicenseManager | ForEach-Object {
  $_.Licenses | Select-Object Name, Total, Used, @{N="Available";E={$_.Total - $_.Used}}
}
```

### SQL Server — Core License Audit

```sql
-- Logical CPU count (for per-core licensing)
SELECT cpu_count, hyperthread_ratio,
       cpu_count / hyperthread_ratio AS physical_cores
FROM sys.dm_os_sys_info;

-- SQL Server edition and version
SELECT @@VERSION;
SELECT SERVERPROPERTY('Edition') AS edition, SERVERPROPERTY('ProductVersion') AS version;
```

## Expiry Monitoring

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

## License Compliance Checklist

- [ ] Software inventory collected from all managed systems this month
- [ ] Deployed count compared to purchased seats — no over-deployment
- [ ] Licenses expiring within 90 days identified and renewal initiated
- [ ] Unused licences (0 active users for 90+ days) flagged for reclamation
- [ ] Open-source licences reviewed for GPL/AGPL copyleft obligations
- [ ] Audit trail maintained for licence purchases and decommissions

## Licence Risk Matrix

| Risk | Condition | Action |
|---|---|---|
| Over-deployed | Installed > purchased | Reduce deployments or purchase additional |
| Near expiry | < 90 days to expiry | Initiate renewal; notify procurement |
| Expired | Past expiry date | Cease use immediately; renew or remove |
| Unlicensed software | Found in discovery, no licence record | Uninstall or acquire licence within 30 days |
| Copyleft dependency | GPL/AGPL in commercial product | Legal review before distribution |

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Discovery shows more installs than expected | Shared installs? VMs cloned with software? | Audit VM templates; remove duplicate installs |
| Microsoft licence count mismatch | Shared mailboxes consuming licences? | Review M365 Admin Centre assigned licences vs active users |
| SQL Server licence audit fails | Edition doesn't match purchased | Downgrade to licensed edition or purchase upgrade |
| SSM inventory incomplete | Not all instances managed? | Verify SSM agent installed and IAM role has `ssm:PutInventory` |
