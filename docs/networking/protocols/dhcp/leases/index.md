# DHCP Leases


<div class="kb-summary">
DHCP Leases reference covering Overview, Viewing Leases, Finding IP from MAC, Lease States Reference, Clearing Stale Leases and 2 more sections.
</div>

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Lease duration: 8 days (example)                                                                     │
│                                                                                                       │
│  │◄──────────────── 8 days ─────────────────────────────►│                                            │
│  │                                                        │                                           │
│  ▼ T0         T1 (50%)       T2 (87.5%)       T3 (100%)  │                                            │
│  ├────────────┼──────────────┼────────────────┼───────────┤                                           │
│  │   Using    │  Renew (unicast               │           │                                           │
│  │   lease    │  to server)  │  Rebind (broad.│ Expired   │                                           │
│  │            │              │  to any server)│           │                                           │
│  └────────────┴──────────────┴────────────────┴───────────┘                                           │
│                                                                                                       │
│  T1 = lease * 0.5  → client unicasts renewal request                                                  │
│  T2 = lease * 0.875 → client broadcasts to any DHCP server                                            │
│  T3 = lease expires → client must start DORA again                                                    │
│                                                                                                       │
│  Lease states: Active | Expired | Declined | ActiveReservation                                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

DHCP leases track which IP address is assigned to which client. On Windows Server, lease management is done with the `DhcpServer` PowerShell module. Stale leases can cause address exhaustion and ghost entries in DNS.

## Viewing Leases

```powershell
# List all leases in a scope
Get-DhcpServerv4Lease -ScopeId 192.168.10.0

# List active leases only
Get-DhcpServerv4Lease -ScopeId 192.168.10.0 | Where-Object { $_.AddressState -eq "Active" }

# Find a lease by IP
Get-DhcpServerv4Lease -ScopeId 192.168.10.0 -IPAddress 192.168.10.55

# Find a lease by MAC address
Get-DhcpServerv4Lease -ScopeId 192.168.10.0 | Where-Object { $_.ClientId -eq "00-11-22-33-44-55" }

# Search across all scopes on a server
Get-DhcpServerv4Scope | ForEach-Object {
  Get-DhcpServerv4Lease -ScopeId $_.ScopeId
} | Where-Object { $_.ClientId -eq "00-11-22-33-44-55" }
```

## Finding IP from MAC

```powershell
$mac = "00-1A-2B-3C-4D-5E"
Get-DhcpServerv4Scope | ForEach-Object {
  Get-DhcpServerv4Lease -ScopeId $_.ScopeId -ErrorAction SilentlyContinue
} | Where-Object { $_.ClientId -like "*$mac*" } |
  Select-Object IPAddress, ClientId, HostName, LeaseExpiryTime, AddressState
```

## Lease States Reference

| State | Description |
|-------|-------------|
| Active | Lease is current and in use |
| Expired | Lease time elapsed, client has not renewed |
| Declined | Client rejected the offered address |
| Inactive | Address offered but not yet acknowledged |
| ActiveReservation | IP assigned via reservation |

## Clearing Stale Leases

```powershell
# Remove a single expired lease
Remove-DhcpServerv4Lease -ScopeId 192.168.10.0 -IPAddress 192.168.10.55

# Remove all expired leases in a scope
Get-DhcpServerv4Lease -ScopeId 192.168.10.0 |
  Where-Object { $_.AddressState -eq "Expired" } |
  Remove-DhcpServerv4Lease

# Reconcile scope (fixes inconsistencies between DB and registry)
Repair-DhcpServerv4IPRecord -ScopeId 192.168.10.0 -Force
```

## Exporting and Importing Leases

```powershell
# Export lease database (full server)
Export-DhcpServer -File C:\dhcp-backup\dhcp-export.xml -Leases

# Export single scope
Export-DhcpServer -File C:\dhcp-backup\scope10-export.xml -ScopeId 192.168.10.0 -Leases

# Import on new/replacement server
Import-DhcpServer -File C:\dhcp-backup\dhcp-export.xml `
  -BackupPath C:\Windows\System32\dhcp\backup -Leases -Force
```

## Known Issues

- DNS records for expired leases linger if DNS dynamic update cleanup is not enabled. Enable scavenging on the DNS zone and confirm the DHCP server is authorized to update DNS.
- `Repair-DhcpServerv4IPRecord` marks inconsistent entries as declined; the address becomes available on the next scope cleanup cycle (default 1 hour).
