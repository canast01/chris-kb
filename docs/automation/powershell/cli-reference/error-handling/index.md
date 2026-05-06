# Error Handling

> Part of the PowerShell CLI Reference.

---

```powershell
# Try/catch
try {
    Get-VM -Name "nonexistent" -ErrorAction Stop
} catch {
    Write-Error "Failed: $_"
}

# Error preference
$ErrorActionPreference = "Stop"     # Terminate on error
$ErrorActionPreference = "Continue" # Default

# -ErrorAction
Get-VM -Name "test" -ErrorAction SilentlyContinue
```
