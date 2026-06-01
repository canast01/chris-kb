# Venafi Scripts


<div class="kb-summary">
Automation scripts for Venafi cover certificate expiry reporting, automated renewal via VCert, discovery scan triggering, policy compliance reporting, and ADCS template alignment checking.
</div>

 Scripts are maintained in PowerShell (Windows environments) and Python (cross-platform / Linux runners).

All scripts authenticate via API token (not username/password) and should store credentials in a secrets manager or environment variable — never hardcoded.

| Script | Language | Purpose |
|---|---|---|
| `venafi-expiry-report.ps1` | PowerShell | Export certificates expiring within N days to CSV |
| `venafi-auto-renew.py` | Python | Trigger renewal for certificates past 80% validity via VCert |
| `venafi-discovery-trigger.ps1` | PowerShell | Initiate an Edge Proxy discovery scan via REST API |
| `venafi-policy-compliance.ps1` | PowerShell | Report certificates violating key algorithm or validity standards |
| `venafi-adcs-template-check.ps1` | PowerShell | Verify ADCS template assignments align with Venafi policy folder settings |

**Example: expiry report (PowerShell)**

```powershell
$token = $env:VENAFI_TOKEN
$tppUrl = "https://tpp.example.com"
$expireBefore = (Get-Date).AddDays(30).ToString("yyyy-MM-ddTHH:mm:ssZ")
$uri = "$tppUrl/vedsdk/certificates?ValidToLess=$expireBefore"
$certs = Invoke-RestMethod -Uri $uri -Headers @{ "X-Venafi-Token" = $token }
$certs.Certificates | Export-Csv -Path "expiring-certs.csv" -NoTypeInformation
```
