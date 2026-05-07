# Monitoring Dashboard Standards
## Required Dashboards

| Dashboard | Audience | Refresh |
|---|---|---|
| Infrastructure Overview | All ops | 5 min |
| Capacity Planning | Infra / storage leads | 1 hour |
| Active Alerts | On-call | 1 min |
| SAN / Storage Health | Storage team | 5 min |
| Backup Status | Infra / backup team | 30 min |
| Network Health | Network team | 5 min |
| Application Availability | App owners | 1 min |

## Infrastructure Overview — Required Panels

1. **Alert count by severity** (Critical / High / Medium)
2. **Host availability %** (uptime across all monitored hosts)
3. **Top CPU consumers** (top 10 hosts by 1-hour avg)
4. **Top memory consumers** (top 10 hosts)
5. **Disk usage heatmap** (filesystems >75% shown as warning; >90% as critical)
6. **Storage array health** (one tile per array — green/amber/red)

## Panel Design Rules

- Use consistent colour coding: **red = critical**, **amber = warning**, **green = healthy**
- Always include a time range selector with default = last 24 hours
- Do not use pie charts for time-series data — use line or bar charts
- Label axes with units (%, MB/s, ms, IOPS)
- Every panel must have a title and a data source label
- Avoid panels with more than 15 series — break into sub-panels

## Naming Convention

```
<environment>-<system>-<metric>
prod-storage-capacity
prod-compute-cpu
uat-network-errors
```

## Grafana — Dashboard as Code

```json
// Store dashboards in Git — provision via Grafana provisioning
// grafana/provisioning/dashboards/infra-overview.json
{
  "title": "Infrastructure Overview",
  "uid": "infra-overview-v1",
  "refresh": "5m",
  "panels": [...]
}
```

```yaml
# grafana/provisioning/dashboards/dashboards.yaml
apiVersion: 1
providers:
  - name: 'Infra Dashboards'
    folder: 'Infrastructure'
    type: file
    options:
      path: /etc/grafana/dashboards
```

## Validation Checklist

- [ ] All required dashboards loading in monitoring tool
- [ ] Metrics updating at configured refresh interval
- [ ] Alert panel reflects current open alerts (not stale)
- [ ] Time-zone consistent across all panels (UTC preferred for ops dashboards)
- [ ] No broken panel queries (missing datasource or deleted metric)
- [ ] Access permissions: read for all ops, edit only for monitoring team
- [ ] Dashboard JSON committed to Git / versioned

## Dashboard Review Cadence

| Trigger | Action |
|---|---|
| Quarterly | Audit for stale panels and unused dashboards |
| After major infra change | Update panels affected by the change |
| New service onboarded | Add service to infrastructure overview within 5 days |
| Alert threshold change | Update the corresponding dashboard annotation |
