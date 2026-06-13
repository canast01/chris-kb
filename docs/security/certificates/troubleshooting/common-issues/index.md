---
tags:
  - security
  - troubleshooting
search:
  boost: 1.5
---
# Certificates — Common Issues


<div class="kb-summary">
Common Issues reference covering Certificate Issue Triage Flow, Common checks, Incident notes, Change notes, Known issues and 2 more sections.
</div>
```text
┌──────────────────────── Security Certificates Troubleshooting — Common Issues ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Certificates common issues: quick-reference for frequently encountered problems        │   │
│   │         Issues: path failures, connectivity errors, capacity alerts, and auth failures        │   │
│   │         For each issue: symptoms, root cause, diagnostic steps, and resolution actions        │   │
│   │           Escalate to vendor support if the issue persists after standard procedures          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify symptom → check logs → diagnose root cause → resolve → verify                             │
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
│    Physical: Security Certificates Troubleshooting infrastructure · management network · monitoring   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Certificates       = Security Certificates Troubleshooting platform overview and core concepts     │
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


## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A{Certificate expired\nor browser error?}
    S --> B{Certificate not\ntrusted / chain error?}
    S --> C{Auto-renewal\nfailed?}
    S --> D{Wrong SAN or CN\non certificate?}
    S --> E{Private key\nmismatch?}
    A -->|Yes| A1{Expired internal\nor external?}
    A1 -->|External| A2[P1 incident: 1-hour SLA\nEmergency renewal via CA]
    A1 -->|Internal| A3[certutil -verify\nRenew via ADCS or ACME]
    A3 --> A4[Expired Certificate Response]
    B -->|Yes| B1[openssl s_client check chain\nAdd intermediate cert to TLS config\nDistribute root CA via GPO]
    B1 --> B2[Certificate Issue Triage Flow]
    C -->|Yes| C1{ACME or\nADCS renewal?}
    C1 -->|ACME| C2[Check DNS/HTTP challenge\nVerify ACME client logs\nConfirm port 80/443 reachable]
    C1 -->|ADCS| C3[certutil -pulse\nCheck CA service and CRL\nVerify template permissions]
    C3 --> C4[Common ADCS Issues]
    D -->|Yes| D1[openssl x509 -text -in cert.pem\nCompare SAN list to hostname\nRequest new cert with correct SANs]
    D1 --> D2[Certificate Issue Triage Flow]
    E -->|Yes| E1[openssl verify cert against key\nIf mismatch: re-issue cert\nor restore correct private key]
    E1 --> E2[Expired Certificate Response]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A4,B2,C4,D2,E2 section
    class A,A1,B,C,C1,D,E decision
    class S start
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Certificate Issue Triage Flow

```mermaid
flowchart TD
    issue["Certificate error reported\n(TLS failure / untrusted / expired)"]
    issue --> checkExpiry{"Is the certificate\nexpired?"}
    checkExpiry -->|"yes"| expiredPath["Emergency renewal\n(P1 if external — 1 hour SLA)"]
    checkExpiry -->|"no"| checkChain{"Chain validation\nfails?"}
    checkChain -->|"yes"| chainFix["Intermediate not sent by server\nAdd intermediate to TLS config\nopenssl verify to confirm"]
    checkChain -->|"no"| checkTrust{"Root CA trusted\nby client?"}
    checkTrust -->|"no"| addRoot["Distribute root CA cert\nvia GPO / system trust store"]
    checkTrust -->|"yes"| checkRevoke{"Certificate\nrevoked?"}
    checkRevoke -->|"yes — CRL / OCSP"| replaceRevoked["Replace with new cert\nIssue on clean host"]
    checkRevoke -->|"no"| checkSAN{"CN / SAN matches\nhostname?"}
    checkSAN -->|"no"| newCert["Request new cert with\ncorrect CN and SANs"]
    checkSAN -->|"yes"| deepDiag["Further diagnostics:\nopenssl s_client full output\ncertutil -verify -urlfetch"]
```

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

## Known issues

Add known issues here as they come up.

## Common ADCS Issues

| Symptom | First Check | Command |
|---|---|---|
| Auto-enrollment not working | GPO applied, CA reachable, template permissions | `certutil -pulse; gpresult /r` |
| CRL download failing | HTTP/LDAP CDP accessibility | `certutil -URL <cdp_url>` |
| CA service fails to start | CA cert or CRL expired | Check `certsvc` event log, `certutil -verify` |
| Certificate request pending | Template requires CA Manager approval | `certsrv.msc` → Pending Requests |

## Expired Certificate Response

```powershell
# Find all expired certificates in the machine store
Get-ChildItem Cert:\LocalMachine\My |
  Where-Object { $_.NotAfter -lt (Get-Date) } |
  Select-Object Subject, NotAfter, Thumbprint

# Check which service is using an expired certificate
netsh http show sslcert | Select-String -Pattern "Thumbprint|IP:port"
```

Target resolution time: expired internal certificate — 2 hours. Expired external/public certificate — 1 hour (P1 incident).

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
