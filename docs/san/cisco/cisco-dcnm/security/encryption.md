---
tags:
  - san
  - security
---
# Cisco DCNM — Encryption
![Cisco DCNM — Encryption](../../../../assets/san-cisco-cisco-dcnm-security-encryption.svg)


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

```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Cisco DCNM Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Cisco Dcnm — Hardening](hardening/)
- [Cisco Dcnm — Authentication](authentication/)
- [Cisco Dcnm — Access Control](access-control/)
