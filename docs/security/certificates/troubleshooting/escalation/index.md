---
tags:
  - security
  - troubleshooting
---
# Certificates — Escalation


<div class="kb-summary">
Procedures for raising support cases with Microsoft ADCS, commercial CAs (DigiCert, Entrust), and Let's Encrypt. Pre-collect diagnostics before opening any case to reduce round-trip delays.
</div>
```text
┌───────────────────────── Security Certificates Troubleshooting — Escalation ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Certificates escalation: severity triage, vendor support contact, and required artifacts   │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
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
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
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


---
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Channel Summary

| Vendor | Support Channel | SLA Notes |
|---|---|---|
| Microsoft ADCS | support.microsoft.com | Premier / Unified Support required for Sev A/B |
| DigiCert | digicert.com/support | 24/7 for critical; portal + phone |
| Entrust | entrust.com/support | Portal; phone for P1 |
| Let's Encrypt | community.letsencrypt.org | Community only; no paid support |
| Venafi | support.venafi.com | See Venafi vendor-support page |

---

## Microsoft ADCS

### Pre-Collection Checklist

Before opening a Microsoft support case, collect:

```powershell
# 1. Export CA event logs
wevtutil epl Application C:\Temp\Application.evtx
wevtutil epl System C:\Temp\System.evtx

# 2. Test CA RPC connectivity
certutil -ping

# 3. Check CRL freshness
certutil -getreg CA\CRLNextPublish
certutil -CRL

# 4. Verify CA service health
sc query certsvc
certutil -cainfo

# 5. Export CA configuration for review
certutil -dump > C:\Temp\ca-dump.txt
certutil -getreg CA > C:\Temp\ca-registry.txt

# 6. Collect certificate database statistics
certutil -view -restrict "Disposition=20" -out "RequestID,CommonName,NotAfter" > C:\Temp\issued-certs.txt
```

### Common ADCS Issues

| Symptom | First Check | Command |
|---|---|---|
| Auto-enrollment not working | GPO applied, CA reachable, template permissions | `certutil -pulse; gpresult /r` |
| CRL download failing | HTTP/LDAP CDP accessibility | `certutil -URL <cdp_url>` |
| CA service fails to start | CA cert or CRL expired | Check `certsvc` event log, `certutil -verify` |
| Certificate request pending | Template requires CA Manager approval | `certsrv.msc` → Pending Requests |

---

## DigiCert

### Pre-Collection Checklist

- Certificate **Order Number** (from DigiCert portal)
- Certificate **Serial Number** (`certutil -dump <cert.cer>` or from browser)
- Full **error message and timestamp**
- Domain validation method used (DNS, HTTP, email)
- For ACME: ACME client version, configuration, and challenge log output

### Emergency Certificate Procedures

DigiCert offers a **Certificate Replacement** (rekey) at no charge within the validity period:

1. Log in to DigiCert portal → **Orders** → locate the certificate.
2. Select **Reissue Certificate** and provide a new CSR.
3. For emergency same-day issuance, call DigiCert Priority Support.

Revocation (when key compromise suspected):

1. Log in to DigiCert portal → **Orders** → **Revoke Certificate**.
2. Provide reason code (Key Compromise, Affiliation Changed, Superseded, etc.).
3. DigiCert revokes within 24 hours for standard reasons, 24 hours maximum for key compromise per BR requirements.

---

## Entrust

### Pre-Collection Checklist

- Entrust **Certificate ID** (from Entrust portal)
- Issuance **date and time**
- Full error message from the requesting application
- Whether the issue affects issuance, renewal, or validation

### Emergency Procedures

For P1 certificate outages (production service down):

1. Open a case via entrust.com/support.
2. Call the Entrust support phone line and reference the case number.
3. For revocation due to key compromise, Entrust complies with CA/Browser Forum 24-hour revocation requirement.

---

## Let's Encrypt

Let's Encrypt provides no paid support. All issues are handled via the community forum at **community.letsencrypt.org**.

### ACME Troubleshooting

```bash
# Test ACME challenge accessibility (HTTP-01)
curl -v http://<domain>/.well-known/acme-challenge/<token>

# Check certificate issuance logs (Certbot)
journalctl -u certbot.service
cat /var/log/letsencrypt/letsencrypt.log

# Force a dry-run to validate ACME flow without issuing
certbot renew --dry-run --cert-name <domain>

# Check current certificate expiry
certbot certificates
```

Common failure causes:
- Port 80 blocked by firewall during HTTP-01 challenge
- DNS propagation delay during DNS-01 challenge
- Rate limit exceeded (5 duplicate certificates per week; 50 per domain per week)

Check current rate limit status: **crt.sh** — search for your domain to see recently issued certificates.

---

## Escalation Path by Vendor

```mermaid
flowchart TD
    issue["Certificate / CA issue requiring vendor support"]
    issue --> vendor{"Which CA\n/ vendor?"}
    vendor -->|"ADCS"| msSupport["Microsoft — support.microsoft.com\n(Premier / Unified Support for Sev A/B)\nPre-collect: event logs, certutil -ping, ca-dump.txt"]
    vendor -->|"DigiCert"| dgSupport["DigiCert — digicert.com/support\n24/7 for critical; portal + phone\nPre-collect: Order Number, Serial, domain validation method"]
    vendor -->|"Entrust"| enSupport["Entrust — entrust.com/support\nPortal; phone for P1\nPre-collect: Certificate ID, issuance date, error"]
    vendor -->|"Let's Encrypt"| leSupport["Let's Encrypt — community.letsencrypt.org\nCommunity only — no paid support\nRun: certbot renew --dry-run first"]
    vendor -->|"Venafi"| venafiSupport["Venafi — see Venafi vendor-support page"]

    msSupport --> preCollect["Run pre-collection checklist\nbefore opening case"]
    dgSupport --> preCollect
    enSupport --> preCollect
```

---

## Certificate Emergency Response

### Suspected Key Compromise

1. **Immediately revoke** the certificate via the issuing CA or vendor portal.
2. Generate a new key pair and CSR on a clean, verified host.
3. Re-issue the certificate with the new key.
4. Replace the certificate in all affected services.
5. Audit access logs for the period the key may have been exposed.
6. Document the incident and notify the security team.

### Expired Certificate Response

```powershell
# Find all expired certificates in the machine store
Get-ChildItem Cert:\LocalMachine\My |
  Where-Object { $_.NotAfter -lt (Get-Date) } |
  Select-Object Subject, NotAfter, Thumbprint

# Check which service is using an expired certificate
netsh http show sslcert | Select-String -Pattern "Thumbprint|IP:port"
```

Target resolution time: expired internal certificate — 2 hours. Expired external/public certificate — 1 hour (P1 incident).
