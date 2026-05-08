# Aria Operations — Health Checks

## Daily Checks

| Check | Location | Expected State |
|-------|----------|----------------|
| Cluster node status | Administration > Cluster Management | All nodes Online |
| Adapter health | Administration > Solutions | All adapters Collecting |
| Active critical alerts | Alerts > All Alerts | Review and acknowledge known issues |
| Capacity headroom | Optimize > Capacity | No red capacity warnings |
| Self-monitoring alerts | Environment > vRealize Operations Health | No critical self-alerts |

## Cluster Health Commands

```bash
ssh admin@<aria-ops-primary-fqdn>

vracli cluster health
vracli status
vracli adapter list
```

## Adapter Health

1. Navigate to **Administration > Solutions > Cloud Accounts** (or **Adapters**)
2. Confirm each adapter shows **Collection State: Collecting**
3. Last collection time should be within 5 minutes

```bash
vracli adapter list --verbose
journalctl -u vmware-casa --since "1 hour ago"
```
