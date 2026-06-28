---
tags:
  - architecture
  - dell
---
# PowerStore — Integrations


<div class="kb-summary">
Integrations reference covering VMware vSphere, Dell Backup and Recovery (Data Domain / PowerProtect), CloudIQ, SupportAssist (ESRS), SNMP Monitoring and 4 more sections.

*Applies to: PowerStore 3.x*
</div>
![PowerStore — Integrations](../../../../assets/storage-dell-powerstore-architecture-integrations.svg)




```d2
direction: right

center: "PowerStore" {shape: hexagon}
vmware_vsphere: "VMware vSphere" {shape: rectangle}
dell_backup_and_recovery_data_domain: "Dell Backup and Recovery (Data Domain / PowerProtect)" {shape: rectangle}
cloudiq: "CloudIQ" {shape: rectangle}
supportassist_esrs: "SupportAssist (ESRS)" {shape: rectangle}
snmp_monitoring: "SNMP Monitoring" {shape: rectangle}
syslog_siem_integration: "Syslog / SIEM Integration" {shape: rectangle}

center -> vmware_vsphere
center -> dell_backup_and_recovery_data_domain
center -> cloudiq
center -> supportassist_esrs
center -> snmp_monitoring
center -> syslog_siem_integration
```

## VMware vSphere

PowerStore is deeply integrated with VMware vSphere and is qualified as a VMware-certified storage solution.

### VMFS Datastores (iSCSI / FC)

Standard block storage datastores — volumes presented to ESXi hosts via Fibre Channel or iSCSI, then formatted as VMFS6. This is the most common VMware integration path and works with all PowerStore models.

```bash
# Create a volume via REST API for VMware use
curl -k -X POST "https://<mgmt-ip>/api/rest/volume" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "vmfs-prod-01",
    "size": 10995116277760,
    "description": "VMFS datastore for production VMs",
    "volume_group_id": "<vg-id>"
  }'

# Map the volume to the ESXi host group
curl -k -X POST "https://<mgmt-ip>/api/rest/host_volume_mapping" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "volume_id": "<volume-id>",
    "host_group_id": "<esxi-cluster-host-group-id>",
    "logical_unit_number": 0
  }'
```

After mapping, rescan storage in vSphere and present the volume as a new VMFS datastore via **vCenter → Storage → New Datastore**.

### NFS Datastores

PowerStore NAS servers serve NFS exports to ESXi hosts. NFS datastores avoid the need for LUN management and provide flexibility for large VM environments.

Configuration steps:

1. Create a NAS server on PowerStore with an NFS protocol enabled interface
2. Create a file system and enable NFS export with appropriate permissions
3. In vSphere, mount the NFS export as a new datastore

```bash
# Create NAS server
curl -k -X POST "https://<mgmt-ip>/api/rest/nas_server" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "nas-vmware-prod",
    "preferred_node": "node-a",
    "current_unix_directory_service": "NIS",
    "description": "NAS server for VMware NFS datastores"
  }'

# NFS export settings recommended for ESXi
# root_squash: no_root_squash (ESXi requires root access)
# Access: read-write, allow all ESXi host IPs in the cluster
# NFS version: NFS v3 (widely supported) or NFS v4.1 (stateful, session trunking)
```

### Virtual Volumes (vVols)

vVols are the recommended storage model for VMware environments requiring per-VM storage policy management. Each virtual disk becomes an individual object on PowerStore rather than a file in a shared VMFS.

| Component | Function |
|---|---|
| VASA Provider | Built into PowerStoreOS; no separate VM required |
| Protocol Endpoint (PE) | A logical I/O access point on PowerStore; created automatically |
| Storage Container | A PowerStore volume group designated as a vVols datastore |
| VM Storage Policy | vSphere policy mapped to a PowerStore capability profile |

```bash
# Verify VASA Provider registration status
curl -k -X GET "https://<mgmt-ip>/api/rest/storage_provider" \
  -H "DELL-EMC-TOKEN: <token>"

# List storage containers (vVols datastores)
curl -k -X GET "https://<mgmt-ip>/api/rest/storage_container" \
  -H "DELL-EMC-TOKEN: <token>"
```

### VMware Site Recovery Manager (SRM)

PowerStore integrates with VMware SRM via the **Storage Replication Adapter (SRA)**. The SRA is a plugin installed on the SRM server that allows SRM to orchestrate PowerStore async replication failover.

| Component | Location |
|---|---|
| Dell PowerStore SRA | Installed on the vCenter SRM server (Windows or Linux) |
| PowerStore async replication | Configured between primary and recovery PowerStore arrays |
| SRM Array Manager | Configured in SRM with the PowerStore management IP and credentials |

Integration workflow:

1. Configure async replication session between primary and recovery PowerStore
2. Install the PowerStore SRA on both SRM servers (protected and recovery sites)
3. Add both PowerStore arrays to SRM under **Array Manager** using the management IP and a dedicated SRM service account
4. Create Protection Groups in SRM that include the replicated volumes/datastores
5. Create Recovery Plans that orchestrate VM shutdown, replication sync, and VM power-on at the recovery site

### VMware HCI (vSAN)

PowerStore X-series running AppsOn can coexist with vSAN, but PowerStore is not itself a vSAN-based solution. When deploying PowerStore alongside a vSAN cluster:

- PowerStore block volumes can serve as supplemental external storage for vSAN-managed clusters (iSCSI or FC datastores)
- PowerStore NAS can provide file storage to VMs running in a vSAN cluster

## Dell Backup and Recovery (Data Domain / PowerProtect)

### PowerProtect Data Manager (PPDM)

PowerProtect Data Manager integrates with PowerStore for application-consistent VM backups using vSphere APIs.

| Integration Method | Description |
|---|---|
| vSphere VADP | PPDM uses VMware VADP (vStorage APIs for Data Protection) to quiesce and snapshot VMs stored on PowerStore |
| Crash-consistent snapshot | PowerStore-native snapshot taken before VADP backup for rollback capability |
| Storage direct backup | PPDM can use PowerStore snapshots as a backup source (snapshot offload), reducing load on production hosts |

### Veeam Backup & Replication

Veeam integrates with PowerStore via:

- **vSphere VADP**: standard VM backup via vCenter — no PowerStore-specific plugin needed
- **Veeam Storage Integration Plugin for PowerStore**: enables Veeam to leverage PowerStore snapshots directly as restore points, offloading backup I/O from production hosts

```bash
# PowerStore REST API credentials for Veeam integration
# Create a dedicated service account in PowerStore Manager for Veeam
# Recommended role: StorageOperator (can create/delete snapshots, read volumes)
# Settings → Security → Users → Add User → Role: StorageOperator
```

### Commvault

Commvault MediaAgent integrates with PowerStore for IntelliSnap snapshot management:

- Commvault creates application-consistent snapshots on PowerStore
- Snapshots are catalogued in Commvault and can be used as instant restore points
- Commvault Snap Engine for Dell PowerStore uses the REST API to manage snapshots

## CloudIQ

All PowerStore systems are supported by Dell CloudIQ for predictive analytics, health scoring, and capacity forecasting. CloudIQ integration is automatic once a Secure Connect Gateway (SCG) is deployed and the PowerStore system is registered.

Data sent to CloudIQ:

| Data Type | Purpose |
|---|---|
| Hardware health | Drive, node, PSU, fan health scores |
| Capacity metrics | Used, free, DRR, and forecast models |
| Performance metrics | IOPS, throughput, latency per volume |
| Configuration metadata | Software version, model, serial number |

No user data, file contents, or application data is transmitted to CloudIQ.

## SupportAssist (ESRS)

SupportAssist is Dell's call-home mechanism. When enabled, PowerStore automatically:

- Sends health telemetry to Dell's SRS (Secure Remote Services) platform
- Creates automated service requests for qualifying hardware faults (e.g., drive failure)
- Enables Dell Support engineers to initiate remote support sessions

```text
PowerStore → SupportAssist → ESRS/SRS Cloud → Dell Support
```

Configure SupportAssist in PowerStore Manager under **Settings → Support → SupportAssist**. Requires outbound HTTPS to `esrs3.emc.com` (port 443). Route through a proxy if direct internet access is not permitted.

## SNMP Monitoring

PowerStore supports SNMP v2c and v3 for integration with enterprise monitoring systems (Nagios, Zabbix, SolarWinds, etc.).

| Setting | Recommended Value |
|---|---|
| Protocol | SNMP v3 (preferred); v2c if v3 is not supported by the NMS |
| Auth protocol (v3) | SHA |
| Privacy protocol (v3) | AES-128 or AES-256 |
| Community string (v2c) | Change from default; restrict by source IP |
| Trap destination | NMS collector IP |
| Trap types | Hardware faults, capacity thresholds, replication failures |

Configure under PowerStore Manager → **Settings → Monitoring → SNMP**.

## Syslog / SIEM Integration

PowerStore can forward event logs to a syslog server for SIEM ingestion (Splunk, Microsoft Sentinel, QRadar, etc.):

- Syslog forwarding is configured in PowerStore Manager → **Settings → Monitoring → Syslog**
- Supported protocols: UDP (port 514), TCP (port 514 or 601), TLS (port 6514)
- Log level: INFO (operational events) and CRITICAL (faults and alerts) at minimum
- CEF (Common Event Format) output is not natively supported; raw syslog messages require parsing in the SIEM

```bash
# Verify syslog forwarding via REST API
curl -k -X GET "https://<mgmt-ip>/api/rest/remote_syslog" \
  -H "DELL-EMC-TOKEN: <token>"

# Add a syslog server
curl -k -X POST "https://<mgmt-ip>/api/rest/remote_syslog" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "192.168.10.200",
    "port": 514,
    "transport": "UDP",
    "enabled": true
  }'
```

## Active Directory / LDAP

PowerStore integrates with Active Directory for:

- **User authentication**: Unisphere/PowerStore Manager logins via AD credentials
- **NAS access control**: file-level permissions on SMB shares and NFS exports using AD users and groups

```bash
# Configure AD for management authentication via REST API
curl -k -X POST "https://<mgmt-ip>/api/rest/ldap" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "domain_name": "corp.example.com",
    "server_address": ["192.168.1.10", "192.168.1.11"],
    "protocol": "LDAP",
    "bind_user": "CN=svc-powerstore,OU=Service Accounts,DC=corp,DC=example,DC=com",
    "bind_password": "<password>",
    "user_search_path": "OU=Users,DC=corp,DC=example,DC=com",
    "group_search_path": "OU=Groups,DC=corp,DC=example,DC=com"
  }'
```

## Ansible

The Dell PowerStore Ansible collection (`dellemc.powerstore`) is available on Ansible Galaxy and provides modules for all major provisioning and management operations.

```bash
# Install the Dell PowerStore Ansible collection
ansible-galaxy collection install dellemc.powerstore

# Example: create a volume
- name: Create a PowerStore volume
  dellemc.powerstore.volume:
    array_ip: "192.168.10.50"
    user: "admin"
    password: "{{ powerstore_password }}"
    validate_certs: false
    vol_name: "app-db-prod-01"
    size: 500
    cap_unit: "GB"
    state: present
    volume_group_name: "app-db-vg"
```

## Terraform

The Dell PowerStore Terraform provider (`registry.terraform.io/dell/powerstore`) supports infrastructure-as-code for PowerStore resources:

```hcl
terraform {
  required_providers {
    powerstore = {
      source  = "dell/powerstore"
      version = ">= 1.0.0"
    }
  }
}

provider "powerstore" {
  username = var.powerstore_user
  password = var.powerstore_password
  endpoint = "https://192.168.10.50/api/rest"
  insecure = false
}

resource "powerstore_volume" "db_lun" {
  name              = "ora-prod-01"
  size              = 2199023255552   # 2 TiB in bytes
  description       = "Oracle production data LUN"
  volume_group_name = "oracle-vg"
}
```

---

## See also

- [Powerstore — How It Works](how-it-works/)
- [Powerstore — Design Standards](design-standards/)
