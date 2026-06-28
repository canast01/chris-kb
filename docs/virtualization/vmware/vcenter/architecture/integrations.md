---
tags:
  - architecture
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter — Integrations


<div class="kb-summary">
Integrations reference covering Veeam Backup & Replication, Identity and Authentication Integration, Monitoring Integration, NSX Integration.

*Applies to: vSphere 7.x · 8.x*
</div>
![vCenter — Integrations](../../../../assets/virtualization-vmware-vcenter-architecture-integrations.svg)



- **IWA**: Uses the machine account of the VCSA; requires VCSA joined to AD domain
- **LDAP**: Explicit bind account; use LDAPS (port 636) for encrypted queries

```d2
direction: right

center: "vCenter Server" {shape: hexagon}
identity_integration: "Identity Integration" {shape: rectangle}
monitoring_integration: "Monitoring Integration" {shape: rectangle}
nsx_integration: "NSX Integration" {shape: rectangle}

center -> identity_integration
center -> monitoring_integration
center -> nsx_integration
```

## Identity Integration

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

## See also

- [vCenter — How It Works](how-it-works/)
- [vCenter — Deploy](../deploy/)
