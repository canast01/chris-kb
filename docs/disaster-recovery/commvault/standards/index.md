# CommVault Standards

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Storage Policy | `<app>-<retention>-<tier>` | `oracle-7yr-primary`, `vm-90d-secondary` |
| Subclient | `<app>-<env>-<host>-<type>` | `oracle-prod-db01-full` |
| Client Group | `<env>-<os>-<tier>` | `prod-linux-db`, `dev-windows-app` |
| Schedule Policy | `<frequency>-<retention>` | `daily-14d`, `weekly-8w` |
| MediaAgent | `<site>-ma-<seq>` | `dc1-ma-01`, `dc2-ma-01` |

## Retention Schedule

| Level | Copy | Retention |
|---|---|---|
| Daily | Primary (disk/dedup) | 14 days |
| Weekly | Primary (disk/dedup) | 8 weeks |
| Monthly | Secondary (offsite or cloud) | 12 months |
| Yearly | Secondary (tape or cloud archive) | 7 years |

Configure via SLA Plans in Command Center (preferred for FR32+) or directly in Storage Policy (legacy).

## Backup Job Design

- Each Storage Policy must have:
  - A primary copy (performance tier disk with dedup)
  - A secondary copy (off-site or cloud, separate schedule) in the same policy
- Do not rely on manual auxiliary copy jobs — secondary copies should be scheduled automatically
- Synthetic full schedule recommended weekly (no additional storage reads from client)

## DDB (Deduplication Database) Standards

| Parameter | Standard |
|---|---|
| DDB storage | Dedicated SSD LUN — never share with OS or backup data |
| DDB free space | Minimum 20% free at all times; alert at 30% |
| Single DDB capacity | Maximum 60TB deduped data per DDB |
| DDB backup | Daily via CommServe backup job |
| DDB validation | Monthly integrity check via DDB Verification job |

```powershell
# Check DDB utilisation
qoperation execute -af ListDDB.xml
```

## VMware vSphere Standards

| Setting | Value |
|---|---|
| Backup proxy type | Hot-add (SAN or VDDK) preferred over NBD |
| Number of proxies | Minimum 2 per site for redundancy |
| VMware concurrent tasks per proxy | Maximum 4 (adjust per MediaAgent CPU) |
| VSA subclient granularity | Per-datastore or per-folder; never entire vCenter in one subclient |
| Application-aware backup | Enabled for SQL Server, Oracle, Exchange VMs |

## Encryption Standard

| Data Classification | Encryption Required | Algorithm |
|---|---|---|
| PII / Regulated | Yes — mandatory | AES-256, MediaAgent-side minimum |
| Business-sensitive | Yes — recommended | AES-256 |
| Internal non-sensitive | Optional | Per policy decision |

- Encryption keys: exported and stored in CyberArk or offline secure vault
- Loss of key = loss of backup data — key management is as critical as backup data itself
