---
tags:
  - architecture
  - netapp
description: "Standards reference covering SyncIQ Policy Naming, DR Readiness Score, Failover Test Frequency, Operational Standards, Policy Configuration."
---
# Superna Eyeglass — Standards

<div class="kb-summary">
Standards reference covering SyncIQ Policy Naming, DR Readiness Score, Failover Test Frequency, Operational Standards, Policy Configuration.

*Applies to: Superna Eyeglass*
</div>
![Superna Eyeglass — Standards](../../../../../assets/storage-netapp-superna-eyeglass-architecture-design-standard.svg)

## SyncIQ Policy Naming

SyncIQ policy names must be consistent between primary and DR clusters and follow the format:

### Viewing Policies

```bash
# List all DR policies
egcli drpolicy list

# Detailed view of a specific policy
egcli drpolicy view --policy <policy_name>

# Status of all policies (replication state, lag, last test)
egcli drpolicy status --all

# List access zones included in a policy
egcli accesszone list --policy <policy_name>

# List SyncIQ policies mapped to a DR policy
egcli synciq list --policy <policy_name>
```


```text title="Expected output"
# List all DR policies
Policy Name          Status    Type        Target Cluster    Last Updated
prod-dr-policy       Active    Async       cluster-dr-02     2024-01-15 14:32:18
backup-hourly        Active    Sync        cluster-dr-03     2024-01-15 14:28:45
test-failover        Inactive  Async       cluster-dr-02     2024-01-14 09:15:22
archive-weekly       Active    Async       cluster-dr-04     2024-01-14 23:59:01

# Detailed view of a specific policy
Policy Name:         prod-dr-policy
Status:              Active
Type:                Asynchronous
Target Cluster:      cluster-dr-02 (192.168.50.10)
RPO (minutes):       15
RTO (minutes):       30
Last Replication:    2024-01-15 14:32:18
Replication Lag:     2 minutes 14 seconds
Last Test Date:      2024-01-10 11:45:00
Test Status:         PASSED

# Status of all policies (replication state, lag, last test)
Policy Name          Replication State    Lag        Last Test Result    Next Test
prod-dr-policy       In Sync              2m 14s     PASSED (Jan 10)     Jan 17 11:00
backup-hourly        In Sync              45s        PASSED (Jan 12)     Jan 19 08:30
test-failover        Idle                 N/A        FAILED (Jan 08)     Jan 22 14:00
archive-weekly       In Sync              8m 32s     PASSED (Jan 07)     Jan 21 06:00

# List access zones included in a policy
Access Zone          Replication Status    Data Size    Last Sync
system               Active                245 GB       2024-01-15 14:32:10
zone-finance         Active                1.2 TB       2024-01-15 14:31:55
zone-hr              Active                340 GB       2024-01-15 14:32:05

# List SyncIQ policies mapped to a DR policy
SyncIQ Policy ID     Source Path          Target Path              Status
sync-001             /ifs/data/finance    /ifs/dr/finance         Active
sync-002             /ifs/data/hr         /ifs/dr/hr              Active
sync-003             /ifs/data/archive    /ifs/dr/archive         Paused
```

!!! warning "Common errors"
    **`Error: Policy '<policy_name>' not found`** — Verify the policy name with `egcli drpolicy list` and use the exact name from the output.
    **`Error: Connection refused to cluster-dr-02`** — Ensure the target cluster is reachable and the network path is not blocked by firewall rules.
    **`Error: Insufficient permissions to view policy details`** — Confirm your user account has the required DR policy read permissions in Eyeglass RBAC settings.
### Creating a DR Policy

DR policies are typically created via the Eyeglass web UI. CLI equivalent:

```bash
# Create a new DR policy (basic parameters)
egcli drpolicy create \
  --name POL-NAS-PROD \
  --source-cluster <production-cluster> \
  --target-cluster <dr-cluster> \
  --access-zone <zone_name> \
  --synciq-policy <synciq_policy_name> \
  --rpo-seconds 300

# Add additional access zones to an existing policy
egcli drpolicy addzone --policy POL-NAS-PROD --access-zone <zone2_name>

# Add additional SyncIQ policies to an existing policy
egcli drpolicy addsync --policy POL-NAS-PROD --synciq-policy <synciq_policy2>

# Enable the policy
egcli drpolicy enable --policy POL-NAS-PROD
```


```text title="Expected output"
Creating DR policy POL-NAS-PROD...
Policy POL-NAS-PROD created successfully
  Source Cluster: prod-cluster-01.corp.local
  Target Cluster: dr-cluster-02.corp.local
  Access Zone: system
  SyncIQ Policy: sync-prod-hourly
  RPO: 300 seconds
  Status: disabled

Adding access zone zone2 to policy POL-NAS-PROD...
Access zone zone2 added successfully

Adding SyncIQ policy sync-prod-daily to policy POL-NAS-PROD...
SyncIQ policy sync-prod-daily added successfully

Enabling policy POL-NAS-PROD...
Policy POL-NAS-PROD enabled successfully
  Current Status: active
  Last Modified: 2024-01-15T09:42:17Z
```

!!! warning "Common errors"
    **`Error: Policy POL-NAS-PROD already exists`** — Use a unique policy name or delete the existing policy with `egcli drpolicy delete --policy POL-NAS-PROD` first.
    **`Error: Access zone <zone2_name> not found on target cluster`** — Verify the access zone exists on the DR cluster with `egcli zone list --cluster <dr-cluster>`.
    **`Error: SyncIQ policy <synciq_policy2> does not exist`** — Confirm the SyncIQ policy name is correct and exists with `egcli synciq list --cluster <production-cluster>`.
### SyncIQ Integration

Eyeglass monitors and manages SyncIQ policies as part of DR orchestration. SyncIQ policies must be pre-configured on the production PowerScale cluster.

```bash
# On production PowerScale — view SyncIQ policy configuration
isi sync policies view <synciq_policy_name>

# Confirm policy target is the DR cluster
# Confirm schedule (should be frequent enough to meet RPO)
# Confirm source/target paths match the access zone directories

# Check last run time and status
isi sync reports list --policy <synciq_policy_name> --limit 5

# Manually trigger a SyncIQ sync (e.g., before a planned failover)
isi sync jobs start <synciq_policy_name>

# Monitor sync job completion
isi sync jobs list
```


```text title="Expected output"
Name: prod-to-dr-sync
Policy ID: 8f4c2a91-7e3f-4d8b-9c1a-5b3e8f2d6a4c
Source Path: /ifs/data/production
Target Cluster: dr-cluster-01.example.com
Target Path: /ifs/data/production
Schedule: Every 6 hours
Enabled: Yes
Last Run: 2024-01-15T14:32:18Z
Last Run Status: Succeeded

ID                                    Policy Name         Start Time              End Time                Status      Duration
8f4c2a91-7e3f-4d8b-9c1a-5b3e8f2d6a4c  prod-to-dr-sync     2024-01-15T14:32:18Z    2024-01-15T14:47:22Z    Succeeded   15m 4s
7e3f4d8b-9c1a-5b3e8f2d6a4c-8f4c2a91   prod-to-dr-sync     2024-01-15T08:15:09Z    2024-01-15T08:29:44Z    Succeeded   14m 35s
5b3e8f2d-6a4c-8f4c-2a91-7e3f4d8b9c1a   prod-to-dr-sync     2024-01-15T02:10:33Z    2024-01-15T02:25:18Z    Succeeded   14m 45s
...

Job ID: 9c1a-5b3e-8f2d-6a4c-8f4c2a91-7e3f
Policy: prod-to-dr-sync
Status: RUNNING
Progress: 847 GB of 1.2 TB (70%)
Elapsed Time: 8m 22s
Estimated Remaining: 3m 45s

ID                                    Policy Name         Status      Progress
9c1a-5b3e-8f2d-6a4c-8f4c2a91-7e3f     prod-to-dr-sync     RUNNING     70%
```

!!! warning "Common errors"
    **`Error: Policy 'prod-to-dr-sync' not found`** — Verify the policy name matches exactly with `isi sync policies list` and check for typos or case sensitivity.
    **`Error: Connection refused to target cluster dr-cluster-01.example.com`** — Confirm network connectivity and HTTPS/port 8080 access between clusters, and verify the target cluster hostname is resolvable.
    **`Error: Job already running for policy 'prod-to-dr-sync'`** — Wait for the current sync job to complete before manually triggering another, or use `isi sync jobs cancel <job_id>` if needed.
| SyncIQ Setting | Recommended Value |
|---|---|
| Schedule | Every 5–15 minutes (match RPO target) |
| Source root | Access zone base directory |
| Target path | Matching path on DR cluster |
| Workers per node | 3 (default; increase for high-throughput environments) |
| Log level | Info |

### Policy RPO Monitoring

```bash
# Check current replication lag vs RPO target per policy
egcli drpolicy status --all

# Alert if lag exceeds RPO
# Eyeglass sends SNMP traps or syslog events on RPO breach
# Forward events to monitoring: Settings → Notifications in Eyeglass UI

# Manually check SyncIQ lag on production cluster
isi sync policies list | grep -E "Name|Last|Status"
```


```text title="Expected output"
Policy Name: prod-hourly-sync
  Target RPO: 1 hour
  Current Lag: 47 minutes
  Status: In Sync
  Last Run: 2024-01-15 14:32:15 UTC

Policy Name: dr-daily-backup
  Target RPO: 24 hours
  Current Lag: 18 hours 23 minutes
  Status: In Sync
  Last Run: 2024-01-15 06:15:42 UTC

Policy Name: archive-weekly
  Target RPO: 7 days
  Current Lag: 5 days 12 hours
  Status: In Sync
  Last Run: 2024-01-14 22:00:08 UTC

Name                          Last Run                Status
prod-hourly-sync              2024-01-15 14:32:15    Finished
dr-daily-backup               2024-01-15 06:15:42    Finished
archive-weekly                2024-01-14 22:00:08    Finished
```

!!! warning "Common errors"
    **`Error: Connection refused to Eyeglass API on 192.168.1.50:8443`** — Verify Eyeglass appliance is running and network connectivity exists with `ping` and `nc -zv`.
    **`isi: command not found`** — Run the `isi` command directly on the OneFS cluster console or configure SSH key-based authentication to the cluster in your shell environment.
### Modifying and Disabling Policies

```bash
# Update RPO target for a policy
egcli drpolicy modify --policy <policy_name> --rpo-seconds 600

# Disable a policy (e.g., when decommissioning a workload)
egcli drpolicy disable --policy <policy_name>

# Remove an access zone from a policy
egcli drpolicy removezone --policy <policy_name> --access-zone <zone_name>

# Delete a policy (caution — removes Eyeglass orchestration but does not
# remove underlying SyncIQ policies from PowerScale)
egcli drpolicy delete --policy <policy_name> --confirm

# After deletion: verify remaining SyncIQ policies on PowerScale are correct
isi sync policies list
```


```text title="Expected output"
Policy 'prod-dr-policy' RPO target updated to 600 seconds
Policy 'prod-dr-policy' disabled successfully
Access zone 'finance_zone' removed from policy 'prod-dr-policy'
Policy 'prod-dr-policy' deleted from Eyeglass orchestration
Sync policies on cluster 'pscale-prod-01':
  prod-dr-policy-sync (source: /ifs/data/prod, target: 10.50.12.45:/ifs/backup, interval: 600s)
  archive-dr-policy-sync (source: /ifs/archive, target: 10.50.12.46:/ifs/backup, interval: 3600s)
  legacy-sync-policy (source: /ifs/legacy, target: 10.50.12.47:/ifs/backup, interval: 7200s)
```

!!! warning "Common errors"
    **`Error: Policy 'prod-dr-policy' not found`** — Verify the policy name with `egcli drpolicy list` and use the exact name.
    **`Error: Cannot remove access zone 'finance_zone': zone is actively replicating`** — Disable the policy first with `egcli drpolicy disable` or wait for the current sync cycle to complete.
    **`Error: SyncIQ policy 'prod-dr-policy-sync' still exists on PowerScale cluster`** — Manually delete orphaned SyncIQ policies from PowerScale using `isi sync policies delete` after confirming they are no longer needed.
---

## See also

- [Superna Eyeglass — How It Works](../how-it-works/)
- [Superna Eyeglass — Integrations](../integrations/)
- [Superna Eyeglass — Deploy](../../deploy/)
