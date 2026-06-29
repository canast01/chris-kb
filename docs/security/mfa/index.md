---
title: MFA
tags:
  - security
---

# Multi-Factor Authentication (MFA)

<div class="kb-summary">
Multi-Factor Authentication (MFA) reference covering Overview, MFA Authentication Flow, TOTP vs Push Comparison, Daily Checks, Health Commands and 1 more sections.
</div>

![Multi-Factor Authentication (MFA) — Diagram](../../assets/security-mfa-diagram.svg)

![Multi-Factor Authentication (MFA) — Diagram](../../assets/security-mfa-d2.svg)

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Authentication flows, MFA method management, health checks, enrollment</div>
  </a>
</div>

## Overview

MFA adds an additional authentication factor beyond passwords to protect accounts and systems from unauthorized access.

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review authentication failures |  |  |
| Validate MFA service availability |  |  |
| Confirm token synchronization |  |  |
| Review access logs |  |  |

## Health Commands

```bash
Get-MsolUser
Get-MsolCompanyInformation
```


```text title="Expected output"
UserPrincipalName                     DisplayName                    isLicensed
john.smith@contoso.onmicrosoft.com    John Smith                     True
sarah.jones@contoso.onmicrosoft.com   Sarah Jones                    True
admin@contoso.onmicrosoft.com         Admin Account                  True
guest_user@contoso.onmicrosoft.com    Guest User                     False

CompanyName                 : Contoso Corporation
CountryLetterCode           : US
PreferredLanguage           : en
MarketingNotificationEmails : {admin@contoso.onmicrosoft.com}
TechnicalNotificationEmails : {admin@contoso.onmicrosoft.com}
```

!!! warning "Common errors"
    **`Get-MsolUser : The term 'Get-MsolUser' is not recognized as the name of a cmdlet, function, script file, or operable program.`** — Install the MSOnline PowerShell module with `Install-Module MSOnline` and import it with `Import-Module MSOnline`.
    **`Get-MsolUser : You must call the Connect-MsolService cmdlet before calling any other cmdlets.`** — Authenticate to Microsoft 365 first by running `Connect-MsolService` and entering your admin credentials.
## Upgrade Workflow

1. Backup configuration
2. Validate identity provider connectivity
3. Apply updates
4. Test user authentication flows
