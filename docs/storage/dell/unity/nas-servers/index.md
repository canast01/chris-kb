# Dell Unity NAS Servers

NAS server lifecycle management — create, configure, and troubleshoot NAS servers on Dell Unity.

## Overview

A NAS server on Dell Unity is a logical entity that owns file interfaces (network ports), AD/LDAP authentication configuration, and NFS/SMB protocol settings. Each NAS server runs on one storage processor and can fail over to the peer SP.

## List and Inspect

```bash
# List all NAS servers
uemcli -d <ip> -u admin /nas/server show
uemcli -d <ip> -u admin /nas/server show -detail

# View a specific NAS server
uemcli -d <ip> -u admin /nas/server -id <nas_id> show -detail
```

## Create a NAS Server

```bash
# Create NAS server on a specific SP
uemcli -d <ip> -u admin /nas/server create \
    -name <nas_name> \
    -sp <spa_or_spb> \
    -pool <pool_id>

# Enable both NFS and SMB protocols
uemcli -d <ip> -u admin /nas/server -id <nas_id> set \
    -fileInterface <if_id>
```

## AD / LDAP Authentication

```bash
# Join NAS server to Active Directory
uemcli -d <ip> -u admin /nas/ad create \
    -server <nas_id> \
    -domain corp.local \
    -username <ad_admin_user> \
    -passwd <password> \
    -organizationalUnit "OU=Servers,DC=corp,DC=local"

# List AD configurations
uemcli -d <ip> -u admin /nas/ad show

# LDAP configuration (for NFS UID/GID mapping)
uemcli -d <ip> -u admin /nas/ldap show
```

## File Interfaces (Network)

```bash
# List file interfaces (IPs on the NAS server)
uemcli -d <ip> -u admin /net/nas/if show
uemcli -d <ip> -u admin /net/nas/if show -detail

# Create a file interface (IP for NFS/SMB access)
uemcli -d <ip> -u admin /net/nas/if create \
    -server <nas_id> \
    -port <sp_port_id> \
    -addr <ip_address> \
    -netmask <mask> \
    -gateway <gateway>
```

## File Systems (on the NAS Server)

```bash
# List file systems
uemcli -d <ip> -u admin /stor/config/fs show
uemcli -d <ip> -u admin /stor/config/fs show -detail

# Create a file system
uemcli -d <ip> -u admin /stor/config/fs create \
    -name <fs_name> \
    -nasServer <nas_id> \
    -pool <pool_id> \
    -size 5T \
    -supportedProtocols Mixed   # NFS + SMB

# Create NFS share on a file system
uemcli -d <ip> -u admin /prot/nfs create \
    -server <nas_id> \
    -path / \
    -fs <fs_id>

# Create SMB share on a file system
uemcli -d <ip> -u admin /prot/smb create \
    -name <share_name> \
    -server <nas_id> \
    -path / \
    -fs <fs_id>
```

## Failover / SP Rebalance

```bash
# Move NAS server to the other SP (planned rebalance)
uemcli -d <ip> -u admin /nas/server -id <nas_id> set -sp <spb>

# Check SP ownership after failover
uemcli -d <ip> -u admin /nas/server show | grep -E "Name|SP"
```

## Troubleshooting

```bash
# Check NAS server health
uemcli -d <ip> -u admin /nas/server -id <nas_id> show -detail | grep -E "Health|State"

# Check file interface status
uemcli -d <ip> -u admin /net/nas/if show | grep -E "Health|Addr"

# Active NFS sessions
uemcli -d <ip> -u admin /prot/nfs/session show

# Active SMB sessions
uemcli -d <ip> -u admin /prot/smb/session show
```
