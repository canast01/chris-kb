# Pure1 Standards

Array tagging in Pure1 follows a mandatory three-tag standard (Site, Environment, Owner) to support reporting, alert routing, and capacity forecasting by business unit. Alert notification routing rules are defined per severity level, with CRITICAL alerts routed to PagerDuty and WARNING alerts delivered via email. Capacity threshold alerts are configured to warn at 70% used and escalate to critical at 85% used, with a weekly capacity report emailed to the storage team.

| Standard | Value |
|---|---|
| Required tags | Site, Environment, Owner |
| Capacity warn threshold | 70% used |
| Capacity critical threshold | 85% used |
| Report schedule | Weekly capacity report via email |
| API access policy | Per-team API keys, rotated annually |
