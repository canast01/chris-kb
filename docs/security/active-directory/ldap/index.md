# AD LDAP Queries

Active Directory exposes its directory over LDAP on port 389 (LDAPS on 636). LDAP queries are the foundation for searches, integrations, and automation against AD.

## LDAP Search Basics

Every LDAP search has four parts: base DN, scope, filter, and attributes.

| Parameter | Description | Example |
|---|---|---|
| Base DN | Starting point in the tree | `DC=corp,DC=example,DC=com` |
| Scope | base / one / sub | `sub` searches entire subtree |
| Filter | Object selector syntax | `(objectClass=user)` |
| Attributes | Fields to return | `sAMAccountName,mail` |

```bash
# Basic ldapsearch against AD (Linux/macOS)
ldapsearch -H ldap://dc01.corp.example.com \
    -D "cn=svc-ldap,ou=serviceaccounts,dc=corp,dc=example,dc=com" \
    -w 'P@ssw0rd!' \
    -b "DC=corp,DC=example,DC=com" \
    -s sub \
    "(sAMAccountName=jsmith)" \
    cn mail memberOf

# Search for all enabled users
ldapsearch -H ldap://dc01.corp.example.com \
    -D "cn=svc-ldap,ou=serviceaccounts,dc=corp,dc=example,dc=com" \
    -w 'P@ssw0rd!' \
    -b "DC=corp,DC=example,DC=com" \
    "(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))" \
    sAMAccountName displayName mail
```

## PowerShell LDAP Queries

```powershell
# Search with Get-ADObject (raw LDAP)
Get-ADObject -LDAPFilter "(objectClass=computer)" `
    -SearchBase "OU=Servers,DC=corp,DC=example,DC=com" `
    -Properties Name, OperatingSystem

# Find users with specific attributes
Get-ADUser -LDAPFilter "(&(objectClass=user)(mail=*)(department=IT))" `
    -Properties mail, department, title

# Find accounts with password never expires flag set
Get-ADUser -Filter * -Properties PasswordNeverExpires |
    Where-Object {$_.PasswordNeverExpires -eq $true} |
    Select-Object Name, SamAccountName

# Find disabled accounts
Get-ADUser -Filter {Enabled -eq $false} |
    Select-Object Name, SamAccountName, DistinguishedName
```

## Common LDAP Filters

```text
# All users
(objectClass=user)

# All enabled users
(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))

# Members of a specific group
(memberOf=CN=SG-ServerAdmins,OU=Groups,DC=corp,DC=example,DC=com)

# Accounts with SPN set (service accounts / Kerberoastable)
(&(objectClass=user)(servicePrincipalName=*))

# Computers with Windows Server OS
(&(objectClass=computer)(operatingSystem=Windows Server*))

# Objects modified in the last 7 days (100ns intervals since 1601-01-01)
(whenChanged>=20260430000000.0Z)
```

## LDAPS and Signing

```powershell
# Test LDAPS connectivity
Test-NetConnection -ComputerName dc01.corp.example.com -Port 636

# Verify LDAP channel binding / signing settings
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters" |
    Select-Object "LDAPServerIntegrity", "LdapEnforceChannelBinding"

# Check LDAP event log for bind failures
Get-WinEvent -LogName "Directory Service" |
    Where-Object {$_.Id -eq 2889} | Select-Object -First 10 TimeCreated, Message
```

## Troubleshooting LDAP Issues

```bash
# Test anonymous bind (should fail if hardening is applied)
ldapsearch -H ldap://dc01.corp.example.com -x -b "" -s base

# Test with explicit credentials and verbose output
ldapsearch -H ldap://dc01.corp.example.com -v \
    -D "cn=svc-ldap,ou=serviceaccounts,dc=corp,dc=example,dc=com" \
    -w 'P@ssw0rd!' \
    -b "DC=corp,DC=example,DC=com" "(cn=jsmith)"

# Check TLS on LDAPS port
openssl s_client -connect dc01.corp.example.com:636 -showcerts
```
