---
tags:
  - operations
  - security
description: "| Field | Value | |---|---| | Risk | Medium | | Approval | Standard change for planned renewals; emergency change if < 7 days to expiry | | Estimated time..."
---
# Certificate Renewal Runbook

<div class="kb-summary">
| Field | Value | |---|---| | Risk | Medium | | Approval | Standard change for planned renewals; emergency change if < 7 days to expiry | | Estimated time | 30–60 minutes | | Impact | Brief service interruption during hot-swap (seconds); expired cert causes full outage |
</div>

| Field | Value |
|---|---|
| Risk | Medium |
| Approval | Standard change for planned renewals; emergency change if < 7 days to expiry |
| Estimated time | 30–60 minutes |
| Impact | Brief service interruption during hot-swap (seconds); expired cert causes full outage |

```d2
direction: down

renewal_timeline: "Renewal Timeline" {shape: rectangle}
step_2_generate_private_key_and_csr: "Step 2 — Generate Private Key and CSR" {shape: rectangle}
step_3_submit_to_ca: "Step 3 — Submit to CA" {shape: rectangle}
step_4_install_certificate: "Step 4 — Install Certificate" {shape: rectangle}
step_5_postrenewal_validation: "Step 5 — Post-Renewal Validation" {shape: rectangle}
rollback: "Rollback" {shape: rectangle}

renewal_timeline -> step_2_generate_private_key_and_csr: uses
step_2_generate_private_key_and_csr -> step_3_submit_to_ca: uses
step_3_submit_to_ca -> step_4_install_certificate: uses
step_4_install_certificate -> step_5_postrenewal_validation: uses
step_5_postrenewal_validation -> rollback: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Renewal Timeline

**Capture:** CN, SANs, issuing CA, expiry date, key algorithm.

## Step 2 — Generate Private Key and CSR

```bash
# RSA 2048 (minimum); prefer RSA 4096 or ECDSA P-256 for new certs
openssl req -new -newkey rsa:4096 -nodes \
    -keyout <hostname>.key \
    -out <hostname>.csr \
    -subj "/CN=<hostname>/O=<org>/C=GB"

# With SANs (required for modern browsers)
openssl req -new -newkey rsa:4096 -nodes \
    -keyout <hostname>.key \
    -out <hostname>.csr \
    -config <(cat /etc/ssl/openssl.cnf <(printf "\n[SAN]\nsubjectAltName=DNS:<hostname>,DNS:<alias>")) \
    -reqexts SAN
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Can't open config file: /etc/ssl/openssl.cnf` | Verify the openssl config path with `openssl version -d` and adjust the path accordingly for your OS (e.g., `/usr/lib/ssl/openssl.cnf` on some Linux distributions). |
    | `unable to write 'random state'` | Ensure the user running the command has write permissions to `$HOME/.rnd` or set `RANDFILE=/tmp/.rnd` before executing. |
    | `req: Unrecognized flag reqexts` | Use `-addext` instead of `-reqexts` for newer OpenSSL versions (3.0+), or verify your OpenSSL version supports the `-reqexts` flag with `openssl version`. |
## Step 3 — Submit to CA

**Internal (ADCS):**
```powershell
# Submit CSR via PowerShell
certreq -submit -attrib "CertificateTemplate:<TemplateName>" <hostname>.csr <hostname>.cer
```

**Venafi:**
- Upload CSR in Aperture → Request Certificate → Paste CSR

**External / Let's Encrypt (ACME):**
```bash
certbot certonly --manual --preferred-challenges dns -d <hostname>
```


```text title="Expected output"
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator (manual), Installer (None)
Starting new HTTPS connection (1): acme-v02.api.letsencrypt.org
Please deploy a DNS TXT record under the name:
_acme-challenge.prod-api.example.com.

with the following value:

a7K9mP2xL_vQ8nR4sT6uW1yZ3aB5cD7eF9gH2jK4lM6nO8pQ0rS2tU4vW6xY8zA

Before continuing, verify the record is deployed. Press ENTER to continue.

Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate is ready at /etc/letsencrypt/live/prod-api.example.com/fullchain.pem
 - Your key file has been saved at /etc/letsencrypt/live/prod-api.example.com/privkey.pem
 - Your cert will expire on 2025-04-15. To renew early, run the same command again.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: The following errors were reported by the server: Domain authorization failed` | Verify the DNS TXT record was created correctly and is propagating (use `dig _acme-challenge.<hostname> TXT`), then retry. |
    | `Error: Timeout during authorization` | Increase the wait time before pressing ENTER by checking DNS propagation with `nslookup` or `dig`, or use `--manual-auth-hook` to automate DNS updates. |
## Step 4 — Install Certificate

**Linux (nginx / apache):**
```bash
cp <hostname>.crt /etc/ssl/certs/<hostname>.crt
cp <hostname>.key /etc/ssl/private/<hostname>.key
cp <ca-chain>.pem /etc/ssl/certs/<ca-chain>.pem

# Test config before reload
nginx -t
systemctl reload nginx
```


```text title="Expected output"
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cp: cannot create regular file '/etc/ssl/certs/<hostname>.crt': Permission denied` | Run the commands with `sudo` or as root user. |
    | `nginx: [error] open() "/etc/ssl/private/<hostname>.key" failed (2: No such file or directory)` | Verify the certificate and key filenames match exactly and exist in the source directory before copying. |
    | `Job for nginx.service failed because the control process exited with error code.` | Check `nginx -t` output for syntax errors in the certificate paths within nginx.conf, or ensure file permissions are readable by the nginx user (644 for certs, 600 for keys). |
**VMware vCenter:**
- vSphere Client → Administration → Certificate Management → Replace Certificate

**NetApp ONTAP:**
```bash
security certificate install -vserver <svm> -type server
```


```text title="Expected output"
Certificate installation initiated for SVM 'prod-svm-01'
Generating certificate signing request (CSR)...
CSR generated successfully with serial number: 4A7B2C9E1F5D8K3L
Waiting for certificate authority response...
Certificate received and validated
Installing certificate on vserver prod-svm-01...
Certificate installation completed successfully
Certificate details:
  Common Name: prod-svm-01.corp.local
  Issuer: CN=Corporate-CA-01
  Valid from: 2024-01-15 to 2026-01-14
  Thumbprint: 8F2E9C1A7B4D6K5L9M3N2O1P
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Vserver <svm> does not exist` | Verify the SVM name with `security certificate show` and ensure you are connected to the correct cluster. |
    | `Error: Certificate installation failed - CSR signing timeout` | Check network connectivity to your certificate authority and verify firewall rules allow outbound HTTPS traffic on port 443. |
    | `Error: A certificate of type 'server' already exists on this vserver` | Delete the existing certificate with `security certificate delete -vserver <svm> -type server` before installing a new one. |
**Windows IIS:**
```powershell
Import-PfxCertificate -FilePath <cert.pfx> -CertStoreLocation Cert:\LocalMachine\My
# Then bind in IIS Manager → Site → Bindings → Edit → Select new cert
```

## Step 5 — Post-Renewal Validation

```bash
# Confirm new expiry date is live
echo | openssl s_client -connect <hostname>:443 -servername <hostname> 2>/dev/null \
    | openssl x509 -noout -dates

# Verify chain is valid
openssl verify -CAfile <ca-chain.pem> <hostname>.crt

# Test from client
curl -sv https://<hostname>/ 2>&1 | grep -i "SSL\|expire\|valid"
```


```text title="Expected output"
notBefore=Jan 15 10:23:45 2024 GMT
notAfter=Jan 15 10:23:45 2025 GMT
<hostname>.crt: OK
*  SSL connection using TLSv1.3 / ECDHE-RSA-AES256-GCM-SHA384
*  Server certificate:
*   subject: CN=<hostname>,O=Example Corp,C=US
*   start date: Jan 15 10:23:45 2024 GMT
*   expire date: Jan 15 10:23:45 2025 GMT
*   issuer: CN=Example Intermediate CA,O=Example Corp,C=US
*   SSL certificate verify ok.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error 20 at 0 depth lookup: unable to get local issuer certificate` | Add the intermediate CA certificate to your CA chain file or ensure the full chain is included in `<ca-chain.pem>`. |
    | `curl: (60) SSL certificate problem: self signed certificate` | Either add the self-signed cert to your system's trusted store or use `curl -k` for testing only, then verify the cert manually with `openssl x509`. |
    | `error in x509_check_cert_time(): certificate has expired` | The certificate notAfter date has passed; renew the certificate immediately and redeploy it to the server. |
Expected: `notAfter` should show the new expiry date (typically 1–2 years out).

## Rollback

Keep the old certificate and key until the new cert is confirmed working:

```bash
# Restore old cert if new cert causes issues
cp <hostname>.crt.bak /etc/ssl/certs/<hostname>.crt
cp <hostname>.key.bak /etc/ssl/private/<hostname>.key
systemctl reload nginx
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cp: cannot stat '<hostname>.crt.bak': No such file or directory` | Replace `<hostname>` with the actual certificate filename (e.g., `cp server.crt.bak /etc/ssl/certs/server.crt`) or verify backup files exist in the current directory. |
    | `cp: permission denied` | Run the commands with `sudo` since `/etc/ssl/certs/` and `/etc/ssl/private/` require root privileges. |
## Common Issues

| Issue | Check | Action |
|---|---|---|
| Certificate chain incomplete | Intermediate CA missing | Include full chain in cert file |
| CN / SAN mismatch | `openssl x509 -noout -text` | Reissue with correct SANs |
| Private key mismatch | `openssl x509 -noout -modulus` vs `openssl rsa -noout -modulus` | Regenerate CSR with original key or new key pair |
| Service still showing old cert | Service not reloaded | Reload / restart service; check if cert path is correct in config |
| Browser shows warning after install | Intermediate CA not installed | Append CA chain to cert file |

## Checklist

- [ ] Expiry date and service confirmed
- [ ] CN and SANs documented
- [ ] New private key and CSR generated
- [ ] CSR submitted to correct CA
- [ ] Signed cert and chain downloaded
- [ ] Old cert backed up
- [ ] New cert installed
- [ ] Service reloaded
- [ ] New expiry date confirmed via openssl
- [ ] Cert inventory updated (Venafi / spreadsheet)
- [ ] Ticket closed

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Account Unlock](../account-unlock/)
- [Chris Kb — Overview](../)
