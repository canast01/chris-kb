# CloudIQ — Design Standards

<div class="kb-summary">
Secure Connect Gateway deployment standards, SCG sizing, network requirements, alert threshold baselines, and naming conventions for CloudIQ.
</div>

```
┌───────────────────────────────────── CloudIQ — Design Standards ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Registration Standards            │  │                 Alert Policy                │   │
│   │            All arrays registered             │  │             Email: ops-storage@             │   │
│   │            Naming: site-model-id             │  │           Webhook: monitoring tool          │   │
│   │               Tag by env+team                │  │           Severity thresholds doc           │   │
│   │             Single org per site              │  │                Review monthly               │   │
│   │             Service account only             │  │              Escalation runbook             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  All Dell arrays must be registered · TCP 443 outbound required from storage management network       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Organisation = CloudIQ tenant; group all arrays from one customer/site into a single org             │
│  Service account = Dedicated Dell account for CloudIQ integration; not a personal login               │
│  Tag = Metadata label applied in CloudIQ to group arrays by environment, team, or location            │
│  Naming convention = Standardised array name in CloudIQ: site-model-serial or similar                 │
│  Alert threshold = Score or metric value at which CloudIQ generates a notification                    │
│  Webhook = HTTP endpoint receiving CloudIQ alert POSTs for integration with Slack/ITSM                │
│  Monthly review = Regular cadence to validate alert thresholds and clear stale recommendations        │
│  Escalation runbook = Documented steps for P1 storage alert from CloudIQ to on-call engineer          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── CloudIQ — Design Standards ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Registration Standards            │  │                 Alert Policy                │   │
│   │            All arrays registered             │  │             Email: ops-storage@             │   │
│   │            Naming: site-model-id             │  │           Webhook: monitoring tool          │   │
│   │               Tag by env+team                │  │           Severity thresholds doc           │   │
│   │             Single org per site              │  │                Review monthly               │   │
│   │             Service account only             │  │              Escalation runbook             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  All Dell arrays must be registered · TCP 443 outbound required from storage management network       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Organisation = CloudIQ tenant; group all arrays from one customer/site into a single org             │
│  Service account = Dedicated Dell account for CloudIQ integration; not a personal login               │
│  Tag = Metadata label applied in CloudIQ to group arrays by environment, team, or location            │
│  Naming convention = Standardised array name in CloudIQ: site-model-serial or similar                 │
│  Alert threshold = Score or metric value at which CloudIQ generates a notification                    │
│  Webhook = HTTP endpoint receiving CloudIQ alert POSTs for integration with Slack/ITSM                │
│  Monthly review = Regular cadence to validate alert thresholds and clear stale recommendations        │
│  Escalation runbook = Documented steps for P1 storage alert from CloudIQ to on-call engineer          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## SCG Deployment Standards

| Parameter | Standard |
|---|---|
| Form factor | OVA deployed on vSphere (not bare metal) |
| Placement | Management cluster; not on production workload hosts |
| HA | Single SCG per site is sufficient; CloudIQ tolerates collection gaps |
| vCPU / RAM | 4 vCPU / 8 GB RAM minimum; 8 vCPU / 16 GB for > 20 arrays |
| Disk | 100 GB thin-provisioned |
| Network | Management VLAN; outbound HTTPS 443 to `*.dell.com` only |

## Naming Convention

| Object | Convention | Example |
|---|---|---|
| SCG VM | `cloudiq-scg-{site}-{seq}` | `cloudiq-scg-dc1-01` |
| SCG display name in portal | `{site}-SCG-{seq}` | `DC1-SCG-01` |

## Network Requirements

- SCG requires **outbound HTTPS (443)** to Dell CloudIQ endpoints — no inbound rules needed
- Proxy support: configure proxy in SCG admin UI if direct internet access is blocked
- Validate connectivity: `curl -s https://cloudiq.dell.com` from SCG should return 200

| Destination | Protocol | Port | Purpose |
|---|---|---|---|
| `*.dell.com` | HTTPS | 443 | Telemetry upload and SCG registration |
| Array management IPs | HTTPS | 443 | Data collection from PowerMax, Unity, etc. |
| Array management IPs | SSH | 22 | Data collection from PowerScale OneFS |

## Alert Threshold Baselines

| Alert Type | Warning | Critical |
|---|---|---|
| Capacity utilisation | 75% | 85% |
| Projected full (days) | 90 days | 30 days |
| Array health score | < 80 | < 60 |
| Component fault (drive/SP) | Any | — |

- Configure email notifications for Critical alerts immediately on SCG registration
- Review and acknowledge Warning alerts at least weekly
- Subscribe the storage team distribution list, not individual mailboxes

## Configuration Checklist

- [ ] SCG OVA deployed and powered on
- [ ] SCG registered to CloudIQ portal (unique registration token per SCG)
- [ ] All managed arrays added to SCG and collection status green
- [ ] SCG VM snapshot policy aligned with management cluster backup schedule
- [ ] Alert notification email configured for storage team DL
- [ ] API key generated and stored in CyberArk for automation use
- [ ] SCG hostname resolves in DNS
