# Active Directory Security

Active Directory security is built around the three-tier admin model: Tier 0 accounts have access only to identity infrastructure (DCs, AD, PKI, PAM); Tier 1 accounts manage servers; Tier 2 accounts manage workstations and end-user resources, with no lateral movement permitted between tiers. Privileged Access Workstations (PAWs) enforce that Tier 0 and Tier 1 admin sessions originate only from hardened, dedicated hosts that cannot browse the internet or receive email. LDAP signing and channel binding must be enforced at DC level to prevent relay attacks, and Kerberos should be restricted to AES-256 encryption only by disabling RC4 and DES via GPO.

| Control | Implementation |
|---|---|
| Tier model | Tier 0/1/2 via GPO logon restrictions and RBAC in CyberArk |
| Protected Users group | Disables NTLM, DES, RC4, unconstrained delegation for members |
| AdminSDHolder | ACL template propagated hourly to all protected accounts |
| PAW | Dedicated hardened workstations; Tier 0 access only from Tier 0 PAW |
| LDAP signing | `Domain Controller: LDAP server signing requirements` = Require signing |
| LDAP channel binding | `Domain Controller: LDAP server channel binding token requirements` = Always |
| Kerberos AES-256 only | Disable RC4 HMAC via `Network security: Configure encryption types allowed for Kerberos` |
| Fine-grained PSO | Stricter policies for service accounts and admin accounts via ADSI Edit |
| Defender for Identity | Sensor on all DCs; lateral movement, pass-the-hash, and DCSync alerting |
