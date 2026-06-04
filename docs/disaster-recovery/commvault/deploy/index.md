# CommVault — Initial Deployment

This guide covers deploying a CommVault CommCell environment from scratch — from
CommServe installation through MediaAgent configuration, client onboarding, policy
creation, and first-backup validation.

---

## Prerequisites

### Hardware and OS

- Windows Server 2019 or 2022, 64-bit (CommServe is Windows-only)
- Minimum 8 vCPU, 16 GB RAM for CommServe; 32 GB recommended in production
- 200 GB+ free disk for CommServe DB and working space (SSD strongly recommended)
- MediaAgent servers: Windows or Linux, sized by throughput requirements

### SQL Server

- SQL Server 2016, 2017, 2019, or 2022 (Standard or Enterprise)
- SQL Express is not supported for CommServe in production
- CommVault creates its own database (`CommServ`); the installer handles schema
- The CommServe service account needs `sysadmin` on the SQL instance during install,
  `db_owner` ongoing

### Java Runtime

- Java JRE 11+ is bundled with the CommVault installer; no separate install required
  on modern releases
- Legacy environments may require a manual JRE installation if the bundled version
  fails a compatibility check

### Service Account

- Create a dedicated domain account (e.g. `SVC-CommVault`)
- Grant it **Local Administrator** on the CommServe server
- Grant it **Local Administrator** on all MediaAgent and client servers
- The account is used for the CommVault services and push installation

### Network Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 8400 | TCP | CommServe communication (clients and MediaAgents) |
| 8401 | TCP | CommServe GUI/Console to server |
| 8403 | TCP | Web Console (Command Center) HTTPS |
| 8600–8699 | TCP | Client data transfer to MediaAgent |
| 443 | TCP | Cloud storage connectors, Command Center |
| 1433 | TCP | SQL Server access from CommServe |

Ensure all firewall rules are in place before starting installation.

### Storage Planning

- CommServe DB size scales with the number of clients and jobs; allow 50–100 GB
  initially, growing over time
- MediaAgent index cache: 128 GB+ per MediaAgent (SSD preferred)
- Deduplicated store (DDB) requires fast I/O; use SSD or NVMe for DDB volumes

---

## Install CommServe (Primary Server)

### Step 1 — Download the Installer

1. Log in to the CommVault Software Store (`cloud.commvault.com`).
2. Download the latest `CommVault_11.x_Windows.exe` or the full installer package.
3. Copy to the CommServe target server.

### Step 2 — Launch Setup

1. Run `Setup.exe` as a local administrator.
2. Select **Install packages on this computer**.
3. Choose **CommServe** from the component list.

### Step 3 — CommCell Configuration

- **CommCell name**: enter a unique name (e.g. `COMMCELL-PROD`). This cannot be
  changed after installation.
- **CommServe host**: the FQDN of this server. Must be DNS-resolvable from all
  clients.
- **SQL instance**: enter `SERVER\INSTANCE` or use the default local instance.
- The installer creates the `CommServ` database and runs schema migrations.

### Step 4 — Service Account

- Enter the `DOMAIN\SVC-CommVault` account and password.
- The installer grants the account required SQL and local rights automatically.

### Step 5 — Firewall Exceptions

- The installer prompts to create Windows Firewall exceptions for ports 8400, 8401,
  8403, and the data transfer range (8600–8699).
- Accept, or configure manually if a third-party firewall is in use.

### Step 6 — Complete Installation

- Click **Finish** and wait 20–30 minutes for the CommServe to initialize.
- After completion, open the **CommCell Console** (Java-based) or browse to
  `https://<commserve>:8403` for the **Command Center** (web UI).
- Verify the CommServe service is running: `CommVault Communications Service`
  in `services.msc`.

---

## Install MediaAgent

MediaAgents manage data movement between clients and storage libraries.

### Step 1 — Push Install from CommCell Console

1. In the CommCell Console, go to **Client Computers** → right-click →
   **Install Software**.
2. Choose **Install on a new client**.
3. Enter the target hostname and credentials (local admin account).

### Step 2 — Component Selection

- Select **MediaAgent** as the package to install.
- Optionally add **File System Agent** if this server will also be backed up.

### Step 3 — Point to CommServe

- The installer pre-fills the CommServe hostname from the console session.
- Confirm the hostname is the FQDN.

### Step 4 — Registration

- The MediaAgent registers with the CommCell automatically after install.
- Verify it appears under **Storage Resources** → **MediaAgents** in the console.
- Status should show **Ready**.

### Step 5 — Index Cache Location

- Right-click the MediaAgent → **Properties** → **Index Cache**.
- Set the index cache path to a fast local volume (128 GB+ SSD).
- Restart the MediaAgent services after changing the path.

---

## Configure a Storage Library

Libraries define the physical or cloud storage attached to a MediaAgent.

### Step 1 — Open Library Configuration

In CommCell Console → **Storage Resources** → **Libraries** → right-click →
**Add Library**.

### Step 2 — Library Types

| Type | When to Use |
|------|-------------|
| Disk Library | NAS share, SAN LUN, or local path on MediaAgent |
| Cloud Library | AWS S3, Azure Blob, Google Cloud Storage, etc. |
| Tape Library | Physical or virtual tape (VTL) |

### Step 3 — Disk Library (Most Common)

1. Select **Disk Library**.
2. Enter the MediaAgent that owns this library.
3. Enter the mount path (e.g. `E:\CommVaultData` or UNC `\\NAS\CVBackups`).
4. For NAS paths, enter credentials with write access.
5. Set the **Low water mark** (minimum free space before jobs are held).

### Step 4 — Cloud Library

1. Select **Cloud Library** → choose the provider.
2. Enter cloud credentials (access key, secret, or storage account key).
3. Enter bucket/container name and region.
4. Set a **Served by MediaAgent** — all data flows through this server.

### Step 5 — Enable Deduplication (Optional but Recommended)

- On a Disk Library, enable **Software Deduplication** under the mount path
  properties.
- Set the Deduplication Database (DDB) location to a fast SSD volume.
- DDB location should not be on the same volume as backup data.

---

## Install Client Agents

Clients are the servers, VMs, or workstations being protected.

### Step 1 — Push Installation

1. CommCell Console → right-click **Client Computers** →
   **Install Software** → **Install on a new client**.
2. Enter the target hostname and admin credentials.
3. Select the agent package:
   - **Windows File System Agent** — for Windows servers
   - **Linux File System Agent** — for Linux servers
   - **Virtual Server Agent (VSA)** — for VMware/Hyper-V protection
   - **SQL Server Agent** — for application-consistent SQL backups
   - **Exchange Agent**, **Oracle Agent**, etc. as needed

### Step 2 — VMware Virtual Server Agent

For VMware backups, install VSA on a proxy server (Windows or Linux):

1. Select **Virtual Server Agent** and enter the proxy hostname.
2. After install, configure the vCenter under
   **Virtualization** → **VMware** → **Add vCenter**.
3. Enter vCenter credentials (read + snapshot permissions minimum).

### Step 3 — Verify Client Registration

After installation, the client appears under **Client Computers** in the console
with status **Ready**.

---

## Create a Storage Policy

Storage policies define how data is moved to and between storage targets.

### Step 1 — New Storage Policy

CommCell Console → **Policies** → **Storage Policies** → right-click →
**New Storage Policy**.

### Step 2 — Policy Configuration

- **Policy name**: e.g. `SP-Daily-Disk-Tape`
- **Primary copy** (required): select the disk library for initial backup landing
  target. Set retention (e.g. 30 days / 2 cycles).
- **Secondary copy** (optional): select a tape library or cloud library for
  long-term retention. Set retention independently (e.g. 1 year).

### Step 3 — Deduplication and Compression

- Enable **Software Compression** on the primary copy unless the library has
  hardware compression.
- Enable **Client-side Deduplication** if clients have sufficient CPU and the
  network is a bottleneck.

### Step 4 — Copy Precedence

- Set secondary copy jobs to run at a defined time (e.g. 02:00 daily) to prevent
  tape/cloud operations from competing with backup windows.

---

## Create a Subclient and Backup Schedule

Subclients define what data is protected and when.

### Step 1 — Locate the Client

CommCell Console → **Client Computers** → expand the client →
**File System** (or the relevant agent) → **defaultBackupSet** →
right-click **default** (subclient) → **Properties**.

### Step 2 — Configure Content

- Go to the **Content** tab.
- Add the paths to protect (e.g. `C:\`, `D:\Data`, or specific folders).
- Add exclusions as needed (temp files, log directories, OS folders already
  covered by system state).

### Step 3 — Assign Storage Policy

- Under the **Storage Device** tab, select the storage policy created above.
- Select the appropriate copy (usually the primary disk copy).

### Step 4 — Set the Schedule

- Under the **Schedules** tab, click **Add**.
- Create a **Full** schedule (e.g. weekly on Sunday at 21:00).
- Create an **Incremental** schedule (e.g. daily Monday–Saturday at 22:00).
- Enable **Automatic Schedule** to let CommVault manage catch-up runs.

### Step 5 — Additional Subclients

For complex clients, create multiple subclients with different content paths,
storage policies, or schedules. For example, separate a database volume from
a general file system volume to assign different retention.

---

## Validate the Deployment

### Step 1 — Run a Full Backup

1. Right-click the subclient → **Backup** → **Full**.
2. Monitor progress in **Job Controller** (CommCell Console) or **Job History**
   in Command Center.
3. A successful job ends in **Committed** state. Any other terminal state
   (Failed, Killed) indicates a problem to investigate.

### Step 2 — Review Job Details

- Open the completed job → **View Logs** to inspect the detail log.
- Check data protected (GB), transfer rate, and deduplication ratio.
- Confirm the storage policy copy shows the data in **Storage Policy Copy Details**.

### Step 3 — Test Restore

1. Right-click the client → **Browse and Restore** → browse to a known file.
2. Restore to an alternate path (e.g. `C:\RestoreTest\`) to avoid overwriting
   live data.
3. Verify the file is intact and accessible after restore.

### Step 4 — Confirm Alerts

- Go to **Alerts** → **Add Alert** in CommCell Console.
- Create alerts for: job failure, disk library low space, MediaAgent offline.
- Set the delivery method to email (SMTP settings under
  **Control Panel** → **Email Server**).
- Trigger a test alert to verify email delivery.

### Step 5 — Document the Deployment

Record the following for the operations runbook:

- CommServe hostname, IP, SQL instance, CommCell name
- MediaAgent hostnames and storage library paths
- Storage policy names and retention settings
- Client list with agent types and subclient content paths
- Backup schedule summary
- Alert recipients and SMTP server
