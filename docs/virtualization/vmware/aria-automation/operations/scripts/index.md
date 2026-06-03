# Aria Automation — Scripts Reference

```powershell
# Get-FailedDeployments.ps1
# Returns all deployments that failed in the last 24 hours.

param(
    [Parameter(Mandatory)][string]$Server,
    [Parameter(Mandatory)][string]$Username,
    [Parameter(Mandatory)][SecureString]$Password
)

$PlainPass = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password)
)

# Authenticate
$LoginBody = @{ username = $Username; password = $PlainPass } | ConvertTo-Json
$TokenResponse = Invoke-RestMethod -Method POST `
    -Uri "https://$Server/csp/gateway/am/api/login" `
    -Body $LoginBody -ContentType "application/json"
$Token = $TokenResponse.access_token

$Headers = @{ Authorization = "Bearer $Token" }

# Fetch deployments with status FAILED
$Deployments = Invoke-RestMethod -Method GET `
    -Uri "https://$Server/deployment/api/deployments?status=FAILED&`$top=100" `
    -Headers $Headers

$CutOff = (Get-Date).AddHours(-24)

$Results = $Deployments.content | Where-Object {
    [datetime]$_.lastUpdatedAt -ge $CutOff
} | Select-Object name, id, status, lastUpdatedAt

if ($Results) {
    $Results | Format-Table -AutoSize
} else {
    Write-Host "No failed deployments in the last 24 hours."
}
```

```text
┌───────────────────────────────── Aria Automation — Scripts Reference ─────────────────────────────────┐
│                                                                                                       │
│  vRA scripting uses ABX actions (Python/Node/PS), Orchestrator workflows, and REST API calls.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             ABX Action Examples              │  │         Orchestrator Script Examples        │   │
│   │         Python: tag VM after deploy          │  │         vCenter: snapshot VM via API        │   │
│   │        Node.js: call ServiceNow REST         │  │         AD: create computer account         │   │
│   │         PowerShell: run WinRM on VM          │  │          NSX: create security group         │   │
│   │          Python: update CMDB record          │  │         DNS: add A record via plugin        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  REST API scripts interact with vRA programmatically for automation and reporting.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           REST API Script Patterns           │  │               Useful Utilities              │   │
│   │         GET token → GET deployments          │  │         vracli status --all (health)        │   │
│   │          POST /request catalog item          │  │         kubectl get pods -n prelude         │   │
│   │       DELETE /deployment/{id} cleanup        │  │            pg_dump for DB backup            │   │
│   │       PATCH /blueprint update template       │  │          curl -k for quick API test         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance · ABX FaaS runtime · Orchestrator embedded · Postgres · vIDM                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ABX action        = Serverless function in Python/Node.js/PowerShell executed by vRA event           │
│  Action input      = JSON context object passed to ABX action with resource properties                │
│  Action output     = Key-value pairs returned by ABX to update deployment properties                  │
│  Orchestrator wf   = Visual workflow in Aria Orchestrator; called from vRA via ABX or event           │
│  WinRM             = Windows Remote Management; used by PowerShell ABX to run scripts on VMs          │
│  REST bearer token = JWT from /csp/gateway/am/api/login; header: Authorization: Bearer <tok>          │
│  CMDB update       = ABX POST to ServiceNow or custom CMDB REST API after resource creation           │
│  Deployment ID     = UUID assigned to each vRA deployment; used in API paths for operations           │
│  vracli status     = Appliance CLI health check; useful in shell scripts for monitoring               │
│  pg_dump           = PostgreSQL backup tool; script to dump vRA DB to NFS before upgrades             │
│  kubectl           = Kubernetes CLI on vRA appliance; script to check pod health or restart           │
│  Event subscription= ABX or Orchestrator wf registered to run on specific vRA resource events         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
