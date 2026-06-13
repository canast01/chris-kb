---
tags:
  - operations
  - security
---
# Venafi — Scripts


<div class="kb-summary">
Automation scripts for Venafi cover certificate expiry reporting, automated renewal via VCert, discovery scan triggering, policy compliance reporting, and ADCS template alignment checking.

*Applies to: Venafi TLS Protect*
</div>
```text
┌───────────────────────── Security Venafi Operations — Scripts and Automation ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Venafi scripts: automation for reporting, health monitoring, and provisioning         │   │
│   │         REST API available for all operations; PowerShell and Python modules supported        │   │
│   │          Scripts must run from dedicated service accounts with least-privilege roles          │   │
│   │        Store credentials in vault; rotate service account passwords on defined schedule       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Script → authenticate REST → execute operation → verify → log result                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Venafi Operations infrastructure · management network · monitoring              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Operations platform overview and core concepts                │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
