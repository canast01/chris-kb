# Certificate Trust

```text
┌──────────────────────────────────────────────────────────────────────┐
│                   Certificate Trust Chain                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │               Internal Root CA Certificate                   │    │
│  │           (self-signed, long-lived, offline)                 │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │  signs                                 │
│  ┌──────────────────────────▼───────────────────────────────────┐    │
│  │             Intermediate / Issuing CA                        │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │  issues leaf certs                     │
│                             ▼                                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────┐     │
│  │  vCenter   │  │  vSAN/NSX  │  │ App Server │  │  Appliance  │     │
│  │ leaf cert  │  │ leaf cert  │  │ leaf cert  │  │  leaf cert  │     │
│  └────────────┘  └────────────┘  └────────────┘  └─────────────┘     │
│                                                                      │
│  Root CA imported to trust store on each system → TLS validates      │
│  Linux: update-ca-certificates  Windows: Cert:\LocalMachine\Root     │
└──────────────────────────────────────────────────────────────────────┘
```

Configure and verify certificate trust chains so that services can validate TLS certificates from internal and external CAs.
## Trust Store Locations

| OS / Platform | System Trust Store | Command to Add CA |
|---|---|---|
| Ubuntu / Debian | `/etc/ssl/certs/` | `update-ca-certificates` |
| RHEL / CentOS / Rocky | `/etc/pki/ca-trust/` | `update-ca-trust extract` |
| macOS | Keychain | `security add-trusted-cert` |
| Windows | `Cert:\LocalMachine\Root` | `Import-Certificate` |
| Java | JRE `cacerts` | `keytool -importcert` |
| Python (requests) | System store or `certifi` | Set `REQUESTS_CA_BUNDLE` |

## Add a CA Certificate — Linux

```bash
# Ubuntu / Debian
cp internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt
update-ca-certificates
# Verify
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt

# RHEL / Rocky / AlmaLinux
cp internal-ca.crt /etc/pki/ca-trust/source/anchors/internal-ca.crt
update-ca-trust extract
# Verify
trust list | grep "internal-ca"
```

## Add a CA Certificate — Windows

```powershell
# Import CA into Trusted Root store (machine level)
Import-Certificate -FilePath "C:\certs\internal-ca.crt" -CertStoreLocation Cert:\LocalMachine\Root

# Verify
Get-ChildItem -Path Cert:\LocalMachine\Root | Where-Object { $_.Subject -like "*Internal CA*" }
```

## Add a CA Certificate — Java

```bash
# Add to JRE trust store
keytool -importcert -alias internal-ca \
  -file /path/to/internal-ca.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit -noprompt

# Verify
keytool -list -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit | grep internal-ca
```

## Verify a Certificate Chain

```bash
# Full chain verification
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt

# Verify chain from a specific CA file
openssl verify -CAfile internal-ca.crt -untrusted intermediate.crt server.crt

# Inspect certificate details
openssl x509 -in server.crt -noout -text | grep -E "Subject:|Issuer:|Not After|Not Before|DNS:"

# Check certificate fingerprint (compare with expected)
openssl x509 -in server.crt -noout -fingerprint -sha256

# Test live TLS trust from the OS
openssl s_client -connect <hostname>:443 -CAfile /etc/ssl/certs/ca-certificates.crt </dev/null 2>&1 | grep -E "Verify return|Certificate chain"
```

## Diagnose Trust Failures

```bash
# Full TLS handshake trace
openssl s_client -connect <host>:443 -showcerts </dev/null

# Check what CA signed the certificate
openssl s_client -connect <host>:443 </dev/null 2>/dev/null | openssl x509 -noout -issuer

# curl verbose TLS debug
curl -v --cacert /path/to/internal-ca.crt https://<host>/endpoint

# Python — test with custom CA
REQUESTS_CA_BUNDLE=/path/to/internal-ca.crt python3 -c "import requests; print(requests.get('https://<host>').status_code)"
```

## Certificate Expiry Check

```bash
# Check expiry of a file
openssl x509 -in server.crt -noout -enddate

# Check expiry on a live endpoint
echo | openssl s_client -connect <host>:443 2>/dev/null | openssl x509 -noout -enddate

# Bulk check for certs expiring within 30 days
for cert in /etc/ssl/certs/*.crt; do
  expiry=$(openssl x509 -in "$cert" -noout -enddate 2>/dev/null | cut -d= -f2)
  if openssl x509 -in "$cert" -noout -checkend 2592000 2>/dev/null; then :
  else echo "EXPIRING: $cert — $expiry"; fi
done
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `certificate verify failed` | CA not trusted? Self-signed? | Add CA to system trust store; `update-ca-certificates` |
| `unable to get local issuer certificate` | Intermediate CA missing | Ensure server sends full chain; or add intermediate to trust store |
| CA added but service still fails | Service using own bundle (Java, Python) | Add CA to app-specific trust store / env var |
| Certificate expired | `openssl x509 -enddate` | Renew certificate; update on all endpoints |
| SNI mismatch | Certificate SAN doesn't match hostname | Reissue cert with correct SAN; or use correct hostname in client |
| Windows app still rejects | Machine vs user store | Import to `Cert:\LocalMachine\Root` not `CurrentUser\Root` |
