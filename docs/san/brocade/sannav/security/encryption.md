---
tags:
  - san
  - security
---
# Brocade SANnav — Encryption
![Brocade SANnav — Encryption](../../../../assets/san-brocade-sannav-security-encryption.svg)

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

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Sannav — Hardening](hardening/)
- [Sannav — Authentication](authentication/)
- [Sannav — Access Control](access-control/)
