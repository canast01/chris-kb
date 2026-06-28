---
tags:
  - troubleshooting
  - aria-operations-for-networks
  - vmware
  - known-issues
---
# VMware Aria Operations for Networks — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Aria Operations for Networks (vRNI) bugs, error codes, and workarounds covering collector connectivity, data source configuration, and flow analysis.

*Applies to: Aria Operations for Networks 6.x*
</div>
![VMware Aria Operations for Networks — Known Issues and Error Codes](../../../../assets/virtualization-vmware-aria-operations-for-networks-troublesh.svg)





```d2
direction: down

symptom: Identify Symptom {shape: diamond}
data_sources: "Data Sources" {shape: rectangle}
flow_analysis: "Flow Analysis" {shape: rectangle}
platform: "Platform" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> data_sources: investigate
symptom -> flow_analysis: investigate
symptom -> platform: investigate
data_sources -> resolution
flow_analysis -> resolution
platform -> resolution
```

## Before you begin

- vRNI errors appear in `Settings → Infrastructure and Support → Data Sources`.
- Logs: SSH to Platform node; logs under `/home/ubuntu/log/`.

## Data Sources

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vCenter data source shows `Auth failed` | vRNI 6.x | vCenter credentials changed or service account locked | Update credentials in vRNI data source settings | N/A |
| NSX-T data source `Connection timeout` | vRNI 6.x | Collector cannot reach NSX Manager on 443 | Verify TCP 443 from Collector to NSX Manager IPs | N/A |
| `SNMP collection failed` for physical switch | vRNI 6.x | SNMP v2c community string mismatch or UDP 161 blocked | Update community string; verify UDP 161 from Collector to switch | N/A |

## Flow Analysis

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| IPFIX flows not appearing from NSX | vRNI 6.x | IPFIX not enabled on NSX logical switches | Enable IPFIX on NSX-T via `Fabric → Profiles → IPFIX Collector Profile` | N/A |
| Flow data missing for specific VMs | vRNI 6.x | VM not in inventory scope of connected vCenter | Ensure VM's vCenter is added as data source; resync inventory | N/A |

## Platform

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Platform UI unreachable` after upgrade | vRNI 6.x | Upgrade script left `nginx` service in failed state | SSH to Platform: `service nginx restart` | N/A |
| Collector shows `Offline` after reboot | vRNI 6.x | Collector appliance NTP drift from Platform | Sync Collector NTP source with Platform; restart Collector registration | N/A |

## See also

- [VMware Aria Operations for Networks — Common Issues](common-issues/)
- [VMware NSX — Known Issues](../../nsx/troubleshooting/known-issues.md)
- [VMware Aria Operations — Known Issues](../../aria-operations/troubleshooting/known-issues.md)
