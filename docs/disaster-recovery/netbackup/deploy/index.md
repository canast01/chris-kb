# NetBackup — Initial Deployment

This guide covers deploying Veritas NetBackup from bare metal through a fully
operational backup environment — Primary Server, Media Servers, storage units,
deduplication pool, client onboarding, and policy creation.

---

## Prerequisites

### Hardware and OS

**Primary Server (Master Server)**

- RHEL 8/9 or Windows Server 2019/2022, 64-bit
- Minimum 8 vCPU, 32 GB RAM; 64 GB recommended for large environments
- 500 GB+ for the NetBackup catalog (grows with job history and image metadata)
- Separate fast volume for catalog recommended (SSD/NVMe)

**Media Server**

- RHEL 8/9 or Windows Server 2019/2022, 64-bit
- 8 vCPU, 16 GB RAM; sized by concurrent stream count
- Storage for MSDP dedup pool (separate high-throughput volume)

### Network Requirements

- All hosts must be FQDN-resolvable in both forward and reverse DNS
- Primary and Media Servers must resolve each other by FQDN
- Clients must resolve the Primary Server by FQDN

### Network Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 1556 | TCP | PBX (NetBackup process broker — all communications) |
| 13724 | TCP | vnetd (legacy daemon, some clients still require this) |
| 13782 | TCP | bpcd (client-side daemon for job initiation) |
| 443 | TCP | NetBackup Web UI (HTTPS) |
| 10082 | TCP | NetBackup API (REST) |
| 1556 | TCP | Media Server to Primary Server |

Ensure port 1556 is open bidirectionally between all NetBackup hosts.

### Service Account

- **Linux**: NetBackup services run as `root` by default; a non-root service
  user can be configured post-install but requires additional setup.
- **Windows**: A local or domain service account with Local Administrator rights;
  the installer assigns required privileges.

### Pre-Install Checklist

- [ ] Hostname set to FQDN on all servers (`hostnamectl set-hostname <fqdn>`)
- [ ] `/etc/hosts` entries for Primary and Media Servers (belt-and-suspenders for DNS)
- [ ] NTP synchronized on all servers
- [ ] SELinux set to `permissive` or configured with NetBackup policy
- [ ] Sufficient `/tmp` space (10 GB+) for installer extraction

---

## Install the Primary Server

### Step 1 — Download the Package

1. Log in to the Veritas entitlement portal.
2. Download the NetBackup 10.x package:
   - Linux: `NetBackup_10.x_LinuxR_x86_64.tar.gz`
   - Windows: `NetBackup_10.x_Win.exe`
3. Transfer to the Primary Server.

### Step 2 — Linux Installation

```bash
# Extract the tarball
tar -xzf NetBackup_10.x_LinuxR_x86_64.tar.gz
cd NetBackup_10.x_LinuxR_x86_64/

# Run the installer
./install
```

At the interactive prompts:

- Select **1** → NetBackup Primary Server
- Confirm the FQDN when prompted for the master server name
- Accept the default install path (`/usr/openv`) or specify a custom path
- Enter the license key when prompted (or apply later via the web UI)

### Step 3 — Windows Installation

1. Run `setup.exe` as local administrator.
2. Select **Custom** installation.
3. Choose **NetBackup Primary Server**.
4. Enter the server FQDN when prompted.
5. Accept the default install directory or change to a data volume.
6. Complete the wizard and wait for installation to finish.

### Step 4 — Verify Services (Linux)

```bash
# Check all NetBackup daemons are running
/usr/openv/netbackup/bin/bpps -a

# Key daemons to verify:
# bpdbm   — database manager
# bprd    — request daemon
# bpcd    — client daemon (runs on primary too)
# nbpem   — policy execution manager
# nbstserv — storage server
```

### Step 5 — Access the Web UI

Browse to `https://<primary-server-fqdn>/webui` and log in as the local admin
or domain account. The web UI is the primary management interface from NBU 9+.

---

## Install Media Servers

### Step 1 — Run the Installer on the Media Server

Follow the same download and extraction steps as for the Primary Server.

On Linux:

```bash
./install
# Select: 2 — NetBackup Media Server
# Enter the Primary Server FQDN when prompted
```

On Windows, choose **NetBackup Media Server** in the setup wizard and enter
the Primary Server hostname.

### Step 2 — Authorize the Media Server on the Primary

After the Media Server installation completes, it must be authorized on the
Primary Server before it can be used.

Via web UI: **Hosts** → **Host Properties** → the Media Server appears in a
pending state → click **Approve**.

Via CLI:

```bash
# Run on the Primary Server
/usr/openv/netbackup/bin/admincmd/nbemmcmd -addhost \
  -machinename <media-server-fqdn> \
  -machinetype media \
  -masterserver <primary-server-fqdn>
```

### Step 3 — Verify Connectivity

```bash
# From the Primary Server, test connection to the Media Server
/usr/openv/netbackup/bin/admincmd/bptestbpcd -host <media-server-fqdn>
# Expected output: EXIT STATUS 0
```

---

## Configure Storage Units

Storage units define how and where NetBackup writes backup data.

### Step 1 — Open Storage Configuration

Web UI → **Storage** → **Storage Units** → **+ Add**.

### Step 2 — BasicDisk Storage Unit

1. **Storage unit type**: Disk
2. **Disk type**: BasicDisk
3. **Media server**: select the Media Server that owns this path
4. **Absolute pathname**: enter the local path (e.g. `/mnt/backup`) or
   Windows path (`D:\NetBackupData`)
5. Set **Maximum concurrent write drives** (typically 4–8 per storage unit)
6. Set **On demand only** if this unit should only be used when explicitly
   selected by a policy

### Step 3 — Verify Free Space

Ensure the target path has sufficient free space before proceeding. NetBackup
will fail jobs when disk utilization exceeds the high-water mark (default 98%).

Adjust the high-water mark under the storage unit **Advanced** settings to 85–90%
to give operational headroom.

---

## Configure MSDP (Media Server Dedup Pool)

MSDP provides inline deduplication and is the recommended storage type for
disk-based backups.

### Step 1 — Create the MSDP Storage Server

```bash
# Run on the Primary Server
/usr/openv/netbackup/bin/admincmd/nbdevconfig -creatests \
  -storage_server <media-server-fqdn> \
  -stype PureDisk \
  -media_server <media-server-fqdn>
```

Or via web UI: **Storage** → **Storage Servers** → **+ Add** →
select **Media Server Deduplication Pool**.

### Step 2 — Create the Dedup Pool

```bash
/usr/openv/netbackup/bin/admincmd/nbdevconfig -createdp \
  -stype PureDisk \
  -storage_server <media-server-fqdn> \
  -dp_name MSDP-Pool-01 \
  -dp_path /mnt/msdp
```

The `/mnt/msdp` path should be a dedicated high-throughput volume. Do not share
this volume with other data.

### Step 3 — Set Catalog Backup Location

The MSDP catalog (dedup metadata) must be protected by a catalog backup policy.
Configure the catalog backup path under:

Web UI → **Primary Server** → **NetBackup Catalog** → set the catalog backup path
to a separate volume or remote NFS share.

### Step 4 — Create MSDP Storage Unit

Web UI → **Storage** → **Storage Units** → **+ Add**:

- Type: **Disk**
- Disk type: **PureDisk (MSDP)**
- Storage server: select the MSDP storage server created above
- Disk pool: select `MSDP-Pool-01`

---

## Add Clients

Clients are the hosts being backed up.

### Step 1 — Add a Client via Web UI

Web UI → **Hosts** → **Add Client** → enter the hostname, OS, and policy type.

For VMware: Web UI → **Virtual Machines** → **Add VMware Server** → enter
vCenter credentials.

### Step 2 — Push Client Software (Windows / Linux)

From the Primary Server web UI:

1. Go to **Hosts** → **Add Client**.
2. Enter the target hostname.
3. Select **Push installation** and provide credentials.
4. NetBackup transfers and installs the client software remotely.

### Step 3 — Manual Client Installation (Linux)

If the Primary Server cannot reach the client directly:

```bash
# On the client, run the installer from a copied package
./install
# Select: 4 — NetBackup Client
# Enter the Primary Server FQDN
```

After install, verify the client is visible under **Hosts** in the web UI.

---

## Create Backup Policies

Policies define what is backed up, how, and when.

### Step 1 — Open Policy Wizard

Web UI → **Protection** → **Policies** → **+ Add Policy**.

### Step 2 — Policy Type

Select the policy type that matches the workload:

| Policy Type | Use Case |
|-------------|----------|
| Standard | UNIX/Linux file system |
| MS-Windows | Windows file system |
| VMware | Agentless VMware VM backup |
| Oracle | Oracle DB backup via RMAN |
| MS-SQL-Server | SQL Server backup |
| NDMP | NAS/filer backup |

### Step 3 — Clients Tab

Add the hostnames of the clients to protect. For VMware policies, add the
vCenter or ESXi host and filter by VM name, folder, tag, or datastore.

### Step 4 — Backup Selections Tab

- **Standard / MS-Windows**: add file paths or use directives (e.g. `ALL_LOCAL_DRIVES`)
- **VMware**: the selection defaults to all VMs under the added vCenter; refine with
  queries (e.g. tag = `backup:daily`)

### Step 5 — Schedules Tab

Add at least two schedule entries:

1. **Full** — Type: Full, Frequency: Weekly, Window: Sunday 20:00–06:00
2. **Incremental** — Type: Differential Incremental, Frequency: Daily,
   Window: Mon–Sat 22:00–06:00

Set **Retention** on each schedule:
- Full: 4 weeks (or longer per compliance requirements)
- Incremental: 2 weeks

### Step 6 — Storage

Assign the MSDP storage unit (or BasicDisk as a fallback) to the policy.

---

## Validate the Deployment

### Step 1 — Run a Manual Backup

Web UI → **Protection** → **Policies** → select the policy →
**Actions** → **Manual Backup**.

Select **Full** for the first run. Monitor the job in
**Activity Monitor** → **Jobs**.

A successful job completes with **Status: 0 (the requested operation was
successfully completed)**.

### Step 2 — Review Job Details

Click the completed job → **Details** → review:

- Data protected (KB/MB/GB)
- Deduplication ratio (on MSDP jobs)
- Any skipped or missed files
- Total elapsed time

### Step 3 — Test a Restore

1. Web UI → **Recovery** → **NetBackup Catalog** → search for the client.
2. Browse the backup image and select a test file or directory.
3. Restore to an alternate path.
4. Verify the restored file is accessible and uncorrupted.

### Step 4 — Verify Catalog Backup

The NetBackup catalog must be protected by a catalog backup policy. Confirm
the catalog backup policy exists and ran successfully:

```bash
/usr/openv/netbackup/bin/admincmd/bpbackupdb
```

A failed catalog backup is a critical risk; the catalog is required for all restores.

### Step 5 — Document the Deployment

Record the following for the operations runbook:

- Primary Server FQDN and IP
- Media Server FQDNs and storage unit paths
- MSDP pool path and capacity
- Policy names, types, schedules, and retention settings
- Client list with OS types
- Catalog backup path and schedule
- Web UI admin account and password vault location
