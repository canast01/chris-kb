---
tags:
  - dr
---
# DR Failback Procedure

<div class="kb-summary">
DR failback procedure: confirm production site healthy, reverse-resync storage replication, redirect hosts back to production, restore daily and weekly backup schedules on production, and validate that retention-compliant backups exist before decommissioning DR workloads.

*Applies to: all products with DR replication*
</div>

```bash
# Confirm primary storage arrays healthy
# ONTAP
system health status show
storage disk show -broken

# Pure FlashArray
purecli array get
purecli drive list | grep -v healthy

# Confirm primary SAN fabric healthy
show interface fc brief           # Cisco MDS
switchshow                        # Brocade
```


```text title="Expected output"
ONTAP Health Status:
Status: ok

Broken Disks:
(no broken disks)

Pure FlashArray Status:
Name                          Revision  Serial                Mode
flasharray-prod-01            6.4.2     5b8c3e2f-a1b2-4c5d   optimal

Pure Drive List (non-healthy):
(no unhealthy drives detected)

Cisco MDS FC Interface Status:
Interface            Status       Speed      State
fc1/1                up           16 Gbps    trunking
fc1/2                up           16 Gbps    trunking
fc1/3                down         unknown    notConnected
fc1/4                up           16 Gbps    trunking

Brocade Switch Status:
Switch Index: [0]
Switch State: Online
Fabric State: Stable
```

!!! warning "Common errors"
    **`system health status show: command not found`** — Verify you are connected to the ONTAP cluster management IP and have appropriate SSH credentials configured.
    **`purecli: command not found`** — Install the Pure Storage CLI package or ensure the FlashArray management network is reachable and purecli is in your PATH.
    **`show interface fc brief: command not found`** — Confirm you are in the correct CLI context (Cisco MDS switch) and not in a different device shell.
```bash
# ONTAP — confirm lag is zero before breaking
snapmirror show -destination-path <primary-svm>:<primary-vol> -fields lag-time
# lag-time should be 00:00:00 or very small

# Break mirror — primary volume becomes writable
snapmirror break -destination-path <primary-svm>:<primary-vol>
```
```powershell
# Shut down VM at DR
Stop-VM -VM "<vm-name>" -Confirm:$false

# Power on at primary (VM should already be registered from original config)
Start-VM -VM "<vm-name>" -Server <primary-vcenter>
```
```bash
# Storage visible at primary hosts
multipath -ll
lsblk
df -h

# Application services
systemctl start <service>
systemctl status <service>

# Application health
curl -vk https://<primary-app-url>/health
```

```text title="Expected output"
mpatha (36001405a1b2c3d4e5f6g7h8i9j0k1l2m) dm-0 NETAPP,LUN C-Mode
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:0:0 sda 8:0  active ready running
  `- 3:0:0:0 sdb 8:16 active ready running

NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0  500G  0 disk
├─sda1   8:1    0  512M  0 part /boot
└─sda2   8:2    0 99.5G  0 part /
sdb      8:16   0  500G  0 disk /mnt/data

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda2       100G   45G   55G  45% /
/dev/sdb       500G  320G  180G  64% /mnt/data
tmpfs          7.8G     0  7.8G   0% /dev/shm

Created symlink /etc/systemd/system/multi-user.target.wants/app-service.service → /etc/systemd/system/app-service.service.
● app-service.service - Application Service
     Loaded: loaded (/etc/systemd/system/app-service.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2s ago
   Main PID: 8742 (java)

*   Trying 10.42.18.105:443...
* Connected to primary-app-01.prod.local (10.42.18.105) port 443 (#0)
> GET /health HTTP/1.1
< HTTP/1.1 200 OK
< Content-Type: application/json
{"status":"UP","timestamp":"2024-01-15T14:32:45Z","version":"8.2.1-build.4521"}
```

!!! warning "Common errors"
    **`Unit app-service.service not found.`** — Verify the service file exists at `/etc/systemd/system/app-service.service` and run `systemctl daemon-reload` before starting.
    **`curl: (7) Failed to connect to primary-app-01.prod.local port 443: Connection refused`** — Confirm the application service is listening on port 443 and firewall rules allow inbound HTTPS traffic to the primary host.
    **`Device or resource busy`** — Ensure no other processes are accessing the multipath devices and that the failback operation has fully completed before attempting to remount storage.
```bash
# PostgreSQL
psql -U <user> -c "SELECT pg_database_size('<db>');"

# MSSQL (PowerShell)
Invoke-Sqlcmd -Query "DBCC CHECKDB('<db>') WITH NO_INFOMSGS" -ServerInstance <primary-sql>
```

```text title="Expected output"
pg_database_size 
------------------
 5368709120
(1 row)

Checking database integrity for database 'production_db'.
DBCC execution completed. If DBCC printed error messages, review and correct the reported problems.
```

!!! warning "Common errors"
    **`psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed`** — Verify the PostgreSQL service is running and the hostname/port in your connection string is correct.
    **`Login failed for user '<user>'. Reason: Could not find a login matching the name provided.`** — Ensure the SQL Server account exists and has appropriate permissions on the target instance.
    **`DBCC CHECKDB statement not recognized`** — Confirm you are running the Invoke-Sqlcmd command on a Windows system with SQL Server PowerShell module installed (Install-Module SqlServer).
```bash
# ONTAP — resync back to original direction
snapmirror resync -source-path <primary-svm>:<primary-vol> -destination-path <dr-svm>:<dr-vol>

# Confirm
snapmirror show -destination-path <dr-svm>:<dr-vol>
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [DR Runbooks](../index.md)
- [Failover](../failover/index.md)
- [Full DR Runbook](../dr-runbook/index.md)
- [DR Design](../../dr-design/index.md)
- [Recovery Testing](../../recovery-testing/index.md)
