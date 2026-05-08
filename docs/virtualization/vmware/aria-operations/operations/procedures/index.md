# Aria Operations — Procedures

## Alert Management

1. Go to **Alerts > All Alerts**
2. Filter by Criticality = Critical or Immediate
3. Investigate root cause before acknowledging
4. Cancel alerts only when the underlying issue is resolved

**Maintenance windows:**

```
Administration > Maintenance Schedules > Add Schedule
```

## Capacity Reclamation Workflow

1. Navigate to **Optimize > Reclaim > Idle VMs** or **Oversized VMs**
2. Review recommendations sorted by waste (GB/CPU)
3. Export report for owner review
4. Coordinate reclamation with VM owners
5. After reclamation, update capacity baselines

## Common Maintenance Tasks

| Task | Steps |
|------|-------|
| Restart adapter | Administration > Solutions > select adapter > Restart |
| Restart all services | `vracli cluster restart` (use with care) |
| Clear stale objects | Environment > Object Browser > Deleted Objects > Purge |
| Update certificate | Administration > Certificates |
| Add/remove data node | Administration > Cluster Management > Add Node |

## Support Bundle Generation

```bash
# Via UI: Administration > Support > Generate Support Bundle

# Via CLI
ssh admin@<aria-ops-primary-fqdn>
vracli support bundle generate
ls /storage/log/support-bundle/
```
