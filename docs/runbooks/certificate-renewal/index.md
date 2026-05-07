# Certificate Renewal Runbook
## Pre-Checks

```bash
# Check certificate expiration date
openssl x509 -in <cert.pem> -noout -dates

# Check expiry on a live service
echo | openssl s_client -connect <hostname>:443 2>/dev/null | openssl x509 -noout -dates

# Check via curl
curl -vk https://<hostname>/ 2>&1 | grep -i "expire\|valid\|issuer"
```

Alert threshold: begin renewal at **30 days** before expiry; escalate at **14 days**.

## Renewal Process

### Self-Signed / Internal CA

1. Generate CSR:
   ```bash
   openssl req -new -newkey rsa:2048 -nodes \
       -keyout <hostname>.key \
       -out <hostname>.csr \
       -subj "/CN=<hostname>/O=<org>/C=US"
   ```
2. Submit CSR to internal CA (AD CS, Venafi, etc.)
3. Download signed certificate (PEM format)

### External / Public CA

1. Generate CSR as above
2. Submit to CA via web portal or ACME (Let's Encrypt)
3. Complete domain validation
4. Download signed certificate + chain

## Install Certificate

**Linux service (nginx/apache):**
```bash
cp <hostname>.crt /etc/ssl/certs/
cp <hostname>.key /etc/ssl/private/
systemctl reload nginx
```

**VMware vCenter:**
- Managed via vSphere Client → Administration → Certificate Management

**NetApp ONTAP:**
```bash
security certificate install -vserver <svm> -type server
```

## Post-Renewal Validation

```bash
# Confirm new certificate is live
echo | openssl s_client -connect <hostname>:443 2>/dev/null | openssl x509 -noout -dates

# Confirm chain is valid
openssl verify -CAfile <ca-chain.pem> <hostname>.crt

# Check from browser — verify no certificate warning
curl -v https://<hostname>/
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Certificate chain incomplete | Intermediate CA missing | Include full chain in cert file |
| Wrong hostname | CN or SAN mismatch | Reissue cert with correct SAN |
| Private key mismatch | Key doesn't match cert | Re-generate CSR with correct key |
| Service still showing old cert | Service not reloaded | Restart / reload the service |
