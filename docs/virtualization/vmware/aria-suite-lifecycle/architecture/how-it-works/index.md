# Aria Suite Lifecycle — How It Works

## Overview

Aria Suite Lifecycle (LCM) is a management appliance that deploys, upgrades, and manages the entire VMware Aria product suite from a single control plane. LCM eliminates per-product upgrade complexity by orchestrating pre-checks, snapshots, binary staging, sequential node upgrades, and post-checks as a single audited workflow. All credentials and certificates are stored in the integrated **Locker** vault.

## Product Management Topology

```mermaid
graph TB
  LCM["Aria Suite Lifecycle\n(LCM appliance)"]
  LCM --> VROPS["Aria Operations"]
  LCM --> VRLI["Aria Ops for Logs"]
  LCM --> VRA["Aria Automation"]
  LCM --> VRNI["Aria Ops for Networks"]
  LCM --> REPO["Product Binaries Repo\n(NFS /data)"]
  ADMIN(["vSphere Admin"]) -->|"web UI"| LCM
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class LCM mgmt
  class VROPS,VRLI,VRA,VRNI ctrl
  class ADMIN host
```

## Core Components

| Component | Role |
|---|---|
| LCM Appliance | Central orchestration, UI, REST API, Locker vault |
| Workspace ONE Access (VIDM) | Identity provider and SSO for all Aria products |
| vRealize Easy Installer | Bootstrap ISO for initial multi-product deployment |
| NFS Share | Binary repository (`.pak` files) and snapshot storage |
| NTP Server | Time synchronisation — mandatory; certificate operations fail on >5s skew |
| DNS | Forward + reverse resolution required for every node FQDN |

## Upgrade Sequencing

Always upgrade in this order to avoid dependency conflicts:

1. Aria Suite Lifecycle (LCM itself)
2. Workspace ONE Access (VIDM) — identity provider must be upgraded first
3. Aria Operations for Logs
4. Aria Operations
5. Aria Automation

## Upgrade Workflow (per product)

1. **Pre-check** — validates DNS, NTP, disk space, NFS, vCenter reachability
2. **Snapshot** — takes VM snapshots of all product appliances (rollback point)
3. **Binary stage** — copies upgrade bundle from NFS to product appliances
4. **Upgrade** — runs in-product upgrade agent; clustered products upgrade node by node
5. **Post-check** — verifies services are running and health indicators are green
6. **Rollback** — if post-check fails, LCM reverts to pre-upgrade snapshots

## Deployment Pre-Requisites

| Prerequisite | Why Required | Verification |
|---|---|---|
| DNS A + PTR records for every FQDN | LCM agents communicate by FQDN; PTR required for SSO | `nslookup <fqdn>` from LCM appliance |
| NTP delta < 5 seconds | Certificate operations fail on time skew | `chronyc tracking` on LCM |
| NFS share at `/data` | Stores `.pak` binary files | `df -h /data && touch /data/.test` |
| vCenter service account | LCM deploys OVAs via vCenter API | Test in LCM → Settings → vCenter |
| CA-signed certificate with full chain | Locker imports require full chain | `openssl verify -CAfile chain.pem leaf.pem` |
| VIDM registered or deployed | All Aria products use VIDM for SSO | `curl -sk https://vidm.corp.local/SAAS/API/1.0/REST/system/health` |

## Product Version Matrix

| Product | Current Version | Min LCM Version | EOS Date |
|---|---|---|---|
| Aria Suite Lifecycle | 8.16 | — | Nov 2026 |
| Aria Operations | 8.17 | 8.14 | Nov 2026 |
| Aria Operations for Logs | 8.16 | 8.14 | Nov 2026 |
| Aria Automation | 8.17 | 8.14 | Nov 2026 |
| Workspace ONE Access | 23.09 | 8.12 | Sep 2025 |

## LCM API Quick Reference

```bash
# Authenticate
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.corp.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# List all environments
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.corp.local/lcm/lcmservice/api/v2/environments" | \
  jq '.[] | {name: .environmentName, health: .environmentHealth}'

# Trigger upgrade
curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.corp.local/lcm/lcmservice/api/v2/environments/<env-id>/products/<product-id>/upgrade" \
  -H "Content-Type: application/json" \
  -d '{"targetVersion":"8.17.0","snapshotBeforeUpgrade":true}'
```

| API Path | Purpose |
|---|---|
| `/lcm/authz/api/v2` | Authentication — login and token management |
| `/lcm/lcmservice/api/v2/environments` | Environment and product inventory |
| `/lcm/lcmservice/api/v2/requests` | Request tracking and audit |
| `/lcm/locker/api/v2/certificates` | Locker — certificate management |
| `/lcm/locker/api/v2/passwords` | Locker — password management |
