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

## Renewal Timeline

```text
┌──────────────────────────────────── Runbook — Certificate Renewal ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Renew SSL/TLS certificates before expiry; update all consumers; verify chain         │   │
│   │       Timeline: start 30+ days before expiry; verify deployment before old cert expires       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Step 1 — Identify expiring certificates (< 30 days)                      │   │
│   │                openssl s_client -connect <host>:443 | openssl x509 -noout -dates              │   │
│   │                        Venafi / cert inventory report for < 30-day expiry                     │   │
│   │                        Step 2 — Generate CSR (or use ACME/Venafi auto)                        │   │
│   │               openssl req -new -key server.key -out server.csr -subj "/CN=<fqdn>"             │   │
│   │                   Step 3 — Submit to CA; download signed certificate + chain                  │   │
│   │             Step 4 — Install new certificate on service (nginx/IIS/appliance GUI)             │   │
│   │                   Step 5 — Verify: openssl verify -CAfile chain.pem cert.pem                  │   │
│   │               Step 6 — Test all consumers (browser, API clients, backup agents)               │   │
│   │                Step 7 — Update Venafi/CMDB with new expiry; close change ticket               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        # Check cert expiry on all hosts from inventory                        │   │
│   │                                 for HOST in "${HOSTS[@]}"; do                                 │   │
│   │                EXPIRY=$(echo | openssl s_client -connect $HOST:443 2>/dev/null \              │   │
│   │                            | openssl x509 -noout -enddate 2>/dev/null)                        │   │
│   │                                   echo "$HOST: $EXPIRY"; done                                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CSR          = Certificate Signing Request; includes public key and subject; sent to CA            │
│    Chain        = CA certificate chain (intermediate + root) required for full trust validation       │
│    ACME         = Automated cert issuance protocol (Let's Encrypt, Venafi, etc.); 90-day auto-renew   │
│    SAN          = Subject Alternative Name; include all FQDNs/IPs the cert covers                     │
│    Venafi       = Enterprise cert lifecycle management; tracks expiry and automates renewal           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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

**VMware vCenter:**
- vSphere Client → Administration → Certificate Management → Replace Certificate

**NetApp ONTAP:**
```bash
security certificate install -vserver <svm> -type server
```

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

Expected: `notAfter` should show the new expiry date (typically 1–2 years out).

## Rollback

Keep the old certificate and key until the new cert is confirmed working:

```bash
# Restore old cert if new cert causes issues
cp <hostname>.crt.bak /etc/ssl/certs/<hostname>.crt
cp <hostname>.key.bak /etc/ssl/private/<hostname>.key
systemctl reload nginx
```

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
