---
tags:
  - networking
description: "LDAP Binds reference covering Overview, Simple Bind, SASL / Kerberos Bind, Service Account Bind Configuration, Anonymous Bind Risks and 1 more sections."
---
# LDAP Binds

<div class="kb-summary">
LDAP Binds reference covering Overview, Simple Bind, SASL / Kerberos Bind, Service Account Bind Configuration, Anonymous Bind Risks and 1 more sections.
</div>

```d2
direction: down

simple_bind: "Simple Bind" {shape: rectangle}
sasl_kerberos_bind: "SASL / Kerberos Bind" {shape: rectangle}
service_account_bind_configuration: "Service Account Bind Configuration" {shape: rectangle}
anonymous_bind_risks: "Anonymous Bind Risks" {shape: rectangle}
bind_test_checklist: "Bind Test Checklist" {shape: rectangle}

simple_bind -> sasl_kerberos_bind: uses
sasl_kerberos_bind -> service_account_bind_configuration: uses
service_account_bind_configuration -> anonymous_bind_risks: uses
anonymous_bind_risks -> bind_test_checklist: uses
```

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


```text title="Expected output"
# LDAP_CONOPT_TIMEOUT=30000
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (objectClass=user)
# requesting: cn
#

# search result
search: 2
result: 0 Success

# numResponses: 127
# numEntries: 126

dn: CN=jsmith,OU=Users,DC=corp,DC=example,DC=com
cn: John Smith

dn: CN=mchen,OU=Users,DC=corp,DC=example,DC=com
cn: Michelle Chen

dn: CN=agarcia,OU=Users,DC=corp,DC=example,DC=com
cn: Angela Garcia

# LDAPS bind successful
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (sAMAccountName=jsmith)
# requesting: cn mail
#

dn: CN=jsmith,OU=Users,DC=corp,DC=example,DC=com
cn: John Smith
mail: jsmith@corp.example.com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_bind: Invalid credentials (49)` | Verify the service account password is correct and the account is not locked; check DC logs with `Get-EventLog -LogName Security -InstanceId 4771 -Newest 10` on the domain controller. |
    | `Can't contact LDAP server (-1)` | Ensure the DC hostname resolves with `nslookup dc01.corp.example.com` and port 389/636 is reachable via `nc -zv dc01.corp.example.com 636`. |
    | `TLS/SSL error: certificate verify failed` | Add the DC's CA certificate to the system trust store with `sudo cp ca.crt /etc/ssl/certs/ && sudo update-ca-certificates` or disable verification temporarily with `-o LDAPTLS_REQCERT=never`. |
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


```text title="Expected output"
Password for svc-ldap@CORP.EXAMPLE.COM: 
# extended LDIF
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (objectClass=organizationalUnit)
# requesting: ou

# Users, corp.example.com
dn: OU=Users,DC=corp,DC=example,DC=com
ou: Users

# Computers, corp.example.com
dn: OU=Computers,DC=corp,DC=example,DC=com
ou: Computers

# Groups, corp.example.com
dn: OU=Groups,DC=corp,DC=example,DC=com
ou: Groups

# search result
search: 2
result: 0 Success

# numResponses: 4
# numEntries: 3

Ticket cache: FILE:/tmp/krb5cc_0
Default principal: svc-ldap@CORP.EXAMPLE.COM

Valid starting       Expires              Service principal
01/15/2025 09:22:13  01/15/2025 19:22:13  krbtgt/CORP.EXAMPLE.COM@CORP.EXAMPLE.COM
01/15/2025 09:22:45  01/15/2025 19:22:13  ldap/dc01.corp.example.com@CORP.EXAMPLE.COM
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)` | Verify the DC hostname resolves and is reachable on port 389 with `nslookup dc01.corp.example.com` and `nc -zv dc01.corp.example.com 389`. |
    | `GSSAPI Error: Unspecified GSS failure. Minor code may provide more information` | Ensure a valid Kerberos ticket exists with `klist` and the service principal `ldap/dc01.corp.example.com@CORP.EXAMPLE.COM` is registered in Active Directory. |
    | `kinit: Client not found in Kerberos database while getting initial credentials` | Confirm the service account `svc-ldap@CORP.EXAMPLE.COM` exists in the KDC and the realm name matches your domain exactly. |
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


```text title="Expected output"
# LDAP anonymous bind test
dn: DC=corp,DC=example,DC=com
dn: CN=Users,DC=corp,DC=example,DC=com
dn: CN=Computers,DC=corp,DC=example,DC=com
dn: CN=Domain Controllers,DC=corp,DC=example,DC=com
dn: CN=Administrator,CN=Users,DC=corp,DC=example,DC=com
dn: CN=Guest,CN=Users,DC=corp,DC=example,DC=com
dn: CN=KRBTGT,CN=Users,DC=corp,DC=example,DC=com
dn: CN=Domain Admins,CN=Users,DC=corp,DC=example,DC=com
dn: CN=Domain Users,CN=Users,DC=corp,DC=example,DC=com
dn: CN=Domain Guests,CN=Users,DC=corp,DC=example,DC=com
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_bind: Invalid credentials (49)` | Verify the DC hostname is reachable and anonymous binds are not already restricted; test with `-D "CN=admin,CN=Users,DC=corp,DC=example,DC=com" -W` to confirm the server is responding. |
    | `Can't contact LDAP server (-1)` | Ensure the DC hostname resolves correctly and port 389 is accessible from your client; test with `ping dc01.corp.example.com` and `nc -zv dc01.corp.example.com 389`. |
    | `ldapsearch: command not found` | Install the ldap-utils package with `apt-get install ldap-utils` (Debian/Ubuntu) or `yum install openldap-clients` (RHEL/CentOS). |
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


```text title="Expected output"
Server:		10.0.1.50
Address:	10.0.1.50#53

Name:	dc01.corp.example.com
Address: 10.0.1.100

Connection to dc01.corp.example.com 389 port [tcp/ldap] succeeded!
Connection to dc01.corp.example.com 636 port [tcp/ldaps] succeeded!

# extended LDIF
#
# LDAPv3
# base <> with scope baseObject
# filter: (objectClass=*)
# requesting: supportedSASLMechanisms
#

#
dn:
supportedSASLMechanisms: GSSAPI
supportedSASLMechanisms: GSS-SPNEGO
supportedSASLMechanisms: EXTERNAL
supportedSASLMechanisms: DIGEST-MD5
supportedSASLMechanisms: CRAM-MD5

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_bind: Invalid credentials (49)` | Verify the service account password is correct and the account is not locked; check DC event logs for failed bind attempts. |
    | `Can't contact LDAP server (-1)` | Confirm DNS resolution works, firewall allows ports 389/636 to the DC, and the DC hostname is reachable via `ping dc01.corp.example.com`. |
    | `Connection refused` | Verify LDAP service is running on the DC with `systemctl status slapd` (Linux) or check Active Directory is operational on Windows DC. |