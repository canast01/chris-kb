# Brocade SANnav — Encryption

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
```text
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
