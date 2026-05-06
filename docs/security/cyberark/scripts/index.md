# CyberArk Scripts

The scripts below use the `psPAS` PowerShell module and the PVWA REST API to automate routine CyberArk operational and audit tasks. All scripts require a PVWA service account with appropriate safe-level and administrative permissions; avoid using a personal admin account for scheduled automation.

| Script | Purpose |
|---|---|
| `Get-RotationStatusReport.ps1` | Queries all accounts via `Get-PASAccount` and flags those with `CPMStatus -ne "success"` or last rotation older than policy threshold; exports to CSV |
| `Get-SafeMembershipAudit.ps1` | Iterates all safes via `Get-PASSafe` and exports each safe's members with permission level using `Get-PASSafeMember`; used for quarterly access review |
| `Send-FailedRotationAlert.ps1` | Runs on schedule; calls PVWA API to detect failed CPM rotation jobs and sends email alert with account name, safe, and failure reason |
| `Add-AccountOnboarding.ps1` | Automates account onboarding via `Add-PASAccount` with standard platform, safe, and policy settings; validates safe exists before creating account |
| `Get-SessionRecordingInventory.ps1` | Lists all PSM recordings via `Get-PASRecording` for a specified date range, exports to CSV including user, target, duration, and safe |
