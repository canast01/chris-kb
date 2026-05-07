# Public Key Infrastructure (PKI)
## PKI Architecture (Typical Enterprise)

```
Root CA (offline, air-gapped)
  └── Intermediate / Issuing CA (online, ADCS)
        ├── Server certificates (internal services)
        ├── User certificates (smart card / email encryption)
        └── Code signing certificates
```

## TLS Handshake Flow

```
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

## Certificate Validation Chain

```
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
