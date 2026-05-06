# Variables, Output & Pipeline

> Part of the PowerShell CLI Reference.

---

## Variables & Output

```powershell
# Variables
$myVar = "value"
$myArray = @(1, 2, 3)
$myHash = @{ key = "value" }

# Output
Write-Output "message"
Write-Host "message" -ForegroundColor Green
Write-Error "error message"
Write-Verbose "verbose" -Verbose

# Null check
if ($null -eq $var) { "null" }

# String formatting
"Server: $($server.Name)"
```

---

## Pipeline & Filtering

```powershell
# Common filters
Get-Service | Where-Object { $_.Status -eq "Running" }
Get-Process | Where-Object { $_.CPU -gt 10 }
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Select properties
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB

# Measure
Get-VM | Measure-Object MemoryGB -Sum -Average

# ForEach
Get-VM | ForEach-Object { Write-Host $_.Name }
1..10 | ForEach-Object { "Item $_" }
```
