# Remoting (PSSession)

> Part of the PowerShell CLI Reference.

---

```powershell
# Connect to remote host
Enter-PSSession -ComputerName <host>
Exit-PSSession

# Persistent session
$session = New-PSSession -ComputerName <host>
Invoke-Command -Session $session -ScriptBlock { Get-Service }
Remove-PSSession $session

# Run command on multiple hosts
$servers = @("srv1", "srv2")
Invoke-Command -ComputerName $servers -ScriptBlock { hostname }
```
