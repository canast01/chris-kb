# Windows Server — Lifecycle

## Version Support Matrix

| Version | GA Date | Mainstream Support End | Extended Support End | Notes |
|---------|---------|----------------------|---------------------|-------|
| Windows Server 2016 | Oct 2016 | Jan 2022 | Jan 2027 | In extended support; no new features |
| Windows Server 2019 | Nov 2018 | Jan 2024 | Jan 2029 | In extended support |
| Windows Server 2022 | Aug 2021 | Oct 2026 | Oct 2031 | Current mainstream |
| Windows Server 2025 | Nov 2024 | Oct 2029 | Oct 2034 | Latest release; preferred for new builds |

> Mainstream support includes new feature additions and non-security fixes. Extended support includes security updates only. After extended support ends, patches require a paid ESU (Extended Security Update) contract.

## Patching Tools

| Tool | Use Case |
|------|---------|
| Windows Update (direct) | Standalone servers; small environments |
| WSUS | On-premises update approval and distribution; no additional cost |
| SCCM / MECM | Enterprise patch orchestration; software deployment; OS deployment |
| Windows Update for Business | Cloud-managed via Intune/Azure AD; ring-based deployment |
| Azure Arc + Azure Update Manager | Hybrid patch management for on-prem + Azure VMs |

## Patching Cadence

| Cycle | Description |
|-------|-------------|
| Patch Tuesday | Second Tuesday of each month; Microsoft releases cumulative updates |
| Out-of-band | Critical zero-day patches released outside Patch Tuesday cycle |
| Preview | Optional preview updates released third Tuesday (non-security fixes) |
| Servicing Stack Updates (SSU) | Released as needed; must be applied before cumulative updates |

Recommended patching rings:

1. **Dev/Test** — Apply within 48 hours of Patch Tuesday
2. **Pre-production** — Apply 7 days after Patch Tuesday (after dev validation)
3. **Production** — Apply 14–21 days after Patch Tuesday (after pre-prod validation)

## Upgrade Paths

| From | To | Method |
|------|----|--------|
| 2016 | 2019 | In-place upgrade or fresh install |
| 2016 | 2022 | In-place upgrade (2016 → 2019 → 2022) or fresh install |
| 2019 | 2022 | In-place upgrade or fresh install |
| 2019 | 2025 | Fresh install recommended; in-place supported |
| 2022 | 2025 | In-place upgrade or fresh install |

> In-place upgrades preserve installed roles, data, and settings. Always take a full backup or VM snapshot before proceeding. Test in a non-production environment first.

## EOL Planning

Actions required 12 months before extended support ends:

- [ ] Identify all servers running the EOL version (`Get-ADComputer` with OS filter)
- [ ] Classify by workload: lift-and-shift, re-platform, decommission
- [ ] Test application compatibility on target OS version
- [ ] Plan maintenance windows for upgrades
- [ ] Update CMDB with new OS version on completion
- [ ] Verify monitoring agents support the new OS version

```powershell
# Find all servers running a specific OS version
Get-ADComputer -Filter {OperatingSystem -like "*2016*"} `
  -Properties OperatingSystem, OperatingSystemVersion |
  Select-Object Name, OperatingSystem, OperatingSystemVersion |
  Sort-Object Name
```

## Hotfix and Patch Status

```powershell
# Last 10 installed hotfixes
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10

# Check Windows Update history
Get-WUHistory  # Requires PSWindowsUpdate module

# Pending updates check
Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate

# WSUS-managed patch status
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software'")
$SearchResult.Updates | Select-Object Title, MsrcSeverity
```

## Related Sections

- [Patching](../patching/) — patching procedures and runbooks
- [Standards](../standards/) — build baseline
- [Operations](../operations/) — daily health checks
