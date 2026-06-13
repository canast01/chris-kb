---
tags:
  - architecture
  - pure
---
# Pure1 — Design Standards

<div class="kb-summary">
Array naming standards, team access model, alert threshold configuration, and operational baselines for Pure1.

*Applies to: Pure1*
</div>

```text
┌────────────────────────────────────── Pure1 — Design Standards ───────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Registration Standards            │  │            Operational Standards            │   │
│   │            All arrays registered             │  │             Email alerts active             │   │
│   │              Phonehome verified              │  │                Review weekly                │   │
│   │              TCP 443 unblocked               │  │              Auto-case enabled              │   │
│   │               Service account                │  │            Capacity plan monthly            │   │
│   │             Tag by env+location              │  │                Alert to ITSM                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  All arrays require TCP 443 outbound to pure1.purestorage.com · Pure handles the rest                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Phonehome verified = Array shows Connected in Pure1; data age < 2 minutes                            │
│  TCP 443 unblocked = Firewall allows outbound from array management IP to Pure cloud                  │
│  Service account = Dedicated Pure1 org user for API access; not personal login                        │
│  Tag = Pure1 metadata for grouping arrays by environment, location, and team                          │
│  Email alerts = Pure1 sending proactive alerts to ops-storage email list                              │
│  Auto-case = Pure1 automatically opening TAC case; must be enabled per org                            │
│  Weekly review = Review Pure1 fleet health and capacity outlooks every Monday                         │
│  Alert to ITSM = Pure1 webhook configured to forward proactive alerts to ServiceNow                   │
│  Capacity monthly = Monthly review of Pure1 forecasts; inform procurement planning                    │
│  Purity current = All arrays on current Purity release; Pure1 flags older versions                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Array Naming Standards

Array names in Pure1 are inherited from the array's configured hostname. Enforce the hostname standard at array deployment — it cannot be changed without array rename.

| Array Type | Convention | Example |
|---|---|---|
| FlashArray | `fa-{site}-{seq}` | `fa-dc1-01` |
| FlashBlade | `fb-{site}-{seq}` | `fb-dc1-01` |

- Use lowercase only; no underscores (Pure1 URL-encodes them inconsistently)
- Site code should match the site codes used in vCenter, CMDB, and monitoring

## Access Model

| Role | Pure1 Permission | Scope |
|---|---|---|
| Storage Admin | Array Admin | Full access to all arrays + Pure1 |
| Storage Operator | Read-only | View performance, capacity, alerts |
| On-call Engineer | Read-only + alert subscription | Alert emails + Pure1 dashboard |
| Vendor Support | Pure Support access (via SupportAssist) | Pure-managed access, logged |

- Use AD group-based SSO for Pure1 access (SAML via Entra ID or Okta)
- Do not create individual accounts — group membership controls access
- Review access quarterly; remove leavers within 24 hours

## Alert Threshold Baselines

Pure1 applies AI-driven thresholds by default. Override only when the default produces excessive noise:

| Alert Type | Override Threshold | Rationale |
|---|---|---|
| Capacity utilisation | 70% warning / 80% critical | Earlier lead time than default 80/90 |
| Drive failure | No override — alert immediately | Hardware fault = always critical |
| Replication lag | > 2× RPO target | Alert before SLA breach |
| Array health score | < 90 | Proactive; default is < 80 |

## Operational Standards

- Review Pure1 capacity forecasting monthly — act on any "full within 90 days" projection
- Subscribe storage team DL to all Critical alerts; on-call engineer to all alerts
- Tag arrays with `site`, `team`, and `tier` tags in Pure1 for dashboard filtering
- Enable **Pure1 Support** (remote support channel) on all production arrays

## Configuration Checklist

- [ ] All FlashArrays and FlashBlades visible in Pure1 (connected via Purity OS outbound HTTPS)
- [ ] SSO configured (SAML with Entra ID / Okta)
- [ ] AD groups mapped to Pure1 roles
- [ ] Alert notification rules configured (email to team DL for Critical)
- [ ] Array tags applied: `site`, `tier`, `team`
- [ ] Pure1 Support (remote support) enabled on all production arrays
- [ ] Capacity forecast reviewed and any < 90-day projections actioned
