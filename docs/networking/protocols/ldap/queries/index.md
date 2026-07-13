---
tags:
  - networking
description: "LDAP Queries reference covering Overview, Filter Syntax, Common AD Attributes, PowerShell: Get-ADObject, Search Scope and Base and 1 more sections."
---
# LDAP Queries

<div class="kb-summary">
LDAP Queries reference covering Overview, Filter Syntax, Common AD Attributes, PowerShell: Get-ADObject, Search Scope and Base and 1 more sections.
</div>

```d2
direction: down

filter_syntax: "Filter Syntax" {shape: rectangle}
common_ad_attributes: "Common AD Attributes" {shape: rectangle}
powershell_getadobject: "PowerShell: Get-ADObject" {shape: rectangle}
search_scope_and_base: "Search Scope and Base" {shape: rectangle}
paging_large_result_sets: "Paging Large Result Sets" {shape: rectangle}

filter_syntax -> common_ad_attributes: uses
common_ad_attributes -> powershell_getadobject: uses
powershell_getadobject -> search_scope_and_base: uses
search_scope_and_base -> paging_large_result_sets: uses
```

## Overview

LDAP queries use a filter syntax based on RFC 4515. Filters are composed of attribute-value assertions enclosed in parentheses. Boolean operators (`&`, `|`, `!`) combine multiple assertions. Knowing the common AD attributes and search bases is essential for effective directory lookups.

| Filter | Matches |
|---|---|
| `(objectClass=user)` | All user objects |
| `(sAMAccountName=jsmith)` | Specific user by login name |
| `(mail=*)` | Objects with any email address |
| `(&(objectClass=user)(enabled=TRUE))` | Enabled users (use `userAccountControl`) |
| `(memberOf=CN=Finance,OU=Groups,DC=corp,DC=example,DC=com)` | Members of a group (direct) |

## Filter Syntax

```bash
# Single attribute match
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" "(sAMAccountName=jsmith)"

# AND filter — user named jsmith with an email address
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    "(&(objectClass=user)(sAMAccountName=jsmith)(mail=*))"

# OR filter — objects that are either users or contacts
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    "(|(objectClass=user)(objectClass=contact))"

# NOT filter — all users except disabled accounts
# userAccountControl bit 2 = ACCOUNTDISABLE
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    "(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
```


```text title="Expected output"
# LDAP query 1: Single attribute match
dn: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: John Smith
sAMAccountName: jsmith
mail: jsmith@corp.example.com
userAccountControl: 512

# LDAP query 2: AND filter
dn: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: John Smith
sAMAccountName: jsmith
mail: jsmith@corp.example.com
userAccountControl: 512

# LDAP query 3: OR filter
dn: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
objectClass: user
sAMAccountName: jsmith

dn: CN=Vendor Contact,OU=Contacts,DC=corp,DC=example,DC=com
objectClass: contact
cn: Vendor Contact
...

# LDAP query 4: NOT filter (enabled users only)
dn: CN=Alice Johnson,OU=Users,DC=corp,DC=example,DC=com
objectClass: user
sAMAccountName: ajohnson
userAccountControl: 512

dn: CN=Bob Wilson,OU=Users,DC=corp,DC=example,DC=com
objectClass: user
sAMAccountName: bwilson
userAccountControl: 512
...
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account has not been locked out; test with `ldapwhoami -H ldap://dc01 -D "svc@corp.example.com" -w "pass"`.
    **`Can't contact LDAP server (-1)`** — Confirm the LDAP server hostname/IP is reachable with `ping dc01` or `nslookup dc01`, and that port 389 is open via `nc -zv dc01 389`.
    **`Malformed filter (87)`** — Check filter syntax for unmatched parentheses and proper escaping of special characters; use online LDAP filter validators to verify the query structure.
## Common AD Attributes

```bash
# Return specific attributes only (saves bandwidth)
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    "(objectClass=user)" cn sAMAccountName mail userPrincipalName memberOf

# Find all groups a user belongs to (recursive via AD memberOf)
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    "(sAMAccountName=jsmith)" memberOf

# Find all members of a group
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    "(CN=Finance Team)" member
```


```text title="Expected output"
# LDAP filter: (&(objectClass=user))
dn: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
cn: John Smith
sAMAccountName: jsmith
mail: jsmith@corp.example.com
userPrincipalName: jsmith@corp.example.com
memberOf: CN=Finance Team,OU=Groups,DC=corp,DC=example,DC=com
memberOf: CN=Domain Users,OU=Groups,DC=corp,DC=example,DC=com

dn: CN=Jane Doe,OU=Users,DC=corp,DC=example,DC=com
cn: Jane Doe
sAMAccountName: jdoe
mail: jdoe@corp.example.com
userPrincipalName: jdoe@corp.example.com
memberOf: CN=Engineering,OU=Groups,DC=corp,DC=example,DC=com
...

# LDAP filter: (sAMAccountName=jsmith)
dn: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
memberOf: CN=Finance Team,OU=Groups,DC=corp,DC=example,DC=com
memberOf: CN=Domain Users,OU=Groups,DC=corp,DC=example,DC=com
memberOf: CN=All Staff,OU=Groups,DC=corp,DC=example,DC=com

# LDAP filter: (CN=Finance Team)
dn: CN=Finance Team,OU=Groups,DC=corp,DC=example,DC=com
member: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
member: CN=Sarah Johnson,OU=Users,DC=corp,DC=example,DC=com
member: CN=Michael Chen,OU=Users,DC=corp,DC=example,DC=com
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account has not been locked out.
    **`Can't contact LDAP server (-1)`** — Confirm the DC hostname resolves and port 389 is reachable; use `nslookup dc01` and `nc -zv dc01 389` to test.
    **`No such object (32)`** — Ensure the base DN `DC=corp,DC=example,DC=com` matches your directory structure; verify with `ldapsearch -H ldap://dc01 -x -s base -b "" namingContexts`.
## PowerShell: Get-ADObject

```powershell
# Basic user lookup
Get-ADUser -Identity "jsmith" -Properties mail, memberOf, LastLogonDate

# Find all disabled users
Get-ADUser -Filter { Enabled -eq $false } -Properties DistinguishedName |
    Select-Object Name, DistinguishedName

# Raw LDAP filter with Get-ADObject
Get-ADObject -LDAPFilter "(&(objectClass=user)(mail=*@corp.example.com))" `
             -Properties sAMAccountName, mail |
    Select-Object sAMAccountName, mail

# Search with a specific search base (limit to one OU)
Get-ADUser -SearchBase "OU=Finance,DC=corp,DC=example,DC=com" `
           -Filter * -Properties Title, Department |
    Select-Object Name, Title, Department
```

## Search Scope and Base

```bash
# Scope: base (only the entry itself), one (one level below), sub (full subtree, default)
# Search base only
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" -s base "(objectClass=*)"

# One level below the search base
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" -s one "(objectClass=organizationalUnit)" ou

# Full subtree (default)
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "OU=Finance,DC=corp,DC=example,DC=com" -s sub "(objectClass=user)" cn
```


```text title="Expected output"
# LDAP query 1: base scope
dn: DC=corp,DC=example,DC=com
objectClass: top
objectClass: domain
dc: corp
distinguishedName: DC=corp,DC=example,DC=com

# LDAP query 2: one level scope
dn: OU=Finance,DC=corp,DC=example,DC=com
ou: Finance

dn: OU=IT,DC=corp,DC=example,DC=com
ou: IT

dn: OU=HR,DC=corp,DC=example,DC=com
ou: HR

# LDAP query 3: subtree scope
dn: CN=jsmith,OU=Finance,DC=corp,DC=example,DC=com
cn: jsmith

dn: CN=mchen,OU=Finance,DC=corp,DC=example,DC=com
cn: mchen

dn: CN=agarcia,OU=Finance,DC=corp,DC=example,DC=com
cn: agarcia

search result
result: 0 Success
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked; check `-D` DN and `-w` password match Active Directory.
    **`Can't contact LDAP server (-1)`** — Confirm the LDAP server hostname `dc01` is resolvable and port 389 is accessible; use `nslookup dc01` and `nc -zv dc01 389` to test connectivity.
    **`No such object (32)`** — Verify the search base DN `DC=corp,DC=example,DC=com` exists in the directory; use a base scope query first to confirm the root DN is correct.
## Paging Large Result Sets

```bash
# Enable paged results to retrieve more than 1000 objects (AD default limit)
ldapsearch -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass" \
    -b "DC=corp,DC=example,DC=com" \
    -E pr=500/noprompt \
    "(objectClass=user)" cn sAMAccountName

# PowerShell: ResultPageSize controls paging automatically
Get-ADUser -Filter * -ResultPageSize 200 -Properties mail |
    Select-Object SamAccountName, mail |
    Export-Csv -Path "C:\Temp\all_users.csv" -NoTypeInformation
```


```text title="Expected output"
# LDAP search output (first 8 results shown):
dn: CN=jsmith,OU=Users,DC=corp,DC=example,DC=com
cn: John Smith
sAMAccountName: jsmith

dn: CN=mchen,OU=Users,DC=corp,DC=example,DC=com
cn: Michelle Chen
sAMAccountName: mchen

dn: CN=dwalker,OU=Users,DC=corp,DC=example,DC=com
cn: David Walker
sAMAccountName: dwalker

dn: CN=agarcia,OU=Users,DC=corp,DC=example,DC=com
cn: Ana Garcia
sAMAccountName: agarcia

...
# search result
search: 2
result: 0 Success

# numResponses: 1247
# numEntries: 1246

# PowerShell output:
SamAccountName                             mail
--------------                             ----
jsmith                                     jsmith@corp.example.com
mchen                                      mchen@corp.example.com
dwalker                                    dwalker@corp.example.com
agarcia                                    agarcia@corp.example.com
...
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked; test with `ldapwhoami -H ldap://dc01 -x -D "svc@corp.example.com" -w "pass"`.
    **`Can't contact LDAP server`** — Confirm the DC hostname resolves and port 389 is accessible; test with `nc -zv dc01 389`.
    **`Export-Csv : Access to the path 'C:\Temp\all_users.csv' is denied`** — Ensure the directory exists and your user account has write permissions, or specify an alternative output path like `$env:TEMP\all_users.csv`.