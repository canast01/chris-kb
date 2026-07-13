---
tags:
  - operations
  - security
description: "Procedures reference covering Certificate Renewal and Revocation Workflow, Renewal, Inventory, TLS Validation."
---
# Certificates — Procedures

<div class="kb-summary">
Procedures reference covering Certificate Renewal and Revocation Workflow, Renewal, Inventory, TLS Validation.
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Certificate Renewal and Revocation Workflow

```d2
direction: right

renewTrigger: "Renewal trigger\n(80% validity elapsed or expiry alert" {shape: rectangle}
checkAuto: "Automated\nrenewal?" {shape: rectangle}
autoRenew: "Automated renewal flow\nNew CSR generated and submitted" {shape: rectangle}
manualRenew: "Generate new key pair + CSR\non target host" {shape: rectangle}
caIssue: "CA issues new certificate" {shape: rectangle}
submitCA: "Submit CSR via Venafi / ADCS portal" {shape: rectangle}
install: "Install on target service\n(verify key matches cert" {shape: rectangle}
tlsTest: "TLS validation:\nopenssl s_client + openssl verify" {shape: rectangle}
done: "Renewal complete\nUpdate inventory" {shape: rectangle}
revokeTrigger: "Revocation trigger\n(key compromise / decommission" {shape: rectangle}
revokeCA: "Revoke via ADCS:\ncertutil -revoke serial 1" {shape: rectangle}
publishCRL: "Publish updated CRL:\ncertutil -CRL" {shape: rectangle}
ocspUpdate: "OCSP responder updated\n(auto from CA database" {shape: rectangle}
replaceCert: "Generate new key + cert\non clean host" {shape: rectangle}
auditDoc: "Document incident\nand root cause" {shape: rectangle}

renewTrigger -> checkAuto
checkAuto -> autoRenew
checkAuto -> manualRenew
autoRenew -> caIssue
manualRenew -> submitCA
submitCA -> caIssue
caIssue -> install
install -> tlsTest
tlsTest -> done
revokeTrigger -> revokeCA
revokeCA -> publishCRL
publishCRL -> ocspUpdate
ocspUpdate -> replaceCert
replaceCert -> auditDoc
```

---

## Renewal

Certificate renewal should be initiated at 80% of the certificate's validity period (e.g., for a 2-year certificate, renew after ~20 months).

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

### Emergency Revocation Checklist

- [ ] Revoke certificate via ADCS or vendor portal
- [ ] Publish updated CRL immediately
- [ ] Notify service owner to replace certificate
- [ ] Verify revocation propagated to OCSP responder
- [ ] Audit which services were using the revoked certificate
- [ ] Generate and install replacement certificate
- [ ] Verify replacement is correctly installed and trusted
- [ ] Document incident with timeline and root cause

---

## Inventory

Maintaining an accurate certificate inventory prevents surprise expirations. Inventory should cover all certificates: public-facing TLS, internal services, code signing, client authentication.

### Discovery Methods

| Method | Coverage | Effort |
|---|---|---|
| Port scanning with nmap | External/internal TLS endpoints | Low — automated |
| openssl per host | Targeted host checks | Low — scriptable |
| Venafi / DigiCert One | Managed certificates | Low (integrated) |
| AD Certificate Services | Internally issued certs | Low (ADCS reports) |
| Manual tracking spreadsheet | Small environments | Medium — human |
| Shodan / Censys | External internet-facing | Low (API) |

### Port Scanning for Certificates

```bash
# Scan a subnet for TLS on common ports
nmap -p 443,8443,636,993,995 --script ssl-cert 192.168.1.0/24 \
    -oX ssl-scan.xml

# Extract CN and expiry from nmap XML output
grep -A5 "ssl-cert" ssl-scan.xml | grep -E "commonName|notAfter"

# Quick single-host TLS cert dump
nmap -p 443 --script ssl-cert example.com \
    | grep -E "Subject:|Not valid after"
```


```text title="Expected output"
Starting Nmap 7.92 ( https://nmap.org ) at 2024-01-15 10:23:45 UTC
Nmap scan report for 192.168.1.50
Host is up (0.042s latency).
PORT     STATE  SERVICE
443/tcp  open   https
8443/tcp closed pcsync-https
636/tcp  closed ldapssl
993/tcp  open   imaps
995/tcp  closed pop3s
| ssl-cert: Subject: commonName=mail.internal.corp/organizationName=Acme Inc
| Not valid before: 2023-06-14T08:22:11Z
|_Not valid after: 2025-06-14T08:22:11Z

Nmap scan report for 192.168.1.51
Host is up (0.038s latency).
PORT     STATE  SERVICE
443/tcp  open   https
...
Nmap done at 2024-01-15 10:24:12 UTC; 256 IP addresses (8 hosts up) scanned in 27.34 seconds

commonName=mail.internal.corp
notAfter=2025-06-14T08:22:11Z
commonName=api-gateway.internal.corp
notAfter=2024-03-22T14:55:33Z

Starting Nmap 7.92 ( https://nmap.org ) at 2024-01-15 10:25:01 UTC
Nmap scan report for example.com (93.184.216.34)
Host is up (0.028s latency).
PORT    STATE SERVICE
443/tcp open  https
| Subject: CN=www.example.com, O=Example Inc, C=US
|_Not valid after: 2025-12-31T23:59:59Z
Nmap done at 2024-01-15 10:25:02 UTC; 1 IP address (1 host up) scanned in 1.34 seconds
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Nmap done at ... ; 0 hosts up scanned` | Verify network connectivity and that the target subnet is reachable; check firewall rules blocking ICMP or the specified ports. |
    | `grep: ssl-scan.xml: No such file or directory` | Ensure the first nmap command completed successfully and the XML output file was written before attempting to parse it. |
    | `Host seems down. If it is really up, but blocking all ping probes, try -Pn` | Add the `-Pn` flag to nmap to skip host discovery and scan ports directly on unresponsive hosts. |
### openssl-Based Discovery

```bash
# Grab cert details from a live endpoint
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 -noout -subject -issuer -dates -fingerprint

# Check SAN entries (Subject Alternative Names)
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 -noout -text | grep -A2 "Subject Alternative Name"

# Extract cert to file for further analysis
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 > example-com.pem
```


```text title="Expected output"
subject=CN = example.com, O = Example Corp, C = US
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
notBefore=Jan 15 10:22:33 2023 GMT
notAfter=Jan 15 10:22:32 2024 GMT
sha1Fingerprint=A1:B2:C3:D4:E5:F6:07:18:29:3A:4B:5C:6D:7E:8F:90:A1:B2:C3:D4

                X509v3 Subject Alternative Name: 
                    DNS:example.com, DNS:www.example.com, DNS:api.example.com
-----BEGIN CERTIFICATE-----
MIIFWTCCBEGgAwIBAgIQD8Z4wyKd/N4OMwegHWLqRDANBgkqhkiG9w0BAQsFADBL
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMSswKQYDVQQDEyJE
...
-----END CERTIFICATE-----
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `connect: Connection refused` | Verify the hostname is correct and the server is listening on port 443 with `nc -zv example.com 443`. |
    | `unable to load certificate` | Ensure the endpoint is returning a valid certificate; test connectivity with `curl -v https://example.com` first. |
    | `grep: (standard input): No such file or directory` | The certificate text output may be empty if the connection fails; add error checking with `set -e` or verify the domain resolves with `nslookup example.com`. |
### Windows Certificate Store Inventory

```powershell
# List all certs in the local machine Personal store
Get-ChildItem Cert:\LocalMachine\My |
    Select-Object Subject, Issuer, Thumbprint, NotBefore, NotAfter |
    Export-Csv C:\CertInventory.csv -NoTypeInformation

# List certs across all stores
foreach ($store in @("My","CA","Root","TrustedPeople")) {
    Get-ChildItem "Cert:\LocalMachine\$store" |
        Select-Object @{N="Store";E={$store}}, Subject, NotAfter, Thumbprint
}

# Find certs issued by a specific CA
Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Issuer -like "*Internal CA*"} |
    Select-Object Subject, NotAfter, Thumbprint
```

### Tracking Spreadsheet Columns

Minimum fields for a useful inventory:

| Field | Notes |
|---|---|
| FQDN / Subject CN | Primary identifier |
| SANs | All covered hostnames |
| Issuer / CA | Root or intermediate that issued it |
| Expiry Date | ISO 8601 format |
| Owner / Team | Who is responsible for renewal |
| Renewal Method | Manual / Venafi / ACME / ADCS |
| Last Renewed | Track renewal history |
| Notes | Any special install steps |

### Venafi Inventory Queries (REST API)

```bash
# Authenticate and get API token
curl -s -X POST https://tpp.corp.example.com/vedauth/authorize \
    -H "Content-Type: application/json" \
    -d '{"Username":"svc-venafi","Password":"P@ssw0rd!"}' \
    | jq '.APIKey'

# List certificates expiring in 90 days
curl -s https://tpp.corp.example.com/vedsdk/certificates \
    -H "X-Venafi-API-Key: $TOKEN" \
    -G --data-urlencode "ValidToLess=2026-08-01" \
    | jq '.Certificates[] | {CN: .Name, Expiry: .ValidTo}'
```


```text title="Expected output"
"62d4f8c9-7e3a-4b21-9f6e-8a2c1d5e9b3f"
{
  "CN": "api.prod.corp.example.com",
  "Expiry": "2026-07-28T23:59:59.000Z"
}
{
  "CN": "db-primary.internal.corp.example.com",
  "Expiry": "2026-07-15T23:59:59.000Z"
}
{
  "CN": "*.services.corp.example.com",
  "Expiry": "2026-07-22T23:59:59.000Z"
}
{
  "CN": "mail.corp.example.com",
  "Expiry": "2026-07-31T23:59:59.000Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: unable to get local issuer certificate` | Add the Venafi server's CA certificate to your system trust store or use `curl -k` to skip verification in non-production environments. |
    | `jq: error (at <stdin>:1): Cannot index null with string "APIKey"` | Verify the service account credentials are correct and the `/vedauth/authorize` endpoint is accessible; check response with `curl -s ... | jq '.'` to see the actual error. |
    | `curl: (7) Failed to connect to tpp.corp.example.com port 443: Connection refused` | Confirm the Venafi TPP hostname and port are correct and the server is running; test connectivity with `ping tpp.corp.example.com` or `nc -zv tpp.corp.example.com 443`. |
---

## TLS Validation

```bash
# Test TLS handshake and show server certificate
openssl s_client -connect <host>:443 -servername <host>

# Check specific TLS version support
openssl s_client -connect <host>:443 -tls1_2
openssl s_client -connect <host>:443 -tls1_3

# Show full certificate chain from a live endpoint
openssl s_client -connect <host>:443 -showcerts </dev/null 2>/dev/null

# Verify certificate against a CA bundle
openssl verify -CAfile ca-bundle.pem cert.pem

# Verify full chain (intermediate + root)
openssl verify -CAfile root.pem -untrusted intermediate.pem cert.pem
```


```text title="Expected output"
CONNECTED(00000000)
depth=0 /C=US/ST=California/L=San Francisco/O=Acme Corp/CN=api.example.com
verify return:1
subject=/C=US/ST=California/L=San Francisco/O=Acme Corp/CN=api.example.com
issuer=/C=US/ST=California/O=DigiCert Inc/CN=DigiCert SHA2 Secure Server CA
-----BEGIN CERTIFICATE-----
MIIFWDCCBECgAwIBAgIQD8CSsj7+UL5vAwAAAAAA7TANBgkqhkiG9w0BAQsFADB1
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExho
...
-----END CERTIFICATE-----
---
Certificate chain
 0 s:/C=US/ST=California/L=San Francisco/O=Acme Corp/CN=api.example.com
   i:/C=US/ST=California/O=DigiCert Inc/CN=DigiCert SHA2 Secure Server CA
 1 s:/C=US/ST=California/O=DigiCert Inc/CN=DigiCert SHA2 Secure Server CA
   i:/C=US/ST=Root CA/O=DigiCert/CN=DigiCert Global Root CA
---
cert.pem: OK
intermediate.pem: OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `verify error:num=20:unable to get local issuer certificate` | Add the issuer's CA certificate to your CA bundle or use the `-untrusted` flag to specify intermediate certificates. |
    | `connect:errno=111 Connection refused` | Verify the hostname and port are correct, and that the target service is running and accessible from your network. |
    | `error:0906D06C:PEM routines:PEM_read_bio:no start line` | Ensure the certificate file is in valid PEM format and not corrupted; check the file encoding with `file cert.pem`. |
---

## Request a Certificate via Web Enrollment

Use the ADCS Web Enrollment portal to submit a CSR and download the issued certificate when auto-enrollment is not available (non-domain systems, network appliances, Linux hosts).

1. Browse to `https://<ca>/certsrv` and authenticate with a domain account that has Enroll permission on the target template.
2. Select **Request a Certificate** → **Advanced certificate request**.
3. Paste the Base-64 encoded CSR into the **Saved Request** field.
4. Select the appropriate certificate template from the **Certificate Template** drop-down.
5. Click **Submit** — if CA policy requires manager approval, the request will be marked Pending.
6. Once issued, return to `https://<ca>/certsrv` → **View the status of a pending certificate request** → select the request → **Download certificate** (Base-64 or DER).
7. Install the certificate on the target host and bind it to the relevant service.

Verify the issued certificate includes the correct Subject CN, SANs, and issuing CA using `openssl x509 -noout -text -in cert.pem`.

---

## Export a Certificate with Private Key (PFX)

Export a certificate and its private key from the Windows certificate store for backup or migration to another host.

1. Open **Certificate Manager** (`certlm.msc`) — this opens the Local Machine store.
2. Expand **Personal → Certificates** and locate the certificate.
3. Right-click the certificate → **All Tasks → Export**.
4. In the Certificate Export Wizard, select **Yes, export the private key** → **Next**.
5. Leave format as **Personal Information Exchange — PKCS #12 (.PFX)** → check **Include all certificates in the certification path** → **Next**.
6. Set a strong password to protect the private key → **Next**.
7. Choose the save location → **Finish**.

```powershell
# Export via PowerShell (alternative)
$cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*webserver*"}
$pwd = ConvertTo-SecureString "ExportP@ss!" -AsPlainText -Force
Export-PfxCertificate -Cert $cert -FilePath C:\Export\webserver.pfx -Password $pwd
```

Store the PFX and password in separate secure locations. Delete the exported file after completing the migration.

---

## Configure Auto-Enrollment GPO

Auto-enrollment automatically issues and renews certificates for domain members based on certificate templates, eliminating manual renewal for internal certificates.

1. Open **Group Policy Management** and create or edit a GPO linked to the target OU (or domain).
2. Navigate to **Computer Configuration → Windows Settings → Security Settings → Public Key Policies → Certificate Services Client — Auto-Enrollment**.
3. Set **Configuration Model** to **Enabled**.
4. Check **Renew expired certificates, update pending certificates, and remove revoked certificates**.
5. Check **Update certificates that use certificate templates**.
6. Click **OK** and close the editor.
7. Force a policy refresh and trigger auto-enrollment:

```cmd
gpupdate /force
certutil -pulse
```

8. Verify issued certificates appear in `certlm.msc` under **Personal → Certificates**.

Ensure the certificate template has **Autoenroll** permission granted to the target computers or users security group. The CA must be published in AD for auto-enrollment to locate it.

---

## Monitor Certificate Expiry (PowerShell)

Run this script on all servers to identify certificates approaching expiry before they cause service outages.

```powershell
# Find certs expiring within 60 days on the local machine
Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.NotAfter -lt (Get-Date).AddDays(60)} |
    Select-Object Subject, Issuer, NotAfter, Thumbprint |
    Sort-Object NotAfter

# Run against multiple remote servers
$servers = "web01","web02","app01","app02"
foreach ($server in $servers) {
    Invoke-Command -ComputerName $server -ScriptBlock {
        Get-ChildItem Cert:\LocalMachine\My |
            Where-Object {$_.NotAfter -lt (Get-Date).AddDays(60)} |
            Select-Object @{N="Server";E={$env:COMPUTERNAME}}, Subject, NotAfter
    }
}

# Export results to CSV for tracking
Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.NotAfter -lt (Get-Date).AddDays(60)} |
    Select-Object Subject, NotAfter, Thumbprint |
    Export-Csv C:\Reports\ExpiringCerts.csv -NoTypeInformation
```

Flag any certificate with fewer than 60 days remaining for immediate renewal. Certificates with fewer than 14 days are critical — raise a P1 change if the service is production.

---

## Revoke and Republish CRL

Revoke a compromised or decommissioned certificate and publish an updated CRL so relying parties stop trusting the certificate immediately.

### Revoke the Certificate

1. Open **Certification Authority** MMC (`certsrv.msc`) on the issuing CA.
2. Expand the CA node → **Issued Certificates**.
3. Locate the certificate by serial number or subject → right-click → **All Tasks → Revoke Certificate**.
4. Select the revocation reason (Key Compromise, CA Compromise, Affiliation Changed, Superseded, Cessation of Operation, or Certificate Hold).
5. Confirm the revocation date and click **Yes**.

```cmd
# Revoke by serial number from the command line
certutil -revoke <SerialNumber> <ReasonCode>
# Reason codes: 0=Unspecified, 1=KeyCompromise, 3=Affiliation, 4=Superseded, 5=CessationOfOperation
```

### Publish an Updated CRL

```cmd
# Publish a new CRL immediately (bypasses normal publication schedule)
certutil -CRL

# Verify the CRL was published and check the next update time
certutil -URL <CRLDistributionPoint-URL>
```

6. Browse to the CRL Distribution Point (CDP) URL configured in the CA and confirm the updated CRL is downloadable.
7. Verify the revoked serial number appears in the CRL:

```bash
openssl crl -in crl.pem -text -noout | grep -A2 "Revoked"
```


```text title="Expected output"
Revoked Certificates:
    Serial Number: 04D2A1F5E8C9B3
        Revocation Date: Jan 15 10:23:45 2024 GMT
    Serial Number: 07E8F2C1A9D4B6
        Revocation Date: Jan 14 15:47:22 2024 GMT
    Serial Number: 0A1B3C5D7E9F2A
        Revocation Date: Jan 10 08:12:33 2024 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `No such file or directory` | Verify the CRL file path is correct and the file exists in the current directory or provide the full path to crl.pem. |
    | `unable to load CRL` | Ensure the CRL file is in valid PEM format; convert from DER format using `openssl crl -inform DER -in crl.der -out crl.pem` if needed. |
Notify service owners relying on the revoked certificate to install a replacement immediately.

---

## Request and Issue a Certificate via certreq

Use `certreq` for CSR-based certificate requests on Windows hosts, especially for server certificates and non-auto-enrolled scenarios.

1. Generate a CSR and private key using a `request.inf` file that specifies Subject, KeyLength, and EnhancedKeyUsage:

```cmd
certreq -new request.inf request.csr
```

2. Submit the CSR to the CA:

```cmd
certreq -submit -attrib "CertificateTemplate:<TemplateName>" -config "<CA-Server>\<CA-Name>" request.csr response.cer
```

3. If the CA requires manager approval, approve the pending request in the Certificate Authority MMC under **Pending Requests**.

4. Retrieve the signed certificate:

```cmd
certreq -retrieve <RequestID> response.cer
```

5. Accept and install the certificate:

```cmd
certreq -accept response.cer
```

6. Verify the certificate appears in the local machine certificate store:

```powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object Subject -like "*<CN>*"
```

---

## Add a Certificate Template

Duplicate and publish a new certificate template to AD CS when a new certificate type is required (e.g., a new application, code signing, or LDAPS).

1. Open the **Certificate Templates** console (`certtmpl.msc`).

2. Right-click an existing template that is closest to the required use case → **Duplicate Template**.

3. Set the **Compatibility** tab to the minimum CA/recipient OS version in your environment.

4. On the **General** tab, set a unique **Template display name** and **Template name** (no spaces).

5. Configure the **Subject Name**, **Extensions** (EKU, Key Usage), **Security** (who can enrol), and **Request Handling** tabs as required.

6. Click **OK** to save the new template.

7. In the **Certificate Authority** MMC (`certsrv.msc`), right-click **Certificate Templates** → **New** → **Certificate Template to Issue**.

8. Select the new template and click **OK** — the template is now available for enrolment.

9. If auto-enrolment is needed, confirm the template has **Autoenroll** permission granted to the target security group, then configure Group Policy (see **Configure Auto-Enrollment GPO** above).

---

## Check CA Service Health

Run these checks on the Issuing CA server to confirm operational status before and after maintenance.

```powershell
# Confirm CA service is running
Get-Service -Name CertSvc

# List CA configuration
certutil -getconfig

# View pending certificate requests
certutil -view -restrict "disposition=9" -out "requestID,requesterName,CommonName,NotAfter"

# Check CRL validity at distribution point
certutil -URL <crl-distribution-point-url>

# Verify CRL freshness and OCSP
certutil -verifyCRL C:\Windows\System32\certsrv\CertEnroll\<ca>.crl

# View recently issued certificates
certutil -view -restrict "Disposition=20" -out "RequestID,CommonName,NotBefore,NotAfter,Requester" | head -100
```

| Event | Action Required |
|---|---|
| Certificate expiring in 60 days | Initiate renewal |
| Certificate expiring in 30 days | Escalate if not renewed |
| Certificate expiring in 7 days | Emergency renewal; notify service owners |
| CA certificate expiring in 6 months | Plan CA renewal (impacts all issued certs) |
| Key compromise suspected | Revoke immediately; issue replacement |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificates — Health Checks](../health-checks/)
- [Certificates — CLI Reference](../cli-reference/)
- [Certificates — Scripts](../scripts/)
- [Certificates — Backup and Restore](../backup-restore/)
- [Certificates — Install and Upgrade](../install-upgrade/)
- [Certificates — Common Issues](../../troubleshooting/common-issues/)
