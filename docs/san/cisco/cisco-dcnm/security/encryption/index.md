```bash
ssh root@dcnm-dc1.corp.example.com

# Generate private key and CSR
openssl req -new -newkey rsa:4096 -nodes \
  -keyout /tmp/dcnm.key \
  -out /tmp/dcnm.csr \
  -subj "/CN=dcnm-dc1.corp.example.com/O=Corp/C=AU" \
  -addext "subjectAltName=DNS:dcnm-dc1.corp.example.com"

# After CA returns signed certificate:
# Create PKCS12 bundle
openssl pkcs12 -export \
  -in dcnm.crt \
  -inkey /tmp/dcnm.key \
  -certfile intermediate-ca.crt \
  -name "dcnm" \
  -out /tmp/dcnm.p12 -passout pass:keystorepass

# Import into DCNM Java keystore
KEYSTORE="/usr/local/cisco/dcm/dcnm/conf/.dcnmkeystore"
keytool -importkeystore \
  -srckeystore /tmp/dcnm.p12 -srcstoretype pkcs12 -srcstorepass keystorepass \
  -destkeystore "${KEYSTORE}" -deststoretype jks \
  -deststorepass <keystore-password> -alias dcnm -noprompt

# Restart DCNM
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart

# Verify certificate
openssl s_client -connect dcnm-dc1.corp.example.com:443 \
  -servername dcnm-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -enddate
```

```text
┌─────────────────────────────────────── Cisco DCNM — Encryption ───────────────────────────────────────┐
│                                                                                                       │
│  DCNM encryption: TLS 1.2/1.3 management, SNMPv3 privacy, OS disk encryption at rest.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Management Traffic Encryption         │  │           Data at Rest Encryption           │   │
│   │          HTTPS: TLS 1.2/1.3 GUI/API          │  │           OS-level: LUKS/dm-crypt           │   │
│   │           REST API: HTTPS port 443           │  │           PostgreSQL on enc volume          │   │
│   │         SNMPv3: AES-128 privacy mode         │  │           Elasticsearch on enc vol          │   │
│   │        syslog: TLS encrypted forward         │  │           Backup: encrypted at NFS          │   │
│   │         Disable HTTP; HTTPS redirect         │  │           Audit trail: append-only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  TLS on all management channels; LUKS disk encryption protects data at rest.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │              Protocol Hardening             │   │
│   │        Replace self-signed cert day 1        │  │           Disable TLS 1.0/1.1 SSL           │   │
│   │          CA-signed cert: production          │  │          Cipher: AES-GCM preferred          │   │
│   │         PKCS#12 import via admin CLI         │  │             HSTS: enforce HTTPS             │   │
│   │         Monitor expiry: 60-day warn          │  │             Disable v1/v2c SNMP             │   │
│   │         Annual renewal: update cert          │  │          SSH key-based: admin only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM Linux VM · vSphere encrypted datastore · PKI CA for certificate issuance                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.3         = Transport Layer Security 1.3; forward secrecy; preferred version                   │
│  SNMPv3 privacy  = AES-128 encryption of SNMP PDU payload; auth + privacy mode                        │
│  LUKS            = Linux Unified Key Setup; full-disk encryption for DCNM VM volumes                  │
│  dm-crypt        = Linux kernel disk encryption subsystem; LUKS uses dm-crypt                         │
│  PostgreSQL enc  = DCNM config DB on encrypted volume; offline access blocked                         │
│  Elasticsearch enc= performance DB on encrypted volume; data protected at rest                        │
│  Audit trail     = append-only log; integrity verifiable; used for forensics                          │
│  PKCS#12         = certificate container format; bundles cert + private key                           │
│  HSTS            = HTTP Strict Transport Security; browser forces HTTPS always                        │
│  AES-GCM         = AES Galois Counter Mode; authenticated encryption cipher suite                     │
│  CA-signed cert  = TLS cert from internal or public CA; replace self-signed in prod                   │
│  syslog TLS      = encrypted syslog forwarding; audit events protected in transit                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Encrypt backup with GPG
pg_dumpall -U postgres | gzip | \
  gpg --batch --yes --passphrase-file /root/.dcnm-backup-pass \
  --symmetric --cipher-algo AES256 \
  -o /var/backup/dcnm/dcnm-db-$(date +%Y%m%d).sql.gz.gpg

# Transfer encrypted backup
scp /var/backup/dcnm/dcnm-db-$(date +%Y%m%d).sql.gz.gpg \
    bkp@backup-server.corp.example.com:/backups/dcnm/

# Decrypt (on restore)
gpg --batch --passphrase-file /root/.dcnm-backup-pass \
  --decrypt dcnm-db-20260506.sql.gz.gpg | gunzip | psql -U postgres
```
```bash
# Check DCNM certificate expiry
openssl s_client -connect dcnm-dc1.corp.example.com:443 \
  -servername dcnm-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate

# Days until expiry
python3 -c "
from datetime import datetime
import subprocess
out = subprocess.run(['openssl','s_client','-connect',
  'dcnm-dc1.corp.example.com:443','-servername','dcnm-dc1.corp.example.com'],
  capture_output=True, input=b'')
cert = subprocess.run(['openssl','x509','-noout','-enddate'],
  input=out.stdout, capture_output=True).stdout.decode()
import re
d = re.search(r'notAfter=(.*)', cert).group(1).strip()
exp = datetime.strptime(d, '%b %d %H:%M:%S %Y %Z')
print(f'Expires in {(exp-datetime.utcnow()).days} days: {exp.date()}')
"
```
