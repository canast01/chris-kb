---
tags:
  - operations
  - powershell
---
# PowerShell — Install & Upgrade

```powershell
# Using winget (Windows 10/11)
winget install --id Microsoft.PowerShell --source winget

# Or via MSI — download from github.com/PowerShell/PowerShell/releases
# After install, verify:
pwsh --version
```
```text
┌─────────────────────────────────── PowerShell — Install & Upgrade ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   PowerShell 7 install: MSI (Windows), package manager (brew, apt, yum), or GitHub releases   │   │
│   │      Upgrade: download new MSI and run; side-by-side with PS 5.1 on Windows; no conflict      │   │
│   │      Module updates: Update-Module -Force; or pin specific version with -RequiredVersion      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Windows Install                │  │                Linux Install                │   │
│   │     winget install Microsoft.PowerShell      │  │       snap install powershell (Ubuntu)      │   │
│   │         Or: download MSI from GitHub         │  │       brew install powershell (macOS)       │   │
│   │       $PSVersionTable (verify version)       │  │         pwsh (launch after install)         │   │
│   │          Update: winget upgrade PS           │  │            apt upgrade powershell           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Side-by-side = PS 7 and 5.1 coexist on Windows; PS 7 binary: pwsh.exe, 5.1: powershell.exe  │   │
│   │     Profile       = $PROFILE; per-user or all-users startup script; loads modules, aliases    │   │
│   │     NuGet provider= required for PSGallery; Install-PackageProvider -Name NuGet if missing    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell
# Update all user-scope modules
Get-Module -ListAvailable | Where-Object { $_.RepositorySourceLocation } |
    Select-Object -ExpandProperty Name -Unique |
    ForEach-Object {
        try {
            Update-Module $_ -Confirm:$false -ErrorAction Stop
            Write-Host "Updated: $_" -ForegroundColor Green
        } catch {
            Write-Warning "Skipped $_: $($_.Exception.Message)"
        }
    }
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powershell — Deploy](../../deploy/)
