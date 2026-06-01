# LDAP Troubleshooting


<div class="kb-summary">
LDAP Troubleshooting reference covering Overview, Bind Failure Diagnostics, Certificate Errors, Using ldp.exe (Windows GUI Tool), LDAP Referrals and 1 more sections.
</div>

```text
        TRIAGE: LDAP BIND FAILS
┌──────────────────────────────────────────────────────────────┐
│  1. Resolve DC name                                          │
│     nslookup dc01.example.local ─── fail ──► fix DNS           │
│          │ ok                                                │
│          ▼                                                   │
│  2. Port reachable?                                          │
│     nc -zv dc01 389 ─────────── fail ──► firewall / DC down │
│     nc -zv dc01 636            (636 = LDAPS)                 │
│          │ ok                                                │
│          ▼                                                   │
│  3. Simple bind (test creds)                                 │
│     ldapsearch -x -D svc@corp -w pass ─ fail ──► check DN,  │
│          │ ok                                   password, lock│
│          ▼                                                   │
│  4. Check network: nc -zv dc01 636 (port reachable)          │
│          ▼                                                   │
│  5. TLS error? openssl s_client -connect dc01:636            │
│     cert untrusted ──────────────────────► install root CA   │
│     cert expired ────────────────────────► renew DC cert     │
│          │ ok                                                │
│          ▼                                                   │
│  6. Query returns no results? ──► check base DN, filter      │
└──────────────────────────────────────────────────────────────┘
```

## Overview

LDAP failures usually manifest as bind errors, query timeouts, certificate problems, or referrals to other directories. Identify the failure layer first: DNS, TCP connectivity, TLS, bind credentials, or query filter.

| Error | Common Cause | First Check |
|---|---|---|
| `49` Invalid credentials | Wrong DN or password | Verify DN format, account lock status |
| `32` No such object | Wrong search base or DN | Check OU structure in AD |
| `52e` Invalid credentials (AD) | Account disabled or locked | `Get-ADUser -Identity` check |
| Connection refused | Port closed or DC not running | `Test-NetConnection -Port 389` |
| SSL handshake failure | Cert untrusted or expired | `openssl s_client -connect :636` |
| Referral returned | Query crossed domain boundary | Use GC port 3268 instead |

## Bind Failure Diagnostics

```bash
# Test anonymous bind (check if anonymous access is allowed)
ldapsearch -H ldap://dc01.corp.example.com -x \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn

# Test simple bind with explicit DN
ldapsearch -H ldap://dc01.corp.example.com -x \
           -D "CN=svc-ldap,OU=Service Accounts,DC=corp,DC=example,DC=com" \
           -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn

# Test bind using UPN format (common for AD)
ldapsearch -H ldap://dc01.corp.example.com -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn
```

## Certificate Errors

```bash
# Check certificate presented by the LDAPS server
openssl s_client -connect dc01.corp.example.com:636 </dev/null 2>&1 | \
    grep -E "subject=|issuer=|Verify return code"

# Check certificate expiry date
openssl s_client -connect dc01.corp.example.com:636 </dev/null 2>/dev/null | \
    openssl x509 -noout -dates

# Test with certificate verification disabled (confirms cert is the problem)
LDAPTLS_REQCERT=never ldapsearch -H ldaps://dc01.corp.example.com:636 -x \
    -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
    -b "" -s base "(objectClass=*)" supportedSASLMechanisms

# Add DC CA cert to trusted store (Linux)
cp corp-root-ca.crt /usr/local/share/ca-certificates/
update-ca-certificates
```

## Using ldp.exe (Windows GUI Tool)

`ldp.exe` is built into Windows and provides a graphical interface for LDAP testing.

```powershell
# Launch ldp.exe
ldp.exe

# Steps in ldp.exe:
# 1. Connection > Connect: enter DC hostname and port (389 or 636)
# 2. Connection > Bind: enter credentials
# 3. View > Tree: set base DN to browse directory
# 4. Browse > Search: enter custom LDAP filters
```

## LDAP Referrals

Referrals occur when a DC redirects a query to another directory server (typically another domain). Use the Global Catalog to avoid cross-domain referrals.

```bash
# If ldapsearch returns referrals, add -r to follow them automatically
ldapsearch -H ldap://dc01.corp.example.com -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           -r "(objectClass=user)" cn

# Alternatively, query the GC to span the entire forest without referrals
ldapsearch -H ldap://dc01.corp.example.com:3268 -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           "(sAMAccountName=jsmith)" cn mail
```

## Event Log and Debug Logging

```powershell
# Enable LDAP interface event logging on the DC (level 2 = verbose)
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Diagnostics" `
                 -Name "16 LDAP Interface Events" -Value 2

# View LDAP events in Directory Service log
Get-WinEvent -LogName "Directory Service" -MaxEvents 50 |
    Where-Object { $_.Message -like "*LDAP*" } |
    Select-Object TimeCreated, Id, Message

# Return logging to default (1 = errors only)
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Diagnostics" `
                 -Name "16 LDAP Interface Events" -Value 1
```
