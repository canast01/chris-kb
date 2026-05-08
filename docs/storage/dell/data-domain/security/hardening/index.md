# Data Domain — Hardening

## Hardening Checklist

- [ ] Change the default `sysadmin` password immediately on commissioning
- [ ] Disable SSH root login: `adminaccess set ssh root disabled`
- [ ] Restrict management access to specific subnets: `adminaccess set allowed-hosts <subnet>`
- [ ] Enable HTTPS only (disable HTTP): `adminaccess set http-auth disabled`
- [ ] Configure LDAP authentication — do not rely solely on local accounts for day-to-day access
- [ ] Set a login banner: `adminaccess set login-banner "Authorised access only"`
- [ ] Set session timeout: `adminaccess set idle-timeout 15`
- [ ] Disable unused protocols (VTL, NFS, CIFS) if not in use on this system
- [ ] Restrict DD Boost client access by IP if feasible: restrict in the backup software and via network ACL
- [ ] Enable syslog forwarding to the central log collector
- [ ] Enable AutoSupport but verify no sensitive data is included in bundles
