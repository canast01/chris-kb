# Replication (ActiveDR)

> Part of the [Pure FlashBlade CLI Reference](../).

---

## Replication (ActiveDR / Async)

```bash
# Replication targets
purefb remote-array show
purefb remote-array create --name <target_name> --management-address <ip>

# Replication links
purefb fs-replica-link show
purefb fs-replica-link create --local-filesystem <fs_name> --remote-filesystem <remote_fs>

# Status
purefb fs-replica-link show --detailed
```
