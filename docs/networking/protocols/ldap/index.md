---
title: LDAP
tags:
  - networking
---

# LDAP

<div class="kb-summary">
Lightweight Directory Access Protocol — directory service query and authentication for infrastructure and applications.
</div>

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="binds/">
  <strong>Binds</strong>
  <span>Binds notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="ports/">
  <strong>Ports</strong>
  <span>Ports notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="tls/">
  <strong>Tls</strong>
  <span>Tls notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic steps, and resolution guides.</span></a>
<a class="kb-card" href="queries/"><strong>Queries</strong><span>LDAP search filters, attribute queries, and ldapsearch examples.</span></a>

</div>

## Key Concepts

| Concept | Description |
|---|---|
| DN (Distinguished Name) | Full path to an object: `CN=user,OU=Users,DC=domain,DC=com` |
| BaseDN | Search starting point in the directory tree |
| Bind DN | Service account used to authenticate to LDAP |
| Filter | Search expression: `(&(objectClass=user)(sAMAccountName=user01))` |
| Attribute | Field on a directory object (e.g., `mail`, `memberOf`, `sAMAccountName`) |
| LDAPS | LDAP over TLS (port 636) — required for credential queries |
| SASL | Simple Authentication and Security Layer — Kerberos/GSSAPI bind |

## Common ldapsearch Queries

```bash
# Basic connectivity test (anonymous bind)
ldapsearch -x -H ldap://<dc-host> -b "dc=domain,dc=com" -s base "(objectclass=*)"

# Authenticated search — find a user
ldapsearch -x -H ldap://<dc-host> \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=domain,DC=com" \
  -W \
  -b "DC=domain,DC=com" \
  "(sAMAccountName=username)" \
  cn mail memberOf

# Find all members of a group
ldapsearch -x -H ldap://<dc-host> \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=domain,DC=com" \
  -W \
  -b "DC=domain,DC=com" \
  "(cn=Domain Admins)" \
  member

# List all OUs
ldapsearch -x -H ldap://<dc-host> \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=domain,DC=com" \
  -W \
  -b "DC=domain,DC=com" \
  "(objectClass=organizationalUnit)" \
  ou

# Find disabled accounts
ldapsearch -x -H ldap://<dc-host> \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=domain,DC=com" \
  -W \
  -b "DC=domain,DC=com" \
  "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))" \
  sAMAccountName
```


```text title="Expected output"
# dn: dc=domain,dc=com
# objectClass: top
# objectClass: dcObject
# objectClass: organization
# o: domain
# dc: domain

Enter LDAP Password: 
# extended LDIF
#
# LDAPv3
# base <DC=domain,DC=com> with scope baseObject
# filter: (sAMAccountName=username)
# requesting: cn mail memberOf
#

dn: CN=John Doe,OU=Users,DC=domain,DC=com
cn: John Doe
mail: john.doe@domain.com
memberOf: CN=Engineering,OU=Groups,DC=domain,DC=com
memberOf: CN=VPN-Users,OU=Groups,DC=domain,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account has not been locked out; check with `net user svc-ldap /domain` on a domain controller.
    **`ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)`** — Confirm the DC hostname resolves and port 389 is reachable; test with `nc -zv <dc-host> 389`.
    **`No such object (32)`** — Verify the base DN matches your Active Directory structure; run `ldapsearch -x -H ldap://<dc-host> -b "" -s base "(objectclass=*)" namingContexts` to confirm the correct DN.
## LDAPS Verification

```bash
# Test LDAPS connectivity
openssl s_client -connect <dc-host>:636 -showcerts

# ldapsearch over TLS
ldapsearch -H ldaps://<dc-host>:636 \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=domain,DC=com" \
  -W \
  -b "DC=domain,DC=com" \
  "(sAMAccountName=username)"

# Test LDAP StartTLS (port 389)
ldapsearch -H ldap://<dc-host>:389 -Z \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=domain,DC=com" \
  -W \
  -b "DC=domain,DC=com" \
  "(sAMAccountName=username)"
```


```text title="Expected output"
CONNECTED(00000003)
depth=0 C = US, ST = California, L = San Francisco, O = ACME Corp, CN = dc01.domain.com
verify return:1 (ok)
-----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgIUK7m8x9pQ2vL4nZ8xK9mR5c7D8+0wDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
...
-----END CERTIFICATE-----
read:errno=0

Enter LDAP Password: 
# extended LDIF
#
# LDAPv3
# base <DC=domain,DC=com> with scope subtree
# filter: (sAMAccountName=username)
# requesting: ALL
#

# username, Users, domain.com
dn: CN=username,CN=Users,DC=domain,DC=com
objectClass: person
sAMAccountName: username
mail: username@domain.com

# search result
search: 2
result: 0 Success

Enter LDAP Password: 
# extended LDIF
# base <DC=domain,DC=com> with scope subtree
# filter: (sAMAccountName=username)
# requesting: ALL
#

# username, Users, domain.com
dn: CN=username,CN=Users,DC=domain,DC=com
objectClass: person
sAMAccountName: username
mail: username@domain.com

# search result
search: 2
result: 0 Success
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account has not been locked out on the domain controller.
    **`Can't contact LDAP server (-1)`** — Confirm the DC hostname resolves correctly with `nslookup <dc-host>` and port 636/389 is accessible via `telnet <dc-host> 636`.
    **`TLS: peer certificate cannot be authenticated with known CA certificates`** — Add the DC's CA certificate to your system's trusted store or use `ldapsearch -H ldaps://<dc-host>:636 -o LDTLS_CACERTDIR=/etc/ssl/certs` to specify the certificate path.
## Application LDAP Integration (Linux PAM/SSSD)

```bash
# Check SSSD status
systemctl status sssd

# Test user lookup via SSSD
id username
getent passwd username

# Clear SSSD cache
sssctl cache-remove -y

# SSSD debug log
tail -f /var/log/sssd/sssd_<domain>.log
```


```text title="Expected output"
● sssd.service - System Security Services Daemon
     Loaded: loaded (/usr/lib/systemd/system/sssd.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
    Process: 2847 ExecStart=/usr/sbin/sssd -i (code=exited, status=0/SUCCESS)
   Main PID: 2848 (sssd)
      Tasks: 8 (limit: 4915)
     Memory: 24.3M
        CPU: 1min 23s
     CGroup: /system.slice/sssd.service
             ├─2848 /usr/sbin/sssd -i
             └─2951 /usr/libexec/sssd/sssd_nss

uid=1042(username) gid=10002(domain_users) groups=10002(domain_users),10045(engineering)
username:*:1042:10002:User Name:/home/username:/bin/bash

Clearing cache for domain 'default'...
Cache cleared successfully.

[2024-01-15 14:35:22] [sssd[be[default]]] [be_get_account_info] (0x0100): User lookup by name [username@default]
[2024-01-15 14:35:22] [sssd[nss]] [nss_cmd_getpwnam_search] (0x0400): Requesting info for user [username]
[2024-01-15 14:35:23] [sssd[be[default]]] [sdap_get_generic_op_finished] (0x0200): LDAP operation completed, result: Success
```

!!! warning "Common errors"
    **`systemctl: command not found`** — Install systemd or use `service sssd status` on systems without systemd.
    **`sssctl: command not found`** — Install sssd-tools package with `apt install sssd-tools` or `yum install sssd-tools`.
    **`tail: cannot open '/var/log/sssd/sssd_<domain>.log' for reading: No such file or directory`** — Replace `<domain>` with your actual SSSD domain name (e.g., `sssd_ldap.log`) or check `/etc/sssd/sssd.conf` for the configured domain.
## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `Invalid credentials` | Bind DN and password | Verify svc account password; confirm account not locked |
| `No such object` | BaseDN | Verify DN exists; check for typo in domain components |
| `Confidentiality required` | LDAPS/StartTLS | Application requires LDAPS — configure TLS on directory port |
| Authentication failing for all users | DC connectivity | `ping <dc>`, `nslookup <domain>` — check DNS resolution |
| SSSD not resolving users | SSSD service / cache | `systemctl restart sssd`; `sssctl cache-remove -y` |
