---
tags:
  - security
---
# Access Review Procedure


<div class="kb-summary">
Periodic access reviews ensure that users and service accounts hold only the permissions required for their current role. Reviews reduce the blast radius of credential compromise and satisfy audit requirements.
</div>
```text
┌─────────────────────────────────────── Security Access Review ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Access Review: Security Access Review platform                        │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Security Access Review management console                     │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Access Review infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Access Review      = Security Access Review platform overview and core concepts                    │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Review workflows, AD exports, stale account cleanup, audit evidence</div>
  </a>
</div>

## Review Schedule

| Scope | Frequency | Owner |
|---|---|---|
| Privileged / admin accounts | Quarterly | Security team |
| Standard user accounts | Semi-annual | IT operations |
| Service accounts | Quarterly | Application owners |
| External / contractor accounts | Monthly | IT operations |
| Shared / generic accounts | Quarterly | Security team |

## Active Directory — Export and Review

```powershell
# Export all enabled users with last logon and group membership
Get-ADUser -Filter {Enabled -eq $true} -Properties LastLogonDate, MemberOf |
  Select-Object Name, SamAccountName, LastLogonDate,
    @{N='Groups';E={($_.MemberOf | ForEach-Object { (Get-ADGroup $_).Name }) -join '; '}} |
  Export-Csv C:\access-review\users-$(Get-Date -Format yyyyMMdd).csv -NoTypeInformation

# Find accounts inactive for >90 days
$cutoff = (Get-Date).AddDays(-90)
Get-ADUser -Filter {Enabled -eq $true -and LastLogonDate -lt $cutoff} -Properties LastLogonDate |
  Select-Object Name, SamAccountName, LastLogonDate | Sort-Object LastLogonDate
```

## Privileged Account Review

```powershell
# List all Domain Admins
Get-ADGroupMember -Identity "Domain Admins" | Select-Object Name, SamAccountName, ObjectClass

# List all members of Administrators group
Get-ADGroupMember -Identity "Administrators" | Select-Object Name, SamAccountName, ObjectClass

# Find accounts with AdminCount=1 (had privileged group at some point)
Get-ADUser -Filter {AdminCount -eq 1 -and Enabled -eq $true} | Select-Object Name, SamAccountName
```

## Service Account Review

```powershell
# Find service accounts (by naming convention or OU)
Get-ADUser -Filter * -SearchBase "OU=ServiceAccounts,DC=domain,DC=com" -Properties PasswordLastSet, LastLogonDate, Description |
  Select-Object Name, SamAccountName, PasswordLastSet, LastLogonDate, Description
```

## Inactive and Stale Account Cleanup

```powershell
# Disable accounts inactive > 90 days (after review and approval)
$cutoff = (Get-Date).AddDays(-90)
Get-ADUser -Filter {Enabled -eq $true -and LastLogonDate -lt $cutoff} -Properties LastLogonDate |
  Disable-ADAccount -WhatIf   # Remove -WhatIf to execute

# Move disabled accounts to a holding OU before deletion
Get-ADUser -Filter {Enabled -eq $false} -SearchBase "OU=Users,DC=domain,DC=com" |
  Move-ADObject -TargetPath "OU=Disabled,DC=domain,DC=com" -WhatIf
```

## Linux / POSIX Account Review

```bash
# List all non-system users
awk -F: '$3 >= 1000 {print $1, $3, $6, $7}' /etc/passwd

# Last login for all users
lastlog | grep -v "Never logged in" | sort -k4 -r

# Sudoers with unrestricted access
grep -E "^\w+.*ALL.*ALL" /etc/sudoers /etc/sudoers.d/* 2>/dev/null
```

## Review Workflow

1. **Export** — generate user/access report from AD and relevant systems
2. **Distribute** — send lists to line managers and application owners for sign-off
3. **Collect decisions** — approved / revoke / transfer for each account
4. **Remediate** — disable or remove accounts per decisions; update group memberships
5. **Document** — record approvals, changes made, and reviewer sign-off in the ticket
6. **Verify** — re-run export after changes; confirm no accounts missed

## Checklist

- [ ] Privileged accounts reviewed and approved by security team
- [ ] Inactive accounts (>90 days) disabled and moved to holding OU
- [ ] Service accounts confirmed still required; passwords within rotation policy
- [ ] External/contractor accounts checked against active contractors list
- [ ] Shared/generic accounts reviewed; owners documented
- [ ] Evidence of review stored (CSV exports, approval records) for audit
