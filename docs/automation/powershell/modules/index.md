# PowerShell Modules

## Installing Modules from PSGallery

PowerShell Gallery is the central repository for PowerShell modules.

```powershell
# Find a module before installing
Find-Module -Name PSReadLine
Find-Module -Name *Azure* | Select-Object -First 10

# Install for current user (no admin required)
Install-Module -Name Posh-Git -Scope CurrentUser -Force

# Install system-wide (requires admin)
Install-Module -Name PSWindowsUpdate -Scope AllUsers

# Install a specific version
Install-Module -Name Az -RequiredVersion 12.0.0 -AllowClobber

# Trust the PSGallery repository
Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
```

## Import-Module and Auto-Loading

Modules in `$PSModulePath` directories are auto-loaded on first use in PowerShell 3+.

```powershell
# Manually import a module
Import-Module -Name ActiveDirectory
Import-Module -Name C:\Modules\MyModule\MyModule.psd1

# Import with prefix to avoid name conflicts
Import-Module -Name AzureRM -Prefix AzureRM

# Force reimport (reload changed module)
Import-Module -Name MyModule -Force

# List all currently loaded modules
Get-Module

# List all available modules (installed but not loaded)
Get-Module -ListAvailable

# Show which commands a module provides
Get-Command -Module ActiveDirectory | Select-Object Name, CommandType
```

## Module Versioning and Side-by-Side Installs

```powershell
# Install multiple versions side by side
Install-Module -Name Az -RequiredVersion 11.0.0 -AllowClobber
Install-Module -Name Az -RequiredVersion 12.0.0 -AllowClobber

# Import a specific version
Import-Module -Name Az -RequiredVersion 11.0.0

# Check installed versions
Get-InstalledModule -Name Az -AllVersions | Select-Object Version, InstalledDate

# Uninstall a specific version
Uninstall-Module -Name Az -RequiredVersion 11.0.0

# Update a module to the latest version
Update-Module -Name Az -Scope CurrentUser
```

## Module Manifest and Structure

```powershell
# Scaffold a new module
$manifestParams = @{
    Path              = 'C:\Modules\MyModule\MyModule.psd1'
    RootModule        = 'MyModule.psm1'
    ModuleVersion     = '1.0.0'
    Author            = 'Your Name'
    Description       = 'Module description'
    PowerShellVersion = '5.1'
    FunctionsToExport = @('Get-Something', 'Set-Something')
}
New-ModuleManifest @manifestParams
```

Module directory layout:

```
MyModule/
  MyModule.psd1   # manifest (metadata)
  MyModule.psm1   # root script module
  Public/         # exported functions
    Get-Something.ps1
  Private/        # internal helpers
    Invoke-Helper.ps1
```

## PSGallery Module Management Reference

| Command | Purpose |
|---|---|
| `Find-Module` | Search PSGallery |
| `Install-Module` | Download and install |
| `Update-Module` | Update to latest or specific version |
| `Uninstall-Module` | Remove installed module |
| `Get-InstalledModule` | List installed modules |
| `Publish-Module` | Publish to PSGallery or private repo |
| `Register-PSRepository` | Add a private NuGet/PSGallery repo |

```powershell
# Register a private repository
Register-PSRepository -Name InternalRepo `
    -SourceLocation 'https://nexus.internal/nuget/psmodules/' `
    -InstallationPolicy Trusted

# Install from the private repo
Install-Module -Name InternalModule -Repository InternalRepo
```
