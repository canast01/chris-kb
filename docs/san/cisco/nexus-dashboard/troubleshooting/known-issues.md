---
tags:
  - troubleshooting
  - nexus-dashboard
  - cisco
  - known-issues
---
# Cisco Nexus Dashboard — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Nexus Dashboard bugs, error codes, and workarounds covering cluster health, service deployment, and upgrade issues.

*Applies to: Nexus Dashboard 3.x*
</div>

```text
┌──────────────────────────────────────── Cisco Nexus Dashboard ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Unified management platform — hosts NDFC, NAE, and fabric assurance apps           │   │
│   │                  Protocols: HTTPS · REST API · gRPC telemetry · SSH · SNMP v3                 │   │
│   │                Management: ND web UI · REST API · NDFC fabric controller · NAE                │   │
│   │               ND cluster -> site onboarding -> NDFC/NAE app -> fabric management              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Platform          │  │    ND cluster (3+ nodes)    │  │      OVA or bare-metal      │   │
│   │         Fabric ctrl         │  │       NDFC (SAN / LAN)      │  │        Replaces DCNM        │   │
│   │          Assurance          │  │           NAE app           │  │      Policy + telemetry     │   │
│   │            Sites            │  │       Multi-site mgmt       │  │      MSO / NDO overlay      │   │
│   │          Telemetry          │  │       gRPC / streaming      │  │      Real-time metrics      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    ND cluster    │App host platform │     HTTPS 443     │   LDAP / local   │3-node HA required│   │
│   │       NDFC       │Fabric controller │    HTTPS / SSH    │    Role-based    │LAN and SAN modes │   │
│   │       NAE        │Network assurance │    gRPC / REST    │     API key      │ Pre/post-change  │   │
│   │       NDO        │Multi-site overlay│       HTTPS       │    LDAP / SSO    │  MSO successor   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: ND cluster nodes -> managed Cisco NX-OS/MDS switches -> physical DC fabric                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ND           = Nexus Dashboard; Cisco unified operations platform (3-node cluster)                   │
│  NDFC         = Nexus Dashboard Fabric Controller; successor to DCNM                                  │
│  NDFC-LAN     = NDFC in LAN mode; manages VXLAN/BGP EVPN underlay + overlay                           │
│  NDFC-SAN     = NDFC in SAN mode; manages Cisco MDS FC zoning and VSANs                               │
│  NAE          = Network Assurance Engine; validates fabric policy and telemetry                       │
│  NDO          = Nexus Dashboard Orchestrator; multi-site VXLAN policy management                      │
│  Site         = a fabric registered with ND; can span multiple DCs                                    │
│  gRPC         = Google RPC; used for streaming telemetry from NX-OS to ND/NAE                         │
│  Micro-seg.   = endpoint policy enforcement at VM/port level via NAE                                  │
│  Assurance    = continuous validation of network state against intended policy                        │
│  MSO          = Multi-Site Orchestrator; predecessor to NDO                                           │
│  Fabric template = NDFC config skeleton for VXLAN/BGP overlay deployment                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Nexus Dashboard cluster health: ND UI → Infrastructure → Cluster Configuration → Health.
- ND runs Kubernetes-based services; pod health: `acs health` from ND admin SSH.
- etcd quorum is critical — never lose more than 1 of 3 ND cluster nodes simultaneously.

## Cluster Health

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Node `Unavailable` in ND cluster | ND 3.x | Node OOM, disk full, or network partition | Check node: `kubectl get pods --all-namespaces`; check disk: `df -h` | N/A |
| etcd cluster `Degraded` with one node down | ND 3.x | etcd quorum requires 2/3 nodes | Restore failed node; do not shut down another node with etcd degraded | N/A |
| `Clock skew` alarm on ND node | ND 3.x | NTP offset between ND nodes | Sync all nodes to same NTP source; verify: `chronyc tracking` | N/A |

## Services

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| NDFC (Nexus Dashboard Fabric Controller) service `Degraded` | ND 3.x | Insufficient memory for NDFC pod | Verify ND node memory meets minimum for NDFC; scale node count | N/A |
| ND Insights service not collecting fabric data | ND 3.x | APIC or switch credentials incorrect in site configuration | Update site credentials in ND → Sites → Edit | N/A |

## Upgrade

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| ND upgrade stuck at `Upgrading node 2 of 3` | ND 3.x | Node not rebooting cleanly during rolling upgrade | SSH to stuck node; check `journalctl -b` for boot errors; manually reboot | N/A |
| Post-upgrade service pods in `CrashLoopBackOff` | ND 3.x | Service requires manual migration step post-upgrade | Check ND upgrade guide for post-upgrade service migration steps | N/A |

## See also

- [Cisco Nexus Dashboard — Common Issues](common-issues/)
- [Cisco DCNM — Known Issues](../../cisco-dcnm/troubleshooting/known-issues.md)
- [Cisco MDS — Known Issues](../../mds/troubleshooting/known-issues.md)
