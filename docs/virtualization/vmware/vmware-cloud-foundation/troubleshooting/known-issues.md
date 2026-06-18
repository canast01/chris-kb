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

```text
┌──────────────────────────────────── VMware Cloud Foundation (VCF) ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Full-stack HCI platform — vSphere + vSAN + NSX + vCenter + SDDC Mgr              │   │
│   │               Protocols: HTTPS (SDDC UI) · vSphere API · NSX API · vSAN internal              │   │
│   │              Management: SDDC Manager UI · REST API · VCF CLI · LCM for upgrades              │   │
│   │              BringUp -> Management Domain -> Workload Domain -> lifecycle manage              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Management         │  │         SDDC Manager        │  │      VCF lifecycle ctrl     │   │
│   │           Compute           │  │       vSphere cluster       │  │          Per domain         │   │
│   │           Storage           │  │             vSAN            │  │     Default HCI storage     │   │
│   │           Network           │  │             NSX             │  │    SDN overlay per domain   │   │
│   │           Domains           │  │       Mgmt + workload       │  │      Separate vCenters      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   SDDC Manager   │VCF control plane │     HTTPS 443     │    local / AD    │ Orchestrates all │   │
│   │     BringUp      │  Initial deploy  │       HTTPS       │       root       │One-time bootstrap│   │
│   │       LCM        │ Upgrade manager  │    HTTPS (API)    │      Admin       │ Bundle upgrades  │   │
│   │       NSX        │    SDN layer     │    HTTPS (API)    │    NSX admin     │Shared or per-dom.│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: VCF hosts -> SDDC Manager -> Management Domain vCenter -> Workload Domains                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCF          = VMware Cloud Foundation; full-stack HCI + SDN + lifecycle platform                    │
│  SDDC Manager = VCF management plane; orchestrates all domain and lifecycle ops                       │
│  BringUp      = VCF day-0 bootstrap process; validates hardware and deploys Mgmt Domain               │
│  Management Domain = first VCF domain; hosts SDDC Manager, vCenter, NSX, vSAN                         │
│  Workload Domain = additional VCF domain provisioned for tenant workloads                             │
│  EMS          = External Management Stack; BYO vCenter/NSX instead of VCF-managed                     │
│  LCM          = VCF Lifecycle Management; coordinates bundle upgrades across stack                    │
│  Bundle       = versioned set of component binaries for VCF upgrade                                   │
│  PSA          = Principal Storage Architecture; vSAN or external storage choice                       │
│  Cloud Builder = VCF deploy VM used during BringUp before SDDC Manager is live                        │
│  vSAN ESA     = vSAN Express Storage Architecture; new engine in VCF 5.x                              │
│  SoS          = Save Our Systems; VCF health-check and log-collection utility                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
