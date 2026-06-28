---
tags:
  - operations
  - vcf
  - vmware
---
# VMware Cloud Foundation — Install & Upgrade
![VMware Cloud Foundation — Install & Upgrade](../../../../assets/virtualization-vmware-vmware-cloud-foundation-operations-ins.svg)





```bash

```d2
direction: right

hub: "VMware Cloud Foundation\nOperations" {shape: hexagon}
run_precheck_for_a_workload_domain_u: "Run pre-check for a workload domain upgrade" {shape: rectangle}
retrieve_precheck_results: "Retrieve pre-check results" {shape: rectangle}
check_sddc_manager_logs_for_precheck: "Check SDDC Manager logs for pre-check detail" {shape: rectangle}
check_current_component_versions_in_: "Check current component versions in SDDC Manager" {shape: rectangle}
verify_nsx_version_compatibility: "Verify NSX version compatibility" {shape: rectangle}
verify_sddc_manager_backup_is_curren: "Verify SDDC Manager backup is current" {shape: rectangle}

hub -> run_precheck_for_a_workload_domain_u
hub -> retrieve_precheck_results
hub -> check_sddc_manager_logs_for_precheck
hub -> check_current_component_versions_in_
hub -> verify_nsx_version_compatibility
hub -> verify_sddc_manager_backup_is_curren
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.

## Run pre-check for a workload domain upgrade
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/upgrades \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "DOMAIN",
    "resourceId": "<domain-id>",
    "bundleId": "<bundle-id>",
    "requestType": "PRECHECK"
  }'

## Retrieve pre-check results
curl -sk -u admin:<password> \
  https://localhost/v1/upgrades/<precheck-id> \
  | python3 -m json.tool

## Check SDDC Manager logs for pre-check detail
tail -200 /var/log/vmware/vcf/sddc-manager/vcf-sddc-manager.log | grep -i "precheck"
```
```bash
## Check current component versions in SDDC Manager
curl -sk -u admin:<password> \
  https://localhost/v1/system/inventory/components \
  | python3 -m json.tool

## See also

- [VCF — Health Checks](health-checks/)
- [VCF Troubleshooting — Common Issues](../troubleshooting/common-issues/)
- [VCF — Procedures](procedures/)

## Verify NSX version compatibility
curl -sk -u admin:<password> \
  https://localhost/v1/nsxt-clusters \
  | python3 -m json.tool | grep -E "version|id"
```
```bash
## Verify SDDC Manager backup is current
curl -sk -u admin:<password> \
  https://localhost/v1/backups/tasks \
  | python3 -m json.tool | grep -E "status|completionTimestamp" | head -20

## Trigger an on-demand SDDC Manager backup
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/backups \
  -H "Content-Type: application/json" \
  -d '{"elements": [{"resourceType": "SDDC_MANAGER"}]}'

## Check for existing VM snapshots that must be removed pre-upgrade
curl -sk -u admin:<password> \
  https://localhost/v1/system/inventory/snapshots \
  | python3 -m json.tool
```
```bash
## Test connectivity from SDDC Manager to VMware depot
curl -sk -o /dev/null -w "%{http_code}" https://depot.vmware.com

## Test vCenter reachability
curl -sk -o /dev/null -w "%{http_code}" https://<vcenter-fqdn>/sdk

## Test NSX Manager reachability
curl -sk -o /dev/null -w "%{http_code}" https://<nsx-manager-fqdn>/api/v1/node
```
```bash
## Add environment-specific commands here
```
