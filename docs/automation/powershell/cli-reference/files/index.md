# Files & Filesystem

> Part of the PowerShell CLI Reference.

---

```powershell
# Navigation
Get-Location
Set-Location C:\scripts
Get-ChildItem
Get-ChildItem -Recurse -Filter "*.ps1"

# File operations
New-Item -Path ".\file.txt" -ItemType File
Copy-Item source.txt dest.txt
Move-Item source.txt dest\
Remove-Item file.txt
Get-Content file.txt
Set-Content file.txt "content"
Add-Content file.txt "new line"

# CSV / JSON
Import-Csv data.csv
Export-Csv -Path output.csv -NoTypeInformation
$obj | ConvertTo-Json
$json | ConvertFrom-Json

# Test path
Test-Path "C:\scripts\file.ps1"
```
