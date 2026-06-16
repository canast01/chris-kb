---
tags:
  - troubleshooting
  - aria-suite-lifecycle
  - vmware
  - known-issues
---
# VMware Aria Suite Lifecycle — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Aria Suite Lifecycle (LCM) bugs, error codes, and workarounds covering product deployment, certificate management, and upgrade operations.

*Applies to: Aria Suite Lifecycle 8.x*
</div>

```text
┌────────────────────────────────── VMware Aria Suite Lifecycle (LCM) ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Lifecycle management for the Aria suite — deploy, upgrade, patch, scale            │   │
│   │               Protocols: HTTPS (UI/API) · vCenter API · SSH (node access) · NFS               │   │
│   │             Management: LCM web UI · REST API · binary downloads from VMware depot            │   │
│   │           LCM deploys OVA -> configures product -> installs cert -> validates health          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Platform          │  │        LCM appliance        │  │        OVA on vCenter       │   │
│   │           Products          │  │        Aria stack VMs       │  │      Auto/Logs/Ops/Nets     │   │
│   │           Packages          │  │        Depot binaries       │  │      Online or NFS repo     │   │
│   │            Certs            │  │      VMware CA / custom     │  │     LCM handles cert ops    │   │
│   │           Identity          │  │         vIDM (VIDM)         │  │      SSO for Aria stack     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  LCM appliance   │Lifecycle manager │     HTTPS 443     │   admin@local    │Manages full stack│   │
│   │     vCenter      │  Deploy target   │    vCenter API    │ Service account  │OVA deploy target │   │
│   │      Depot       │  Binary source   │    HTTPS / NFS    │   depot creds    │Online or air-gap │   │
│   │       vIDM       │   SSO provider   │     HTTPS 443     │   admin@local    │Integrated by LCM │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: LCM VM (vCenter) -> deploys Aria product VMs -> manages cert/upgrade lifecycle             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM          = Lifecycle Manager; VMware tool managing Aria product installs + upgrades              │
│  Environment  = LCM grouping of Aria products sharing vIDM and certificate config                     │
│  Product node = LCM-managed VM (e.g. Aria Operations master node)                                     │
│  Depot        = VMware product binary repository; online (vmware.com) or offline NFS                  │
│  Patch        = incremental version update applied via LCM without full redeploy                      │
│  Upgrade      = major or minor version update orchestrated by LCM                                     │
│  vIDM         = VMware Identity Manager; manages SSO and SAML for Aria products                       │
│  Certificate  = LCM replaces certs on all products in an environment at once                          │
│  Locker       = LCM credential and certificate vault for managed products                             │
│  Precheck     = LCM health validation run before an upgrade begins                                    │
│  Snapshot     = LCM takes VM snapshots before upgrade for rollback                                    │
│  Air-gap      = LCM configured with local NFS depot when internet is unavailable                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Aria LCM errors appear in `Lifecycle Operations → Requests`.
- Logs: SSH to Aria LCM appliance; logs under `/var/log/vmware/vrlcm/`.
- NTP sync and DNS resolution are the most common root causes of Aria LCM deployment failures.

## Product Deployment

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Deployment fails: `OVF deploy error — datastore insufficient space` | LCM 8.x | Target datastore lacks space for thin-provisioned product VM | Free datastore space; or select different datastore in LCM environment settings | N/A |
| `Product health check failed after deployment` | LCM 8.x | Deployed product services not started within timeout (often NTP issue) | Verify NTP sync on all deployed VMs; retry health check | N/A |
| `Cannot connect to vCenter for OVF deploy` | LCM 8.x | Aria LCM cannot reach vCenter on port 443 | Check 443 from LCM appliance to vCenter; verify credentials in LCM → vCenter Inventory | N/A |

## Certificate Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Certificate replacement fails: `Product not in STARTED state` | LCM 8.x | Target product service degraded before cert rotation | Restore product to healthy state first; retry certificate operation | N/A |
| `VMCA certificate import failed` | LCM 8.x | VMCA root CA not imported into Aria LCM trust store | Import vCenter CA into Aria LCM: `Settings → Certificates → Add CA` | N/A |

## Upgrade

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Product upgrade fails: `Snapshot creation failed` | LCM 8.x | vCenter snapshot quota exceeded or vSAN space insufficient | Free vSAN space; increase snapshot max per VM in vCenter; retry | N/A |
| `Binary mapping not found` for upgrade | LCM 8.x | Product binary not loaded into LCM binary mapping | Upload product binary to LCM → Lifecycle Operations → Settings → Binary Mapping | N/A |

## See also

- [VMware Aria Suite Lifecycle — Common Issues](common-issues.md)
- [VMware Aria Automation — Known Issues](../../aria-automation/troubleshooting/known-issues/)
- [VMware Aria Operations — Known Issues](../../aria-operations/troubleshooting/known-issues/)
