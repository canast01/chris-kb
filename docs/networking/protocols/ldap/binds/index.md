---
tags:
  - networking
---
# LDAP Binds

<div class="kb-summary">
LDAP Binds reference covering Overview, Simple Bind, SASL / Kerberos Bind, Service Account Bind Configuration, Anonymous Bind Risks and 1 more sections.
</div>

## Overview

A bind is how an LDAP client authenticates to a directory server. The bind operation establishes the identity used for subsequent queries. Choosing the wrong bind method exposes credentials or fails entirely in hardened environments.

| Bind Type | Auth Method | Use Case |
|---|---|---|
| Anonymous | None | Public directory queries (if permitted) |
| Simple | DN + password (cleartext) | Service accounts over LDAPS only |
| SASL GSSAPI | Kerberos ticket | Preferred for AD environments |
| SASL DIGEST-MD5 | Hashed password | Legacy; avoid in new deployments |
| NTLM (SASL GSS-SPNEGO) | NTLM token | Windows clients without Kerberos |

## Simple Bind

Simple bind sends the Distinguished Name (DN) and password in plaintext (base64 encoded, not encrypted). Always use LDAPS (port 636) or StartTLS with simple bind.

```bash
# Test simple bind with ldapsearch
ldapsearch -H ldap://dc01.corp.example.com \
           -D "CN=svc-ldap,OU=Service Accounts,DC=corp,DC=example,DC=com" \
           -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           "(objectClass=user)" cn

# Bind using LDAPS (encrypted)
ldapsearch -H ldaps://dc01.corp.example.com:636 \
           -D "CN=svc-ldap,OU=Service Accounts,DC=corp,DC=example,DC=com" \
           -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           "(sAMAccountName=jsmith)" cn mail
```

## SASL / Kerberos Bind

SASL with GSSAPI uses a Kerberos ticket, avoiding password exposure. This is the preferred method for Active Directory.

```bash
# Obtain Kerberos ticket first
kinit svc-ldap@CORP.EXAMPLE.COM

# Bind using existing Kerberos ticket (GSSAPI / SASL)
ldapsearch -H ldap://dc01.corp.example.com \
           -Y GSSAPI \
           -b "DC=corp,DC=example,DC=com" \
           "(objectClass=organizationalUnit)" ou

# Check current Kerberos tickets
klist
```

## Service Account Bind Configuration

Service accounts used for LDAP bind should be dedicated, low-privilege accounts.

```powershell
# Create a dedicated service account in AD
New-ADUser -Name "svc-ldap" `
           -SamAccountName "svc-ldap" `
           -UserPrincipalName "svc-ldap@corp.example.com" `
           -AccountPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) `
           -PasswordNeverExpires $true `
           -Enabled $true `
           -Path "OU=Service Accounts,DC=corp,DC=example,DC=com"

# Grant only read access to the directory (deny write by default via AD defaults)
# Set delegation: right-click OU > Delegate Control > Read all user info
```

## Anonymous Bind Risks

Anonymous bind allows queries without authentication. In Active Directory, anonymous bind is disabled by default since Windows Server 2003.

```bash
# Test whether anonymous bind is permitted
ldapsearch -H ldap://dc01.corp.example.com \
           -x \
           -b "DC=corp,DC=example,DC=com" \
           "(objectClass=*)" dn 2>&1 | head -20

# If anonymous access returns results, enforce restriction on the DC:
# HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters
# "DSHeuristics" value — see KB 326690
```

## Bind Test Checklist

```bash
# 1. Resolve the DC name
nslookup dc01.corp.example.com

# 2. Test port reachability
nc -zv dc01.corp.example.com 389
nc -zv dc01.corp.example.com 636

# 3. Test simple bind
ldapsearch -H ldap://dc01.corp.example.com -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "" -s base "(objectClass=*)" supportedSASLMechanisms

# 4. Check supported SASL mechanisms
ldapsearch -H ldap://dc01.corp.example.com -x \
           -b "" -s base "(objectClass=*)" supportedSASLMechanisms
```
