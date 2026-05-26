# SANnav — Encryption

> Part of the [SANnav](../../index.md) reference.

---

## Overview

SANnav encrypts data in transit using TLS and encrypts sensitive stored data (switch credentials, LDAP bind passwords) at rest using AES encryption. This page covers the configuration and verification of both.

---

## Data in Transit

### Web UI and REST API (HTTPS)

All browser access and REST API calls use HTTPS (TLS 1.2 minimum; TLS 1.3 preferred). The NGINX front-end handles TLS termination.

#### Replace the Default Self-Signed Certificate

```bash
ssh admin@sannav-dc1.corp.example.com

# Generate a 4096-bit RSA key and CSR
openssl req -new -newkey rsa:4096 -nodes \
  -keyout /tmp/sannav.key \
  -out /tmp/sannav.csr \
  -subj "/CN=sannav-dc1.corp.example.com/OU=Infrastructure/O=Corp/C=AU" \
  -addext "subjectAltName=DNS:sannav-dc1.corp.example.com,IP:10.10.5.20"

# Submit /tmp/sannav.csr to your CA
# After receiving sannav.crt (and any intermediate certs):

cat sannav.crt intermediate-ca.crt > /tmp/sannav-bundle.crt

sudo install -m 640 /tmp/sannav.key    /opt/sannav/conf/ssl/server.key
sudo install -m 644 /tmp/sannav-bundle.crt /opt/sannav/conf/ssl/server.crt

# Reload NGINX without service interruption
sudo systemctl reload nginx

# Verify the new certificate is served
openssl s_client -connect sannav-dc1.corp.example.com:443 -servername sannav-dc1.corp.example.com \
  </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```
┌───────────────────────────────────── Brocade SANnav — Encryption ─────────────────────────────────────┐
│                                                                                                       │
│  SANnav encryption: TLS 1.2/1.3 for all management traffic; DB and log encryption at rest.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Management Traffic Encryption         │  │           Data at Rest Encryption           │   │
│   │          HTTPS: TLS 1.2/1.3 for GUI          │  │        PostgreSQL: encrypted volumes        │   │
│   │           REST API: HTTPS port 443           │  │           OS-level: dm-crypt/LUKS           │   │
│   │         SNMPv3: AES-128 privacy mode         │  │          Log files: filesystem enc          │   │
│   │        syslog: TLS-encrypted forward         │  │         Backup: encrypted NFS files         │   │
│   │       Disable HTTP: redirect to HTTPS        │  │           Audit trail: append-only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  TLS secures all management channels; disk encryption protects data if VM is extracted.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │              Protocol Hardening             │   │
│   │       Replace default self-signed cert       │  │          Disable TLS 1.0/1.1 + SSL          │   │
│   │         CA-signed cert for prod GUI          │  │          Cipher: AES-GCM preferred          │   │
│   │         Certificate renewal reminder         │  │          HSTS header: enforce HTTPS         │   │
│   │         PKCS#12 import via admin CLI         │  │          Disable weak SNMP strings          │   │
│   │        Annual rotation before expiry         │  │          SSH: key-based admin only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav Linux VM · vSphere encrypted datastore · PKI CA for cert issuance                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.3         = Transport Layer Security 1.3; forward secrecy; preferred version                   │
│  REST API HTTPS   = all SANnav API calls over port 443; token in Authorization header                 │
│  SNMPv3 privacy   = AES-128 encryption of SNMP PDU payload; auth + privacy mode                       │
│  dm-crypt/LUKS   = Linux kernel disk encryption; used for SANnav VM data volumes                      │
│  PostgreSQL enc   = database files on encrypted volume; prevents offline data access                  │
│  Audit trail      = append-only event log; tampering detectable via log integrity check               │
│  PKCS#12         = certificate format; bundles cert + private key for import                          │
│  HSTS            = HTTP Strict Transport Security; forces HTTPS for all future requests               │
│  AES-GCM         = AES Galois/Counter Mode; authenticated encryption cipher suite                     │
│  Self-signed cert = default SANnav cert; replace with CA-signed cert in production                    │
│  CA-signed cert   = TLS certificate issued by internal or public CA; trusted by browsers              │
│  syslog TLS       = encrypted syslog; audit and event logs forwarded securely to SIEM                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### SANnav to Switch Communication

SANnav communicates with switches via HTTPS (FOS REST API). This is encrypted by default and uses the switch's self-signed certificate. SANnav trusts switch certificates by hostname/IP matching rather than full chain verification by default — an acceptable trade-off for closed management networks.

If the switch has a certificate from the corporate CA, it can be imported into the SANnav truststore for full verification.

### SANnav to LDAP (LDAPS)

Configure port 636 (LDAPS) rather than 389 (plain LDAP) to encrypt LDAP traffic. See [Authentication](../authentication/index.md) for CA certificate import steps.

### SNMP

SNMP v3 with `authPriv` security level encrypts SNMP traffic. Configure SNMPv3 on all managed switches using AES-128 or AES-256 for encryption. See the [Design Standards](../../architecture/design-standards/index.md) page for switch-side SNMP configuration.

---

## Data at Rest

### Stored Credentials

SANnav stores the following sensitive data in its PostgreSQL database, encrypted at rest using AES-256:
- Switch HTTPS usernames and passwords
- SNMPv3 auth and priv passwords
- LDAP bind DN password
- SMTP authentication credentials
- Webhook signing keys

Encryption keys are managed internally by SANnav and are stored in a protected keystore on the appliance. The keystore is tied to the appliance instance and is included in full backups (which are also encrypted).

### Database-Level Encryption

The embedded PostgreSQL database does not use full-disk encryption by default. To add a layer of protection for the appliance storage:

- Deploy the SANnav VM on a VMware datastore with vSphere VM Encryption enabled, or
- Use Linux LUKS full-disk encryption on the underlying VM disk (requires custom deployment)

For most environments, the combination of field-level AES encryption of credentials and physical/hypervisor access controls is sufficient.

### Backup Encryption

Enable backup encryption to protect backup archives in transit and at rest on the backup target:

1. Navigate to **Administration > Backup > Settings**.
2. Enable **Encrypt Backup**.
3. Set a strong backup encryption passphrase (store in vault — required for restore).

Encrypted backups use AES-256. The passphrase is required at restore time; without it, the backup cannot be decrypted.

---

## Certificate Expiry Monitoring

Track SANnav's TLS certificate expiry:

```bash
# Check certificate expiry from the command line
openssl s_client -connect sannav-dc1.corp.example.com:443 \
  -servername sannav-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate
# notAfter=Aug 12 00:00:00 2026 GMT

# Check days until expiry
python3 -c "
from datetime import datetime
import subprocess, re
result = subprocess.run(['openssl','s_client','-connect','sannav-dc1.corp.example.com:443',
  '-servername','sannav-dc1.corp.example.com'], capture_output=True, input=b'')
cert_pem = subprocess.run(['openssl','x509','-noout','-enddate'], 
  input=result.stdout, capture_output=True).stdout.decode()
date_str = re.search(r'notAfter=(.*)', cert_pem).group(1).strip()
exp = datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
days = (exp - datetime.utcnow()).days
print(f'Certificate expires in {days} days ({exp.date()})')
"
```

Renew the SANnav certificate at least 30 days before expiry. A Nagios/Icinga check on port 443 with `--certificate` flag provides automated alerting.

---

## Encryption Summary

| Data Category | Encryption | Standard |
|---|---|---|
| Web UI / REST API traffic | TLS 1.2/1.3 | HTTPS on port 443 |
| Switch management traffic | TLS (HTTPS) | FOS REST API |
| LDAP authentication traffic | TLS (LDAPS) | Port 636 |
| SNMP traffic | AES-128 (authPriv) | SNMPv3 |
| Stored credentials (DB) | AES-256 | SANnav internal keystore |
| Backup archives | AES-256 | Passphrase from vault |
| SANnav OS disk | VM encryption (hypervisor layer) | vSphere or LUKS |
