# Venafi Architecture

Venafi Trust Protection Platform (TPP) is the enterprise certificate lifecycle management system. It enforces certificate policy, integrates with multiple CA backends, automates renewal, and provides visibility across all managed certificates. The SaaS equivalent is Venafi as a Service (VaaS / TLS Protect Cloud).

---
## Component Overview

| Component | Role | Deployment |
|---|---|---|
| Policy Server | Lifecycle management, CA integration, policy enforcement | On-prem VM (primary + secondary) |
| Edge Proxy | Certificate discovery across segmented networks | Lightweight on-prem agent |
| Log Server | Audit event aggregation and SIEM forwarding | On-prem VM or syslog target |
| VaaS / TLS Protect Cloud | SaaS alternative to TPP | Hosted by Venafi |
| CA Connectors | Integration adapters for ADCS, DigiCert, Entrust | Configured on Policy Server |
| Venafi SDK / REST API | Automation and integration interface | Consumed by CI/CD and scripts |

---


## Trust Protection Platform Topology

```mermaid
graph TB
  TPP["Venafi Trust Protection Platform"]
  TPP --> DISC["Discovery Engine\n(network scan / agent)"]
  TPP --> CA1["CA Connector — ADCS"]
  TPP --> CA2["CA Connector — DigiCert / Entrust"]
  TPP --> AUTO["Automation\n(renewal / provisioning)"]
  DISC -->|"found certs"| TPP
  ADMIN(["Security Admin"]) -->|"portal"| TPP
  TPP -->|"SIEM / SNMP"| SIEM(["SIEM / Monitoring"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class TPP,DISC ctrl
  class CA1,CA2,AUTO mgmt
  class ADMIN,SIEM host
```

## Policy Tree Structure

The Venafi policy tree (`\VED\Policy\`) organises certificates into folders that apply inheritance-based policy. Certificates inherit policy settings from parent folders unless explicitly overridden.

```
\VED\Policy\
├── Internal\
│   ├── Production\
│   │   ├── Servers\
│   │   └── Services\
│   ├── Non-Production\
│   │   ├── Dev\
│   │   └── Test\
│   └── Infrastructure\
│       ├── Network\
│       └── VMware\
└── External\
    ├── Public\
    └── Partners\
```

Policy folder settings (configured per folder):
- CA template / connector to use for issuance
- Validity period and renewal window
- Key algorithm and minimum key size
- Required SANs and prohibited wildcard usage
- Approval workflow (auto-issue vs. manual approval)
- Notification contacts for expiry alerts

---

## CA Integration Hierarchy

```mermaid
graph TD
    tpp["Venafi Trust Protection Platform"]
    tpp --> adcs["CA Connector: ADCS\n(Microsoft Active Directory CS)"]
    tpp --> digicert["CA Connector: DigiCert\n(public OV / EV / DV)"]
    tpp --> entrust["CA Connector: Entrust\n(public / OV)"]
    tpp --> acme["ACME Connector\n(Let's Encrypt)"]
    tpp --> vault["HashiCorp Vault PKI\n(short-lived / service mesh)"]

    adcs -->|"DCOM / CES"| adcsServer["ADCS Issuing CA Server"]
    digicert -->|"REST API"| digicertCloud["DigiCert API Cloud"]
    entrust -->|"REST API"| entrustCloud["Entrust API Cloud"]
    acme -->|"ACME RFC 8555"| leCloud["Let's Encrypt"]
    vault -->|"Vault REST API"| vaultPKI["Vault PKI Engine"]
```

---

## CA Connectors

Venafi integrates with multiple CA backends. Each connector is configured once at the Policy Server level and referenced by policy folders.

| CA Type | Connector | Notes |
|---|---|---|
| Microsoft ADCS | ADCS connector (built-in) | Requires CES/CEP or direct RPC access to CA |
| DigiCert | DigiCert connector | Requires DigiCert API key; supports OV/EV/DV |
| Entrust | Entrust connector | Requires Entrust API key and client credentials |
| Let's Encrypt | ACME connector | HTTP-01 or DNS-01 challenge; requires accessible validation endpoint |
| Internal standalone CA | Generic PKCS#10 / SCEP | For CAs without a native connector |

```powershell
# List configured CA connectors via Venafi REST API
$headers = @{ "X-Venafi-API-Key" = $apiKey }
Invoke-RestMethod -Uri "https://venafi.corp.example.com/vedsdk/Certificates/CheckPolicy" `
  -Headers $headers -Method Post -ContentType "application/json" `
  -Body '{"PolicyDN":"\\VED\\Policy\\Internal\\Production"}'
```

---

## Certificate Lifecycle Flow

```mermaid
flowchart TD
    request["Certificate Request\n(UI / API / vcert CLI / CI-CD)"]
    request --> policyCheck{"Policy engine\nvalidation"}
    policyCheck -->|"SAN missing / key too small\npolicy violation"| reject["Reject with\nviolation message"]
    policyCheck -->|"internal auto-issue"| submitCA["Submit CSR to\nconfigured CA connector"]
    policyCheck -->|"external / approval required"| approvalQ["Enter Approval Queue\n(Security team review)"]
    approvalQ -->|"approved"| submitCA
    approvalQ -->|"rejected"| reject
    submitCA --> caIssue["CA issues certificate"]
    caIssue --> tppStore["Venafi stores certificate\n+ notifies owner"]
    tppStore --> monitor["Expiry monitoring begins\n(30-day alert window)"]
    monitor -->|"within renewal window"| autoRenew["Auto-renew triggered\n(new CSR generated)"]
    autoRenew --> submitCA
    monitor -->|"key compromise / decommission"| revoke["Revoke via CA connector\n+ update CRL / OCSP"]
```

---

## High Availability

Venafi TPP is deployed as a primary + secondary pair sharing a common Microsoft SQL Server backend.

```
[Client / API consumer]
         |
         | HTTPS (443)
         v
[Load Balancer / VIP]
    /           \
[TPP Primary]  [TPP Secondary]
         \           /
          [SQL Server]
          (Always On AG preferred)
```

- Both nodes are active; the load balancer distributes requests.
- SQL Server is the single source of truth; both nodes are stateless with respect to certificate data.
- Failover is transparent — if one node fails, the load balancer routes all traffic to the remaining node.

```powershell
# Check TPP service health on both nodes (run on each node)
Get-Service -Name "Venafi*" | Select-Object Name, Status

# Verify SQL connectivity from TPP node
Test-NetConnection -ComputerName sql01.corp.example.com -Port 1433
```

---

## Network Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| TPP Policy Server | ADCS (CES endpoint) | TCP 443 | Certificate enrolment |
| TPP Policy Server | DigiCert / Entrust APIs | TCP 443 | External CA issuance |
| TPP Policy Server | SQL Server | TCP 1433 | Database backend |
| Edge Proxy | TPP Policy Server | TCP 443 | Proxy registration and data sync |
| Admin / CI-CD | TPP Policy Server | TCP 443 | REST API and web UI |
| TPP Log Server | Splunk / SIEM | TCP 514 / 6514 | Syslog event forwarding |

---

## REST API Access

Venafi TPP exposes a REST API at `https://<tpp-fqdn>/vedsdk/`.

```powershell
# Authenticate and get API key
$body = @{ Username = "svc-venafi-api"; Password = "password" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "https://venafi.corp.example.com/vedauth/authorize" `
  -Method Post -ContentType "application/json" -Body $body
$apiKey = $response.APIKey

# Request a certificate
$certRequest = @{
    PolicyDN = "\\VED\\Policy\\Internal\\Production\\Servers"
    Subject  = "app01.corp.example.com"
    SubjectAltNames = @(
        @{ TypedName = "dns:app01.corp.example.com" },
        @{ TypedName = "dns:app01-internal.corp.example.com" }
    )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "https://venafi.corp.example.com/vedsdk/Certificates/Request" `
  -Headers @{ "X-Venafi-API-Key" = $apiKey } `
  -Method Post -ContentType "application/json" -Body $certRequest
```
