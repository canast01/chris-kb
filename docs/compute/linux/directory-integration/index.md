---
tags:
  - linux
---
# Integration — Directory Integration (LDAP / Active Directory)

```bash
# Install required packages (RHEL/Rocky)
dnf install -y realmd sssd adcli samba-common-tools krb5-workstation

# Install (Debian/Ubuntu)
apt-get install -y realmd sssd sssd-tools adcli samba-common-bin krb5-user

# Discover domain
realm discover corp.example.com

# Join domain (requires domain admin credentials)
realm join -U administrator corp.example.com

# Verify join
realm list
id administrator@corp.example.com
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 14 Nov 2024 09:47:22 AM UTC.
Dependencies resolved.
Installing:
 realmd                    x86_64    0.17.10-13.el9    rhel-9-appstream    185 kB
 sssd                      x86_64    2.9.1-4.el9       rhel-9-appstream    1.2 MB
 adcli                     x86_64    0.9.2-3.el9       rhel-9-appstream    98 kB
 samba-common-tools        x86_64    4.18.5-4.el9      rhel-9-appstream    542 kB
 krb5-workstation          x86_64    1.21.1-1.el9      rhel-9-appstream    876 kB

Complete! 

  corp.example.com
    type: kerberos
    realm-name: CORP.EXAMPLE.COM
    domain-name: corp.example.com
    configured: no
    server-software: active-directory
    client-software: sssd
    required-package: sssd-tools
    required-package: oddjob
    required-package: oddjob-mkhomedir
    required-package: sssd
    required-package: adcli

Password for administrator: 
 * Successfully enrolled machine in realm

corp.example.com
  type: kerberos
  realm-name: CORP.EXAMPLE.COM
  domain-name: corp.example.com
  configured: yes
  server-software: active-directory
  client-software: sssd
  enrolled-as: RHEL9-PROD-01$

uid=1234567890(administrator@corp.example.com) gid=1234567890(corp.example.com\domain users) groups=1234567890(corp.example.com\domain users),1234567891(corp.example.com\domain admins)
```

!!! warning "Common errors"
    **`realm: Couldn't resolve host: corp.example.com`** — Verify DNS resolution with `nslookup corp.example.com` and check network connectivity to the domain controller.
    **`realm join: Couldn't authenticate with kerberos: PKINIT client certificate not found`** — Ensure the domain admin account credentials are correct and the domain controller is reachable on port 88 (Kerberos).
    **`Error looking up administrator@corp.example.com - No such user`** — Run `systemctl restart sssd` to reload the SSSD cache after domain join completes.
```bash
# Allow only members of 'linux-admins' AD group to log in
realm permit -g linux-admins@corp.example.com
# Or edit /etc/sssd/sssd.conf:
# access_provider = simple
# simple_allow_groups = linux-admins@corp.example.com
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: No such realm`** — Run `realm discover corp.example.com` first to initialize the realm integration.
    **`Error: access_provider not found in [domain/corp.example.com]`** — Ensure the `[domain/corp.example.com]` section exists in `/etc/sssd/sssd.conf` before adding access_provider directives, then run `systemctl restart sssd`.
```bash
# smb.conf excerpt for AD membership
[global]
   workgroup = CORP
   realm = CORP.EXAMPLE.COM
   security = ADS
   idmap config * : range = 10000-19999
   idmap config CORP : backend = rid
   idmap config CORP : range = 1000000-1999999
   winbind use default domain = yes
   winbind enum users = no
   winbind enum groups = no

# Join
net ads join -U administrator
systemctl enable --now winbind

# Test
wbinfo -t        # check trust
wbinfo -u        # list domain users
wbinfo -g        # list domain groups
wbinfo -i <user> # get user info
```

```text title="Expected output"
Enter administrator's password: 
Using short domain name -- CORP
Joined 'WEBSERVER01' to dns domain 'corp.example.com'
Created /etc/krb5.keytab
Created /var/lib/samba/private/secrets.tdb
synchronizing passwords
Created symlink /etc/systemd/system/multi-user.target.wants/winbind.service → /etc/systemd/system/winbind.service
winbind.service is not a native service, redirecting to systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable winbind
checking the trust secret via RPC calls succeeded
CORP\jsmith
CORP\mchen
CORP\dwalker
...
CORP\Domain Admins
CORP\Domain Users
CORP\Enterprise Admins
...
uid=1000000(CORP\jsmith) gid=1000001(CORP\Domain Users) groups=1000001(CORP\Domain Users),1000002(CORP\Domain Admins)
```

!!! warning "Common errors"
    **`failed to bind to server socket -- No such file or directory`** — Ensure `/var/lib/samba` directory exists and winbind has write permissions; run `mkdir -p /var/lib/samba/private && chown root:root /var/lib/samba`.
    **`CIFS VFS: Couldn't find suitable server with type=0x20`** — Verify DNS resolves the domain controller with `nslookup corp.example.com` and check firewall allows port 389/636 to the DC.
    **`wbinfo: error looking up domain users -- WBC_ERR_DOMAIN_NOT_FOUND`** — Confirm the domain join succeeded by checking `net ads testjoin` and restart winbind with `systemctl restart winbind`.
```bash
# SSSD with LDAP provider
# /etc/sssd/sssd.conf
[domain/ldap.example.com]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldaps://ldap.example.com:636
ldap_search_base = dc=example,dc=com
ldap_default_bind_dn = cn=readonly,dc=example,dc=com
ldap_default_authtok = <bind-password>
ldap_tls_reqcert = demand
ldap_tls_cacert = /etc/ssl/certs/internal-ca.crt
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: SSSD service failed to start - TLS: TLSV1_ALERT_UNKNOWN_CA`** — Verify the CA certificate path in `ldap_tls_cacert` exists and contains the LDAP server's signing CA, then restart SSSD with `systemctl restart sssd`.
    **`LDAP connection refused on ldaps://ldap.example.com:636`** — Confirm the LDAP server hostname resolves correctly with `nslookup ldap.example.com` and that port 636 is open via `nc -zv ldap.example.com 636`.
    **`Error: Authentication failure - Invalid credentials for cn=readonly,dc=example,dc=com`** — Verify the bind DN and password are correct by testing the connection manually with `ldapsearch -x -D "cn=readonly,dc=example,dc=com" -W -H ldaps://ldap.example.com:636 -b dc=example,dc=com`.
```bash
# Test LDAP query
ldapsearch -x -H ldaps://ldap.example.com \
  -D "cn=readonly,dc=example,dc=com" -w <password> \
  -b "dc=example,dc=com" "(uid=testuser)" cn mail
```
```powershell
# Join to domain
Add-Computer -DomainName "corp.example.com" -Credential (Get-Credential) -Restart

# Verify domain membership
(Get-WmiObject Win32_ComputerSystem).Domain
nltest /dsgetdc:corp.example.com
```
```bash
# SSSD health
systemctl status sssd
sssctl domain-status corp.example.com    # shows DC used and last successful auth
sssctl cache-expire -u <username>        # force cache refresh for one user

# Kerberos ticket
klist -c                                 # show current tickets
kinit <user>@CORP.EXAMPLE.COM            # obtain ticket manually

# Clear SSSD cache (force re-fetch from DC)
sssctl cache-remove -y && systemctl restart sssd

# Winbind
wbinfo --ping-dc                         # check DC reachable
net ads testjoin                         # verify machine account still valid
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
