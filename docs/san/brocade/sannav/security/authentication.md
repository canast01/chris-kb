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


```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "SANnav Core" {shape: hexagon}

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

- [Sannav — Access Control](access-control/)
- [Sannav — Hardening](hardening/)
- [Sannav — Encryption](encryption/)
