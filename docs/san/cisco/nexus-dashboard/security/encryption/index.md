---
tags:
  - san
  - security
---
# Cisco Nexus Dashboard — Security Encryption

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
```text
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
```
```bash
# The passphrase can also be set via CLI
acs backup settings --encryption-passphrase-file /home/ndadmin/.nd-backup-pass
```
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
