# Public Key Infrastructure (PKI)

<div class="kb-summary">
Public Key Infrastructure (PKI) reference covering PKI Architecture (Typical Enterprise), TLS Handshake Flow, Certificate Validation Chain, ADCS Health Checks, CRL and OCSP Monitoring and 5 more sections.
</div>
```text
┌──────────────────────────────────────────── Security Pki ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Pki: Security Pki platform                                  │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                          Management: Security Pki management console                          │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│    Physical: Security Pki infrastructure · management network · monitoring                            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Pki                = Security Pki platform overview and core concepts                              │
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

```text
┌──────────────────────────── PKI / ADCS — CA Hierarchy Deployment Sequence ────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────                │
│  2 × Windows Server 2022 VMs: Root CA (isolated) + Issuing CA (domain-joined)                         │
│  Root CA: static IP for initial config only — disconnect from network after install                   │
│  Issuing CA: domain-joined, management VLAN access from all certificate consumers                     │
│  Plan: hierarchy name, CDP/AIA HTTP URLs, key algorithm (RSA-4096 root, RSA-2048 issuing)             │
│  Vault: CA admin creds, DSRM passwords, private key backup location before any install                │
│                                                                                                       │
│                                        │  build Root CA offline                                       │
│                                        ▼                                                              │
│  Step 2 · Root CA — Offline, Air-Gapped                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────                │
│  Install AD CS: StandaloneRootCA  ·  RSA-4096  ·  SHA-256  ·  20-year validity                        │
│  Set CDP/AIA extensions to point to Issuing CA HTTP publication path (not self)                       │
│  Configure CRL: 1-year base + 6-month delta  ·  certutil -CRL to publish immediately                  │
│  Export Root CA cert + CRL to secure media (USB) for import on Issuing CA                             │
│  Snapshot VM; store private key backup in offline vault; disconnect from all networks                 │
│                                                                                                       │
│                                        │  deploy Issuing CA online                                    │
│                                        ▼                                                              │
│  Step 3 · Issuing CA — Enterprise ADCS                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────                │
│  Install AD CS: EnterpriseSubordinateCA  ·  domain-joined  ·  RSA-2048  ·  5-year validity            │
│  Submit CSR to Root CA (offline): certutil -submit  ·  sign  ·  import response                       │
│  Publish Root CA cert to AD NTAuth store: certutil -dspublish -f RootCA.cer RootCA                    │
│  Verify chain: certutil -urlfetch -verify IssuingCA.cer  ·  confirm AIA + CDP resolve                 │
│  Check: CA service running; Event ID 26 (CA started) in Application event log                         │
│                                                                                                       │
│                                        │  configure CRL / OCSP                                        │
│                                        ▼                                                              │
│  Step 4 · CRL and OCSP Infrastructure                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────                │
│  Publish CRL to IIS: http://pki.<domain>/CRL/ — accessible to all cert consumers                      │
│  Install Online Responder: Add-WindowsFeature ADCS-Online-Cert  ·  open port 80                       │
│  Configure OCSP Signing template: grant auto-enroll to CA service account                             │
│  Set revocation provider on Issuing CA to point at its own CRL path                                   │
│  Verify: certutil -URL <AIA-URL>  ·  alert if CRL nextUpdate < 50% lifetime remaining                 │
│                                                                                                       │
│                                        │  create certificate templates                                │
│                                        ▼                                                              │
│  Step 5 · Certificate Templates                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────                │
│  Duplicate built-in templates: Web Server → Server Auth; User → Client Auth                           │
│  Set: key usage, EKU, 1–2 yr validity, RSA-2048 min, subject from AD or CSR                           │
│  Grant Enroll + Auto-Enroll: Domain Computers (server certs), Domain Users (user certs)               │
│  Publish templates: CA snap-in → Certificate Templates → New → Template to Issue                      │
│  Test: manual request via http://IssuingCA/certsrv — confirm download and chain                       │
│                                                                                                       │
│                                        │  enable auto-enrollment and validate                         │
│                                        ▼                                                              │
│  Step 6 · Auto-Enrollment and Validation                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────                │
│  GPO: Cert Services Client — Auto-Enrollment → Enabled + renew expired and pending                    │
│  Link GPO to Domain Computers OU and Domain Users OU  ·  gpupdate /force to test                      │
│  Verify: certmgr.msc → Personal → Certificates — auto-enrolled cert present                           │
│  Full chain validation: certutil -verify -urlfetch cert.cer on multiple consumers                     │
│  Set expiry alerting: certutil -view -restrict "NotAfter<NOW+60D" as daily baseline                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
Root CA (offline, air-gapped)
  └── Intermediate / Issuing CA (online, ADCS)
        ├── Server certificates (internal services)
        ├── User certificates (smart card / email encryption)
        └── Code signing certificates
```

```text
  Client                                          Server
    │                                               │
    │── ClientHello ───────────────────────────────►│
    │   (TLS version, cipher suites, client random) │
    │                                               │
    │◄── ServerHello ──────────────────────────────│
    │    (chosen cipher, server random)             │
    │◄── Certificate ──────────────────────────────│
    │    (server cert + chain)                      │
    │◄── ServerHelloDone ──────────────────────────│
    │                                               │
    │   [Client validates cert chain]               │
    │   [Checks: not expired, trusted CA, CN/SAN]   │
    │   [Checks: CRL / OCSP — not revoked]          │
    │                                               │
    │── ClientKeyExchange ────────────────────────►│
    │   (pre-master secret, enc with server pubkey) │
    │── ChangeCipherSpec ─────────────────────────►│
    │── Finished (enc) ───────────────────────────►│
    │                                               │
    │◄── ChangeCipherSpec ─────────────────────────│
    │◄── Finished (enc) ───────────────────────────│
    │                                               │
    │          [TLS session established]            │
    │◄──────── Application Data (encrypted) ───────►│
```

```text
  Browser / Client
       │  verify signature
       ▼
  Issuing CA cert  ──────── OCSP / CRL check ──► CA's OCSP Responder
       │  verify signature                             (revoked? yes/no)
       ▼
  Intermediate CA cert
       │  verify signature
       ▼
  Root CA cert  ──── in OS / browser trust store? ──► Trust anchor
       │
       └── [trusted]  →  chain valid
           [not found] →  UNKNOWN_CA / PKIX error
```

<div class="kb-grid">
  <a class="kb-card" href="deploy/">
    <div class="kb-card-icon">🚀</div>
    <div class="kb-card-title">Deploy</div>
    <div class="kb-card-desc">CA hierarchy deployment: Root CA, Issuing CA, CRL/OCSP, and auto-enrollment</div>
  </a>
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Certificate issuance, renewal, revocation, ADCS health checks</div>
  </a>
</div>

## ADCS Health Checks

```powershell
# Confirm CA service is running
Get-Service -Name CertSvc

# List CA configuration
certutil -getconfig

# View pending certificate requests
certutil -view -restrict "disposition=9" -out "requestID,requesterName,CommonName,NotAfter"

# Check CRL validity
certutil -URL <crl-distribution-point-url>

# Verify CRL freshness and OCSP
certutil -verifyCRL C:\Windows\System32\certsrv\CertEnroll\<ca>.crl

# View issued certificates (last 100)
certutil -view -restrict "Disposition=20" -out "RequestID,CommonName,NotBefore,NotAfter,Requester" | head -100
```

## CRL and OCSP Monitoring

```bash
# Linux — verify OCSP responder
openssl ocsp \
  -issuer issuing-ca.pem \
  -cert server.pem \
  -url http://<ocsp-responder>/ocsp \
  -resp_text

# Verify CRL freshness from a PEM cert
openssl crl -in <crl-file>.crl -noout -nextupdate
# nextUpdate must be in the future — if expired, CRL is stale
```

## Certificate Inventory and Expiry Check

```bash
# Check expiry for a certificate
openssl x509 -in cert.pem -noout -dates -subject -issuer

# Scan a live service
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | \
  openssl x509 -noout -dates -subject

# Bulk check from a list of hosts
while read host; do
  expiry=$(echo | openssl s_client -connect "${host}:443" -servername "$host" 2>/dev/null | \
    openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$host: $expiry"
done < hosts.txt
```

## Certificate Lifecycle Events

| Event | Action Required |
|---|---|
| Certificate expiring in 60 days | Initiate renewal |
| Certificate expiring in 30 days | Escalate if not renewed |
| Certificate expiring in 7 days | Emergency renewal; notify service owners |
| CA certificate expiring in 6 months | Plan CA renewal (impacts all issued certs) |
| Key compromise suspected | Revoke immediately; issue replacement |

## Certificate Revocation

```powershell
# Revoke a certificate in ADCS
# Get request ID from certutil -view output
certutil -revoke <request-id> 3   # 3 = keyCompromise

# Publish new CRL immediately after revocation
certutil -CRL
```

## Backup and DR for ADCS

```powershell
# Backup CA database and private key
certutil -backup C:\CA-Backup

# Or full backup including config
certutil -backupdb C:\CA-Backup

# Verify backup
certutil -verifystore -enterprise NTAuth
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| CRL too large / slow to download | Number of revoked certs | Enable Delta CRL; increase CRL publication frequency |
| OCSP not responding | OCSP responder service | Restart Online Responder service; check CRL is current |
| Auto-enrollment failing | Group Policy / template | Check "Certificate Services Client - Auto-Enrollment" GPO; verify user has Enroll permission on template |
| CA certificate expired | CA cert validity | Renew CA cert; redistribute trust to all clients via GPO |
