# Aria Operations — Operations

## Daily Checks

| Check | Location | Expected State |
|-------|----------|----------------|
| Cluster node status | Administration > Cluster Management | All nodes Online |
| Adapter health | Administration > Solutions | All adapters Collecting |
| Active critical alerts | Alerts > All Alerts | Review and acknowledge known issues |
| Capacity headroom | Optimize > Capacity | No red capacity warnings |
| Self-monitoring alerts | Environment > vRealize Operations Health | No critical self-alerts |

---

## Cluster Health Check

```bash
# SSH to primary node
ssh admin@<aria-ops-primary-fqdn>

# Check cluster health via CLI
vracli cluster health

# Check all services status
vracli status

# Check adapter collection status
vracli adapter list
```

---

## Adapter Health

### Check adapter status via UI

1. Navigate to **Administration > Solutions > Cloud Accounts** (or **Adapters**)
2. Confirm each adapter shows **Collection State: Collecting**
3. Last collection time should be within 5 minutes

### Check adapter logs

```bash
# SSH to primary node
ssh admin@<aria-ops-primary-fqdn>

# List adapter instances and their collection status
vracli adapter list --verbose

# View adapter logs
journalctl -u vmware-casa --since "1 hour ago"
```

---

## Alert Management

### Review and bulk-acknowledge alerts

1. Go to **Alerts > All Alerts**
2. Filter by Criticality = Critical or Immediate
3. Investigate root cause before acknowledging
4. Cancel alerts only when the underlying issue is resolved

### Maintenance windows

```
Administration > Maintenance Schedules > Add Schedule
```
- Assign object groups to suppress alerts during maintenance

---

## Capacity Reclamation Workflow

1. Navigate to **Optimize > Reclaim > Idle VMs** or **Oversized VMs**
2. Review recommendations sorted by waste (GB/CPU)
3. Export report for owner review
4. Coordinate reclamation with VM owners
5. After reclamation, update capacity baselines

---

## Support Bundle Generation

```bash
# Via UI
# Administration > Support > Generate Support Bundle

# Via CLI
ssh admin@<aria-ops-primary-fqdn>
vracli support bundle generate

# Bundle is saved to /storage/log/support-bundle/
ls /storage/log/support-bundle/
```

---

## Common Maintenance Tasks

| Task | Steps |
|------|-------|
| Restart adapter | Administration > Solutions > select adapter > Restart |
| Restart all services | `vracli cluster restart` (use with care) |
| Clear stale objects | Environment > Object Browser > Deleted Objects > Purge |
| Update certificate | Administration > Certificates |
| Add/remove data node | Administration > Cluster Management > Add Node |

---

## Related Sections

- [Architecture](../architecture/) — cluster topology
- [Troubleshooting](../troubleshooting/) — error diagnosis
- [CLI Reference](../cli-reference/) — full command reference
