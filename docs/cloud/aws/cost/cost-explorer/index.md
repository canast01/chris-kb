# AWS Cost Explorer

```text
Cost Explorer: Usage Graph → Filter → Forecast
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────┐
  │  Usage / Spend Graph (monthly bars)                  │
  │  Jan  Feb  Mar  Apr  May ...                         │
  │  ███  ███  ████ ███  ████                            │
  └───────────────────┬──────────────────────────────────┘
                      │ apply filters
          ┌───────────┼──────────────────┐
          ▼           ▼                  ▼
  ┌─────────────┐ ┌─────────────┐ ┌────────────────┐
  │ Filter by   │ │ Filter by   │ │ Filter by      │
  │ Service     │ │ Account     │ │ Tag            │
  │ EC2 / RDS   │ │ Linked acct │ │ env=prod       │
  └─────────────┘ └─────────────┘ └────────────────┘
                      │
                      ▼
  ┌──────────────────────────────────────────────────────┐
  │  Forecast (28/91 day projection)                     │
  │  Based on trend line + seasonality                   │
  │  Confidence interval shown                           │
  └──────────────────────────────────────────────────────┘
```

## Overview

AWS Cost Explorer is a core cloud infrastructure service used for production operations, automation, monitoring, and platform support.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review service health |  |  |
| Check active alerts |  |  |
| Validate access permissions |  |  |
| Confirm backup or recovery coverage where applicable |  |  |
| Review recent configuration changes |  |  |

## Operational Tasks


| Task | Command |
|---|---|
| Confirm resource status |  |
| Review logs and metrics |  |
| Validate security configuration |  |
| Check cost or capacity trends |  |
| Document changes |  |

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Access denied | IAM or RBAC issue | Review permissions |
| Service unavailable | Regional or dependency issue | Check service health |
| High cost | Resource growth or unused assets | Review usage and tagging |
| Connectivity failure | Network or security rule issue | Validate routes and rules |

## Maintenance Notes

- Review configuration before changes
- Validate rollback plan
- Test in non-production where possible
- Confirm monitoring after changes
