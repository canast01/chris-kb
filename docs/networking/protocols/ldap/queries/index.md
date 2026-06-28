---
tags:
  - networking
---
# LDAP Queries

<div class="kb-summary">
LDAP Queries reference covering Overview, Filter Syntax, Common AD Attributes, PowerShell: Get-ADObject, Search Scope and Base and 1 more sections.
</div>

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
