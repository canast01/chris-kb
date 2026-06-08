# SMB — Sessions

```text
┌────────────┐                              ┌───────────────────────────────────────────────────────────┐
│  Client    │                              │   SMB Server                                              │
└─────┬──────┘                              └────────┬──────────────────────────────────────────────────┘
```
```powershell

## Overview

An SMB session is established after a client authenticates to a server. Sessions can be inspected, disconnected, and constrained via PowerShell and legacy tools. Understanding active sessions is essential for access audits, capacity planning, and incident response.

| Command | Purpose |
|---|---|
| `Get-SmbSession` | List active SMB sessions (PowerShell) |
| `net session` | List or disconnect sessions (legacy) |
| `Get-SmbConnection` | List outbound SMB connections from this host |
| `Get-SmbServerConfiguration` | View SMB signing and version settings |

## Listing and Managing Sessions

```

```powershell
## List all active SMB sessions
Get-SmbSession

## Show session details including client IP and username
Get-SmbSession | Select-Object SessionId, ClientComputerName, ClientUserName, NumOpens, SecondsExists

## Close a specific session by ID
Close-SmbSession -SessionId 17179869218 -Force

## Close all sessions from a specific client
Get-SmbSession | Where-Object { $_.ClientComputerName -eq "192.168.1.55" } |
    Close-SmbSession -Force
```
```bash
## List all active sessions (legacy)
net session

## Disconnect a specific session
net session \\192.168.1.55 /DELETE

## Disconnect all sessions
net session /DELETE
```
```powershell
## Check current server signing settings
Get-SmbServerConfiguration | Select-Object RequireSecuritySignature, EnableSecuritySignature

## Require signing on the server (clients without signing cannot connect)
Set-SmbServerConfiguration -RequireSecuritySignature $true -Force

## Check client signing settings
Get-SmbClientConfiguration | Select-Object RequireSecuritySignature, EnableSecuritySignature

## Require signing on the client side
Set-SmbClientConfiguration -RequireSecuritySignature $true -Force
```
```powershell
## Check which SMB versions are enabled on the server
Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol, EnableSMB2Protocol

## Disable SMB1 (do not re-enable unless required for legacy devices)
Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force

## Enable SMB2/3
Set-SmbServerConfiguration -EnableSMB2Protocol $true -Force

## Check active dialect of an established session
Get-SmbSession | Select-Object ClientComputerName, Dialect
```
```powershell
## View current idle timeout settings (AutoDisconnectTimeout in minutes, 0 = never)
Get-SmbServerConfiguration | Select-Object AutoDisconnectTimeout

## Set idle session timeout to 15 minutes
Set-SmbServerConfiguration -AutoDisconnectTimeout 15 -Force

## View maximum connections (0 = unlimited for domain editions)
Get-SmbShare -Name "Finance" | Select-Object ConcurrentUserLimit

## Set per-share connection limit
Set-SmbShare -Name "Finance" -ConcurrentUserLimit 100 -Force
```
```powershell
## List all open files across all shares
Get-SmbOpenFile | Select-Object FileId, SessionId, ShareRelativePath, ClientComputerName

## Close a specific open file (use when a locked file blocks access)
Close-SmbOpenFile -FileId 4503599627432131 -Force

## Find open files by share path
Get-SmbOpenFile | Where-Object { $_.ShareRelativePath -like "*Finance*" }
```
