---
tags:
  - deployment
  - netbackup
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
install_the_primary_server: "Install the Primary Server" {shape: rectangle}
install_media_servers: "Install Media Servers" {shape: rectangle}
configure_storage_units: "Configure Storage Units" {shape: rectangle}
configure_msdp_media_server_dedup_po: "Configure MSDP (Media Server Dedup Pool)" {shape: rectangle}
add_clients: "Add Clients" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> install_the_primary_server
install_the_primary_server -> install_media_servers
install_media_servers -> configure_storage_units
configure_storage_units -> configure_msdp_media_server_dedup_po
configure_msdp_media_server_dedup_po -> add_clients
add_clients -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

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


```text title="Expected output"
Extracting NetBackup_10.x_LinuxR_x86_64.tar.gz...
NetBackup 10.x Installation Package
Copyright (c) 2023 Veritas Technologies LLC. All rights reserved.

Checking system requirements...
  OS: Red Hat Enterprise Linux 8.5
  Kernel: 5.15.0-1234-generic
  Memory: 16 GB (minimum 8 GB required) ✓
  Disk space: 45 GB available (minimum 20 GB required) ✓

Installing NetBackup components...
  [████████████████████] 100%
  - NetBackup Master Server
  - NetBackup Media Server
  - NetBackup Client

Installation completed successfully.
NetBackup services started:
  nbmaster (PID: 4521)
  nbmediasrv (PID: 4589)

Installation log: /var/log/netbackup/install.log
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `tar: NetBackup_10.x_LinuxR_x86_64.tar.gz: No such file or directory` | Verify the tarball exists in the current directory with `ls -la` and check the exact filename matches. |
    | `./install: Permission denied` | Run `chmod +x install` to make the installer executable before running it. |
    | `Error: Insufficient disk space. Required: 20 GB, Available: 8 GB` | Free up disk space on the target partition or mount the installation directory on a volume with adequate free space. |
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


```text title="Expected output"
UID        PID  PPID C STIME TTY STAT TIME     CMD
root      1234     1 0 08:15 ?   Ss   0:02     /usr/openv/netbackup/bin/bpdbm -d
root      1245     1 0 08:15 ?   Ss   0:01     /usr/openv/netbackup/bin/bprd -d
root      1256     1 0 08:15 ?   Ss   0:03     /usr/openv/netbackup/bin/bpcd -d
root      1267     1 0 08:15 ?   Ss   0:02     /usr/openv/netbackup/bin/nbpem -d
root      1278     1 0 08:15 ?   Ss   0:04     /usr/openv/netbackup/bin/nbstserv -d
root      1289     1 0 08:16 ?   Ss   0:01     /usr/openv/netbackup/bin/vnetd -d
root      1301     1 0 08:16 ?   Ss   0:00     /usr/openv/netbackup/bin/bpjobd -d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bpps: command not found` | Add `/usr/openv/netbackup/bin` to PATH or use the full path `/usr/openv/netbackup/bin/bpps -a`. |
    | `No matching processes found` | Verify NetBackup is installed in `/usr/openv/netbackup` and start daemons with `/usr/openv/netbackup/bin/bpup -start`. |
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


```text title="Expected output"
NetBackup Installation Wizard v9.1.2
=====================================

Select installation type:
1 — NetBackup Master Server
2 — NetBackup Media Server
3 — NetBackup Client
4 — Custom Installation

Enter your selection (1-4): 2

NetBackup Media Server Installation
====================================

Enter the Primary Server FQDN: nbmaster.corp.example.com
Validating connection to nbmaster.corp.example.com... OK
Detected OS: Linux 8.6 (x86_64)
Installation path: /opt/veritas/netbackup
Disk space required: 15 GB
Disk space available: 487 GB

Proceeding with Media Server installation...
Installing NetBackup Media Server 9.1.2
[████████████████████████████] 100%
Installation completed successfully.
Media Server hostname: nbmedia01.corp.example.com
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Enter your selection (1-4): invalid input` | Ensure you enter a single digit (1–4) without extra characters or spaces. |
    | `Validating connection to nbmaster.corp.example.com... FAILED` | Verify the Primary Server FQDN is correct, reachable on the network, and that port 13782 is open between the two hosts. |
    | `Disk space required: 15 GB / Disk space available: 2 GB` | Free up at least 15 GB on the target installation disk before running the installer. |
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


```text title="Expected output"
Adding host media-server-prod.corp.local as media server...
Host media-server-prod.corp.local added successfully.
Master server: primary-nbk.corp.local
Media server role: enabled
Configuration synchronized to catalog.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nbemmcmd: host already exists` | Remove the existing host entry with `nbemmcmd -removehost -machinename <media-server-fqdn>` before re-adding it. |
    | `nbemmcmd: cannot connect to master server` | Verify the Primary Server is running NetBackup services with `bpps -a` and confirm network connectivity to the master server hostname. |
    | `nbemmcmd: invalid machine type 'media'` | Use a valid machine type such as `media`, `client`, or `gateway`; confirm the exact spelling matches your NetBackup version documentation. |
### Step 3 — Verify Connectivity

```bash
# From the Primary Server, test connection to the Media Server
/usr/openv/netbackup/bin/admincmd/bptestbpcd -host <media-server-fqdn>
# Expected output: EXIT STATUS 0
```


```text title="Expected output"
Contacting host <media-server-fqdn> ...
Connected to host <media-server-fqdn>
bptestbpcd: Sending test request to bpcd on host <media-server-fqdn>
bptestbpcd: Received response from bpcd on host <media-server-fqdn>
bptestbpcd: Host <media-server-fqdn> is reachable
EXIT STATUS 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bptestbpcd: Cannot connect to host <media-server-fqdn>` | Verify the Media Server hostname/FQDN is correct and the host is reachable via `ping` or `nslookup`. |
    | `bptestbpcd: bpcd is not running on host <media-server-fqdn>` | Start the NetBackup daemon on the Media Server with `/usr/openv/netbackup/bin/bprd` or verify it is running via `ps -ef | grep bpcd`. |
    | `EXIT STATUS 1` | Check firewall rules allow port 13782 (bpcd) between Primary and Media Server, and verify NetBackup is properly installed on the Media Server. |
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


```text title="Expected output"
Creating storage server configuration...
Storage server: backup-media-01.corp.local
Storage type: PureDisk
Media server: backup-media-01.corp.local
Configuration ID: a7f2c8e1-9d4b-4a2f-b1e6-3c5d9f2a8b4e
Storage server successfully created and added to NetBackup catalog.
Synchronizing with master server...
Sync completed in 12 seconds.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nbdevconfig: command not found` | Ensure the NetBackup bin directory is in your PATH or use the full path `/usr/openv/netbackup/bin/admincmd/nbdevconfig`. |
    | `Error: Storage server already exists` | Verify the media server FQDN is correct and not already registered; use `nbdevconfig -liststs` to check existing storage servers. |
    | `Error: Cannot connect to media server <media-server-fqdn>` | Confirm the media server hostname resolves correctly and NetBackup services are running on it with `nslookup <media-server-fqdn>` and `bpps -l` on the media server. |
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


```text title="Expected output"
Creating disk pool MSDP-Pool-01...
Storage server: media-server-prod-01.corp.local
Disk pool path: /mnt/msdp
Pool type: PureDisk
Disk pool MSDP-Pool-01 created successfully.
Pool ID: 8a2f4c9e-1b3d-47f2-9c5a-6d8e2f1a4b7c
Status: Active
Capacity: 2.5 TB
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Storage server media-server-prod-01.corp.local is not reachable` | Verify the media server hostname is correct and the NetBackup daemons are running with `bpps -a` on the media server. |
    | `Error: Disk pool path /mnt/msdp does not exist or is not writable` | Create the directory with `mkdir -p /mnt/msdp` and ensure the NetBackup user has read/write permissions with `chown -R nbuser:nbgroup /mnt/msdp`. |
    | `Error: Disk pool MSDP-Pool-01 already exists` | Use a unique pool name or remove the existing pool with `nbdevconfig -deletedp -dp_name MSDP-Pool-01` before recreating. |
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


```text title="Expected output"
NetBackup Client Installer v9.1.2.1
=====================================

Select installation type:
1 — NetBackup Server
2 — NetBackup Media Server
3 — NetBackup Master Server
4 — NetBackup Client
5 — Exit

Enter selection [1-5]: 4

NetBackup Client Installation
==============================
Enter Primary Server FQDN: nbmaster.corp.example.com
Validating server connectivity... OK
Installing NetBackup Client 9.1.2.1
[████████████████████████] 100%
Installation completed successfully.
Client ID: 550e8400-e29b-41d4-a716-446655440000
NetBackup services started.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Validating server connectivity... FAILED` | Verify the Primary Server FQDN is correct and reachable from the client (test with `ping` or `nslookup`). |
    | `Permission denied` | Run the installer with `sudo ./install` or as the root user. |
    | `./install: No such file or directory` | Ensure you are in the correct directory where the NetBackup package was extracted and the install script exists. |
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


```text title="Expected output"
NetBackup Database Backup Utility
Version 10.1.0.1 (Build 20230815)

Usage: bpbackupdb [-h] [-d <backup_dir>] [-c] [-v] [-f] [-t <timeout>]

Options:
  -h              Display this help message
  -d <backup_dir> Specify backup directory (default: /usr/openv/netbackup/db/data)
  -c              Compress backup
  -v              Verbose output
  -f              Force backup (skip validation checks)
  -t <timeout>    Set timeout in seconds (default: 3600)

Example: bpbackupdb -d /mnt/backup -c -v

For detailed documentation, visit: https://www.veritas.com/support
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bpbackupdb: command not found` | Verify NetBackup is installed and /usr/openv/netbackup/bin/admincmd is in your PATH, or use the full path with correct permissions. |
    | `Permission denied` | Run the command as root or a user with sudo privileges, as database backup operations require elevated permissions. |
    | `Cannot access backup directory: No such file or directory` | Create the target backup directory first with `mkdir -p /path/to/backup` before running bpbackupdb. |
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

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Netbackup — Procedures](../operations/procedures/)
- [Netbackup — Common Issues](../troubleshooting/common-issues/)
- [Netbackup — How It Works](../architecture/how-it-works/)
