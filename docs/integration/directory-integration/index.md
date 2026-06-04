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
```text
┌──────────────────── Integration — Directory Integration (LDAP / Active Directory) ────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Integrate infrastructure services with Active Directory via LDAPS for authentication     │   │
│   │      Service account: dedicated bind account; read-only to OU; password rotation tracked      │   │
│   │        Required: LDAPS (port 636) only; import AD CA cert; test bind before production        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 LDAP Config                  │  │               Troubleshooting               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            Server: DC IP or FQDN             │  │             ldapsearch bind test            │   │
│   │              Port: 636 (LDAPS)               │  │           Check CA in trust store           │   │
│   │           Bind DN: svc-ldap@domain           │  │        Verify service acct not locked       │   │
│   │          Base DN: DC=corp,DC=local           │  │         Check OU search permissions         │   │
│   │            Group filter: memberOf            │  │           AD event log: 4771/4776           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Bind DN      = Distinguished Name of service account used to authenticate to LDAP                  │
│    Base DN      = Search root in directory tree; e.g. DC=corp,DC=local for full domain                │
│    LDAPS        = LDAP over TLS port 636; required; plain LDAP (389) transmits creds in clear         │
│    memberOf     = AD attribute listing group DNs; used for group-based role mapping                   │
│    ldapsearch   = CLI tool to test LDAP queries; confirm bind and attribute retrieval                 │
│    Event 4776   = AD credential validation attempt; logged on DC; useful for bind failures            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
