# ECS Replication

ECS replication provides geo-redundancy by replicating objects across sites using replication groups.

## Replication Groups

ECS uses **replication groups** to define which VDCs (Virtual Data Centers) participate in replication and the replication mode:

| Mode | Description |
|---|---|
| Synchronous | Write acknowledged only after replicated to all VDCs |
| Asynchronous | Write acknowledged immediately; replicated in background |
| Metered | Asynchronous with bandwidth throttling |

## Monitoring Replication

From the ECS Management Console:

- **Monitor** → **Replication** → view per-replication-group status
- Check **Replication Lag** — bytes or time behind
- Check for **Failed** replication segments

```bash
# S3 API — verify object exists on remote site
# (After replication) query the remote ECS endpoint
aws s3 ls s3://<bucket>/<key> \
    --endpoint-url https://<remote_ecs_endpoint>
```

## Replication Failure Response

If replication fails:

1. Check the ECS Management Console for the specific replication error
2. Check network connectivity between VDCs
3. Check disk space on the destination VDC
4. Review ECS system logs for replication-specific error codes

## Cross-VDC Failover

In a failover scenario (primary VDC unavailable):

1. Update client S3 endpoint to the secondary ECS VDC IP/FQDN
2. Confirm data is accessible:
   ```bash
   aws s3 ls s3://<bucket>/ --endpoint-url https://<secondary_ecs>
   ```
3. Note: asynchronous replication may have RPO lag — verify with the ECS monitoring console

## Bandwidth Management

```bash
# Replication throttling is configured via ECS Management Console
# Monitor → Replication → Bandwidth Management
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| High replication lag | Network bandwidth saturation | Check network utilisation; throttle if needed |
| Replication failed | Destination VDC offline or full | Restore connectivity or add capacity |
| Objects missing on replica | Check replication lag time | Wait for async replication; check for errors |
