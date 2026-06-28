---
tags:
  - pure1
  - pure-storage
  - networking
  - firewall
  - ports
  - monitoring
---
# Pure1 — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Pure1 (Pure Storage cloud management and analytics SaaS). Pure1 requires only outbound HTTPS from each managed array to pure1.purestorage.com. No inbound connection from Pure to on-premises infrastructure is required.

*Applies to: Pure1 (cloud portal — no on-premises install)*
</div>
![Pure1 — Ports and Network Requirements](../../../../assets/storage-pure-pure1-architecture-ports.svg)





```d2
direction: right

center: "Pure1" {shape: hexagon}
how_it_works: "How It Works" {shape: rectangle}
outbound_arrays_to_pure1_cloud_requi: "Outbound — Arrays to Pure1 Cloud (Required)" {shape: rectangle}
admin_access_saas: "Admin Access (SaaS)" {shape: rectangle}
firewall_zone_summary: "Firewall Zone Summary" {shape: rectangle}
verify: "Verify" {shape: rectangle}

center -> how_it_works
center -> outbound_arrays_to_pure1_cloud_requi
center -> admin_access_saas
center -> firewall_zone_summary
center -> verify
```

## How It Works

Pure1 is a fully SaaS-based cloud management platform. Each FlashArray and FlashBlade array ships with a built-in phone-home agent that establishes an **outbound-only** TLS connection to Pure's cloud. Administrators access Pure1 via browser at `pure1.purestorage.com` — no on-premises software is needed.

## Outbound — Arrays to Pure1 Cloud (Required)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | FlashArray management IP | pure1.purestorage.com | Telemetry, health data, proactive support, capacity forecasting |
| 443 | TCP | FlashBlade management IP | pure1.purestorage.com | Same as FlashArray |

## Admin Access (SaaS)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | pure1.purestorage.com | Admin browser — Pure1 dashboard, AI-driven analytics, support cases |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| FlashArray mgmt IP | pure1.purestorage.com | 443 | Outbound only — no inbound from Pure cloud |
| FlashBlade mgmt IP | pure1.purestorage.com | 443 | Outbound only |
| Admin browsers | pure1.purestorage.com | 443 | SaaS portal |

## Verify

```bash
# From FlashArray or FlashBlade management IP — test Pure1 connectivity
curl -sk -o /dev/null -w "%{http_code}" https://pure1.purestorage.com/

# From FlashArray CLI — verify phone-home status
puremessage test

# From FlashBlade CLI — verify Pure1 telemetry
purealertalert test

# Check outbound 443 from array management network to pure1.purestorage.com
nc -zv pure1.purestorage.com 443
```

## See also

- [Pure1 — Architecture](how-it-works/)
