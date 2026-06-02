# LDAP Ports


<div class="kb-summary">
LDAP Ports reference covering Overview, Port 389 and 636, Global Catalog Ports (3268 and 3269), Firewall Rules, StartTLS vs LDAPS and 1 more sections.
</div>

        LDAP PORT MAP
```text
┌──────────────────────────────────────────────────────────────┐
│  Port 389 (LDAP)                                                                                      │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │ App ──────────────────────── cleartext (or StartTLS)──►│                                           │
│  │     plain query or -ZZ upgrade to TLS (STARTTLS)       │                                           │
│  └────────────────────────────────────────────────────────┘                                           │
│                                                                                                       │
│  Port 636 (LDAPS)                                                                                     │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │ App ──── TLS from first byte ────────────────────────►│                                            │
│  │     Always encrypted; cert check on connect            │                                           │
│  └────────────────────────────────────────────────────────┘                                           │
│                                                                                                       │
│  Port 3268 (Global Catalog)                                                                           │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │ App ──── forest-wide query (partial replica) ────────►│                                            │
│  │     Use when querying across multiple AD domains       │                                           │
│  └────────────────────────────────────────────────────────┘                                           │
│                                                                                                       │
│  Port 3269 (Global Catalog over TLS)                                                                  │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │ App ──── 3268 + TLS ─────────────────────────────────►│                                            │
│  └────────────────────────────────────────────────────────┘                                           │
└──────────────────────────────────────────────────────────────┘
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
