---
tags:
  - nutanix
  - architecture
  - integrations
description: "Prism Central multi-cluster registration, Active Directory/LDAP integration, backup product compatibility, monitoring with Prometheus and SNMP, Nutanix..."
---
# Nutanix — Integrations

<div class="kb-summary">
Prism Central multi-cluster registration, Active Directory/LDAP integration, backup product compatibility, monitoring with Prometheus and SNMP, Nutanix Files/Objects, and VMware vCenter plugin for ESXi-based clusters.

*Applies to: AOS 6.x · AHV*
</div>
![Nutanix — Integrations](../../../assets/virtualization-nutanix-architecture-integrations.svg)

---

## Prism Central Registration

Prism Central (PC) is the multi-cluster management layer. Each Prism Element (PE) cluster must be registered with PC.

**Register a cluster with Prism Central:**

```bash
# From Prism Element (PE) UI:
# Settings → Prism Central Registration → Register

# Via ncli:
ncli multicluster add-to-multicluster \
  external-ip-address-or-svm-ips=<prism-central-ip> \
  username=admin \
  password=<pc-password>
```


```text title="Expected output"
Registering cluster to Prism Central...
Cluster UUID: 00051234-1234-1234-1234-123456789abc
Prism Central IP: 10.45.67.89
Registration Status: SUCCEEDED
Cluster Name: PHX-Cluster-01
Multicluster UUID: 00051234-5678-9abc-def0-123456789abc
Sync Status: IN_SYNC
Last Sync Time: 2024-01-15 14:32:18
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused to Prism Central IP 10.45.67.89:9440` | Verify Prism Central is running and accessible on the network, and confirm the IP address is correct. |
    | `Error: Authentication failed for user 'admin'` | Ensure the Prism Central admin password is correct and the user account has cluster registration permissions. |
    | `Error: Cluster already registered to multicluster UUID 00051234-5678-9abc-def0-123456789abc` | Unregister the cluster first using `ncli multicluster remove-from-multicluster` before re-registering. |
**Verify registration:**

```bash
ncli multicluster get-cluster-state
```


```text title="Expected output"
Cluster UUID                 : 00051234-1234-1234-1234-123456789abc
Cluster Name                 : prod-cluster-01
Cluster Incarnation ID       : 1702834567890123
Cluster Version              : el7.9-5.20.4.1
Cluster Redundancy Factor    : 2
Cluster Timezone             : UTC
Cluster External Subnet Mask : 255.255.255.0
Cluster External Gateway     : 10.20.30.1
NTP Server List              : 10.20.30.50
Domain Name Server List      : 8.8.8.8, 8.8.4.4
Cluster Virtual IP           : 10.20.30.100
Cluster Multicast Address    : 224.0.0.1
Cluster Multicast Mask       : 255.255.255.0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused (111)` | Verify the Prism Central or cluster management service is running with `systemctl status nutanix_cluster_manager` and check network connectivity to the cluster IP. |
    | `Error: Authentication failed: Invalid credentials` | Ensure you are authenticated with valid Nutanix credentials using `ncli user whoami` or re-authenticate with `ncli -u admin -p <password>`. |
**Expected output:** `Cluster State: Connected`

---

## Active Directory / LDAP Integration

### Prism Central AD Integration

```text
Prism Central → Settings → Authentication → Directory Services → Add Directory
  Type: Active Directory
  Domain: corp.local
  Directory URL: ldap://dc01.corp.local:389 (or ldaps://... port 636)
  Domain search path: DC=corp,DC=local
  Service account: svc-nutanix@corp.local + password
```

**Role mapping (Prism Central):**

| AD Group | Prism Role |
|---|---|
| `nutanix-admins` | Prism Admin |
| `nutanix-operators` | Prism Operator |
| `nutanix-viewers` | Prism Viewer |

Add role mappings: Prism Central → Settings → Role Mappings → Add Mapping

**Verify AD auth:**

```bash
# From any CVM:
ncli authconfig get-directory-services
# Check: Status = Connected
```


```text title="Expected output"
Directory Services Configuration
=================================
   Directory Service Type: Active Directory
   Directory Service Name: corp.example.com
   Status: Connected
   Domain: CORP.EXAMPLE.COM
   Base DN: cn=Users,dc=corp,dc=example,dc=com
   Admin User: administrator@corp.example.com
   Last Sync Time: 2024-01-15 14:32:18
   Connection Timeout (sec): 30
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Status: Disconnected` | Verify network connectivity to the domain controller and confirm firewall rules allow port 389 (LDAP) or 636 (LDAPS) from the CVM. |
    | `Error: Directory service configuration not found` | Run `ncli authconfig add-directory-services` to configure directory services before attempting to query status. |
    | `Connection timeout to LDAP server` | Check DNS resolution for the domain controller hostname and ensure the CVM can reach it with `ping` or `nslookup`. |
### LDAP Integration (non-AD)

Supported for OpenLDAP, FreeIPA, and other LDAP-compliant directories. Use `ldaps://` (TLS) for production. Configure the same way as AD but set Type = OpenLDAP and provide the user/group search base DN.

---

## Backup Integrations

Nutanix AOS provides crash-consistent and app-consistent snapshots that backup products consume via API.

| Product | Integration method | Notes |
|---|---|---|
| Veeam Backup & Replication | AHV Backup Proxy (Nutanix plugin) | Full + incremental via changed-block tracking |
| Commvault | Nutanix REST API (v2/v3) | Snapshot-based; IntelliSnap support |
| Zerto | Replication appliance on AHV | Continuous replication; near-zero RPO |
| HYCU | Native Nutanix integration | Application-aware backup for AHV VMs |
| Veritas NetBackup | NetBackup for AHV | Standard Nutanix AHV API |

**Nutanix native protection (no third-party license):**
- **Protection Domains** (legacy): define VM groups, schedule snapshots, replicate to another cluster
- **Nutanix DR** (PC-managed): policy-based replication, linear/non-linear snapshot schedules, failover runbooks

---

## Monitoring

### Prometheus + Nutanix Exporter

The Nutanix community Prometheus exporter exposes cluster metrics via `/metrics` endpoint.

```bash
# Run as a container or VM
docker run -d \
  -e NUTANIX_HOST=<prism-central-ip> \
  -e NUTANIX_USERNAME=admin \
  -e NUTANIX_PASSWORD=<password> \
  -p 9408:9408 \
  ghcr.io/nutanix/nutanix-exporter:latest
```


```text title="Expected output"
Unable to find image 'ghcr.io/nutanix/nutanix-exporter:latest' locally
latest: Pulling from nutanix/nutanix-exporter
a1d0c7532f0e: Pull complete
b3fd9c332a9b: Pull complete
e8614d09c7b7: Pull complete
Digest: sha256:8f4c2a9b1e7d3c5f6a2b8e9c0d1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e
Status: Downloaded newer image for ghcr.io/nutanix/nutanix-exporter:latest
7f8e9d0c1b2a3f4e5d6c7b8a9f0e1d2c3b4a5f6e7d8c9b0a1f2e3d4c5b6a7f
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error response from daemon: Get "https://ghcr.io/v2/": net/http: request canceled` | Verify network connectivity and ensure your Docker daemon can reach ghcr.io, or use a private registry mirror. |
    | `Error: No such image: ghcr.io/nutanix/nutanix-exporter:latest` | Pull the image first with `docker pull ghcr.io/nutanix/nutanix-exporter:latest` before running the container. |
    | `Error response from daemon: driver failed programming external connectivity on endpoint: Bind for 0.0.0.0:9408 failed: port is already allocated` | Change the host port mapping to an available port (e.g., `-p 9409:9408`) or stop the container using port 9408. |
**Key metrics exposed:**
- `nutanix_cluster_cpu_usage_ppm` — cluster CPU utilisation (ppm = parts per million)
- `nutanix_cluster_memory_usage_bytes` — memory utilisation
- `nutanix_storage_usage_bytes` / `nutanix_storage_capacity_bytes` — storage fill
- `nutanix_host_cpu_usage_ppm` — per-node CPU
- `nutanix_vm_cpu_ready_time_ppm` — VM CPU ready time (latency indicator)

### SNMP

Nutanix supports SNMP v2c and v3 for alert forwarding to existing NMS platforms.

```text
Prism Element → Settings → SNMP → Enable SNMP
  Version: v3 (recommended)
  Traps: configure trap receiver IP and community string
  MIB: download from Prism Settings → SNMP → Download MIB
```

### Email Alerts

```text
Prism Element → Settings → SMTP → Configure SMTP server
Prism Element → Settings → Alert Email → Add recipient
Alert severity: Critical / Warning / Info
```

---

## Nutanix Files (Scale-Out NFS/SMB)

Nutanix Files runs as a cluster of File Server VMs (FSVMs) on AHV, providing NFS v4 and SMB 2/3 shares using capacity from the AOS datastore.

**Deploy from Prism Central:**
```text
Prism Central → Files → Create File Server
  Name: nutanix-files
  Internal IPs: 3 IPs on storage network (one per FSVM)
  External IPs: floating IPs on client network
  Storage: select container; allocate initial capacity
```

**Create shares:**
```text
Prism Element → Files → Shares → Create
  Type: SMB (Windows) or NFS (Linux)
  Protocol: SMB 3 / NFSv4
  Authentication: AD passthrough (SMB), Kerberos or AUTH_SYS (NFS)
```

---

## Nutanix Objects (S3-Compatible)

Nutanix Objects provides S3-compatible object storage on AHV. Used for backup targets, media, analytics cold storage.

**Deploy from Prism Central:**
```text
Prism Central → Objects → Create Object Store
  Name: nutanix-objects
  Worker nodes: 3+ (scales horizontally)
  Storage: select container and initial capacity
  Domain: corp.local (for AD-integrated access)
```

**Access:**
```bash
# S3 CLI using standard AWS endpoint syntax
aws s3 ls s3://my-bucket/ \
  --endpoint-url https://<objects-ip>:443 \
  --no-verify-ssl
```


```text title="Expected output"
2024-01-15 09:23:14        0 PRE backups/
2024-01-15 09:18:47        0 PRE logs/
2024-01-15 09:15:32   524288 config.tar.gz
2024-01-15 09:12:01  1048576 database-snapshot.sql
2024-01-15 08:45:22        0 PRE archives/
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unable to locate credentials` | Configure AWS credentials via `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. |
    | `SSL: CERTIFICATE_VERIFY_FAILED` | Ensure the `--no-verify-ssl` flag is present, or add the Nutanix Objects certificate to your system's CA bundle. |
    | `An error occurred (InvalidEndpointAddress) when calling the ListBucket operation: Could not connect to the endpoint URL` | Verify the Objects IP is correct, reachable from your client, and that port 443 is open in firewall rules. |
---

## VMware vCenter Plugin (ESXi-Based Clusters)

If the Nutanix cluster runs ESXi (not AHV), the Nutanix vCenter Plugin extends vCenter with Nutanix management:

```text
Install: Prism Element → Settings → vCenter Registration → Register vCenter
  vCenter FQDN: vcenter.corp.local
  Username: svc-nutanix@corp.local
  Password: <password>
```

After registration:
- vCenter Datastores panel shows Nutanix containers
- vCenter → Hosts shows Nutanix hardware health (disk, CVM status)
- VM snapshots route through Nutanix snapshot API (crash-consistent)

---

## Calm (Infrastructure Automation)

Nutanix Calm is a blueprint-based automation engine available through Prism Central.

- **Blueprints**: define multi-VM application topologies (DB + web + LB) as infrastructure as code
- **Providers**: AHV, ESXi, AWS, Azure, GCP, bare metal
- **Runbooks**: scripted operations (day-2 tasks, remediation)
- **Marketplace**: publish/subscribe blueprints across teams

---

## See also

- [Nutanix — How It Works](../how-it-works/)
- [Nutanix — Deploy](../../deploy/)
