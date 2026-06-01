# Nexus Dashboard — Encryption

> Part of the [Nexus Dashboard](../../index.md) reference.

---

## Overview

Nexus Dashboard encrypts all management traffic in transit using TLS. Sensitive configuration data (credentials, LDAP bind passwords) is encrypted at rest. This page covers TLS configuration, credential storage, backup encryption, and certificate management.

---

## Data in Transit

### Web UI and REST API (HTTPS)

All browser and API access uses HTTPS (TLS 1.2 minimum, TLS 1.3 preferred). The ND Nginx ingress handles TLS termination.

#### Verify TLS Version and Ciphers

```bash
# Check TLS version accepted
openssl s_client -tls1 -connect nd-dc1.corp.example.com:443 </dev/null 2>&1 | grep "alert\|Cipher"
# Expected: alert handshake failure (TLS 1.0 rejected)

openssl s_client -tls1_3 -connect nd-dc1.corp.example.com:443 </dev/null 2>&1 | grep "Protocol"
# Expected: Protocol: TLSv1.3

# Enumerate ciphers (requires nmap)
nmap --script ssl-enum-ciphers -p 443 nd-dc1.corp.example.com
# Acceptable: ECDHE+AESGCM, ECDHE+CHACHA20; No RC4, DES, 3DES, NULL
```
┌───────────────────────────── Cisco Nexus Dashboard — Security Encryption ─────────────────────────────┐
│                                                                                                       │
│  TLS for all management interfaces; AES-256 for backup data and secrets at rest.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            In-Transit Encryption             │  │              At-Rest Encryption             │   │
│   │         HTTPS: TLS 1.2+ on port 443          │  │             Backup: AES-256-GCM             │   │
│   │         Inter-node: mTLS cluster bus         │  │           Secrets: etcd encrypted           │   │
│   │          Syslog: TLS transport opt.          │  │           Passwords: bcrypt hashed          │   │
│   │           API: TLS cert validation           │  │          Keys: stored in K8s secret         │   │
│   │          Disable TLS 1.0/1.1 + RC4           │  │        Disk: OS-level encryption opt        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  All external traffic TLS 1.2+; inter-node cluster traffic uses mutual TLS                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │                  Compliance                 │   │
│   │         Default: self-signed on init         │  │          FIPS 140-2 mode: optional          │   │
│   │        Replace: upload CA-signed cert        │  │         Cipher suite: AES-GCM pref.         │   │
│   │         SAN: cluster VIP + hostnames         │  │         TLS 1.3: supported on newer         │   │
│   │          Expiry alert: UI + syslog           │  │         Audit: TLS handshake errors         │   │
│   │           Auto-renew: not built-in           │  │         Annual cipher review policy         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · CA server · management switch · backup storage target                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  mTLS           = Mutual TLS; both client and server present certificates                             │
│  AES-256-GCM    = Symmetric cipher providing confidentiality + integrity for backups                  │
│  etcd encrypted = Kubernetes encrypts secret objects in etcd using AES-CBC/GCM                        │
│  K8s secret     = Kubernetes object storing sensitive data (keys, tokens, passwords)                  │
│  FIPS 140-2     = US federal crypto module standard; disables non-compliant algos                     │
│  SAN cert       = TLS cert with Subject Alternative Names for VIP and all node FQDNs                  │
│  Self-signed    = Default ND cert; must be replaced with CA-signed for production                     │
│  Bcrypt         = One-way hash for passwords; not reversible even with DB access                      │
│  TLS 1.3        = Latest TLS version; eliminates weak handshake options                               │
│  Cipher suite   = Negotiated algorithm set: key exchange + auth + encryption + hash                   │
│  Auto-renew     = ND does not auto-renew certs; monitor expiry and replace manually                   │
│  Disk encryption= OS-level feature (LUKS) optional on bare-metal ND deployments                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### ND to Managed Switch Communication (SSH and SNMP)

NDFC uses SSH (port 22) for all configuration push operations to MDS switches. Ensure:
- SSH v2 enforced on managed switches: `show ssh server` on each MDS
- RSA keys ≥ 2048-bit: `show crypto key mypubkey rsa` on each MDS
- NDFC stores switch host keys on first connection; if a switch is replaced, remove the old host key from NDFC: **NDFC > Fabrics > [Fabric] > Edit Switch > Reset Host Key**

SNMP polling uses SNMPv3 with `authPriv` (SHA auth + AES-128 priv). Configure on managed switches per the [Design Standards](../../architecture/design-standards/index.md) page.

### ND Cluster Internal Communication

Inter-node cluster communication (Kubernetes, etcd, Kafka) uses mutual TLS (mTLS) with internally managed certificates. These are managed automatically by ND and do not require operator attention under normal circumstances.

### LDAP Traffic

Use port 636 (LDAPS) for all LDAP connections. Import the corporate CA certificate to ensure proper trust chain validation. Never use plain LDAP port 389 in production — it transmits bind credentials in cleartext.

---

## Data at Rest

### Stored Credentials

ND stores the following sensitive data encrypted at rest in its internal database (Keycloak + PostgreSQL):
- LDAP bind DN password
- TACACS+ shared key
- Switch SSH usernames and passwords (via NDFC)
- SNMPv3 auth and priv passwords (via NDFC)
- SMTP authentication credentials
- Backup encryption passphrase

Encryption keys are managed by the ND platform's internal key management service (Vault). Keys are tied to the cluster instance and are included in cluster backups.

### Kubernetes Secret Encryption

ND stores application credentials and configuration in Kubernetes Secrets. Kubernetes Secrets are base64-encoded by default, but ND enables etcd encryption at rest for Secrets using AES-GCM:

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Verify etcd encryption is enabled (should be configured by ND platform)
kubectl get secret -n kube-system encryptionconfig -o yaml 2>/dev/null | grep -i "aes\|secretbox"
# Expected: encryption configuration present
```

### Backup Encryption

ND backups are encrypted with a passphrase using AES-256 when encryption is enabled. Configure under **Admin Console > Operations > Backup > Settings > Enable Encryption**:

1. Set a strong encryption passphrase (20+ characters, stored in vault).
2. Click **Save**.

**Critical:** The passphrase is required at restore time. Without it, the backup cannot be decrypted. Store the passphrase in vault immediately after setting it.

```bash
# The passphrase can also be set via CLI
acs backup settings --encryption-passphrase-file /home/ndadmin/.nd-backup-pass
```

### VM-Level Disk Encryption

The ND nodes' local storage is not encrypted at the OS level by default. Add encryption at the hypervisor layer:
- **VMware**: enable vSphere VM Encryption on the ND VM datastore. This encrypts all VM disks including the ND data volumes.
- **Physical appliance**: the Cisco UCS C220 M6 appliance supports self-encrypting drives (SED) with Cisco SafeStore.

---

## Certificate Expiry Monitoring

Track the ND UI certificate expiry to ensure renewal well before expiry:

```bash
# Check certificate expiry
openssl s_client -connect nd-dc1.corp.example.com:443 \
  -servername nd-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# Days until expiry
python3 -c "
from datetime import datetime
import subprocess, re
r = subprocess.run(['openssl','s_client','-connect','nd-dc1.corp.example.com:443',
  '-servername','nd-dc1.corp.example.com'], capture_output=True, input=b'')
c = subprocess.run(['openssl','x509','-noout','-enddate'],
  input=r.stdout, capture_output=True).stdout.decode()
d = re.search(r'notAfter=(.*)', c).group(1).strip()
exp = datetime.strptime(d, '%b %d %H:%M:%S %Y %Z')
print(f'Certificate expires in {(exp - datetime.utcnow()).days} days ({exp.date()})')
"
# Alert when < 60 days remaining; renew by < 30 days
```

Add this check to the weekly health check procedure and configure monitoring alerts for certificate expiry.

---

## Encryption Summary

| Data Category | Encryption | Standard |
|---|---|---|
| Web UI / REST API traffic | TLS 1.2/1.3 (HTTPS port 443) | Nginx ingress |
| Switch management (NDFC) | SSH v2 | RSA 2048+ |
| LDAP authentication traffic | TLS (LDAPS port 636) | |
| SNMP polling traffic | AES-128 (SNMPv3 authPriv) | |
| Cluster inter-node traffic | mTLS (mutual TLS) | Kubernetes / etcd |
| Stored credentials (DB) | AES-GCM (Kubernetes Secrets + etcd encryption) | ND internal key mgmt |
| Backup archives | AES-256 (passphrase-based) | ND backup encryption |
| VM disks | vSphere VM Encryption or SED | Hypervisor / hardware |
