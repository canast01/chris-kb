# vCenter — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering vCenter Upgrade Procedure (VCSA), vSphere Lifecycle Manager (vLCM), Interoperability Matrix, Patch Cadence, EOL Planning and 2 more sections.
</div>

```text
vSphere Upgrade Sequence
════════════════════════════════════════════════════════

  MUST follow this order — newer ESXi is NOT supported by older vCenter

  ┌─────────────────┐
  │ 1. Pre-checks   │  interop matrix · backup · disk space · certs
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 2. vCenter      │  Stage 1 (deploy new appliance alongside existing)
  │    Server       │  Stage 2 (migrate data, cut over, old VCSA off)
  │    (VCSA first) │  ← always upgrade vCenter before ESXi
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 3. vSAN         │  vSAN upgrade wizard (if deployed)
  │    (if used)    │  must match vSphere release train
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 4. NSX Manager  │  check interop matrix for new vCenter version
  │    (if used)    │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 5. ESXi Hosts   │  vLCM cluster image remediation
  │    (one cluster │  one host at a time → maintenance mode
  │     at a time)  │  → apply image → reboot → exit maintenance
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 6. VM Hardware  │  optional — check guest OS compat first
  │    + VMware     │
  │    Tools        │
  └─────────────────┘

  Rollback: full restore from pre-upgrade backup only
            (no in-place rollback; keep old VCSA off for 24h window)
```
┌───────────────────────────────── vCenter Server — Install & Upgrade ──────────────────────────────────┐
│                                                                                                       │
│  vCenter is deployed as an OVA; upgrades use the built-in VCSA installer ISO                          │
│  which migrates config from the old appliance in two stages.                                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Pre-Install Checklist             │  │               Deployment Steps              │   │
│   │          DNS A + PTR records ready           │  │            Mount ISO on jump host           │   │
│   │           NTP configured on hosts            │  │            Run vcsa-ui-installer            │   │
│   │            Port 443/80/9443 open             │  │             Stage 1: OVA deploy             │   │
│   │         SSO password complexity met          │  │            Stage 2: configure SSO           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pre-install DNS and NTP are critical; failures here block SSO certificate issuance.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Pre-Checks              │  │              Upgrade Procedure              │   │
│   │              Snapshot old VCSA               │  │           ISO: vcsa-deploy upgrade          │   │
│   │           Run Pre-Upgrade Checker            │  │           Stage 1: new VCSA boots           │   │
│   │           Check cert expiry first            │  │           Stage 2: config migrated          │   │
│   │          Drain old VC of snapshots           │  │           Old VC powered off after          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Target ESXi host needs sufficient RAM/CPU/storage for VCSA size tier;                                │
│  upgrade deploys a second appliance temporarily (needs 2x storage).                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA installer = GUI/CLI ISO tool; runs on Windows/Linux/Mac jump host                               │
│  vcsa-deploy    = CLI installer included in the VCSA ISO                                              │
│  Stage 1        = OVA deployment; network and storage config                                          │
│  Stage 2        = SSO setup; inventory and config import                                              │
│  Pre-check      = built-in checker; validates certs, DNS, ports, DB                                   │
│  Snapshot (pre) = rollback point before upgrade; remove after success                                 │
│  Jump host      = Windows/Linux machine that mounts and runs ISO installer                            │
│  DNS PTR        = reverse lookup; required for VCSA identity establishment                            │
│  SSO complexity = min 8 chars, upper, lower, digit, special                                           │
│  Drain snapshots= remove all VM snapshots before upgrading to avoid bloat                             │
│  Port 9443      = VCSA appliance management HTTPS (VAMI)                                              │
│  2x storage     = upgrade deploys new VCSA alongside old; same datastore OK                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

## vCenter Upgrade Procedure (VCSA)

1. Take a **file-based backup** of vCenter (VAMI → Backup)
2. Snapshot the VCSA VM (if on a separate vCenter; do not rely on this for recovery)
3. Download the new VCSA ISO from Broadcom portal
4. Mount ISO and run the **Stage 1** installer (deploys new appliance alongside existing)
5. Run **Stage 2** (migrates data, cuts over, shuts down old appliance)
6. Validate: vSphere Client accessible, all hosts connected, SSO working
7. Remove old appliance after 24-hour validation window

## vSphere Lifecycle Manager (vLCM)

vLCM replaces the legacy vSphere Update Manager (VUM) for ESXi host lifecycle management. vLCM uses **cluster images** — a single desired-state image (ESXi base + vendor add-ons + VIBs) applied cluster-wide via remediation.

Key concepts:
- **Image**: ESXi base version + vendor add-ons (drivers) + components (VIBs)
- **Depot**: VMware Online depot or a local UMDS-synced depot
- **Compliance**: Per-host comparison of running state against cluster image
- **Remediation**: Puts host in maintenance mode, applies image, reboots, exits maintenance mode

## Interoperability Matrix

Before any upgrade, check the [VMware Product Interoperability Matrix](https://interopmatrix.broadcom.com):

| Component | Constraint |
|---|---|
| vSAN version | Must match vSphere version (same release train) |
| NSX-T / NSX 4.x | Supported vCenter versions listed per NSX release |
| Aria Operations | Specific adapter versions per vCenter/vSphere release |
| Veeam Backup | Veeam release supports specific vCenter/ESXi versions |
| Hardware (HCL) | ESXi version must support the physical server model |

## Patch Cadence

- VMware releases patches quarterly and out-of-band for critical CVEs
- **Critical Security Advisories (VMSA)**: apply within 30 days; P1 CVEs within 72 hours per most security policies
- Subscribe to [Broadcom Security Advisories](https://support.broadcom.com/web/ecx/security-advisory) RSS/email feed

## EOL Planning

When a vSphere version approaches EOL:

1. Identify all vCenter instances and ESXi hosts on the EOL version
2. Check interop matrix for target version vs. NSX, vSAN, plugins
3. Plan upgrade windows (typically 2–3 cluster-per-weekend cadence)
4. Update runbooks, monitoring thresholds, and backup schedules post-upgrade
5. Validate vLCM cluster images for all clusters post-upgrade

## Rollback Considerations

vCenter upgrade rollback is possible only via **file-based backup restore** — there is no in-place rollback. The old appliance is kept powered off for the validation window. Key points:

- Rollback means full restore from pre-upgrade backup
- Any changes made post-upgrade (new VMs, config changes) are lost on rollback
- ESXi downgrades are **not supported** — test on one host first and maintain rollback window before cluster-wide remediation

## Lifecycle

### vSphere Update Manager (VUM) — Legacy

Baseline-based patching. Still available in vSphere 7 but deprecated in 8. Use for standalone hosts not in vLCM-managed clusters.
