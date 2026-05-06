# Connection & Session

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Connection & Session

```powershell
# Install PowerCLI
Install-Module VMware.PowerCLI -Scope CurrentUser
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
Set-PowerCLIConfiguration -ParticipateInCeip $false -Confirm:$false

# Connect
Connect-VIServer -Server <vcenter>
Connect-VIServer -Server <vcenter> -User <user> -Password <pass>
Disconnect-VIServer * -Confirm:$false

# Who am I
$global:DefaultVIServer
```
