---
tags:
  - san
  - security
---
# Cisco DCNM — Authentication
![Cisco DCNM — Authentication](../../../../assets/san-cisco-cisco-dcnm-security-authentication.svg)

```bash
ssh root@dcnm-dc1.corp.example.com

# Copy CA cert to DCNM
scp corp-ca.crt root@dcnm-dc1.corp.example.com:/tmp/

# Import into Java truststore
keytool -import -trustcacerts -alias corp-ldap-ca \
  -file /tmp/corp-ca.crt \
  -keystore /usr/java/default/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart DCNM to apply
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart
```


```text title="Expected output"
root@dcnm-dc1.corp.example.com's password: 
corp-ca.crt                                          100% 1847     1.2MB/s   00:00
Certificate was added to keystore
DCNM Server is stopping...
Stopping Tomcat...
Waiting for Tomcat to stop...
Tomcat stopped.
DCNM Server is starting...
Starting Tomcat...
Tomcat started successfully.
DCNM Server started.
```

!!! warning "Common errors"
    **`keytool error: java.lang.Exception: Input not an X.509 certificate`** — Verify the CA cert is in PEM format (not DER) and contains the `-----BEGIN CERTIFICATE-----` header.
    **`Permission denied: /usr/java/default/jre/lib/security/cacerts`** — Run the keytool command with `sudo` or as root, or check that the keystore file is writable by the current user.
    **`Connection refused` or `dcnm-server: command not found`** — Confirm DCNM is installed in `/usr/local/cisco/dcm/dcnm/` and SSH session has root privileges; check the actual installation path with `find / -name dcnm-server -type f 2>/dev/null`.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Cisco Dcnm — Access Control](../access-control/)
- [Cisco Dcnm — Hardening](../hardening/)
- [Cisco Dcnm — Encryption](../encryption/)
