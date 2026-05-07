# AD DNS Dependency

Active Directory is fundamentally dependent on DNS. Every DC registration, client logon, and Kerberos ticket request relies on DNS SRV and A records being correct and resolvable. A broken DNS layer is the most common root cause of AD-wide outages.

## SRV Records and DC Locator

DCs register SRV records in DNS automatically via the Netlogon service. The DC Locator process uses these records to find the right DC for a given site and service.

Key SRV record types:

| Record | Purpose |
|---|---|
| `_ldap._tcp.<domain>` | Generic LDAP over TCP |
| `_kerberos._tcp.<domain>` | Kerberos KDC (TCP) |
| `_ldap._tcp.dc._msdcs.<domain>` | DC-specific LDAP |
| `_kerberos._udp.<domain>` | Kerberos KDC (UDP) |
| `_gc._tcp.<domain>` | Global Catalog |
| `_ldap._tcp.<site>._sites.<domain>` | Site-scoped LDAP |

```cmd
# List all AD SRV records in DNS
nslookup -type=SRV _ldap._tcp.corp.example.com
nslookup -type=SRV _kerberos._tcp.corp.example.com
nslookup -type=SRV _gc._tcp.corp.example.com
```

## Checking DNS Health

```cmd
# Run dcdiag DNS tests on local DC
dcdiag /test:dns /v

# Run against a specific DC
dcdiag /test:dns /s:dc01.corp.example.com /v

# Check that Netlogon has registered SRV records
nltest /dsgetdc:corp.example.com

# Force Netlogon to re-register DNS records
nltest /dsregdns

# Verify a DC can be found for a specific site
nltest /dsgetdc:corp.example.com /site:LondonSite
```

## DC Locator Process

When a client needs a DC it sends a DNS query for `_ldap._tcp.<site>._sites.<domain>`. If no site-scoped record is found it falls back to the domain-wide `_ldap._tcp.<domain>` SRV records. The client then sends an LDAP ping (CLDAP) to the returned DCs and selects the fastest responder.

```powershell
# Show which DC a machine is currently using
(Get-ADDomainController -Discover).Name

# Force rediscovery of a DC
nltest /sc_reset:corp.example.com

# Display the DC locator cache
nltest /dclist:corp.example.com
```

## DNS Zone Configuration for AD

AD-integrated DNS zones are recommended. They replicate via AD replication rather than zone transfers and support secure dynamic updates.

```cmd
# Check DNS zone type
dnscmd /zoneinfo corp.example.com

# List all DNS zones on a DC
dnscmd /enumzones

# Force dynamic DNS re-registration from a client
ipconfig /registerdns

# Check _msdcs zone exists (critical for AD)
nslookup -type=NS _msdcs.corp.example.com
```

## DNS Health Checks Runbook

```powershell
# Check all DCs have registered A records
Get-ADDomainController -Filter * | ForEach-Object {
    Resolve-DnsName $_.HostName -Type A -ErrorAction SilentlyContinue
}

# Confirm SRV records are present for every DC
$domain = "corp.example.com"
Resolve-DnsName "_ldap._tcp.$domain" -Type SRV
Resolve-DnsName "_kerberos._tcp.$domain" -Type SRV

# Check for DNS scavenging (stale record removal)
Get-DnsServerZoneAging -Name "corp.example.com"
```

## Common DNS-Caused AD Failures

- Missing SRV records after DC promotion: restart Netlogon and run `nltest /dsregdns`
- Clients caching old DC addresses: flush with `ipconfig /flushdns`
- Split-brain DNS: internal clients resolving to external IPs — ensure internal DNS is authoritative for the AD domain
- Scavenging too aggressive: valid DC records deleted — review AgingEnabled and NoRefreshInterval settings
- Wrong DNS server on DC NIC: DCs must point to AD-integrated DNS, not a public resolver
