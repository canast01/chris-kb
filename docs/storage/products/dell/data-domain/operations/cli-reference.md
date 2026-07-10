---
tags:
  - dell
  - operations
---
# Dell Data Domain CLI Reference

*Applies to: Dell EMC Storage*
![Dell Data Domain CLI Reference](../../../../../assets/storage-dell-data-domain-operations-cli-reference.svg)

```bash
# Create a config backup
config backup create

# List available backups
config backup list

# Show backup details
config backup show

# Restore from a named backup
config backup restore <backup_name>
```


```text title="Expected output"
Creating backup... Done.
Backup ID: backup-20240115-143022
Location: /data/domain0/backup/backup-20240115-143022

Backup Name                          Created              Size       Status
backup-20240115-143022               2024-01-15 14:30:22  2.3 GB     completed
backup-20240114-091547               2024-01-14 09:15:47  2.3 GB     completed
backup-20240113-165833               2024-01-13 16:58:33  2.2 GB     completed

Backup ID:       backup-20240115-143022
Created:         2024-01-15 14:30:22
Size:            2.3 GB
Status:          completed
Checksum:        a7f3e9c2d1b8f4e6
Retention Days:  30
```

!!! warning "Common errors"
    **`Error: Backup name not found`** — Verify the backup name exists by running `config backup list` and use the exact name from the output.
    **`Error: Insufficient space for backup (need 3 GB, have 1.2 GB available)`** — Free up disk space or delete older backups with `config backup delete <backup_name>` before creating a new backup.
    **`Error: Restore operation failed - backup corrupted`** — Verify backup integrity with `config backup validate <backup_name>` and restore from an earlier backup if the current one is damaged.
```bash
# Show SNMP configuration
snmp show config

# Show alert notification config
alerts notify-list show
```

```text title="Expected output"
SNMP Configuration:
  SNMP Version: v2c
  Community String: public
  Trap Destination: 192.168.1.50
  Trap Port: 162
  Engine ID: 800007E5033A4D44E5A1
  System Contact: storage-admin@company.com
  System Location: Data Center 2A

Alert Notification List:
  ID    Recipient              Type      Enabled  Protocol
  ----  ---------------------  --------  -------  --------
  1     alerts@company.com     email     yes      SMTP
  2     192.168.10.100         snmp      yes      SNMPv2c
  3     syslog.internal.net    syslog    yes      UDP:514
  4     pagerduty-webhook      webhook   yes      HTTPS
```

!!! warning "Common errors"
    **`snmp: command not found`** — Verify you are logged into the Data Domain system directly (SSH to the management IP) rather than running from a remote host.
    **`alerts notify-list show: permission denied`** — Ensure your user account has administrative privileges; use `su` or request elevated access from your storage administrator.
```bash
# Show syslog configuration
log show config

# Forward logs to syslog server (via GUI or config file)
# Admintools → Maintenance → Syslog
```

```text title="Expected output"
Syslog Configuration
====================
Syslog Server Address: 192.168.1.45
Syslog Server Port: 514
Protocol: UDP
Facility: LOCAL0
Severity Level: INFO
Status: Enabled
Last Updated: 2024-01-15 14:32:18 UTC

Active Syslog Forwarding Rules:
  Rule 1: system.* → 192.168.1.45:514
  Rule 2: replication.* → 192.168.1.45:514
  Rule 3: alerts.* → 192.168.1.45:514

Connection Status: Connected
Messages Forwarded (24h): 4,287
```

!!! warning "Common errors"
    **`Error: Syslog server unreachable at 192.168.1.45:514`** — Verify network connectivity to the syslog server and confirm the IP address and port are correct in the configuration.
    **`Error: Permission denied - cannot modify syslog configuration`** — Ensure you are logged in with administrative privileges (sysadmin or admin role).
    **`Error: Invalid syslog facility value 'LOCAL9'`** — Use only valid facility values (LOCAL0–LOCAL7, USER, DAEMON, etc.) as defined in RFC 3164.
```bash
config backup create
system show version
net show config
filesys show compression
replication show all
```

```text title="Expected output"
Backup creation initiated. Backup ID: backup-20240115-143022
Backup destination: /backup/system
Backup status: In Progress

Data Domain OS Version: 7.15.1.10
Build: 7.15.1.10-620847
Release Date: 2024-01-10

Interface: eth0
  IP Address: 192.168.1.45
  Netmask: 255.255.255.0
  Gateway: 192.168.1.1
Interface: eth1
  IP Address: 10.20.30.50
  Netmask: 255.255.255.0

Compression Status: Enabled
Compression Ratio: 4.2:1
Compressed Data: 2.3 TB
Uncompressed Data: 9.8 TB

Replication Job: prod-backup-01
  Status: Active
  Remote System: dd-remote-02.corp.local
  Last Sync: 2024-01-15 14:28:15 UTC
  Bytes Replicated: 156.4 GB

Replication Job: archive-weekly
  Status: Idle
  Remote System: dd-archive-01.corp.local
  Last Sync: 2024-01-14 22:00:00 UTC
  Bytes Replicated: 89.2 GB
```

!!! warning "Common errors"
    **`Error: Backup destination /backup/system is full`** — Increase storage capacity or redirect backup destination to a different filesystem with available space.
    **`Error: Replication connection to dd-remote-02.corp.local failed: Connection timeout`** — Verify network connectivity and firewall rules between the primary and remote Data Domain systems.
```bash
# DDBoost service status and connection count
ddboost status

# Active client connections
ddboost show clients
ddboost show clients --verbose
```

```text title="Expected output"
DDBoost Service Status:
  Service Name: DDBoost
  Status: Running
  Port: 19500
  Protocol: TCP
  Connections: 12
  Max Connections: 256
  Uptime: 45 days, 3 hours, 22 minutes
  Version: 7.4.1.0

Active Client Connections:
Host                    User            Protocol  Connected Since         Bytes Sent
backup-srv-01.corp      root            DDBoost   2024-01-15 08:23:14     2.3 TB
backup-srv-02.corp      backupuser      DDBoost   2024-01-14 22:15:47     1.8 TB
nas-primary.local       admin           DDBoost   2024-01-15 06:44:22     892 GB
vm-hypervisor-03        svc_backup      DDBoost   2024-01-13 14:32:09     456 GB
...

Verbose Client Details:
Client ID: 0x4a2c91f3
  Hostname: backup-srv-01.corp
  IP Address: 192.168.10.45
  User: root
  Connection Time: 2024-01-15 08:23:14 UTC
  Session Duration: 31 hours, 12 minutes
  Bytes Sent: 2.3 TB
  Bytes Received: 45 GB
  Active Operations: 2
  Last Activity: 2024-01-15 14:35:22 UTC
```

!!! warning "Common errors"
    **`DDBoost Service Status: Service is not running`** — Start the DDBoost service with `sudo systemctl start ddboost` or equivalent Data Domain management command.
    **`ddboost: command not found`** — Ensure you are logged into the Data Domain system directly (via SSH or console) and that DDBoost CLI tools are in your PATH; check `/opt/ddboost/bin/` exists.
    **`Connection refused on port 19500`** — Verify the DDBoost service is running and listening with `netstat -tlnp | grep 19500` and check firewall rules allow access to port 19500.
```bash
# List all storage units
ddboost storage-unit list
ddboost storage-unit show <storage_unit_name>

# Create a storage unit
ddboost storage-unit create <storage_unit_name>

# Create with MTree path
ddboost storage-unit create <name> --user <ddboost_user>

# Delete a storage unit
ddboost storage-unit delete <storage_unit_name>

# Storage unit usage and quota
ddboost storage-unit show <name> --verbose
```

```text title="Expected output"
# ddboost storage-unit list
Name                          Type        Capacity      Used          Available
backup-prod-01                MTree       10.0 TB       7.2 TB        2.8 TB
backup-prod-02                MTree       10.0 TB       5.1 TB        4.9 TB
backup-dev-01                 MTree       5.0 TB        1.3 TB        3.7 TB
backup-archive-01             MTree       20.0 TB       18.5 TB       1.5 TB
backup-test-01                MTree       2.0 TB        0.8 TB        1.2 TB

# ddboost storage-unit show backup-prod-01
Storage Unit: backup-prod-01
Type: MTree
Status: Active
Capacity: 10.0 TB
Used: 7.2 TB
Available: 2.8 TB
Owner: ddboost_admin
Created: 2024-01-15 09:23:45 UTC

# ddboost storage-unit create backup-prod-03
Storage unit 'backup-prod-03' created successfully
UUID: 550e8400-e29b-41d4-a716-446655440000

# ddboost storage-unit create backup-dev-02 --user ddboost_svc
Storage unit 'backup-dev-02' created successfully with user 'ddboost_svc'
UUID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8

# ddboost storage-unit delete backup-test-01
Warning: This will permanently delete storage unit 'backup-test-01' and all associated data.
Confirm deletion (yes/no): yes
Storage unit 'backup-test-01' deleted successfully

# ddboost storage-unit show backup-prod-02 --verbose
Storage Unit: backup-prod-02
Type: MTree
Status: Active
Capacity: 10.0 TB
Used: 5.1 TB
Available: 4.9 TB
Owner: ddboost_admin
Created: 2024-01-10 14:52:30 UTC
Last Modified: 2024-02-20 08:15:12 UTC
Quota Enabled: Yes
Quota Limit: 10.0 TB
Quota Used: 5.1 TB
Replication Status: Healthy
Last Backup: 2024-02-21 03:45:22 UTC
```

!!! warning "Common errors"
    **`Error: Storage unit 'backup-prod-01' already exists`** — Choose a unique storage unit name or delete the existing unit first.
    **`Error: User 'ddboost_user' not found or insufficient permissions`** — Verify the ddboost user exists and has appropriate Data Domain credentials.
    **`Error: Insufficient capacity to create storage unit`** — Check available space on the Data Domain system and reduce the requested capacity.
```bash
# List DDBoost users
ddboost user list

# Add a user
ddboost user add <username>

# Change password
ddboost user change password <username>

# Assign user to a storage unit
ddboost user assign <username> storage-unit <storage_unit_name>

# Remove user
ddboost user del <username>
```

```text title="Expected output"
User Name                    UID    GID    Home Directory
admin                        0      0      /home/admin
backup_user                  1001   1001   /home/backup_user
replication_svc              1002   1002   /home/replication_svc
archive_mgr                  1003   1003   /home/archive_mgr
(no output — command completes silently)
(no output — command completes silently)
User 'backup_user' successfully assigned to storage unit 'prod-tier1'
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ddboost: command not found`** — Ensure the DDBoost CLI package is installed and the PATH includes the DDBoost binary directory (typically `/opt/ddboost/bin`).
    **`Error: User 'backup_user' already exists`** — Choose a different username or use `ddboost user del <username>` to remove the existing user first.
    **`Error: Storage unit 'prod-tier1' not found`** — Verify the storage unit name exists by running `ddboost storage list` and use the correct name.
```bash
# DDBoost throughput statistics
ddboost show stats

# Connection statistics per client
ddboost show clients --verbose | grep -E "host|throughput|bytes"
```

```text title="Expected output"
DDBoost Statistics:
  Total Throughput: 2.847 GB/s
  Active Connections: 12
  Total Bytes Processed: 18.5 TB
  Average Latency: 4.2 ms
  Peak Throughput: 3.156 GB/s
  Compression Ratio: 2.34:1

Client Connection Statistics:
host: backup-srv-01.corp.local, throughput: 487.3 MB/s, bytes: 2.3 TB
host: backup-srv-02.corp.local, throughput: 512.1 MB/s, bytes: 2.5 TB
host: backup-srv-03.corp.local, throughput: 298.7 MB/s, bytes: 1.8 TB
host: archive-node-04.internal, throughput: 156.2 MB/s, bytes: 892 GB
host: repl-gateway-01.prod, throughput: 1.392 GB/s, bytes: 11.2 TB
...
```

!!! warning "Common errors"
    **`ddboost: command not found`** — Verify DDBoost is installed and the Data Domain CLI is in your PATH, or source the appropriate environment setup script.
    **`Permission denied`** — Ensure your user account has administrative privileges or run the command with appropriate credentials (ssh as sysadmin user or use sudo if configured).
```bash
# DSP status
ddboost option show | grep -i "dist-seg"

# Enable DSP
ddboost option set distributed-segment-processing enabled
```

```text title="Expected output"
Distributed-Segment-Processing: disabled
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ddboost: command not found`** — Ensure you are logged into the Data Domain system via SSH or console, not your local workstation.
    **`Error: option 'distributed-segment-processing' is not recognized`** — Verify the Data Domain firmware version supports DSP; upgrade if running a version older than 7.0.
```bash
# View system log (most recent events)
log view

# List available log files
log list

# Dump the full system log to stdout
log dump system

# Follow the log in real time
log watch

# Specific log file
log view <log_filename>
```

```text title="Expected output"
# log view
2024-01-15 14:32:18 UTC [INFO] Replication job completed successfully for domain: prod-backup-01
2024-01-15 14:28:45 UTC [WARN] Disk utilization at 87% on /dev/sda1
2024-01-15 14:15:22 UTC [INFO] NFS client 192.168.10.45 connected
2024-01-15 14:02:10 UTC [ERROR] SMTP relay timeout connecting to mail.corp.local
2024-01-15 13:58:33 UTC [INFO] Snapshot created: snap-20240115-135833-uuid-a7f2c9e1

# log list
Available log files:
  system.log (current)
  replication.log
  nfs-access.log
  smtp-alerts.log
  backup-jobs.log
  network.log
  authentication.log

# log dump system
2024-01-15 14:32:18 UTC [INFO] Replication job completed successfully for domain: prod-backup-01
2024-01-15 14:28:45 UTC [WARN] Disk utilization at 87% on /dev/sda1
2024-01-15 14:15:22 UTC [INFO] NFS client 192.168.10.45 connected
2024-01-15 14:02:10 UTC [ERROR] SMTP relay timeout connecting to mail.corp.local
2024-01-15 13:58:33 UTC [INFO] Snapshot created: snap-20240115-135833-uuid-a7f2c9e1
2024-01-15 13:45:01 UTC [INFO] System health check passed
...
(output continues for 2847 lines)

# log watch
2024-01-15 14:35:42 UTC [INFO] Garbage collection cycle started
2024-01-15 14:35:51 UTC [INFO] Freed 12.4 GB from expired snapshots
2024-01-15 14:36:03 UTC [WARN] High CPU usage detected: 78%
(watching — press Ctrl+C to exit)

# log view replication.log
2024-01-15 14:32:18 UTC [INFO] Replication job completed: prod-backup-01 → remote-dd-02 (847 GB transferred)
2024-01-15 14:15:05 UTC [INFO] Replication job started: prod-backup-01 → remote-dd-02
2024-01-15 13:22:44 UTC [WARN] Replication bandwidth throttled to 500 Mbps
2024-01-15 12:58:10 UTC [INFO] Replication job completed: archive-01 → remote-dd-03 (156 GB transferred)
```

!!! warning "Common errors"
    **`log view: command not found`** — Ensure you are logged into the Data Domain CLI (use `ssh admin@<dd-ip>`) and have appropriate permissions.
    **`log view <log_filename>: No such file or directory`** — Run `log list` first to verify the exact log filename, then use the correct name from the available list.
    **`log watch: Permission denied`** — Verify your user account has read access to system logs
```bash
# Create a support bundle
support bundle create

# List available bundles
support bundle show

# Export bundle to remote server (SCP)
support bundle export scp://user@host:/path/bundle.tar.gz

# Export bundle to FTP
support bundle export ftp://user:pass@host/path/
```

```text title="Expected output"
Creating support bundle...
Bundle creation in progress: [████████████████████] 100%
Bundle created successfully: bundle_20240115_143022.tar.gz
Bundle size: 2.3 GB
Bundle ID: 550e8400-e29b-41d4-a716-446655440000

Available support bundles:
Name                              Size      Created              Status
bundle_20240115_143022.tar.gz     2.3 GB    2024-01-15 14:30:22  Ready
bundle_20240114_091545.tar.gz     2.1 GB    2024-01-14 09:15:45  Ready
bundle_20240113_165800.tar.gz     2.4 GB    2024-01-13 16:58:00  Ready

Exporting bundle to scp://user@host:/path/bundle.tar.gz
Transfer initiated...
Transfer complete: 2.3 GB transferred in 847 seconds
Bundle exported successfully.

Exporting bundle to ftp://user:pass@host/path/
Transfer initiated...
Transfer complete: 2.3 GB transferred in 923 seconds
Bundle exported successfully.
```

!!! warning "Common errors"
    **`Error: SSH key authentication failed for user@host`** — Verify SSH public key is installed on the remote host and permissions are correct (chmod 600 ~/.ssh/authorized_keys).
    **`Error: FTP connection timeout - unable to reach host:21`** — Confirm the FTP server is reachable and listening on port 21, and check firewall rules allow outbound FTP from the Data Domain.
    **`Error: Insufficient disk space - bundle creation requires 3.5 GB free space, only 1.2 GB available`** — Delete older bundles using `support bundle delete <bundle_name>` or expand storage capacity before retrying.
```bash
# Enter the diagnostic shell
ddsh

# Inside ddsh:
diagnose all             # full system diagnostic run
iostat 1 10              # I/O statistics (1s interval, 10 iterations)
vmstat 1 10              # Virtual memory and CPU stats
netstat -an              # Active network connections
df -h                    # Filesystem usage
top                      # Process list
```

```text title="Expected output"
Data Domain Diagnostic Shell
Copyright (c) Dell Inc. All rights reserved.

dd> diagnose all
Running full system diagnostics...
System Health Status: HEALTHY
  CPU: OK (4 cores, avg load 2.3)
  Memory: OK (32GB total, 24GB free)
  Disks: OK (8 x 4TB, 78% utilized)
  Network: OK (2 x 1GbE active)
  Replication: OK (lag: 45 seconds)
Diagnostic run completed successfully at 2024-01-15 14:32:18 UTC

dd> iostat 1 10
Linux 5.10.0-dd (dd-backup-01)  01/15/2024  _x86_64_
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           18.42    0.00   12.15   8.33    0.00   61.10
Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda             145.20      2048.50      8192.30   2097152   8388608
sdb             142.80      2010.25      8156.75   2060288   8355840
...

dd> vmstat 1 10
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  1      0 24576000 512000 8192000  0    0   512  2048 1200 3400 18 12 62  8  0
 1  0      0 24512000 512000 8192000  0    0   480  2010 1180 3350 17 11 64  8  0
...

dd> netstat -an
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 192.168.1.50:5106       192.168.1.100:443       ESTABLISHED
tcp        0      0 192.168.1.50:5107       192.168.1.101:443       ESTABLISHED
tcp        0      0 192.168.1.50:111        0.0.0.0:*               LISTEN
...

dd> df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   78G   22G  78% /
/dev/mapper/dd-pool0  30T   23.4T  6.6T  78% /data
tmpfs            16G      0   16G   0% /dev/shm
...

dd> top
top - 14:35:22 up 127 days, 3:42,  2 users,  load average: 2.31, 2.18, 2.05
Tasks: 156 total,   3 running, 153 sleeping,   0 stopped,   0 zombie
%Cpu(s): 18.2 us,
```
```bash
# Ping from the Data Domain
net ping <ip>

# Traceroute
net traceroute <ip>

# Interface error counters
net show stats | grep -i error
```

```text title="Expected output"
PING <ip> (192.168.1.50): 56 data bytes
64 bytes from 192.168.1.50: icmp_seq=0. time=2.341 ms
64 bytes from 192.168.1.50: icmp_seq=1. time=2.287 ms
64 bytes from 192.168.1.50: icmp_seq=2. time=2.315 ms
----192.168.1.50 PING Statistics----
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.287/2.314/2.341 ms

traceroute to 192.168.1.50 (192.168.1.50), 30 hops max, 40 byte packets
 1  gateway.local (192.168.1.1)  1.245 ms  1.198 ms  1.267 ms
 2  core-switch.local (10.0.0.1)  3.421 ms  3.398 ms  3.445 ms
 3  192.168.1.50 (192.168.1.50)  4.112 ms  4.089 ms  4.156 ms

Interface: eth0
  RX errors: 0
  TX errors: 0
Interface: eth1
  RX errors: 0
  TX errors: 0
```

!!! warning "Common errors"
    **`net ping: unknown host <ip>`** — Replace `<ip>` with an actual IP address or resolvable hostname.
    **`net traceroute: command not found`** — Verify you are in the Data Domain CLI context; use `net traceroute` only after entering the network shell.
    **`net show stats: No such file or directory`** — Use the correct command syntax `net show interface stats` or check Data Domain OS version compatibility.
```bash
# Overall health check (hardware + software)
health check show

# Disk health
disk show state
disk show detail | grep -E "error|sector"

# Enclosure sensors (temperature, power, fan)
enclosure show hardware
```

```text title="Expected output"
Health Status: HEALTHY
System Uptime: 45 days 12:34:56
CPU Usage: 23%
Memory Usage: 67%
Disk Status: HEALTHY
Replication Status: IDLE

Disk 0.0: HEALTHY
Disk 0.1: HEALTHY
Disk 0.2: HEALTHY
Disk 0.3: HEALTHY
Disk 1.0: HEALTHY
...

Enclosure 0:
  Temperature: 28°C (Normal)
  Power Supply 1: OK (287W)
  Power Supply 2: OK (291W)
  Fan 1: 4200 RPM (Normal)
  Fan 2: 4150 RPM (Normal)
  Fan 3: 4180 RPM (Normal)
```

!!! warning "Common errors"
    **`health check: command not found`** — Verify you are logged into the Data Domain management interface (SSH to the system's management IP, not a client interface).
    **`disk show: permission denied`** — Ensure your user account has administrative privileges; use `sysadmin` or equivalent admin role.
    **`enclosure show hardware: invalid option`** — Check Data Domain firmware version compatibility; some older versions use `enclosure show sensors` instead.
```bash
# Inside ddsh — capture IOPS and throughput
iostat -x 1 30

# Filesystem stats snapshot
filesys show stats

# DDBoost throughput
ddboost show stats
```

```text title="Expected output"
Linux 5.10.0-8-amd64 (dd-backup-01)	01/15/2025	_x86_64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           12.45    0.00   18.32   24.18    0.00   45.05

Device            r/s     w/s     rMB/s     wMB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await svctm  %util
sda             156.2   892.4    245.67   1847.32    12.5    156.8   7.4   14.9   4.2    18.6   1.8   188.4
sdb             148.9   878.1    238.45   1823.19    11.2    152.3   7.0   14.7   4.5    19.2   1.9   194.7

Filesystem Statistics:
  Total Capacity:        450.5 TB
  Used Capacity:         387.2 TB
  Available Capacity:     63.3 TB
  Filesystem Utilization: 85.9%
  Inodes Used:           2,847,392,156
  Inodes Available:      1,152,607,844

DDBoost Statistics:
  Active Connections:    24
  Total Throughput:      2.8 GB/s
  Read Throughput:       1.2 GB/s
  Write Throughput:      1.6 GB/s
  Deduplication Ratio:   4.7:1
  Compression Ratio:     2.1:1
```

!!! warning "Common errors"
    **`ddsh: command not found`** — Ensure you are connected to the Data Domain appliance via SSH or are running commands within an active ddsh session.
    **`filesys show stats: command not found`** — Verify you are in the correct ddsh shell context; exit and re-enter ddsh if needed.
    **`Permission denied`** — Confirm your user account has administrative privileges on the Data Domain system.
```bash
# Export all current and historical alerts
alert show history > /tmp/alert_history.txt
support bundle create   # includes alert history automatically
```

```text title="Expected output"
Alert History exported to /tmp/alert_history.txt
Generating support bundle...
Support bundle created: /var/tmp/support_bundle_20240115_143022.tar.gz
Bundle size: 2.3 GB
Included components: system logs, alert history, performance metrics, configuration backup
Bundle ready for upload to Dell support portal
```

!!! warning "Common errors"
    **`alert show history: command not found`** — Ensure you are logged into the Data Domain CLI (via SSH or console) and not a standard Linux shell; use `sysadmin` or `admin` user context.
    **`support bundle create: insufficient disk space`** — Free up at least 5 GB on /var/tmp by removing old bundles with `support bundle delete <bundle_name>` before retrying.
```bash
# All disks with state (normal, unknown, suspect, failed)
disk show state

# Full hardware detail per disk
disk show hardware

# Disk performance statistics
disk show stats

# Disk error counts
disk show detail | grep -E "slot|error"
```

```text title="Expected output"
Slot 0: state normal, capacity 4.0 TB, temp 38C
Slot 1: state normal, capacity 4.0 TB, temp 39C
Slot 2: state normal, capacity 4.0 TB, temp 37C
Slot 3: state suspect, capacity 4.0 TB, temp 52C
Slot 4: state normal, capacity 4.0 TB, temp 38C
...

Slot 0: SAS 12Gb/s, Seagate Barracuda Pro ST4000DM004, FW CC47, S/N Z305ABCD
Slot 1: SAS 12Gb/s, Seagate Barracuda Pro ST4000DM004, FW CC47, S/N Z305ABCE
Slot 2: SAS 12Gb/s, Seagate Barracuda Pro ST4000DM004, FW CC47, S/N Z305ABCF
...

Slot 0: read_ops 1.2M, write_ops 890K, read_latency_ms 4.3, write_latency_ms 5.1
Slot 1: read_ops 1.1M, write_ops 920K, read_latency_ms 4.1, write_latency_ms 5.3
Slot 2: read_ops 1.3M, write_ops 875K, read_latency_ms 4.5, write_latency_ms 4.9
...

Slot 0: crc_errors 0, timeout_errors 0, media_errors 0
Slot 3: crc_errors 12, timeout_errors 3, media_errors 1
Slot 4: crc_errors 0, timeout_errors 0, media_errors 0
```

!!! warning "Common errors"
    **`disk show: command not found`** — Verify you are logged into the Data Domain management interface (SSH to the appliance IP, not a Linux host).
    **`Permission denied`** — Ensure your user account has administrative privileges; use `sysadmin` or equivalent privileged account.
```bash
# Enclosure hardware overview
enclosure show hardware

# All enclosures with status
enclosure show all

# Specific enclosure
enclosure show hardware enclosure <enc_id>
```

```text title="Expected output"
=== Enclosure Hardware Overview ===
Enclosure ID: enc-001
Model: Dell EMC Data Domain DD9900
Serial Number: 3K8N9L2M5P
Firmware Version: 7.15.1.0
Status: HEALTHY
Power Supplies: 2/2 operational
Cooling Fans: 6/6 operational
Temperature: 22°C (Normal)

=== All Enclosures ===
Enclosure ID    Model              Status      Capacity    Used
enc-001         DD9900             HEALTHY     840TB       612TB
enc-002         DD9900             HEALTHY     840TB       589TB
enc-003         DD9500             DEGRADED    420TB       398TB

=== Enclosure enc-001 Hardware Details ===
Component Type          Slot    Status      Serial Number
Power Supply            PSU-1   OK          PSU-3K8N9L2M-01
Power Supply            PSU-2   OK          PSU-3K8N9L2M-02
Fan Module              FAN-1   OK          FAN-3K8N9L2M-01
Fan Module              FAN-2   OK          FAN-3K8N9L2M-02
Fan Module              FAN-3   OK          FAN-3K8N9L2M-03
NVRAM Battery           NVRAM   OK          NVRAM-3K8N9L2M
```

!!! warning "Common errors"
    **`enclosure: command not found`** — Verify you are logged into the Data Domain CLI (via SSH or console) and not a standard Linux shell.
    **`Invalid enclosure ID: <enc_id>`** — Replace `<enc_id>` with a valid enclosure identifier from the `enclosure show all` output.
    **`Permission denied`** — Ensure your user account has administrative or operator privileges on the Data Domain system.
```bash
# List all tiers (active, cloud)
tier list

# Detail on each tier (capacity, compression, usage)
tier show detail

# Cloud tier configuration (if licensed)
tier show detail cloud
```

```text title="Expected output"
Tier: active
  Capacity: 50.2 TB
  Used: 38.7 TB
  Available: 11.5 TB
  Compression Ratio: 2.3:1

Tier: cloud
  Capacity: 500 TB
  Used: 245.3 TB
  Available: 254.7 TB
  Compression Ratio: 1.8:1

Tier Name: active
  Total Capacity: 50.2 TB
  Used Capacity: 38.7 TB
  Compression Enabled: yes
  Compression Ratio: 2.3:1
  Replication Status: healthy
  Last Backup: 2024-01-15 03:22:15 UTC

Tier Name: cloud
  Total Capacity: 500 TB
  Used Capacity: 245.3 TB
  Cloud Provider: AWS S3
  Bucket Name: dd-backup-prod-us-east-1
  Compression Enabled: yes
  Compression Ratio: 1.8:1
  Replication Status: healthy
  Last Sync: 2024-01-15 02:45:33 UTC
```

!!! warning "Common errors"
    **`Error: Cloud tier not licensed`** — Verify the Data Domain license includes cloud tiering by running `license show` and contact Dell support if the feature is not enabled.
    **`Error: Tier 'cloud' does not exist`** — Initialize the cloud tier first using `tier create cloud` with appropriate cloud provider credentials and bucket configuration.
```bash
# RAID group state and disk members
raid show all
raid show detail

# RAID rebuilding progress (after disk replacement)
raid show detail | grep -E "Rebuilding|Complete"
```

```text title="Expected output"
RAID Group 0 (RAID 6):
  State: Optimal
  Disk Members: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5
  Capacity: 7.2 TB
  Used: 5.8 TB

RAID Group 1 (RAID 6):
  State: Optimal
  Disk Members: 1.0, 1.1, 1.2, 1.3, 1.4, 1.5
  Capacity: 7.2 TB
  Used: 4.2 TB

RAID Group 0 Detail:
  State: Optimal
  Stripe Size: 64 KB
  Block Size: 4 KB
  Hot Spares: 2
  Disk 0.0: Online, 1.2 TB
  Disk 0.1: Online, 1.2 TB
  Disk 0.2: Online, 1.2 TB
  Disk 0.3: Online, 1.2 TB
  Disk 0.4: Online, 1.2 TB
  Disk 0.5: Online, 1.2 TB

Rebuilding: 45% Complete
Rebuilding: 67% Complete
```

!!! warning "Common errors"
    **`raid: command not found`** — Verify you are logged into the Data Domain management interface (SSH to the system's IP address) and not a local workstation shell.
    **`Error: RAID group not accessible`** — Check that no disks are in Failed state by running `disk show all` and replace any failed disks before querying RAID status.
```bash
# Filesystem space usage
filesys show space

# Compressed vs logical usage
filesys show compression summary

# Tier capacity breakdown
tier show detail
```

```text title="Expected output"
Filesystem space used: 2.3 TB
Filesystem space available: 8.7 TB
Filesystem space total: 11.0 TB

Compression ratio: 3.2:1
Logical GB: 7,456
Compressed GB: 2,328
Compression savings: 5,128 GB

Tier Name: Performance
  Capacity: 2.0 TB
  Used: 1.8 TB
  Available: 0.2 TB
  
Tier Name: Capacity
  Capacity: 9.0 TB
  Used: 3.2 TB
  Available: 5.8 TB
```

!!! warning "Common errors"
    **`Error: filesys command not found`** — Verify you are logged into the Data Domain CLI (use `sysconfig show` to confirm system access) and not a standard Linux shell.
    **`Error: Permission denied - insufficient privileges`** — Ensure your user account has admin or operator role; use `user show` to check current permissions.
    **`Error: Tier show detail: invalid syntax`** — Use the correct command `tier show` or `tier show capacity` depending on your Data Domain OS version.
```bash
# List all NFS exports
nfs show exports

# NFS service status
nfs status

# NFS client connections
nfs show clients
```

```text title="Expected output"
NFS Exports:
/data/backup1                    192.168.1.0/24(rw,sync,no_root_squash)
/data/backup2                    10.0.0.0/8(ro,sync,root_squash)
/data/archive                    172.16.50.0/24(rw,async,no_subtree_check)
/mnt/replication                 *
Total exports: 4

NFS Service Status: RUNNING
Process ID: 2847
Uptime: 45 days 12:34:56
Port: 2049

NFS Client Connections:
Client IP          Mount Point         Access Type  Connected Since
192.168.1.105      /data/backup1       rw           2024-01-15 09:23:14
192.168.1.110      /data/backup1       ro           2024-01-14 16:45:22
10.0.2.50         /data/backup2       ro           2024-01-15 02:11:08
172.16.50.25      /data/archive       rw           2024-01-12 18:56:41
Total connections: 4
```

!!! warning "Common errors"
    **`NFS service is not running`** — Run `nfs start` to enable the NFS service.
    **`Permission denied: cannot list exports`** — Verify your user account has administrative privileges or use `sudo` if available.
```bash
# Create an NFS export for an MTree
nfs add export /data/col1/<mtree_name> clients <ip_or_cidr>

# Allow multiple clients
nfs add export /data/col1/<mtree_name> clients <ip1>,<ip2>

# Modify export options (root squash, read-write)
nfs modify export /data/col1/<mtree_name> clients <ip> options rw,root-squash

# Remove a client from an export
nfs del export /data/col1/<mtree_name> clients <ip_or_cidr>

# Remove the entire export
nfs del export /data/col1/<mtree_name>
```

```text title="Expected output"
NFS export /data/col1/backup_mtree added successfully
  Clients: 192.168.1.50
  Options: default

NFS export /data/col1/backup_mtree modified successfully
  Clients: 192.168.1.50,192.168.1.51
  Options: default

NFS export /data/col1/backup_mtree modified successfully
  Clients: 192.168.1.50
  Options: rw,root-squash

Client 192.168.1.50 removed from export /data/col1/backup_mtree
  Remaining clients: 192.168.1.51

NFS export /data/col1/backup_mtree removed successfully
```

!!! warning "Common errors"
    **`Error: Export path /data/col1/backup_mtree does not exist`** — Verify the MTree name is correct and the MTree has been created with `mtree create`.
    **`Error: Invalid client IP address <ip_or_cidr>`** — Ensure the IP address or CIDR notation is properly formatted (e.g., 192.168.1.0/24 or 10.0.0.5).
    **`Error: Client <ip> is not authorized for this export`** — Confirm the client IP exists in the export's client list before attempting to remove it.
```bash
# CIFS service status and configuration
cifs show

# Active client connections
cifs show clients

# All CIFS shares
cifs share show

# Create a CIFS share for an MTree
cifs share add /data/col1/<mtree_name>

# Remove a CIFS share
cifs share del /data/col1/<mtree_name>
```

```text title="Expected output"
# CIFS show
CIFS Service: enabled
CIFS Server Name: dd-storage-01
Workgroup: CORP
Domain: corp.local
Domain Controller: dc01.corp.local
CIFS Port: 445
NetBIOS Port: 139

# CIFS show clients
Client IP          Connected Since      User              Share
192.168.10.45      2024-01-15 09:23:11  corp\jsmith       data-col1-prod
192.168.10.67      2024-01-15 08:15:44  corp\achen        backup-archive
192.168.10.89      2024-01-15 10:02:33  corp\mwilson      data-col1-prod
10.50.20.112       2024-01-15 07:44:22  corp\sroberts     reports-share
...

# CIFS share show
Share Name                    Path                          Comment
data-col1-prod                /data/col1/mtree_prod         Production data
data-col1-dev                 /data/col1/mtree_dev          Development data
backup-archive                /data/col1/mtree_archive      Archive backups
reports-share                 /data/col1/mtree_reports      Reporting data

# CIFS share add /data/col1/mtree_analytics
Share added successfully: /data/col1/mtree_analytics

# CIFS share del /data/col1/mtree_analytics
Share deleted successfully: /data/col1/mtree_analytics
```

!!! warning "Common errors"
    **`Error: Share path does not exist`** — Verify the MTree exists with `mtree show` and use the correct path `/data/col1/<mtree_name>`.
    **`Error: Share already exists`** — Remove the existing share with `cifs share del` before attempting to add a share with the same path.
    **`Error: Cannot delete share - active client connections`** — Disconnect all clients from the share or use `cifs share del -f` to force deletion.
```bash
# Restrict share access to specific AD groups
cifs share modify <share_name> add-writable-users <DOMAIN>\<group>

# View share permissions
cifs share show <share_name>
```

```text title="Expected output"
Share modified successfully.
Share: backup_data
  Protocol: CIFS
  Path: /data/backup_data
  Writable Users: CORP\backup_admins, CORP\storage_team
  Read-Only Users: CORP\auditors
  Browseable: yes
  Comment: Production backup share
```

!!! warning "Common errors"
    **`Error: Share 'backup_data' not found`** — Verify the share name exists with `cifs share list` and use the exact name from the output.
    **`Error: User or group 'DOMAIN\group' not found in directory service`** — Confirm the AD group name and domain are correct, and that the Data Domain appliance has active directory connectivity via `net ads info`.
```bash
# Filesystem state (enabled/disabled)
filesys status

# Full status overview
filesys show

# Compression and deduplication statistics
filesys show compression

# Space usage breakdown (pre-comp, post-comp, physical)
filesys show space
```

```text title="Expected output"
Filesystem Status:
  State: enabled
  Filesystem: /data
  Mount Point: /data
  Total Capacity: 50.0 TB
  Used Capacity: 34.2 TB
  Available Capacity: 15.8 TB

Filesystem Information:
  Name: /data
  State: enabled
  Block Size: 4096 bytes
  Inode Count: 268435456
  Used Inodes: 142857291
  Free Inodes: 125578165
  Last Check: 2024-01-15 09:23:47 UTC

Compression Statistics:
  Compression Enabled: yes
  Compression Ratio: 3.2:1
  Pre-Compression Size: 108.6 TB
  Post-Compression Size: 34.2 TB
  Compression Savings: 74.4 TB (68.5%)
  Deduplication Ratio: 2.1:1
  Deduplication Savings: 28.9 TB

Space Usage Breakdown:
  Pre-Compression Logical: 108.6 TB
  Post-Compression Logical: 34.2 TB
  Physical Used: 16.3 TB
  Physical Available: 33.7 TB
  Overhead: 1.2 TB (3.6%)
  Snapshots: 2.8 TB
```

!!! warning "Common errors"
    **`filesys: command not found`** — Verify you are logged into the Data Domain CLI (SSH to the management IP) and not a standard Linux shell.
    **`Permission denied`** — Ensure your user account has administrative privileges; use `user show` to verify your role is "admin".
    **`Filesystem is disabled`** — Enable the filesystem with `filesys enable` before querying compression and space statistics.
```bash
# Enable the filesystem (required before accepting backup data)
filesys enable

# Disable the filesystem (maintenance only — stops all I/O)
filesys disable
```

```text title="Expected output"
filesys enable
Filesystem enabled successfully.
Status: ONLINE
Capacity: 45.2 TB
Available: 12.8 TB

filesys disable
WARNING: Disabling filesystem will terminate all active connections.
Filesystem disabled successfully.
Status: OFFLINE
```

!!! warning "Common errors"
    **`filesys: command not found`** — Ensure you are logged into the Data Domain CLI (via SSH or console) and have administrative privileges; this command is not available in standard bash shells.
    **`Error: Filesystem is already enabled`** — Check current filesystem status with `filesys status` before attempting to enable; skip the enable command if status shows ONLINE.
    **`Error: Active backup jobs detected. Cannot disable filesystem.`** — Wait for all running backup jobs to complete or force-abort them with `job abort -all` before disabling the filesystem.
```bash
# Start a cleaning cycle
filesys clean start

# Show cleaning status
filesys clean status

# Stop an in-progress clean
filesys clean stop
```

```text title="Expected output"
Starting cleaning cycle on /data1...
Cleaning cycle initiated. Cycle ID: CLEAN-20240115-0847
Estimated duration: 2 hours 15 minutes

Cleaning Status Report
======================
Cycle ID: CLEAN-20240115-0847
Status: IN_PROGRESS
Progress: 42%
Filesystems being cleaned: /data1, /data2
Estimated time remaining: 1 hour 18 minutes
Last updated: 2024-01-15 08:52:33 UTC

Stopping cleaning cycle CLEAN-20240115-0847...
Cleaning cycle stopped successfully.
Final statistics: 847 GB reclaimed, 12,453 files processed
```

!!! warning "Common errors"
    **`filesys clean start: Error - cleaning cycle already in progress (Cycle ID: CLEAN-20240115-0847)`** — Wait for the current cycle to complete or run `filesys clean stop` first.
    **`filesys clean status: Error - no active cleaning cycle found`** — Start a cleaning cycle with `filesys clean start` before checking status.
    **`filesys clean stop: Error - insufficient privileges to stop cleaning cycle`** — Run the command with appropriate administrative credentials or use `sudo`.
```bash
# Overall capacity summary
filesys show space

# Compression ratio and savings
filesys show compression summary

# Per-MTree compression
filesys show compression | grep -A5 "mtree"

# Logical vs physical usage
filesys show space | grep -E "Used|Available|Total"
```

```text title="Expected output"
Filesystem                Total         Used      Available   Use%
/data                     50.0TB        38.5TB    11.5TB      77%
/var                      2.0TB         1.2TB     0.8TB       60%
/nfs                      100.0TB       87.3TB    12.7TB       87%

Compression Summary
Overall Compression Ratio: 3.2:1
Total Logical Data: 278.4TB
Total Physical Data: 86.9TB
Compression Savings: 191.5TB (68.7%)

mtree: /data/mtree_prod_01
  Compression Ratio: 3.5:1
  Logical: 95.2TB
  Physical: 27.2TB
mtree: /data/mtree_prod_02
  Compression Ratio: 3.1:1
  Logical: 102.8TB
  Physical: 33.2TB

Used: 38.5TB
Available: 11.5TB
Total: 50.0TB
```

!!! warning "Common errors"
    **`filesys: command not found`** — Verify you are logged into the Data Domain CLI (SSH to the management IP) and not a standard Linux shell.
    **`permission denied`** — Ensure your user account has admin or operator privileges; request elevated access from your Data Domain administrator.
```bash
# Expire old backup data (via backup application policy — not DD CLI)
# Data Domain only deletes data when the backup app marks it expired

# After deletions, run cleaning to reclaim space
filesys clean start

# Monitor reclaim progress
filesys clean status
filesys show space   # compare before/after
```

```text title="Expected output"
Data Domain OS v7.15.1.20 (dd-backup-01)
Cleaning started at 2024-01-15 14:32:18 UTC
Cleaning job ID: clean-20240115-143218

filesys clean status
Status: In Progress
Start time: 2024-01-15 14:32:18
Elapsed time: 2m 34s
Estimated completion: 12m 45s
Blocks processed: 1,247,856 / 3,892,104 (32%)
Space reclaimed so far: 847.3 GB

filesys show space
Filesystem: /data
Total capacity: 50.0 TB
Used space: 32.4 TB
Available space: 17.6 TB
Compression ratio: 2.8:1
Deduplication savings: 18.2 TB
Last cleaning: 2024-01-15 14:32:18
```

!!! warning "Common errors"
    **`filesys clean start: Operation already in progress`** — Wait for the current cleaning job to complete using `filesys clean status` before starting a new one.
    **`filesys show space: Permission denied`** — Ensure your user account has administrative privileges or use `sudo` if available on your Data Domain system.
```bash
# Check filesystem integrity
filesys check

# View filesystem event log
filesys show log
```

```text title="Expected output"
Filesystem check started at 2024-01-15 14:32:18 UTC
Checking filesystem: /data/col1
  Inodes: 2847291 total, 156432 free
  Blocks: 18456789 total, 3214567 free
  Checking directory structure... OK
  Checking block allocation... OK
  Checking inode allocation... OK
Filesystem check completed successfully in 287 seconds
No errors found.

Filesystem Event Log (last 20 entries):
2024-01-15 14:32:18 INFO  Filesystem check initiated by admin
2024-01-15 14:15:42 INFO  Garbage collection completed: 234 GB freed
2024-01-15 13:48:09 WARN  Replication lag detected on node-02: 45 seconds
2024-01-15 13:22:31 INFO  Backup snapshot created: snap_20240115_132231
2024-01-15 12:56:17 INFO  Capacity threshold warning: 78% utilized
2024-01-15 11:30:05 INFO  Filesystem expansion completed: +500 GB
```

!!! warning "Common errors"
    **`filesys: command not found`** — Verify you are logged into the Data Domain management interface or use the correct CLI command syntax for your DD OS version.
    **`Error: Filesystem check already in progress`** — Wait for the current check to complete or use `filesys check abort` if necessary before retrying.
```bash
# List all MTrees
mtree list

# Detail for a specific MTree
mtree show /data/col1/<mtree_name>

# All MTrees with usage stats
mtree list --verbose
```

```text title="Expected output"
Name                          Status    Capacity      Used          Available
/data/col1/backup_prod        normal    10.0 TB       7.2 TB        2.8 TB
/data/col1/archive_2024       normal    5.0 TB        3.1 TB        1.9 TB
/data/col1/dr_replica         normal    8.0 TB        4.5 TB        3.5 TB
/data/col1/compliance_hold    normal    2.0 TB        1.8 TB        0.2 TB

MTree Name:           /data/col1/backup_prod
Status:               normal
Capacity:             10.0 TB
Used:                 7.2 TB
Available:            2.8 TB
Compression Ratio:    1.34:1
Deduplication Ratio:  2.18:1
Last Modified:        2024-01-15 14:32:18 UTC
Replication Status:   in-sync

Name                          Status    Capacity      Used          Available    Compression  Dedup
/data/col1/backup_prod        normal    10.0 TB       7.2 TB        2.8 TB       1.34:1       2.18:1
/data/col1/archive_2024       normal    5.0 TB        3.1 TB        1.9 TB       1.12:1       1.89:1
/data/col1/dr_replica         normal    8.0 TB        4.5 TB        3.5 TB       1.28:1       2.05:1
/data/col1/compliance_hold    normal    2.0 TB        1.8 TB        0.2 TB       1.01:1       1.15:1
```

!!! warning "Common errors"
    **`mtree: command not found`** — Ensure you are logged into the Data Domain management interface (SSH to the DD appliance) or use the Web UI instead of your local shell.
    **`Error: MTree /data/col1/<mtree_name> does not exist`** — Verify the exact MTree path using `mtree list` first, as the name may differ from your expected value.
    **`Permission denied`** — Confirm your user account has administrative privileges on the Data Domain system; contact your DD administrator if needed.
```bash
# Create an MTree
mtree create /data/col1/<mtree_name>

# Delete an MTree (must be empty or use force)
mtree delete /data/col1/<mtree_name>
```

```text title="Expected output"
mtree create /data/col1/backup_prod
MTree /data/col1/backup_prod created successfully
Capacity: 100.0 TB
Replication factor: 2
Status: Active

mtree delete /data/col1/backup_prod
MTree /data/col1/backup_prod deleted successfully
Reclaimed space: 100.0 TB
```

!!! warning "Common errors"
    **`Error: MTree /data/col1/backup_prod is not empty`** — Add the `--force` flag to delete a non-empty MTree, or manually purge contents first with `mtree purge`.
    **`Error: Permission denied for operation on /data/col1/backup_prod`** — Ensure your user account has sysadmin or mtree-admin privileges on the Data Domain system.
```bash
# View current quotas
mtree quota show

# Set hard limit (backup fails when limit is reached)
mtree quota set hard-limit 10 TiB /data/col1/<mtree_name>

# Set soft limit (alert raised when exceeded)
mtree quota set soft-limit 8 TiB /data/col1/<mtree_name>

# Remove a quota
mtree quota reset /data/col1/<mtree_name>
```

```text title="Expected output"
mtree quota show
Quota Summary for /data/col1/
=====================================
Mtree Name          Hard Limit    Soft Limit    Used Space    Status
prod-backup-01      10 TiB        8 TiB         7.2 TiB       OK
dev-backup-02       5 TiB         4 TiB         4.8 TiB       WARNING
archive-mtree       20 TiB        16 TiB        18.5 TiB      OK
test-col-03         2 TiB         1.5 TiB       2.1 TiB       EXCEEDED

mtree quota set hard-limit 10 TiB /data/col1/prod-backup-01
Hard limit set successfully for /data/col1/prod-backup-01

mtree quota set soft-limit 8 TiB /data/col1/prod-backup-01
Soft limit set successfully for /data/col1/prod-backup-01

mtree quota reset /data/col1/prod-backup-01
Quota reset successfully for /data/col1/prod-backup-01
```

!!! warning "Common errors"
    **`mtree: command not found`** — Ensure you are logged into the Data Domain management interface or CLI with appropriate credentials.
    **`Error: Invalid path /data/col1/<mtree_name>`** — Replace `<mtree_name>` with the actual mtree name (e.g., `prod-backup-01`) and verify the path exists with `mtree show`.
    **`Error: Quota limit must be greater than soft limit`** — Set the hard limit to a value larger than the soft limit (e.g., hard-limit 10 TiB, soft-limit 8 TiB).
```bash
# Enable retention lock on an MTree
mtree retention-lock enable mode enterprise /data/col1/<mtree_name>

# Set minimum/maximum retention period
mtree retention-lock set min-retention-period 30days /data/col1/<mtree_name>
mtree retention-lock set max-retention-period 7years /data/col1/<mtree_name>

# View retention lock settings
mtree retention-lock status /data/col1/<mtree_name>
```

```text title="Expected output"
Retention lock enabled on MTree: col1/backup_prod_001
Mode: enterprise
Status: ACTIVE

Minimum retention period set to: 30 days
Maximum retention period set to: 7 years

MTree Retention Lock Status
===========================
MTree Name: col1/backup_prod_001
Retention Lock: ENABLED
Mode: enterprise
Min Retention Period: 30 days
Max Retention Period: 7 years
Current Lock State: ACTIVE
Last Modified: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`Error: MTree /data/col1/<mtree_name> does not exist or is not accessible`** — Verify the MTree name is correct and the path exists using `mtree list`.
    **`Error: Retention lock mode 'enterprise' is not supported on this system`** — Check Data Domain firmware version supports enterprise mode; use `mtree retention-lock enable mode compliance` as an alternative.
    **`Error: Cannot enable retention lock - MTree is currently in use by active backup jobs`** — Wait for running backup jobs to complete or pause them before enabling retention lock.
```bash
# Add an MTree as a replication source (see replication CLI ref for full setup)
replication add source mtree://<src_host>/data/col1/<mtree_name> destination mtree://<dst_host>/data/col1/<mtree_name>

# View replication contexts for this MTree
replication show all | grep <mtree_name>
```

```text title="Expected output"
Replication source added successfully.
Source: mtree://dd-prod-01.corp.local/data/col1/finance_backup
Destination: mtree://dd-dr-02.corp.local/data/col1/finance_backup
Replication ID: rep-4f8c2a91-7d3e-4a2b-9c1f-e8b5d2c6a3f9
Status: Initialized

finance_backup          mtree://dd-prod-01.corp.local/data/col1/finance_backup    mtree://dd-dr-02.corp.local/data/col1/finance_backup    Active    Last sync: 2024-01-15 14:32:18 UTC    Next sync: 2024-01-15 15:32:18 UTC
```

!!! warning "Common errors"
    **`Error: Invalid MTree path format`** — Ensure the path follows the exact format `mtree://<hostname>/data/col1/<mtree_name>` with no trailing slashes or extra characters.
    **`Error: Destination MTree does not exist`** — Create the destination MTree on the target Data Domain system before adding the replication relationship.
    **`Error: Authentication failed for destination host`** — Verify network connectivity and credentials between source and destination Data Domain systems are properly configured.
```bash
# Space used by each MTree
mtree list --verbose | grep -E "name|pre-comp|post-comp|quota"

# Compare pre-compression vs post-compression (dedup savings)
filesys show compression | grep -A5 "mtree"
```

```text title="Expected output"
Name                          Pre-Comp(GB)  Post-Comp(GB)  Quota(GB)
mtree_prod_db                 2847.3        856.2          5000
mtree_backup_tier1            5124.6        1243.8         8000
mtree_archive_2024            1956.4        487.1          3000
mtree_dev_test                 412.8        198.5          1000
mtree_replication_staging      678.2        201.4          2000

Compression Ratio Summary:
mtree_prod_db:              70.1% reduction
mtree_backup_tier1:         75.8% reduction
mtree_archive_2024:         75.1% reduction
mtree_dev_test:             51.9% reduction
mtree_replication_staging:   70.3% reduction
```

!!! warning "Common errors"
    **`mtree: command not found`** — Ensure you are logged into the Data Domain management interface or have the DD CLI tools installed in your PATH.
    **`grep: (standard input) is empty`** — Run `mtree list` without filters first to verify mtrees exist and the command syntax is correct for your DD OS version.
```bash
# All interfaces — IP, speed, state
net show all

# Interface configuration (IP, netmask, MTU, bonding)
net show config

# Network settings summary
net show settings

# Interface statistics (rx/tx, errors, drops)
net show stats
```

```text title="Expected output"
=== All Interfaces ===
Interface    IP Address       Netmask          Speed    State
eth0         192.168.1.45     255.255.255.0    1000M    UP
eth1         192.168.2.50     255.255.255.0    1000M    UP
eth2         10.0.0.100       255.255.255.0    10000M   UP
bond0        172.16.10.20     255.255.255.0    2000M    UP
eth3         -                -                1000M    DOWN

=== Interface Configuration ===
Interface: eth0
  IP: 192.168.1.45
  Netmask: 255.255.255.0
  MTU: 1500
  Bonding: None

Interface: bond0
  IP: 172.16.10.20
  Netmask: 255.255.255.0
  MTU: 9000
  Bonding: Active (eth1, eth2)

=== Network Settings Summary ===
Hostname: dd-backup-01.corp.local
Domain: corp.local
DNS Servers: 8.8.8.8, 8.8.4.4
Gateway: 192.168.1.1
NTP Servers: ntp.corp.local

=== Interface Statistics ===
Interface  RX Packets    TX Packets    RX Errors  TX Errors  RX Drops  TX Drops
eth0       4521847       3892156       0          0          12        0
eth1       12847392      11923847      2          0          45        8
eth2       11923847      12847392      0          1          38        0
bond0      24771239      24771239      2          1          83        8
eth3       0             0             0          0          0         0
```

!!! warning "Common errors"
    **`net: command not found`** — Verify you are logged into the Data Domain management interface (SSH to the DD system, not a separate host) and that your user role has network view permissions.
    **`Error: Unable to retrieve network configuration`** — Restart the network management service with `service network restart` or check system connectivity with `ping 127.0.0.1`.
    **`Permission denied`** — Ensure your user account has admin or network-operator privileges; request elevated access from your Data Domain administrator.
```bash
# Configure an interface IP
net config eth1 <ip_address> netmask <mask>

# Bring an interface up or down
net enable eth1
net disable eth1
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Interface eth1 not found`** — Verify the interface exists with `net show interfaces` and use the correct interface name.
    **`Error: Invalid netmask format`** — Use standard dotted-decimal notation (e.g., 255.255.255.0) or CIDR prefix length (e.g., /24).
```bash
# Current routing table
net route show

# Add a host route
net route add host <destination_ip> gateway <gateway_ip> dev <interface>

# Add a network route
net route add net <network_ip> netmask <mask> gateway <gateway_ip>

# Delete a route
net route del host <destination_ip>
```

```text title="Expected output"
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.20.1.1       0.0.0.0         UG    100    0      0   eth0
10.20.1.0       0.0.0.0         255.255.255.0   U     0      0      0   eth0
192.168.100.5   10.20.1.254     255.255.255.255 UGH   0      0      0   eth1
172.16.0.0      10.20.1.254     255.255.255.0   UG    0      0      0   eth1
10.0.0.0        10.20.1.100     255.0.0.0       UG    50     0      0   eth2
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Invalid gateway address <gateway_ip>`** — Verify the gateway IP is reachable and correctly formatted (e.g., 10.20.1.1 not 10.20.1.256).
    **`Error: Interface <interface> does not exist`** — Confirm the interface name with `net interface show` and use the correct name (e.g., eth0 not eth-0).
    **`Error: Route does not exist`** — Ensure the exact destination IP and host/net type match an existing route before deletion.
```bash
# Hosts file entries
net hosts show

# Add a static host entry
net config hosts add <ip_address> <hostname>

# DNS server configuration
net show settings | grep -i dns
```

```text title="Expected output"
# Hosts file entries
192.168.1.10    ddmd-primary.corp.local    ddmd-primary
192.168.1.11    ddmd-secondary.corp.local   ddmd-secondary
127.0.0.1       localhost
::1              localhost

# Add a static host entry
Host entry added successfully: 192.168.1.50 backup-node01.corp.local

# DNS server configuration
dns-servers: 8.8.8.8 8.8.4.4
dns-search-domains: corp.local internal.local
dns-timeout: 5
dns-retries: 2
```

!!! warning "Common errors"
    **`net: command not found`** — Verify you are logged into the Data Domain management interface (SSH to the system's IP address) rather than a local workstation shell.
    **`Host entry added successfully: ERROR - Invalid IP address format`** — Ensure the IP address is in valid dotted-decimal notation (e.g., 192.168.1.50) and the hostname contains only alphanumeric characters and hyphens.
    **`ERROR: Duplicate host entry already exists`** — Remove the existing entry with `net config hosts remove <ip_address>` before adding the new one.
```bash
# NTP server list
ntp show

# NTP sync status
ntp status

# Add NTP server
ntp add timeserver <ntp_ip>

# Remove NTP server
ntp del timeserver <ntp_ip>
```

```text title="Expected output"
NTP Servers:
  Server Address: 10.45.12.8
  Server Address: 10.45.12.9
  Server Address: 203.0.113.45

NTP Status:
  System Clock Status: synchronized
  Leap Indicator: 0
  Stratum: 2
  Precision: -24
  Root Delay: 0.015625 sec
  Root Dispersion: 0.019531 sec
  Peer Dispersion: 0.001953 sec
  Reference ID: 10.45.12.8
  Reference Time: Wed Jan 15 14:32:18 2025

NTP server 10.50.20.15 added successfully.
NTP server 10.45.12.9 removed successfully.
```

!!! warning "Common errors"
    **`Error: NTP server 10.50.20.15 is already configured`** — Remove the duplicate entry with `ntp del timeserver 10.50.20.15` before re-adding it.
    **`Error: Cannot remove NTP server, minimum 1 server required`** — Ensure at least one NTP server remains configured; add a replacement server before deleting the last one.
    **`Error: Invalid NTP server address <ntp_ip>`** — Verify the IP address format is valid and the server is reachable on port 123 UDP.
```bash
# Ping from Data Domain
net ping <destination_ip>
net ping <destination_ip> count 10

# Traceroute
net traceroute <destination_ip>
```

```text title="Expected output"
PING 192.168.1.50 (192.168.1.50): 56 data bytes
64 bytes from 192.168.1.50: icmp_seq=0. time=2.341 ms
64 bytes from 192.168.1.50: icmp_seq=1. time=2.156 ms
64 bytes from 192.168.1.50: icmp_seq=2. time=2.289 ms

---- 192.168.1.50 PING Statistics----
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.156/2.262/2.341 ms

PING 10.20.30.40 (10.20.30.40): 56 data bytes
64 bytes from 10.20.30.40: icmp_seq=0. time=1.823 ms
64 bytes from 10.20.30.40: icmp_seq=1. time=1.945 ms
64 bytes from 10.20.30.40: icmp_seq=2. time=2.067 ms
64 bytes from 10.20.30.40: icmp_seq=4. time=2.134 ms
64 bytes from 10.20.30.40: icmp_seq=5. time=1.998 ms
64 bytes from 10.20.30.40: icmp_seq=6. time=2.211 ms
64 bytes from 10.20.30.40: icmp_seq=7. time=2.089 ms
64 bytes from 10.20.30.40: icmp_seq=8. time=1.876 ms
64 bytes from 10.20.30.40: icmp_seq=9. time=2.043 ms

---- 10.20.30.40 PING Statistics----
10 packets transmitted, 10 packets received, 0% packet loss
round-trip min/avg/max = 1.823/2.019/2.211 ms

traceroute to 10.20.30.40 (10.20.30.40), 30 hops max, 40 byte packets
 1  10.0.0.1 (10.0.0.1)  1.234 ms  1.156 ms  1.289 ms
 2  10.1.0.5 (10.1.0.5)  5.432 ms  5.601 ms  5.378 ms
 3  10.2.1.1 (10.2.1.1)  8.945 ms  9.123 ms  8.876 ms
 4  10.20.30.40 (10.20.30.40)  12.567 ms  12.634 ms  12.501 ms
```

!!! warning "Common errors"
    **`net ping: unknown host <destination_ip>`** — Verify the destination IP address is correct and resolvable from the Data Domain's network configuration.
    **`net ping: sendto: No route to host`** — Confirm the destination IP is on an accessible subnet and check Data Domain network interface configuration with `net show interface`.
```bash
# Show bonding configuration
net config bond show

# Create a bond
net config bond create bond0 <eth1> <eth2> lacp
```

```text title="Expected output"
=== Bond Configuration ===
Bond: bond0
  Status: active
  Mode: lacp
  Members: eth1, eth2
  MAC Address: 00:14:4c:12:ab:cd
  MTU: 1500
  Active Slave: eth1
  Slaves:
    eth1: up
    eth2: up

Bond created successfully: bond0
  Mode: lacp
  Interfaces: eth1, eth2
  Status: active
```

!!! warning "Common errors"
    **`Error: Interface eth1 is already in use`** — Remove the interface from its current bond or configuration before adding it to a new bond.
    **`Error: LACP mode requires at least 2 interfaces`** — Provide at least two valid physical interfaces separated by spaces in the bond create command.
```bash
# Show open ports and firewall rules
net config firewall show
```

```text title="Expected output"
Firewall Configuration
======================

Inbound Rules (Active):
  Rule ID    Source          Destination    Port    Protocol  Action
  ---------------------------------------------------------------------------
  FW-001     0.0.0.0/0       0.0.0.0/0      22      TCP       ALLOW
  FW-002     0.0.0.0/0       0.0.0.0/0      111     TCP       ALLOW
  FW-003     0.0.0.0/0       0.0.0.0/0      2049    TCP       ALLOW
  FW-004     10.0.0.0/8      0.0.0.0/0      3009    TCP       ALLOW
  FW-005     192.168.1.0/24  0.0.0.0/0      13115   TCP       ALLOW
  FW-006     0.0.0.0/0       0.0.0.0/0      443     TCP       ALLOW

Outbound Rules (Active):
  All traffic permitted by default

Open Ports:
  22 (SSH), 111 (RPC), 443 (HTTPS), 2049 (NFS), 3009 (Data Domain), 13115 (Replication)
```

!!! warning "Common errors"
    **`net config firewall: command not found`** — Verify you are logged into the Data Domain CLI (use `ssh admin@<dd-ip>`) and not a standard Linux shell.
    **`Permission denied`** — Ensure your user account has administrative privileges; use `su` or contact your system administrator.
```bash
# All replication contexts (summary)
replication show all

# Replication configuration
replication show config

# Per-context statistics (lag, bytes sent, compression)
replication show stats

# Quick status — state of all contexts
replication status
```

```text title="Expected output"
=== Replication Contexts ===
Context Name          State      Remote Host        Last Update
prod-backup-01        ACTIVE     dd-remote-01.lab   2024-01-15 14:32:18
prod-backup-02        ACTIVE     dd-remote-02.lab   2024-01-15 14:31:55
dr-sync-primary       ACTIVE     dd-dr.corp.net     2024-01-15 14:33:02
archive-offsite       IDLE       dd-archive.aws     2024-01-14 08:15:33

=== Replication Configuration ===
Context: prod-backup-01
  Remote Host: dd-remote-01.lab
  Remote User: sysadmin
  Bandwidth Limit: 100 Mbps
  Compression: lz4
  Retention: 30 days

Context: prod-backup-02
  Remote Host: dd-remote-02.lab
  Remote User: sysadmin
  Bandwidth Limit: 100 Mbps
  Compression: lz4
  Retention: 30 days

=== Replication Statistics ===
Context              Lag (min)  Bytes Sent (GB)  Compression Ratio  Status
prod-backup-01       2.3        1847.5           2.1:1              SYNCED
prod-backup-02       5.7        1847.2           2.1:1              SYNCING
dr-sync-primary      0.8        2156.3           1.9:1              SYNCED
archive-offsite      1440+      512.8            2.3:1              IDLE

=== Replication Status ===
prod-backup-01: ACTIVE (lag: 2 min, last sync: 14:32:18)
prod-backup-02: ACTIVE (lag: 5 min, last sync: 14:31:55)
dr-sync-primary: ACTIVE (lag: 0 min, last sync: 14:33:02)
archive-offsite: IDLE (lag: 24+ hours, last sync: 2024-01-14 08:15:33)
```

!!! warning "Common errors"
    **`replication show: command not found`** — Verify you are logged into the Data Domain CLI (use `ssh admin@<dd-hostname>`) and not a standard Linux shell.
    **`Error: Access denied for replication commands`** — Confirm your user account has replication administrator privileges; contact your Data Domain admin to grant the required role.
    **`Context 'prod-backup-01' not found`** — Check the exact context name with `replication show all` and verify it has not been deleted or renamed.
```bash
# Add MTree-level replication (directional — source to destination)
replication add source mtree://<src_host>/data/col1/<mtree_name> \
    destination mtree://<dst_host>/data/col1/<mtree_name>

# Initialize replication (first sync — can take hours for large datasets)
replication initialize <context_id>
```

```text title="Expected output"
Adding replication context...
Context ID: ctx-20250314-a7f2-4d9e-b1c2-9e8f3a2b1d4c
Source: mtree://ddve-prod-01.corp.local/data/col1/backup_archive
Destination: mtree://ddve-dr-02.corp.local/data/col1/backup_archive
Replication direction: unidirectional (source → destination)
Status: configured
Bandwidth limit: unlimited
Compression: enabled

Initializing replication context ctx-20250314-a7f2-4d9e-b1c2-9e8f3a2b1d4c...
Initial sync started at 2025-03-14T09:47:22Z
Estimated completion: 2025-03-14T18:32:15Z (8h 44m remaining)
Data to replicate: 2.3 TB
Current throughput: 72.4 MB/s
```

!!! warning "Common errors"
    **`Error: destination mtree does not exist`** — Create the destination MTree on the target Data Domain system before adding the replication context.
    **`Error: replication context already exists for this pair`** — Use `replication modify` to update an existing context instead of `replication add`.
    **`Error: network connectivity failed to destination host`** — Verify network connectivity and firewall rules between source and destination Data Domain systems on port 7144.
```bash
# Trigger an immediate sync (outside scheduled window)
replication sync <context_id>

# Pause replication (source continues; changes accumulated)
replication disable <context_id>

# Resume replication
replication enable <context_id>

# Break a context (irreversible — removes replication relationship)
replication break <context_id>
```

```text title="Expected output"
# Trigger an immediate sync (outside scheduled window)
replication sync 7f3a9c2e-4b1d-11ed-a891-0050568a1234
Sync initiated for context 7f3a9c2e-4b1d-11ed-a891-0050568a1234
Status: In Progress
Bytes transferred: 0 / 2.3 TB
Elapsed time: 0 seconds

# Pause replication (source continues; changes accumulated)
replication disable 7f3a9c2e-4b1d-11ed-a891-0050568a1234
Replication disabled for context 7f3a9c2e-4b1d-11ed-a891-0050568a1234
Accumulated changes will be queued for next sync

# Resume replication
replication enable 7f3a9c2e-4b1d-11ed-a891-0050568a1234
Replication enabled for context 7f3a9c2e-4b1d-11ed-a891-0050568a1234
Next scheduled sync: 2024-01-15 02:00:00 UTC
Pending changes to replicate: 847 GB

# Break a context (irreversible — removes replication relationship)
replication break 7f3a9c2e-4b1d-11ed-a891-0050568a1234
WARNING: This action is irreversible. Replication relationship will be destroyed.
Context 7f3a9c2e-4b1d-11ed-a891-0050568a1234 has been broken.
Replication relationship removed.
```

!!! warning "Common errors"
    **`Error: Context 7f3a9c2e-4b1d-11ed-a891-0050568a1234 not found`** — Verify the context ID is correct using `replication list` and check for typos.
    **`Error: Replication sync already in progress for this context`** — Wait for the current sync to complete or use `replication abort` before triggering a new sync.
    **`Error: Cannot break context while sync is in progress`** — Wait for the active replication sync to finish before attempting to break the context.
```bash
# Lag in bytes (amount of data not yet replicated)
replication show stats | grep lag

# Lag in time
replication status | grep -E "context|lag"
```

```text title="Expected output"
lag: 0 bytes
context: replication_context_1
lag: 2 hours 14 minutes
```

!!! warning "Common errors"
    **`replication: command not found`** — Ensure you are logged into the Data Domain CLI (SSH to the management IP) and have appropriate admin privileges.
    **`grep: (standard input) is empty`** — Run `replication show` first to verify replication is configured; if no output appears, replication may not be initialized on this system.
```bash
# Break the context (makes destination writeable)
replication failover <context_id>
```

```text title="Expected output"
Failover initiated for context: ctx-prod-backup-001
Source: dd-primary.corp.local (192.168.1.45)
Destination: dd-secondary.corp.local (192.168.1.46)
Status: IN_PROGRESS
Replication paused
Context lock released
Destination now accepting writes
Failover completed successfully in 47 seconds
New primary: dd-secondary.corp.local
Replication direction: REVERSED
```

!!! warning "Common errors"
    **`Error: Context ctx-prod-backup-001 not found`** — Verify the context ID with `replication show` and ensure it exists on this system.
    **`Error: Failover blocked - replication still in progress`** — Wait for the current replication cycle to complete or force abort with `replication abort <context_id>` before retrying.
    **`Error: Destination system unreachable (192.168.1.46)`** — Confirm network connectivity to the destination Data Domain and verify it is powered on and responsive.
```bash
# Step 1 — resync (when primary recovers)
replication resync <context_id>

# Step 2 — confirm sync complete
replication status
replication show stats | grep lag

# Step 3 — failback: swap source/destination roles
# (requires breaking and recreating context in reverse)
```

```text title="Expected output"
# Step 1 — resync (when primary recovers)
Resync initiated for context 'prod-dd-01-to-dd-02' (ID: ctx-8f2a9c1e)
Resync status: IN_PROGRESS
Estimated time remaining: 2h 34m

# Step 2 — confirm sync complete
Context ID: ctx-8f2a9c1e
Source: dd-prod-01.corp.local (192.168.10.45)
Destination: dd-prod-02.corp.local (192.168.10.46)
Status: SYNCED
Last sync: 2024-01-15 14:22:18 UTC
Replication lag: 0 seconds
Throughput: 847 MB/s
```

!!! warning "Common errors"
    **`Error: Context 'ctx-8f2a9c1e' not found or is in BROKEN state`** — Verify the context exists and is active with `replication show contexts`; recreate if necessary.
    **`Error: Resync failed — destination has uncommitted writes`** — Ensure no active replication jobs are running on the destination with `replication show jobs` before retrying resync.
    **`Error: Cannot resync — replication lag exceeds 24 hours`** — Break the context and perform a full re-initialization instead of resync using `replication break` followed by `replication create`.
```bash
# Trust a remote DD (exchange certs — required for encrypted replication)
replication add source ... --encryption aes128
admintool certify <remote_dd_hostname>
```

```text title="Expected output"
Adding replication source configuration...
Source replication context created: src-dd-prod-01
Encryption: AES-128
Remote host: dd-backup-02.corp.local
Waiting for certificate exchange...
Certificate request sent to dd-backup-02.corp.local
Remote certificate received and verified
Fingerprint: 47:8B:2F:D1:9A:E4:C6:5B:3D:92:F7:41:E8:6C:B3:A9
Certificate installed successfully
Replication trust established
```

!!! warning "Common errors"
    **`Error: Certificate exchange timeout after 60 seconds`** — Verify network connectivity between the two Data Domain systems and check firewall rules allowing port 3009 (replication service).
    **`Error: Remote host dd-backup-02.corp.local not found or unreachable`** — Ensure the remote Data Domain hostname is resolvable via DNS and the system is powered on and network-accessible.
    **`Error: Certificate verification failed - fingerprint mismatch`** — Confirm you are connecting to the correct remote Data Domain system and that no man-in-the-middle interference is occurring.
```bash
# Full system overview
system show all

# Software version
system show version

# Hardware inventory (disks, enclosures, NIC, HBA)
system show hardware

# Current system statistics (CPU, memory, throughput)
system show stats

# Uptime
system show uptime

# Serial number and model
system show summary
```

```text title="Expected output"
System Model: Dell EMC Data Domain DD9900
System ID: 4a7c9e2b-f1d3-4e8a-b2c1-9d5f3a8e2c1b
System Name: dd-prod-01.corp.local
System Status: HEALTHY

Data Domain OS Version: 7.15.1.20
Build: 7.15.1.20-623847
Release Date: 2024-01-15

Hardware Inventory:
  Enclosures: 1
  Disk Drives: 48 (SAS 3.5" 10TB)
  NICs: 4 (1GbE)
  HBAs: 2 (SAS)
  Memory: 512 GB
  CPU: 2x Intel Xeon E5-2680 v4

System Statistics:
  CPU Usage: 34%
  Memory Usage: 67%
  Throughput (Current): 1.2 GB/s
  Throughput (Average): 856 MB/s

System Uptime: 287 days, 14 hours, 23 minutes

Serial Number: DD9900-SN-A7F2K9X1
Model: Dell EMC Data Domain DD9900
```

!!! warning "Common errors"
    **`Error: Access Denied`** — Verify your user account has admin privileges or use `sudo` if available on your Data Domain system.
    **`Error: Command not found: system show all`** — Ensure you are connected to the Data Domain CLI (via SSH or console) and not a standard Linux shell; use `ssh admin@<dd-ip>` to connect.
    **`Error: System is in maintenance mode`** — Wait for maintenance operations to complete or contact your system administrator before running diagnostic commands.
```bash
# Run built-in health check
health check show

# Active alerts (open, unacknowledged)
alert show current

# Alert history (all alerts, resolved and unresolved)
alert show history

# Brief alert history (most recent)
alert show history brief

# Clear a resolved alert
alert acknowledge --id <alert_id>
```

```text title="Expected output"
Health Check Status:
  System Status: HEALTHY
  CPU Usage: 42%
  Memory Usage: 58%
  Disk Usage: 73%
  Network Status: UP
  Replication Status: IN_SYNC
  Last Check: 2024-01-15 14:32:18 UTC

Current Alerts:
  ID: ALR-2847-001 | Severity: WARNING | Component: DISK_SPACE | Message: Capacity approaching threshold on tier-2
  ID: ALR-2847-002 | Severity: INFO | Component: REPLICATION | Message: Replication lag detected (45 seconds)

Alert History:
  ID: ALR-2847-001 | Severity: WARNING | Status: OPEN | Timestamp: 2024-01-15 14:15:22 UTC
  ID: ALR-2847-002 | Severity: INFO | Status: OPEN | Timestamp: 2024-01-15 13:58:47 UTC
  ID: ALR-2846-998 | Severity: CRITICAL | Status: RESOLVED | Timestamp: 2024-01-14 22:41:05 UTC
  ID: ALR-2846-997 | Severity: WARNING | Status: RESOLVED | Timestamp: 2024-01-14 19:33:12 UTC
  ...

Recent Alerts (Brief):
  ALR-2847-002 | INFO | REPLICATION | 2024-01-15 13:58:47 UTC
  ALR-2847-001 | WARNING | DISK_SPACE | 2024-01-15 14:15:22 UTC

Alert ALR-2846-998 acknowledged successfully.
```

!!! warning "Common errors"
    **`alert acknowledge: invalid alert ID format`** — Verify the alert ID exists and matches the format shown in `alert show history` (e.g., ALR-2847-001).
    **`health check show: command not found`** — Confirm you are connected to the Data Domain CLI (not the host shell); use `ssh admin@<dd-ip>` to access the correct interface.
    **`alert show current: insufficient permissions`** — Request admin or operator role privileges from your Data Domain administrator.
```bash
# Show installed software packages
system software version show

# License status
elicense show
```

```text title="Expected output"
Dell EMC Data Domain OS 7.15.1.20
Build: 7.15.1.20-694847
System Serial Number: DD9300-123456789
Installed Packages:
  - Data Domain OS Core: 7.15.1.20
  - DDOS Kernel: 7.15.1.20-k4
  - Management Services: 7.15.1.20
  - Replication Engine: 7.15.1.20
  - Cloud Tier Module: 7.15.1.20

License Status:
  License Key ID: ABC123DEF456GHI789
  Product: Data Domain 9300
  Capacity: 500 TB
  Status: VALID
  Expiration Date: 2026-03-15
  Features Enabled: Replication, Cloud Tier, Advanced Dedup
```

!!! warning "Common errors"
    **`system software version show: command not found`** — Ensure you are logged into the Data Domain CLI (via SSH or console) and not a standard Linux shell.
    **`elicense show: Permission denied`** — Verify your user account has administrative privileges; use `user show` to check your role.
```bash
# Power supply status
enclosure show hardware | grep -i power

# Fan status
enclosure show hardware | grep -i fan

# Temperature sensors
enclosure show hardware | grep -i temp
```

```text title="Expected output"
Power Supply Status:
  Power Supply 1 (PSU-1):        OK
  Power Supply 2 (PSU-2):        OK
  Power Supply Redundancy:       Enabled

Fan Status:
  Fan Module 1:                  OK (8500 RPM)
  Fan Module 2:                  OK (8200 RPM)
  Fan Module 3:                  OK (8450 RPM)
  System Fan Speed:              Normal

Temperature Sensors:
  CPU Temperature:               42°C (Normal)
  Ambient Temperature:           28°C (Normal)
  Disk Enclosure Temp:           35°C (Normal)
  PSU-1 Temperature:             38°C (Normal)
  PSU-2 Temperature:             39°C (Normal)
```

!!! warning "Common errors"
    **`enclosure: command not found`** — Verify you are logged into the Data Domain system directly (not a remote host) and have appropriate admin privileges.
    **`grep: (standard input) is empty`** — Run `enclosure show hardware` without grep first to confirm the command syntax and that hardware monitoring is enabled on this system.
```bash
# Current time
ntp status

# NTP servers configured
ntp show

# Add NTP server
ntp add timeserver <ntp_ip>
```

```text title="Expected output"
Current time: 2024-01-15 14:32:47 UTC
NTP Status: synchronized
Stratum: 2
Offset: 0.002ms
Jitter: 0.001ms

NTP Servers Configured:
  216.239.35.0 (time.google.com)
  129.6.15.28 (time.nist.gov)
  91.189.89.198 (ntp.ubuntu.com)

NTP server 203.0.113.42 added successfully.
```

!!! warning "Common errors"
    **`ntp add: error - invalid IP address format`** — Verify the NTP server IP is in valid dotted-decimal notation (e.g., 192.0.2.1) and rerun the command.
    **`ntp add: error - NTP server already configured`** — Check existing NTP servers with `ntp show` and use a different IP address or remove the duplicate first.
    **`ntp: command not found`** — Ensure you are logged in with administrative privileges and the Data Domain system is running the latest firmware version.
```bash
# Safe shutdown (completes in-progress operations)
system shutdown

# Restart the DDOS software (not a full reboot)
system restart

# Full reboot
system reboot
```

```text title="Expected output"
system shutdown
Initiating safe shutdown sequence...
Waiting for in-progress operations to complete...
All active jobs completed successfully.
System will halt in 30 seconds. Press Ctrl+C to cancel.
Shutdown initiated at 2024-01-15 14:32:18 UTC

system restart
Restarting DDOS software...
Stopping DDOS services: [OK]
Clearing cache and temporary files...
Restarting DDOS daemon: [OK]
DDOS software restart completed in 12 seconds.

system reboot
Initiating full system reboot...
Syncing filesystems...
All filesystems synced.
System will reboot in 60 seconds. Press Ctrl+C to cancel.
Rebooting at 2024-01-15 14:33:45 UTC
```

!!! warning "Common errors"
    **`Error: Cannot shutdown while replication is in progress`** — Wait for active replication jobs to complete using `job status` before attempting shutdown.
    **`Error: DDOS restart failed - port 3009 already in use`** — Kill the existing DDOS process with `pkill -f ddos` or wait 30 seconds for the port to release, then retry.
    **`Error: Reboot denied - active user sessions detected`** — Force disconnect users with `system session kill all` or wait for sessions to end naturally before rebooting.
```bash
# Create a support bundle (for TAC cases)
support bundle create

# List available bundles
support bundle show

# Transfer to external server
support bundle export scp://user@host:/path/bundle.tar.gz
```

```text title="Expected output"
Creating support bundle...
Bundle creation started. Bundle ID: bundle-20240115-143022
Gathering system logs... [████████████████████] 100%
Gathering configuration data... [████████████████████] 100%
Gathering performance metrics... [████████████████████] 100%
Bundle created successfully: /var/log/support/bundle-20240115-143022.tar.gz (2.3 GB)

Bundle ID                      Created             Size      Status
bundle-20240115-143022         2024-01-15 14:30    2.3 GB    Ready
bundle-20240114-091545         2024-01-14 09:15    2.1 GB    Ready
bundle-20240113-162203         2024-01-13 16:22    2.4 GB    Ready

Exporting bundle to scp://user@host:/path/bundle.tar.gz...
Connecting to host... Connected
Transferring bundle-20240115-143022.tar.gz... [████████████████████] 100%
Transfer completed successfully. Transferred 2.3 GB in 4m 32s
```

!!! warning "Common errors"
    **`support bundle export: Authentication failed for user@host`** — Verify SSH credentials and ensure the remote user has write permissions to the destination path.
    **`support bundle create: Insufficient disk space. Required: 5 GB, Available: 2.1 GB`** — Delete older bundles with `support bundle delete <bundle-id>` or expand storage before retrying.
    **`support bundle export: Connection timeout connecting to host`** — Confirm network connectivity to the remote host and verify the hostname/IP is reachable from the Data Domain appliance.
```bash
# List all local users
user list

# User detail (role, last login)
user show <username>

# Add a local user
user add <username>

# Change a user's password
user change password <username>

# Delete a user
user del <username>
```

```text title="Expected output"
# List all local users
admin
sysadmin
backup_operator
readonly_user
support_tech

# User detail (role, last login)
User Name: sysadmin
Role: sysadmin
Last Login: 2024-01-15 14:32:18 UTC
Account Status: Active

# Add a local user
User 'newuser' created successfully.

# Change a user's password
Password for user 'newuser' changed successfully.

# Delete a user
User 'newuser' deleted successfully.
```

!!! warning "Common errors"
    **`Error: User 'nonexistent' not found`** — Verify the username exists with `user list` before attempting to show, modify, or delete it.
    **`Error: Cannot delete user 'admin': system user cannot be removed`** — Use a non-system account or contact Dell support if admin account modification is required.
    **`Error: Password does not meet complexity requirements`** — Ensure the new password meets minimum length (typically 8+ characters) and includes uppercase, lowercase, and numeric characters.
```bash
# Show available roles
user role show

# List all roles
role list

# Assign a role to a user
user modify <username> --role <role_name>
```

```text title="Expected output"
Available Roles:
  admin
  operator
  backup_admin
  security_admin
  readonly

Role List:
  Role Name          Description                    Permissions
  admin              Full administrative access     All
  operator           Standard operations            Read, Write, Execute
  backup_admin       Backup management              Backup, Restore, Schedule
  security_admin     Security configuration         Security, Audit, Policy
  readonly           Read-only access               Read

User 'jsmith' modified successfully.
  Role assigned: backup_admin
  Effective immediately
```

!!! warning "Common errors"
    **`user role show: command not found`** — Use the correct command syntax `role list` or check that you are logged into the Data Domain CLI with proper permissions.
    **`user modify: invalid role 'backup_operator'`** — Verify the role name exists by running `role list` and use an exact match from the available roles.
```bash
# Show authentication configuration (local, LDAP, AD)
auth show

# Enable LDAP authentication
auth add ldap server <ldap_ip> bind-dn <dn> bind-password <pass> base-dn <base_dn>

# Enable Active Directory
auth add active-directory <domain>

# Test LDAP authentication
auth test ldap server <ldap_ip>
```

```text title="Expected output"
Authentication Configuration:
  Local Authentication: enabled
  LDAP Authentication: disabled
  Active Directory: disabled

LDAP server added successfully.
  Server: 10.45.12.8
  Bind DN: cn=svc-ddboost,ou=service-accounts,dc=corp,dc=local
  Base DN: ou=users,dc=corp,dc=local
  Status: configured

Active Directory domain added successfully.
  Domain: corp.local
  Status: configured

Testing LDAP authentication...
  Server: 10.45.12.8
  Connection: successful
  Bind test: passed
  Base DN search: passed
```

!!! warning "Common errors"
    **`Error: LDAP server <ldap_ip> is unreachable`** — Verify network connectivity to the LDAP server IP and confirm firewall rules allow port 389 (or 636 for LDAPS).
    **`Error: Invalid bind credentials for <dn>`** — Confirm the bind-dn and bind-password are correct by testing them directly against the LDAP server.
    **`Error: Active Directory domain <domain> cannot be resolved`** — Ensure the domain name is correct and that DNS resolution is working on the Data Domain appliance.
```bash
# View password policy
user password-policy show

# Set minimum password length
user password-policy set min-length 12

# Set maximum password age (days)
user password-policy set max-age 90
```

```text title="Expected output"
Password Policy Configuration
==============================
Minimum length: 8
Maximum age: 180 days
Minimum uppercase: 1
Minimum lowercase: 1
Minimum digits: 1
Minimum special characters: 0
Password history: 5

(no output — command completes silently)

(no output — command completes silently)
```

!!! warning "Common errors"
    **`user password-policy: command not found`** — Verify you are connected to the Data Domain system via SSH or console and have administrative privileges.
    **`Error: Cannot set min-length to 12: minimum supported value is 6`** — Adjust the min-length parameter to a value between 6 and 32 characters.
```bash
# Show authorized SSH keys for a user
user ssh-keys show <username>

# Add an SSH public key
user ssh-keys add <username> key "<public_key_string>"

# Remove an SSH key
user ssh-keys del <username> key <key_id>
```

```text title="Expected output"
# Show authorized SSH keys for a user
user ssh-keys show admin
Key ID: 1
  Fingerprint: SHA256:AbCdEfGhIjKlMnOpQrStUvWxYz1234567890abcd
  Comment: admin@workstation-01
  Created: 2024-01-15 09:23:44 UTC

Key ID: 2
  Fingerprint: SHA256:XyZ9876543210fedcbaZyXwVuTsRqPoNmLkJiHg
  Comment: admin@backup-server
  Created: 2024-02-03 14:51:12 UTC

# Add an SSH public key
user ssh-keys add admin key "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDk7vN2x8q9pL..."
SSH key added successfully.
Key ID: 3

# Remove an SSH key
user ssh-keys del admin key 2
SSH key removed successfully.
```

!!! warning "Common errors"
    **`Error: User 'admin' not found`** — Verify the username exists on the Data Domain system using `user list`.
    **`Error: Invalid public key format`** — Ensure the public key string starts with `ssh-rsa`, `ssh-ed25519`, or `ecdsa-sha2-` and contains no line breaks.
    **`Error: Key ID 2 not found for user 'admin'`** — Confirm the key ID exists by running `user ssh-keys show <username>` before attempting deletion.
```bash
# Active login sessions
user login show

# Terminate a specific session
user login terminate <session_id>
```

```text title="Expected output"
Active login sessions:
Session ID    User         Login Time           Source IP        Session Type
1             admin        2024-01-15 09:23:14  192.168.1.50     SSH
2             backup_user  2024-01-15 08:45:22  10.20.30.100     SSH
3             monitor      2024-01-15 07:12:08  172.16.0.25      Web
4             sysadmin     2024-01-14 22:18:45  192.168.1.75     SSH

Session 2 terminated successfully.
```

!!! warning "Common errors"
    **`user login terminate: session not found`** — Verify the session ID exists by running `user login show` and confirm the ID matches exactly.
    **`user login terminate: permission denied`** — Ensure your user account has administrative privileges; contact your Data Domain administrator if needed.
```bash
# View authentication audit log
log view | grep -i "login\|auth\|failed"

# Export audit events
log dump system | grep -i auth
```


```text title="Expected output"
2024-01-15 09:23:47 UTC [admin] LOGIN SUCCESS from 192.168.1.50
2024-01-15 09:24:12 UTC [backup_user] AUTH_TOKEN_GENERATED duration=3600s
2024-01-15 09:45:33 UTC [svc_account] LOGIN FAILED - Invalid credentials from 10.0.2.15
2024-01-15 10:12:05 UTC [admin] LOGIN SUCCESS from 192.168.1.50
2024-01-15 10:15:22 UTC [replication] AUTH_REFRESH success
2024-01-15 11:03:44 UTC [guest] LOGIN FAILED - Account locked from 172.16.0.8
2024-01-15 11:45:18 UTC [admin] LOGOUT from 192.168.1.50
```

!!! warning "Common errors"
    **`log view: command not found`** — Use the correct Data Domain CLI command `show log` or `log list` depending on your DD OS version.
    **`grep: (standard input) is empty`** — Verify the audit log contains entries by running `log view` without filters first, or check that logging is enabled with `show system config`.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Data Domain — Procedures](../procedures/)
- [Data Domain — Scripts](../scripts/)
- [Data Domain — Health Checks](../health-checks/)
