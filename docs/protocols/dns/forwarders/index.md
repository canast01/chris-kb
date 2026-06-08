# DNS Forwarders


<div class="kb-summary">
DNS Forwarders reference covering Overview, Configuring Global Forwarders, Conditional Forwarders, Root Hints vs Forwarders, Split-Brain DNS and 2 more sections.
</div>

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Internal DNS (DC)            External / Upstream                                                     │
│  ┌──────────────────┐         ┌──────────────────────────┐                                            │
│  │ corp.local zone  │         │  Forwarder: 8.8.8.8      │                                            │
│  │ (authoritative)  │         │  (for unknown names)     │                                            │
│  └────────┬─────────┘         └──────────────────────────┘                                            │
│           │                                                                                           │
│  Query: web01.example.local  ──► answered from local zone                                             │
│  Query: google.com        ──► forwarded to 8.8.8.8 ─► answer                                          │
│                                                                                                       │
│  CONDITIONAL FORWARDER:                                                                               │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │ partner.example.com ──► forward to 172.16.1.10         │                                           │
│  │ (specific domain sent to designated server)            │                                           │
│  └────────────────────────────────────────────────────────┘                                           │
│                                                                                                       │
│  Forwarder unreachable? ──► fallback to root hints                                                    │
│  (if UseRootHint = $true — recommended for resilience)                                                │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

DNS forwarders direct queries for names a server cannot resolve locally to another DNS server. Conditional forwarders send queries for a specific domain to a designated server — essential for split-brain DNS and cross-forest resolution. Root hints are the fallback when no forwarder is configured.

## Configuring Global Forwarders

```powershell
# Set global forwarders on a Windows DNS server
Set-DnsServerForwarder -IPAddress 8.8.8.8, 8.8.4.4 -UseRootHint $false

# View current forwarders
Get-DnsServerForwarder

# Remove all forwarders (reverts to root hints)
Remove-DnsServerForwarder -IPAddress 8.8.8.8, 8.8.4.4
```

## Conditional Forwarders

```powershell
# Add a conditional forwarder for corp.local -> internal DC
Add-DnsServerConditionalForwarderZone `
  -Name "corp.local" `
  -MasterServers 10.0.0.53, 10.0.0.54 `
  -ReplicationScope "Forest"

# Add forwarder for a partner domain
Add-DnsServerConditionalForwarderZone `
  -Name "partner.example.com" `
  -MasterServers 172.16.1.10 `
  -ReplicationScope "None"

# View all conditional forwarders
Get-DnsServerZone | Where-Object { $_.ZoneType -eq "Forwarder" }

# Remove a conditional forwarder
Remove-DnsServerZone -Name "partner.example.com"
```

## Root Hints vs Forwarders

| Mode | Use Case | Notes |
|------|----------|-------|
| Root hints only | Air-gapped or root hint preferred | Slower, iterative resolution |
| Forwarders only | Corporate with proxy DNS | Fast, but single point of failure if forwarder is down |
| Forwarders + root hints fallback | Typical production | Forwarders tried first; root hints if forwarder fails |
| Conditional forwarder | Split-brain or cross-domain | Specific domain sent to known server |

## Split-Brain DNS

Split-brain (split-horizon) uses the same domain name internally and externally with different answer sets. Internal clients resolve to RFC 1918 addresses; external clients get public IPs.

```powershell
# Internal zone for corp.example.com (AD-integrated)
# Already exists as primary zone on internal DCs

# Confirm external queries are NOT forwarded internally
# The internal zone answers first; no conditional forwarder needed for this domain
Get-DnsServerZone -Name "example.com"

# Verify the zone is authoritative (not a forwarder)
(Get-DnsServerZone -Name "example.com").ZoneType   # Should return "Primary"
```

## Loop Prevention

A forwarding loop occurs when Server A forwards to Server B and B forwards back to A.

```powershell
# Check each server's forwarder list
Get-DnsServerForwarder   # run on both servers

# On Windows, DNS will detect simple loops and log event ID 4016
# Check DNS event log
Get-WinEvent -LogName "DNS Server" -MaxEvents 50 |
  Where-Object { $_.Id -eq 4016 }
```

## Known Issues

- If a conditional forwarder is configured with `ReplicationScope "Forest"` but the DNS server is not a DC, the zone will fail to replicate. Use `"None"` for standalone servers.
- Forwarders with `UseRootHint $false` will fail all resolution if the forwarder is unreachable. Set `UseRootHint $true` as a safety net in production.
- Avoid forwarding `.local` to external resolvers — multicast DNS clients use `.local` and leaking those queries causes delays and NXDOMAIN noise.
