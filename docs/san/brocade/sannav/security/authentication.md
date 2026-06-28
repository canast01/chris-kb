---
tags:
  - san
  - security
---
# Brocade SANnav — Authentication
![Brocade SANnav — Authentication](../../../../assets/san-brocade-sannav-security-authentication.svg)

```bash
# Copy CA cert to SANnav appliance
scp corp-ca.crt admin@sannav-dc1.corp.example.com:/tmp/

# SSH to appliance and import
ssh admin@sannav-dc1.corp.example.com

# Import CA certificate into Java truststore used by SANnav
sudo keytool -import -trustcacerts -alias corp-ldap-ca \
  -file /tmp/corp-ca.crt \
  -keystore /opt/sannav/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart SANnav to pick up new truststore
sudo sannav restart
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Sannav — Access Control](../access-control/)
- [Sannav — Hardening](../hardening/)
- [Sannav — Encryption](../encryption/)
