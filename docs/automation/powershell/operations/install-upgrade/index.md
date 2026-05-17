# PowerShell — Install & Upgrade

## Install PowerShell 7+ (Windows)

```powershell
# Using winget (Windows 10/11)
winget install --id Microsoft.PowerShell --source winget

# Or via MSI — download from github.com/PowerShell/PowerShell/releases
# After install, verify:
pwsh --version
```

## Install PowerShell 7+ (Linux)

```bash
# Ubuntu / Debian
sudo apt-get update
sudo apt-get install -y wget apt-transport-https
wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y powershell

# RHEL / CentOS
sudo rpm -Uvh https://packages.microsoft.com/config/rhel/8/packages-microsoft-prod.rpm
sudo dnf install -y powershell
```

## Install VMware PowerCLI

```powershell
# Install
Install-Module VMware.PowerCLI -Scope CurrentUser -AllowClobber -Force

# Configure (run once after install)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
Set-PowerCLIConfiguration -ParticipateInCeip $false -Confirm:$false

# Verify
Get-Module VMware.PowerCLI -ListAvailable | Select-Object Name, Version
```

## Upgrade PowerCLI

```powershell
# Check current version
Get-Module VMware.PowerCLI -ListAvailable | Select-Object Name, Version

# Unload current session modules
Get-Module VMware* | Remove-Module -Force

# Upgrade
Update-Module VMware.PowerCLI -Confirm:$false

# Verify
Get-Module VMware.PowerCLI -ListAvailable | Select-Object Name, Version
```

## Update All Installed Modules

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

## Version Reference

| Component | Min Recommended | Check Command |
|---|---|---|
| PowerShell | 7.2+ | `$PSVersionTable.PSVersion` |
| VMware.PowerCLI | 13.x+ | `Get-Module VMware.PowerCLI -ListAvailable` |
| .NET | 6.0+ | `dotnet --version` |
