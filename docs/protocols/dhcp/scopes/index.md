# DHCP Scopes


<div class="kb-summary">
DHCP Scopes reference covering Overview, Creating a Scope, Exclusions, Scope Planning Reference, Superscopes and 2 more sections.
</div>

        SCOPE STRUCTURE
```
┌──────────────────────────────────────────────────────────────┐
│  Scope: Corp LAN – Floor 1 (192.168.10.0/24)                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Range:  192.168.10.1 – 192.168.10.254               │    │
│  │  ┌─────────────────────────────────────────────┐     │    │
│  │  │ Exclusions: .1–.20  (network devices, GW)  │     │    │
│  │  │             .21–.50 (servers, static)       │     │    │
│  │  │             .51–.99 (printers, AP, resvd)   │     │    │
│  │  └─────────────────────────────────────────────┘     │    │
│  │  Dynamic pool: .100 – .254 (workstations)             │    │
│  │  Lease time:  8 days (servers) / 24h (workstations)   │    │
│  │                                                       │    │
│  │  Options delivered with lease:                        │    │
│  │  003 Router:  192.168.10.1                            │    │
│  │  006 DNS:     10.0.0.53, 10.0.0.54                    │    │
│  │  015 Domain:  corp.local                              │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## Overview

A DHCP scope defines the pool of IP addresses available for a subnet. Scopes include a range, exclusions, lease duration, and options. Superscopes group multiple scopes for multinet subnets. DHCP relay (IP helper) is required when the DHCP server is on a different subnet from clients.

## Creating a Scope

```powershell
# Create a new scope
Add-DhcpServerv4Scope `
  -Name "Corp LAN - Floor 1" `
  -StartRange 192.168.10.1 `
  -EndRange 192.168.10.254 `
  -SubnetMask 255.255.255.0 `
  -LeaseDuration 8.00:00:00 `
  -State Active

# Set common options on the new scope
Set-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 3 -Value 192.168.10.1
Set-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 6 -Value 10.0.0.53, 10.0.0.54
Set-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 15 -Value "corp.local"
```

## Exclusions

```powershell
# Exclude static range from the dynamic pool
Add-DhcpServerv4ExclusionRange `
  -ScopeId 192.168.10.0 `
  -StartRange 192.168.10.1 `
  -EndRange 192.168.10.20

# View current exclusions
Get-DhcpServerv4ExclusionRange -ScopeId 192.168.10.0

# Remove an exclusion range
Remove-DhcpServerv4ExclusionRange `
  -ScopeId 192.168.10.0 `
  -StartRange 192.168.10.1 `
  -EndRange 192.168.10.20
```

## Scope Planning Reference

| Block | Suggested Use | Example Range |
|-------|---------------|---------------|
| .1 - .10 | Network devices (gateways, switches) | 192.168.10.1–10 |
| .11 - .50 | Servers (statically assigned, excluded) | 192.168.10.11–50 |
| .51 - .100 | Printers, APs, reservations | 192.168.10.51–100 |
| .101 - .254 | Dynamic DHCP pool for workstations | 192.168.10.101–254 |

## Superscopes

```powershell
# Create a superscope grouping two scopes (multinet)
Add-DhcpServerv4Superscope `
  -SuperscopeName "Building-A-Multinet" `
  -ScopeId 192.168.10.0, 192.168.11.0

# View superscopes and their member scopes
Get-DhcpServerv4Superscope

# Remove a scope from a superscope
Set-DhcpServerv4Scope -ScopeId 192.168.11.0 -SuperscopeName ""
```

## DHCP Relay (IP Helper)

DHCP relay forwards broadcast DHCP packets from clients on remote subnets to the DHCP server. Configure on the Layer 3 switch or router interface facing the client subnet.

```bash
# Cisco IOS — add IP helper on the client-facing interface
interface GigabitEthernet0/1
  ip helper-address 10.0.0.10   ! primary DHCP server
  ip helper-address 10.0.0.11   ! secondary DHCP server
```

```powershell
# Verify scope is active and check utilization
Get-DhcpServerv4ScopeStatistics -ScopeId 192.168.10.0

# Resize an existing scope
Set-DhcpServerv4Scope `
  -ScopeId 192.168.10.0 `
  -StartRange 192.168.10.1 `
  -EndRange 192.168.10.254
```

## Known Issues

- A scope shows 0% utilization but clients report "no IP available": check that `Add-DhcpServerv4ExclusionRange` has not accidentally excluded the entire pool.
- Superscope members must each have their own default gateway option; the superscope itself cannot hold options.
- After resizing a scope, run `Repair-DhcpServerv4IPRecord -ScopeId -Force` to reconcile the lease database with the new bounds.
