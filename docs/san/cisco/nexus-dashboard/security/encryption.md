---
tags:
  - san
  - security
---
# Cisco Nexus Dashboard — Security Encryption

*Applies to: Cisco MDS / NX-OS*
![Cisco Nexus Dashboard — Security Encryption](../../../../assets/san-cisco-nexus-dashboard-security-encryption.svg)

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


```text title="Expected output"
alert handshake failure
Cipher : (NONE)
Protocol  : TLSv1.3
Cipher    : TLS_AES_256_GCM_SHA384

Starting Nmap 7.92 ( https://nmap.org ) at 2024-01-15 14:32:18 UTC
Nmap scan report for nd-dc1.corp.example.com (10.48.12.55)
Host is up (0.024s latency).

PORT    STATE SERVICE
443/tcp open  https

| ssl-enum-ciphers:
|   TLSv1.3:
|     ciphers:
|       TLS_AES_256_GCM_SHA384 (256) - A
|       TLS_CHACHA20_POLY1305_SHA256 (256) - A
|       TLS_AES_128_GCM_SHA256 (128) - A
|   TLSv1.2:
|     ciphers:
|       ECDHE-RSA-AES256-GCM-SHA384 (256) - A
|       ECDHE-RSA-CHACHA20-POLY1305 (256) - A
|_  least strength: A

Nmap done at 2024-01-15 14:32:21 UTC; 1 IP address (1 host up) scanned in 3.12 seconds
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to load client cert` | Verify the Nexus Dashboard certificate is valid and the hostname resolves correctly with `nslookup nd-dc1.corp.example.com`. |
    | `nmap: command not found` | Install nmap with `apt-get install nmap` (Ubuntu/Debian) or `yum install nmap` (RHEL/CentOS). |
    | `Connection refused` | Confirm the Nexus Dashboard is running and port 443 is accessible from your host using `telnet nd-dc1.corp.example.com 443`. |
```bash
# The passphrase can also be set via CLI
acs backup settings --encryption-passphrase-file /home/ndadmin/.nd-backup-pass
```

```text title="Expected output"
Backup encryption passphrase settings updated successfully.
Passphrase file: /home/ndadmin/.nd-backup-pass
Encryption algorithm: AES-256-GCM
Status: Active
Last modified: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Passphrase file not found: /home/ndadmin/.nd-backup-pass` | Verify the file path exists and run `ls -la /home/ndadmin/.nd-backup-pass` to confirm permissions and location. |
    | `Error: Permission denied reading passphrase file` | Ensure the ndadmin user has read permissions on the file with `chmod 600 /home/ndadmin/.nd-backup-pass` and verify ownership. |
    | `Error: Passphrase file is empty or invalid format` | Confirm the passphrase file contains at least 8 characters and no trailing newlines by running `cat /home/ndadmin/.nd-backup-pass | wc -c`. |
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


```text title="Expected output"
notBefore=Sep 15 08:22:14 2023 GMT
notAfter=Sep 14 08:22:14 2025 GMT
Certificate expires in 287 days (2025-09-14)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to connect to nd-dc1.corp.example.com:443` | Verify the hostname resolves and the Nexus Dashboard is reachable on port 443 using `ping` or `nc -zv`. |
    | `error:0900006e:PEM routines:PEM_read_bio:no start line` | Ensure the openssl s_client connection succeeded; add `2>&1` to stderr capture to diagnose TLS handshake failures. |
    | `ValueError: time data does not match format` | The certificate date format may differ on your system; run the openssl command standalone first to verify the exact date string format. |
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Nexus Dashboard — Hardening](../hardening/)
- [Nexus Dashboard — Authentication](../authentication/)
- [Nexus Dashboard — Access Control](../access-control/)
