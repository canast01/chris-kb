# Aria Operations for Networks — Install and Upgrade


<div class="kb-summary">
Install and Upgrade reference covering Prerequisites, Platform VM Deployment, Upgrade Process.
</div>

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

OVAs are downloaded from [Broadcom Support Portal](https://support.broadcom.com/) under My Downloads → Aria Operations for Networks.

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
| Hostname (FQDN) | `aon-platform.example.local` |
| NTP Server | `ntp.example.local` |
| Admin Password | (set initial password) |

7. Power on the VM. First boot takes 10–15 minutes for service initialization.

### Verify Platform VM Is Ready

```bash
# Check HTTPS is reachable
curl -sk https://aon-platform.example.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200 (redirect to login page)

# SSH to platform to verify services
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra
```
```
┌─────────────────────────────────────── vRNI Install & Upgrade ────────────────────────────────────────┐
│                                                                                                       │
│  OVA deployment, PAK upgrade process, and pre-requisites for Aria Operations for Networks.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Pre-Requisites                │  │             OVA Deployment Steps            │   │
│   │         vSphere 6.7+ for platform VM         │  │          1. Download OVA from depot         │   │
│   │         DNS A + PTR records created          │  │         2. Deploy via vSphere client        │   │
│   │             NTP server reachable             │  │          3. Set IP/DNS/NTP in VAMI          │   │
│   │         Network ports opened (docs)          │  │           4. Register license key           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pre-requisites must be met before OVA deploy; PAK upgrade follows same sequence.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              PAK Upgrade Steps               │  │               Collector Deploy              │   │
│   │           1. Snapshot platform VM            │  │             Deploy collector OVA            │   │
│   │          2. Download PAK from depot          │  │         Register to platform via UI         │   │
│   │            3. Upload PAK via VAMI            │  │        Set IPFIX target to collector        │   │
│   │            4. Monitor upgrade log            │  │            Validate flow receipt            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere cluster for platform + collector VMs; NFS/vSAN datastore; 1GbE+ management NIC               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA                 = Open Virtualization Appliance; vRNI platform/collector package                 │
│  PAK File            = Product Activation Key file; contains upgrade binaries for vRNI                │
│  VAMI                = Virtual Appliance Mgmt Interface on port 5480; used for upgrade                │
│  Depot               = VMware Customer Connect or LCM depot for PAK download                          │
│  DNS PTR             = Reverse DNS record; required for vRNI hostname resolution                      │
│  NTP                 = Time sync; mismatched clocks cause flow correlation failures                   │
│  License Key         = vRNI entitlement; applied in VAMI after first boot                             │
│  Collector OVA       = Separate lightweight VM for remote segment flow collection                     │
│  IPFIX Target        = Device config pointing flow export to the collector IP                         │
│  Snapshot            = vSphere VM checkpoint taken before upgrade for rollback                        │
│  Upgrade Log         = Available in VAMI during PAK apply; shows progress and errors                  │
│  Port Requirements   = UDP 2055, TCP 443, TCP 5480; documented in VMware port guide                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

### Prepare for Upgrade

```bash
# 1. Take config backup
TOKEN=$(curl -sk -X POST "https://aon.example.local/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk "https://aon.example.local/api/ni/settings/backup" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  --output "aon-backup-pre-upgrade-$(date +%Y%m%d).tar.gz"

# 2. Take vSphere snapshot of Platform VM (via PowerCLI or vCenter UI)
# PowerCLI:
Get-VM "aon-platform-01" | New-Snapshot -Name "Pre-Upgrade-6.14.0" -Description "Before AON upgrade to 6.14.0"

# 3. Note current version
curl -sk "https://aon.example.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool
```

### Upgrade Platform VM

**UI method:**

Settings → Infrastructure → Upgrade → Browse → select Platform upgrade bundle → Install

The upgrade bundle file is a `.pak` file downloaded from Broadcom.

**CLI method (if UI upgrade fails):**

```bash
ssh ubuntu@aon-platform.example.local

# Upload the upgrade bundle to the platform
scp VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak ubuntu@aon-platform.example.local:/tmp/

# On Platform VM
sudo /opt/vmware/bin/upgrade.sh /tmp/VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak

# Monitor upgrade progress
sudo tail -f /var/log/vrni-platform/upgrade.log
```

Platform will restart services during upgrade. Expect 15–30 minutes of downtime. The UI will be unavailable during this period.

### Verify Platform After Upgrade

```bash
# Check version
curl -sk "https://aon.example.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool

# Check all services are running
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Check Collectors re-connected (they should reconnect automatically)
curl -sk "https://aon.example.local/api/ni/collectors" \
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
ssh ubuntu@aon-collector-dc1.example.local
sudo /home/ubuntu/support/pairing.sh
```

Snapshot-based rollback restores flow data to the snapshot point. Config changes made between snapshot and upgrade are lost.
