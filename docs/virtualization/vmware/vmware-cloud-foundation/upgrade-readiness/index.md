# VCF Upgrade Readiness

## Overview

Before initiating any VMware Cloud Foundation upgrade, run through this pre-upgrade checklist in full. SDDC Manager will perform its own pre-checks but environmental issues outside its scope must be validated manually.

## Pre-Upgrade Checklist

Work through all items before opening the upgrade wizard in SDDC Manager:

| Check | Command / Location | Pass Criteria |
|---|---|---|
| SDDC Manager health | SDDC Manager UI > Dashboard | All domains green |
| vCenter health | `vSphere Client > Health` | No critical alarms |
| NSX health | NSX Manager > System > Overview | All components up |
| ESXi host health | `esxcli system healthcheck` | No critical hardware alarms |
| Disk space on management VMs | `df -h` on each appliance | < 70% on all mounts |
| NTP sync across all components | `chronyc tracking` | Offset < 5 seconds |
| Snapshot inventory | SDDC Manager UI | No stale snapshots older than 72h |
| Bundle download complete | SDDC Manager > Lifecycle > Bundle Management | Status: Available |

## Bundle Download and Validation

```bash
# SSH into SDDC Manager
ssh vcf@<sddc-manager-fqdn>

# Check available and downloaded bundles
curl -sk -u admin:<password> \
  https://localhost/v1/bundles \
  | python3 -m json.tool

# Trigger bundle download from VMware depot
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/bundles \
  -H "Content-Type: application/json" \
  -d '{"bundleType": "PATCH", "productType": "ESXI"}'

# Check download status
curl -sk -u admin:<password> \
  https://localhost/v1/bundles/<bundle-id> \
  | python3 -m json.tool | grep -E "status|downloadedSize|totalSize"

# List available bundles on local depot
ls -lh /nfs/vmware/vcf/nfs-mount/bundles/
```

## SDDC Manager Pre-Check Execution

```bash
# Run pre-check for a workload domain upgrade
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/upgrades \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "DOMAIN",
    "resourceId": "<domain-id>",
    "bundleId": "<bundle-id>",
    "requestType": "PRECHECK"
  }'

# Retrieve pre-check results
curl -sk -u admin:<password> \
  https://localhost/v1/upgrades/<precheck-id> \
  | python3 -m json.tool

# Check SDDC Manager logs for pre-check detail
tail -200 /var/log/vmware/vcf/sddc-manager/vcf-sddc-manager.log | grep -i "precheck"
```

## Compatibility Matrix Verification

VCF BOM (Bill of Materials) defines the exact component versions per VCF release:

| VCF Version | vCenter | ESXi | NSX | SDDC Manager |
|---|---|---|---|---|
| 5.2 | 8.0 U3 | 8.0 U3 | 4.1.2 | 5.2 |
| 5.1 | 8.0 U2 | 8.0 U2 | 4.1.1 | 5.1 |
| 4.5.2 | 7.0 U3p | 7.0 U3p | 3.2.3 | 4.5.2 |
| 4.4 | 7.0 U3f | 7.0 U3f | 3.2.1 | 4.4 |

```bash
# Check current component versions in SDDC Manager
curl -sk -u admin:<password> \
  https://localhost/v1/system/inventory/components \
  | python3 -m json.tool

# Verify NSX version compatibility
curl -sk -u admin:<password> \
  https://localhost/v1/nsxt-clusters \
  | python3 -m json.tool | grep -E "version|id"
```

## Snapshot and Backup Verification

```bash
# Verify SDDC Manager backup is current
curl -sk -u admin:<password> \
  https://localhost/v1/backups/tasks \
  | python3 -m json.tool | grep -E "status|completionTimestamp" | head -20

# Trigger an on-demand SDDC Manager backup
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/backups \
  -H "Content-Type: application/json" \
  -d '{"elements": [{"resourceType": "SDDC_MANAGER"}]}'

# Check for existing VM snapshots that must be removed pre-upgrade
curl -sk -u admin:<password> \
  https://localhost/v1/system/inventory/snapshots \
  | python3 -m json.tool
```

## Network and Firewall Pre-Checks

Required network connectivity for VCF upgrade operations:

| Source | Destination | Port | Purpose |
|---|---|---|---|
| SDDC Manager | depot.vmware.com | 443 | Bundle download |
| SDDC Manager | All ESXi hosts | 443, 22 | Upgrade orchestration |
| SDDC Manager | vCenter | 443 | vSphere operations |
| SDDC Manager | NSX Manager | 443 | NSX upgrade |
| All ESXi hosts | NFS mount | 2049 | Bundle staging |

```bash
# Test connectivity from SDDC Manager to VMware depot
curl -sk -o /dev/null -w "%{http_code}" https://depot.vmware.com

# Test vCenter reachability
curl -sk -o /dev/null -w "%{http_code}" https://<vcenter-fqdn>/sdk

# Test NSX Manager reachability
curl -sk -o /dev/null -w "%{http_code}" https://<nsx-manager-fqdn>/api/v1/node
```
