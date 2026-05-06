# Active Directory Standards

OU structure follows a geographic or functional top-level layout (e.g., OU=Servers,OU=EMEA) to enable scoped GPO application and delegation. Group naming uses prefixes to indicate scope: `GG_` for Global groups, `DL_` for Domain Local groups, and `U_` for user accounts; service accounts follow the `svc-appname` convention. GPO names use the pattern `ENV-SCOPE-PURPOSE` (e.g., `PROD-SERVERS-SecBaseline`), and fine-grained Password Settings Objects (PSOs) override the domain default for privileged and service accounts.

| Standard | Value |
|---|---|
| Service account prefix | `svc-appname` |
| Global group prefix | `GG_` |
| Domain local group prefix | `DL_` |
| GPO naming | `ENV-SCOPE-PURPOSE` |
| Domain default password min length | 14 characters |
| Kerberos TGT lifetime | 10 hours |
| Kerberos max renewal | 7 days |
| PSO for service accounts | 90-day max age, 20-char minimum |
