# DHCP Options


<div class="kb-summary">
DHCP Options reference covering Overview, Common Option Codes, Setting Scope-Level Options, Setting Server-Level Options, Vendor-Specific Options (043) and 2 more sections.
</div>

        DHCP OPTION HIERARCHY (most specific wins)
```
┌──────────────────────────────────────────────────────────────┐
│  Server-level options (apply to ALL scopes)                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  006 DNS: 10.0.0.53, 10.0.0.54  (server-wide)        │    │
│  └──────────────────────────┬─────────────────────────┘    │
│                             │ inherited unless overridden    │
│  Scope-level options        ▼                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  003 Router: 192.168.10.1  (per subnet)              │    │
│  │  015 Domain: corp.local                              │    │
│  └──────────────────────────┬─────────────────────────┘    │
│                             │ inherited unless overridden    │
│  Reservation-level options  ▼                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  006 DNS: 10.0.0.60  (overrides for this MAC/IP)     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Common codes:  003=gateway  006=DNS  042=NTP                │
│                 066=TFTP server  067=PXE boot file           │
└──────────────────────────────────────────────────────────────┘
```

## Overview

DHCP options deliver network configuration alongside an IP address. Options can be set at the server level (apply to all scopes), scope level (apply to one subnet), reservation level (apply to one client), or class level (apply to clients presenting a matching vendor or user class).

## Common Option Codes

| Code | Name | Typical Value |
|------|------|---------------|
| 003 | Router | Default gateway IP |
| 006 | DNS Servers | Up to 4 DNS server IPs |
| 015 | DNS Domain Name | `corp.local` |
| 043 | Vendor-Specific Info | PXE, VoIP phone config |
| 044 | WINS Servers | WINS server IP |
| 046 | WINS Node Type | 0x8 (H-node) |
| 066 | Boot Server Hostname | PXE/TFTP server |
| 067 | Bootfile Name | `pxelinux.0` |

## Setting Scope-Level Options

```powershell
# Set default gateway for a scope
Set-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 3 -Value 192.168.10.1

# Set DNS servers for a scope
Set-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 6 -Value 10.0.0.53, 10.0.0.54

# Set DNS domain name
Set-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 15 -Value "corp.local"

# View all options on a scope
Get-DhcpServerv4OptionValue -ScopeId 192.168.10.0
```

## Setting Server-Level Options

```powershell
# Server-level DNS servers (apply to all scopes unless overridden)
Set-DhcpServerv4OptionValue -OptionId 6 -Value 10.0.0.53, 10.0.0.54

# View all server-level options
Get-DhcpServerv4OptionValue

# Show effective options for a scope (includes inherited server options)
Get-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -All
```

## Vendor-Specific Options (043)

```powershell
# Define a vendor class (e.g., for Cisco VoIP phones)
Add-DhcpServerv4Class -Name "CiscoPhone" -Type Vendor `
  -Data "Cisco Systems, Inc. IP Phone"

# Set vendor-specific option for that class
Set-DhcpServerv4OptionValue `
  -ScopeId 192.168.30.0 `
  -VendorClass "CiscoPhone" `
  -OptionId 43 `
  -Value ([byte[]](0x01,0x04,0x0A,0x00,0x00,0x0A))
```

## Removing Options

```powershell
# Remove a scope-level option (falls back to server-level)
Remove-DhcpServerv4OptionValue -ScopeId 192.168.10.0 -OptionId 6

# Remove a server-level option
Remove-DhcpServerv4OptionValue -OptionId 15

# Remove a reservation-level option
Remove-DhcpServerv4OptionValue `
  -ScopeId 192.168.10.0 `
  -ReservedIP 192.168.10.200 `
  -OptionId 6
```

## Known Issues

- Scope options override server options for the same code. If a client is getting unexpected DNS servers, check for a conflicting scope-level option 006.
- Vendor option 043 must match the exact vendor class string the client broadcasts in option 060. Capture a packet with Wireshark to verify the client's `Vendor Class Identifier` before configuring.
- Option 051 (lease time) set at scope level overrides the scope's configured lease duration shown in the DHCP console. Use `Get-DhcpServerv4OptionValue -All` to detect hidden overrides.
