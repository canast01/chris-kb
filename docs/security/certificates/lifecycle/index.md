# Certificates Lifecycle

The certificate lifecycle spans six stages: enrolment, issuance, installation, monitoring, renewal, and revocation. Auto-renewal must be configured wherever possible (Venafi, ACME, cert-manager). Manual processes are a fallback only.

---
## Lifecycle Overview

| Stage | Trigger | Owner | Target SLA |
|---|---|---|---|
| Enrolment | Service provisioning or renewal request | Application / infra team | — |
| Issuance | CA receives valid CSR | CA (automated or manual) | < 1 hour (internal), same day (external) |
| Installation | Certificate issued | Application / infra team | Same day |
| Monitoring | Continuous | Venafi / monitoring team | Alert at 30 days, escalate at 7 days |
| Renewal | 80% of validity elapsed | Automated (Venafi / ACME) | Before expiry |
| Revocation | Compromise, decommission, or policy violation | Certificate owner + CA admin | Immediate for key compromise |

---

## CSR Generation

Always generate the key pair on the target host or in an HSM — never send private keys over the network.

```bash
# Generate a 4096-bit RSA key and CSR (Linux)
openssl req -new -newkey rsa:4096 -nodes \
  -keyout server.key \
  -out server.csr \
  -subj "/CN=app.corp.example.com/O=Example Corp/C=GB"

# Generate with SANs using a config file
cat > san.cnf <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions     = v3_req
prompt             = no

[req_distinguished_name]
CN = app.corp.example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = app.corp.example.com
DNS.2 = app-internal.corp.example.com
IP.1  = 10.10.10.50
EOF

openssl req -new -newkey rsa:4096 -nodes \
  -keyout server.key -out server.csr -config san.cnf
```

```powershell
# Generate CSR on Windows using certreq
# 1. Create request INF
$inf = @"
[NewRequest]
Subject       = "CN=app.corp.example.com, O=Example Corp, C=GB"
KeyAlgorithm  = RSA
KeyLength     = 4096
HashAlgorithm = SHA256
Exportable    = FALSE
MachineKeySet = TRUE

[Extensions]
2.5.29.17 = "{text}dns=app.corp.example.com&dns=app-internal.corp.example.com"
"@
$inf | Out-File "C:\Temp\request.inf" -Encoding ASCII

# 2. Generate CSR
certreq -new "C:\Temp\request.inf" "C:\Temp\request.csr"
```

---

## Certificate Issuance (Internal ADCS)

```powershell
# Submit CSR to internal ADCS CA and retrieve certificate
certreq -submit -attrib "CertificateTemplate:WebServer-Internal" `
  "C:\Temp\request.csr" "C:\Temp\issued.cer"

# If pending (requires manager approval), retrieve after approval
certreq -retrieve <RequestID> "C:\Temp\issued.cer"

# Install the issued certificate
certreq -accept "C:\Temp\issued.cer"
```

---

## Certificate Installation

```bash
# Verify certificate and key match before installation
openssl x509 -noout -modulus -in server.crt | md5sum
openssl rsa  -noout -modulus -in server.key | md5sum
# Output must match

# Combine into PEM bundle (cert + intermediates)
cat server.crt intermediate-ca.crt > bundle.pem

# Verify the full chain
openssl verify -CAfile root-ca.crt -untrusted intermediate-ca.crt server.crt
```

---

## Expiry Monitoring

### Venafi

Venafi TPP monitors all managed certificates automatically. Set email alerts at 30-day and 7-day thresholds in the policy folder settings. See the [Venafi Lifecycle page](../../venafi/lifecycle/index.md) for details.

### Manual Monitoring Scripts

```powershell
# Scan local machine certificate store for certificates expiring within 30 days
$warnDays = 30
Get-ChildItem Cert:\LocalMachine\My |
  Where-Object { $_.NotAfter -lt (Get-Date).AddDays($warnDays) } |
  Select-Object Subject, NotAfter, Thumbprint, @{N="DaysLeft"; E={($_.NotAfter - (Get-Date)).Days}} |
  Sort-Object NotAfter
```

```bash
# Check expiry of a remote TLS certificate
echo | openssl s_client -connect app.corp.example.com:443 -servername app.corp.example.com 2>/dev/null |
  openssl x509 -noout -enddate

# Bulk check a list of hostnames
while IFS= read -r host; do
  expiry=$(echo | openssl s_client -connect "$host:443" -servername "$host" 2>/dev/null |
    openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$host: $expiry"
done < hosts.txt
```

---

## Certificate Renewal

Renewal should be initiated at 80% of the certificate's validity period (e.g., for a 2-year certificate, renew after ~20 months).

```powershell
# Trigger auto-enrollment renewal on a Windows host
certutil -pulse

# Force renewal of a specific certificate (using Venafi API — see Venafi lifecycle page)
# Or: request a new certificate using the same template and replace the binding
```

### Renewing a CA Certificate

CA certificate renewal is a planned event requiring co-ordination with all relying parties:

1. Generate a new key pair and CSR on the CA.
2. Have the parent CA (or Root CA key ceremony) sign the new CA certificate.
3. Publish the new CA certificate to AD (auto-distributes to domain members via GPO):

```powershell
# Publish new Issuing CA certificate to AD
certutil -dspublish -f IssuingCA.cer SubCA
```

4. Update CDP and AIA extensions to reference the new certificate.
5. Update any trust stores that reference the CA certificate explicitly (non-domain systems, network devices, Java keystores).

---

## Certificate Revocation

### Revoke via ADCS

```powershell
# Revoke a certificate by serial number
$serial = "1f2e3d4c5b6a7988"
certutil -revoke $serial 3   # Reason code 3 = Key Compromise

# Publish a new CRL immediately after revocation
certutil -CRL

# Verify the revoked certificate appears in the CRL
certutil -verify -urlfetch <revoked-cert.cer>
```

Reason codes: 0 = Unspecified, 1 = Key Compromise, 2 = CA Compromise, 3 = Affiliation Changed, 4 = Superseded, 5 = Cessation of Operation.

### Emergency Revocation Checklist

- [ ] Revoke certificate via ADCS or vendor portal
- [ ] Publish updated CRL immediately
- [ ] Notify service owner to replace certificate
- [ ] Verify revocation propagated to OCSP responder
- [ ] Audit which services were using the revoked certificate
- [ ] Generate and install replacement certificate
- [ ] Verify replacement is correctly installed and trusted
- [ ] Document incident with timeline and root cause
