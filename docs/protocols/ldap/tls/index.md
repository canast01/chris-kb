# LDAP TLS (LDAPS)

```
        STARTTLS vs LDAPS
┌──────────────────────────────────────────────────────────────┐
│  STARTTLS (port 389 → upgrade to TLS)                        │
│  ┌────────────┐         ┌──────────────────────────────┐     │
│  │ App        │         │ DC port 389                  │     │
│  │            ├────────►│ 1. plain TCP connect         │     │
│  │ -H ldap:   │         │ 2. STARTTLS extended op      │     │
│  │ :389 -ZZ   ├────────►│ 3. TLS negotiated (same conn)│     │
│  │            │◄────────┤ 4. cert check + query        │     │
│  └────────────┘         └──────────────────────────────┘     │
│  Risk: downgrade attack if STARTTLS not enforced              │
│                                                              │
│  LDAPS (port 636 — TLS from first byte)                      │
│  ┌────────────┐         ┌──────────────────────────────┐     │
│  │ App        │         │ DC port 636                  │     │
│  │            ├────────►│ 1. TLS handshake immediately │     │
│  │ -H ldaps:  │         │ 2. cert verified             │     │
│  │ :636       ├────────►│ 3. LDAP bind + query         │     │
│  │            │◄────────┤                              │     │
│  └────────────┘         └──────────────────────────────┘     │
│  Preferred; no downgrade risk                                │
└──────────────────────────────────────────────────────────────┘
```

## Overview

LDAPS (LDAP over TLS on port 636) and StartTLS (TLS upgrade on port 389) protect LDAP traffic from eavesdropping and tampering. Active Directory enforces LDAP channel binding and signing requirements via KB4520412 and related updates. Misconfigured TLS is a common cause of bind failures after patch cycles.

| Setting | Description | Registry Path |
|---|---|---|
| `LdapEnforceChannelBinding` | Require channel binding tokens | `HKLM\SYSTEM\CCS\Services\NTDS\Parameters` |
| `LDAPServerIntegrity` | Require signing (0=none, 1=negotiate, 2=require) | `HKLM\SYSTEM\CCS\Services\NTDS\Parameters` |
| `LdapClientIntegrity` | Client-side signing requirement | `HKLM\SYSTEM\CCS\Services\ldap` |

## Certificate Requirements for LDAPS

A Domain Controller's LDAPS certificate must meet:

- Subject or SAN matches the DC's FQDN (e.g., `dc01.corp.example.com`)
- Key Usage includes **Digital Signature** and **Key Encipherment**
- Enhanced Key Usage includes **Server Authentication** (OID 1.3.6.1.5.5.7.3.1)
- Not expired and trusted by clients (issued by an enterprise or public CA)

```bash
# Check the LDAPS certificate presented by a DC
openssl s_client -connect dc01.corp.example.com:636 -showcerts </dev/null 2>/dev/null |
    openssl x509 -noout -text | grep -E "Subject:|DNS:|Not After"

# Test full TLS handshake
openssl s_client -connect dc01.corp.example.com:636 </dev/null
```

## Configuring LDAPS on Active Directory

```powershell
# LDAPS is enabled automatically when a valid certificate is installed on the DC.
# Request a certificate from your enterprise CA:
$cert = Get-Certificate -Template "DomainController" -CertStoreLocation "Cert:\LocalMachine\My"

# Verify the DC is listening on 636 after certificate is installed
netstat -an | findstr ":636"

# Test LDAPS from a Windows client
Test-NetConnection -ComputerName dc01.corp.example.com -Port 636
```

```bash
# Test LDAPS bind from Linux
ldapsearch -H ldaps://dc01.corp.example.com:636 \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           "(objectClass=domain)" dn

# Disable certificate verification for testing only (never in production)
LDAPTLS_REQCERT=never ldapsearch -H ldaps://dc01.corp.example.com:636 \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "" -s base "(objectClass=*)"
```

## Channel Binding and LDAP Signing

Enforced via Group Policy or registry. Required for security hardening (Microsoft guidance post-2020).

```powershell
# Check current LDAP server integrity setting
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters" |
    Select-Object LDAPServerIntegrity

# Set LDAP signing to Required (2) on the DC
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters" `
                 -Name "LDAPServerIntegrity" -Value 2

# Check channel binding token requirement
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters" |
    Select-Object LdapEnforceChannelBinding
# 0 = disabled, 1 = supported clients, 2 = always required

# Set channel binding to always required
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters" `
                 -Name "LdapEnforceChannelBinding" -Value 2
```

## LdapClientIntegrity (Client Side)

```powershell
# Check client-side LDAP signing policy
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\ldap" |
    Select-Object LdapClientIntegrity
# 0 = none, 1 = negotiate signing, 2 = require signing

# Set client to negotiate signing
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\ldap" `
                 -Name "LdapClientIntegrity" -Value 1

# Via Group Policy: Computer Configuration > Windows Settings > Security Settings >
# Local Policies > Security Options > "Network security: LDAP client signing requirements"
```

## Testing TLS Configuration

```bash
# Check supported TLS versions on the DC
nmap --script ssl-enum-ciphers -p 636 dc01.corp.example.com

# Verify certificate chain is complete
openssl s_client -connect dc01.corp.example.com:636 -CAfile /etc/ssl/certs/ca-certificates.crt \
    </dev/null 2>&1 | grep -E "Verify return code|certificate"

# Test StartTLS upgrade (port 389)
ldapsearch -H ldap://dc01.corp.example.com:389 -ZZ \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn
```
