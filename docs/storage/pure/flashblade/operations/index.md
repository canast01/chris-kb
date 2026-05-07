# Operations

> Part of the [Pure FlashBlade](../) reference.

---
## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Run `purefb alert list` | `purefb alert list` | review all active alerts; flag any hardware, capacity, or replication warnings |
| [ ] Run `purefb blade list` | `purefb blade list` | confirm all blades are in `healthy` state; flag any `failed` or `missing` blades |
| [ ] Run `purefb hardware list` | `purefb hardware list` | confirm all hardware components (power supplies, fans, fabric modules) are healthy |
| [ ] Run `purefb filesystem list` | `purefb filesystem list` | review filesystem utilization; flag any filesystem above 80% of provisioned limit |
| [ ] Run `purefb bucket list` | `purefb bucket list` | check S3 bucket count and data growth trends |
| [ ] Run `purefb replication list` | `purefb replication list` | confirm all ActiveDR links are in `active` status with lag within RPO |
| [ ] Check Pure1 portal for capacity growth forecasts, anomalies, and h |  |  |

## Health Check

- [ ] No active alerts in `purefb alert list`
- [ ] All blades are `healthy` — no `failed` or `missing` blades in `purefb blade list`
- [ ] All hardware components healthy — no PSU, fan, or FM (fabric module) failures
- [ ] No filesystems at or above provisioned limit — clients would receive ENOSPC errors
- [ ] All ActiveDR replication links are `active` and lag is within RPO
- [ ] All network interfaces are `up`: `purefb network interface list`
- [ ] Purity//FB version is within Pure's supported N-2 release window

~~~bash
# FlashBlade array status and Purity//FB version
purefb array list

# All blades and their health state
purefb blade list

# All hardware components (PSUs, fans, FMs) and status
purefb hardware list

# All filesystems with provisioned and used capacity
purefb filesystem list

# All S3 buckets and usage
purefb bucket list

# All active alerts
purefb alert list

# ActiveDR replication links and lag
purefb replication list

# All snapshots for filesystems and object store
purefb snap list

# Network interfaces and their operational state
purefb network interface list
~~~

## Change Readiness

- [ ] No active blade rebuilds or hardware failures — `purefb blade list` and `purefb hardware list` are clean
- [ ] ActiveDR replication is current — lag is within RPO; document baseline lag before the change
- [ ] NFS and SMB clients are informed of the potential brief reconnection event during Purity upgrades
- [ ] S3 clients and applications are notified if the change could cause a brief service interruption
- [ ] Filesystem capacity headroom is sufficient — no filesystems above 70% provisioned limit during the window
- [ ] Pure1 upgrade readiness report reviewed (for Purity//FB upgrades): no blockers flagged
- [ ] Snapshot schedule expiry policy is functioning — no runaway snapshot growth that could fill capacity during the window

| Item | Status | Notes |
|---|---|---|
| No active blade rebuilds | | |
| ActiveDR replication current | | |
| NFS/SMB client impact assessed | | |
| Filesystem capacity headroom sufficient | | |
| Pure1 upgrade readiness checked (if upgrading) | | |

## Incident Triage

- [ ] Run `purefb alert list` first — active alerts identify the failure domain (blade, hardware, replication, capacity)
- [ ] Run `purefb blade list` — a failed or missing blade is a capacity and performance degradation event; open a Pure support case immediately
- [ ] Run `purefb hardware list` — check for failed PSU, fan, or fabric module; multiple failures on the same chassis indicate a critical event
- [ ] Check filesystem and bucket accessibility: `purefb filesystem list` — a filesystem at its provisioned limit causes client write failures
- [ ] Check replication: `purefb replication list` — an `inactive` or high-lag replication link requires investigation of the network path between sites
- [ ] For NFS `stale file handle` errors: the issue is typically client-side after a FlashBlade event — unmount and remount on affected clients
- [ ] For S3 403 errors: run `purefb objectstoreaccount list` to check access key status and verify bucket policies

| Question | Answer |
|---|---|
| What does `purefb alert list` show? | |
| Are any blades failed or missing? | |
| Is any filesystem at or near its provisioned limit? | |
| Are ActiveDR replication links active and within RPO? | |
| Is this affecting NFS, SMB, S3, or all protocols? | |

## Maintenance Window

1. Notify NFS, SMB, and S3 clients of the maintenance window — Purity//FB upgrades are non-disruptive but protocol sessions may briefly re-establish
2. For blade maintenance: use `purefb blade maintenance` to put the blade in maintenance mode before physical intervention — data rebalances automatically
3. For Purity//FB upgrade: confirm `purefb blade list` shows all blades `healthy` and no alerts are open before starting
4. Download the Purity//FB upgrade image from the Pure Support portal and stage it on the array
5. Run the pre-upgrade validation from the GUI or CLI to confirm no blockers
6. Execute the upgrade during the window; monitor progress from the Purity//FB GUI or `purefb array list`
7. For ActiveDR: pause replication links if required during the change with `purefb replication link update --paused true`; resume with `--paused false` after the change

## Post-Change Validation

- [ ] `purefb alert list` — no unresolved alerts
- [ ] `purefb blade list` — all blades `healthy`; no blades in maintenance or failed state
- [ ] `purefb hardware list` — all hardware components healthy
- [ ] `purefb filesystem list` — all filesystems accessible and below provisioned limit
- [ ] Test NFS mount from a representative client: `mount -t nfs <fb-data-vip>:/<filesystem> /mnt/test`
- [ ] Test S3 API response: confirm bucket listing or object operation succeeds from an S3 client or `aws s3 ls`
- [ ] `purefb replication list` — all ActiveDR links are `active` and lag is recovering toward RPO
- [ ] Pure1 shows the new Purity//FB version and no new hardware alerts (if this was an upgrade)
