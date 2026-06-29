---
tags:
  - security
---
# Access Review Procedure

<div class="kb-summary">
Periodic access reviews ensure that users and service accounts hold only the permissions required for their current role. Reviews reduce the blast radius of credential compromise and satisfy audit requirements.
</div>

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


```text title="Expected output"
alice 1000 /home/alice /bin/bash
bob 1001 /home/bob /bin/bash
charlie 1002 /home/charlie /bin/nologin
diana 1003 /home/diana /bin/bash
eve 1004 /home/eve /bin/bash

alice                                    pts/0                192.168.1.45     Wed Dec 20 14:32:10 +0000 2024
bob                                      pts/2                10.0.2.15        Tue Dec 19 09:18:22 +0000 2024
charlie                                  pts/1                192.168.1.88     Mon Dec 18 16:45:01 +0000 2024
diana                                    tty1                 -                 Sun Dec 17 11:22:33 +0000 2024

/etc/sudoers:root	ALL=(ALL) ALL
/etc/sudoers:alice	ALL=(ALL) NOPASSWD: ALL
/etc/sudoers.d/admin-group:%admin	ALL=(ALL) ALL
```

!!! warning "Common errors"
    **`grep: /etc/sudoers.d/*: No such file or directory`** — Create the `/etc/sudoers.d/` directory with `mkdir -p /etc/sudoers.d/` or remove the glob pattern if the directory doesn't exist.
    **`awk: command not found`** — Install `gawk` or `mawk` package, or use `cut -d: -f1,3,6,7 /etc/passwd` as an alternative.
    **`lastlog: command not found`** — Install the `util-linux` package which provides the `lastlog` utility.
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
