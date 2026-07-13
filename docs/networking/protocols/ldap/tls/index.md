---
title: TLS (LDAP)
tags:
  - networking
description: "TLS (LDAP) reference covering Overview, Certificate Requirements for LDAPS, Configuring LDAPS on Active Directory, Channel Binding and LDAP Signing..."
---

# TLS (LDAP)

<div class="kb-summary">
TLS (LDAP) reference covering Overview, Certificate Requirements for LDAPS, Configuring LDAPS on Active Directory, Channel Binding and LDAP Signing, LdapClientIntegrity (Client Side) and 1 more sections.
</div>

        STARTTLS vs LDAPS

```d2
direction: down

certificate_requirements_for_ldaps: "Certificate Requirements for LDAPS" {shape: rectangle}
configuring_ldaps_on_active_director: "Configuring LDAPS on Active Directory" {shape: rectangle}
channel_binding_and_ldap_signing: "Channel Binding and LDAP Signing" {shape: rectangle}
ldapclientintegrity_client_side: "LdapClientIntegrity (Client Side)" {shape: rectangle}
testing_tls_configuration: "Testing TLS Configuration" {shape: rectangle}

certificate_requirements_for_ldaps -> configuring_ldaps_on_active_director: uses
configuring_ldaps_on_active_director -> channel_binding_and_ldap_signing: uses
channel_binding_and_ldap_signing -> ldapclientintegrity_client_side: uses
ldapclientintegrity_client_side -> testing_tls_configuration: uses
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


```text title="Expected output"
Subject: CN=dc01.corp.example.com, OU=Domain Controllers, O=Example Corp, C=US
DNS:dc01.corp.example.com, DNS:*.corp.example.com
Not After : Dec 15 23:59:59 2025 GMT

CONNECTED(00000003)
depth=1 C = US, O = Example Corp, CN = Example Corp CA
verify return:1
depth=0 CN = dc01.corp.example.com, OU = Domain Controllers, O = Example Corp, C = US
verify return:1
---
Certificate chain
 0 s:CN=dc01.corp.example.com, OU=Domain Controllers, O=Example Corp, C=US
   i:C=US, O=Example Corp, CN=Example Corp CA
-----BEGIN CERTIFICATE-----
MIIDpDCCAoygAwIBAgIQK7m8Z5+...
-----END CERTIFICATE-----
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the DC's root CA certificate to your system's trusted CA store or use `-CAfile` to specify the CA bundle path.
    **`connect: Connection refused`** — Verify the DC hostname/IP is correct, the LDAPS port (636) is open, and the DC is online with `nslookup dc01.corp.example.com` and `telnet dc01.corp.example.com 636`.
    **`Timeout waiting for input`** — The command is waiting for stdin; ensure `</dev/null` is appended to close stdin immediately after the connection completes.
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


```text title="Expected output"
# LDAP Result: Success (0x0)
dn: DC=corp,DC=example,DC=com

# numResponses: 1
# numEntries: 1

dn: cn=config
objectClass: top
objectClass: OpenLDAProotDSE
namingContexts: DC=corp,DC=example,DC=com
supportedLDAPVersion: 3
supportedSASLMechanisms: GSSAPI
supportedControl: 1.3.6.1.4.1.4203.2.11.3.4.2
supportedExtension: 1.3.6.1.4.1.1466.20037.2
```

!!! warning "Common errors"
    **`TLS certificate problem: self signed certificate`** — Add the DC's certificate to `/etc/ldap/cacerts/` and configure `TLS_CACERT /etc/ldap/cacerts/ca-cert.pem` in `/etc/ldap/ldap.conf`, or use `LDAPTLS_REQCERT=never` for testing only.
    **`ldap_sasl_bind_s: Invalid credentials (49)`** — Verify the service account password is correct and the account exists in Active Directory with `ldapsearch -x -H ldaps://dc01.corp.example.com:636 -D "svc-ldap@corp.example.com" -w "PASSWORD"`.
    **`Can't contact LDAP server (-1)`** — Confirm the LDAPS port 636 is open and reachable with `telnet dc01.corp.example.com 636` or `nc -zv dc01.corp.example.com 636`.
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


```text title="Expected output"
Starting Nmap 7.92 ( https://nmap.org ) at 2024-01-15 14:32:18 UTC
Nmap scan report for dc01.corp.example.com (192.168.1.50)
Host is up (0.0042s latency).

PORT    STATE SERVICE
636/tcp open  ldapssl

| ssl-enum-ciphers:
|   TLSv1.2:
|     ciphers:
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|     least strength: A
|   TLSv1.3:
|     ciphers:
|       TLS_AES_256_GCM_SHA384 (ecdh_x25519) - A
|     least strength: A
|_  least strength: A

Verify return code: 0 (ok)
subject=CN=dc01.corp.example.com, O=Corp, C=US
issuer=CN=Corp Root CA, O=Corp, C=US

# command: ldapsearch
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (objectClass=domain)
# requesting: dn
#

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    **`ldap_start_tls: Connect error (-1)`** — Verify the LDAP server is listening on port 389 and firewall allows the connection; check with `netstat -tlnp | grep 389`.
    **`Verify return code: 20 (unable to get local issuer certificate)`** — Add the DC's issuing CA certificate to the system trust store with `update-ca-certificates` or specify the correct CA bundle path.
    **`ldap_bind: Invalid credentials (49)`** — Confirm the service account password is correct and the account is not locked; test with `ldapwhoami -H ldap://dc01.corp.example.com:389 -D "svc-ldap@corp.example.com" -w "password"`.