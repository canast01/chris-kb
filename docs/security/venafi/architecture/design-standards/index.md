# Venafi — Standards


<div class="kb-summary">
Certificate policy standards enforced through the Venafi policy tree. All certificates issued through Venafi must comply with these standards. Non-compliant requests are rejected at the policy folder level.
</div>
```text
┌──────────────────── Security Venafi Architecture — Architecture Design Standards ─────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Venafi design standards: network isolation, redundancy, sizing, naming conventions      │   │
│   │          Network: dedicated storage VLAN; jumbo frames for iSCSI; dual-fabric for FC          │   │
│   │          Redundancy: dual controllers, multipath I/O, and no single points of failure         │   │
│   │       Monitoring: set capacity and latency alerts; baseline performance after deployment      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Requirements → architecture design → redundancy review → size → deploy                             │
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
│    Physical: Security Venafi Architecture infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Architecture platform overview and core concepts              │
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


---
## Policy Tree Naming Conventions

Policy folders use lowercase-hyphenated names. Certificate objects (leaf nodes) use the FQDN as the object name.

```text
\VED\Policy\
├── internal\
│   ├── production\          e.g., \VED\Policy\internal\production\servers\
│   ├── non-production\
│   └── infrastructure\
│           ├── network\
│           └── vmware\
└── external\
    └── public\
```

Certificate object naming within a folder: `<fqdn>` (e.g., `app01.corp.example.com`). For wildcard certificates: `wildcard.<domain>` (e.g., `wildcard.corp.example.com`). No spaces or special characters in object names.

---

## Key Algorithm Standards

| Usage | Algorithm | Minimum Key Size |
|---|---|---|
| Server / service certificates | RSA | 4096 bits |
| Server / service certificates | ECDSA | P-256 (NIST secp256r1) |
| Code signing | RSA | 4096 bits |
| User / client certificates | RSA | 2048 bits minimum; 4096 preferred |
| CA certificates (Issuing CA) | RSA | 4096 bits |
| CA certificates (Root CA) | RSA | 4096 bits |

RSA-2048 is accepted for user/client certificates only. RSA-2048 server certificates are rejected by Venafi policy for internal production and all external certificates.

SHA-256 is the minimum hash algorithm. SHA-1 certificates are blocked at the policy level.

---

## Validity Period Standards

| Certificate Type | Maximum Validity | Renewal Window |
|---|---|---|
| Internal — Production | 2 years | 30 days before expiry |
| Internal — Non-production | 3 years | 30 days before expiry |
| External / Public-facing | 1 year | 30 days before expiry |
| Internal CA (Issuing) | 10 years | Renew 12 months before expiry |
| Root CA | 20 years | Renew 24 months before expiry |
| Code signing | 1 year | 30 days before expiry |

Note: CA/Browser Forum mandates a maximum 398-day (roughly 13-month) validity for publicly trusted TLS certificates. Venafi policy enforces 365-day maximum for all external certificates to allow headroom.

---

## Subject and SAN Requirements

| Field | Requirement |
|---|---|
| Common Name (CN) | Must be the primary FQDN or service name |
| Subject Alternative Name | Mandatory on all certificates |
| CN must appear in SAN | Yes — CN alone is not accepted by modern browsers/clients |
| IP SANs | Permitted for infrastructure; must be in addition to DNS SAN |
| Email SANs | Only for S/MIME or user certificates |
| Organisation (O) | Required for OV and EV certificates |
| Country (C) | Required for OV and EV certificates |

Venafi policy rejects CSRs where:
- No SAN extension is present
- The CN is not also listed as a DNS SAN
- The SAN contains an internal hostname (`*.local`, `*.internal`) in an external policy folder

---

## Wildcard Certificate Policy

| Scope | Policy |
|---|---|
| Internal production | Permitted with documented justification |
| Internal non-production | Permitted |
| External / public-facing | Restricted — explicit approval required |
| External wildcard for `*.com` TLD | Prohibited |

Wildcard approval process (external):
1. Requestor submits a certificate request with business justification.
2. Security team reviews and approves or rejects within 5 business days.
3. Approved wildcards are subject to annual review.
4. Approved wildcards must be onboarded to CyberArk for private key protection.

---

## Certificate Request Workflow

### Certificate Request Decision Flow

```mermaid
flowchart TD
    csrSubmit["Requestor submits CSR\n(UI / vcert / REST API)"]
    csrSubmit --> folderPolicy{"Venafi policy\nvalidation"}
    folderPolicy -->|"key size below minimum\nSHA-1 / no SAN"| policyFail["Reject — policy violation\nMessage returned to requestor"]
    folderPolicy -->|"internal production folder"| autoIssue{"Auto-issue\nenabled?"}
    folderPolicy -->|"external public folder"| manualApproval["Enter Approval Queue"]
    autoIssue -->|"yes"| caConnector["Submit to CA connector\n(ADCS / DigiCert)"]
    autoIssue -->|"no"| manualApproval
    manualApproval --> secReview{"Security team\nreview"}
    secReview -->|"approve"| caConnector
    secReview -->|"reject"| policyFail
    caConnector --> caIssues["CA issues certificate"]
    caIssues --> tppStores["Venafi stores + notifies requestor"]
```

### Internal Production (Auto-Issue)

```text
Requestor submits CSR via Venafi UI or API
         |
         v
Venafi validates against folder policy
  (key size, hash, SAN, validity)
         |
    Pass: auto-submit to ADCS
    Fail: reject with policy violation message
         |
         v
ADCS issues certificate
         |
         v
Venafi stores certificate, notifies requestor
```

### External Public (Manual Approval)

```text
Requestor submits CSR via Venafi UI or API
         |
         v
Venafi validates against folder policy
         |
         v
Certificate request enters Approval Queue
         |
         v
Security team reviews and approves/rejects
         |
    Approved: Venafi submits to DigiCert connector
    Rejected: requestor notified with reason
         |
         v
DigiCert performs DV/OV validation and issues
         |
         v
Venafi stores certificate, notifies requestor
```

---

## Private Key Handling

| Scenario | Standard |
|---|---|
| Key generated by requestor | Private key stays on origin host; only CSR sent to Venafi |
| Key generated by Venafi | Venafi generates key, stores encrypted copy; key exported once to requestor |
| Key export from Venafi | Requires `Safe` permission level in Venafi RBAC; logged as audit event |
| Production server keys | Never exported or stored outside of the origin host and CyberArk (if applicable) |

Keys for high-value services (CA certificates, wildcard certificates, code signing) must be stored in an HSM or managed within CyberArk with controlled retrieval.

---

## Policy Configuration

## Purpose

Use this page for practical Venafi Policy notes, checks, troubleshooting, commands, change notes, and field references.

## Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful commands

Add tested commands here.

## Known issues

Add known issues here as they come up.
