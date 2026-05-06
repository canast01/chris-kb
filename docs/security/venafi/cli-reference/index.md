# Venafi CLI Reference

The VCert CLI is the primary command-line tool for interacting with Venafi TPP and VaaS. Key commands cover credential management, certificate enrolment, renewal, and revocation. The Venafi REST API (VEDSK) provides the same capabilities for automation and integration workflows.

PowerShell module commands (`VenafiPS`) are available for Windows-based automation and wrap both the REST API and VCert functionality.

**VCert CLI:**

```bash
# Obtain API credentials
vcert getcredential --tpp-url https://tpp.example.com --username admin

# Enrol a new certificate
vcert enroll --tpp-url https://tpp.example.com \
  --token <token> \
  --zone "\VED\Policy\Internal\Production" \
  --cn server.example.com \
  --san-dns server.example.com

# Renew an existing certificate
vcert renew --tpp-url https://tpp.example.com \
  --token <token> \
  --id "\VED\Policy\Internal\Production\server.example.com"

# Revoke a certificate
vcert revoke --tpp-url https://tpp.example.com \
  --token <token> \
  --id "\VED\Policy\Internal\Production\server.example.com"
```

**Venafi REST API (VEDSDK):**

```bash
# List certificates
GET /vedsdk/certificates?Limit=100&Offset=0

# Request a new certificate
POST /vedsdk/certificates/request
Content-Type: application/json
{ "PolicyDN": "\\VED\\Policy\\Internal\\Production", "Subject": "CN=server.example.com" }
```

**PowerShell (VenafiPS):**

```powershell
Import-Module VenafiPS
New-VenafiSession -Server 'tpp.example.com' -Credential $cred
Find-VcCertificate -ExpireBefore (Get-Date).AddDays(30)
Invoke-VcCertificateAction -CertificateId $id -Renew
```
