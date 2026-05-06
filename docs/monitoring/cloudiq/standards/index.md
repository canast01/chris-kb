# CloudIQ Standards

CloudIQ tagging policy mirrors the team's standard three-tag taxonomy (site, environment, team) applied to all onboarded systems for reporting and alert routing. Alert notification rules are configured per severity: CRITICAL alerts route to PagerDuty, WARNING alerts route to email. Systems with health scores below 80 trigger a team review; below 60 triggers an incident. API client secrets are rotated on a scheduled basis.

| Standard | Value |
|---|---|
| Required tags | Site, Environment, Team |
| Health score — review threshold | Below 80 |
| Health score — incident threshold | Below 60 |
| CRITICAL alert routing | PagerDuty |
| WARNING alert routing | Email distribution list |
| API secret rotation | Every 12 months |
