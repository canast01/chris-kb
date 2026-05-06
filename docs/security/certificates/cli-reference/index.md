# Certificates CLI Reference

Windows certificate operations use `certutil` for verification, revocation, and store management, plus `certmgr.msc` for the GUI store. Linux operations rely on the `openssl` CLI for inspection, verification, and TLS connectivity testing. PowerShell provides `Get-ChildItem Cert:\` for browsing the Windows certificate store and `Test-Certificate` for chain validation.

**Windows (`certutil`):**

```cmd
# Verify a certificate file
certutil -verify cert.cer

# Display certificate details
certutil -dump cert.cer

# Revoke a certificate (CA admin)
certutil -revoke <SerialNumber> <ReasonCode>

# Check CRL freshness
certutil -urlcache crl

# Verify chain against a CA
certutil -verify -urlfetch cert.cer
```

**Linux (`openssl`):**

```bash
# Test TLS connectivity and view server certificate
openssl s_client -connect host:443 -showcerts

# Display certificate details from a PEM file
openssl x509 -in cert.pem -noout -text

# Verify certificate against a CA chain
openssl verify -CAfile chain.pem cert.pem

# Check certificate expiry date
openssl x509 -in cert.pem -noout -enddate

# Generate a CSR
openssl req -new -newkey rsa:4096 -keyout key.pem -out csr.pem -subj "/CN=server.example.com"
```

**PowerShell:**

```powershell
# Browse the Windows certificate store
Get-ChildItem Cert:\LocalMachine\My

# Find certificates expiring within 30 days
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.NotAfter -lt (Get-Date).AddDays(30) }

# Validate a certificate chain
Test-Certificate -Cert (Get-Item Cert:\LocalMachine\My\<Thumbprint>)
```
