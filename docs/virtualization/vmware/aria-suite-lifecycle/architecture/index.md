# Aria Suite Lifecycle Architecture

## Overview

Aria Suite Lifecycle (LCM) is a management appliance that deploys, upgrades, and manages the entire VMware Aria (formerly vRealize) product suite from a single control plane. LCM eliminates the need to update each Aria product independently.

## Core Components

| Component | Role |
|---|---|
| LCM Appliance | Central orchestration, UI, API, Locker (certificate/password vault) |
| Workspace ONE Access (VIDM) | Identity provider and SSO for all Aria products |
| vRealize Easy Installer | Bootstrap ISO for initial multi-product deployment |
| NFS Share | Binary repository (downloaded product bundles) and snapshot storage |
| NTP Server | Time synchronisation — mandatory for certificate validity |
| DNS | Forward and reverse resolution required for every node FQDN |

## LCM Appliance Internal Architecture

```
LCM Appliance VM
├── Lifecycle Manager Service (Java)
│   ├── Orchestration engine — handles upgrade/deploy workflows
│   ├── REST API (port 443)
│   └── Embedded PostgreSQL (configuration database)
├── Locker
│   ├── Certificate store (encrypted at rest)
│   └── Password vault for managed product credentials
└── NFS mount (/data) — binary bundles and product snapshots
```

The `/data` partition is the most disk-intensive — size the NFS share with at least 200 GB per major product version stored.

## Supported Products

LCM manages the following Aria products:

| Product | Notes |
|---|---|
| Aria Operations (vROps) | Monitoring and analytics |
| Aria Automation (vRA) | Self-service cloud automation |
| Aria Log Insight (vRLI) | Log management and analytics |
| Aria Operations for Networks (vRNI) | Network visibility |
| Workspace ONE Access (VIDM) | Identity — always deployed first |

## Deployment Models

- **Standalone**: LCM appliance + individual product VMs; suitable for smaller environments
- **Clustered products**: Aria Operations and Aria Automation can be deployed in HA clusters; LCM manages all nodes
- **Multi-environment**: Single LCM can manage multiple environments (e.g., Prod + Pre-Prod) with separate data centres

## Network Requirements

| Traffic | Port | Notes |
|---|---|---|
| Admin browser to LCM | 443 (HTTPS) | Management access |
| LCM to vCenter | 443 | OVA deployment and VM management |
| LCM to NSX-T | 443 | Network provisioning (optional) |
| LCM to NFS | 2049 (NFS) | Binary repo mount |
| LCM to managed products | 443 | Health polling and upgrade orchestration |
| LCM to internet | 443 | Bundle downloads (or use a proxy / offline depot) |

## High Availability

LCM itself runs as a single VM — there is no HA mode for LCM. Protect it via:
- VM snapshot before every upgrade
- Daily configuration backup via LCM's built-in backup feature
- NFS share backed up independently (contains all product binaries)
