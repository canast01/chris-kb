# vCenter — Integrations


<div class="kb-summary">
Integrations reference covering Veeam Backup & Replication, Identity and Authentication Integration, Monitoring Integration, NSX Integration.
</div>

```text
vCenter Integration Map
════════════════════════════════════════════════════════

                    ┌──────────────────┐
                    │   vCenter Server │
                    │   (VCSA)         │
                    └────────┬─────────┘
        ┌───────────┬────────┼─────────┬───────────┐
        │           │        │         │           │
  ┌─────▼──────┐ ┌──▼──────┐ │  ┌──────▼──────┐ ┌─▼──────────┐
  │  Identity  │ │ Storage │ │  │  NSX         │ │  Monitoring │
  │  (AD/LDAP) │ │ (VASA / │ │  │  Manager     │ │  (Aria Ops) │
  │  SAML/ADFS │ │  VMFS / │ │  │  Compute Mgr │ │  vCenter    │
  │  LDAPS:636 │ │  NFS /  │ │  │  ↔ DFW tags  │ │  Adapter    │
  └────────────┘ │  vVols) │ │  └─────────────┘ └────────────┘
                 └─────────┘ │
                             │
                   ┌─────────▼──────────────────────┐
                   │  Backup (VADP)                  │
                   │  Backup Server (Veeam/Commvault) │
                   │    → vCenter API (snapshot/CBT) │
                   │    → Backup Proxy (hot-add)      │
                   │    → Repository (SFTP/S3/disk)  │
                   └─────────────────────────────────┘

  SSO / Certificate Trust
  ┌──────────────────────────────────────────────────┐
  │  vCenter SSO (vsphere.local)                     │
  │    ├── AD Identity Source (LDAPS)  ← user authn  │
  │    ├── VMCA (CA)                  ← cert signing │
  │    └── Lookup Service             ← registry     │
  └──────────────────────────────────────────────────┘
```
┌──────────────────────────────────── vCenter Server — Integrations ────────────────────────────────────┐
│                                                                                                       │
│  vCenter integrates with identity, storage, network, backup, and monitoring                           │
│  systems via standardised APIs and plugin frameworks.                                                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Identity Integrations             │  │             Storage Integrations            │   │
│   │          Active Directory via LDAP           │  │            VASA: storage policies           │   │
│   │             SAML IdP federation              │  │            vVols: per-VM volumes            │   │
│   │               SSO local domain               │  │           NFS / iSCSI / FC mounts           │   │
│   │          MFA via smart card/RADIUS           │  │             HCI: vSAN integrated            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Identity gates all logins; storage providers register via VASA for policy management.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network & Security              │  │             Backup & Monitoring             │   │
│   │             NSX: SDN via vCenter             │  │               VADP: backup API              │   │
│   │          vDS: distributed switching          │  │           CBT: changed block track          │   │
│   │            Firewall rules via NSX            │  │            vROps: perf monitoring           │   │
│   │           Microsegmentation policy           │  │             SNMP / syslog export            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Integration traffic crosses the management network; VADP uses NBD or SAN transport.                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VADP    = vStorage APIs for Data Protection; backup quiescing and CBT                                │
│  CBT     = Changed Block Tracking; incremental backup efficiency mechanism                            │
│  VASA    = vSphere APIs for Storage Awareness; policy-based storage mgmt                              │
│  vVols   = Virtual Volumes; per-VM storage objects on VASA-capable arrays                             │
│  vDS     = vSphere Distributed Switch; centralised network config in VC                               │
│  NSX     = Network & Security virtualisation; integrates with vCenter                                 │
│  vROps   = VMware Aria Operations; pulls metrics via vCenter APIs                                     │
│  SAML    = Security Assertion Markup Language; federated SSO token format                             │
│  LDAP    = Lightweight Directory Access Protocol; AD identity source                                  │
│  NBD     = Network Block Device; backup transport over TCP (slower)                                   │
│  SAN     = Storage Area Network; fast backup transport via FC/iSCSI                                   │
│  HCI     = Hyper-Converged Infrastructure; vSAN = primary HCI integration                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```sql

- **IWA**: Uses the machine account of the VCSA; requires VCSA joined to AD domain
- **LDAP**: Explicit bind account; use LDAPS (port 636) for encrypted queries

### SSO Domain

vCenter ships with a local `vsphere.local` SSO domain. The `administrator@vsphere.local` account is the bootstrap admin. In production:

- Add AD as an identity source
- Grant required AD groups vSphere roles
- Do not use `administrator@vsphere.local` for day-to-day operations
- Rotate `administrator@vsphere.local` password per policy; document in password vault

### SAML Federation

vCenter can act as a SAML service provider for external IdPs (ADFS, Okta, Azure AD). Configure under **SSO → Configuration → SAML Service Provider**. Useful for MFA enforcement at the IdP level.

## Monitoring Integration

### Aria Operations (VMware)

- Deploy Aria Operations (formerly vRealize Operations) and register vCenter as a **vCenter Adapter**
- Provides capacity analytics, performance anomaly detection, cost reporting
- Aria Operations vCenter adapter collects metrics every 5 minutes by default
- Predictive DRS requires Aria Operations integration with vCenter

### REST API

vCenter exposes a modern REST API at `https://<vcenter>/api` (vSphere 7.0+). The legacy vSphere Automation SDK endpoint is at `https://<vcenter>/rest`.

```bash
# Authenticate and get session token
curl -sk -u 'administrator@vsphere.local:password' \
  -X POST https://<vcenter>/api/session

# List VMs
curl -sk -H "vmware-api-session-id: <token>" \
  https://<vcenter>/api/vcenter/vm
```

### Syslog / SIEM

vCenter forwards events as syslog (RFC 5424). Configure in VAMI or via PowerCLI:

```powershell
Set-VMHostSysLogServer -SysLogServer 'udp://<syslog-host>:514' -VMHost <host>
```

For vCenter appliance-level syslog, configure at **VAMI → Syslog**.

## NSX Integration

NSX registers vCenter as a **Compute Manager**. This enables:

- NSX automatically discovers ESXi hosts from vCenter inventory
- vCenter tags flow into NSX for dynamic security group membership (DFW policies)
- VDS (vSphere Distributed Switch) is used as the NSX data plane transport on ESXi (VDS 7.0+)
- NSX segments appear as vCenter port groups

Register from NSX Manager: **System → Fabric → Compute Managers → Add vCenter**

Permissions required: vCenter account with `Host → Configuration` and `Network` privileges.
