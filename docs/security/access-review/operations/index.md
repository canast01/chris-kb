---
tags:
  - operations
  - security
---
# Access Review — Procedures

<div class="kb-summary">
Step-by-step procedures for conducting, documenting, and remediating periodic access reviews across AD, service accounts, and privileged groups.
</div>

```text
┌───────────────────────────────────── Access Review — Operations ──────────────────────────────────────┐
│                                                                                                       │
│   Quarterly cycle: create campaign → assign managers → export AD snapshot → collect evidence          │
│   Scope: all AD users, service accounts, and tier-0 privileged groups (DA, EA, Schema Admins)         │
│   Tools: SailPoint / Saviynt / AD PowerShell; evidence in \\fileserver\Audit\AccessReview\            │
│   SLA: 10-business-day certification window; 5-day remediation SLA for access removal findings        │
│                                                                                                       │
│   Review types                                                                                        │
│   User access       Quarterly; managers certify direct-report memberships; 90-day inactivity cut      │
│   Service accounts  Confirm owner, group memberships, no interactive logon, 365-day rotation          │
│   Privileged groups DA / EA / Schema Admins; compare to approved register; remove unauthorised        │
│   AD group export   Get-ADGroupMember; pivot table; Compare-Object quarter-on-quarter                 │
│                                                                                                       │
│   Stale account remediation                                                                           │
│   Identify: Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly                        │
│   Step 1: Disable-ADAccount + move to Disabled Users OU                                               │
│   Step 2: Set-ADAccountExpiration +30 days (grace period for reinstatement requests)                  │
│   Step 3: Remove-ADUser after 30-day hold; log each removal with ticket reference                     │
│                                                                                                       │
│   Evidence package (AR-YYYYQQ)                                                                        │
│   Raw group membership CSV; reviewer sign-off log; removals/changes CSV; exception log                │
│   Hash each file: Get-FileHash | Export-Csv manifest.csv; upload to GRC platform                      │
│   Retain evidence ≥ 3 years; escalate SLA breaches to department head                                 │
│                                                                                                       │
│   Key terms:                                                                                          │
│   SailPoint / Saviynt = identity governance platforms for running access review campaigns             │
│   PAM justification  = privileged access ticket required for tier-0 group membership approval         │
│   tier-0 groups      = Domain Admins, Schema Admins, Enterprise Admins — highest AD privilege         │
│   inactive query     = Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly             │
│   GRC platform       = governance, risk, and compliance tool (e.g., ServiceNow GRC, Archer)           │
│   grace period       = 30-day expiry hold allowing account reinstatement before permanent removal     │
│   Compare-Object     = PowerShell cmdlet used to diff two CSVs and identify new quarter additions     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run Quarterly Access Review

Initiate a formal access review cycle to confirm that all user accounts hold only the access required for their current role.

1. Open the Identity Governance tool (e.g., SailPoint, Saviynt, or AD-based script) and create a new campaign scoped to all Active Directory users.
2. Set the review period to 90 days and assign managers as reviewers for their direct reports.
3. Export the current access snapshot: `Get-ADUser -Filter * -Properties MemberOf | Select-Object Name,SamAccountName,MemberOf | Export-Csv C:\AccessReview\users-$(Get-Date -Format yyyyMMdd).csv`.
4. Send the reviewer task list via email with a 10-business-day deadline.
5. Track completion percentage daily in the governance dashboard; chase non-respondents at the 5-day mark.
6. Close the campaign and capture the final approval log for audit evidence.

---

## Export AD Group Membership Report

Generate a full report of AD group memberships to support certification and audit activities.

1. Run the following PowerShell on a domain controller or a machine with RSAT installed:
   ```powershell
   Get-ADGroup -Filter * -SearchBase "OU=Security Groups,DC=corp,DC=local" |
     ForEach-Object {
       $g = $_.Name
       Get-ADGroupMember -Identity $_ -Recursive |
         Select-Object @{n='Group';e={$g}}, Name, SamAccountName, objectClass
     } | Export-Csv C:\AccessReview\group-membership-$(Get-Date -Format yyyyMMdd).csv -NoTypeInformation
   ```
2. Open the CSV in Excel and apply a pivot table grouped by `Group` to count members per group.
3. Flag any group with more than 50 members for targeted review.
4. Compare against the previous quarter's export to identify new additions: `Compare-Object (Import-Csv .\prev.csv) (Import-Csv .\current.csv) -Property SamAccountName`.
5. Save the report to the shared audit evidence folder under `\\fileserver\Audit\AccessReview\`.

---

## Remove Stale Accounts

Disable or delete accounts identified as inactive during the access review to reduce the attack surface.

1. Identify accounts inactive for more than 90 days:
   ```powershell
   $cutoff = (Get-Date).AddDays(-90)
   Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly |
     Select-Object Name,SamAccountName,LastLogonDate | Export-Csv C:\AccessReview\stale-accounts.csv
   ```
2. Cross-check the stale list against HR systems to confirm the employees are no longer active.
3. Disable (do not immediately delete) each confirmed stale account:
   ```powershell
   Disable-ADAccount -Identity <SamAccountName>
   Move-ADObject -Identity <DN> -TargetPath "OU=Disabled Users,DC=corp,DC=local"
   ```
4. Set an account expiry 30 days in the future to allow grace-period restoration: `Set-ADAccountExpiration -Identity <SamAccountName> -DateTime (Get-Date).AddDays(30)`.
5. After the 30-day hold, remove the account if no reinstatement request has been raised: `Remove-ADUser -Identity <SamAccountName> -Confirm:$false`.
6. Log each removal with the ticket reference in the access review evidence document.

---

## Review Service Account Access

Ensure service accounts hold only the minimum permissions needed for their function.

1. List all service accounts in their dedicated OU:
   ```powershell
   Get-ADUser -Filter * -SearchBase "OU=Service Accounts,DC=corp,DC=local" -Properties Description,MemberOf |
     Select-Object Name,SamAccountName,Description,MemberOf | Export-Csv C:\AccessReview\service-accounts.csv
   ```
2. For each service account, confirm there is a documented owner in the CMDB or service account register.
3. Review group memberships and remove any group that is not listed in the service account's approved access record.
4. Verify no service account has interactive logon rights unless explicitly approved: `Get-GPO -All | Get-GPOReport -ReportType XML | Select-String "SeInteractiveLogonRight"`.
5. Check that each service account password was rotated within the last 365 days; flag exceptions for immediate rotation.
6. Update the service account register with the review date and any changes made.

---

## Review Privileged Group Membership

Validate that membership in high-privilege AD groups (Domain Admins, Schema Admins, Enterprise Admins) is limited to authorised personnel.

1. Export membership of each tier-0 group:
   ```powershell
   foreach ($g in @("Domain Admins","Schema Admins","Enterprise Admins","Administrators")) {
     Get-ADGroupMember -Identity $g -Recursive |
       Select-Object @{n='Group';e={$g}}, Name, SamAccountName |
       Export-Csv "C:\AccessReview\$g-$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation -Append
   }
   ```
2. Compare current membership against the approved privileged access register.
3. For any member not on the register, immediately remove them: `Remove-ADGroupMember -Identity "Domain Admins" -Members <SamAccountName> -Confirm:$false`.
4. Confirm that all remaining members have an active PAM justification ticket.
5. Ensure each privileged account is a dedicated admin account (not the user's daily-use account).
6. Document the final approved membership list and obtain sign-off from the Security Manager.

---

## Document Access Review Evidence

Compile and store evidence required to demonstrate a completed access review to auditors.

1. Collect the following artefacts into a single evidence package folder named `AR-YYYYQQ`:
   - Raw group membership export (CSV)
   - Reviewer sign-off log (PDF or email thread)
   - List of accounts removed or access changed (CSV)
   - Exception log with approvals
2. Create a summary spreadsheet with sheets: `Summary`, `Removals`, `Exceptions`, `Sign-off`.
3. Hash each file for integrity: `Get-FileHash C:\AccessReview\AR-YYYYQQ\* | Export-Csv C:\AccessReview\AR-YYYYQQ\manifest.csv`.
4. Upload the evidence package to the GRC platform (e.g., ServiceNow GRC, Archer) linked to the relevant control record.
5. Retain the package for a minimum of 3 years in the `\\fileserver\Audit\AccessReview\` archive.

---

## Remediate Access Review Findings

Act on findings raised during the review cycle to bring access back into compliance.

1. Export all findings from the governance campaign into a remediation tracker spreadsheet with columns: `Finding`, `Account`, `Excess Access`, `Owner`, `Due Date`, `Status`.
2. Assign each finding to the account owner's manager with a 5-business-day remediation deadline.
3. For access removals, execute the change via the provisioning tool or directly in AD and record the ticket number.
4. Re-validate each remediation by re-running the membership report and confirming the excess access no longer appears.
5. Update the tracker status to `Closed` with the remediation date and evidence reference.
6. Report the overall remediation rate to the Security team at the end of the cycle.

---

## Escalate Unresolved Access Issues

Manage access review findings that are not remediated within the agreed SLA.

1. At SLA expiry, flag overdue items in the remediation tracker and generate an escalation report.
2. Send a formal escalation email to the account owner's department head with the finding details and deadline breach noted.
3. If the account poses an active risk (e.g., a leaver still with Domain Admin access), disable the account immediately and notify HR: `Disable-ADAccount -Identity <SamAccountName>`.
4. Raise a risk acceptance ticket in the GRC platform if business justification prevents immediate remediation; require CISO or VP sign-off.
5. Track each escalation to closure and include it in the quarterly security risk report.
