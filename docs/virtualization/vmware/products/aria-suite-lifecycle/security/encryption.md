---
tags:
  - aria-lcm
  - security
  - vmware
description: "Encryption reference covering Importing a Signed Certificate into Locker, Verifying a Certificate Before Import, Applying a Certificate to a Product..."
---
# Aria Suite Lifecycle — Encryption

<div class="kb-summary">
Encryption reference covering Importing a Signed Certificate into Locker, Verifying a Certificate Before Import, Applying a Certificate to a Product, Password Encryption in Locker, TLS Standards and 1 more sections.

*Applies to: Aria LCM 8.x*
</div>
![Aria Suite Lifecycle — Encryption](../../../../../assets/virtualization-vmware-aria-suite-lifecycle-security-encrypti.svg)

  LCM Encryption Coverage

Submit the generated CSR to the CA. Retrieve the signed certificate chain (leaf + intermediates + root) in PEM format.

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Importing a Signed Certificate into Locker

After the CA returns the signed certificate:

**Via UI:**

```text
LCM → Locker → Certificates → Import Certificate
```

Paste:
1. Certificate (leaf PEM only — not the chain)
2. Private key (unencrypted PEM — no passphrase)
3. CA chain (all intermediates + root, concatenated in PEM format)

**Via API:**

```bash
# Read PEM files and escape newlines for JSON payload
CERT=$(awk '{printf "%s\\n", $0}' leaf.pem)
KEY=$(awk '{printf "%s\\n", $0}' private.key)
CHAIN=$(awk '{printf "%s\\n", $0}' chain.pem)

curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://lcm-prod-01.example.local/lcm/locker/api/v2/certificates/import" \
  -d "{
    \"alias\": \"vrops-prod-2027\",
    \"certificateChain\": \"$CERT\",
    \"privateKey\": \"$KEY\",
    \"caChain\": \"$CHAIN\"
  }"
```


```text title="Expected output"
{
  "documentSelfLink": "/lcm/locker/api/v2/certificates/8f4a2c91-7e3d-4b9a-8c1f-2d5e9a3b7c6f",
  "alias": "vrops-prod-2027",
  "certificateChain": "-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAKp...",
  "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA2x8q...",
  "caChain": "-----BEGIN CERTIFICATE-----\nMIIEWDCCA0CgAwIBAgIQRA...",
  "issuer": "CN=example-ca.local,O=Example Corp,C=US",
  "subject": "CN=vrops-prod-2027.example.local,O=Example Corp,C=US",
  "validFrom": "2024-01-15T00:00:00Z",
  "validTo": "2027-01-14T23:59:59Z",
  "thumbprint": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "status": "IMPORTED"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification for self-signed certificates (already present; verify TOKEN is set and endpoint is reachable). |
    | `jq: parse error: Invalid JSON at line 1` | Ensure newlines in PEM files are properly escaped; use `sed 's/$/\\n/g'` instead of awk, or pipe output through `jq -R -s` to validate JSON structure before sending. |
    | `{"errorCode":"INVALID_CERTIFICATE","message":"Certificate chain validation failed"}` | Verify the order of certificates in chain.pem (leaf first, then intermediates, then root) and that all three files are in valid PEM format without extra whitespace. |
---

## See also

- [Aria Suite Lifecycle — Hardening](../hardening/)
- [Aria Suite Lifecycle — Health Checks](../../operations/health-checks/)

## Verifying a Certificate Before Import

Always validate the certificate chain and key pair match before importing into Locker — a mismatch causes the certificate replacement workflow to fail mid-operation.

```bash
# Verify the certificate chain is valid (leaf verifiable against the CA chain)
openssl verify -CAfile chain.pem leaf.pem
# Expected: leaf.pem: OK

# Verify the private key matches the certificate (moduli must match)
openssl x509 -noout -modulus -in leaf.pem | md5sum
openssl rsa  -noout -modulus -in private.key | md5sum
# Both hashes must be identical

# Confirm the private key has no passphrase
openssl rsa -in private.key -check 2>&1 | head -1
# Expected: RSA key ok
# BAD: "Enter pass phrase" — LCM requires an unencrypted key

# Confirm SANs are present
openssl x509 -noout -text -in leaf.pem | grep -A 5 "Subject Alternative Name"

# Confirm validity period
openssl x509 -noout -dates -in leaf.pem

# Confirm key size (minimum 2048-bit; 4096-bit recommended)
openssl x509 -noout -text -in leaf.pem | grep "Public-Key"
```


```text title="Expected output"
leaf.pem: OK
5d41402abc4b2a76b9719d911017c592
5d41402abc4b2a76b9719d911017c592
RSA key ok
Subject Alternative Name: 
    DNS:aria-lcm.corp.local, DNS:*.aria-lcm.corp.local, IP Address:10.42.8.15
notBefore=Jan 15 10:22:33 2024 GMT
notAfter=Jan 14 10:22:33 2026 GMT
        Public-Key: (4096 bit, RSA)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `leaf.pem: error 20 at 0 depth lookup: unable to get local issuer certificate` | Add the intermediate CA certificate to chain.pem between the leaf and root, or use `-partial_chain` if the chain is incomplete. |
    | `5d41402abc4b2a76b9719d911017c592` (first hash) does not match second hash` | Regenerate the private key or certificate so they correspond to the same key pair. |
    | `Enter pass phrase for private.key:` | Decrypt the private key with `openssl rsa -in private.key -out private-unencrypted.key` and use the unencrypted version for LCM. |
---

## Applying a Certificate to a Product

After importing the certificate into Locker, apply it to the product:

```text
LCM → Lifecycle Operations → Environments → select environment → product card → Replace Certificate
```

1. Select the new Locker certificate alias from the dropdown
2. LCM validates the certificate is applicable (SANs cover all product node FQDNs)
3. Click **Replace** — LCM applies the certificate to all product nodes sequentially
4. Monitor progress: **Lifecycle Operations → Requests**

A successful certificate replacement shows the request in `COMPLETED` state. Verify by testing the product URL in a browser — the new certificate should be presented by the server.

```bash
# Verify the new certificate is active on the product
openssl s_client -connect vrops-prod-01.example.local:443 -servername vrops-prod-01.example.local \
  2>/dev/null | openssl x509 -noout -subject -dates -issuer
# Confirm: subject matches the new certificate, issuer is your internal CA
```


```text title="Expected output"
subject=CN=vrops-prod-01.example.local,O=Example Corp,C=US
notBefore=Jan 15 10:23:45 2024 GMT
notAfter=Jan 15 10:23:45 2025 GMT
issuer=CN=Example Corp Internal CA,O=Example Corp,C=US
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to get local issuer certificate` | The internal CA certificate is not in the system's trusted store; add it to `/etc/ssl/certs/` and run `update-ca-certificates` on Linux or import it to the certificate store on the vRealize Ops appliance. |
    | `connect: Connection refused` | The vRealize Ops service is not listening on port 443; verify the service is running with `systemctl status vrops` and check firewall rules with `iptables -L -n | grep 443`. |
---

## Password Encryption in Locker

Passwords stored in the Locker (service account credentials, vCenter passwords, etc.) are encrypted using the Locker Master Password. They are never returned in plain text via the API — only the alias and username are readable.

```bash
# List stored passwords (alias and username only — not the values)
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/locker/api/v2/passwords" | \
  jq '.passwords[] | {alias: .alias, username: .userName, description: .description}'

# Update a stored password (when the source password changes)
curl -sk -X PUT -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://lcm-prod-01.example.local/lcm/locker/api/v2/passwords/<password-id>" \
  -d '{"alias": "<alias>", "userName": "<username>", "password": "<new-password>"}'
```


```text title="Expected output"
{
  "alias": "vcenter-admin",
  "username": "administrator@vsphere.local",
  "description": "vCenter 7.0 root credentials"
}
{
  "alias": "nsxt-api",
  "username": "admin",
  "description": "NSX-T Manager API user"
}
{
  "alias": "vsan-witness",
  "username": "root",
  "description": "vSAN Witness Appliance SSH"
}
{
  "alias": "sddc-backup",
  "username": "backup_svc",
  "description": "SDDC backup service account"
}
{
  "alias": "aria-ops-db",
  "username": "postgres",
  "description": "Aria Operations PostgreSQL"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag (already present) or import the LCM root CA into your system trust store with `update-ca-certificates`. |
    | `jq: error (at <stdin>:1): Cannot index null with string "passwords"` | Verify `$TOKEN` is set and valid by running `echo $TOKEN` and confirm the LCM API endpoint is reachable with `curl -sk https://lcm-prod-01.example.local/lcm/locker/api/v2/passwords -H "x-xenon-auth-token: $TOKEN"`. |
After updating a Locker password, re-validate any product integrations that use the credential (vCenter cloud accounts in Aria Automation, adapter credentials in Aria Operations, etc.).

---

## TLS Standards

All LCM API and UI endpoints use TLS. Verify the appliance TLS configuration:

```bash
# Confirm TLS 1.2 is accepted
openssl s_client -connect lcm-prod-01.example.local:443 -tls1_2 2>/dev/null | \
  grep "Protocol"

# Confirm TLS 1.0 is rejected (expected: alert handshake failure)
openssl s_client -connect lcm-prod-01.example.local:443 -tls1 2>&1 | \
  grep -E "alert|error"

# Check cipher suite negotiated
openssl s_client -connect lcm-prod-01.example.local:443 2>/dev/null | \
  grep "Cipher is"
```


```text title="Expected output"
Protocol  : TLSv1.2
alert handshake failure
Cipher is ECDHE-RSA-AES256-GCM-SHA384
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `connect: Connection refused` | Verify the LCM host is running and accessible on port 443 with `ping lcm-prod-01.example.local` and `nc -zv lcm-prod-01.example.local 443`. |
    | `alert handshake failure` (appears for TLS 1.2 test instead of 1.0)` | Confirm the server's minimum TLS version is actually 1.2 by checking `/opt/vmware/vcac/server/conf/catalina.properties` or the LCM security policy. |
    | `grep: (standard input) is empty` | The openssl connection succeeded but grep found no matching line; try removing `2>/dev/null` to see the full output and verify the expected string format. |
LCM 8.x defaults to TLS 1.2 minimum. If TLS 1.0 or 1.1 must be disabled explicitly, configure this via the NGINX configuration on the LCM appliance — consult the Broadcom hardening guide for the specific configuration path for each LCM version.

---

## Pre-Change Certificate Validation Checklist

Run before replacing any certificate via LCM:

- [ ] New certificate verified: `openssl verify -CAfile chain.pem leaf.pem` — output `OK`
- [ ] Key moduli match between leaf and private key
- [ ] Private key has no passphrase
- [ ] SAN entries cover all product node FQDNs and VIP
- [ ] Certificate validity period >= 90 days from today
- [ ] Locker Master Password is accessible (in case restore is needed)
- [ ] VM snapshot of the product appliance taken before replacement
- [ ] Old certificate alias retained in Locker for rollback reference (do not delete until new cert is confirmed working)
