# DNS Records

```text
        COMMON RECORD TYPES
┌──────────────────────────────────────────────────────────────┐
│  Forward zone: corp.local                                    │
│  ┌────┬─────────────────────────────────────────────────┐   │
│  │ A  │ web01  →  192.168.10.100  (IPv4 address)        │   │
│  │AAAA│ web01  →  2001:db8::1     (IPv6 address)        │   │
│  │CNAME│www   →  web01.example.local (alias)               │   │
│  │ MX │ @     →  10 mail.example.local (mail exchanger)    │   │
│  │ NS │ @     →  dc01.example.local  (nameserver)          │   │
│  │TXT │ @     →  "v=spf1 ..."    (SPF/DKIM/verify)      │   │
│  │SRV │_ldap._tcp → dc01:389     (service locator)      │   │
│  └────┴─────────────────────────────────────────────────┘   │
│                                                              │
│  Reverse zone: 10.168.192.in-addr.arpa                       │
│  ┌─────┬────────────────────────────────────────────────┐   │
│  │ PTR │ 100  →  web01.example.local  (reverse lookup)     │   │
│  └─────┴────────────────────────────────────────────────┘   │
│                                                              │
│  SOA record: serial + refresh + retry + expire + min-TTL    │
└──────────────────────────────────────────────────────────────┘
```

## Overview

DNS records define how names map to resources. Each record type serves a distinct purpose. On Windows DNS Server, records are managed with `DnsServer` PowerShell cmdlets or `dnscmd`. Dynamic DNS (DDNS) allows DHCP servers and clients to register records automatically.

## Common Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | `web01 A 192.168.10.100` |
| AAAA | IPv6 address | `web01 AAAA 2001:db8::1` |
| CNAME | Alias to another name | `www CNAME web01.example.local` |
| MX | Mail exchange | `@ MX 10 mail.example.local` |
| PTR | Reverse lookup | `100 PTR web01.example.local` |
| SRV | Service location | `_ldap._tcp SRV 0 100 389 dc01.example.local` |
| TXT | Arbitrary text (SPF, DKIM) | `@ TXT "v=spf1 ip4:203.0.113.10 -all"` |
| NS | Name server | `@ NS dc01.example.local` |

## Managing Records with PowerShell

```powershell
# Add an A record
Add-DnsServerResourceRecordA `
  -ZoneName "corp.local" `
  -Name "web01" `
  -IPv4Address "192.168.10.100" `
  -TimeToLive (New-TimeSpan -Hours 1)

# Add a CNAME
Add-DnsServerResourceRecordCName `
  -ZoneName "corp.local" `
  -Name "www" `
  -HostNameAlias "web01.example.local"

# Add a PTR record
Add-DnsServerResourceRecordPtr `
  -ZoneName "10.168.192.in-addr.arpa" `
  -Name "100" `
  -PtrDomainName "web01.example.local"

# Add an MX record
Add-DnsServerResourceRecord -MX `
  -ZoneName "corp.local" `
  -Name "@" `
  -MailExchange "mail.example.local" `
  -Preference 10

# Remove a record
Remove-DnsServerResourceRecord `
  -ZoneName "corp.local" `
  -RRType "A" `
  -Name "web01" `
  -Force
```

## Scavenging and Aging

Aging and scavenging clean up stale dynamically registered records.

```powershell
# Enable aging on a zone
Set-DnsServerZoneAging `
  -Name "corp.local" `
  -Aging $true `
  -ScavengeServers 10.0.0.53 `
  -RefreshInterval (New-TimeSpan -Days 7) `
  -NoRefreshInterval (New-TimeSpan -Days 7)

# Start an immediate scavenging pass
Start-DnsServerScavenging -Force

# Check aging settings
Get-DnsServerZoneAging -Name "corp.local"
```

## Dynamic DNS

```powershell
# Configure zone to allow secure dynamic updates (AD-integrated zones)
Set-DnsServerPrimaryZone -Name "corp.local" -DynamicUpdate Secure

# Allow non-secure updates (test/lab only)
Set-DnsServerPrimaryZone -Name "corp.local" -DynamicUpdate NonsecureAndSecure

# Force a client to re-register its DNS records
ipconfig /registerdns   # run on Windows client
```

## Known Issues

- CNAME records cannot coexist with other records at the same name (zone apex). Use A records or ALIAS/ANAME flattening at the apex instead.
- Stale A records from retired servers prevent their IPs from being reused cleanly. Run scavenging or remove records manually with `Remove-DnsServerResourceRecord`.
- After enabling aging on a zone with many existing records, the first scavenging pass may remove records that predate aging enablement (they have no timestamp). Pre-stamp existing records or wait for clients to refresh before enabling scavenging in production.
