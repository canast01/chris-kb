---
tags:
  - operations
  - security
---
# Venafi CLI Reference

<div class="kb-summary">
Venafi is managed via the `vcert` CLI (Trust Protection Platform and Venafi as a Service), the TPP REST API, and PowerShell cmdlets. The `vcert` CLI is the primary tool for certificate request, renewal, and retrieval automation.

*Applies to: Venafi TLS Protect*
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## vcert CLI Workflow

```d2
direction: right

auth: "vcert getcred\n(authenticate to TPP or VaaS" {shape: rectangle}
action: "Operation" {shape: rectangle}
enroll: "vcert enroll\n--zone policy-folder --cn hostname" {shape: rectangle}
renew: "vcert renew\n--thumbprint or --id cert-DN" {shape: rectangle}
retrieve: "vcert retrieve\n--id cert-DN --format pkcs12" {shape: rectangle}
certFiles: "cert.pem + key.pem\n+ chain.pem on disk" {shape: rectangle}
deploy: "Deploy to target service\n(nginx / IIS / F5 / etc." {shape: rectangle}

auth -> action
action -> enroll
action -> renew
action -> retrieve
enroll -> certFiles
renew -> certFiles
retrieve -> certFiles
certFiles -> deploy
```

---

## vcert CLI — Authentication

```bash
# Authenticate to Venafi as a Service (VaaS)
vcert getcred --platform vaas --apiKey <api_key>

# Authenticate to Trust Protection Platform (TPP)
vcert getcred --platform tpp --url https://<tpp_fqdn>/vedsdk   --username <user> --password <pass>

# Verify credentials
vcert checkcred --platform tpp --url https://<tpp_fqdn>/vedsdk   -t <token>
```


```text title="Expected output"
Successfully authenticated to Venafi as a Service
Credentials saved to: /home/admin/.vcert/credentials.json
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Successfully authenticated to Trust Protection Platform
Credentials saved to: /home/admin/.vcert/credentials.json
Session established with tpp.example.com
Token expires: 2025-02-15T14:32:00Z

Credentials verified successfully
Platform: Trust Protection Platform
User: admin@example.com
Status: Valid
Token expiration: 2025-02-15T14:32:00Z
```

!!! warning "Common errors"
    **`Error: invalid API key format`** — Verify the API key is correctly copied from the Venafi console and contains no extra whitespace.
    **`Error: unable to connect to https://<tpp_fqdn>/vedsdk: connection refused`** — Confirm the TPP FQDN is correct, the server is running, and network connectivity exists from your client to the TPP instance.
    **`Error: authentication failed: invalid credentials`** — Verify the username and password are correct and the user account has not been locked or disabled in TPP.
---

## Certificate Requests

```bash
# Request a certificate (TPP)
vcert enroll --platform tpp --url https://<tpp_fqdn>/vedsdk   -t <token>   --zone "\VED\Policy\Certificates\<policy_folder>"   --cn <common_name>   --san-dns <san1> --san-dns <san2>   --key-type rsa --key-size 2048   --cert-file cert.pem --key-file key.pem --chain-file chain.pem

# Request a certificate (VaaS)
vcert enroll --platform vaas --apiKey <key>   --zone "<application>\<issuing_template>"   --cn <common_name>   --cert-file cert.pem --key-file key.pem
```


```text title="Expected output"
Successfully enrolled certificate.
Certificate: cert.pem
Private Key: key.pem
Chain: chain.pem
Request ID: 550e8400-e29b-41d4-a716-446655440000
Status: ISSUED
Common Name: example.com
Subject Alternative Names: www.example.com, api.example.com
Key Algorithm: RSA
Key Size: 2048
Thumbprint: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

!!! warning "Common errors"
    **`Error: failed to authenticate to TPP server: invalid token`** — Verify the token is valid and has not expired by checking TPP token management settings.
    **`Error: certificate request failed: policy path not found`** — Confirm the zone path exists in TPP and matches the exact folder structure with correct escaping (e.g., `\\VED\\Policy\\Certificates\\<policy_folder>`).
    **`Error: failed to write certificate file: permission denied`** — Ensure the user running vcert has write permissions to the target directory where cert.pem, key.pem, and chain.pem will be created.
---

## Certificate Renewal

```bash
# Renew a certificate by thumbprint
vcert renew --platform tpp --url https://<tpp_fqdn>/vedsdk   -t <token>   --thumbprint <sha1_thumbprint>   --cert-file renewed.pem --key-file renewed-key.pem

# Renew by certificate DN (TPP path)
vcert renew --platform tpp --url https://<tpp_fqdn>/vedsdk   -t <token>   --id "\VED\Policy\Certificates\<policy_folder>\<cn>"   --cert-file renewed.pem
```


```text title="Expected output"
Renewing certificate...
Successfully renewed certificate
Certificate saved to: renewed.pem
Private key saved to: renewed-key.pem
Renewal completed at: 2024-01-15T14:32:18Z
Certificate details:
  Subject: CN=app.example.com,O=Acme Corp,C=US
  Issuer: CN=Venafi Test CA,O=Venafi,C=US
  Valid from: 2024-01-15 to 2025-01-15
  Thumbprint: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

!!! warning "Common errors"
    **`Error: invalid thumbprint format`** — Ensure the thumbprint is a valid SHA-1 hash (40 hexadecimal characters) without spaces or special characters.
    **`Error: authentication failed: invalid token`** — Verify the token is current and has not expired by checking TPP token validity or regenerating a new authentication token.
    **`Error: certificate not found at specified DN path`** — Confirm the DN path exists in TPP by navigating to the policy folder in the Venafi console and verifying the exact certificate path.
---

## Certificate Retrieval

```bash
# Retrieve an existing certificate
vcert retrieve --platform tpp --url https://<tpp_fqdn>/vedsdk   -t <token>   --id "\VED\Policy\Certificates\<folder>\<cn>"   --cert-file cert.pem --key-file key.pem --chain-file chain.pem

# Retrieve in PKCS#12 format
vcert retrieve --platform tpp --url https://<tpp_fqdn>/vedsdk   -t <token>   --id "\VED\Policy\Certificates\<folder>\<cn>"   --format pkcs12 --file cert.p12 --password <p12_pass>
```


```text title="Expected output"
Successfully retrieved certificate.
Certificate: cert.pem
Private Key: key.pem
Chain: chain.pem
Successfully retrieved certificate.
Certificate: cert.p12
```

!!! warning "Common errors"
    **`Error: invalid credentials`** — Verify the token is valid and has not expired by checking TPP token management or regenerating a new token.
    **`Error: certificate not found at path \VED\Policy\Certificates\<folder>\<cn>`** — Confirm the certificate path exists in TPP by navigating to the policy folder and checking the exact certificate object name.
    **`Error: permission denied writing to cert.pem`** — Ensure the output directory is writable and the user running vcert has write permissions to the target location.
---

## TPP REST API

The TPP REST API base URL is `https://<tpp_fqdn>/vedsdk`.

```bash
# Authenticate and get token
curl -X POST https://<tpp_fqdn>/vedauth/authorize/integrated   -H "Content-Type: application/json"   -d '{"Username":"<user>","Password":"<pass>","client_id":"vcert-cli","scope":"certificate:manage,delete,discover"}'

# List certificates in a policy folder
curl -X POST https://<tpp_fqdn>/vedsdk/certificates/retrieve   -H "X-Venafi-Api-Key: <token>"   -H "Content-Type: application/json"   -d '{"PolicyDN":"\\VED\\Policy\\Certificates\\<folder>"}'

# Get certificate details
curl -X GET "https://<tpp_fqdn>/vedsdk/certificates/<cert_guid>"   -H "X-Venafi-Api-Key: <token>"

# Request a new certificate
curl -X POST https://<tpp_fqdn>/vedsdk/certificates/request   -H "X-Venafi-Api-Key: <token>"   -H "Content-Type: application/json"   -d '{"PolicyDN":"\\VED\\Policy\\Certificates\\<folder>","Subject":"CN=<cn>"}'
```


```text title="Expected output"
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTMxNjgwMH0.x7K9mN2pQ5vW8zL1","token_type":"Bearer","expires_in":3600}
{"Certificates":[{"Guid":"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6","Name":"web-prod-01.example.com","Subject":"CN=web-prod-01.example.com","Issuer":"CN=Internal CA","ValidFrom":"2024-01-15T10:30:00Z","ValidUntil":"2025-01-15T10:30:00Z"},{"Guid":"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7","Name":"api-staging.example.com","Subject":"CN=api-staging.example.com","Issuer":"CN=Internal CA","ValidFrom":"2024-02-01T14:22:00Z","ValidUntil":"2025-02-01T14:22:00Z"}],"Count":2}
{"Guid":"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6","Name":"web-prod-01.example.com","Subject":"CN=web-prod-01.example.com,O=Example Corp,C=US","Issuer":"CN=Internal CA,O=Example Corp,C=US","ValidFrom":"2024-01-15T10:30:00Z","ValidUntil":"2025-01-15T10:30:00Z","Thumbprint":"3F2504E0A27EA1D01D4F0368B0EE4B92E94C57D8","Status":"Active"}
{"Guid":"c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8","CertificateRequestId":"req-2024-031847","Status":"Pending","Subject":"CN=newapp.example.com","CreatedDate":"2024-03-18T09:45:22Z"}
```

!!! warning "Common errors"
    **`{"Error":"Unauthorized","Code":401}`** — Verify credentials are correct and the user account has API access permissions in Venafi TPP.
    **`{"Error":"Invalid policy path","Code":400}`** — Ensure the PolicyDN path uses correct escaping (double backslashes) and the folder exists in the certificate policy tree.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl or configure proper CA certificates if using self-signed TPP certificates in non-production environments.
---

## Certificate Inspection (openssl)

```bash
# Verify a retrieved certificate
openssl x509 -in cert.pem -noout -text | grep -E "Subject:|Issuer:|Not After"

# Check certificate matches the private key
openssl x509 -noout -modulus -in cert.pem | md5sum
openssl rsa -noout -modulus -in key.pem | md5sum

# Verify certificate chain
openssl verify -CAfile chain.pem cert.pem

# Test TLS with the certificate
openssl s_client -connect <host>:443 -servername <host>
```


```text title="Expected output"
Subject: CN = example.acme.com, O = ACME Corporation, C = US
Issuer: CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
Not After : Dec 15 10:30:45 2025 GMT
5d41402abc4b2a76b9719d911017c592
5d41402abc4b2a76b9719d911017c592
cert.pem: OK
depth=0 self signed certificate
verify return:1
---
Certificate chain
 0 s:CN = example.acme.com, O = ACME Corporation, C = US
   i:CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
-----BEGIN CERTIFICATE-----
MIIFWTCCBEGgAwIBAgIQD8CSqAc+TEwrlXuwMlqWDDANBgkqhkiG9w0BAQsFADB
...
-----END CERTIFICATE-----
subject=CN = example.acme.com, O = ACME Corporation, C = US
issuer=CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
---
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and the file contains valid PEM-formatted data.
    **`unable to load Private Key`** — Ensure the private key file exists, is readable, and matches the certificate's key pair.
    **`error 20 at 0 depth lookup: unable to get local issuer certificate`** — Add the complete certificate chain (intermediate and root CA) to the chain.pem file in the correct order.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Venafi — Procedures](../procedures/)
- [Venafi — Health Checks](../health-checks/)
- [Venafi — Scripts](../scripts/)
- [Venafi — Backup and Restore](../backup-restore/)
- [Venafi — Install and Upgrade](../install-upgrade/)
- [Venafi — Common Issues](../../troubleshooting/common-issues/)
