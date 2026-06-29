---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
---
# LDAP Troubleshooting

<div class="kb-summary">
LDAP Troubleshooting reference covering Overview, Bind Failure Diagnostics, Certificate Errors, Using ldp.exe (Windows GUI Tool), LDAP Referrals and 1 more sections.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
bind_failure_diagnostics: "Bind Failure Diagnostics" {shape: rectangle}
certificate_errors: "Certificate Errors" {shape: rectangle}
using_ldpexe_windows_gui_tool: "Using ldp.exe (Windows GUI Tool)" {shape: rectangle}
ldap_referrals: "LDAP Referrals" {shape: rectangle}
event_log_and_debug_logging: "Event Log and Debug Logging" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> bind_failure_diagnostics: investigate
symptom -> certificate_errors: investigate
symptom -> using_ldpexe_windows_gui_tool: investigate
symptom -> ldap_referrals: investigate
symptom -> event_log_and_debug_logging: investigate
symptom -> verify_resolution: investigate
bind_failure_diagnostics -> resolution
certificate_errors -> resolution
using_ldpexe_windows_gui_tool -> resolution
ldap_referrals -> resolution
event_log_and_debug_logging -> resolution
verify_resolution -> resolution
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

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


```text title="Expected output"
# dn
DC=corp,DC=example,DC=com

# dn
DC=corp,DC=example,DC=com

# dn
DC=corp,DC=example,DC=com
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked; check with `net ads info` or Active Directory Users and Computers.
    **`Can't contact LDAP server (-1)`** — Confirm dc01.corp.example.com resolves and port 389 is reachable using `nslookup dc01.corp.example.com` and `telnet dc01.corp.example.com 389`.
    **`ldap_bind: Inappropriate authentication (48)`** — The LDAP server requires TLS/SSL; change `ldap://` to `ldaps://` and use port 636, or add `-ZZ` flag for STARTTLS on port 389.
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


```text title="Expected output"
subject=CN=dc01.corp.example.com,OU=Domain Controllers,DC=corp,DC=example,DC=com
issuer=CN=corp-root-ca,OU=Certification Authority,DC=corp,DC=example,DC=com
Verify return code: 21 (unable to verify the first certificate)
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2025 GMT
# SASL supported control OIDs:
dn:
supportedSASLMechanisms: GSSAPI
supportedSASLMechanisms: GSS-SPNEGO
supportedSASLMechanisms: EXTERNAL
supportedSASLMechanisms: DIGEST-MD5
Updating certificates in /etc/ssl/certs...
Processing triggers for ca-certificates (20230101) ...
```

!!! warning "Common errors"
    **`Verify return code: 20 (unable to get local issuer certificate)`** — Add the DC's root CA certificate to `/usr/local/share/ca-certificates/` and run `update-ca-certificates`.
    **`ldapsearch: error code 1 - 000004DC: LdapErr: DSID-0C090A4C, comment: In order to perform this operation a successful bind must be completed before, data 0, v4563`** — Verify the service account credentials and ensure the LDAP bind DN format matches your directory schema (e.g., `cn=svc-ldap,cn=users,dc=corp,dc=example,dc=com`).
    **`cp: cannot stat 'corp-root-ca.crt': No such file or directory`** — Verify the CA certificate file path is correct and the file exists in the current working directory or provide an absolute path.
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


```text title="Expected output"
# LDAP 3.13.11 (protocol 3.29)
dn: CN=John Smith,OU=Users,DC=corp,DC=example,DC=com
cn: John Smith

dn: CN=Jane Doe,OU=Users,DC=corp,DC=example,DC=com
cn: Jane Doe

dn: CN=Admin Service,OU=Service Accounts,DC=corp,DC=example,DC=com
cn: Admin Service

# referral ldap://dc02.corp.example.com/DC=corp,DC=example,DC=com??sub

dn: CN=jsmith,OU=Users,DC=corp,DC=example,DC=com
cn: jsmith
mail: jsmith@corp.example.com
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked; check with `net ads info` or Active Directory Users and Computers.
    **`Can't contact LDAP server (-1)`** — Confirm the DC hostname resolves and port 389 (or 3268 for GC) is accessible; test with `nc -zv dc01.corp.example.com 389`.
    **`Referral limit exceeded (11)`** — Add the `-r` flag to follow referrals automatically, or query the Global Catalog on port 3268 instead of the standard LDAP port.
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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Binds](../binds/)
- [Ports](../ports/)
- [Queries](../queries/)
- [Tls](../tls/)
- [LDAP — Overview](../)
