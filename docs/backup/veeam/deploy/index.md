---
tags:
  - deployment
  - veeam
search:
  boost: 1.5
---
# Veeam — Initial Deployment

This guide walks through deploying Veeam Backup & Replication from bare metal to a
fully operational backup environment. Steps cover server installation, infrastructure
onboarding, proxy and repository configuration, and first-job validation.

```text
┌───────────────────────────────────── Veeam — Initial Deployment ──────────────────────────────────────┐
│                                                                                                       │
│   VBR server: Windows 2019/2022; min 4 vCPU / 16 GB RAM; SQL Server for catalog                       │
│   Proxy servers offload data processing from VBR; one per VMware cluster or subnet                    │
│   Repositories store backup files; NAS, SAN LUN, object storage, or Scale-Out                         │
│   Configuration DB: bundled SQL Express (10 GB limit) or external SQL for production                  │
│                                                                                                       │
│   VBR server installation                                                                             │
│   Run Veeam installer; select Backup & Replication component; provide SQL connection                  │
│   Accept port defaults (9392 TCP for service, 443 for API and Enterprise Manager)                     │
│   Apply latest Veeam cumulative patches (P-series) immediately after initial install                  │
│   License: Help → License → Add License; enter NFR, rental, or perpetual key                          │
│                                                                                                       │
│   Infrastructure onboarding                                                                           │
│   Add vCenter: Infrastructure → Add Server → VMware vSphere → vCenter Server                          │
│   Add Hyper-V host: Infrastructure → Add Server → Microsoft Hyper-V                                   │
│   Add physical servers (Linux/Windows): Infrastructure → Add Server → Windows/Linux                   │
│   Credentials stored in Veeam Credentials Manager; use service accounts, not admin                    │
│                                                                                                       │
│   Proxy and repository configuration                                                                  │
│   Add proxy: Infrastructure → Backup Proxies → Add VMware Backup Proxy                                │
│   Proxy transport mode: Direct SAN (fastest), Hot-Add (vSAN), NBD (fallback)                          │
│   Add repository: Backup Infrastructure → Backup Repositories → Add Backup Repository                 │
│   Scale-Out: combines multiple repositories into a single performance-tiering pool                    │
│                                                                                                       │
│   First-job validation                                                                                │
│   Create job: Home → Backup Job → Virtual machine; select VMs, policy, retention                      │
│   Run immediately: right-click job → Start; verify status = Success in last run column                │
│   Smoke test: restore single file from backup; verify content is intact and usable                    │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   VBR VM: Windows 2019/2022 with SQL; dedicated disk for VBRCatalog                                   │
│   Proxy VMs co-located with ESXi clusters; repositories on NAS or directly on SAN LUNs                │
│                                                                                                       │
│   Key terms:                                                                                          │
│   VBR          = Veeam Backup & Replication; the main server and console application                  │
│   proxy        = data processing VM; handles de-dup, compression, and encryption                      │
│   repository   = storage target holding .vbk (full) and .vib (incremental) backup files               │
│   Hot-Add      = proxy inside same vSAN cluster; accesses VMDKs via vSphere storage API               │
│   Direct SAN   = proxy reads VM data directly from SAN LUN; bypasses ESXi network path                │
│   NBD          = Network Block Device; LAN-based data path; slowest but always available              │
│   Scale-Out    = performance tier + capacity tier pool; auto-moves old data to cold storage           │
│   retention    = number of restore points kept; older points expire per policy settings               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Hardware and OS

- Windows Server 2019 or 2022 (Standard or Datacenter), 64-bit
- Minimum 4 vCPU, 8 GB RAM for the VBR server; 16 GB+ recommended for production
- 100 GB free disk for VBR installation and temporary files
- Separate volume recommended for the backup catalog (default: `C:\VBRCatalog`)

### SQL Server

- Veeam bundles Microsoft SQL Server 2019 Express (10 GB DB limit)
- For production, use an existing SQL Server 2016 or later instance
- Create a dedicated database (`VeeamBackup`) or let the installer create it
- VBR service account needs `db_owner` on the VeeamBackup database

### Network Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 9392 | TCP | VBR console to VBR server (default management) |
| 9401 | TCP | REST API (Veeam Backup Enterprise Manager / REST clients) |
| 2500–3300 | TCP | Data mover ports between proxy, repository, and VBR server |
| 443 | TCP | vCenter and ESXi API access |
| 902 | TCP | ESXi host management (NBD transport) |
| 6160 | TCP | Veeam Installer Service on managed Windows servers |
| 6162 | TCP | Veeam Data Mover on Linux servers |

### Domain and Service Accounts

- VBR server must be domain-joined (or workgroup with consistent local accounts)
- Create a dedicated service account (e.g. `SVC-Veeam`) with:
  - Local Administrator on the VBR server
  - Local Administrator on all proxy and repository servers
  - Read-only or backup-operator role on vCenter (or higher if using guest interaction)
- DNS resolution for all target hosts must be forward and reverse resolvable

---

## Install Veeam Backup & Replication Server

### Step 1 — Obtain the ISO

1. Download `VeeamBackup_12.x.iso` from the Veeam customer portal or
   the free trial page at `veeam.com/downloads`.
2. Mount the ISO on the Windows Server target (double-click or use
   `Mount-DiskImage` in PowerShell).

### Step 2 — Launch the Installer

1. Open the mounted ISO root and run `Setup.exe`.
2. The Veeam Backup & Replication setup hub opens.
3. Click **Install** under *Veeam Backup & Replication*.

### Step 3 — Select Components

On the component selection screen, choose:

- **Veeam Backup & Replication** (required)
- **Veeam Backup Catalog** (required; powers instant file-level search)
- **Veeam Backup & Replication Console** (install on VBR server; also installable remotely)
- **Veeam REST API** (required for automation and Enterprise Manager integration)

### Step 4 — License

- Enter your license file (`.lic`) or select *Free* for the Community Edition.
- Socket-based and instance-based licenses are supported; instance-based is common
  for virtual environments.

### Step 5 — SQL Configuration

- Select an existing SQL instance or accept the bundled SQL Express.
- For an existing instance: enter `SERVER\INSTANCE` and credentials.
- The installer creates the `VeeamBackup` database automatically.

### Step 6 — Service Account

- Enter the VBR service account (`DOMAIN\SVC-Veeam`) and password.
- The installer grants the account required local privileges automatically.

### Step 7 — Complete Installation

- Review the summary, click **Install**, and wait 10–15 minutes.
- After completion, the VBR Console opens automatically.
- Verify the VBR services are running in `services.msc`:
  - `Veeam Backup Service`
  - `Veeam Broker Service`
  - `Veeam Mount Service`

---

## Add vCenter / Hypervisor

### Step 1 — Open Managed Servers

In the VBR Console, navigate to **Backup Infrastructure** → **Managed Servers**.

### Step 2 — Add VMware vCenter

1. Click **Add Server** → **VMware vSphere** → **vCenter Server**.
2. Enter the vCenter FQDN or IP address.
3. Enter credentials (a dedicated read/backup-operator account is sufficient for
   inventory; use admin rights if enabling guest interaction features).
4. Click **Next** → accept the certificate fingerprint.

### Step 3 — Scan Inventory

- VBR connects to vCenter and enumerates all datacenters, clusters, hosts, and VMs.
- Verify the inventory tree appears under **Backup Infrastructure** →
  **Virtual Infrastructure**.
- For standalone ESXi hosts (no vCenter), choose **ESXi host** instead and enter
  the host address and root credentials.

---

## Add Backup Proxies

Backup proxies offload data movement from the VBR server.

### Step 1 — Add the Proxy Server

1. In VBR Console, go to **Backup Infrastructure** → **Backup Proxies**.
2. Click **Add VMware Backup Proxy**.
3. Select an existing managed server or add a new Windows/Linux server.

### Step 2 — Configure Transport Mode

| Mode | When to Use |
|------|-------------|
| Direct SAN Access | Proxy has direct FC/iSCSI access to production datastores |
| Virtual Appliance (HotAdd) | Proxy is a VM on the same ESXi host or cluster |
| Network (NBD/NBDSSL) | Fallback; uses ESXi management network — lower throughput |
| Backup from Storage Snapshots | Array integration (NetApp, HPE, etc.) |

- Choose the appropriate mode or set to **Automatic** to let VBR decide.
- Set the **Maximum concurrent tasks** (typically 2–4 per proxy core).

### Step 3 — Linux Proxy (Optional)

For Linux-based proxies (higher throughput, lower cost):

1. Add the Linux server under **Managed Servers** first.
2. Under **Backup Proxies**, add **Linux backup proxy**, select the managed Linux host.
3. VBR deploys the Veeam Data Mover service over SSH automatically.

---

## Add Backup Repositories

Repositories are where backup files are stored.

### Step 1 — Add a Repository

1. Go to **Backup Infrastructure** → **Backup Repositories**.
2. Click **Add Repository**.
3. Select the repository type:
   - **Direct attached storage** — Windows or Linux path
   - **SMB share** — network path (CIFS/NFS)
   - **Object storage** (S3-compatible) — AWS S3, MinIO, Wasabi, etc.
   - **Deduplication appliance** — DataDomain, StoreOnce, ExaGrid

### Step 2 — Windows / Linux Path

- Enter server and path (e.g. `E:\VeeamBackups`).
- Set **Concurrent tasks** (controls how many backup jobs write simultaneously).
- Enable **Per-VM backup chains** for faster synthetic fulls and parallel restores.
- Set **Max backup file size** if splitting large chains across volumes.

### Step 3 — Object Storage Repository

- Choose **Amazon S3** or **S3 Compatible**.
- Enter endpoint URL, access key, secret key, and bucket name.
- Select a storage class (Standard, Infrequent Access, Glacier — note restore latency
  for archive tiers).
- Object storage is typically used as a **capacity tier** in a Scale-Out Backup
  Repository (SOBR), not as a standalone repository for primary backups.

---

## Create First Backup Job

### Step 1 — New Backup Job

In VBR Console, go to **Home** → **Jobs** → **Backup** → **Virtual Machine**.

### Step 2 — Select VMs

- Browse the vCenter inventory or search by name.
- Add individual VMs, folders, resource pools, or entire clusters.
- Exclusions can be set by tag or datastore.

### Step 3 — Assign Storage

- **Backup proxy**: set to **Automatic** or pin to a specific proxy.
- **Backup repository**: select the repository created above.
- **Restore points to keep**: typically 7–14 (daily) or 28 (with weekly/monthly GFS).

### Step 4 — Configure Guest Processing

Enable **Application-aware processing** for:

- VSS-consistent backups of Windows applications (SQL, Exchange, Active Directory)
- Transaction log truncation (SQL Server, Exchange)
- Pre/post freeze scripts

Enter guest OS credentials (domain admin or local admin on each VM).

### Step 5 — Schedule

- Set the job to run daily (e.g. 22:00) or on a specific interval.
- Enable **Retry failed items** (3 retries is common).
- Set **Backup window** to terminate the job if it runs past a defined time.

### Step 6 — Notifications

- Under **Advanced** → **Notifications**, configure SMTP settings and send
  a summary email to backup administrators on success and failure.

### Step 7 — Finish and Run

- Click **Finish**.
- Right-click the new job → **Start** to trigger the first run immediately.
- Monitor progress in the **Home** → **Last 24 Hours** view.

---

## Add Veeam ONE (Optional)

Veeam ONE provides monitoring, reporting, and capacity planning for VBR.

### Step 1 — Install Veeam ONE Server

- Run the Veeam ONE installer (from the same ISO or a separate download).
- Select components: **Veeam ONE Server**, **Veeam ONE Web UI**, **Veeam ONE Agent**.
- Point to an SQL instance for the Veeam ONE database.

### Step 2 — Connect to VBR

1. Open the Veeam ONE Web UI (`https://<server>:1239`).
2. Go to **Settings** → **Data Sources** → **Add** → **Veeam Backup & Replication**.
3. Enter the VBR server address and credentials.
4. Veeam ONE imports all jobs, repositories, and infrastructure objects.

### Step 3 — Configure Scope and Alarms

- Assign monitoring scope (specific VMs, jobs, or repositories).
- Review default alarm thresholds (repository free space, job failure count, RPO breach).
- Adjust thresholds to match your environment's baseline.
- Configure alarm notification recipients under **Settings** → **Notifications**.

---

## Validate the Deployment

### Step 1 — Run a SureBackup Job (Recommended)

SureBackup boots VMs from backup in an isolated virtual lab and tests recoverability.

1. Create a **Virtual Lab** under **Backup Infrastructure** → **Virtual Labs**.
2. Create an **Application Group** with the VMs to test.
3. Create a **SureBackup Job** → point to the backup job → assign the Virtual Lab.
4. Run the SureBackup job and verify each VM passes heartbeat and application tests.

### Step 2 — Instant VM Recovery Test

If SureBackup is not licensed:

1. Right-click a backup restore point → **Instant Recovery** → **VMware vSphere VM**.
2. Power on the recovered VM in an isolated network.
3. Confirm the VM boots and the guest OS is accessible.
4. Use **Migrate to Production** or **Stop Publishing** to clean up.

### Step 3 — Repository Health Check

- In VBR Console, right-click the repository → **Check** → confirm no corrupted
  restore points.
- Verify free space is above 20% (below 10% triggers job failures).

### Step 4 — Confirm Notifications

- Send a test email from the SMTP settings to confirm alerting is working.
- Verify Veeam ONE (if deployed) shows no critical alarms.

### Step 5 — Document the Deployment

Record the following for the operations runbook:

- VBR server hostname, IP, and SQL instance
- Service account names
- Repository paths and free capacity
- Backup job names and schedules
- Proxy server hostnames and transport modes
- Contact for backup alerts

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Veeam — Procedures](../operations/procedures/)
- [Veeam — Common Issues](../troubleshooting/common-issues/)
- [Veeam — How It Works](../architecture/how-it-works/)
