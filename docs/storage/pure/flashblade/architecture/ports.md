---
tags:
  - flashblade
  - pure-storage
  - networking
  - firewall
  - ports
---
# Pure Storage FlashBlade — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Pure Storage FlashBlade. FlashBlade provides unified fast file and object storage. Covers management access, NFS, SMB, S3 object, replication, and Pure1 cloud telemetry.

*Applies to: FlashBlade//S, FlashBlade//E, Purity//FB 4.x*
</div>
![Pure Storage FlashBlade — Ports and Network Requirements](../../../../assets/storage-pure-flashblade-architecture-ports.svg)


```d2
direction: right

center: "FlashBlade" {shape: hexagon}
network_zones: "Network Zones" {shape: rectangle}
management_inbound: "Management (Inbound)" {shape: rectangle}
data_access_protocols: "Data Access Protocols" {shape: rectangle}
replication_flashblade_to_flashblade: "Replication (FlashBlade to FlashBlade)" {shape: rectangle}
pure1_cloud_telemetry_outbound: "Pure1 Cloud Telemetry (Outbound)" {shape: rectangle}
vsphere_integration_optional: "vSphere Integration (Optional)" {shape: rectangle}

center -> network_zones
center -> management_inbound
center -> data_access_protocols
center -> replication_flashblade_to_flashblade
center -> pure1_cloud_telemetry_outbound
center -> vsphere_integration_optional
```

## Network Zones

```
┌──────────────────┐         ┌──────────────────────────────────────────────────────────────────────────┐
│  Admin browsers  │──443───▶│  FlashBlade                                                              │
│  REST API clients│──443───▶│  ┌─────────────┐  ┌──────────────────┐                                   │
│  Pure1 cloud     │◀──443───│  │ Blade Mgmt  │  │  Data Blades     │                                   │
└──────────────────┘         │  │ Network     │  │  (NFS/SMB/S3)    │    │
                             │  └─────────────┘  └──────────────────┘    │
                             └────────────────────────────────────────────┘
                                                         │
                             ┌───────────┬──────────────┬┤
                           NFS         SMB            S3
                          2049         445           9000
```

## Management (Inbound)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin browsers, REST API clients | Purity//FB web UI and REST API |
| 22 | TCP | Jump hosts | SSH — diagnostic access to FlashBlade OS |

## Data Access Protocols

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 2049 | TCP | NFS client hosts | NFS file access |
| 111 | TCP/UDP | NFS client hosts | Portmapper / rpcbind for NFS mount |
| 635 | TCP/UDP | NFS client hosts | NFS mountd |
| 2049 | UDP | NFS client hosts | NFS (UDP — legacy clients) |
| 445 | TCP | SMB client hosts | SMB file access |
| 9000 | TCP | S3 client applications | S3 object API (HTTP) |
| 443 | TCP | S3 client applications | S3 object API (HTTPS) — if SSL-enabled VIP configured |

## Replication (FlashBlade to FlashBlade)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | FlashBlade (source) replication VIP | FlashBlade (target) replication VIP | ActiveDR / async replication control and data transfer |

## Pure1 Cloud Telemetry (Outbound)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | FlashBlade management IP | pure1.purestorage.com | Pure1 telemetry, health monitoring, and proactive support |

## vSphere Integration (Optional)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | vCenter Server | FlashBlade management IP | VASA provider — vSphere storage policy integration |
| 443 | TCP | FlashBlade management IP | vCenter Server | vSphere event subscription |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin browsers | FlashBlade mgmt IP | 443, 22 | Management |
| NFS clients | FlashBlade data VIP | 2049, 111, 635 | NFS data access |
| SMB clients | FlashBlade data VIP | 445 | SMB data access |
| S3 clients | FlashBlade data VIP | 9000 (or 443) | Object storage |
| FlashBlade (replication) | Remote FlashBlade | 443 | Replication |
| FlashBlade mgmt | pure1.purestorage.com | 443 | Telemetry — required for proactive support |

## Verify

```bash
# From admin workstation — test FlashBlade UI
curl -sk -o /dev/null -w "%{http_code}" https://<flashblade-mgmt-ip>/

# From NFS client — test mount
showmount -e <flashblade-nfs-vip>
mount -t nfs <flashblade-nfs-vip>:/path/to/share /mnt/test

# From S3 client — test object access
curl -sk -o /dev/null -w "%{http_code}" http://<flashblade-s3-vip>:9000/

# From FlashBlade — verify Pure1 connectivity
# (via Purity//FB CLI)
purealertalert test
```

## See also

- [Pure Storage FlashBlade — Architecture](how-it-works/)
