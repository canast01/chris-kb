---
tags:
  - architecture
  - pure
---
# FlashBlade — Integrations

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                       FlashBlade                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                                                             │
│  │  NFS/SMB │  │    S3    │  │   Mgmt   │                                                             │
│  │  data    │  │  object  │  │  HTTPS   │                                                             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                                                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

> Part of the [FlashBlade Architecture](../index.md) reference.

---

## VMware Integration

FlashBlade integrates with VMware primarily as an NFS datastore and backup target — it is not a block storage device and does not use VMFS or vVols in the same way as FlashArray.

**NFS datastore for vSphere:**

- Mount FlashBlade filesystems as NFSv3 or NFSv4.1 datastores in vCenter
- NFSv4.1 is recommended for vSphere 7.x/8.x — enables Kerberos authentication and improved locking semantics
- Create a dedicated filesystem per datastore type (e.g., `prod-vsphere-vmstore`, `prod-vsphere-templates`)
- Set NFS export policies to restrict access to the ESXi management IP range only

**vSphere integration steps:**

1. Create a FlashBlade filesystem for the datastore: `purefb filesystem create --nfs --nfs-rules '<subnet>(rw,root_squash)' prod-vsphere-vmstore`
2. In vCenter, add a new NFS datastore pointing to the FlashBlade data VIP and the export path
3. Mount the datastore on all ESXi hosts in the cluster using vCenter's storage configuration wizard
4. Configure VAAI (vStorage APIs for Array Integration) — FlashBlade supports NAS VAAI for hardware-accelerated copy offload

**Backup target for Veeam:**

- Use a dedicated FlashBlade filesystem as a Veeam NFS backup repository
- FlashBlade's Rapid Restore integration with Veeam provides backup-from-snapshot and instant recovery capabilities — see Backup Integration below

## Backup Integration

**Veeam Backup & Replication:**

- Add FlashBlade as an NFS share repository in Veeam: `Backup Infrastructure > Backup Repositories > Add Repository > Network Attached Storage > NFS Share`
- For Veeam Rapid Restore (FlashBlade native integration): install the Pure Storage Veeam Plugin; configure FlashBlade as a snapshot-enabled repository
- Veeam uses FlashBlade snapshot APIs to create instant, consistent snapshots before backup starts — backup reads from the snapshot, not live data, so production filesystem performance is not impacted
- Use a dedicated filesystem per Veeam backup tier (daily, weekly, monthly) to simplify retention management

**Commvault:**

- Configure FlashBlade as an NFS media agent library in Commvault
- Commvault IntelliSnap integrates with FlashBlade via the REST API to orchestrate snapshot-based backups
- FlashBlade snapshots are used as the backup source, avoiding impact to live production filesystems

**Veritas NetBackup:**

- Add FlashBlade NFS exports as disk storage units in NetBackup
- NetBackup Snapshot Client can orchestrate FlashBlade filesystem snapshots via the FlashBlade REST API

**General backup best practices:**

- Dedicate separate filesystems per backup application and tier
- Set filesystem capacity limits to match backup retention design
- Enable per-filesystem snapshot schedules as an additional recovery layer
- Use NFS export IP restrictions to limit backup server access to the backup filesystem only

## Pure1 Monitoring

FlashBlade phones home to Pure1 automatically over HTTPS once registered.

**Phone-home requirements:**

- Outbound HTTPS (port 443) from the FlashBlade management interface to `*.purestorage.com`
- If a proxy is required: configure via the FlashBlade GUI under System > Support

**Pure1 capabilities for FlashBlade:**

- Fleet health dashboard including blade status, hardware faults, and capacity forecasting
- Throughput and latency analytics per filesystem and per protocol (NFS, SMB, S3)
- Replication lag monitoring for ActiveDR links
- Upgrade readiness reports and prescriptive upgrade paths
- AI-driven anomaly detection for capacity and performance trends

**Verify phone-home status:**

```

```bash
purefb array list --phonehome
```
```bash
## Log in and obtain a session token
curl -s -k -X POST "https://<fb_ip>/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"pureuser","password":"<password>"}' \
  -c /tmp/fb_cookies.txt

## Use the session cookie for subsequent requests
curl -s -k -X GET "https://<fb_ip>/api/2.x/arrays" \
  -b /tmp/fb_cookies.txt | jq .

## Alternatively, use an API token (preferred for automation)
curl -s -k -X GET "https://<fb_ip>/api/2.x/arrays" \
  -H "x-auth-token: <api_token>" | jq .
```
```bash
## On the array CLI
purefb admin apitoken create <username>
```
```bash
## Get array status and version
GET /api/2.x/arrays

## List all filesystems with space usage
GET /api/2.x/file-systems?space=true

## List all blades and health
GET /api/2.x/blades

## List all active alerts
GET /api/2.x/alerts?filter=state%3D%27unflagged%27

## List S3 buckets
GET /api/2.x/buckets

## List replication relationships
GET /api/2.x/array-connections
```
