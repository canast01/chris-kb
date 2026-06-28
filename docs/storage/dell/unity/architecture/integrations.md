---
tags:
  - architecture
  - dell
---
# Unity — Integrations


<div class="kb-summary">
Integrations reference covering Integration Map, VMware Integration, Backup Integration, CloudIQ Monitoring, Active Directory and 1 more sections.

*Applies to: Unity XT*
</div>
![Unity — Integrations](../../../../assets/storage-dell-unity-architecture-integrations.svg)




```d2
direction: right

center: "Unity XT" {shape: hexagon}
integration_map: "Integration Map" {shape: rectangle}
vmware_integration: "VMware Integration" {shape: rectangle}
backup_integration: "Backup Integration" {shape: rectangle}
cloudiq_monitoring: "CloudIQ Monitoring" {shape: rectangle}
active_directory: "Active Directory" {shape: rectangle}
rest_api: "REST API" {shape: rectangle}

center -> integration_map
center -> vmware_integration
center -> backup_integration
center -> cloudiq_monitoring
center -> active_directory
center -> rest_api
```

## Integration Map

```mermaid
graph LR
  subgraph "VMware vSphere"
    VC["vCenter Server"]
    ESX["ESXi Hosts"]
    VC --> ESX
  end
  subgraph "Dell Unity XT"
    UNI["Unisphere / REST API"]
    VASA["VASA Provider\n(vVols)"]
    LUN["FC / iSCSI LUNs"]
    NFS["NAS Exports\n(NFS / SMB)"]
  end
  subgraph "Backup Ecosystem"
    VBR["Veeam B&R"]
    COMM["CommVault\nIntelliSnap"]
    NDMP["NDMP Client"]
  end
  subgraph "Monitoring"
    CIQ["Dell CloudIQ\n(via SCG)"]
    AD["Active Directory\n(LDAP / Kerberos)"]
  end
  VC --> VASA
  ESX --> LUN & NFS
  VBR & COMM --> UNI
  NDMP --> NFS
  UNI --> CIQ
  UNI --> AD
```

## VMware Integration

Unity XT integrates with VMware vSphere via multiple paths:

**VASA Provider (vVols)**

Unity includes an embedded VASA provider that enables VMware Virtual Volumes (vVols). Register the VASA provider in vCenter under **Storage > Storage Providers**. Use the Unity management IP and credentials. With vVols, each VMDK gets its own Unity LUN, enabling per-VM snapshot and replication policies.

**NFS and VMFS Datastores**

- NFS datastores: create a Unity filesystem and NFS export, then add the NFS datastore in vCenter. Use NFS v3 or v4.1.
- VMFS datastores: provision a Unity LUN over FC or iSCSI and add it as a VMFS datastore in vCenter.
- Enable VAAI (VMware APIs for Array Integration) — Unity supports VAAI for hardware offload of VMFS clone, zero, and lock operations.

**Unity Plugin for vCenter**

Install the Dell Unity vCenter plugin to provision Unity storage directly from the vCenter UI without switching to Unisphere.

## Backup Integration

| Backup Tool | Integration Method | Notes |
|---|---|---|
| Veeam Backup & Replication | Unity storage snapshot integration (Veeam Storage Snapshots) | Veeam triggers Unity snapshots at backup time; requires Veeam Enterprise or higher |
| CommVault | Unity snapshot API integration via IntelliSnap | Configure Unity array in CommVault as an IntelliSnap-capable array |
| Veritas NetBackup | NetBackup Snapshot Manager with Unity snapshot support | Configure Unity as a snapshot array in NetBackup Snapshot Manager |
| Generic NDMP | Unity NAS servers support NDMP for file-level backup | Use any NDMP-compatible backup tool; configure NDMP on the NAS server via `uemcli /net/nas/ndmp` |

## CloudIQ Monitoring

Unity XT registers with Dell CloudIQ automatically when a Secure Connect Gateway (SCG) is deployed and connected. CloudIQ provides health scores, capacity forecasting, and proactive alerts for Unity.

Configuration steps:

1. Deploy the SCG virtual appliance and configure it with your Dell account.
2. In the SCG web UI, add the Unity array using its management IP and credentials.
3. The Unity array appears in CloudIQ within 15–30 minutes after SCG registration.
4. SupportAssist must be enabled on Unity (Unisphere > **Settings > SupportAssist**) for CloudIQ telemetry collection.

## Active Directory

Unity supports LDAP/AD integration for two distinct purposes:

| Integration | Purpose | Configuration |
|---|---|---|
| Unisphere AD authentication | Admin users log in to Unisphere with AD credentials | Unisphere: **Settings > Access > Directory Services** |
| NAS server AD domain join | CIFS/SMB shares use AD for share permissions and Kerberos auth | `uemcli /net/nas/ad join` per NAS server |

For CIFS/SMB, each NAS server must be independently joined to the AD domain with a machine account in the appropriate OU. Ensure the NAS server's DNS is configured to resolve the domain controllers.

## REST API

Unisphere for Unity exposes a REST API for all management operations. Use it for automation and integration with ITSM and monitoring tools.

```bash
# Base URL
https://<sp-ip>/api/types/

# Authenticate (session-based — returns a cookie for subsequent requests)
curl -c cookie.txt -b cookie.txt -k -u admin:<password> \
  -X GET "https://<sp-ip>/api/instances/system/0"

# List all storage pools
curl -c cookie.txt -b cookie.txt -k \
  -X GET "https://<sp-ip>/api/types/pool/instances?fields=name,sizeTotal,sizeUsed,health"

# List all LUNs
curl -c cookie.txt -b cookie.txt -k \
  -X GET "https://<sp-ip>/api/types/lun/instances?fields=name,sizeTotal,pool,health"
```

The API supports basic auth and session (cookie) auth. Use session auth for scripts that make multiple API calls to avoid authenticating on each request. The full API reference is available in Unisphere under **Help > REST API Reference**.

---

## See also

- [Unity — How It Works](how-it-works/)
- [Unity — Design Standards](design-standards/)
