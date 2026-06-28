---
tags:
  - architecture
  - netapp
---
# ONTAP — Integrations


<div class="kb-summary">
Integrations reference covering VMware, SnapCenter Plugin, Active Directory / CIFS Authentication, Veeam Storage Integration (VeeamON / Direct Storage Access), ONTAP REST API and 2 more sections.

*Applies to: ONTAP 9.x*
</div>
![ONTAP — Integrations](../../../../assets/storage-netapp-ontap-architecture-integrations.svg)




```d2
direction: right

center: "NetApp ONTAP" {shape: hexagon}
vmware: "VMware" {shape: rectangle}
snapcenter_plugin: "SnapCenter Plugin" {shape: rectangle}
active_directory_cifs_authentication: "Active Directory / CIFS Authentication" {shape: rectangle}
veeam_storage_integration_veeamon_di: "Veeam Storage Integration (VeeamON / Direct Storage Access)" {shape: rectangle}
ontap_rest_api: "ONTAP REST API" {shape: rectangle}
cloud_volumes_ontap_integration: "Cloud Volumes ONTAP Integration" {shape: rectangle}

center -> vmware
center -> snapcenter_plugin
center -> active_directory_cifs_authentication
center -> veeam_storage_integration_veeamon_di
center -> ontap_rest_api
center -> cloud_volumes_ontap_integration
```

## VMware

ONTAP integrates with VMware vSphere at multiple layers:

- **NFS datastores**: Mount ONTAP NFS exports directly as vSphere datastores; NFSv3 or NFSv4.1 (pNFS for parallel I/O); configure NFS export policy to allow ESXi management IPs
- **VMFS (iSCSI/FC)**: Present ONTAP LUNs as VMFS datastores via iSCSI or FC; use round-robin multipath policy on ESXi with ALUA enabled on ONTAP
- **VAAI (vStorage APIs for Array Integration)**: Enable VAAI-NAS (`vserver nfs modify -vserver <svm> -vstorage enabled`) and VAAI-SCSI for hardware offload of copy, zero, and compare operations — reduces ESXi CPU and network load significantly
- **vVols (Virtual Volumes)**: ONTAP supports vVols via the NetApp VASA Provider (part of ONTAP Tools for VMware); each VMDK is a separate ONTAP volume object with granular QoS and snapshot capability
- **ONTAP Tools for VMware vSphere**: vCenter plugin providing datastore provisioning, VAAI registration, VASA, and SRA (Site Recovery Adapter) for VMware SRM integration; deployed as an OVA

## SnapCenter Plugin

The SnapCenter Plug-in for VMware vSphere is deployed as a separate OVA and registered in vCenter. It provides VM-consistent and crash-consistent snapshot-based backup of VMs and vSphere datastores using ONTAP snapshots, and supports SnapVault replication for long-term retention. See the [SnapCenter section](../../snapcenter/index.md) for full coverage.

## Active Directory / CIFS Authentication

```bash
# Join an SVM to Active Directory for CIFS/SMB
vserver cifs create -vserver <svm> -cifs-server <netbios-name> -domain <domain.corp> -ou "OU=Servers,DC=domain,DC=corp"

# Verify CIFS domain join and DC connectivity
vserver cifs domain info -vserver <svm>

# Configure LDAP for NFS Kerberos and user mapping
vserver services name-service ldap create -vserver <svm> -client-config <ldap-config>
```

## Veeam Storage Integration (VeeamON / Direct Storage Access)

Veeam Backup & Replication integrates with ONTAP via the Veeam Backup & Replication storage plugin, enabling:
- Direct NFS/iSCSI access to ONTAP snapshots for backup from storage snapshots (avoiding VM stun)
- SnapVault integration for secondary-target backup jobs
- Storage snapshot orchestration from the Veeam job engine

Register the ONTAP cluster in Veeam under Storage Infrastructure using the cluster-management LIF and a dedicated `vsadmin`-equivalent account with minimum required permissions.

## ONTAP REST API

ONTAP exposes a full RESTful API available at:

```text
https://<cluster-mgmt-lif>/api
```

- Interactive documentation at `https://<cluster-mgmt-lif>/docs/api`
- Authenticate with Basic Auth (over HTTPS) or OAuth2 tokens
- Use service accounts with minimum required RBAC roles for automation

```bash
# Example: list SVMs via REST API using curl
curl -sk -u admin:<password> https://<cluster>/api/svm/svms | python3 -m json.tool

# Example: list volumes
curl -sk -u admin:<password> "https://<cluster>/api/storage/volumes?fields=name,used,size" | python3 -m json.tool
```

Python SDK (`netapp-ontap` package) and Ansible (`netapp.ontap` collection) provide higher-level abstractions for automation.

## Cloud Volumes ONTAP Integration

ONTAP on-premises clusters can peer with Cloud Volumes ONTAP (CVO) deployments in AWS, Azure, or GCP:
- Use intercluster LIFs and cluster peering for SnapMirror relationships to/from CVO
- FabricPool: tier cold data blocks from on-premises aggregates to object storage (S3/Azure Blob/GCS) transparently — configure via `storage aggregate object-store attach`
- BlueXP acts as the management plane for both on-premises ONTAP and CVO, providing unified capacity and replication views

## Monitoring Integration

| Tool | Integration Method |
|---|---|
| Prometheus / Grafana | ONTAP REST API metrics endpoint or NetApp Harvest (open source collector) |
| Splunk / Syslog | `vserver audit` for file events; EMS log forwarding via `event notification destination` |
| SNMP monitoring (Nagios, Zabbix) | SNMPv3 only; MIB files available from NetApp support site |
| NetApp Active IQ / BlueXP | AutoSupport-based; enabled by default; provides AI-driven health and capacity advisories |
| PagerDuty / OpsGenie | EMS email notifications forwarded via relay or webhook integrations |

---

## See also

- [Ontap — How It Works](how-it-works/)
- [Ontap — Design Standards](design-standards/)
