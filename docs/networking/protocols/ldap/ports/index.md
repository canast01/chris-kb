---
tags:
  - networking
description: "LDAP Ports reference covering Overview, Port 389 and 636, Global Catalog Ports (3268 and 3269), Firewall Rules, StartTLS vs LDAPS and 1 more sections."
---
# LDAP Ports

<div class="kb-summary">
LDAP Ports reference covering Overview, Port 389 and 636, Global Catalog Ports (3268 and 3269), Firewall Rules, StartTLS vs LDAPS and 1 more sections.
</div>

```d2
direction: down

port_389_and_636: "Port 389 and 636" {shape: rectangle}
global_catalog_ports_3268_and_3269: "Global Catalog Ports (3268 and 3269)" {shape: rectangle}
firewall_rules: "Firewall Rules" {shape: rectangle}
starttls_vs_ldaps: "StartTLS vs LDAPS" {shape: rectangle}
port_troubleshooting: "Port Troubleshooting" {shape: rectangle}

port_389_and_636 -> global_catalog_ports_3268_and_3269: uses
global_catalog_ports_3268_and_3269 -> firewall_rules: uses
firewall_rules -> starttls_vs_ldaps: uses
starttls_vs_ldaps -> port_troubleshooting: uses
```

## Overview

LDAP uses a small set of well-known TCP ports. All are required in different scenarios — plain LDAP for legacy compatibility, LDAPS for encrypted binds, and Global Catalog ports for forest-wide searches in Active Directory.

| Port | Protocol | Purpose |
|---|---|---|
| 389 | TCP/UDP | Standard LDAP (cleartext or StartTLS) |
| 636 | TCP | LDAPS — LDAP over TLS (always encrypted) |
| 3268 | TCP | LDAP Global Catalog (forest-wide, cleartext) |
| 3269 | TCP | LDAPS Global Catalog (forest-wide, encrypted) |
| 49152–65535 | TCP | Dynamic RPC ports (AD replication) |

## Port 389 and 636

Port 389 is the default LDAP port. Traffic is cleartext unless the client issues a StartTLS extended operation to upgrade the connection. Port 636 always uses TLS from the initial connection.

```bash
# Test port 389 connectivity
nc -zv dc01.corp.example.com 389

# Test port 636 connectivity
nc -zv dc01.corp.example.com 636

# Query via LDAP (port 389)
ldapsearch -H ldap://dc01.corp.example.com:389 -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn

# Query via LDAPS (port 636)
ldapsearch -H ldaps://dc01.corp.example.com:636 -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn
```


```text title="Expected output"
Connection to dc01.corp.example.com 389 port [tcp/ldap] succeeded!
Connection to dc01.corp.example.com 636 port [tcp/ldaps] succeeded!
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (objectClass=domain)
# requesting: dn
#

# DC=corp,DC=example,DC=com
dn: DC=corp,DC=example,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1

# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (objectClass=domain)
# requesting: dn
#

# DC=corp,DC=example,DC=com
dn: DC=corp,DC=example,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nc: getaddrinfo failed for dc01.corp.example.com: Name or service not known` | Verify the hostname is correct and resolvable by running `nslookup dc01.corp.example.com` or update your DNS/hosts file. |
    | `ldap_bind: Invalid credentials (49)` | Confirm the service account password is correct and the account is not locked; test with `ldapwhoami -H ldap://dc01.corp.example.com:389 -D "svc-ldap@corp.example.com" -w "password"`. |
    | `TLS: peer certificate cannot be authenticated with known CA certificates` | Add the LDAPS server certificate to your system CA store or disable certificate verification by adding `-o LDAPTLS_REQCERT=never` to the ldapsearch command. |
## Global Catalog Ports (3268 and 3269)

The Global Catalog contains a partial replica of all objects across all domains in the AD forest. Use these ports when queries must span multiple domains.

```bash
# Test GC port 3268
nc -zv dc01.corp.example.com 3268

# Query Global Catalog
ldapsearch -H ldap://dc01.corp.example.com:3268 -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           "(mail=jsmith@corp.example.com)" cn sAMAccountName

# Query Global Catalog over SSL (port 3269)
ldapsearch -H ldaps://dc01.corp.example.com:3269 -x \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" \
           "(sAMAccountName=jsmith)" memberOf
```


```text title="Expected output"
Connection to dc01.corp.example.com 3268 port [tcp/*] succeeded!
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (mail=jsmith@corp.example.com)
# requesting: cn sAMAccountName
#

dn: CN=John Smith,OU=Users,OU=Corp,DC=corp,DC=example,DC=com
cn: John Smith
sAMAccountName: jsmith

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1

# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (sAMAccountName=jsmith)
# requesting: memberOf
#

dn: CN=John Smith,OU=Users,OU=Corp,DC=corp,DC=example,DC=com
memberOf: CN=Engineering,OU=Groups,DC=corp,DC=example,DC=com
memberOf: CN=VPN-Users,OU=Groups,DC=corp,DC=example,DC=com

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
    | `Can't contact LDAP server` | Confirm port 3268/3269 is open in firewall rules between the client and domain controller, and that the DC hostname resolves correctly. |
## Firewall Rules

```bash
# Linux: allow LDAP and LDAPS outbound from an application server
iptables -A OUTPUT -p tcp -d 10.0.0.0/8 --dport 389 -j ACCEPT
iptables -A OUTPUT -p tcp -d 10.0.0.0/8 --dport 636 -j ACCEPT
iptables -A OUTPUT -p tcp -d 10.0.0.0/8 --dport 3268 -j ACCEPT
iptables -A OUTPUT -p tcp -d 10.0.0.0/8 --dport 3269 -j ACCEPT

# Windows Firewall: allow inbound LDAP to a DC
netsh advfirewall firewall add rule name="LDAP" protocol=TCP dir=in localport=389 action=allow
netsh advfirewall firewall add rule name="LDAPS" protocol=TCP dir=in localport=636 action=allow
netsh advfirewall firewall add rule name="LDAP-GC" protocol=TCP dir=in localport=3268 action=allow
netsh advfirewall firewall add rule name="LDAPS-GC" protocol=TCP dir=in localport=3269 action=allow
```


```text title="Expected output"
(no output — command completes silently)
Ok.
Ok.
Ok.
Ok.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iptables: No chain/target/match by that name` | Ensure iptables is installed and the kernel module is loaded with `modprobe iptable_filter`. |
    | `netsh: The filename, directory name, or volume name syntax is not correct` | Run the netsh command from an elevated (Administrator) PowerShell or Command Prompt window. |
    | `iptables: Bad rule (does a matching rule exist?)` | Verify the OUTPUT chain exists and no conflicting DROP rules precede these ACCEPT rules with `iptables -L OUTPUT -n`. |
## StartTLS vs LDAPS

```bash
# Use StartTLS on port 389 (upgrade cleartext connection to TLS)
ldapsearch -H ldap://dc01.corp.example.com:389 -ZZ \
           -D "svc-ldap@corp.example.com" -w "P@ssw0rd!" \
           -b "DC=corp,DC=example,DC=com" "(objectClass=domain)" dn

# Verify if StartTLS is supported
ldapsearch -H ldap://dc01.corp.example.com -x \
           -b "" -s base "(objectClass=*)" supportedExtension
# Look for OID 1.3.6.1.4.1.1466.20037 = StartTLS

# Test LDAPS certificate
openssl s_client -connect dc01.corp.example.com:636 -showcerts </dev/null 2>/dev/null |
    openssl x509 -noout -text | grep -E "Subject:|Issuer:|Not After"
```


```text title="Expected output"
# LDAP StartTLS Search
dn: DC=corp,DC=example,DC=com

# StartTLS Support Check
dn: 
supportedExtension: 1.3.6.1.4.1.1466.20037
supportedExtension: 1.3.6.1.5.1.4.1.1466.20037
supportedExtension: 1.3.6.1.4.1.1466.20037.8
supportedExtension: 1.3.6.1.4.1.1466.20037.12

# LDAPS Certificate Details
        Subject: CN=dc01.corp.example.com, OU=Domain Controllers, O=Corp, C=US
        Issuer: CN=Corp-CA, OU=Certification Authority, O=Corp, C=US
            Not After : Dec 15 23:59:59 2025 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_start_tls: Connect error (-1)` | Verify the LDAP server is listening on port 389 and StartTLS is enabled in the LDAP service configuration. |
    | `ldapsearch: Invalid credentials (49)` | Confirm the service account password is correct and the account is not locked or expired in Active Directory. |
    | `error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed` | Add the CA certificate to your system's trusted store or use `openssl s_client -connect dc01.corp.example.com:636 -CAfile /path/to/ca.crt` to verify with a specific CA bundle. |
## Port Troubleshooting

```powershell
# Test from Windows client
Test-NetConnection -ComputerName dc01.corp.example.com -Port 389
Test-NetConnection -ComputerName dc01.corp.example.com -Port 636
Test-NetConnection -ComputerName dc01.corp.example.com -Port 3268
Test-NetConnection -ComputerName dc01.corp.example.com -Port 3269

# Check DC is listening on LDAP ports
netstat -an | findstr ":389\|:636\|:3268\|:3269"
```
