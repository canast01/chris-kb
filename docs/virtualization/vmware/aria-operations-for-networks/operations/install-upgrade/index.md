# Aria Operations for Networks — Install and Upgrade

```
┌──────────── Aria Networks Upgrade Sequence ────────────────────────────────────┐
│                                                                                 │
│  Pre-upgrade                                                                    │
│  ├── config backup: GET /api/ni/settings/backup ──► .tar.gz                    │
│  └── snapshot Platform VM (vSphere)                                             │
│       │                                                                         │
│       ▼                                                                         │
│  Step 1: Upgrade Platform VM  (CRITICAL: always first)                          │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  UI: Settings ► Upgrade ► upload .pak bundle ► Install                  │   │
│  │  CLI: sudo /opt/vmware/bin/upgrade.sh <bundle.pak>                      │   │
│  │  Duration: 15–30 min (UI unavailable during upgrade)                    │   │
│  └───────────────────────────────────────┬──────────────────────────────────┘  │
│                                          │ verify: systemctl + version API      │
│       ▼                                  ▼                                      │
│  Step 2: Upgrade Collector VMs (Platform must be healthy first)                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  UI: Settings ► Collectors ► Upgrade All  OR  per-collector              │  │
│  │  Each Collector restarts ► auto-reconnects ► flow ingestion resumes     │   │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  Rollback: revert Platform VM snapshot ► Collectors auto-reconnect              │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Infrastructure Requirements

| Requirement | Minimum | Notes |
|---|---|---|
| vCenter Server | 7.0 U3 | 8.0 recommended; check interop matrix |
| NSX-T Manager | 3.2 | 4.x supported in AON 6.13+ |
| ESXi | 7.0 U3 | For hosting Platform and Collector VMs |
| DNS | Forward + reverse resolution for all AON VMs | Mandatory — AON will fail to start without PTR records |
| NTP | All AON VMs time-synced to same NTP source | Time drift causes flow correlation failures |
| IP addressing | Static IPs for Platform VM and each Collector VM | DHCP not supported |

### Version Compatibility Matrix

| AON Version | NSX-T | vCenter | NSX-V | Notes |
|---|---|---|---|---|
| 6.11.x | 3.0, 3.1, 3.2 | 7.0 | 6.4 | EOL |
| 6.12.x | 3.1, 3.2, 4.0 | 7.0, 8.0 | 6.4 | EOL |
| 6.13.x | 3.2, 4.0, 4.1 | 7.0, 8.0 | Not supported | NSX-V dropped |
| 6.14.x | 4.0, 4.1, 4.2 | 7.0 U3+, 8.0, 8.0 U2 | Not supported | Current GA |

Always verify on the [VMware Interoperability Matrix](https://interopmatrix.vmware.com/) before deploying.

### Required OVA Files

| Component | OVA Name (example) |
|---|---|
| Platform VM | `VMware-Aria-Operations-for-Networks-6.14.0-Platform.ova` |
| Collector VM | `VMware-Aria-Operations-for-Networks-6.14.0-Collector.ova` |

OVAs are downloaded from [Broadcom Customer Connect](https://customerconnect.broadcom.com/) under My Downloads → Aria Operations for Networks.

## Platform VM Deployment

### Deploy OVA via vCenter UI

1. vCenter → Actions → Deploy OVF Template
2. Select the Platform OVA file
3. Set VM name (e.g., `aon-platform-01`) and target inventory location
4. Select the target compute cluster and datastore
5. Select the management network portgroup
6. Configure OVF properties:

| Property | Value |
|---|---|
| IP Address | `10.10.10.50` |
| Subnet Mask | `255.255.255.0` |
| Default Gateway | `10.10.10.1` |
| DNS Server 1 | `10.10.0.1` |
| DNS Server 2 | `10.10.0.2` |
| Hostname (FQDN) | `aon-platform.corp.local` |
| NTP Server | `ntp.corp.local` |
| Admin Password | (set initial password) |

7. Power on the VM. First boot takes 10–15 minutes for service initialization.

### Verify Platform VM Is Ready

```bash
# Check HTTPS is reachable
curl -sk https://aon-platform.corp.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200 (redirect to login page)

# SSH to platform to verify services
ssh ubuntu@aon-platform.corp.local
sudo systemctl status vrni-platform nginx cassandra
```

### Initial Setup Wizard

Navigate to `https://aon-platform.corp.local` in a browser.

1. **Login**: admin@local / (password set during OVA deployment)
2. **License key**: Enter the AON license key obtained from Broadcom
3. **Network config review**: Verify hostname, IP, DNS, NTP shown match what was set
4. **Accept EULA**
5. Click **Finish** — platform is now ready for data sources

## Collector VM Deployment

### Generate Pairing Key

Before deploying the Collector OVA, generate a pairing key from the Platform UI:

Settings → Accounts and Data Sources → Collectors → Add Collector → Generate Pairing Key

Copy the pairing key — it is a long random string. It expires after 24 hours if unused.

### Deploy Collector OVA

1. vCenter → Deploy OVF Template → select Collector OVA
2. Set VM name (e.g., `aon-collector-dc1`) and target location
3. Configure OVF properties:

| Property | Value |
|---|---|
| IP Address | `10.10.10.51` |
| Subnet Mask | `255.255.255.0` |
| Default Gateway | `10.10.10.1` |
| DNS Server | `10.10.0.1` |
| Hostname (FQDN) | `aon-collector-dc1.corp.local` |
| NTP Server | `ntp.corp.local` |
| Platform IP/FQDN | `aon-platform.corp.local` |
| Pairing Key | (paste from UI) |

4. Power on the Collector VM. First boot takes 5–10 minutes.

### Verify Collector Pairing

```bash
# SSH to Collector and check pairing status
ssh ubuntu@aon-collector-dc1.corp.local
sudo systemctl status ni-collector
sudo journalctl -u ni-collector -n 50

# From Platform UI:
# Settings → Accounts and Data Sources → Collectors
# Collector should show Status: Connected
```

If the Collector does not appear as Connected within 10 minutes, check:
1. TCP 443 from Collector to Platform is open
2. DNS resolves Platform FQDN from the Collector
3. Pairing key was not expired or already used

### Add vCenter as a Data Source

Settings → Accounts and Data Sources → Add Source → vCenter Server

| Field | Value |
|---|---|
| vCenter IP/FQDN | `vcenter.corp.local` |
| Username | `svc-aon@vsphere.local` |
| Password | — |
| Collector | Select the paired Collector |
| Nickname | `vCenter-Production` |

Click **Validate** to test credentials, then **Submit**.

### Add NSX-T Manager as a Data Source

Settings → Accounts and Data Sources → Add Source → NSX-T Manager

| Field | Value |
|---|---|
| NSX-T Manager IP/FQDN | `nsxmgr.corp.local` |
| Username | `svc-aon` |
| Password | — |
| Collector | Select the paired Collector |
| Nickname | `NSX-T-Production` |

NSX-T data source auto-discovers VNIs, segments, and DFW rules within the first sync cycle (10 minutes).

## Upgrade Process

### Upgrade Order — Critical

**Always upgrade Platform VM before Collector VMs.** A newer Collector cannot communicate with an older Platform. Upgrading Collectors first will cause them to disconnect and lose flow data during the window.

```
Correct order:
1. Snapshot Platform VM
2. Upgrade Platform VM
3. Verify Platform is healthy
4. Snapshot each Collector VM
5. Upgrade each Collector VM (one at a time or in parallel if environment allows)
6. Verify all Collectors reconnect
7. Delete snapshots (after 48-hour burn-in)
```

### Prepare for Upgrade

```bash
# 1. Take config backup
TOKEN=$(curl -sk -X POST "https://aon.corp.local/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk "https://aon.corp.local/api/ni/settings/backup" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  --output "aon-backup-pre-upgrade-$(date +%Y%m%d).tar.gz"

# 2. Take vSphere snapshot of Platform VM (via PowerCLI or vCenter UI)
# PowerCLI:
Get-VM "aon-platform-01" | New-Snapshot -Name "Pre-Upgrade-6.14.0" -Description "Before AON upgrade to 6.14.0"

# 3. Note current version
curl -sk "https://aon.corp.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool
```

### Upgrade Platform VM

**UI method:**

Settings → Infrastructure → Upgrade → Browse → select Platform upgrade bundle → Install

The upgrade bundle file is a `.pak` file downloaded from Broadcom.

**CLI method (if UI upgrade fails):**

```bash
ssh ubuntu@aon-platform.corp.local

# Upload the upgrade bundle to the platform
scp VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak ubuntu@aon-platform.corp.local:/tmp/

# On Platform VM
sudo /opt/vmware/bin/upgrade.sh /tmp/VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak

# Monitor upgrade progress
sudo tail -f /var/log/vrni-platform/upgrade.log
```

Platform will restart services during upgrade. Expect 15–30 minutes of downtime. The UI will be unavailable during this period.

### Verify Platform After Upgrade

```bash
# Check version
curl -sk "https://aon.corp.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool

# Check all services are running
ssh ubuntu@aon-platform.corp.local
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Check Collectors re-connected (they should reconnect automatically)
curl -sk "https://aon.corp.local/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys,json
for c in json.load(sys.stdin).get('results',[]):
    print(c.get('nickname',''), c.get('status',''))
"
```

### Upgrade Collector VMs

Settings → Accounts and Data Sources → Collectors → Select Collector → Upgrade

Alternatively, push upgrade from the Platform UI to all Collectors simultaneously:

Settings → Infrastructure → Upgrade → Upgrade All Collectors

Collectors will restart their services. Expect 5–10 minutes per Collector. Flow data ingestion will pause for each Collector during its upgrade.

### Rollback

If the upgrade fails or causes issues:

```bash
# Revert Platform VM snapshot (this is a destructive operation — confirm before proceeding)
Get-VM "aon-platform-01" | Get-Snapshot -Name "Pre-Upgrade-6.14.0" | Set-VM -SnapShot $_ -Confirm:$false

# After revert, Collectors should auto-reconnect to the older Platform
# If not, re-pair manually:
ssh ubuntu@aon-collector-dc1.corp.local
sudo /home/ubuntu/support/pairing.sh
```

Snapshot-based rollback restores flow data to the snapshot point. Config changes made between snapshot and upgrade are lost.
