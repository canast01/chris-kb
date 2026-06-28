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

```bash
# Allow only members of 'linux-admins' AD group to log in
realm permit -g linux-admins@corp.example.com
# Or edit /etc/sssd/sssd.conf:
# access_provider = simple
# simple_allow_groups = linux-admins@corp.example.com
```
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
