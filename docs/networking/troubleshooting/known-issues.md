---
tags:
  - troubleshooting
  - networking
  - known-issues
---
# Networking — Known Issues Reference

<div class="kb-summary">
Index of protocol-specific known issues and error codes for networking components. This top-level page links to per-protocol known-issues catalogs.

*Applies to: All network protocols in this KB*
</div>

```text
┌───────────────────────────────── Networking Protocols — Known Issues ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Index linking DNS, NFS, SMB, iSCSI, FC, TLS, LDAP known-issues pages             │   │
│   │            Scope: Layer 3 (IP/routing), Layer 4 (TCP/UDP), Layer 7 (app protocols)            │   │
│   │                           Management: N/A — documentation index only                          │   │
│   │                 Identify protocol layer -> Open known-issues page -> Diagnose                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Topic            │  │           Resource          │  │            Notes            │   │
│   │           Layer 3           │  │         Routing, VPN        │  │     Routing tables, MTU     │   │
│   │           Layer 4           │  │        TCP/UDP ports        │  │     Check firewall rules    │   │
│   │           Layer 7           │  │        App protocols        │  │     DNS/NFS/SMB/iSCSI/FC    │   │
│   │          Cross-cut          │  │             DNS             │  │    Root cause, many apps    │   │
│   │          Cross-cut          │  │           TLS/PKI           │  │      See security pages     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │     DNS page     │ Name resolution  │        N/A        │       N/A        │  protocols/dns   │   │
│   │  NFS/SMB pages   │  File protocols  │        N/A        │       N/A        │protocols/nfs,smb │   │
│   │  iSCSI/FC pages  │ Block protocols  │        N/A        │       N/A        │protocols/iscsi,fc│   │
│   │  TLS/LDAP pages  │Security protocols│        N/A        │       N/A        │protocols/tls,ldap│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: N/A — documentation index page, not a deployed system                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Layer 3        = IP routing layer; addressing and path selection                                     │
│  Layer 4        = TCP/UDP transport layer; ports and connection state                                 │
│  Layer 7        = application layer; protocol-specific behavior                                       │
│  MTU            = Maximum Transmission Unit; affects fragmentation                                    │
│  DNS            = translates names to IPs; root cause of many failures                                │
│  TLS            = encrypts and authenticates network connections                                      │
│  iSCSI          = block storage protocol over TCP/IP                                                  │
│  Fibre Channel  = dedicated block storage network protocol/fabric                                     │
│  NFS            = POSIX-style network file sharing protocol                                           │
│  SMB            = Windows-native network file sharing protocol                                        │
│  LDAP           = directory query and authentication protocol                                         │
│  Split-horizon  = different internal vs external DNS resolution                                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

For network issues, identify the protocol layer first before looking up specific errors:
- **Layer 3** (IP routing, VPN) → check routing tables, MTU, firewall logs
- **Layer 4** (TCP/UDP port) → check firewall rules, port open/close status
- **Layer 7** (application protocol) → check the specific protocol known-issues page below

## Protocol Known-Issues Pages

| Protocol | Known Issues |
|---|---|
| DNS | [DNS — Known Issues](protocols/dns/troubleshooting/known-issues/) |
| NFS | [NFS — Known Issues](protocols/nfs/troubleshooting/known-issues/) |
| SMB / CIFS | [SMB — Known Issues](protocols/smb/troubleshooting/known-issues/) |
| iSCSI | [iSCSI — Known Issues](protocols/iscsi/troubleshooting/known-issues/) |
| Fibre Channel | [FC — Known Issues](protocols/fibre-channel/troubleshooting/known-issues/) |
| TLS / SSL | [TLS — Known Issues](protocols/tls/troubleshooting/known-issues/) |
| LDAP / LDAPS | [LDAP — Known Issues](protocols/ldap/troubleshooting/known-issues/) |

## See also

- [Networking — Common Issues](index.md)
- [Brocade Fabric OS — Known Issues](../san/brocade/fabric-os/troubleshooting/known-issues/)
- [Cisco MDS — Known Issues](../san/cisco/mds/troubleshooting/known-issues/)
