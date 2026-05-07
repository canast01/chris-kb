# Azure Site Recovery

Azure Site Recovery (ASR) — VM replication, failover, and failback between Azure regions or from on-premises.
## Supported Scenarios

| Source | Target | Method |
|---|---|---|
| Azure VM (region A) | Azure VM (region B) | Native ASR |
| VMware / physical | Azure | Mobility Service agent + replication appliance |
| Hyper-V | Azure | Azure Site Recovery Provider |

## Common Azure CLI Commands

```bash
# List Recovery Services vaults
az backup vault list --query '[*].{Name:name,RG:resourceGroup,Location:location}' -o table

# List replicated items (VMs) in a vault
az site-recovery protected-item list \
  --vault-name <vault-name> -g <rg> \
  --query '[*].{VM:name,State:properties.protectionState,Health:properties.replicationHealth}' -o table

# Trigger test failover (non-destructive — creates test VMs in isolation)
az site-recovery protected-item failover-cancel \
  --vault-name <vault-name> -g <rg> \
  --fabric-name <target-fabric> \
  --protection-container-name <container> \
  --replicated-protected-item-name <item-name>
```

## Health Checks

**Portal checks (daily):**
1. Recovery Services vault → **Replicated items** — all items show `Protected` and `Healthy`
2. Review **Replication health** — no warnings or errors
3. Check **RPO** compliance — green means within SLA
4. Review **Jobs** → any failed jobs from last 24 hours

```bash
# Get replication health for all items
az site-recovery replication-protected-item list \
  --vault-name <vault-name> \
  --resource-group <rg> \
  --fabric-name <primary-fabric> \
  --protection-container-name <container> \
  --query '[*].{Name:name,State:properties.protectionState,Health:properties.replicationHealth,RPO:properties.rpoInSeconds}'
```

## Test Failover Workflow

1. Portal: Vault → Replicated items → select VM → **Test Failover**
2. Select recovery point (latest processed or latest app-consistent)
3. Select test virtual network (isolated — not production)
4. Review test VM at target region — verify OS boots, app responds
5. **Cleanup test failover** — removes test VMs, marks test complete

## Planned Failover (migration, no data loss)

1. Portal: Replicated items → **Planned failover**
2. Confirm replication is synced (RPO = 0)
3. Execute failover — source VM shuts down, replica starts at target
4. Verify application at target region
5. **Commit** — severs replication; target is now primary

## Failback to Primary

1. After commit: **Re-protect** the VM (replicates from target back to primary)
2. Wait for synchronisation
3. **Planned failover** again — back to primary region
4. **Commit** and **Re-protect** to resume normal replication direction

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Replication health unhealthy | VM events in vault | Check for connectivity issues between source and replication appliance |
| RPO breach | Network bandwidth | Ensure sufficient bandwidth between source and target; check large data change rate |
| Test failover VM not starting | Target network / NSG | Verify test network has no restrictive NSGs blocking boot |
| Agent not communicating | Mobility Service status | Restart Mobility Service on source VM; check proxy settings |
| Delta sync slow | Disk churn rate | High-churn disks may require larger cache; review exclusion of temp/swap disks |
