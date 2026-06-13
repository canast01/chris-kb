---
tags:
  - security
  - troubleshooting
---
# Authentication Failures Troubleshooting


<div class="kb-summary">
Authentication Failures Troubleshooting reference covering Overview, Symptom Classification, Diagnostic Flowchart, AD Account Lockout Investigation, LDAP Bind Failure Diagnosis and 4 more sections.
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

Authentication failures span multiple subsystems: Active Directory (Kerberos and NTLM), LDAP bind operations, certificate-based authentication, and MFA. This guide provides structured diagnosis from symptom to root cause with enterprise-grade tooling.

---

## Symptom Classification

| Symptom | Likely Subsystem | First Check |
|---|---|---|
| "Logon failure: unknown username or bad password" | AD / NTLM | Event 4625 on DC; account lockout status |
| "The referenced account is currently locked out" | AD lockout | Event 4740; lockout source IP |
| KRB5KDC_ERR_PREAUTH_FAILED | Kerberos pre-auth | Wrong password or disabled pre-auth |
| KRB5KRB_AP_ERR_SKEW | Kerberos clock skew | Time difference >5 min between client and KDC |
| KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN | Kerberos | Account does not exist in target realm |
| LDAP error 49 (Invalid Credentials) | LDAP bind | Wrong bind DN or password |
| LDAP error 32 (No Such Object) | LDAP | Bind DN path incorrect |
| LDAP error 81 (Server Down) | LDAP network | Port 389/636 blocked or service down |
| SEC_E_CERT_EXPIRED | Certificate auth | Client or server cert expired |
| CRL check failed / OCSP unreachable | Certificate auth | CRL distribution point not reachable |
| MFA push not received | MFA | RADIUS proxy or MFA agent issue |
| "No logon servers available" | AD network | DC unreachable — DNS or firewall |

---

## Diagnostic Flowchart

```mermaid
flowchart TD
    A[Authentication Failure Reported] --> B{Can user reach DC?}
    B -- No --> C[Check DNS: nltest /dsgetdc]
    C --> D{DC resolved?}
    D -- No --> E[Fix DNS / conditional forwarder]
    D -- Yes --> F[Check firewall port 88/389/636]
    B -- Yes --> G{Account locked?}
    G -- Yes --> H[Identify lockout source\nEvent 4740 on PDC emulator]
    H --> I[Find rogue process / stale credential\nReset password]
    G -- No --> J{Clock skew issue?}
    J -- Yes --> K[Fix NTP / w32tm /resync]
    J -- No --> L{Kerberos or LDAP?}
    L -- Kerberos --> M[Run klist / kinit\nCheck SPN with setspn -L]
    M --> N{Valid TGT obtained?}
    N -- No --> O[Check KDC connectivity\nVerify pre-auth enabled]
    N -- Yes --> P[Check service ticket\nSPN misconfiguration?]
    L -- LDAP --> Q[Test ldp.exe or ldapsearch\nConfirm bind DN and credentials]
    Q --> R{TLS/SSL required?}
    R -- Yes --> S[Verify cert chain\nCheck LDAPS port 636]
    L -- Certificate --> T[Check cert expiry\nopenssl x509 -noout -dates]
    T --> U{CRL/OCSP reachable?}
    U -- No --> V[Fix CDP / add OCSP proxy]
    U -- Yes --> W[Check EKU — Client Auth OID 1.3.6.1.5.5.7.3.2]
```
```text
┌─────────────────────────────────────── Authentication Failures ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth failures: account lockout, expired password, Kerberos clock skew, SSO config       │   │
│   │      First check: Is the user account locked? Is the service account credential expired?      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          AD / LDAP          │  │           Kerberos          │  │          SSO / SAML         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Account locked       │  │      Clock skew > 5 min     │  │      Metadata mismatch      │   │
│   │       Password expired      │  │         SPN missing         │  │     Certificate expired     │   │
│   │      LDAP port blocked      │  │       Delegation issue      │  │       ACS URL mismatch      │   │
│   │        DC unreachable       │  │        Realm mismatch       │  │        Claim mapping        │   │
│   │      Group policy block     │  │       KDC unreachable       │  │       IdP unreachable       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     Symptom      │   First check    │      Command      │       Fix        │      Verify      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Locked out    │   AD LockedOut   │     Get-ADUser    │ Unlock-ADAccount │     Login OK     │   │
│   │  Kerberos fail   │    NTP clock     │    w32tm /query   │     Sync NTP     │ klist purge+test │   │
│   │     SSO fail     │     IdP logs     │   Browser trace   │   Fix metadata   │    SAML trace    │   │
│   │   LDAP blocked   │   Port 389/636   │    Test-NetConn   │     Open FW      │  ldapsearch OK   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Clock skew     = Kerberos requires all participants within 5 min; verify NTP on all hosts          │
│    SPN            = Service Principal Name; must exist and be unique for Kerberos auth to work        │
│    SAML trace     = Browser extension (SAML Tracer) captures assertion for SP/IdP debugging           │
│    ACS URL        = Assertion Consumer Service URL; SP endpoint; must match IdP configuration         │
│    klist purge    = Clears cached Kerberos tickets; forces re-auth after fixing KDC issue             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Clock Skew Detection

Kerberos requires clocks within 5 minutes. Skew >5 min causes KRB5KRB_AP_ERR_SKEW.

```powershell
# Check domain time sync status
w32tm /query /status

# Example output:
# Leap Indicator: 0(no warning)
# Stratum: 3 (secondary reference - syncd by (S)NTP)
# Precision: -23 (119.209ns per tick)
# Root Delay: 0.0151367s
# Root Dispersion: 0.0397949s
# Reference Id: 0xC0A8010A (source  dc01.corp.example.com)
# Last Successful Sync Time: 5/8/2026 8:10:22 AM

# Force resync
w32tm /resync /force

# Compare time between client and KDC
w32tm /stripchart /computer:dc01.corp.example.com /samples:5
```

### 4. SPN Diagnosis

```powershell
# List SPNs registered for a service account
setspn -L svc-sql

# Check for duplicate SPNs (common cause of auth failures)
setspn -X -F

# Example duplicate SPN output:
# Checking domain DC=corp,DC=example,DC=com
# Duplicate SPNs found!
# MSSQLSvc/sql01.corp.example.com:1433 is registered on:
#   CN=svc-sql,OU=ServiceAccounts,...
#   CN=sql01$,OU=Servers,...
```

---

## AD Account Lockout Investigation

### Locate Lockout Source

```powershell
# Check lockout status (run on PDC emulator or target DC)
Get-ADUser -Identity jsmith -Properties LockedOut, BadLogonCount, BadPasswordTime, LastBadPasswordAttempt |
    Select-Object Name, LockedOut, BadLogonCount, BadPasswordTime, LastBadPasswordAttempt

# Unlock account
Unlock-ADAccount -Identity jsmith

# Find the PDC emulator (lockouts are forwarded here)
(Get-ADDomain).PDCEmulator
```

### Search Security Event Logs

```powershell
# Event 4625 = Failed logon
# Event 4740 = Account locked out
# Event 4776 = NTLM credential validation attempt

# Search for lockout events on PDC emulator
Get-WinEvent -ComputerName pdc01 -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4740
    StartTime = (Get-Date).AddHours(-2)
} | Select-Object TimeCreated, Message | Format-List

# Extract caller workstation from event 4740
Get-WinEvent -ComputerName pdc01 -FilterHashtable @{LogName='Security'; Id=4740} -MaxEvents 10 |
    ForEach-Object {
        $xml = [xml]$_.ToXml()
        [PSCustomObject]@{
            Time      = $_.TimeCreated
            User      = $xml.Event.EventData.Data | Where-Object Name -eq 'TargetUserName' | Select-Object -Expand '#text'
            Caller    = $xml.Event.EventData.Data | Where-Object Name -eq 'CallerComputerName' | Select-Object -Expand '#text'
        }
    }
```

---

## LDAP Bind Failure Diagnosis

```bash
# Linux: test anonymous and authenticated bind
ldapsearch -x -H ldap://dc01.corp.example.com -b "DC=corp,DC=example,DC=com" "(sAMAccountName=jsmith)"

# Test authenticated bind
ldapsearch -x -H ldap://dc01.corp.example.com \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=corp,DC=example,DC=com" \
  -W -b "DC=corp,DC=example,DC=com" "(sAMAccountName=jsmith)"

# Test LDAPS (port 636)
ldapsearch -x -H ldaps://dc01.corp.example.com:636 \
  -D "CN=svc-ldap,OU=ServiceAccounts,DC=corp,DC=example,DC=com" \
  -W -b "DC=corp,DC=example,DC=com" "(sAMAccountName=jsmith)"
```

### LDAP Result Codes

| Code | Meaning | Fix |
|---|---|---|
| 0 | Success | — |
| 32 | No Such Object | Verify base DN and bind DN path |
| 49 | Invalid Credentials | Wrong password or account locked |
| 52e | Invalid credentials (Windows extended) | Wrong password |
| 530 | Not permitted to logon at this time | Logon hours restriction |
| 531 | Not permitted to logon from this workstation | Workstation restriction |
| 533 | Account disabled | Enable the account |
| 701 | Account expired | Extend account expiry |
| 773 | Password must change | Force password reset |

---

## Certificate-Based Authentication Failures

```bash
# Check certificate expiry dates
openssl x509 -in /etc/ssl/certs/client.crt -noout -dates
# Output:
# notBefore=May  8 00:00:00 2025 GMT
# notAfter=May  8 23:59:59 2026 GMT

# Verify the full certificate chain
openssl verify -CAfile /etc/ssl/certs/ca-bundle.crt /etc/ssl/certs/client.crt

# Check CRL distribution point from certificate
openssl x509 -in /etc/ssl/certs/client.crt -noout -text | grep -A3 "CRL Distribution"

# Test OCSP manually
openssl ocsp -issuer issuer.crt -cert client.crt \
  -url http://ocsp.corp.example.com -text

# Check Extended Key Usage (must include Client Authentication)
openssl x509 -in client.crt -noout -text | grep -A2 "Extended Key Usage"
# Expected: TLS Web Client Authentication
```

```powershell
# Windows: check certificate store
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.NotAfter -lt (Get-Date).AddDays(30)} |
    Select-Object Subject, NotAfter, Thumbprint

# Check NTAuth store (required for smart card / certificate logon to AD)
certutil -viewstore -enterprise NTAuth
```

---

## Kerberos Error Code Reference

| Error Code | Hex | Meaning | Common Cause |
|---|---|---|---|
| KDC_ERR_NONE | 0x0 | No error | — |
| KDC_ERR_C_PRINCIPAL_UNKNOWN | 0x6 | Client not found in Kerberos DB | Account doesn't exist or wrong realm |
| KDC_ERR_PREAUTH_FAILED | 0x18 | Pre-auth failed | Wrong password |
| KRB_AP_ERR_SKEW | 0x25 | Clock skew too large | >5 min time difference |
| KRB_AP_ERR_TKT_EXPIRED | 0x20 | Ticket expired | Clock issue or ticket TTL exceeded |
| KDC_ERR_BADOPTION | 0x11 | KDC cannot accommodate requested option | Constrained delegation misconfiguration |
| KDC_ERR_ETYPE_NOTSUPP | 0x1B | Encryption type not supported | RC4 disabled; client doesn't support AES |
| KDC_ERR_WRONG_REALM | 0x44 | Wrong realm | Cross-forest trust misconfiguration |

---

## Escalation Criteria

Escalate to Active Directory / Identity team when:

- Domain Controller is unreachable from multiple sites simultaneously
- Mass lockouts affecting >10 accounts within 15 minutes (potential credential stuffing)
- Kerberos encryption type changes (RC4 disabled) causing widespread failures
- Certificate Authority is offline or CRL is expired
- SPN conflicts cannot be resolved without schema-level investigation
- Federated identity (ADFS / Azure AD) trust failures affecting external access
- Smart card / PIV authentication failure affecting regulated users (compliance impact)

---

## Quick Reference: Time Sync Verification Chain

```text
Authoritative NTP (Stratum 1)
        ↓
PDC Emulator DC (Stratum 2) ← All DCs sync here
        ↓
Domain Members / Servers (Stratum 3)
        ↓
VMs (sync from ESXi host OR domain — not both)
```

```powershell
# Verify which NTP server a machine is using
w32tm /query /peers

# Identify PDC emulator in domain
netdom query fsmo | findstr "PDC"
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
