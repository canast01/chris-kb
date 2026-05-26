# PowerShell — Coding Standards

Consistent standards reduce review friction, improve reliability, and make automation maintainable by the whole team — not just the original author.

---

## Approved Verbs

PowerShell enforces a fixed set of approved verbs. Using unapproved verbs generates a warning on module import and breaks discoverability conventions.

```powershell
# List all approved verbs
Get-Verb | Sort-Object Group, Verb | Format-Table -AutoSize
```
```

Root module pattern — dot-source all files:

```powershell
# MyModule.psm1
$Private = Get-ChildItem -Path "$PSScriptRoot/Private" -Filter '*.ps1' -Recurse
$Public  = Get-ChildItem -Path "$PSScriptRoot/Public"  -Filter '*.ps1' -Recurse

foreach ($file in ($Private + $Public)) {
    try   { . $file.FullName }
    catch { Write-Error "Failed to import $($file.FullName): $_" }
}

Export-ModuleMember -Function $Public.BaseName
```

---

## Parameter Validation Attributes

Always validate parameters at the function boundary — never inside the function body.

```powershell
function Set-Widget {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
    param (
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [ValidateNotNullOrEmpty()]
        [string]$Name,

        [Parameter(Mandatory)]
        [ValidateRange(1, 100)]
        [int]$Priority,

        [Parameter()]
        [ValidateSet('Active', 'Inactive', 'Maintenance')]
        [string]$State = 'Active',

        [Parameter()]
        [ValidatePattern('^[A-Z]{2}-\d{4}$')]
        [string]$Code,

        [Parameter()]
        [ValidateScript({
            if (Test-Path $_) { $true }
            else { throw "Path '$_' does not exist." }
        })]
        [string]$ConfigPath
    )

    process {
        if ($PSCmdlet.ShouldProcess($Name, 'Set-Widget')) {
            # implementation
        }
    }
}
```

Key attributes reference:

| Attribute | Purpose |
|---|---|
| `[Parameter(Mandatory)]` | Force caller to supply a value |
| `[Parameter(ValueFromPipeline)]` | Accept pipeline input by value |
| `[Parameter(ValueFromPipelineByPropertyName)]` | Accept pipeline input by property name |
| `[ValidateNotNullOrEmpty()]` | Reject null or empty string |
| `[ValidateSet(...)]` | Restrict to enumerated values |
| `[ValidateRange(min,max)]` | Numeric range enforcement |
| `[ValidatePattern(regex)]` | Regex format validation |
| `[ValidateScript({...})]` | Arbitrary validation logic |
| `[Alias('n')]` | Alternative parameter name |

---

## Error Handling

PowerShell has two error types: **terminating** (exceptions, thrown with `throw`) and **non-terminating** (reported with `Write-Error`). Use `$ErrorActionPreference = 'Stop'` or `-ErrorAction Stop` to promote non-terminating errors to terminating.

```powershell
function Invoke-WidgetDeploy {
    [CmdletBinding()]
    param([string]$WidgetName)

    # Promote all errors to terminating within this scope
    $ErrorActionPreference = 'Stop'

    try {
        Write-Verbose "Starting deployment of $WidgetName"

        $result = Invoke-RestMethod -Uri "https://api.example.com/widgets/$WidgetName" `
                                    -Method Post `
                                    -ErrorAction Stop

        Write-Verbose "Deployment response: $($result.status)"
        return $result
    }
    catch [System.Net.WebException] {
        # Specific exception type — handle network errors
        Write-Error "Network error deploying $WidgetName`: $_" -ErrorAction Stop
    }
    catch [System.UnauthorizedAccessException] {
        Write-Error "Access denied for $WidgetName`: $_" -ErrorAction Stop
    }
    catch {
        # Catch-all for unexpected errors
        Write-Error "Unexpected error deploying $WidgetName`: $($_.Exception.Message)"
        throw  # Re-throw to preserve stack trace for caller
    }
    finally {
        # Always runs — use for cleanup regardless of success/failure
        Write-Verbose "Deployment attempt for $WidgetName complete"
    }
}
```

---

## Logging Standards

### Write-EventLog (Windows — Structured System Log)

```powershell
# Register event source once (requires admin)
New-EventLog -LogName Application -Source 'WidgetAutomation' -ErrorAction SilentlyContinue

function Write-AutomationEvent {
    param(
        [string]$Message,
        [ValidateSet('Information','Warning','Error')]
        [string]$EntryType = 'Information',
        [int]$EventId = 1000
    )
    Write-EventLog -LogName Application `
                   -Source 'WidgetAutomation' `
                   -EntryType $EntryType `
                   -EventId $EventId `
                   -Message $Message
}
```

### Structured JSON Logging (cross-platform)

```powershell
function Write-StructuredLog {
    param(
        [string]$Level,
        [string]$Message,
        [hashtable]$Properties = @{}
    )

    $entry = [ordered]@{
        timestamp   = (Get-Date -Format 'o')   # ISO 8601
        level       = $Level.ToUpper()
        message     = $Message
        host        = $env:COMPUTERNAME
        pid         = $PID
        script      = $PSCommandPath
    } + $Properties

    $entry | ConvertTo-Json -Compress | Tee-Object -FilePath $LogPath -Append
}

# Usage
Write-StructuredLog -Level 'INFO' -Message 'Widget deployed' -Properties @{
    widget = 'widget-42'
    duration_ms = 342
}
```

### PSFramework Logging (recommended for modules)

```powershell
Import-Module PSFramework

Set-PSFLoggingProvider -Name FileSystem -Enabled $true `
    -FilePath 'C:\Logs\widget-%Date%.log'

Write-PSFMessage -Level Important -Message "Widget $Name deployed successfully"
Write-PSFMessage -Level Warning   -Message "Widget $Name in degraded state" -Tag 'health'
Write-PSFMessage -Level Error     -Message "Widget deployment failed" -ErrorRecord $_
```

---

## Comment-Based Help

Every exported function must have comment-based help. This powers `Get-Help` and PlatyPS documentation generation.

```powershell
function Get-Widget {
    <#
    .SYNOPSIS
        Retrieves one or more widget objects from the widget service.

    .DESCRIPTION
        Get-Widget queries the widget service API and returns widget objects
        matching the specified criteria. Supports pipeline input and wildcards.

    .PARAMETER Name
        The name of the widget to retrieve. Accepts wildcards.

    .PARAMETER State
        Filter widgets by operational state. Valid values: Active, Inactive, Maintenance.

    .EXAMPLE
        Get-Widget -Name 'widget-*'
        Returns all widgets whose name starts with 'widget-'.

    .EXAMPLE
        Get-Widget -State Inactive | Remove-Widget
        Retrieves all inactive widgets and pipes them to removal.

    .INPUTS
        System.String. You can pipe widget names to Get-Widget.

    .OUTPUTS
        PSCustomObject. Returns widget objects with Name, State, and Priority properties.

    .NOTES
        Author:  Platform Automation Team
        Version: 1.2.0
        Requires API key in environment variable WIDGET_API_KEY.
    #>
    [CmdletBinding()]
    param (
        [Parameter(ValueFromPipeline)]
        [string]$Name = '*',

        [ValidateSet('Active','Inactive','Maintenance')]
        [string]$State
    )
    process { <# implementation #> }
}
```

---

## Testing with Pester

All exported functions require Pester tests. Target **Pester 5.x**.

```powershell
# Tests/Get-Widget.Tests.ps1
BeforeAll {
    Import-Module "$PSScriptRoot/../MyModule.psd1" -Force
}

Describe 'Get-Widget' {
    Context 'When the API returns results' {
        BeforeEach {
            Mock Invoke-RestMethod {
                return [PSCustomObject]@{ Name = 'widget-01'; State = 'Active'; Priority = 5 }
            } -ModuleName MyModule
        }

        It 'Returns a widget object with expected properties' {
            $result = Get-Widget -Name 'widget-01'
            $result.Name     | Should -Be 'widget-01'
            $result.State    | Should -Be 'Active'
        }

        It 'Calls the API with the correct URI' {
            Get-Widget -Name 'widget-01'
            Should -Invoke Invoke-RestMethod -Times 1 -ModuleName MyModule `
                   -ParameterFilter { $Uri -like '*widget-01*' }
        }
    }

    Context 'When the API is unreachable' {
        BeforeEach {
            Mock Invoke-RestMethod { throw 'Connection refused' } -ModuleName MyModule
        }

        It 'Throws a terminating error' {
            { Get-Widget -Name 'widget-01' } | Should -Throw
        }
    }
}
```

Run tests:

```powershell
# Run all tests with detailed output
Invoke-Pester -Path ./Tests -Output Detailed

# With code coverage
Invoke-Pester -Path ./Tests -CodeCoverage ./Public/*.ps1 -CodeCoverageOutputFile coverage.xml

# CI — output NUnit XML for test reporting
Invoke-Pester -Path ./Tests -OutputFormat NUnitXml -OutputFile test-results.xml
```

---

## Checklist: New Function Review

- [ ] Approved verb used
- [ ] `[CmdletBinding()]` present
- [ ] All parameters validated with attributes
- [ ] `SupportsShouldProcess` added for state-changing operations
- [ ] `try/catch/finally` wraps all external calls
- [ ] `$ErrorActionPreference = 'Stop'` set where appropriate
- [ ] Comment-based help complete (Synopsis, Description, all Parameters, at least 2 Examples)
- [ ] Pester tests written (happy path + at least one error path)
- [ ] No hardcoded credentials or paths
- [ ] `Write-Verbose` present for key decision points
