---
tags:
  - snapmirror
  - netapp
  - networking
  - firewall
  - ports
  - replication
---
# NetApp SnapMirror — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for NetApp SnapMirror. SnapMirror is a replication feature built into ONTAP — it is not a separate product. All traffic flows between ONTAP intercluster LIFs. The only ports required are the ONTAP cluster peering and replication ports.

*Applies to: ONTAP 9.x (SnapMirror and SnapVault)*
</div>

## Network Zones

```text
Site A                                    Site B
┌─────────────────────────────┐           ┌─────────────────────────────────────────────────────────────┐
│  ONTAP Cluster A            │           │  ONTAP Cluster B                                            │
│  ┌────────────────────┐     │  WAN/IP   │  ┌───────────────────┐                                      │
│  │ Intercluster LIF   │─────┼──────────▶│  │ Intercluster LIF  │                                      │
│  │ (dedicated or mgmt)│◀────┼───────────┤  │                   │                                      │
│  └────────────────────┘     │  11104/   │  └───────────────────┘                                      │
│                             │  11105    │                                                             │
└─────────────────────────────┘           └─────────────────────────────────────────────────────────────┘
```

## Before you begin

- SnapMirror traffic uses **intercluster LIFs** — dedicated data LIFs configured for intercluster role, or management LIFs if no dedicated intercluster LIF is configured.
- Ports must be open **bidirectionally** between both clusters (each side initiates transfers at different points).
- SnapMirror over IP requires routable connectivity between intercluster LIFs across the WAN/routed network.
- For SnapMirror over FC (SMBC / MetroCluster), there are no IP port requirements — traffic runs over Fibre Channel fabric.

## Intercluster Replication Ports

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 11104 | TCP | Intercluster LIF (Cluster A) | Intercluster LIF (Cluster B) | SnapMirror control traffic — peering negotiation |
| 11105 | TCP | Intercluster LIF (Cluster A) | Intercluster LIF (Cluster B) | SnapMirror data transfer (Snapshot block transfer) |
| 443 | TCP | Intercluster LIF | Intercluster LIF (remote) | Cluster peering authentication and management |

## Cloud SnapMirror (SnapMirror to Cloud / S3)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | ONTAP cluster management LIF | AWS S3 / StorageGRID / ONTAP S3 endpoint | SnapMirror to Cloud control and data path |

## ONTAP System Manager / SnapCenter (Management)

SnapMirror relationships are managed through ONTAP System Manager or SnapCenter. See:
- [NetApp ONTAP — Ports](../../ontap/architecture/ports/) for ONTAP management port requirements
- [NetApp SnapCenter — Ports](../../snapcenter/architecture/ports/) for backup orchestration

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Cluster A intercluster LIF | Cluster B intercluster LIF | 11104, 11105 | Both directions |
| ONTAP mgmt LIF | Remote cluster mgmt LIF | 443 | Cluster peer setup |
| ONTAP intercluster LIF | Cloud S3 endpoint | 443 | SnapMirror to Cloud only |

## Verify

```bash
# From ONTAP CLI on source cluster — ping intercluster LIF on destination
network ping -lif <source-intercluster-lif> -destination <dest-intercluster-lif-ip>

# Check cluster peer health
cluster peer show
cluster peer health show

# Check SnapMirror relationship status
snapmirror show -fields state,healthy,lag-time

# Verify intercluster LIF status
network interface show -role intercluster
```

## See also

- [NetApp ONTAP — Ports](../../ontap/architecture/ports/)
- [NetApp SnapCenter — Ports](../../snapcenter/architecture/ports/)
- [NetApp ONTAP — Architecture](../../ontap/architecture/how-it-works/)
