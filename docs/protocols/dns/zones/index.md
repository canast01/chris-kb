# DNS Zones

## Overview

DNS zones are authoritative containers for a portion of the DNS namespace. Windows DNS supports primary, secondary, stub, and forward zones. AD-integrated zones store data in Active Directory, enabling multi-master replication and secure dynamic updates. Zone delegation carves out sub-domains to separate DNS servers.

## Zone Types Reference

| Type | Writable | Data Store | Use Case |
|------|----------|------------|----------|
| Primary | Yes | File or AD | Authoritative source |
| Secondary | No | File only | Read-only replica from primary |
| Stub | No | File or AD | Holds NS/A for child zone only |
| Forward | No | File or AD | Redirects queries for a domain |
| AD-integrated Primary | Yes | AD database | Best for domain environments |

## Creating Zones

```powershell
# Create a primary zone (file-backed)
Add-DnsServerPrimaryZone `
  -Name "corp.local" `
  -ZoneFile "corp.local.dns" `
  -DynamicUpdate NonsecureAndSecure

# Create an AD-integrated zone
Add-DnsServerPrimaryZone `
  -Name "corp.local" `
  -ReplicationScope "Forest" `
  -DynamicUpdate Secure

# Create a reverse lookup zone
Add-DnsServerPrimaryZone `
  -NetworkId "192.168.10.0/24" `
  -ReplicationScope "Forest" `
  -DynamicUpdate Secure

# Create a secondary zone
Add-DnsServerSecondaryZone `
  -Name "corp.local" `
  -ZoneFile "corp.local.dns" `
  -MasterServers 10.0.0.53
```

## Zone Transfer

```powershell
# Allow zone transfer to specific servers
Set-DnsServerPrimaryZone `
  -Name "corp.local" `
  -SecureSecondaries TransferToSecureServers `
  -SecondaryServers 10.0.0.54

# Trigger manual zone transfer on secondary
Start-DnsServerZoneTransfer -Name "corp.local"

# Check transfer status
Get-DnsServerZone -Name "corp.local" | Select-Object ZoneName, LastZoneTransferAttempt
```

## Zone Delegation

```powershell
# Delegate child.corp.local to a child DNS server
Add-DnsServerZoneDelegation `
  -Name "corp.local" `
  -ChildZoneName "child" `
  -NameServer "ns1.child.corp.local" `
  -IPAddress 10.1.0.53

# Verify delegation NS record exists
Resolve-DnsName -Name "child.corp.local" -Type NS -Server 10.0.0.53
```

## AD-Integrated Zone Replication Scopes

```powershell
# View current replication scope
Get-DnsServerZone -Name "corp.local" | Select-Object ReplicationScope

# Change replication scope
Set-DnsServerPrimaryZone `
  -Name "corp.local" `
  -ReplicationScope "Forest"
# Options: Forest | Domain | Legacy | None
```

## Known Issues

- Secondary zones stop updating if the primary's `SecureSecondaries` setting blocks the secondary's IP. Add the secondary to `SecondaryServers` or set `TransferToAnyServer` for testing.
- AD-integrated zones with `ReplicationScope "Domain"` are not visible to DCs in other domains. Use `"Forest"` for enterprise-wide zones.
- After converting a file-backed primary to AD-integrated, the old `.dns` zone file is not deleted automatically but is no longer used. Remove it to avoid confusion.
