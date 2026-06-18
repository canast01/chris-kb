---
tags:
  - evergreen-one
  - pure-storage
  - networking
  - firewall
  - ports
  - storage-as-a-service
---
# Pure Storage Evergreen//One — Ports and Network Requirements

<div class="kb-summary">
Pure Storage Evergreen//One is a Storage as a Service (STaaS) consumption model — Pure-owned hardware is deployed on customer premises and managed by Pure Storage. No separate Evergreen//One appliance exists; port requirements are identical to the underlying FlashArray or FlashBlade deployed.

*Applies to: Evergreen//One STaaS for FlashArray and FlashBlade*
</div>

```text
┌───────────────────────────────────────── Pure Evergreen//ONE ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Evergreen//ONE: Storage as a Service subscription delivered on Pure FlashArray/FlashBlade   │   │
│   │                        Protocols: FC · iSCSI · NVMe-oF · NFS · SMB · S3                       │   │
│   │                              Management: Pure1 / Purity REST API                              │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Hardware          │  │         On-prem Pure        │  │          Pure-owned         │   │
│   │           Billing           │  │        Committed TiB        │  │         Monthly sub.        │   │
│   │           Refresh           │  │        Non-disruptive       │  │        Pure delivers        │   │
│   │          Management         │  │          Pure1 SaaS         │  │         AI analytics        │   │
│   │           Support           │  │        24x7 proactive       │  │          AI-driven          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      Pure1       │   SaaS portal    │       HTTPS       │     SSO/SAML     │   AI analytics   │   │
│   │    FlashArray    │    Block/file    │    FC/iSCSI/NFS   │  CHAP/Kerberos   │     All-NVMe     │   │
│   │    FlashBlade    │   File/object    │     NFS/SMB/S3    │   Kerberos/IAM   │   Parallel I/O   │   │
│   │  ActiveCluster   │ Sync replication │    Internal RPC   │   Certificate    │     Zero RPO     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Pure FlashArray or FlashBlade on-prem (Pure-owned) · Pure1 cloud · WAN to Pure           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Evergreen//ONE     = Pure STaaS; Pure-owned hardware on customer premises with subscription billi  │
│    Pure1              = Pure Storage cloud management portal; AI-based analytics and capacity planni  │
│    Non-disruptive upgrade = hardware upgrade without host I/O interruption; Pure handles logistics    │
│    Committed TiB      = minimum subscribed capacity; billed monthly regardless of actual usage        │
│    Burst capacity     = additional capacity above commitment; no pre-ordering; billed as consumed     │
│    Hardware refresh   = Pure delivers and installs new controllers and shelves on 3-year cadence      │
│    Purity//FA         = FlashArray OS; unified block and file with NVMe-native architecture           │
│    Purity//FB         = FlashBlade OS; object and file storage with massive parallel throughput       │
│    AI copilot         = Pure1 AI feature; recommends workload placement and anomaly remediation       │
│    TaaS               = Technology as a Service; hardware ownership stays with Pure throughout subsc  │
│    ActiveCluster      = sync stretch replication included; ActiveDR async replication optional        │
│    SAML SSO           = Pure1 supports SAML 2.0; identity provider integrates with corporate IdP      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## How It Works

Evergreen//One deploys Pure hardware on-premises under a consumption billing model. Pure Storage manages the hardware lifecycle, capacity planning, and upgrades. The array runs standard Purity software — the only operational difference is that Pure personnel access the system for maintenance via the Pure1 cloud (outbound-only from the array).

## Port Requirements — Same as Underlying Array

| Component | Ports Page |
|---|---|
| FlashArray (block storage) | [Pure Storage FlashArray — Ports](../flasharray/architecture/ports/) |
| FlashBlade (file/object) | [Pure Storage FlashBlade — Ports](../flashblade/architecture/ports/) |
| Pure1 cloud management | [Pure1 — Ports](../pure1/architecture/ports/) |

## Evergreen//One Specific — Pure Cloud Connectivity (Required)

Pure requires uninterrupted outbound access to Pure1 for remote management, metering, and capacity tracking:

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | FlashArray/FlashBlade mgmt IP | pure1.purestorage.com | Required for STaaS billing metering, remote management, capacity enforcement |

> **Note:** Blocking port 443 to pure1.purestorage.com on Evergreen//One arrays may trigger a service contract breach — Pure requires continuous phone-home connectivity.

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Array mgmt IP | pure1.purestorage.com | 443 | Mandatory for Evergreen//One STaaS metering |
| Client hosts | Array data IPs | Per protocol | Same as FlashArray or FlashBlade standard ports |

## See also

- [Pure Storage Evergreen//One — Architecture](how-it-works/)
