# vCenter Integration
## Storage Integration

### VASA Providers

Storage vendors register as VASA (vSphere APIs for Storage Awareness) providers to expose storage capabilities to vCenter for SPBM (Storage Policy-Based Management).

| Vendor | Provider | vVols Support |
|---|---|---|
| Pure Storage FlashArray | Pure Storage VASA Provider | Yes |
| Dell PowerStore | Dell EMC VASA Provider | Yes |
| NetApp ONTAP | NetApp VASA Provider | Yes |
| HPE Nimble | HPE Nimble VASA Provider | Yes |

Register VASA providers: **vCenter → Storage → Storage Providers → Add**

### Traditional Datastores

| Type | Protocol | Notes |
|---|---|---|
| VMFS6 | FC, iSCSI, FCoE | Block storage; default for most deployments |
| NFS 4.1 | NFS | File storage; Kerberos auth supported |
| vVols | FC, iSCSI, NFS | Object-based; requires VASA |
| vSAN | Internal (vSAN network) | HCI; managed from within vCenter |

### iSCSI Configuration Flow

1. Enable iSCSI adapter on ESXi hosts (`esxcli iscsi adapter add`)
2. Add dynamic/static discovery targets
3. Rescan HBAs
4. Apply multipathing policy (typically Round Robin for iSCSI)
5. Format and mount VMFS datastore from vCenter

## Backup Integration

### VADP (vSphere APIs for Data Protection)

VADP is the standard backup API. Backup solutions use VADP to take crash-consistent or application-consistent snapshots without requiring an agent inside each VM.

**Supported backup proxy modes:**
- **Hot-add** (preferred) — backup proxy VM mounts target VM disks directly; highest performance
- **NBD/NBDSSL** — network-based transfer over LAN; fallback mode
- **SAN** — FC/iSCSI direct access; requires backup proxy on same SAN fabric

### Veeam Backup & Replication

- Registers vCenter as a managed server in Veeam Console
- Uses VADP for VM backup; leverages Changed Block Tracking (CBT)
- vCenter credentials need: `Datastore.Browse`, `VirtualMachine.Config.*`, `VirtualMachine.State.CreateSnapshot`, and `Global.DisableMethods`
- Veeam Proxy VMs should be deployed in same cluster/datastore as protected VMs for hot-add

### CommVault IntelliSnap

- Integrates via vCenter API + array-level snapshot APIs
- Uses array snapshots for near-instant backup; VADP for recovery
- CommVault iDataAgent or VSA Proxy installed in vCenter environment

## Identity and Authentication

### Active Directory Integration

Connect vCenter SSO to AD so AD users/groups can be granted vSphere permissions:

```
vCenter → Administration → Single Sign On → Configuration → Identity Sources → Add
Type: Active Directory (Integrated Windows Authentication) or LDAP/LDAPS
```

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

## NSX-T Integration

NSX-T registers vCenter as a **Compute Manager**. This enables:

- NSX automatically discovers ESXi hosts from vCenter inventory
- vCenter tags flow into NSX for dynamic security group membership (DFW policies)
- VDS (vSphere Distributed Switch) is used as the NSX data plane transport on ESXi (VDS 7.0+)
- NSX segments appear as vCenter port groups

Register from NSX Manager: **System → Fabric → Compute Managers → Add vCenter**

Permissions required: vCenter account with `Host → Configuration` and `Network` privileges.
