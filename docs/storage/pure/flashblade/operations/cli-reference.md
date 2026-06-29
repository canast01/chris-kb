---
tags:
  - operations
  - pure
---
# FlashBlade — CLI Reference

<div class="kb-summary">
CLI Reference reference covering Array Hardware, File Systems (NFS / SMB), Network, Object Store (S3), Replication (ActiveDR) and 3 more sections.

*Applies to: FlashBlade Purity//FB 4.x*
</div>
![FlashBlade — CLI Reference](../../../../assets/storage-pure-flashblade-operations-cli-reference.svg)

![FlashBlade — CLI Reference — Diagram](../../../../assets/storage-pure-flashblade-operations-cli-reference-diagram.svg)

> Part of the [FlashBlade Operations](index.md) reference.

Commonly used `purefb` commands for managing Pure Storage FlashBlade arrays. FlashBlade is a scale-out NAS and object storage platform — it serves NFS and SMB file shares as well as S3-compatible object storage.

> Connect via SSH to the FlashBlade management IP, or use `purefb` from a host with the CLI installed and configured.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Array Hardware

### Array Status & Identity

```bash
# Array info — model, version, capacity
purefb array show
purefb array show --version

# Hardware status overview
purefb hardware show
purefb hardware show --blades
purefb hardware show --chassis

# Active alerts
purefb alert show
purefb alert show --filter "state='open'"

# Capacity usage
purefb array show --space
purefb filesystem show --space
```


```text title="Expected output"
$ purefb array show
Name                          Model            Version          Capacity
flashblade-prod-01            FB15000          4.10.5           147.5TB
flashblade-prod-02            FB20000          4.10.5           295.0TB

$ purefb array show --version
Name                          Version          Build
flashblade-prod-01            4.10.5           20240115_123456
flashblade-prod-02            4.10.5           20240115_123456

$ purefb hardware show
Name                          Status           Temperature      Power
flashblade-prod-01            Healthy          22°C             1200W
flashblade-prod-02            Healthy          24°C             1850W

$ purefb hardware show --blades
Name                          Blade            Status           Model
flashblade-prod-01            0                Healthy          FB-Blade-X20
flashblade-prod-01            1                Healthy          FB-Blade-X20
flashblade-prod-02            0                Healthy          FB-Blade-X30
flashblade-prod-02            1                Healthy          FB-Blade-X30
flashblade-prod-02            2                Healthy          FB-Blade-X30
...

$ purefb hardware show --chassis
Name                          Chassis          Status           Model
flashblade-prod-01            0                Healthy          FB15000-Chassis
flashblade-prod-02            0                Healthy          FB20000-Chassis

$ purefb alert show
Severity          Code              Name                          State
warning           DISK_PREDICTIVE   Disk predictive failure       open
info              UPGRADE_READY     Upgrade available             open

$ purefb alert show --filter "state='open'"
Severity          Code              Name                          State
warning           DISK_PREDICTIVE   Disk predictive failure       open
info              UPGRADE_READY     Upgrade available             open

$ purefb array show --space
Name                          Used              Available         Snapshot
flashblade-prod-01            89.3TB            58.2TB            12.1TB
flashblade-prod-02            156.7TB           138.3TB           28.4TB

$ purefb filesystem show --space
Name                          Used              Available         Total
data-share-01                 34.5TB            15.2TB            49.7TB
backup-archive-02             78.9TB            89.1TB            168.0TB
media-storage-03              12.1TB            8.4TB             20.5TB
...
```

!!! warning "Common errors"
    **`Error: Array 'flashblade-prod-01' is unreachable`** — Verify network connectivity and that the management IP is reachable with `ping` or `ssh`.
    **`Error: Invalid filter syntax in alert query`** — Use proper filter format with quotes: `--filter "state='open' and severity='warning'"`.
### Blades & Hardware

```bash
# Blade status (each blade is a combined compute+flash module)
purefb blade show
purefb blade show --id <blade_id>

# Drive health
purefb drive show
purefb drive show --blade <blade_id>

# Chassis
purefb chassis show
```


```text title="Expected output"
Name    Status  Model              Serial           Capacity
blade0  healthy FB20-HA2-2U-40     PFB2142300001    40TB
blade1  healthy FB20-HA2-2U-40     PFB2142300002    40TB
blade2  healthy FB20-HA2-2U-40     PFB2142300003    40TB

Name    Status  Blade   Capacity  Used
SSD-0   healthy blade0  3.6TB     2.1TB
SSD-1   healthy blade0  3.6TB     1.9TB
SSD-2   healthy blade1  3.6TB     2.4TB
SSD-3   healthy blade1  3.6TB     2.2TB
...

Name       Status  Model         Serial         Temp(C)  PSU_Status
chassis-1  healthy FB20-HA2-2U   PFC2142300001  32       OK
```

!!! warning "Common errors"
    **`Error: blade <blade_id> not found`** — Verify the blade ID exists by running `purefb blade show` without filters first.
    **`Error: Connection refused on management IP`** — Ensure the FlashBlade management interface is reachable and the purefb CLI is authenticated with valid credentials.
---

## File Systems (NFS / SMB)

File systems are the NAS shares on a FlashBlade. You create a file system, set its size, and enable NFS or SMB access (or both). NFS rules control which client IPs can mount, and what read/write permissions they get.

### List File Systems

```bash
purefb filesystem show
purefb filesystem show --name <name>
purefb filesystem show --all    # includes destroyed
```


```text title="Expected output"
Name                          Size      Used      Snapshots  NFS  SMB  HTTP
data-prod                     10.0T     7.2T      12         on   on   off
backup-archive                50.0T     48.3T     8          on   off  off
dev-testing                   5.0T      1.1T      3          on   on   on
logs-retention                20.0T     19.8T     24         off  on   off

Name                          Size      Used      Snapshots  NFS  SMB  HTTP
data-prod                     10.0T     7.2T      12         on   on   off

Name                          Size      Used      Snapshots  NFS  SMB  HTTP  State
data-prod                     10.0T     7.2T      12         on   on   off   available
backup-archive                50.0T     48.3T     8          on   off  off   available
dev-testing                   5.0T      1.1T      3          on   on   on    available
logs-retention                20.0T     19.8T     24         off  on   off   available
archive-2024-q1               2.0T      2.0T      0          on   off  off   destroyed
...
```

!!! warning "Common errors"
    **`Error: Invalid filesystem name '<name>'`** — Verify the filesystem name exists with `purefb filesystem show` and use the exact name without angle brackets.
    **`Error: Connection refused to management IP`** — Ensure the FlashBlade management IP is reachable and your `purefb` credentials are configured with `purefb login`.
### Create a File System

```bash
# NFS file system with export rules
purefb filesystem create \
    --name <name> \
    --size 10T \
    --nfs \
    --nfs-rules "*(rw,no_root_squash)"

# SMB file system
purefb filesystem create --name <name> --size 10T --smb

# Both NFS and SMB
purefb filesystem create \
    --name <name> \
    --size 10T \
    --nfs --nfs-rules "*(rw,no_root_squash)" \
    --smb
```


```text title="Expected output"
Creating filesystem 'data-share-01'...
Filesystem created successfully
Name: data-share-01
Size: 10T
Protocol: NFS
NFS Rules: *(rw,no_root_squash)
State: Available
Created: 2024-01-15T09:42:33Z

Creating filesystem 'smb-share-02'...
Filesystem created successfully
Name: smb-share-02
Size: 10T
Protocol: SMB
State: Available
Created: 2024-01-15T09:43:18Z

Creating filesystem 'dual-protocol-03'...
Filesystem created successfully
Name: dual-protocol-03
Size: 10T
Protocols: NFS, SMB
NFS Rules: *(rw,no_root_squash)
State: Available
Created: 2024-01-15T09:44:05Z
```

!!! warning "Common errors"
    **`Error: Invalid NFS rules syntax`** — Verify NFS export rules follow standard format (e.g., `"*(rw,no_root_squash)"` or `"192.168.1.0/24(rw)"`).
    **`Error: Filesystem name already exists`** — Choose a unique filesystem name or delete the existing filesystem with `purefb filesystem delete --name <existing-name>`.
    **`Error: Insufficient capacity on array`** — Reduce the requested size or check available capacity with `purefb hardware list`.
### Resize a File System

```bash
purefb filesystem update --name <name> --size 20T
```


```text title="Expected output"
Filesystem updated. Name: <name>, Size: 20T, Used: 8.3T, Available: 11.7T, Snapshot Count: 12, Last Modified: 2024-01-15T09:42:31Z
```

!!! warning "Common errors"
    **`Error: Filesystem '<name>' not found`** — Verify the filesystem name exists by running `purefb filesystem list` and use the correct name.
    **`Error: Size must be larger than current usage (8.3T)`** — Increase the size to a value greater than the current used capacity shown in `purefb filesystem info --name <name>`.
    **`Error: Authentication failed`** — Ensure you are authenticated to the FlashBlade array with valid credentials using `purefb login`.
### Update NFS Export Rules

```bash
# Restrict to specific network
purefb filesystem update \
    --name <name> \
    --nfs-rules "<ip_cidr>(rw,no_root_squash)"

# Multiple rules
purefb filesystem update \
    --name <name> \
    --nfs-rules "10.0.1.0/24(rw,no_root_squash):10.0.2.0/24(ro)"
```


```text title="Expected output"
Filesystem updated successfully.
Name: my-data-fs
NFS Rules: 10.0.1.0/24(rw,no_root_squash):10.0.2.0/24(ro)
Export Path: /my-data-fs
State: available
```

!!! warning "Common errors"
    **`Error: Invalid CIDR notation in NFS rules`** — Verify the IP range uses proper CIDR format (e.g., 10.0.1.0/24) and separate multiple rules with colons without spaces.
    **`Error: Filesystem '<name>' not found`** — Confirm the filesystem name matches exactly using `purefb filesystem list` and check for typos or special characters.
    **`Error: NFS rules syntax invalid: missing parentheses`** — Ensure each rule follows the format `<ip_cidr>(<options>)` with options in parentheses immediately after the CIDR block.
### SMB Shares

```bash
# List SMB shares
purefb smb-share show

# Create an SMB share
purefb smb-share create --name <share_name> --filesystem <fs_name>

# Delete an SMB share
purefb smb-share destroy --name <share_name>
```


```text title="Expected output"
Name          Filesystem    Protocol  Exported  Clients Connected
marketing     data-fs       smb       true      3
engineering   eng-data      smb       true      1
archive       backup-fs     smb       false     0

Share 'project-share' created successfully
Filesystem: project-fs
Protocol: smb
State: available

Are you sure you want to destroy SMB share 'project-share'? (yes/no): yes
SMB share 'project-share' destroyed successfully
```

!!! warning "Common errors"
    **`Error: Filesystem <fs_name> not found`** — Verify the filesystem exists with `purefb filesystem show` before creating the share.
    **`Error: SMB share <share_name> is in use by 1 client(s)`** — Disconnect all clients or use `--force` flag to destroy an active share.
### Destroy and Eradicate

```bash
# Destroy (recoverable for 24 hours)
purefb filesystem destroy --name <name>

# Permanently eradicate
purefb filesystem eradicate --name <name>

# Recover a destroyed file system
purefb filesystem recover --name <name>
```


```text title="Expected output"
Destroying filesystem 'data-backup'...
Filesystem 'data-backup' destroyed successfully. Recovery available for 24 hours.
Permanently eradicating filesystem 'data-backup'...
Filesystem 'data-backup' eradicated permanently.
Recovering filesystem 'archive-fs'...
Filesystem 'archive-fs' recovered successfully.
```

!!! warning "Common errors"
    **`Error: Filesystem 'data-backup' not found`** — Verify the filesystem name with `purefb filesystem list` and ensure you have the correct spelling.
    **`Error: Filesystem 'data-backup' is not in destroyed state`** — Run `purefb filesystem destroy --name <name>` first before attempting eradication.
    **`Error: Recovery window expired for filesystem 'old-fs'`** — Destroyed filesystems can only be recovered within 24 hours; if the window has passed, the data cannot be recovered.
### Common Issues

| Issue | Check | Action |
|---|---|---|
| NFS mount refused | Export rules | Verify client IP is in NFS rules |
| SMB share not visible | SMB enabled | Ensure `--smb` flag was used at create |
| File system full | Capacity | `purefb filesystem update --size` |
| Cannot destroy | NFS mounts active | Unmount all clients first |

---

## Network

FlashBlade networking includes data interfaces for NFS/SMB/S3 traffic and VIPs (Virtual IPs) that float between blades for high availability. VIPs are what clients actually connect to.

### Network Interfaces

```bash
# List all interfaces (data, management, replication)
purefb network-interface show
purefb network-interface show --name <if_name>
purefb network-interface show | grep -E "Name|Speed|State|Address"
```


```text title="Expected output"
Name                          Speed      State      Address
eth0                          10Gbps     up         192.168.1.10
eth1                          10Gbps     up         192.168.1.11
eth2                          1Gbps      up         10.0.0.5
mgmt0                         1Gbps      up         172.16.0.50
repl0                         10Gbps     down       10.1.0.20

Name                          Speed      State      Address
eth0                          10Gbps     up         192.168.1.10

Name                          Speed      State      Address
eth0                          10Gbps     up         192.168.1.10
eth1                          10Gbps     up         192.168.1.11
eth2                          1Gbps      up         10.0.0.5
mgmt0                         1Gbps      up         172.16.0.50
repl0                         10Gbps     down       10.1.0.20
```

!!! warning "Common errors"
    **`Error: Invalid interface name '<if_name>'`** — Replace `<if_name>` with an actual interface name like `eth0` or `mgmt0`.
    **`Error: Connection refused — unable to reach management IP`** — Verify the FlashBlade management IP is reachable and the purefb CLI is authenticated with `purefb login`.
### Subnets

```bash
purefb subnet show

purefb subnet create \
    --name <subnet_name> \
    --prefix <cidr> \
    --gateway <gateway_ip>

purefb subnet delete --name <subnet_name>
```


```text title="Expected output"
Name          Prefix            Gateway         VLAN
subnet-mgmt   10.0.1.0/24       10.0.1.1        100
subnet-data   10.0.2.0/24       10.0.2.1        101
subnet-repl   10.0.3.0/24       10.0.3.1        102

Created subnet 'subnet-prod' with prefix 10.0.4.0/24 and gateway 10.0.4.1
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Subnet 'subnet-prod' already exists`** — Verify the subnet name is unique or delete the existing subnet before recreating it.
    **`Error: Invalid CIDR prefix '<cidr>' — must be /24 to /30`** — Ensure the subnet prefix is within the supported range (typically /24 to /30 for FlashBlade).
    **`Error: Gateway IP '<gateway_ip>' is not in subnet prefix range`** — Confirm the gateway IP falls within the specified CIDR block (e.g., 10.0.4.1 for 10.0.4.0/24).
### DNS and NTP

```bash
# DNS
purefb dns show
purefb dns update --nameservers <ns1_ip>,<ns2_ip>
purefb dns update --search <search_domain>

# NTP
purefb ntp show
purefb ntp update --ntpservers <ntp1_ip>,<ntp2_ip>
```


```text title="Expected output"
# DNS
Name Servers
  8.8.8.8
  8.8.4.4
Search Domains
  corp.example.com

(no output — command completes silently)
(no output — command completes silently)

# NTP
NTP Servers
  ntp1.corp.example.com (10.20.30.40)
  ntp2.corp.example.com (10.20.30.41)
Enabled: true

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Invalid IP address format`** — Verify the IP addresses are correctly formatted and separated by commas with no spaces (e.g., `10.0.0.1,10.0.0.2`).
    **`Error: Connection refused to management interface`** — Ensure the FlashBlade management IP is reachable and the `purefb` CLI is authenticated with valid credentials.
    **`Error: DNS/NTP server unreachable`** — Confirm the specified nameserver or NTP server IPs are accessible from the FlashBlade's management network before applying the update.
### VIPs (Virtual IPs) for NFS/SMB

VIPs are what NFS/SMB clients mount — they float between blades for availability:

```bash
# List VIPs
purefb vip show

# Create a VIP
purefb vip create \
    --name <vip_name> \
    --address <vip_ip> \
    --subnet <subnet_name> \
    --services <nfs,smb>
```


```text title="Expected output"
Name          Address         Subnet          Services        Status
management    192.168.1.10    mgmt-subnet     nfs,smb         active
replication   192.168.1.11    mgmt-subnet     replication     active
backup        192.168.1.12    backup-subnet   nfs             active

Name          Address         Subnet          Services        Status
data-vip-01   192.168.1.20    data-subnet     nfs,smb         active
```

!!! warning "Common errors"
    **`Error: VIP address 192.168.1.20 already in use`** — Verify the IP address is not assigned to another VIP or host on the network using `purefb vip show`.
    **`Error: Subnet 'subnet_name' not found`** — Confirm the subnet exists by running `purefb subnet show` and use the correct subnet name.
    **`Error: Invalid service specification: smb`** — Ensure service names are lowercase and comma-separated without spaces (e.g., `--services nfs,smb`).
### Static Routes

```bash
purefb static-route show

purefb static-route create \
    --address <destination_cidr> \
    --gateway <gateway_ip>
```


```text title="Expected output"
Name                Address         Gateway         Metric
default             0.0.0.0/0       10.20.1.1       0
corp-network        192.168.0.0/16  10.20.1.254     10
dmz-segment         172.16.0.0/12   10.20.2.1       20

Static route created successfully.
Name: prod-backup
Address: 10.100.0.0/24
Gateway: 10.20.1.100
Metric: 0
```

!!! warning "Common errors"
    **`Error: Invalid CIDR notation for address`** — Verify the destination_cidr parameter uses valid CIDR format (e.g., 10.0.0.0/8) and is not malformed.
    **`Error: Gateway IP 10.20.1.254 is not reachable on any configured interface`** — Ensure the gateway_ip is on a subnet directly connected to one of the FlashBlade's network interfaces.
    **`Error: Static route to 192.168.0.0/16 already exists`** — Delete the existing route first using `purefb static-route delete --address 192.168.0.0/16` or modify it with the `--metric` flag.
### Network Troubleshooting

```bash
# Interface errors and statistics
purefb network-interface show --detailed | grep -i error

# Ping from FlashBlade
purefb ping --to <destination_ip>

# DNS resolution test
purefb dns-lookup --name <hostname>
```


```text title="Expected output"
# Interface errors and statistics
eth0.mgmt                errors_in: 0          errors_out: 0          crc_errors: 0
eth1.data                errors_in: 0          errors_out: 0          crc_errors: 0
eth2.data                errors_in: 12         errors_out: 3          crc_errors: 0
eth3.replication         errors_in: 0          errors_out: 0          crc_errors: 0

# Ping from FlashBlade
PING 192.168.1.50 (192.168.1.50) from 10.20.30.40
64 bytes from 192.168.1.50: icmp_seq=1 ttl=64 time=2.341 ms
64 bytes from 192.168.1.50: icmp_seq=2 ttl=64 time=2.156 ms
64 bytes from 192.168.1.50: icmp_seq=3 ttl=64 time=2.289 ms
64 bytes from 192.168.1.50: icmp_seq=4 ttl=64 time=2.412 ms
--- 192.168.1.50 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3012ms

# DNS resolution test
Resolving storage.example.com...
storage.example.com resolves to 10.20.30.50
```

!!! warning "Common errors"
    **`Error: Invalid destination IP address`** — Verify the destination IP is valid and reachable from the FlashBlade management network.
    **`Error: DNS lookup failed for <hostname>`** — Confirm the hostname is correct and DNS servers are configured and accessible on the FlashBlade.
    **`Error: Connection timeout - no response from <destination_ip>`** — Check network connectivity, firewall rules, and that the destination host is online and responding to ICMP.
| Issue | Check | Command |
|---|---|---|
| NFS mount fails | VIP exists and reachable? | `purefb vip show` |
| DNS not resolving | DNS servers configured? | `purefb dns show` |
| Interface down | Physical link? | `purefb network-interface show` |
| Replication not connecting | Remote array management IP reachable? | `purefb remote-array show` |

---

## Object Store (S3)

FlashBlade serves S3-compatible object storage. Buckets hold objects (files), accounts group users, and access keys authenticate S3 API calls.

### Buckets

```bash
# List buckets
purefb bucket list
purefb bucket list --all          # includes destroyed

# Create a bucket
purefb bucket create --name <bucket> --account <account>

# Destroy a bucket (must be empty)
purefb bucket destroy --name <bucket>

# Eradicate permanently
purefb bucket eradicate --name <bucket>
```


```text title="Expected output"
purefb bucket list
Name                          Account              Created
test-backup-01                prod-account         2024-01-15T09:23:44Z
analytics-data-v2             analytics-team       2024-01-10T14:51:22Z
archive-2024-q1               compliance           2024-01-08T07:19:33Z
dev-scratch                    engineering         2024-01-12T16:45:10Z

purefb bucket list --all
Name                          Account              Created              Destroyed
test-backup-01                prod-account         2024-01-15T09:23:44Z
analytics-data-v2             analytics-team       2024-01-10T14:51:22Z
archive-2024-q1               compliance           2024-01-08T07:19:33Z
dev-scratch                    engineering         2024-01-12T16:45:10Z
old-logs-archive              legacy-ops           2023-12-20T11:02:15Z 2024-01-18T13:47:29Z

purefb bucket create --name backup-prod-02 --account prod-account
Created bucket 'backup-prod-02'

purefb bucket destroy --name backup-prod-02
Destroyed bucket 'backup-prod-02'

purefb bucket eradicate --name backup-prod-02
Eradicated bucket 'backup-prod-02'
```

!!! warning "Common errors"
    **`Error: Bucket 'backup-prod-02' is not empty`** — Use `purefb bucket list-objects --name <bucket>` to verify contents, then delete objects before destroying the bucket.
    **`Error: Bucket 'backup-prod-02' not found`** — Verify the bucket name spelling and that it has not already been eradicated; use `purefb bucket list --all` to confirm its status.
### Accounts and Users

```bash
# List object store accounts (tenants)
purefb object-store-account list

# Create an account
purefb object-store-account create --name <account>

# List users
purefb object-store-user list

# Create a user under an account
purefb object-store-user create --name <user> --account <account>

# Destroy a user
purefb object-store-user destroy --name <user> --account <account>
```


```text title="Expected output"
$ purefb object-store-account list
Name                          Created
acme-prod                      2024-01-15T09:23:47Z
acme-dev                       2024-01-14T14:12:33Z
backup-tier                    2024-01-10T16:45:22Z

$ purefb object-store-account create --name finance-ops
Created object store account 'finance-ops'

$ purefb object-store-user list
Name                 Account              Created
s3-backup-user       acme-prod            2024-01-15T10:01:12Z
data-sync-user       acme-dev             2024-01-14T15:33:44Z
archive-bot          backup-tier          2024-01-12T08:22:55Z

$ purefb object-store-user create --name etl-service --account finance-ops
Created object store user 'etl-service' in account 'finance-ops'
Access Key: PSFB123456789ABCDEF01
Secret Key: 8xK9mL2pQ4vW6yN8jH5gF3dR7sT1uV4xZ9cB2eM5nP

$ purefb object-store-user destroy --name etl-service --account finance-ops
Destroyed object store user 'etl-service' from account 'finance-ops'
```

!!! warning "Common errors"
    **`Error: Account '<account>' not found`** — Verify the account name exists with `purefb object-store-account list` and use the correct spelling.
    **`Error: User '<user>' not found in account '<account>'`** — Confirm the user exists in the specified account using `purefb object-store-user list` before attempting to destroy.
### Access Keys

```bash
# List all access keys
purefb object-store-access-key list

# Create an access key for a user
purefb object-store-access-key create --user <user>/<account>

# Delete an access key
purefb object-store-access-key destroy --name <key_id>
```


```text title="Expected output"
# List all access keys
Name                                 User/Account         Created                  Last Used
9a7f2c1e-4b9d-11ec-81d4-0242ac130002 admin/acme-prod      2024-01-15T09:23:44Z     2024-01-18T14:52:10Z
b3e8d5f2-7c2a-11ec-92e5-0242ac130003 devops/acme-prod     2024-01-10T16:45:22Z     2024-01-19T08:15:33Z
c4f9e6g3-8d3b-11ec-a3f6-0242ac130004 backup/acme-staging  2024-01-12T11:30:15Z     2024-01-17T22:41:05Z

# Create an access key for a user
Access Key Name: d5g0h7i4-9e4c-11ec-b4g7-0242ac130005
Access Key ID: AKIAIOSFODNN7EXAMPLE
Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# Delete an access key
Destroyed access key: 9a7f2c1e-4b9d-11ec-81d4-0242ac130002
```

!!! warning "Common errors"
    **`Error: user '<user>/<account>' not found`** — Verify the user and account exist on the FlashBlade system using `purefb admin list`.
    **`Error: access key '<key_id>' not found`** — Confirm the key ID is correct by running `purefb object-store-access-key list` to see all available keys.
> The secret access key is only shown at creation time — store it securely immediately.

### S3 Endpoint

```bash
# Show S3 service endpoint
purefb array | grep s3

# Test S3 connectivity
aws s3 ls --endpoint-url https://<flashblade_s3_vip>/
```


```text title="Expected output"
Name                          S3 Endpoint
flashblade-prod-01            s3.flashblade.internal
flashblade-prod-02            s3.flashblade.internal

An error occurred (InvalidAccessKeyId) when calling the ListBuckets operation: The Access Key Id you provided does not exist in our records.
```

!!! warning "Common errors"
    **`An error occurred (InvalidAccessKeyId) when calling the ListBuckets operation: The Access Key Id you provided does not exist in our records.`** — Verify AWS credentials are configured correctly with `aws configure` and match a valid FlashBlade S3 user account.
    **`Unable to locate credentials`** — Set AWS credentials via environment variables (`export AWS_ACCESS_KEY_ID=...`) or create `~/.aws/credentials` with valid FlashBlade S3 access keys.
    **`SSL: CERTIFICATE_VERIFY_FAILED`** — Add `--no-verify-ssl` flag to the aws command or configure a trusted CA certificate for the FlashBlade S3 endpoint.
### Bucket Replication

```bash
# List bucket replica links
purefb bucket-replica-link list

# Create a replica link to a remote FlashBlade
purefb bucket-replica-link create \
    --local-bucket <local_bucket> \
    --remote-bucket <remote_bucket> \
    --remote <remote_array_name>
```


```text title="Expected output"
Name                          Remote Array      Remote Bucket         Direction    Status
us-east-backup                fb-west-01        prod-data-backup      Bidirectional  Connected
eu-central-replica            fb-eu-02          eu-prod-data          Unidirectional  Connected
asia-dr-link                  fb-asia-01        asia-backup           Unidirectional  Disconnected

Replica link 'us-west-dr' created successfully.
Local Bucket: prod-analytics
Remote Bucket: analytics-replica
Remote Array: fb-west-02
Direction: Unidirectional
Status: Connecting
```

!!! warning "Common errors"
    **`Error: bucket 'prod-data' not found on local array`** — Verify the local bucket name exists with `purefb bucket list` and matches the `--local-bucket` parameter exactly.
    **`Error: unable to connect to remote array 'fb-west-01': connection timeout`** — Confirm the remote array name is registered and reachable by running `purefb array list --remote` and checking network connectivity.
    **`Error: bucket 'backup-replica' already has an active replica link`** — Remove the existing replica link with `purefb bucket-replica-link delete <link_name>` before creating a new one to the same bucket.
---

## Replication (ActiveDR)

FlashBlade supports asynchronous snapshot-based replication and ActiveDR (near-synchronous) for file systems.

### Remote Array (Replication Target)

```bash
# List configured remote arrays
purefb remote-array show

# Add a replication target
purefb remote-array create \
    --name <target_name> \
    --management-address <target_management_ip>
```


```text title="Expected output"
Name                    Management Address      Status      Connection Status
target-array-01         192.168.1.50            Connected   Online
target-array-02         192.168.1.51            Connected   Online
target-array-03         192.168.1.52            Disconnected Offline

Remote Array 'prod-dr-array' created successfully.
Management Address: 10.20.30.40
Status: Connecting
Connection Status: Pending
```

!!! warning "Common errors"
    **`Error: Management address 10.20.30.40 is unreachable`** — Verify network connectivity to the target array's management IP and ensure firewall rules permit FlashBlade replication traffic.
    **`Error: Remote array name 'target-array-01' already exists`** — Use a unique name for the new remote array or remove the existing configuration first with `purefb remote-array delete`.
### File System Replica Links

```bash
# List all replica links
purefb fs-replica-link show

# Detailed view — state, lag, direction
purefb fs-replica-link show --detailed

# Create a replica link
purefb fs-replica-link create \
    --local-filesystem <local_fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>
```


```text title="Expected output"
Name                          Direction  State      Remote Array      Remote Filesystem
fs-prod-replica               Outbound   Idle       flashblade-dr     fs-prod-backup
fs-logs-replica               Outbound   Syncing    flashblade-dr     fs-logs-archive
fs-archive-replica            Outbound   Idle       flashblade-west   fs-archive-copy
fs-db-replica                 Inbound    Idle       flashblade-main   fs-database

Name                          Direction  State      Remote Array      Remote Filesystem    Lag (ms)  Last Update
fs-prod-replica               Outbound   Idle       flashblade-dr     fs-prod-backup       0         2024-01-15T14:32:18Z
fs-logs-replica               Outbound   Syncing    flashblade-dr     fs-logs-archive      245       2024-01-15T14:32:05Z
fs-archive-replica            Outbound   Idle       flashblade-west   fs-archive-copy      12        2024-01-15T14:31:52Z
fs-db-replica                 Inbound    Idle       flashblade-main   fs-database          0         2024-01-15T14:32:18Z

Created replica link 'fs-prod-replica' from fs-prod to fs-prod-backup on flashblade-dr
```

!!! warning "Common errors"
    **`Error: filesystem 'fs-prod' not found on local array`** — Verify the local filesystem name matches exactly with `purefb fs show` output.
    **`Error: unable to connect to remote array 'flashblade-dr': connection timeout`** — Ensure the remote array hostname is reachable and configured in the replication network settings.
    **`Error: replica link 'fs-prod-replica' already exists`** — Use a unique replica link name or delete the existing link before recreating it.
### Replication Status

| Status | Meaning |
|---|---|
| `replicating` | Data actively syncing |
| `idle` | Up to date — no new changes |
| `paused` | Manually suspended |
| `broken` | Link failed — investigate |

### Pause and Resume

```bash
# Pause replication
purefb fs-replica-link update \
    --paused true \
    --local-filesystem <fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>

# Resume replication
purefb fs-replica-link update \
    --paused false \
    --local-filesystem <fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>

# Delete a replica link
purefb fs-replica-link delete \
    --local-filesystem <fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>

# Monitor lag
purefb fs-replica-link show --detailed | grep -i lag
```


```text title="Expected output"
Name: prod-data
Local Filesystem: prod-data
Remote Filesystem: prod-data-dr
Remote Array: flashblade-dr.example.com
Paused: true
Last Replicated: 2024-01-15T14:32:18Z
Replication Lag: 0 bytes

Name: prod-data
Local Filesystem: prod-data
Remote Filesystem: prod-data-dr
Remote Array: flashblade-dr.example.com
Paused: false
Last Replicated: 2024-01-15T14:35:42Z
Replication Lag: 0 bytes

Replica link deleted successfully.

Replication Lag: 1.2 GB
Replication Lag: 0 bytes
```

!!! warning "Common errors"
    **`Error: Filesystem 'prod-data' not found on local array`** — Verify the local filesystem name matches exactly with `purefb fs list` output.
    **`Error: Connection to remote array 'flashblade-dr.example.com' failed`** — Confirm the remote array hostname is reachable and the replication link credentials are configured with `purefb connect`.
    **`Error: Replica link does not exist between 'prod-data' and 'prod-data-dr'`** — Check that the replica link is already established using `purefb fs-replica-link list` before attempting to pause or delete.
### Object Store Replication (Buckets)

```bash
purefb os-replica-link show

purefb os-replica-link create \
    --local-bucket <bucket_name> \
    --remote-bucket <remote_bucket_name> \
    --remote-array <target_name>
```


```text title="Expected output"
Name                  Local Bucket      Remote Bucket     Remote Array      Direction  Status
replica-link-prod-01  data-archive      data-archive-dr   fb-dr-array-02    Outbound   Connected
replica-link-prod-02  logs-backup       logs-backup-dr    fb-dr-array-02    Outbound   Connected

Creating replica link...
Name: replica-link-prod-03
Local Bucket: customer-data
Remote Bucket: customer-data-dr
Remote Array: fb-dr-array-02
Direction: Outbound
Status: Connecting
```

!!! warning "Common errors"
    **`Error: bucket '<bucket_name>' not found`** — Verify the local bucket exists with `purefb bucket list` and use the correct bucket name.
    **`Error: remote array '<target_name>' is not connected`** — Ensure the remote array is reachable and has an established connection using `purefb array-connection show`.
    **`Error: replica link already exists between these buckets`** — Check existing replica links with `purefb os-replica-link show` and use a different bucket pair or remove the existing link first.
---

## Snapshots

Snapshots are instant, space-efficient point-in-time copies of file systems. They are read-only and accessible via the `.snapshot` directory inside any NFS export.

### List Snapshots

```bash
purefb snapshot show
purefb snapshot show --source <filesystem_name>
purefb snapshot show --name <snapshot_name>
```


```text title="Expected output"
Name                          Source                        Created                       Size
snapshot-prod-2024-01-15      data-tier-01                  2024-01-15T09:23:47Z          2.3TB
snapshot-prod-2024-01-14      data-tier-01                  2024-01-14T09:15:22Z          2.3TB
snapshot-backup-weekly        backup-fs                     2024-01-14T02:00:00Z          1.8TB
snapshot-archive-q1           archive-storage               2024-01-10T18:45:33Z          4.7TB
snapshot-dev-test-01          dev-filesystem                2024-01-09T14:22:11Z          512GB
...

Name                          Source                        Created                       Size
snapshot-prod-2024-01-15      data-tier-01                  2024-01-15T09:23:47Z          2.3TB
snapshot-prod-2024-01-14      data-tier-01                  2024-01-14T09:15:22Z          2.3TB

Name                          Source                        Created                       Size
snapshot-prod-2024-01-15      data-tier-01                  2024-01-15T09:23:47Z          2.3TB
```

!!! warning "Common errors"
    **`Error: filesystem <filesystem_name> not found`** — Verify the filesystem name exists using `purefb filesystem show` and check for typos.
    **`Error: snapshot <snapshot_name> does not exist`** — Confirm the snapshot name is correct and has not been deleted with `purefb snapshot show`.
### Create a Snapshot

```bash
# Manual snapshot of a file system
purefb snapshot create \
    --source <filesystem_name> \
    --name <snapshot_name>

# Pre-change snapshot example
purefb snapshot create --source prod-nfs --name pre-maint-20260506
```


```text title="Expected output"
Created snapshot 'pre-maint-20260506' from filesystem 'prod-nfs'
Snapshot ID: 8c4e9f2a-7b1d-4e6c-9a3f-2d8e5c1b4a9f
Source Filesystem: prod-nfs
Size: 2.3 TB
Created: 2026-05-06T14:32:18Z
```

!!! warning "Common errors"
    **`Error: filesystem 'prod-nfs' not found`** — Verify the filesystem name exists with `purefb fs list` and correct any typos in the `--source` parameter.
    **`Error: snapshot 'pre-maint-20260506' already exists`** — Use a unique snapshot name or delete the existing snapshot with `purefb snapshot delete --name pre-maint-20260506` before retrying.
    **`Error: insufficient space for snapshot`** — Check available capacity on the array with `purefb capacity` and ensure at least 10% free space remains.
### Restore from Snapshot

```bash
# Restore (copy) a snapshot to a new file system
purefb snapshot copy \
    --name <snapshot_name> \
    --target <new_filesystem_name>
```


```text title="Expected output"
Restoring snapshot 'daily-backup-2024-01-15' to new filesystem 'prod-fs-restored'...
Snapshot copy initiated.
Source: daily-backup-2024-01-15 (size: 2.3 TiB, created: 2024-01-15T09:30:00Z)
Target: prod-fs-restored
Status: In Progress
Job ID: job-a7f3c9e2-1b4d-4a8f-9c2e-5d8f1a3b6c9e
Estimated time remaining: 18 minutes
```

!!! warning "Common errors"
    **`Error: Snapshot 'daily-backup-2024-01-15' not found`** — Verify the snapshot name with `purefb snapshot list` and ensure it exists on the array.
    **`Error: Filesystem 'prod-fs-restored' already exists`** — Use a unique target filesystem name or delete the existing filesystem before retrying the copy operation.
    **`Error: Insufficient space available on array`** — Check available capacity with `purefb array info` and ensure the target filesystem size fits within remaining array capacity.
### Destroy and Eradicate

```bash
# Step 1 — destroy (moves to pending eradication)
purefb snapshot destroy --name <snapshot_name>

# Step 2 — eradicate (permanently deletes — 24-hour hold by default)
purefb snapshot eradicate --name <snapshot_name>

# List pending eradication items
purefb snapshot show --pending-only
```


```text title="Expected output"
Snapshot 'daily-backup-2024-01-15' destroyed successfully.
Snapshot 'daily-backup-2024-01-15' eradicated successfully.

Name                          Created                  Destroyed                 Eradicated
daily-backup-2024-01-15       2024-01-15T08:30:22Z     2024-01-15T14:45:10Z      —
weekly-backup-2024-01-08      2024-01-08T09:00:00Z     2024-01-15T10:22:15Z      —
hourly-backup-2024-01-15-14   2024-01-15T14:00:00Z     2024-01-15T14:30:45Z      —
```

!!! warning "Common errors"
    **`Error: Snapshot '<snapshot_name>' not found`** — Verify the snapshot name with `purefb snapshot show` and use the exact name including any timestamp or suffix.
    **`Error: Snapshot '<snapshot_name>' is in use by replication or clone`** — Check active replications or clones with `purefb snapshot show --detail` and remove dependencies before destruction.
### Scheduled Snapshot Policies

```bash
# List snapshot policies
purefb snapshot-rule show

# Create a snapshot policy
purefb snapshot-rule create \
    --name <rule_name> \
    --keep-for 7d

# Attach a policy to a file system
purefb fs-snapshot-rule create \
    --filesystem <fs_name> \
    --rule <rule_name>
```


```text title="Expected output"
Name                Frequency    Keep For    At
daily-backup        daily        7d          00:00
weekly-archive      weekly       30d         Sunday 02:00
monthly-retain      monthly      90d         1st 00:00

Rule 'hourly-snapshots' created successfully
Snapshot rule 'hourly-snapshots' (keep-for: 7d) attached to filesystem 'data-vol-01'
```

!!! warning "Common errors"
    **`Error: Filesystem 'data-vol-01' not found`** — Verify the filesystem name exists with `purefb fs list` and use the correct name.
    **`Error: Snapshot rule 'hourly-snapshots' already attached to filesystem 'data-vol-01'`** — Remove the existing attachment with `purefb fs-snapshot-rule delete --filesystem <fs_name> --rule <rule_name>` before reattaching.
### Accessing Snapshots via NFS

```bash
# Snapshots are visible in the .snapshot directory on the NFS mount
ls /mnt/nfs_export/.snapshot/

# Restore a file from snapshot
cp /mnt/nfs_export/.snapshot/<snapshot_name>/path/to/file /mnt/nfs_export/path/to/file
```


```text title="Expected output"
daily-2024-01-15-0200
daily-2024-01-16-0200
daily-2024-01-17-0200
hourly-2024-01-17-1400
hourly-2024-01-17-1500
hourly-2024-01-17-1600
weekly-2024-01-14-0000
```

!!! warning "Common errors"
    **`ls: cannot access '/mnt/nfs_export/.snapshot/': No such file or directory`** — Verify the NFS mount is active with `mount | grep nfs_export` and ensure snapshot visibility is enabled on the FlashBlade export policy.
    **`cp: cannot stat '/mnt/nfs_export/.snapshot/<snapshot_name>/path/to/file': No such file or directory`** — Replace `<snapshot_name>` with an actual snapshot name from the listing and verify the source file path exists in that snapshot.
    **`Permission denied`** — Ensure your user has read permissions on the snapshot directory; check with `ls -ld /mnt/nfs_export/.snapshot/` and adjust NFS export permissions if needed.
---

## Users & Authentication

These commands manage admin users, API clients, and directory service (LDAP/AD) integration.

### Local Admin Users

```bash
purefb admin show

purefb admin create --name <username> --role array_admin

purefb admin update --name <username> --password <new_password>

purefb admin delete --name <username>
```


```text title="Expected output"
Name          Role         Created                   Last Login
admin         array_admin  2024-01-15T09:23:44Z     2024-01-18T14:52:12Z
backup_user   readonly     2024-01-10T11:05:22Z     2024-01-17T08:30:45Z
monitor_svc   operator     2024-01-12T16:18:33Z     2024-01-18T13:22:09Z

Admin user 'jsmith' created successfully with role 'array_admin'.

Admin user 'jsmith' password updated successfully.

Admin user 'jsmith' deleted successfully.
```

!!! warning "Common errors"
    **`Error: Admin user 'admin' cannot be deleted`** — Ensure you are not attempting to delete the default admin account; create an alternative admin user first.
    **`Error: User 'jsmith' already exists`** — Choose a unique username or delete the existing user before recreating it with the same name.
    **`Error: Invalid role 'invalid_role'. Valid roles are: array_admin, operator, readonly`** — Specify one of the three valid roles (array_admin, operator, or readonly) in the create command.
### Roles

| Role | Permissions |
|---|---|
| `array_admin` | Full administrative access |
| `readonly` | Read-only — view configuration and stats |
| `ops_admin` | Operational access (not configuration) |

### API Clients

```bash
# List API clients / tokens
purefb api-client show

# Create an API client
purefb api-client create \
    --name <client_name> \
    --role array_admin

# Delete an API client
purefb api-client delete --name <client_name>

# Generate a new API token for a user
purefb admin apitoken create --name <username>
```


```text title="Expected output"
# List API clients / tokens
Name                          Enabled  Role
api-client-prod-01            True     array_admin
api-client-backup-svc         True     array_admin
api-client-monitoring         True     read_only
api-client-legacy-app         False    storage_admin
api-client-dr-replication     True     array_admin

# Create an API client
Name: api-client-prod-02
Role: array_admin
Enabled: True
Created: 2024-01-15T09:42:31Z

# Delete an API client
api-client-prod-02 deleted successfully

# Generate a new API token for a user
Token ID: 8f7e3c2a-91d4-4b6e-8c1f-5a9d2e7b4c6f
Token: T-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Created: 2024-01-15T09:43:15Z
Expires: 2025-01-15T09:43:15Z
```

!!! warning "Common errors"
    **`Error: API client 'api-client-prod-02' not found`** — Verify the client name exists with `purefb api-client show` before attempting deletion.
    **`Error: Role 'invalid_role' is not valid`** — Use only valid roles: `array_admin`, `storage_admin`, or `read_only` when creating API clients.
    **`Error: User '<username>' does not exist`** — Ensure the user account exists on the FlashBlade system before generating an API token.
### Directory Services (LDAP / Active Directory)

```bash
purefb directory-service show

purefb directory-service update \
    --enabled true \
    --uri "ldap://ldap.example.local" \
    --base-dn "DC=corp,DC=local" \
    --bind-user "CN=svcldap,OU=ServiceAccounts,DC=corp,DC=local" \
    --bind-password <password>

purefb directory-service test
```


```text title="Expected output"
Name: default
Enabled: true
URI: ldap://ldap.example.local
Base DN: DC=corp,DC=local
Bind User: CN=svcldap,OU=ServiceAccounts,DC=corp,DC=local
Bind Password: ••••••••
Join Ou: 
Timeout: 30

Name: default
Enabled: true
URI: ldap://ldap.example.local
Base DN: DC=corp,DC=local
Bind User: CN=svcldap,OU=ServiceAccounts,DC=corp,DC=local
Bind Password: ••••••••
Join Ou: 
Timeout: 30

Directory Service Test Results:
Status: PASSED
Connection: OK
Bind: OK
Base DN Search: OK
```

!!! warning "Common errors"
    **`Error: Invalid URI format`** — Verify the LDAP URI follows the format `ldap://hostname:port` or `ldaps://hostname:port` and that the hostname is resolvable.
    **`Error: Bind failed - Invalid credentials`** — Confirm the bind-user DN and bind-password are correct and the service account has permission to query the directory.
    **`Error: Base DN not found`** — Ensure the Base DN path exists in your LDAP directory and matches your domain structure exactly.
### Multi-Factor Authentication

```bash
# MFA configuration
purefb mfa show

# Require MFA for all admin logins
purefb mfa update --enabled true
```


```text title="Expected output"
MFA Status:
  enabled: false
  grace_period: 0

MFA Status:
  enabled: true
  grace_period: 0
```

!!! warning "Common errors"
    **`Error: Invalid credentials or insufficient permissions`** — Ensure your user account has administrative privileges and valid API token authentication is configured.
    **`Error: MFA configuration is not supported on this system`** — Verify the FlashBlade system firmware version supports MFA (requires Purity 3.0+) by running `purefb version`.
### Session Management

```bash
# Active admin sessions
purefb admin show --sessions

# Logout all sessions for a user (emergency)
purefb admin invalidate-sessions --name <username>
```


```text title="Expected output"
Name                IP Address      Login Time           Idle Time
admin               192.168.1.45    2024-01-15 09:23:14  0:02:15
svc-backup          192.168.1.102   2024-01-15 08:45:22  1:34:08
netadmin            192.168.1.67    2024-01-15 10:11:03  0:00:42
readonly-user       192.168.1.88    2024-01-14 16:20:19  18:15:33

Sessions invalidated for user: svc-backup
```

!!! warning "Common errors"
    **`Error: User '<username>' not found`** — Replace `<username>` with an actual user name from the `purefb admin show --sessions` output.
    **`Error: Permission denied`** — Ensure your current admin account has sufficient privileges to invalidate sessions; contact your FlashBlade administrator if needed.
### Audit Log

```bash
# View admin audit log (login, config changes)
purefb audit show

# Export audit log
purefb audit export
```


```text title="Expected output"
Admin Audit Log:
Time                          User          Event Type        Details
2024-01-15T14:32:18Z          admin         LOGIN             Successful login from 192.168.1.50
2024-01-15T14:35:42Z          svc_backup    API_CALL          Created snapshot: daily_backup_001
2024-01-15T14:42:09Z          admin         CONFIG_CHANGE     Modified replication policy: prod-dr
2024-01-15T15:01:33Z          monitor_user  API_CALL          Queried performance metrics
2024-01-15T15:18:55Z          admin         CONFIG_CHANGE     Updated NTP server to 10.0.0.5
2024-01-15T15:45:22Z          svc_backup    API_CALL          Deleted snapshot: weekly_backup_042
2024-01-15T16:02:11Z          admin         LOGOUT            Session terminated

Exporting audit log to: /var/log/purity/audit_export_20240115_160215.csv
Export completed successfully. Records exported: 1247
```

!!! warning "Common errors"
    **`Error: Authentication failed. Invalid credentials.`** — Verify the purefb CLI is authenticated with `purefb login` using valid admin credentials.
    **`Error: Audit log export failed: Insufficient disk space on management interface.`** — Free up space on the management partition or export to an external location using `purefb audit export --target <remote_path>`.
---

## Support & Diagnostics

These commands manage the array's connection to Pure Support.

```bash
# View phone home status
purefb phonehome show

# Send a phone home bundle manually
purefb phonehome send --type auto

# Test phonehome connectivity only
purefb phonehome send --type test

# View remote support configuration
purefb support show

# Enable / disable remote support
purefb support update --enabled true
purefb support update --enabled false

# Export logs for TAC support cases
purefb support log export

# Current Purity//FB version
purefb array show | grep -i version

# Available software upgrades
purefb software show
```


```text title="Expected output"
=== Phone Home Status ===
Name                 Status      Last Update
phonehome            enabled     2024-01-15T09:42:33Z

=== Phone Home Bundle Sent ===
Bundle Type: auto
Status: sent
Timestamp: 2024-01-15T09:43:12Z

=== Phone Home Connectivity Test ===
Test Status: passed
Latency: 142ms
Timestamp: 2024-01-15T09:43:45Z

=== Remote Support Configuration ===
Name                 Enabled     Last Modified
remote_support       true        2024-01-15T08:30:22Z

(no output — command completes silently)
(no output — command completes silently)

=== Support Log Export ===
Export Status: in_progress
Log File: support_logs_fb-m20-12345_20240115_094512.tar.gz
Destination: Pure Support Portal
Estimated Time: 3 minutes

=== Purity//FB Version ===
version                          6.2.1

=== Available Software Upgrades ===
Current Version    Available Version    Release Date       Status
6.2.1              6.2.2                2024-01-10         available
6.2.1              6.3.0                2023-12-15         available
```

!!! warning "Common errors"
    **`Error: Connection refused — ensure the FlashBlade management network is reachable and SSH credentials are configured correctly.`** — Verify network connectivity to the FlashBlade management IP and confirm SSH access with `ssh admin@<fb-mgmt-ip>`.
    **`Error: Permission denied (publickey,password) — user does not have sufficient privileges to execute phonehome commands.`** — Confirm the user account has admin or operator role by running `purefb admin list`.
    **`Error: Phone home bundle send failed: Service unavailable — the phone home service is temporarily offline.`** — Wait 5-10 minutes and retry, or check Pure's status page for known service incidents.
### Alerts

```bash
purefb alert show
purefb alert show --all
purefb alert update --id <alert_id> --status closed
```


```text title="Expected output"
Name                          Severity    Status    Created
alert-001-cpu-high            warning     open      2024-01-15T09:23:45Z
alert-002-ntp-sync            critical    open      2024-01-15T10:12:30Z
alert-003-disk-usage          warning     open      2024-01-14T16:45:22Z

Name                          Severity    Status    Created
alert-001-cpu-high            warning     open      2024-01-15T09:23:45Z
alert-002-ntp-sync            critical    open      2024-01-15T10:12:30Z
alert-003-disk-usage          warning     open      2024-01-14T16:45:22Z
alert-004-repl-lag            info        closed    2024-01-13T08:11:09Z
alert-005-cert-expiry         warning     closed    2024-01-12T14:33:51Z
...

Alert alert-002-ntp-sync updated successfully.
Status: closed
Updated: 2024-01-15T10:15:08Z
```

!!! warning "Common errors"
    **`Error: Invalid alert ID 'alert-999-unknown'`** — Verify the alert ID exists by running `purefb alert show --all` and use the exact Name value from the output.
    **`Error: Authentication failed. Check credentials.`** — Ensure your Pure Storage credentials are configured correctly with `purefb login` or verify environment variables are set.
### Common Support Scenarios

| Issue | First Step | Command |
|---|---|---|
| System alert | Check alert detail | `purefb alert show` |
| Blade failure | Check blade health | `purefb blade show --detailed` |
| Replication issue | Check replica link state | `purefb fs-replica-link show --detailed` |
| Capacity concern | Check capacity | `purefb array show` |
| Phone home not working | Check connectivity | `purefb support show` |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [FlashBlade — Procedures](../procedures/)
- [FlashBlade — Scripts](../scripts/)
- [FlashBlade — Health Checks](../health-checks/)
