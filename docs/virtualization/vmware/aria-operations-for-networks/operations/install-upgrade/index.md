---
tags:
  - aria-networks
  - operations
  - vmware
---
# vRNI Install & Upgrade

```bash
# Check HTTPS is reachable
curl -sk https://aon-platform.example.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200 (redirect to login page)

# SSH to platform to verify services
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra
```
```text
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
```bash
ssh ubuntu@aon-platform.example.local

# Upload the upgrade bundle to the platform
scp VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak ubuntu@aon-platform.example.local:/tmp/

# On Platform VM
sudo /opt/vmware/bin/upgrade.sh /tmp/VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak

# Monitor upgrade progress
sudo tail -f /var/log/vrni-platform/upgrade.log
```
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
```bash
# Revert Platform VM snapshot (this is a destructive operation — confirm before proceeding)
Get-VM "aon-platform-01" | Get-Snapshot -Name "Pre-Upgrade-6.14.0" | Set-VM -SnapShot $_ -Confirm:$false

# After revert, Collectors should auto-reconnect to the older Platform
# If not, re-pair manually:
ssh ubuntu@aon-collector-dc1.example.local
sudo /home/ubuntu/support/pairing.sh
```
