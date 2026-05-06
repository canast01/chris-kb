# Pure FlashBlade CLI Reference

Commonly used `purefb` commands for managing Pure Storage FlashBlade arrays.

> Connect via SSH to the FlashBlade management IP, or use `purefb` from a host with the CLI installed and configured.

---

## Array Status & Identity

```bash
# Array info
purefb array show
purefb array show --version

# Hardware status
purefb hardware show
purefb hardware show --blades
purefb hardware show --chassis

# Alerts
purefb alert show
purefb alert show --filter "state='open'"

# Capacity
purefb array show --space
purefb filesystem show --space
```

---

## Blades & Hardware

```bash
# Blade status
purefb blade show
purefb blade show --id <blade_id>

# Drive health
purefb drive show
purefb drive show --blade <blade_id>

# Chassis
purefb chassis show
```

---

## File Systems (NFS / SMB)

```bash
# List file systems
purefb filesystem show
purefb filesystem show --name <name>

# Create file system
purefb filesystem create --name <name> --size 10T --nfs --nfs-rules "*(rw,no_root_squash)"
purefb filesystem create --name <name> --size 10T --smb

# Resize
purefb filesystem update --name <name> --size 20T

# Destroy / eradicate
purefb filesystem destroy --name <name>
purefb filesystem eradicate --name <name>

# NFS exports
purefb filesystem show --name <name>
purefb filesystem update --name <name> --nfs-rules "<ip_or_cidr>(rw,no_root_squash)"

# SMB shares
purefb smb-share show
purefb smb-share create --name <share_name> --filesystem <fs_name>
purefb smb-share destroy --name <share_name>
```

---

## Object Store (S3)

```bash
# Buckets
purefb bucket show
purefb bucket create --name <bucket> --account <account>
purefb bucket destroy --name <bucket>
purefb bucket eradicate --name <bucket>

# Accounts
purefb object-store-account show
purefb object-store-account create --name <account>

# Users
purefb object-store-user show
purefb object-store-user create --name <user> --account <account>

# Access keys
purefb object-store-access-key show
purefb object-store-access-key create --user <user>/<account>
```

---

## Snapshots

```bash
# List snapshots
purefb snapshot show
purefb snapshot show --name <snapshot_name>

# Create snapshot
purefb snapshot create --source <filesystem_name> --name <snapshot_name>

# Restore
purefb snapshot copy --name <snapshot_name> --target <new_fs_name>

# Destroy / eradicate
purefb snapshot destroy --name <snapshot_name>
purefb snapshot eradicate --name <snapshot_name>

# Scheduled policies
purefb snapshot-rule show
```

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

---

## Network

```bash
# Network interfaces
purefb network-interface show
purefb network-interface show --name <if_name>

# Subnets
purefb subnet show
purefb subnet create --name <subnet> --prefix <cidr> --gateway <gw>

# DNS
purefb dns show
purefb dns update --nameservers <ip1,ip2>

# NTP
purefb ntp show
purefb ntp update --ntpservers <ntp_ip>
```

---

## Users & Authentication

```bash
# Admin users
purefb admin show
purefb admin create --name <user> --role array_admin
purefb admin update --name <user> --password <pass>

# API tokens
purefb api-client show
purefb api-client create --name <client_name> --role array_admin

# Directory services (LDAP/AD)
purefb directory-service show
```

---

## Support & Diagnostics

```bash
# Phone home / phonehome
purefb phonehome show
purefb phonehome send --type auto

# Support connectivity
purefb support show
purefb support update --enabled true

# Log export
purefb support log export
```
