# IRE Security

```powershell
# Verify IRE local admin accounts are not shared with production
$prodAdmins = (Invoke-Command -ComputerName prod-dc01 { Get-ADGroupMember Administrators }).Name
$ireAdmins  = (Invoke-Command -ComputerName ire-dc01  { Get-ADGroupMember Administrators }).Name
Compare-Object $prodAdmins $ireAdmins -IncludeEqual | Where-Object {$_.SideIndicator -eq "=="}
# Should return empty — no overlapping accounts
```

```text
┌──────────────────────────────────────────── IRE Security ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        IRE Security — access control, two-person integrity, audit logging in the vault        │   │
│   │                   See product-specific sub-sections for detailed procedures                   │   │
│   │          DR success depends on: documented runbooks · tested failover · validated RTO         │   │
│   │          Minimum DR posture: defined RPO/RTO · tested backups · known escalation path         │   │
│   │        Test DR procedures quarterly; document results; update runbooks after each test        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Production site · DR site · Replication link · Management network · Vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; max acceptable data loss window                            │
│  RTO           = Recovery Time Objective; max acceptable downtime before restore                      │
│  Failover      = activating the DR site; redirecting hosts to replica resources                       │
│  Failback      = returning operations to production site after DR resolved                            │
│  Runbook       = step-by-step documented procedure for a specific DR scenario                         │
│  IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery                    │
│  Clean Room    = isolated vCenter + workstations for cyber recovery validation                        │
│  Air Gap       = network isolation preventing attacker lateral movement to vault                      │
│  DR Test       = planned failover test; validates RTO without real disaster                           │
│  Replication   = continuous or periodic data copy to secondary site or vault                          │
│  Recovery Tier = classification: hot/warm/cold based on RTO requirement                               │
│  BIA           = Business Impact Analysis; drives RPO/RTO targets per system                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Syslog forwarding to isolated log server (IRE-internal only)
# /etc/rsyslog.d/ire-audit.conf
*.* @@10.200.254.10:514   # IRE syslog server — no route to production

# Azure: route IRE activity logs to separate Log Analytics workspace
az monitor diagnostic-settings create \
  --resource /subscriptions/<ire-sub-id>/resourceGroups/ire-rg \
  --name "ire-audit" \
  --workspace <ire-log-analytics-workspace-id> \
  --logs '[{"category":"Administrative","enabled":true},{"category":"Security","enabled":true}]'
```
```bash
# Azure: deallocate and delete IRE VMs after sign-off
az vm list --resource-group ire-rg --output table
az vm delete --resource-group ire-rg --name <ire-vm> --yes --no-wait

# Rotate break-glass account passwords
$newPass = [System.Web.Security.Membership]::GeneratePassword(32, 6)
Set-ADAccountPassword -Identity ire-breakglass -NewPassword (ConvertTo-SecureString $newPass -AsPlainText -Force)
# Print and seal in envelope — never store in digital form
```
