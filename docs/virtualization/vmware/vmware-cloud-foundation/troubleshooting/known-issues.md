---
tags:
  - troubleshooting
  - vcf
  - vmware
  - known-issues
  - vcf-5
---
# VMware Cloud Foundation — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known VCF bugs, error codes, and workarounds covering SDDC Manager, bring-up, and lifecycle management.

*Applies to: VCF 4.x / 5.x*
</div>
![VMware Cloud Foundation — Known Issues and Error Codes](../../../../assets/virtualization-vmware-vmware-cloud-foundation-troubleshootin.svg)





## Before you begin

- VCF errors appear in SDDC Manager → Inventory → Workflows; expand failed task for error detail.
- SDDC Manager logs: `/var/log/vmware/vcf/domainmanager/` and `/var/log/vmware/vcf/lcm/`.
- VCF bring-up failures require fresh deployment — partial bring-up cannot be resumed from all failure points.

## Bring-Up

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Cloud Builder validation fails: `DNS resolution failed` | VCF 4.x / 5.x | DNS not pre-configured for all VCF component FQDNs | Create all A/PTR records before bring-up; VCF requires forward and reverse DNS | N/A |
| Bring-up fails at `Deploying VCSA` | VCF 4.x | Insufficient disk space on management host | Ensure each management host has ≥1.4 TB raw per VCF BOM; verify vSAN datastore headroom | N/A |
| `NTP validation failed` during preflight | VCF 4.x / 5.x | NTP offset >500ms on Cloud Builder or management hosts | Sync all hosts to same NTP source; verify offset with `ntpq -p` | N/A |

## SDDC Manager

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `SDDC Manager services not responding` after upgrade | VCF 5.x | LCM upgrade incomplete due to disk pressure | Check `/var/log/` disk usage on SDDC Manager VM; purge old logs; restart `vcf-lcm` service | N/A |
| Workload domain creation fails: `Cannot contact NSX Manager` | VCF 4.x / 5.x | NSX Manager not fully initialized before VCF calls it | Wait for NSX Manager cluster to reach STABLE state; retry domain creation | N/A |

## Lifecycle Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| LCM upgrade fails: `Bundle checksum mismatch` | VCF 4.x / 5.x | Bundle downloaded with network interruption | Re-download bundle from depot; verify SHA256 checksum | N/A |
| `Host precheck failed — existing VIBs conflict` | VCF 5.x | Third-party VIBs installed outside VCF lifecycle | Remove conflicting VIBs before upgrade; re-add via VCF-managed mechanism post-upgrade | N/A |
| Certificate rotation fails on NSX component | VCF 5.x | NSX certificate rotation requires Manager in STABLE state | Check NSX Manager cluster status; ensure no pending DFW realizations before rotation | N/A |

## See also

- [VMware VCF — Common Issues](common-issues/)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues.md)
- [VMware NSX — Known Issues](../../nsx/troubleshooting/known-issues.md)
- [VMware vSAN — Known Issues](../../vsan/troubleshooting/known-issues.md)
