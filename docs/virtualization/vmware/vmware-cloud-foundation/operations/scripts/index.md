# VCF Operations — Scripts

```text
VCF API Automation — Data Flow
┌─────────────────────────────────────────────────────┐
│  Automation Script / Pipeline                       │
│  (Python / Bash / PowerShell)                       │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS POST /v1/tokens
                       ▼
┌─────────────────────────────────────────────────────┐
│  SDDC Manager REST API                              │
│  https://<sddc-mgr>/v1                              │
│                                                     │
│  GET /v1/domains      ◄── list workload domains     │
│  GET /v1/clusters     ◄── list all clusters         │
│  GET /v1/hosts        ◄── list managed hosts        │
│  POST /v1/system/     ◄── trigger health check      │
│       health-summary                                │
│  PATCH /v1/credentials ◄── rotate credentials       │
└──────────────────────┬──────────────────────────────┘
                       │ returns JSON
                       ▼
┌─────────────────────────────────────────────────────┐
│  Script Output / Integration                        │
│  → stdout / CSV / JSON                              │
│  → monitoring platform (HTTP POST)                  │
│  → ITSM ticketing system                            │
│  → CMDB asset discovery                             │
└─────────────────────────────────────────────────────┘
```
┌──────────────────────────── VMware Cloud Foundation — Operational Scripts ────────────────────────────┐
│                                                                                                       │
│  PowerVCF scripts automate VCF operations: domain inventory, upgrade status,                          │
│  credential audit, certificate expiry check, and health report generation.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Inventory Scripts               │  │            Health & Cert Scripts            │   │
│   │          Get-VCFDomain | Export-Csv          │  │           Request-VCFToken (auth)           │   │
│   │           Get-VCFHost (all hosts)            │  │         Get-VCFCertificate (expiry)         │   │
│   │        Get-VCFCluster (all clusters)         │  │       VMware.CloudFoundation.Reporting      │   │
│   │          Get-VCFCredential (audit)           │  │            Invoke-VcfHealthReport           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  PowerVCF scripts connect to SDDC Manager REST API; read-only ops need no approval.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Scripts                │  │             Automation Examples             │   │
│   │         Get-VCFBundle (list bundles)         │  │            New-VCFDomain (create)           │   │
│   │            Start-VCFBundleUpload             │  │           Add-VCFHost (commission)          │   │
│   │          Start-VCFUpgrade (trigger)          │  │          Set-VCFCredential (rotate)         │   │
│   │          Get-VCFTask (status poll)           │  │          Watch upgrade via task ID          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Scripts run from management jump host; connect to SDDC Manager on port 443;                          │
│  VMware.CloudFoundation.Reporting module needs PowerCLI + PowerVCF.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerVCF       = PowerShell module for SDDC Manager automation                                       │
│  Request-VCFToken= authenticate and store bearer token for session                                    │
│  Get-VCFBundle  = list available upgrade bundles in depot/local                                       │
│  Start-VCFUpgrade= trigger upgrade for a domain or component                                          │
│  Get-VCFTask   = poll async task status by task ID                                                    │
│  Invoke-VcfHealthReport= generates HTML health report for all domains                                 │
│  Get-VCFCertificate= certificate expiry report for all components                                     │
│  New-VCFDomain = automate workload domain creation via API                                            │
│  Add-VCFHost   = commission new host to SDDC Manager                                                  │
│  Set-VCFCredential= trigger credential rotation for component                                         │
│  Reporting module= VMware.CloudFoundation.Reporting on PowerShell Gallery                             │
│  Task ID       = async operation ID; poll with Get-VCFTask until complete                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## Trigger SoS Health Check and Poll Result (Bash)

```bash
#!/usr/bin/env bash
SDDC=$1; USER=$2; PASS=$3
# Trigger health check task
TASK=$(curl -sk -u "$USER:$PASS" -X POST \
  "https://$SDDC/v1/system/health-summary" | jq -r '.id')
echo "SoS task ID: $TASK"
# Poll until complete
while true; do
  STATUS=$(curl -sk -u "$USER:$PASS" \
    "https://$SDDC/v1/tasks/$TASK" | jq -r '.status')
  echo "  Status: $STATUS"
  [[ "$STATUS" == "Successful" || "$STATUS" == "Failed" ]] && break
  sleep 10
done
```
